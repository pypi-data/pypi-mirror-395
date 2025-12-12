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


class StringDataType(JsonDataType[str]):
    """String data type.

    The string value is serialized as CBOR-format binary.
    """

    type_code = 17
    type_name: typing.Literal['string'] = "string"
    @classmethod
    def get_raw_types(cls) -> typing.Type[typing.Optional[str]]:
        return cls.raw_types

    raw_types: typing.Type[typing.Optional[str]] = typing.cast(
        typing.Type[typing.Optional[str]], typing.Optional[str]
    )
