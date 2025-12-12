#  Copyright (c) 2025 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

from __future__ import annotations

import abc
import copy
import sys
import typing
import collections.abc
from abc import abstractmethod

import typing_extensions
from typing_extensions import runtime_checkable
if sys.version_info >= (3, 9):
    from collections.abc import Mapping
else:
    from typing import Mapping

@runtime_checkable
class StrictHashable(typing.Protocol):
    def __hash__(self) -> int:
        ...


HashableElement = typing.Union[
    StrictHashable,
    typing.Collection[StrictHashable],
    typing.Mapping[StrictHashable, "HashableElement"],
]

HashableElement_T = typing.TypeVar("HashableElement_T", bound=HashableElement)


class ImmutableList(collections.abc.Sequence):
    """
    An immutable, hashable list that returns another ImmutableList when sliced.
    """

    def __init__(self, iterable=()):
        self._data = tuple(iterable)  # Freeze contents

    def __getitem__(self, index):
        # For slices, return a new ImmutableList; otherwise, return the element.
        if isinstance(index, slice):
            return type(self)(self._data[index])
        return self._data[index]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __eq__(self, other):
        return isinstance(other, ImmutableList) and self._data == other._data

    def __hash__(self):
        # ImmutableList is hashable if all its elements are hashable.
        return hash(self._data)

    def __repr__(self):
        return f"{type(self).__qualname__}({self._data})"


class BaseFreezer(typing.Generic[HashableElement_T], abc.ABC):
    def __call__(
        self,
        item: HashableElement_T,
        _visited: typing.Optional[set[int]] = None,
    ) -> StrictHashable:
        """
        Recursively freeze' an object so that all nested elements are hashable.
        Uses cycle detection (via a recursion stack) and raises a ValueError
        if a cycle is detected.
        """
        if _visited is None:
            _visited = set()
        if id(item) in _visited:
            raise ValueError(
                "Cycle detected in data structure. Cyclic references are not supported."
            )
        _visited.add(id(item))
        result: StrictHashable
        try:
            if isinstance(item, (HashableDict, TransparentHashableDict)):
                result = item
            elif isinstance(item, typing.Mapping):
                result = TransparentHashableDict.create(
                    {k: self(v, _visited=_visited) for k, v in item.items()}
                )
            elif isinstance(item, (set, frozenset)):
                result = frozenset(self(x, _visited=_visited) for x in item)
            elif isinstance(item, list):
                result = ImmutableList(self(x, _visited=_visited) for x in item)
            elif isinstance(item, tuple):
                transformed = tuple(self(x, _visited=_visited) for x in item)
                # If the tuple is a namedtuple (has _fields), attempt to reconstruct it.
                if hasattr(item, "_fields"):
                    try:
                        result = type(item)(*transformed)  # type: ignore[arg-type]
                        if not isinstance(result, type(item)):
                            result = self.fallback_freeze(item)
                    except TypeError:
                        result = self.fallback_freeze(item)
                else:
                    result = self.fallback_freeze(transformed)
            else:
                result = self.fallback_freeze(item)
        finally:
            _visited.remove(id(item))

        # Final check: ensure that the frozen result is hashable.
        try:
            hash(result)
        except TypeError:
            raise TypeError(
                f"The frozen object of type {type(result).__name__} is not hashable."
            )
        return result

    def fallback_freeze(
        self,
        item: typing.Any,
        _visited: typing.Optional[typing.Set[int]] = None,
    ) -> StrictHashable:
        """
        Fallback freezing method for items not handled by the recursive cases.
        """
        try:
            return self.fallback_freeze_impl(item, _visited=_visited)
        except Exception as ex:
            raise TypeError(
                f"Item {item} is not strictly hashable and cannot be frozen."
            ) from ex

    @abstractmethod
    def fallback_freeze_impl(
        self,
        item: typing.Any,
        _visited: typing.Optional[typing.Set[int]] = None,
    ) -> StrictHashable: ...


class StrictFreezer(BaseFreezer[HashableElement]):
    def fallback_freeze_impl(
        self,
        item: typing.Any,
        _visited: typing.Optional[typing.Set[int]] = None,
    ) -> StrictHashable:
        hash(item)
        return copy.deepcopy(item)


strict_freezer = StrictFreezer()


_KT = typing.TypeVar("_KT", bound=StrictHashable)
_VT_co = typing.TypeVar("_VT_co", covariant=True, bound=HashableElement)
_VT_strict_co = typing.TypeVar("_VT_strict_co", covariant=True, bound=StrictHashable)
_KT_other = typing.TypeVar("_KT_other", bound=StrictHashable)
ET = typing_extensions.TypeVar("ET", bound="HashableDict")

class HashableDict(typing.Generic[_KT, _VT_co], Mapping[_KT, _VT_co]):
    class HashableDictContents(typing.Tuple[typing.Tuple[_KT, _VT_co], ...]):
        ...

    def __init__(self, value: typing.Mapping[_KT, _VT_co]) -> None:
        # Use deepcopy to freeze the internal state and compute a stable hash.
        frozen_contents = {k: strict_freezer(v) for k, v in value.items()}
        self._value = copy.deepcopy(value)
        self.hash = hash(tuple(frozen_contents.items()))


    @classmethod
    @typing_extensions.overload
    def create(
            cls,
            value: typing.Mapping[_KT, _VT_co],
    ) -> HashableDict[_KT, _VT_co]: ...

    @classmethod
    @typing_extensions.overload
    def create(
            cls,
            value: typing.Mapping[_KT, _VT_co],
            *expected_types:typing.Type[ET],
    ) -> ET: ...

    @classmethod
    def create(
        cls,
        value: typing.Mapping[_KT, _VT_co],
        *expected_types:typing.Type[ET],
    ) -> typing.Union[HashableDict[_KT, _VT_co], ET]:
        if isinstance(value, (cls, *expected_types)):
            return typing.cast(typing.Union[typing_extensions.Self, ET], value)
        return cls(value)

    def __invert__(
        self: HashableDict[_VT_strict_co, _KT_other],
    ) -> HashableDict[_KT_other, _VT_strict_co]:
        return HashableDict.create(
            typing.cast(
                typing.Mapping[_KT_other, _VT_strict_co], {v: k for k, v in self.items()}
            )
        )

    def __hash__(self) -> int:
        return self.hash

    def __getitem__(self, key: _KT, /) -> _VT_co:
        return self._value.__getitem__(key)

    def __len__(self) -> int:
        return len(self._value)

    def __iter__(self) -> typing.Iterator[_KT]:
        return iter(self._value)

    def __repr__(self):
        return f"{type(self).__qualname__}({self._value})"


class TransparentHashableDict(
    typing.Generic[_KT, _VT_co],
    HashableDict[_KT, _VT_co],
):
    def __repr__(self):
        # For a transparent representation, simply use the internal dict’s repr.
        return repr(self._value)
