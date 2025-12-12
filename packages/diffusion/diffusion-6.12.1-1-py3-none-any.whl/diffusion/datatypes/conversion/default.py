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

import diffusion.internal.pydantic_compat.v1 as pydantic

from diffusion.datatypes.foundation.object import Object
from diffusion.datatypes.foundation.abstract import (
    AbstractDataType,
    ValueType_target,
)
from diffusion.datatypes.foundation.ibytesdatatype import IBytes
if typing.TYPE_CHECKING:
    from diffusion.features.topics.fetch.types import FetchQueryValueType_WildCards, \
        TValue_Not_WildCard
from diffusion.internal.utils import (
    VeryStrictConfig,
)

AT_T_Or_WildCard = typing.Union[AbstractDataType, IBytes, "FetchQueryValueType_WildCards"]


class StrictDefaultConverter(object):
    def __init__(self) -> None:
        self.mappings: typing.Dict[typing.Type, typing.Type[AbstractDataType]] = {
            object: Object
        }

    @typing_extensions.overload
    def __call__(
        self,
        source_type: typing.Type[FetchQueryValueType_WildCards]
    ) -> typing.Type[AbstractDataType]: ...

    @typing_extensions.overload
    def __call__(
        self,
        source_type: typing.Union[
            typing.Type[ValueType_target],
            typing.Type[AbstractDataType[typing.Any, ValueType_target, typing.Any]],
        ],
    ) -> typing.Type[AbstractDataType[typing.Any, ValueType_target, typing.Any]]: ...

    def __call__(
        self, source_type: typing.Union[
            typing.Type[FetchQueryValueType_WildCards],
            typing.Type[ValueType_target],
            typing.Type[AbstractDataType[typing.Any, ValueType_target, typing.Any]],
        ],
    ) -> typing.Union[typing.Type[TValue_Not_WildCard], typing.Type[AbstractDataType]]:

        result = self.mappings.get(source_type)
        if result:
            return result

        @pydantic.validate_arguments(config=VeryStrictConfig)
        def abstract_data_type_fallback(
            source_type: typing.Type[AbstractDataType],
        ) -> typing.Type[AbstractDataType]:
            return source_type

        result = abstract_data_type_fallback(
            typing.cast(typing.Type[AbstractDataType], source_type)
        )
        self.mappings[source_type] = result
        return result

    @typing_extensions.overload
    def maybe_concrete_type(
        self,
        source_type: typing.Type[FetchQueryValueType_WildCards]
    ) -> typing.Optional[
        typing.Type[AbstractDataType]
    ]: ...

    @typing_extensions.overload
    def maybe_concrete_type(
        self,
        source_type: typing.Union[
            typing.Type[ValueType_target],
            typing.Type[AbstractDataType[typing.Any, ValueType_target, typing.Any]]
        ],
    ) -> typing.Optional[
        typing.Type[AbstractDataType[typing.Any, ValueType_target, typing.Any]],
    ]: ...

    def maybe_concrete_type(
        self,
        source_type: typing.Union[
            typing.Type[FetchQueryValueType_WildCards],
            typing.Type[ValueType_target],
            typing.Type[AbstractDataType[typing.Any, ValueType_target, typing.Any]]
        ],
    ) -> typing.Optional[
        typing.Union[
            typing.Type[ValueType_target],
            typing.Type[AbstractDataType[typing.Any, ValueType_target, typing.Any]],
            typing.Type[AbstractDataType],
        ]
    ]:
        try:
            return typing.cast(
                typing.Union[
                    typing.Type[ValueType_target],
                    typing.Type[
                        AbstractDataType[typing.Any, ValueType_target, typing.Any]
                    ],
                    typing.Type[AbstractDataType],
                ],
                self(typing.cast(typing.Type[AT_T_Or_WildCard], source_type)),
            )
        except pydantic.ValidationError:
            return None


class DefaultConverter(StrictDefaultConverter):
    pass


STRICT_DEFAULT_CONVERTER = StrictDefaultConverter()
DEFAULT_CONVERTER = DefaultConverter()
