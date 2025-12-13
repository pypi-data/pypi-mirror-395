import json
import os
import platform

from enum import Enum
from pathlib import Path
from typing import Optional, Union

from common.base import BaseFrozen
from common.result import Result, Ok, Err, try_catch


class CommitConvention(str, Enum):
    CONVENTIONAL = "conventional"
    IMPERATIVE = "imperative"
    CUSTOM = "custom"


class Config(BaseFrozen):
    api_key: str
    commit_convention: CommitConvention
    custom_template: Optional[str] = None


class ConfigNotFound(BaseFrozen):
    path: str


class ConfigParseError(BaseFrozen):
    message: str


class ConfigWriteError(BaseFrozen):
    message: str


ConfigError = Union[ConfigNotFound, ConfigParseError, ConfigWriteError]


def error_to_message(error: ConfigError) -> str:
    match error:
        case ConfigNotFound(path=p):
            return f"Config not found at {p}"
        case ConfigParseError(message=m):
            return f"Config parse error: {m}"
        case ConfigWriteError(message=m):
            return f"Config write error: {m}"


def validate_commit_convention(value: str) -> Result[ConfigParseError, CommitConvention]:
    try:
        return Result.ok(CommitConvention(value))
    except ValueError:
        return Result.err(ConfigParseError(message=f"Invalid commit convention: {value}"))


def get_home_path() -> Path:
    if platform.system() == "Windows":
        userprofile = os.environ.get("USERPROFILE")
        if userprofile:
            return Path(userprofile)
    return Path.home()


def get_config_dir() -> Path:
    return get_home_path() / ".quick-assistant"


def get_config_path() -> Path:
    return get_config_dir() / "config.json"


def load_config() -> Result[ConfigError, Config]:
    config_path = get_config_path()

    if not config_path.exists():
        return Result.err(ConfigNotFound(path=str(config_path)))

    read_result = try_catch(lambda: config_path.read_text())
    match read_result.inner:
        case Err(error=e):
            return Result.err(ConfigParseError(message=str(e)))
        case Ok(value=content):
            pass

    parse_result = try_catch(lambda: json.loads(content))
    match parse_result.inner:
        case Err(error=parse_err):
            return Result.err(ConfigParseError(message=str(parse_err)))
        case Ok(value=data):
            pass

    convention_result = validate_commit_convention(data.get("commit_convention", ""))
    match convention_result.inner:
        case Err(error=conv_err):
            return Result.err(conv_err)
        case Ok(value=convention):
            data["commit_convention"] = convention

    validate_result = try_catch(lambda: Config(**data))
    match validate_result.inner:
        case Err(error=validation_err):
            return Result.err(ConfigParseError(message=str(validation_err)))
        case Ok(value=config):
            return Result.ok(config)


def save_config(config: Config) -> Result[ConfigWriteError, None]:
    config_path = get_config_path()

    mkdir_result = try_catch(lambda: config_path.parent.mkdir(parents=True, exist_ok=True))
    match mkdir_result.inner:
        case Err(error=e):
            return Result.err(ConfigWriteError(message=str(e)))
        case Ok():
            pass

    data = {
        "api_key": config.api_key,
        "commit_convention": config.commit_convention.value,
        "custom_template": config.custom_template,
    }

    write_result = try_catch(lambda: config_path.write_text(json.dumps(data, indent=2)))
    match write_result.inner:
        case Err(error=e):
            return Result.err(ConfigWriteError(message=str(e)))
        case Ok():
            return Result.ok(None)


def is_configured() -> bool:
    return get_config_path().exists()


def is_ready() -> bool:
    env_key = os.getenv("GOOGLE_API_KEY")
    if env_key:
        return True
    return get_config_path().exists()


def get_api_key() -> Result[ConfigNotFound, str]:
    env_key = os.getenv("GOOGLE_API_KEY")
    if env_key:
        return Result.ok(env_key)

    config_result = load_config()
    match config_result.inner:
        case Ok(value=config):
            return Result.ok(config.api_key)
        case Err(error=e):
            match e:
                case ConfigNotFound():
                    return Result.err(e)
                case _:
                    return Result.err(ConfigNotFound(path=str(get_config_path())))
