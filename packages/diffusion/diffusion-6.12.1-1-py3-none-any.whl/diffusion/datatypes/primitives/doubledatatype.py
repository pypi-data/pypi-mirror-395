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


class DoubleDataType(JsonDataType[float]):
    """Data type that supports double-precision floating point numbers.

    (Eight-byte IEEE 754)

    The integer value is serialized as CBOR-format binary. A serialized value
    can be read as a JSON instance.
    """

    @classmethod
    def get_raw_types(cls) -> typing.Type[typing.Optional[float]]:
        return cls.raw_types

    type_code = 19
    type_name = "double"
    raw_types: typing.Type[typing.Optional[float]] = typing.cast(
        typing.Type[typing.Optional[float]], typing.Optional[float]
    )

