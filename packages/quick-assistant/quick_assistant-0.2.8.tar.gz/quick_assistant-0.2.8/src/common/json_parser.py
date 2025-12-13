from typing import Type, TypeVar, Dict, Any
from common.result import Result, Ok, Err
from pydantic import BaseModel, ValidationError


T = TypeVar("T", bound=BaseModel)


def try_parse_json(model_type: Type[T], data: Dict[str, Any]) -> Result[str, T]:
    try:
        parsed = model_type.model_validate(data)
        return Result(Ok(parsed))
    except ValidationError as e:
        error_message = "; ".join([f"{err['loc']}: {err['msg']}" for err in e.errors()])
        return Result(Err(error_message))
    except Exception as e:
        return Result(Err(str(e)))
