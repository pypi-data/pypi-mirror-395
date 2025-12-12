#  Copyright (c) 2024 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

import functools
import typing
from typing import Any

from diffusion.datatypes import AbstractDataType
from diffusion.datatypes.foundation.abstract import (
    TS_T,
    ValueType,
    RealValue,
    ValueType_target,
    Converter,
    IDENTITY, A_T,
)
from diffusion.features.topics import TopicSpecification


@typing.final
class Object(
    AbstractDataType[TopicSpecification["Object"], "Object", "Object"],
):
    """Object (token) implementation."""

    @classmethod
    @functools.lru_cache(maxsize=None)
    def _converter_from(
        cls: typing.Type[AbstractDataType[TS_T, ValueType, RealValue]],
        source_type: typing.Type[ValueType_target],
    ) -> typing.Optional[Converter[ValueType_target, ValueType]]:
        return typing.cast(Converter[ValueType_target, ValueType], IDENTITY)

    @classmethod
    def can_read_as(
            cls,
            result_type: typing.Type[AbstractDataType],
    ) -> bool:
        return cls.is_wildcard(result_type)

    @classmethod
    def encode(cls, value: Any) -> bytes:
        raise NotImplementedError()

    @classmethod
    def decode(cls: typing.Type[A_T], data: bytes) -> Any:
        raise NotImplementedError()
