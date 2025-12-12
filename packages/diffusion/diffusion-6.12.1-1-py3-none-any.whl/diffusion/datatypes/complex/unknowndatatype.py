#  Copyright (c) 2021 - 2025 DiffusionData Ltd., All Rights Reserved.
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

from diffusion.datatypes.foundation.abstract import (
    AbstractDataType,
    TS_T,
    ValueType,
    RealValue,
    ValueType_target,
    Converter
)
from diffusion.datatypes.foundation.ibytesdatatype import IBytes
from diffusion.features.topics import TopicSpecification


@typing.final
class UnknownDataType(
    IBytes[
        TopicSpecification["UnknownDataType"], "UnknownDataType", "UnknownDataType"
    ],
):
    """Unknown data type implementation."""

    type_code = 21
    type_name = "unknown"

    @classmethod
    @functools.lru_cache(maxsize=None)
    def _converter_from(
        cls: typing.Type[AbstractDataType[TS_T, ValueType, RealValue]],
        source_type: typing.Type[ValueType_target],
    ) -> typing.Optional[Converter[ValueType_target, ValueType]]:
        return None

    @classmethod
    def can_read_as(
        cls: typing.Type[AbstractDataType],
        result_type: typing.Type[AbstractDataType],
    ) -> bool:
        return False
