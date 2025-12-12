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
import typing_extensions

from .primitivedatatype import PrimitiveDataType
from ..foundation.datatype import TypeCode_Bound, TypeName_Bound

JsonTypes: typing_extensions.TypeAlias = typing_extensions.Union[
    typing_extensions.Mapping[str, "JsonTypes"],
    typing_extensions.Sequence["JsonTypes"],
    str,
    int,
    float,
    bool,
    None,
]
"""
A JSON value.
"""

JsonTypes_Raw: typing_extensions.TypeAlias = typing_extensions.Union[
    typing_extensions.Dict[str, "JsonTypes_Raw"],
    typing_extensions.List["JsonTypes_Raw"],
    str,
    int,
    float,
    bool,
    None,
]
JsonTypes_Var_co = typing_extensions.TypeVar(
    "JsonTypes_Var_co", bound=JsonTypes, covariant=True
)
JsonTypes_Var_contra = typing_extensions.TypeVar(
    "JsonTypes_Var_contra", bound=JsonTypes, contravariant=True
)

T_json = typing_extensions.TypeVar(
    "T_json",
    bound=JsonTypes,
    default=JsonTypes,
    contravariant=True,
)

T_json_upper_bound = typing_extensions.TypeVar(
    "T_json_upper_bound",
    bound=JsonTypes,
    default=JsonTypes,
    contravariant=True,
)

T_json_lower_bound = typing_extensions.TypeVar(
    "T_json_lower_bound",
    bound=JsonTypes,
    default=JsonTypes,
    contravariant=True,
)

T_json_target = typing_extensions.TypeVar(
    "T_json_target",
    bound=JsonTypes,
    default=JsonTypes,
    contravariant=True,
)

TypeCode_Json = typing_extensions.TypeVar(
    "TypeCode_Json", bound=TypeCode_Bound, default=typing.Literal[15]
)
TypeCode_Json_target = typing_extensions.TypeVar(
    "TypeCode_Json_target", bound=TypeCode_Bound, default=typing.Literal[15]
)
TypeName_Json = typing_extensions.TypeVar(
    "TypeName_Json", bound=TypeName_Bound, default=typing.Literal["json"]
)
TypeName_Json_target = typing_extensions.TypeVar(
    "TypeName_Json_target", bound=TypeName_Bound, default=typing.Literal["json"]
)

JsonTypes_Bound = typing.Optional[JsonTypes]
"""
An optional [JsonTypes][diffusion.datatypes.primitives.jsondatatype.JsonTypes] type.
"""

JsonTypes_Raw_Bound = typing.Optional[JsonTypes_Raw]

class JsonDataType(
    PrimitiveDataType[
        T_json
    ],
    typing.Generic[T_json]
):

    type_code: TypeCode_Bound = 15
    type_name: TypeName_Bound = "json"
    raw_types: typing.Type[typing.Optional[T_json]] = typing.cast(
        typing.Type[typing.Optional[T_json]], JsonTypes_Raw
    )


    @classmethod
    def get_raw_types(cls) -> typing.Type[typing.Optional[JsonTypes]]:
        return typing.cast(typing.Type[typing.Optional[JsonTypes]], cls.raw_types)

