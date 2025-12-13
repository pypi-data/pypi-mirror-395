import json
import subprocess
import sys
import time
import requests

from pathlib import Path
from importlib.metadata import PackageNotFoundError, version
from typing import Literal, Union

from packaging.version import Version

from rich.console import Console

from common.base import BaseFrozen
from common.config import get_config_dir
from common.result import Err, Ok, Result, try_catch


PACKAGE_NAME = "quick-assistant"
PYPI_URL = f"https://pypi.org/pypi/{PACKAGE_NAME}/json"
CHECK_INTERVAL = 3600 * 24
CACHE_FILE = get_config_dir() / "update-cache.json"
UV_TOOL_PATH_PART = "uv"
UV_TOOL_NAME = "quick-assistant"


class NetworkError(BaseFrozen):
    url: str
    message: str


class VersionCheckError(BaseFrozen):
    message: str


class PackageNotInstalled(BaseFrozen):
    package: str


class SubprocessError(BaseFrozen):
    command: str
    exit_code: int
    stderr: str


class CacheError(BaseFrozen):
    path: str
    message: str


UpdateError = Union[NetworkError, VersionCheckError, PackageNotInstalled, SubprocessError, CacheError]
UpdateMethod = Literal["uv", "pipx", "pip"]


def format_update_error(error: UpdateError) -> str:
    match error:
        case NetworkError(url=url, message=msg):
            return f"Network error fetching {url}: {msg}"
        case VersionCheckError(message=msg):
            return f"Version check failed: {msg}"
        case PackageNotInstalled(package=pkg):
            return f"Package '{pkg}' not installed"
        case SubprocessError(command=cmd, exit_code=code, stderr=err):
            return f"Command '{cmd}' failed (exit {code}): {err.strip()}"
        case CacheError(path=path, message=msg):
            return f"Cache error at {path}: {msg}"
        case _:
            return "Unknown error"


def get_current_version() -> Result[PackageNotInstalled, str]:
    try:
        return Result.ok(version(PACKAGE_NAME))
    except PackageNotFoundError:
        return Result.err(PackageNotInstalled(package=PACKAGE_NAME))


def get_latest_version() -> Result[Union[NetworkError, VersionCheckError], str]:
    try:
        response = requests.get(PYPI_URL, timeout=3)
        response.raise_for_status()
    except requests.RequestException as e:
        return Result.err(NetworkError(url=PYPI_URL, message=str(e)))

    try:
        data = response.json()
        return Result.ok(data["info"]["version"])
    except (json.JSONDecodeError, KeyError) as e:
        return Result.err(VersionCheckError(message=f"Invalid PyPI response: {e}"))


def should_check_update() -> Result[CacheError, bool]:
    mkdir_result = try_catch(lambda: CACHE_FILE.parent.mkdir(parents=True, exist_ok=True))
    match mkdir_result.inner:
        case Err(error=e):
            return Result.err(CacheError(path=str(CACHE_FILE.parent), message=str(e)))
        case Ok():
            pass

    if not CACHE_FILE.exists():
        return Result.ok(True)

    read_result = try_catch(lambda: json.loads(CACHE_FILE.read_text()))
    match read_result.inner:
        case Err():
            return Result.ok(True)  # Cache corrupted, check anyway
        case Ok(value=data):
            last_check = data.get("last_check", 0)
            return Result.ok(time.time() - last_check > CHECK_INTERVAL)


def save_check_timestamp() -> Result[CacheError, None]:
    mkdir_result = try_catch(lambda: CACHE_FILE.parent.mkdir(parents=True, exist_ok=True))
    match mkdir_result.inner:
        case Err(error=e):
            return Result.err(CacheError(path=str(CACHE_FILE.parent), message=str(e)))
        case Ok():
            pass

    write_result = try_catch(lambda: CACHE_FILE.write_text(json.dumps({"last_check": time.time()})))
    match write_result.inner:
        case Err(error=e):
            return Result.err(CacheError(path=str(CACHE_FILE), message=str(e)))
        case Ok():
            return Result.ok(None)


def run_command(cmd: list[str]) -> Result[SubprocessError, subprocess.CompletedProcess[str]]:
    try:
        completed = subprocess.run(cmd, capture_output=True, text=True)
        return Result.ok(completed)
    except FileNotFoundError as e:
        return Result.err(SubprocessError(command=" ".join(cmd), exit_code=127, stderr=str(e)))


