#  Copyright (c) 2024 - 2025 DiffusionData Ltd., All Rights Reserved.
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
from typing import Any

from diffusion.datatypes.foundation.abstract import AbstractDataType, ValueType, \
    ValueType_target, Converter, A_T
from diffusion.features.topics.details.topic_specification import TopicSpecification


class NoneType(object):
    @property
    def value(
            self
    ) -> typing.Any:
        raise NotImplementedError()  # pragma: no cover

    def to_bytes(self) -> bytes:
        raise NotImplementedError()  # pragma: no cover

    @classmethod
    def converter_from(
        cls: typing.Type[ValueType],
        source_type: typing.Type[ValueType_target],
    ) -> typing.Optional[Converter[ValueType_target, ValueType]]:
        raise NotImplementedError()  # pragma: no cover


@typing.final
class IVoidFetch(
    AbstractDataType[TopicSpecification["IVoidFetch"], NoneType, NoneType]
):
    """
    Internal representation of an untyped fetch request/result.

    """

    type_code = -1
    type_name = "IVoidFetch"
    @classmethod
    def encode(cls, value: Any) -> bytes:
        """Convert a value into the corresponding binary representation.

        Args:
            value:
                Native value to be serialised

        Returns:
            Serialised binary representation of the value.
        """
        raise NotImplementedError()

    @classmethod
    def decode(cls: typing.Type[A_T], data: bytes) -> Any:
        """Convert a binary representation into the corresponding value.

        Args:
            data: Serialised binary representation of the value.

        Returns:
            Deserialised value.
        """
        raise NotImplementedError()
