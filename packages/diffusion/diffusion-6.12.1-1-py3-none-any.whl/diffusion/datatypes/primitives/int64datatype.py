#  Copyright (c) 2021 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

import typing

from .jsondatatype import JsonDataType
from diffusion.datatypes.exceptions import InvalidDataError


class Int64DataType(JsonDataType[int]):
    """Data type that supports 64-bit, signed integer values.

    The integer value is serialized as CBOR-format binary. A serialized value
    can be read as JSON instance.
    """

    type_code = 18
    type_name = "int64"
    raw_types: typing.Type[typing.Optional[int]] = typing.cast(
        typing.Type[typing.Optional[int]], typing.Type[typing.Optional[int]]
    )

    MAX_VALUE = 1 << 63
    MIN_VALUE = -MAX_VALUE + 1


    @classmethod
    def get_raw_types(cls) -> typing.Type[typing.Optional[int]]:
        return cls.raw_types

    def validate(self) -> None:
        """Check the current value for correctness.

        Raises:
            `InvalidDataError`: If the value is invalid.
        """
        message = ""
        if self.value is not None:
            if not isinstance(self.value, int):
                message = f"Expected an integer but got {type(self.value).__name__}"
            elif not self.MIN_VALUE <= self.value <= self.MAX_VALUE:
                message = "Integer value out of bounds."
        if message:
            raise InvalidDataError(message)
