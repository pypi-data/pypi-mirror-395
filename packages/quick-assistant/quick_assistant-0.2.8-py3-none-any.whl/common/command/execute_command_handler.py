from typing import Type, TypeVar, Callable, Awaitable, Optional, Dict, Any, assert_never
from common.http_response import json_response as json_response, to_response
from common.json_parser import try_parse_json
from common.result import Ok, Err
from common.command.base_command import BaseCommand
from common.command.base_command_handler import BaseCommandHandler
from common.base import BaseFrozen
from common.errors import Fail, Forbidden, Unauthorized, BadRequest, InternalServerError


class BaseCommandResponse(BaseFrozen):
    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__


C = TypeVar("C", bound=BaseCommand)


async def execute_command_handler(
    command_type: Type[C], request_data: Dict[str, Any], command_handler: Callable[[], BaseCommandHandler[C]]
) -> tuple[Dict[str, Any], int]:
    rcommand = try_parse_json(command_type, request_data)
    match rcommand.inner:
        case Err(error=error):
            return to_response(BadRequest(message=f"Invalid request schema: {error}"))
        case Ok(value=value):
            command = value
        case _:
            assert_never(rcommand)

    try:
        result = await command_handler().handle_command(command)
        return result
    except Fail as failure:
        return to_response(failure)
    except Forbidden as failure:
        return to_response(failure)
    except Unauthorized as failure:
        return to_response(failure)
    except BadRequest as failure:
        return to_response(failure)
    except Exception as error:
        return to_response(InternalServerError(message=f"Internal error: {str(error)}"))


async def execute_command_handler_with_api_key(
    command_type: Type[C],
    request_data: Dict[str, Any],
    api_key_header: Optional[str],
    required_api_key: str,
    command_handler: Callable[[], BaseCommandHandler[C]],
) -> tuple[Dict[str, Any], int]:
    if api_key_header != required_api_key:
        return to_response(Unauthorized(message="Invalid API key"))

    return await execute_command_handler(command_type, request_data, command_handler)


async def retrying_on_failure(
    max_retries: int, action: Callable[[], Awaitable[tuple[Dict[str, Any], int]]]
) -> tuple[Dict[str, Any], int]:
    error: Optional[Exception] = None
    retry_count = 0

    while retry_count < max_retries:
        try:
            response = await action()
            return response
        except Exception as err:
            error = err
            retry_count += 1

    if error is None:
        raise RuntimeError("Retries exhausted without an error")

    msg = f"Unable to complete after {max_retries} retries: {error}"
    raise RuntimeError(msg) from error
