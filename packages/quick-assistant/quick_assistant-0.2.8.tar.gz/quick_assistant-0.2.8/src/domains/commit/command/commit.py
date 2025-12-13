import os
import subprocess
import tempfile

from typing import Any, Dict, Literal, Optional, Union
from google import genai
from google.genai import types
from common.base import BaseFrozen, BaseFrozenArbitrary, BaseSerializable
from common.command.base_command import BaseCommand
from common.command.base_command_handler import BaseCommandHandler
from common.command.execute_command_handler import json_response, execute_command_handler
from common.config import CommitConvention, load_config, get_api_key
from common.loading import spinner
from common.prompts import prompt_commit_message, select_option, text_input
from common.result import Result, Ok, Err, async_try_catch
from rich.console import Console


Action = Literal["generate"]
Selection = Literal["commit", "commit_push", "regenerate", "adjust", "cancel"]

PRIMARY_MODEL = "models/gemini-flash-latest"
FALLBACK_MODEL = "models/gemini-flash-lite-latest"


class MissingApiKey(BaseFrozen):
    pass


class NotGitRepo(BaseFrozen):
    pass


class GitError(BaseFrozen):
    message: str


class NoStagedChanges(BaseFrozen):
    pass


class EmptyAIResponse(BaseFrozen):
    pass


class UnsupportedAction(BaseFrozen):
    action: str


CommitError = Union[MissingApiKey, NotGitRepo, GitError, NoStagedChanges, EmptyAIResponse, UnsupportedAction]


class CommitState(BaseFrozen):
    api_key: str
    cwd: str
    diff: str
    message: str
    convention: CommitConvention = CommitConvention.IMPERATIVE
    custom_template: Optional[str] = None

    def with_message(self, new_message: str) -> "CommitState":
        return self.model_copy(update={"message": new_message})


class RegenerateSignal(BaseFrozenArbitrary):
    state: CommitState


class AdjustSignal(BaseFrozenArbitrary):
    state: CommitState


LoopResult = Union["CommandResponse", RegenerateSignal, AdjustSignal]


class Command(BaseCommand):
    action: str


class CommandResponse(BaseSerializable):
    message: str
    commit_message: Optional[str] = None
    action: Optional[str] = None
    git_output: Optional[str] = None


def validate_api_key() -> Result[MissingApiKey, str]:
    result = get_api_key()
    match result.inner:
        case Ok(value=key):
            return Result.ok(key)
        case Err():
            return Result.err(MissingApiKey())


def validate_git_repo(path: str) -> Result[NotGitRepo, str]:
    result = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], capture_output=True, text=True, cwd=path)
    if result.returncode != 0:
        return Result.err(NotGitRepo())
    return Result.ok(path)


def get_staged_diff(path: str) -> Result[Union[GitError, NoStagedChanges], str]:
    result = subprocess.run(["git", "diff", "--staged"], capture_output=True, cwd=path)
    if result.returncode != 0:
        return Result.err(
            GitError(message=result.stderr.decode("utf-8", errors="replace").strip() or "Failed to get staged changes")
        )
    stdout = result.stdout.decode("utf-8", errors="replace")
    if not stdout.strip():
        return Result.err(NoStagedChanges())
    return Result.ok(stdout)


def validate_action(action: str) -> Result[UnsupportedAction, Action]:
    if action != "generate":
        return Result.err(UnsupportedAction(action=action))
    return Result.ok("generate")


async def generate_message(
    api_key: str,
    diff: str,
    convention: CommitConvention = CommitConvention.IMPERATIVE,
    custom_template: Optional[str] = None,
) -> Result[Union[Exception, EmptyAIResponse], str]:
    async def attempt(model: str):
        return await async_try_catch(lambda: _generate_message_impl(api_key, diff, convention, custom_template, model))

    result = await attempt(PRIMARY_MODEL)
    match result.inner:
        case Ok(value=msg):
            if not msg.strip():
                return Result.err(EmptyAIResponse())
            return Result.ok(msg)
        case Err(error=e):
            if is_rate_limit_error(e):
                console = Console()
                console.print("[yellow]Rate limited. Trying fallback model...[/yellow]")
                fallback_result = await attempt(FALLBACK_MODEL)
                match fallback_result.inner:
                    case Ok(value=msg):
                        if not msg.strip():
                            return Result.err(EmptyAIResponse())
                        return Result.ok(msg)
                    case Err(error=fallback_err):
                        return Result.err(fallback_err)
            return Result.err(e)


async def _generate_message_impl(
    api_key: str,
    diff: str,
    convention: CommitConvention,
    custom_template: Optional[str],
    model: str = PRIMARY_MODEL,
) -> str:
    with spinner("Generating…", spinner_style="dots"):
        response = await genai.Client(api_key=api_key).aio.models.generate_content(
            model=model,
            contents=diff,
            config=types.GenerateContentConfig(
                system_instruction=prompt_commit_message(diff, convention, custom_template),
                response_mime_type="text/plain",
            ),
        )
    return _extract_text(response)


