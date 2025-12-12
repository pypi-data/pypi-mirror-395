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

from diffusion.datatypes import AbstractDataType
from diffusion.datatypes.foundation.abstract import ValueType_target
if typing.TYPE_CHECKING:
    from diffusion.features.topics.fetch.types import (
        FetchQueryValueType_WildCards,
    )


class GenericConverter(typing.Protocol, typing.Hashable):
    """
    A datatype converter, takes end user types and returns valid Diffusion types
    """
    @typing_extensions.overload
    def __call__(
        self, source_type: typing.Type[FetchQueryValueType_WildCards]
    ) -> typing.Optional[typing.Type[AbstractDataType]]:
        ...

    @typing_extensions.overload
    def __call__(
        self,
        source_type: typing.Union[
            typing.Type[ValueType_target],
            typing.Type[
                AbstractDataType[typing.Any, ValueType_target, typing.Any]
            ],
        ],
    ) -> typing.Optional[
        typing.Type[AbstractDataType[typing.Any, ValueType_target, typing.Any]],
    ]:
        ...

    def __call__( # type: ignore[misc]
        self,
        source_type: typing.Union[
            typing.Type[FetchQueryValueType_WildCards],
            typing.Type[ValueType_target],
            typing.Type[
                AbstractDataType[typing.Any, ValueType_target, typing.Any]
            ],
        ],
    ) -> typing.Union[
        typing.Optional[typing.Type[AbstractDataType]],
        typing.Type[AbstractDataType[typing.Any, ValueType_target, typing.Any]],
    ]:
        pass  # pragma: no cover

    @typing_extensions.overload
    def maybe_concrete_type(
        self, source_type: typing.Type[FetchQueryValueType_WildCards]
    ) -> typing.Optional[typing.Type[AbstractDataType]]:
        ...

    @typing_extensions.overload
    def maybe_concrete_type(
        self,
        source_type: typing.Union[
            typing.Type[ValueType_target],
            typing.Type[
                AbstractDataType[typing.Any, ValueType_target, typing.Any]
            ],
        ],
    ) -> typing.Optional[
        typing.Type[AbstractDataType[typing.Any, ValueType_target, typing.Any]],
    ]:
        ...

    def maybe_concrete_type(
        self,
        source_type: typing.Union[
            typing.Type[FetchQueryValueType_WildCards],
            typing.Type[ValueType_target],
            typing.Type[
                AbstractDataType[typing.Any, ValueType_target, typing.Any]
            ],
        ],
    ) -> typing.Optional[
        typing.Union[
            typing.Type[ValueType_target],
            typing.Type[
                AbstractDataType[typing.Any, ValueType_target, typing.Any]
            ],
            typing.Type[AbstractDataType],
        ]
    ]:
        pass  # pragma: no cover
