from __future__ import annotations
from pydantic import BaseModel, ConfigDict
from typing import (
    Dict,
    TypeVar,
    Type,
    Self,
    List,
    Any,
    Union,
    Callable,
    NewType,
    Literal,
    get_args,
    get_type_hints,
    get_origin,
    assert_never,
)
from decimal import Decimal
from json import dumps
from common.reflection import concrete_type_hints, get_type_constructor, UnboundTypeVar
from common.result import Result, Ok, Err
from pydantic import ValidationError


T = TypeVar("T")


class ParsingOptions(BaseModel):
    model_config = ConfigDict(strict=True, frozen=True, arbitrary_types_allowed=False, extra="forbid")
    fill_missing_optionals: bool


defaultParsingOptions = ParsingOptions(fill_missing_optionals=False)


def parse_json(ty: Type[T], data: JSONObject, opts: ParsingOptions = defaultParsingOptions) -> T:
    result: Result[str, T] = try_parse_json(ty, data, opts)
    match result.inner:
        case Err(error=error):
            raise ValueError(error)
        case Ok(value=value):
            return value
    assert_never(result)


def try_parse_json(ty: Type[T], data: JSONObject, opts: ParsingOptions = defaultParsingOptions) -> Result[str, T]:
    return parse(ty, data, opts)


def to_json(data: Serializeable) -> JSONObject:
    if isinstance(data, int) or isinstance(data, float) or isinstance(data, str) or data is None:
        return data

    if isinstance(data, list) or isinstance(data, set):
        return [to_json(element) for element in data]

    if isinstance(data, dict):
        return {key: to_json(value) for key, value in data.items()}

    if isinstance(data, Decimal):
        return str(data)

    if isinstance(data, ToJSON):
        return data.to_json()

    raise ValueError(f"Cannot convert {type(data).__name__} to JSON")


JSONObject = str | float | int | None | list | dict


class ToJSON:
    def to_json(self: Self) -> JSONObject:
        properties: List[str] = list(get_type_hints(self.__class__).keys())
        return {prop: to_json(self.__dict__[prop]) for prop in properties}


def is_optional(typ: Type[Any]) -> bool:
    return get_origin(typ) is Union and type(None) in get_args(typ)


class FromJSON:
    @classmethod
    def from_json(cls: Type[T], json: JSONObject, opts: ParsingOptions = defaultParsingOptions) -> Result[str, T]:
        return parser_for_class(cls)(json, opts)


def parser_for_class(cls: Type[T]) -> Parser[T]:
    def class_parser(json: JSONObject, opts: ParsingOptions = defaultParsingOptions) -> Result[str, T]:
        if not isinstance(json, dict):
            return Result.err(
                f"Expected dict but found {type(json).__name__}, when decoding {cls.__name__} from value: {dumps(json)}"
            )

        rhints = try_concrete_type_hints(cls)
        match rhints.inner:
            case Err(error=error):
                return Result.err(f"When decoding {repr(cls)}\n{error}")
            case Ok(value=hints):
                args: dict[str, Any] = {}
                for field, field_type in hints.items():
                    if field not in json:
                        if is_optional(field_type) and opts.fill_missing_optionals:
                            args[field] = None
                        continue
                    parsed = parser_for(field_type)(json[field], opts)
                    match parsed.inner:
                        case Ok(value=value):
                            args[field] = value
                        case Err(error=error):
                            return Result.err(f"Parsing field '{field}': {error}")
                try:
                    return Result.ok(cls(**args))
                except ValidationError as e:

                    def pretty_loc(v: tuple[int | str, ...] | None) -> str:
                        if v is None:
                            return ""
                        return ".".join([f"'{str(el)}'" for el in list(v)])

                    return Result.err(
                        ". ".join(
                            [
                                pretty_loc(details.get("loc")) + ": " + (details.get("msg") or "")
                                for details in e.errors()
                            ]
                        )
                    )

    return class_parser


def try_concrete_type_hints(ty: Type[T]) -> Result[str, Dict[str, Type]]:
    try:
        return Result.ok(concrete_type_hints(ty))
    except UnboundTypeVar as e:
        return Result.err(", ".join(list(e.args)))


BuiltInSupported = str | float | int | None | list | dict | set | Decimal

Serializeable = JSONObject | ToJSON | BuiltInSupported

Parseable = JSONObject | FromJSON | BuiltInSupported

Parser = Callable[[JSONObject, ParsingOptions], Result[str, T]]


def parse(ty: Type[T], data: JSONObject, opts: ParsingOptions) -> Result[str, T]:
    return parser_for(ty)(data, opts)


def parse_any(json: JSONObject, _: ParsingOptions) -> Result[str, Any]:
    return Result.ok(json)


def parse_string(json: JSONObject, _: ParsingOptions) -> Result[str, str]:
    if isinstance(json, str):
        return Result.ok(json)
    return Result.err(f"Expected str but found {type(json).__name__}")


def parse_bool(json: JSONObject, _: ParsingOptions) -> Result[str, bool]:
    if isinstance(json, bool):
        return Result.ok(json)
    return Result.err(f"Expected bool but found {type(json).__name__}")