async def refine_message(
    api_key: str, current_message: str, adjustment: str, diff: str
) -> Result[Union[Exception, EmptyAIResponse], str]:
    async def attempt(model: str):
        return await async_try_catch(lambda: _refine_message_impl(api_key, current_message, adjustment, diff, model))

    result = await attempt(PRIMARY_MODEL)
    match result.inner:
        case Ok(value=msg):
            if not msg.strip():
                return Result.err(EmptyAIResponse())
            return Result.ok(msg)
        case Err(error=e):
            if is_rate_limit_error(e):
                console = Console()
                console.print("[yellow]Rate limited. Trying fallback model...[/yellow]")
                fallback_result = await attempt(FALLBACK_MODEL)
                match fallback_result.inner:
                    case Ok(value=msg):
                        if not msg.strip():
                            return Result.err(EmptyAIResponse())
                        return Result.ok(msg)
                    case Err(error=fallback_err):
                        return Result.err(fallback_err)
            return Result.err(e)


async def _refine_message_impl(
    api_key: str, current_message: str, adjustment: str, diff: str, model: str = PRIMARY_MODEL
) -> str:
    system = (
        "You revise commit messages. Use the diff and the user's adjustment to produce a polished commit message. "
        "Preserve required formatting rules: SMALL=single line; MEDIUM/LARGE=title, blank line, bullets prefixed with '- '."
    )
    contents = (
        f"<diff>\n{diff}\n</diff>\n<current>\n{current_message}\n</current>\n<adjustment>\n{adjustment}\n</adjustment>"
    )
    with spinner("Refining…", spinner_style="dots"):
        response = await genai.Client(api_key=api_key).aio.models.generate_content(
            model=model,
            contents=contents,
            config=types.GenerateContentConfig(system_instruction=system, response_mime_type="text/plain"),
        )
    return _extract_text(response)


def _extract_text(response: types.GenerateContentResponse) -> str:
    candidates = getattr(response, "candidates", ()) or ()
    parts = tuple(p for c in candidates for p in (getattr(getattr(c, "content", None), "parts", ()) or ()))
    return "".join(text for p in parts if (text := getattr(p, "text", None)))


def is_rate_limit_error(error: Exception) -> bool:
    error_str = str(error).lower()
    return "429" in error_str or "resource_exhausted" in error_str


def perform_commit(message: str, cwd: str) -> Result[GitError, str]:
    with tempfile.NamedTemporaryFile("w", delete=False) as tmp:
        tmp.write(message)
        tmp_path = tmp.name
    try:
        result = subprocess.run(["git", "commit", "-F", tmp_path], capture_output=True, text=True, cwd=cwd)
        output = (result.stdout or "") + (result.stderr or "")
        if result.returncode != 0:
            return Result.err(GitError(message=output.strip() or "Commit failed"))
        stats_only = "\n".join(line for line in output.strip().split("\n") if not line.startswith("["))
        return Result.ok("\n" + stats_only + "\n")
    finally:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass


def perform_push(cwd: str) -> Result[GitError, str]:
    result = subprocess.run(["git", "push"], capture_output=True, text=True, cwd=cwd)
    output = (result.stdout or "") + (result.stderr or "")
    if result.returncode != 0:
        return Result.err(GitError(message=output.strip() or "Push failed"))
    return Result.ok(output)


def handle_selection(selection: Selection, state: CommitState) -> Result[CommitError, LoopResult]:
    match selection:
        case "commit":
            commit_result = perform_commit(state.message, state.cwd)
            match commit_result.inner:
                case Err(error=git_err):
                    return Result[CommitError, LoopResult].err(git_err)
                case Ok(value=commit_output):
                    return Result[CommitError, LoopResult].ok(
                        CommandResponse(
                            message="commit", commit_message=state.message, action="commit", git_output=commit_output
                        )
                    )
        case "commit_push":
            commit_result = perform_commit(state.message, state.cwd)
            match commit_result.inner:
                case Err(error=git_err):
                    return Result[CommitError, LoopResult].err(git_err)
                case Ok(value=commit_output):
                    push_result = perform_push(state.cwd)
                    match push_result.inner:
                        case Err(error=push_err):
                            return Result[CommitError, LoopResult].err(push_err)
                        case Ok(value=push_output):
                            return Result[CommitError, LoopResult].ok(
                                CommandResponse(
                                    message="commit_push",
                                    commit_message=state.message,
                                    action="commit_push",
                                    git_output=f"{commit_output}{push_output}",
                                )
                            )
        case "regenerate":
            return Result.ok(RegenerateSignal(state=state))
        case "adjust":
            return Result.ok(AdjustSignal(state=state))
        case "cancel":
            return Result.ok(CommandResponse(message="cancelled", commit_message=state.message, action="cancel"))


