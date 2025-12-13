from typing import List, TypeVar, Type, Dict, Any, Union, get_type_hints
import typing
from pathlib import Path
import importlib
from common.result import Result, Ok, Err


T = TypeVar("T")


def leaf_classes(superclass: Type[T]) -> List[Type[T]]:
    leaf_classes = []

    def is_generic_leaf(parent: type, cls: type) -> bool:
        is_leaf = len(cls.__subclasses__()) == 0
        is_generic = get_type_constructor(cls) is parent
        return is_leaf and is_generic

    def find_subclasses(cls: type) -> None:
        subclasses = [c for c in cls.__subclasses__() if not is_generic_leaf(cls, c)]

        for subclass in subclasses:
            find_subclasses(subclass)

        if not subclasses:
            leaf_classes.append(cls)

    find_subclasses(superclass)
    return leaf_classes


def import_all(prefix: str) -> None:
    files = [str(file) for file in Path.cwd().rglob("*.py") if file.is_file()]

    modules = [
        module
        for file in files
        for module in [file.replace(str(Path.cwd()) + "/", "").replace("/", ".").replace(".py", "")]
        if module.startswith(prefix)
    ]

    for module in modules:
        importlib.import_module(module)


TypeArgument = Union[Type, Any]


def get_type_constructor(ty: Type[Any]) -> Type[Any]:
    if hasattr(ty, "__pydantic_generic_metadata__"):
        return ty.__pydantic_generic_metadata__["origin"] or ty
    return typing.get_origin(ty) or ty


def get_type_parameters(ty: Type) -> List[TypeVar]:
    if hasattr(ty, "__parameters__"):
        return list(ty.__parameters__)
    if hasattr(ty, "__pydantic_generic_metadata__"):
        return list(ty.__pydantic_generic_metadata__["parameters"])
    return []


def get_type_arguments(ty: Type) -> List[TypeArgument]:
    if hasattr(ty, "__pydantic_generic_metadata__"):
        return list(ty.__pydantic_generic_metadata__["args"])
    return list(typing.get_args(ty))


class UnboundTypeVar(ValueError):
    pass


def concrete_type_hints(concrete: Type[T]) -> Dict[str, Type]:
    origin = get_type_constructor(concrete)
    hints = get_type_hints(origin)
    if len(hints) == 0:
        return {}
    params: List[TypeVar] = get_type_parameters(origin)
    args: List[TypeArgument] = get_type_arguments(concrete) + [Any for _ in params]
    bindings: dict[TypeVar, TypeArgument] = dict(zip(params, args))

    concrete_hints = {}
    for name, ty in hints.items():
        match concrete_type(bindings, ty).inner:
            case Ok(value=value):
                concrete_hints[name] = value
            case Err(error=error):
                raise UnboundTypeVar(f"{error}\nIn field '{name}' of {repr(concrete)} with type {repr(ty)}")
    return concrete_hints


def concrete_type(bound: dict[TypeVar, TypeArgument], generic: Type | TypeVar) -> Result[str, TypeArgument]:
    if isinstance(generic, TypeVar):
        if generic in bound:
            return Result.ok(bound[generic])
        else:
            return Result.ok(Any)

    origin: Type = get_type_constructor(generic)
    args = get_type_arguments(generic)
    if len(args) == 0:
        return Result.ok(origin)

    return Result.traverse(args, lambda ty: concrete_type(bound, ty)).map(lambda concrete_args: origin[*concrete_args])
