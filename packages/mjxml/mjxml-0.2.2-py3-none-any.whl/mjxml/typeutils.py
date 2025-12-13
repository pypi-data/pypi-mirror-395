from typing import (
    Any,
    Iterator,
    Protocol,
    TypeVar,
    SupportsIndex,
    overload,
    runtime_checkable,
    SupportsFloat,
    SupportsInt,
)
from types import new_class
import numpy as np

__all__ = [
    "ArrayLike",
    "Str",
    "EPS",
    "Natural",
    "StrictNatural",
    "PosFloat",
    "StrictPosFloat",
    "SupportsBool",
    "compare",
    "floatarr_to_str",
    "intarr_to_str",
    "floatarr_to_tuple",
    "intarr_to_tuple",
]

EPS: float = float(np.finfo(np.float32).eps)


class NaturalMeta(type(Protocol)):
    def __instancecheck__(cls, instance):
        if not isinstance(instance, SupportsInt):
            return False
        return int(instance) >= 0


class StrictNaturalMeta(type(Protocol)):
    def __instancecheck__(cls, instance) -> bool:
        if not isinstance(instance, SupportsInt):
            return False
        return int(instance) > 0


class PosFloatMeta(type(Protocol)):
    def __instancecheck__(cls, instance) -> bool:
        if not isinstance(instance, SupportsFloat):
            return False
        return float(instance) >= 0.0


class StrictPosFloatMeta(type(Protocol)):
    def __instancecheck__(cls, instance) -> bool:
        if not isinstance(instance, SupportsFloat):
            return False
        return float(instance) >= EPS


@runtime_checkable
class Natural(Protocol, metaclass=NaturalMeta):
    def __int__(self) -> int: ...


@runtime_checkable
class StrictNatural(Protocol, metaclass=StrictNaturalMeta):
    def __int__(self) -> int: ...


@runtime_checkable
class PosFloat(Protocol, metaclass=PosFloatMeta):
    def __float__(self) -> float: ...


@runtime_checkable
class StrictPosFloat(Protocol, metaclass=StrictPosFloatMeta):
    def __float__(self) -> float: ...


@runtime_checkable
class Str(Protocol):
    def __str__(self) -> str: ...


@runtime_checkable
class SupportsBool(Protocol):
    def __bool__(self) -> bool: ...


class _ArrayTypeChecker(type):
    def __instancecheck__(self, instance) -> bool:
        length: tuple[int, ...] | None = getattr(self, "length", None)
        item_type: type[Any] | tuple[Any, ...] = getattr(self, "item_type", Any)

        if not isinstance(instance, ArrayLike):
            return False

        to = len(instance)

        if length is not None:
            if to not in length:
                return False

        iterator = iter(instance)
        for i, val in enumerate(range(to)):
            val = next(iterator)
            if not isinstance(val, item_type):
                return False
        return True


T = TypeVar("T", covariant=True)
N = TypeVar("N", bound=Any | type[int] | None, default=None)


@runtime_checkable
class ArrayLike(Protocol[T, N]):
    @classmethod
    def __class_getitem__(cls, item) -> Any:
        if isinstance(item, tuple):
            item_type, length = item
        else:
            item_type, length = item, None

        if isinstance(length, int):
            length = (length,)
        elif "__args__" in getattr(length, "__dict__", {}):
            length = length.__args__  # type: ignore

        nc_name = "ArrayLike[{0}{1}]".format(
            item_type.__name__, "" if length is None else f", allowed_lengths={length}"
        )
        return new_class(
            nc_name,
            (),
            {"metaclass": _ArrayTypeChecker},
            lambda ns: ns.update({"item_type": item_type, "length": length}),
        )

    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[T]: ...
    @overload
    def __getitem__(self, i: SupportsIndex, /) -> T: ...
    @overload
    def __getitem__(self, s: slice, /) -> "ArrayLike"[T]: ...


def compare(a: ArrayLike[Any] | None, b: ArrayLike[Any] | None) -> bool:
    if a is None or b is None: 
        return (a is None) and (b is None)

    assert a is not None and b is not None
    if len(a) != len(b):
        return False
    for x, y in zip(a, b):
        if isinstance(x, SupportsFloat) and isinstance(y, SupportsFloat):
            if abs(float(x) - float(y)) > EPS:
                return False
        elif isinstance(x, SupportsInt) and isinstance(y, SupportsInt):
            if int(x) != int(y):
                return False
        else:
            if x != y:
                return False
    return True

def floatarr_to_str(arr: ArrayLike[SupportsFloat] | None) -> str:
    if arr is None: 
        return ""
    return " ".join(str(float(v)) for v in arr)

def intarr_to_str(arr: ArrayLike[SupportsInt] | None) -> str:
    if arr is None:
        return ""
    return " ".join(str(int(v)) for v in arr)

def floatarr_to_tuple(arr: ArrayLike[SupportsFloat] | None) -> tuple[float, ...] | None:
    if arr is None:
        return None
    return tuple(float(v) for v in arr)

def intarr_to_tuple(arr: ArrayLike[SupportsInt] | None) -> tuple[int, ...] | None:
    if arr is None:
        return None
    return tuple(int(v) for v in arr)