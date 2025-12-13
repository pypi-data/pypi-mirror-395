import argparse

from typing import Optional
from pydantic import BaseModel, ConfigDict
from enum import Enum


class CommandType(Enum):
    COMMIT = "commit"
    UPDATE = "update"
    SETUP = "setup"
    DOCTOR = "doctor"
    HELP = "help"


class ParsedArgs(BaseModel):
    model_config = ConfigDict(frozen=True)

    command: Optional[str] = None

    def get_command_type(self) -> CommandType:
        match self.command:
            case "commit":
                return CommandType.COMMIT
            case "update":
                return CommandType.UPDATE
            case "setup":
                return CommandType.SETUP
            case "doctor":
                return CommandType.DOCTOR
            case _:
                return CommandType.HELP


class QuickCLIConfig:
    prog = "quick"
    description = "Quick Assistant - CLI tool for productivity"
    epilog = "Examples:\n    quick commit\n    quick update"


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=QuickCLIConfig.prog,
        description=QuickCLIConfig.description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=QuickCLIConfig.epilog,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser("commit", help="Generate a commit message")
    subparsers.add_parser("update", help="Update quick-assistant to the latest version")
    subparsers.add_parser("setup", help="Configure quick-assistant")
    subparsers.add_parser("doctor", help="Diagnose installation and PATH issues")

    return parser
