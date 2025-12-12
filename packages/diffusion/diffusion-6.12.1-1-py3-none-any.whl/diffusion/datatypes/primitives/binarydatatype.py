#  Copyright (c) 2021 - 2025 DiffusionData Ltd., All Rights Reserved.
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

from ..foundation.abstract import A_T
from .primitivedatatype import PrimitiveDataType


class BinaryDataType(PrimitiveDataType[bytes]):
    """
    Binary data type. Not convertible to or from other types
    """

    type_code = 14
    type_name = "binary"
    raw_types: typing.Type[typing.Optional[bytes]] = typing.cast(
        typing.Type[typing.Optional[bytes]], typing.Optional[bytes]
    )

    @classmethod
    def get_raw_types(cls) -> typing.Type[typing.Optional[bytes]]:
        return cls.raw_types

    @classmethod
    def encode(cls, value: typing.Any) -> bytes:
        return value

    @classmethod
    def decode(cls: typing.Type[A_T], data: bytes) -> typing.Any:
        return data

    def __str__(self):
        return self.value.decode()
