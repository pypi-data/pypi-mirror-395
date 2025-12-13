from dataclasses import dataclass
from typing import Optional, Any


@dataclass(frozen=True)
class Fail(Exception):
    code: int
    message: str
    details: Optional[Any] = None


@dataclass(frozen=True)
class Forbidden(Exception):
    message: str


@dataclass(frozen=True)
class Unauthorized(Exception):
    message: str


@dataclass(frozen=True)
class BadRequest(Exception):
    message: str
    details: Optional[Any] = None


@dataclass(frozen=True)
class InternalServerError(Exception):
    message: str


def annotate(message: str, error: Exception) -> Exception:
    error.args = (f"{message}: {error.args[0]}" if error.args else message,) + error.args[1:]
    return error