def is_uv_tool_install() -> bool:
    exe_path = Path(sys.executable).resolve()
    parts = [p.lower() for p in exe_path.parts]
    return UV_TOOL_PATH_PART in parts and "tools" in parts and UV_TOOL_NAME in parts


def try_uv_update() -> Result[SubprocessError, None]:
    cmd = ["uv", "tool", "install", PACKAGE_NAME, "--force"]
    result = run_command(cmd)

    match result.inner:
        case Ok(value=cp) if cp.returncode == 0:
            return Result.ok(None)
        case Ok(value=cp):
            stderr = cp.stderr or cp.stdout or "Unknown error"
            return Result.err(SubprocessError(command=" ".join(cmd), exit_code=cp.returncode, stderr=stderr))
        case Err(error=err):
            return Result.err(err)


def try_pipx_update() -> Result[SubprocessError, None]:
    cmd = ["pipx", "upgrade", PACKAGE_NAME]
    result = run_command(cmd)

    match result.inner:
        case Ok(value=cp) if cp.returncode == 0:
            return Result.ok(None)
        case Ok(value=cp):
            stderr = cp.stderr or cp.stdout or "Unknown error"
            return Result.err(SubprocessError(command=" ".join(cmd), exit_code=cp.returncode, stderr=stderr))
        case Err(error=err):
            return Result.err(err)


def try_pip_update() -> Result[SubprocessError, None]:
    cmd = [sys.executable, "-m", "pip", "install", "--upgrade", PACKAGE_NAME]
    result = run_command(cmd)

    match result.inner:
        case Ok(value=cp) if cp.returncode == 0:
            return Result.ok(None)
        case Ok(value=cp):
            stderr = cp.stderr or cp.stdout or "Unknown error"
            return Result.err(SubprocessError(command=" ".join(cmd), exit_code=cp.returncode, stderr=stderr))
        case Err(error=err):
            return Result.err(err)


def update_package() -> Result[SubprocessError, UpdateMethod]:
    """Attempt to update via uv tool (if installed that way), then pipx, then pip.

    Handles missing executables (e.g., uv or pipx not in PATH) gracefully.
    Returns the method used on success.
    """
    if is_uv_tool_install() and try_uv_update().is_ok:
        return Result.ok("uv")

    if try_pipx_update().is_ok:
        return Result.ok("pipx")

    pip_result = try_pip_update()
    return pip_result.map(lambda _: "pip")


def check_and_update() -> None:
    """Auto-update check on startup. Silently ignores errors to avoid interrupting user."""
    console = Console()

    should_check_result = should_check_update()
    match should_check_result.inner:
        case Err():
            return
        case Ok(value=should_check):
            if not should_check:
                return

    save_check_timestamp()  # Ignore errors for silent operation

    current_result = get_current_version()
    match current_result.inner:
        case Err():
            return
        case Ok(value=current):
            pass

    latest_result = get_latest_version()
    match latest_result.inner:
        case Err():
            return
        case Ok(value=latest):
            pass

    if Version(latest) > Version(current):
        console.print(f"Updating quick-assistant {current} → {latest}...")
        update_result = update_package()
        match update_result.inner:
            case Ok():
                console.print("Update complete. Please restart the command.")
                sys.exit(0)
            case Err(error=error):
                console.print(f"Auto-update failed: {format_update_error(error)}")


def execute_update() -> int:
    """Manual update command. Returns exit code."""
    console = Console()

    current_result = get_current_version()
    match current_result.inner:
        case Err(error=current_err):
            console.print(f"[red]Error: {format_update_error(current_err)}[/red]")
            return 1
        case Ok(value=current):
            pass

    latest_result = get_latest_version()
    match latest_result.inner:
        case Err(error=latest_err):
            console.print(f"[red]Error: {format_update_error(latest_err)}[/red]")
            return 1
        case Ok(value=latest):
            pass

    if Version(latest) <= Version(current):
        console.print(f"Already at latest version ({current}).")
        return 0

    console.print(f"Updating quick-assistant {current} → {latest}...")
    update_result = update_package()
    match update_result.inner:
        case Ok(value=method):
            console.print(f"[green]Update complete![/green] (via {method})")
            return 0
        case Err(error=update_err):
            console.print(f"[red]Update failed: {format_update_error(update_err)}[/red]")
            return 1
