#!/usr/bin/env python3

import sys
import asyncio

from typing import List, Optional, Union

from dotenv import load_dotenv
from rich.console import Console

from common.base import BaseFrozen
from common.result import Result, Ok, Err
from common.updater import check_and_update
from common.arguments import CommandType, ParsedArgs, create_parser
from common.config import is_ready
from common.doctor import execute_doctor
from common.updater import execute_update
from domains.commit.command.commit import execute_commit
from domains.setup.command.setup import execute_setup


class UserCancelled(BaseFrozen):
    pass


class AppError(BaseFrozen):
    message: str


AppErrorType = Union[UserCancelled, AppError]


def error_to_message(error: AppErrorType) -> str:
    match error:
        case UserCancelled():
            return "Operation cancelled by user."
        case AppError(message=m):
            return f"Error: {m}"


def initialize() -> None:
    """Load environment variables."""
    load_dotenv()


def run_command(command_type: CommandType) -> int:
    """Execute the appropriate command handler."""
    match command_type:
        case CommandType.COMMIT:
            return asyncio.run(execute_commit("generate"))
        case CommandType.UPDATE:
            return execute_update()
        case CommandType.SETUP:
            return asyncio.run(execute_setup())
        case CommandType.DOCTOR:
            return execute_doctor()
        case CommandType.HELP:
            return 1


def run(args: Optional[List[str]] = None) -> Result[AppErrorType, int]:
    """Main application entry point."""
    parser = create_parser()

    try:
        namespace = parser.parse_args(args)
    except SystemExit:
        return Result.ok(1)

    parsed_args = ParsedArgs(command=getattr(namespace, "command", None))
    command_type = parsed_args.get_command_type()

    if not is_ready() and command_type not in (CommandType.SETUP, CommandType.HELP, CommandType.DOCTOR):
        return Result.ok(asyncio.run(execute_setup()))

    if command_type == CommandType.HELP:
        parser.print_help()
        return Result.ok(1)

    return Result.ok(run_command(command_type))


def safe_run(args: Optional[List[str]] = None) -> int:
    """Wrapper that catches exceptions and returns exit code."""
    console = Console()

    try:
        result = run(args)
        match result.inner:
            case Ok(value=exit_code):
                return exit_code
            case Err(error=e):
                console.print(f"[red]{error_to_message(e)}[/red]")
                return 1
    except KeyboardInterrupt:
        console.print("\n\nOperation cancelled by user.")
        return 1
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        return 1


def main() -> int:
    initialize()
    check_and_update()
    return safe_run(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())
