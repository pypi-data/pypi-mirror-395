from typing import Any, Dict, Optional, Union

from google import genai
from rich.console import Console

from common.base import BaseFrozen, BaseSerializable
from common.command.base_command import BaseCommand
from common.command.base_command_handler import BaseCommandHandler
from common.command.execute_command_handler import json_response, execute_command_handler
from common.config import CommitConvention, Config, ConfigWriteError, save_config
from common.loading import spinner
from common.prompts import select_option, password_input
from common.result import Result, Ok, Err, async_try_catch


class InvalidApiKey(BaseFrozen):
    message: str


class SetupCancelled(BaseFrozen):
    pass


SetupError = Union[InvalidApiKey, ConfigWriteError, SetupCancelled]


class SetupResponse(BaseSerializable):
    message: str
    config_path: Optional[str] = None


class Command(BaseCommand):
    pass


CONVENTION_OPTIONS = [
    ("Conventional Commits (feat:, fix:, refactor:)", "conventional"),
    ("Imperative (add, fix, update)", "imperative"),
    ("Custom template", "custom"),
]


async def prompt_convention(console: Console) -> Optional[CommitConvention]:
    raw = await select_option("Select commit convention:", CONVENTION_OPTIONS)
    if raw is None:
        return None
    match raw:
        case "conventional":
            return CommitConvention.CONVENTIONAL
        case "imperative":
            return CommitConvention.IMPERATIVE
        case "custom":
            return CommitConvention.CUSTOM
        case _:
            return None


async def prompt_custom_template(console: Console) -> Optional[str]:
    from common.prompts import text_input

    console.print("\n[dim]Enter your custom commit message template.[/dim]")
    console.print("[dim]Use {diff} as placeholder for the git diff.[/dim]\n")
    return await text_input("Custom template:")


async def prompt_api_key() -> Optional[str]:
    return await password_input("Enter your GOOGLE_API_KEY:")


async def validate_api_key(api_key: str) -> Result[InvalidApiKey, str]:
    result = await async_try_catch(lambda: _validate_api_key_impl(api_key))
    match result.inner:
        case Ok():
            return Result.ok(api_key)
        case Err(error=e):
            return Result.err(InvalidApiKey(message=str(e)))


async def _validate_api_key_impl(api_key: str) -> None:
    with spinner("Validating API key...", spinner_style="dots"):
        await genai.Client(api_key=api_key).aio.models.generate_content(
            model="models/gemini-flash-latest", contents="Say 'ok' in one word."
        )


async def execute_setup_flow(console: Console) -> Result[SetupError, SetupResponse]:
    console.print("\n[bold]Quick Assistant Setup[/bold]\n")

    convention = await prompt_convention(console)
    if convention is None:
        return Result.err(SetupCancelled())

    custom_template: Optional[str] = None
    if convention == CommitConvention.CUSTOM:
        custom_template = await prompt_custom_template(console)
        if custom_template is None:
            return Result.err(SetupCancelled())

    console.print("")
    api_key = await prompt_api_key()
    if api_key is None or not api_key.strip():
        return Result.err(SetupCancelled())

    console.print("")
    validate_result = await validate_api_key(api_key.strip())
    match validate_result.inner:
        case Err(error=e):
            return Result.err(e)
        case Ok(value=validated_key):
            pass

    config = Config(api_key=validated_key, commit_convention=convention, custom_template=custom_template)

    save_result = save_config(config)
    match save_result.inner:
        case Err(error=write_err):
            return Result.err(write_err)
        case Ok():
            pass

    from common.config import get_config_path

    return Result.ok(SetupResponse(message="setup_complete", config_path=str(get_config_path())))


def error_to_response(error: SetupError) -> tuple[Dict[str, Any], int]:
    match error:
        case InvalidApiKey(message=m):
            msg = f"Invalid API key: {m}"
        case ConfigWriteError(message=m):
            msg = f"Failed to save config: {m}"
        case SetupCancelled():
            msg = "Setup cancelled"

    return {"error": {"message": msg}}, 400


class Handler(BaseCommandHandler[Command]):
    async def handle_command(self, command: Command) -> tuple[Dict[str, Any], int]:
        console = Console()
        result = await execute_setup_flow(console)

        match result.inner:
            case Ok(value=response):
                console.print("\n[green]Setup complete![/green]")
                console.print(f"[dim]Configuration saved to {response.config_path}[/dim]\n")
                return json_response(response, 200)
            case Err(error=e):
                return error_to_response(e)


async def execute_setup() -> int:
    console = Console()

    try:
        request_data: Dict[str, Any] = {}
        response, status_code = await execute_command_handler(Command, request_data, Handler)

        if status_code != 200:
            error_msg = response.get("error", {}).get("message", "Unknown error")
            if error_msg != "Setup cancelled":
                console.print(f"[red]{error_msg}[/red]")

        return 0 if status_code == 200 else 1

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        return 1
