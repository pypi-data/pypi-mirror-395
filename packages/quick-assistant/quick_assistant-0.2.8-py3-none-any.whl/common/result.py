from typing import TypeVar, Generic, Callable, Union, List, Any, Awaitable
from dataclasses import dataclass


F = TypeVar("F")
S = TypeVar("S")
T = TypeVar("T")


@dataclass(frozen=True)
class Err(Generic[F]):
    error: F


@dataclass(frozen=True)
class Ok(Generic[S]):
    value: S


Unwrapped = Union[Err[F], Ok[S]]


@dataclass(frozen=True)
class Result(Generic[F, S]):
    inner: Unwrapped[F, S]

    @staticmethod
    def ok(value: S) -> "Result[F, S]":
        return Result(Ok(value))

    @staticmethod
    def err(error: F) -> "Result[F, S]":
        return Result(Err(error))

    def map(self, func: Callable[[S], T]) -> "Result[F, T]":
        match self.inner:
            case Ok(value=value):
                return Result(Ok(func(value)))
            case Err(error=error):
                return Result(Err(error))

    def map_err(self, func: Callable[[F], T]) -> "Result[T, S]":
        match self.inner:
            case Ok(value=value):
                return Result(Ok(value))
            case Err(error=error):
                return Result(Err(func(error)))

    def then(self, func: Callable[[S], "Result[F, T]"]) -> "Result[F, T]":
        match self.inner:
            case Ok(value=value):
                return func(value)
            case Err(error=error):
                return Result(Err(error))

    def unwrap(self) -> S:
        match self.inner:
            case Ok(value=value):
                return value
            case Err(error=error):
                raise RuntimeError(f"Called unwrap on an Err value: {error}")

    def unwrap_or(self, default: S) -> S:
        match self.inner:
            case Ok(value=value):
                return value
            case Err():
                return default

    @property
    def is_ok(self) -> bool:
        return isinstance(self.inner, Ok)

    @property
    def is_err(self) -> bool:
        return isinstance(self.inner, Err)

    @staticmethod
    def traverse(items: List[T], func: Callable[[T], "Result[F, S]"]) -> "Result[F, List[S]]":
        results = []
        for item in items:
            result = func(item)
            match result.inner:
                case Ok(value=value):
                    results.append(value)
                case Err(error=error):
                    return Result(Err(error))
        return Result(Ok(results))


def try_catch(func: Callable[[], S]) -> Result[Exception, S]:
    try:
        return Result(Ok(func()))
    except Exception as e:
        return Result(Err(e))


def safe(func: Callable[..., S]) -> Callable[..., Result[Exception, S]]:
    def wrapper(*args: Any, **kwargs: Any) -> Result[Exception, S]:
        return try_catch(lambda: func(*args, **kwargs))

    return wrapper


async def async_try_catch(func: Callable[[], Awaitable[S]]) -> Result[Exception, S]:
    try:
        return Result(Ok(await func()))
    except Exception as e:
        return Result(Err(e))


def async_safe(func: Callable[..., Awaitable[S]]) -> Callable[..., Awaitable[Result[Exception, S]]]:
    async def wrapper(*args: Any, **kwargs: Any) -> Result[Exception, S]:
        return await async_try_catch(lambda: func(*args, **kwargs))

    return wrapper