async def interaction_loop(state: CommitState, console: Console) -> Result[CommitError, CommandResponse]:
    console.print("")
    console.print(state.message)
    console.print("")

    raw_selection = await select_option(
        "Select action:",
        [
            ("Commit & Push", "commit_push"),
            ("Commit", "commit"),
            ("Regenerate", "regenerate"),
            ("Adjust", "adjust"),
            ("Cancel", "cancel"),
        ],
    )

    selection: Selection
    if raw_selection in ("commit", "commit_push", "regenerate", "adjust", "cancel"):
        selection = raw_selection  # type: ignore[assignment]
    else:
        selection = "cancel"
    result = handle_selection(selection, state)

    match result.inner:
        case Ok(value=loop_result):
            match loop_result:
                case RegenerateSignal(state=s):
                    gen_result = await generate_message(s.api_key, s.diff, s.convention, s.custom_template)
                    match gen_result.inner:
                        case Ok(value=new_msg):
                            return await interaction_loop(s.with_message(new_msg), console)
                        case Err(error=e):
                            console.print(f"[red]Generation failed: {e}[/red]")
                            return await interaction_loop(s, console)
                case AdjustSignal(state=s):
                    adj = await text_input("What adjustments would you like?")
                    if not adj:
                        return await interaction_loop(s, console)
                    refine_result = await refine_message(s.api_key, s.message, adj, s.diff)
                    match refine_result.inner:
                        case Ok(value=new_msg):
                            return await interaction_loop(s.with_message(new_msg), console)
                        case Err(error=e):
                            console.print(f"[red]Refinement failed: {e}[/red]")
                            return await interaction_loop(s, console)
                case CommandResponse() as response:
                    return Result.ok(response)
        case Err(error=e):
            return Result.err(e)


async def execute_commit_flow(action: str, console: Console) -> Result[CommitError, CommandResponse]:
    action_result = validate_action(action)
    match action_result.inner:
        case Err(error=action_err):
            return Result.err(action_err)
        case Ok():
            pass

    api_key_result = validate_api_key()
    match api_key_result.inner:
        case Err(error=key_err):
            return Result.err(key_err)
        case Ok(value=api_key):
            pass

    convention = CommitConvention.IMPERATIVE
    custom_template: Optional[str] = None
    config_result = load_config()
    match config_result.inner:
        case Ok(value=config):
            convention = config.commit_convention
            custom_template = config.custom_template
        case Err():
            pass

    cwd = os.getcwd()
    repo_result = validate_git_repo(cwd)
    match repo_result.inner:
        case Err(error=repo_err):
            return Result.err(repo_err)
        case Ok():
            pass

    diff_result = get_staged_diff(cwd)
    match diff_result.inner:
        case Err(error=diff_err):
            return Result.err(diff_err)
        case Ok(value=diff):
            pass

    gen_result = await generate_message(api_key, diff, convention, custom_template)
    match gen_result.inner:
        case Err(error=gen_err):
            match gen_err:
                case EmptyAIResponse():
                    return Result.err(gen_err)
                case _:
                    return Result.err(GitError(message=str(gen_err)))
        case Ok(value=message):
            pass

    initial_state = CommitState(
        api_key=api_key, cwd=cwd, diff=diff, message=message, convention=convention, custom_template=custom_template
    )
    return await interaction_loop(initial_state, console)


def error_to_response(error: CommitError) -> tuple[Dict[str, Any], int]:
    match error:
        case MissingApiKey():
            msg = "API key not configured. Run 'quick setup' to configure."
        case NotGitRepo():
            msg = "Not a git repository. Initialize with 'git init' or navigate to a git project."
        case GitError(message=m):
            msg = f"Git error: {m}"
        case NoStagedChanges():
            msg = "No staged changes found. Use 'git add <file>' to stage files before generating a commit."
        case EmptyAIResponse():
            msg = "Empty response from commit message generation"
        case UnsupportedAction(action=a):
            msg = f"Unsupported commit action: '{a}'. Use 'generate'."

    return {"error": {"message": msg}}, 400


class Handler(BaseCommandHandler[Command]):
    async def handle_command(self, command: Command) -> tuple[Dict[str, Any], int]:
        console = Console()
        result = await execute_commit_flow(command.action, console)

        match result.inner:
            case Ok(value=response):
                status = 200 if response.message in ("commit", "commit_push", "cancelled") else 400
                if response.git_output:
                    console.print(response.git_output)
                return json_response(response, status)
            case Err(error=e):
                return error_to_response(e)


async def execute_commit(action: str = "generate") -> int:
    console = Console()

    try:
        request_data = {"action": action}

        response, status_code = await execute_command_handler(Command, request_data, Handler)

        if status_code != 200:
            error_msg = response.get("error", {}).get("message", "Unknown error")
            console.print(f"[red]{error_msg}[/red]")

        return 0 if status_code == 200 else 1

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        return 1