def parse_float(json: JSONObject, _: ParsingOptions) -> Result[str, float]:
    if isinstance(json, float):
        return Result.ok(json)
    return Result.err(f"Expected float but found {type(json).__name__}")


def parse_int(json: JSONObject, _: ParsingOptions) -> Result[str, int]:
    if isinstance(json, int):
        return Result.ok(json)
    return Result.err(f"Expected int but found {type(json).__name__}")


def parse_None(json: JSONObject, _: ParsingOptions) -> Result[str, None]:
    if isinstance(json, type(None)):
        return Result.ok(None)
    return Result.err(f"Expected None but found {type(json).__name__}")


def parse_list(json: JSONObject, element_ty: Type[T], opts: ParsingOptions) -> Result[str, list[T]]:
    if isinstance(json, list):

        def parseAt(x: tuple[int, JSONObject]) -> Result[str, T]:
            index, value = x
            parser = parser_for(element_ty)
            parsed = parser(value, opts)
            return parsed.map_err(lambda err: f"At index {str(index)}: {err}")

        return Result.traverse(list(enumerate(json)), parseAt)
    return Result.err(f"Expected List but found {type(json).__name__}")


def parse_set(json: JSONObject, element_ty: Type[T], opts: ParsingOptions) -> Result[str, set[T]]:
    if isinstance(json, list):
        return parse_list(json, element_ty, opts).map(set)
    return Result.err(f"Expected Set but found {type(json).__name__}")


W = TypeVar("W")


def parse_dict(json: JSONObject, key_ty: Type[T], value_ty: Type[W], opts: ParsingOptions) -> Result[str, dict[T, W]]:
    if isinstance(json, dict):
        r = {}
        for key, value in json.items():
            parsed_key = parse(key_ty, key, opts)
            parsed_val = parse(value_ty, value, opts)
            match parsed_key.inner:
                case Err(error=error):
                    return Result.err(f"Parsing key name {key}: {error}")
            match parsed_val.inner:
                case Err(error=error):
                    return Result.err(f"Parsing key {key}: {error}")
            r[parsed_key.inner.value] = parsed_val.inner.value
        return Result.ok(r)
    return Result.err(f"Expected Dict but found {type(json).__name__}")


def parse_decimal(json: JSONObject, opts: ParsingOptions) -> Result[str, Decimal]:
    return parse_string(json, opts).map(Decimal)


def parse_one_of(json: JSONObject, parsers: List[Parser[T]], opts: ParsingOptions) -> Result[str, T]:
    parsed = [parser(json, opts).inner for parser in parsers]
    successes = [result.value for result in parsed if isinstance(result, Ok)]

    if len(successes) == 0:
        failures = [result.error for result in parsed if isinstance(result, Err)]

        return Result.err("No parse.\n" + "\n".join(failures))
    elif len(successes) == 1:
        return Result.ok(successes[0])
    else:
        successes_str = map(lambda x: str(x), successes)
        return Result.err(f"Ambiguous parse of {dumps(json)}: {successes_str}")


def parser_for(ty: Type[T]) -> Parser[T]:
    if ty is Any:
        return parse_any
    if ty is str:
        return parse_string  # type: ignore
    if ty is bool:
        return parse_bool  # type: ignore
    if ty is float:
        return parse_float  # type: ignore
    if ty is int:
        return parse_int  # type: ignore
    if ty is type(None):
        return parse_None  # type: ignore
    if get_type_constructor(ty) is list:
        (element_ty,) = get_args(ty) or (Any,)
        return lambda json, opts: parse_list(json, element_ty, opts)  # type: ignore
    if get_type_constructor(ty) is dict:
        key_ty, value_ty = get_args(ty) or (Any, Any)
        return lambda json, opts: parse_dict(json, key_ty, value_ty, opts)  # type: ignore
    if get_type_constructor(ty) is set:
        (element_ty,) = get_args(ty) or (Any,)
        return lambda json, opts: parse_set(json, element_ty, opts)  # type: ignore
    if ty is Decimal:
        return parse_decimal  # type: ignore
    if get_origin(ty) is Union:
        args = list(get_args(ty))
        parsers = [parser_for(arg) for arg in args]
        return lambda json, opts: parse_one_of(json, parsers, opts)

    if isinstance(ty, NewType):
        return parser_for(ty.__supertype__)  # type: ignore

    if isinstance(ty, type) and issubclass(ty, FromJSON):
        return lambda json, opts: ty.from_json(json, opts)  # type: ignore

    if get_origin(ty) is Literal:
        parsers = [parse_literal(arg) for arg in list(ty.__args__)]  # type: ignore
        return lambda json, opts: parse_one_of(json, parsers, opts)

    raise ValueError(f"No JSON parser available for {ty.__name__}")


def parse_literal(arg: Any) -> Parser[T]:
    parser = parser_for(type(arg))
    return lambda value, opts: parser(value, opts).then(lambda v: check_literal(arg, v))


def check_literal(argument: Any, value: Any) -> Result[str, Any]:
    if argument == value:
        return Result.ok(value)
    else:
        return Result.err(f"Value mismatch. Expected {argument}, found {value}")
