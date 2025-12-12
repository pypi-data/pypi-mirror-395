#  Copyright (c) 2020 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

from __future__ import annotations

import typing
from enum import Enum
from typing import Iterator, Optional, Sequence, Type, Union, Mapping, MutableMapping

from diffusion.internal.hashable_dict import StrictHashable, \
    strict_freezer, HashableElement

import structlog

from diffusion.internal.encoded_data import (
    Byte,
    Bytes,
    EncodingProtocol,
    Int32,
    Int64,
    String,
)

LOG = structlog.get_logger()

EncodingClass = Type[EncodingProtocol]
SerialiserChain = Sequence[Optional[EncodingClass]]
SerialiserMapValue = Union[EncodingClass, SerialiserChain]
SerialiserMap = Mapping[str, SerialiserMapValue]
MutableSerialiserMap = MutableMapping[str, SerialiserMapValue]
SerialiserOutput = Iterator[Optional[Type[EncodingProtocol]]]

NULL_VALUE_KEY = "void"
ENCODING_TYPE_KEYS = {
    NULL_VALUE_KEY: [],
    "BYTE": Byte,
    "BYTES": Bytes,
    "FIXED_BYTES": Bytes,
    "INT32": Int32,
    "INT64": Int64,
    "STRING": String,
}


class CompoundSpec(typing.NamedTuple):
    type: Compound
    args: typing.Tuple[StrictHashable, ...]

    def __repr__(self):
        return f"{self.type}({','.join(map(repr, self.args))})"


class Compound(Enum):
    """Types of compound types."""

    # noinspection PyMethodParameters
    def _generate_next_value_(name, start, count, last_values):  # NOQA: N805
        return name

    ONE_OF = "one-of"
    N_OF = "n-of"
    SET_OF = "set-of"
    SORTED_SET = "sorted-set"
    MAP_OF = "map-of"
    STRING = "string"

    def __call__(self, *args: HashableElement) -> CompoundSpec:
        """Return an instance of the corresponding spec."""
        return CompoundSpec(type=self, args=tuple(strict_freezer(x) for x in args))

    def __repr__(self, *args):
        return f"Compound.{self._name_}"


SpecItem = Union[str, CompoundSpec]
SerialiserSpecItem = Optional[Union[EncodingClass, Sequence[SpecItem], SerialiserChain]]


