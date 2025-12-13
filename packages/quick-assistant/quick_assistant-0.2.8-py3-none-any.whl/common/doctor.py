import os
import sys
from pathlib import Path
from typing import Union
from importlib.metadata import version as get_pkg_version

from common.base import BaseFrozen
from common.result import Result, Ok, Err
from rich.console import Console


PACKAGE_NAME = "quick-assistant"


class VersionRetrievalError(BaseFrozen):
    message: str


class PathCheckError(BaseFrozen):
    message: str


DoctorError = Union[VersionRetrievalError, PathCheckError]


class DiagnosticsInfo(BaseFrozen):
    version: str
    platform: str
    python_version: str
    executable: str


class PathIssue(BaseFrozen):
    name: str
    path: str


class DoctorResult(BaseFrozen):
    info: DiagnosticsInfo
    issues: tuple[PathIssue, ...]


def get_version() -> Result[VersionRetrievalError, str]:
    try:
        return Result.ok(get_pkg_version(PACKAGE_NAME))
    except Exception as e:
        return Result.err(VersionRetrievalError(message=str(e)))


def get_diagnostics_info() -> Result[DoctorError, DiagnosticsInfo]:
    version_result = get_version()
    match version_result.inner:
        case Err(error=e):
            return Result.err(e)
        case Ok(value=ver):
            return Result.ok(
                DiagnosticsInfo(
                    version=ver, platform=sys.platform, python_version=sys.version.split()[0], executable=sys.executable
                )
            )


def check_windows_path() -> Result[PathCheckError, tuple[PathIssue, ...]]:
    scripts_dir = Path(sys.executable).parent / "Scripts"
    pipx_bin = Path.home() / ".local" / "bin"
    path_env = os.environ.get("PATH", "")

    issues: list[PathIssue] = []

    if scripts_dir.exists() and str(scripts_dir).lower() not in path_env.lower():
        issues.append(PathIssue(name="pip Scripts", path=str(scripts_dir)))

    if pipx_bin.exists() and str(pipx_bin).lower() not in path_env.lower():
        issues.append(PathIssue(name="pipx bin", path=str(pipx_bin)))

    return Result.ok(tuple(issues))


def run_doctor() -> Result[DoctorError, DoctorResult]:
    info_result = get_diagnostics_info()
    match info_result.inner:
        case Err(error=e):
            return Result.err(e)
        case Ok(value=info):
            pass

    if sys.platform == "win32":
        issues_result = check_windows_path()
        match issues_result.inner:
            case Err(error=e):
                return Result.err(e)
            case Ok(value=issues):
                return Result.ok(DoctorResult(info=info, issues=issues))

    return Result.ok(DoctorResult(info=info, issues=()))


def error_to_message(error: DoctorError) -> str:
    match error:
        case VersionRetrievalError(message=m):
            return f"Failed to retrieve version: {m}"
        case PathCheckError(message=m):
            return f"PATH check failed: {m}"


def _print_diagnostics(console: Console, info: DiagnosticsInfo) -> None:
    console.print("Quick Assistant - System Diagnostics\n")
    console.print(f"Version: {info.version}")
    console.print(f"Platform: {info.platform}")
    console.print(f"Python: {info.python_version}")
    console.print(f"Executable: {info.executable}")


def _print_issues(console: Console, issues: tuple[PathIssue, ...]) -> None:
    console.print("\nPATH issues detected:\n")
    for issue in issues:
        console.print(f"  - {issue.name} not in PATH: {issue.path}")

    console.print("\nRemediation:")
    console.print("  1. For pipx installations:")
    console.print("     pipx ensurepath")
    console.print("")
    console.print("  2. For pip installations, add to PATH manually:")
    scripts_dir = Path(sys.executable).parent / "Scripts"
    console.print(f'     setx PATH "%PATH%;{scripts_dir}"')
    console.print("")
    console.print("  3. Restart your terminal after making changes.")


def _print_success(console: Console) -> None:
    if sys.platform == "win32":
        console.print("\nPATH appears correctly configured.")
    else:
        console.print("\nPATH configuration typically works out-of-the-box on Unix systems.")


def execute_doctor() -> int:
    console = Console()
    result = run_doctor()

    match result.inner:
        case Err(error=e):
            console.print(f"[red]{error_to_message(e)}[/red]")
            return 1
        case Ok(value=doctor_result):
            _print_diagnostics(console, doctor_result.info)

            if doctor_result.issues:
                _print_issues(console, doctor_result.issues)
                return 1

            _print_success(console)
            return 0
