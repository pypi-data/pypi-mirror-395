from typing import Union, Any, Dict
from common.errors import Fail, Forbidden, Unauthorized, BadRequest, InternalServerError
from common.json import to_json


def to_response(
    failure: Union[Fail, Forbidden, Unauthorized, BadRequest, InternalServerError],
) -> tuple[Dict[str, Any], int]:
    match failure:
        case Fail():
            content = {"error": {"message": failure.message, "details": failure.details}}
            return content, failure.code
        case Forbidden():
            content = {"error": {"message": failure.message}}
            return content, 403
        case Unauthorized():
            content = {"error": {"message": failure.message}}
            return content, 401
        case BadRequest():
            content = {"error": {"message": failure.message, "details": failure.details}}
            return content, 400
        case InternalServerError():
            content = {"error": {"message": failure.message}}
            return content, 500


def json_response(data: Union[Dict[str, Any], Any], status: int = 200) -> tuple[Dict[str, Any], int]:
    if isinstance(data, dict):
        json_data = data
    else:
        converted = to_json(data)
        if not isinstance(converted, dict):
            raise ValueError(f"Expected dict from to_json, got {type(converted).__name__}")
        json_data = converted
    return json_data, status
