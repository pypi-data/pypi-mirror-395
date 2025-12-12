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

import diffusion.internal.pydantic_compat.v1 as pydantic
from typing_extensions import TypeAlias, TYPE_CHECKING

import diffusion.datatypes
from diffusion.datatypes import TimeSeriesEventDataType, TimeSeriesDataType
from diffusion.datatypes.foundation.object import Object
from diffusion.datatypes.foundation.bytesdatatype import Bytes
from diffusion.datatypes.foundation.ibytesdatatype import IBytes
from diffusion.features.topics import IVoidFetch
from diffusion.internal.utils import get_base_type_parameters, validate_member_arguments

if typing.TYPE_CHECKING:
    TimeSeriesOfBytes: TypeAlias = TimeSeriesEventDataType[Bytes]
    """
    A timeseries with Bytes values
    """
else:
    TimeSeriesOfBytes = typing.cast(
        typing.Type[TimeSeriesEventDataType[Bytes]],
        TimeSeriesDataType.of(Bytes),
    )
    """
    A timeseries with Bytes values
    """

FetchQueryValueType_Diffusion = typing.Union[
    diffusion.datatypes.JSON,
    diffusion.datatypes.BINARY,
    diffusion.datatypes.DOUBLE,
    diffusion.datatypes.INT64,
    diffusion.datatypes.STRING,
    diffusion.datatypes.RECORD_V2,
    TimeSeriesOfBytes
]
"""
Concrete Fetch Query Value Types
"""

FetchQueryValueType_Not_WildCard = typing.Union[FetchQueryValueType_Diffusion, IBytes]
"""
Fetch Query Value Type excluding
[wildcards][diffusion.features.topics.fetch.types.FetchQueryValueType_WildCards]
"""

FetchQueryValueType_WildCards = typing.Union[Object, IVoidFetch]
"""
Fetch Query Value Type wildcards
"""

FetchQueryValueType = typing.Union[
    FetchQueryValueType_Not_WildCard, FetchQueryValueType_WildCards
]
"""
A Fetch Query Value type
"""

FetchQueryValueType_Not_IVoidFetch = typing.Union[
    FetchQueryValueType_Not_WildCard, Object
]
"""
A Fetch Query Value type, excluding
[IVoidFetch][diffusion.features.topics.fetch.fetch_common.IVoidFetch]
"""


class FQVTWrapper(pydantic.BaseModel):
    value: typing.Type[FetchQueryValueType_Not_WildCard]

    class Config(pydantic.BaseConfig):
        frozen = True

    @classmethod
    def acceptable_time_series_value_types(cls) -> typing.FrozenSet[typing.Type]:
        return frozenset({Bytes})

    @classmethod
    def validate_tp(
        cls, val: typing.Type[FetchQueryValueType_Not_WildCard]
    ) -> typing.Type[FetchQueryValueType_Not_WildCard]:
        from diffusion.datatypes.timeseries import (
            TimeSeriesEventDataType,
            TimeSeriesDataType,
        )
        from diffusion.datatypes.conversion.default import DEFAULT_CONVERTER
        from diffusion.datatypes.timeseries import TimeSeriesValueType

        @validate_member_arguments
        def validator(
            val_to_check: typing.Type[FetchQueryValueType_Not_WildCard],
        ) -> typing.Type[FetchQueryValueType_Not_WildCard]:
            return val_to_check

        validator(val)
        val_to_check = val
        if issubclass(val_to_check, TimeSeriesEventDataType):
            ivt: typing.Type[TimeSeriesValueType] = typing.cast(
                typing.Type[TimeSeriesValueType],
                DEFAULT_CONVERTER(val_to_check.inner_value_type()),
            )
            if ivt not in cls.acceptable_time_series_value_types():
                raise ValueError(
                    f"Got {ivt.__qualname__} for FetchQuery TimeSeries inner value type, "
                    "can't specify something of other than "
                    f"{cls.acceptable_time_series_value_types()}"
                )
            return TimeSeriesDataType.of(typing.cast(typing.Type[Bytes], ivt))
        try:
            return typing.cast(
                typing.Type[FetchQueryValueType_Not_WildCard],
                DEFAULT_CONVERTER(val_to_check),
            )
        except Exception as e:
            raise ValueError(f"{val_to_check} is not a valid fetch query value type") from e

    @classmethod
    def __get_validators__(cls):
        def convert(val: typing.Type[FetchQueryValueType_Not_WildCard]) -> FQVTWrapper:
            return FQVTWrapper(value=cls.validate_tp(val))

        yield convert


UnfrozenTopicTypeSet = typing.Set[typing.Type[FetchQueryValueType_Not_WildCard]]
"""
A set of [Fetch Query Value Types, not including wildcards]
[diffusion.features.topics.fetch.types.FetchQueryValueType_Not_WildCard]
"""

FrozenTopicTypeSet = typing.FrozenSet[typing.Type[FetchQueryValueType_Not_WildCard]]

"""
A frozen set of [Fetch Query Value Types, not including wildcards]
[diffusion.features.topics.fetch.types.FetchQueryValueType_Not_WildCard]
"""

TopicTypeSet_Internal: TypeAlias = FrozenTopicTypeSet

if TYPE_CHECKING:
    TopicTypeSet = typing.Union[FrozenTopicTypeSet, UnfrozenTopicTypeSet]
    """
    Type alias of
    typing.Union[[FrozenTopicTypeSet][diffusion.features.topics.fetch.types.FrozenTopicTypeSet],
    [FrozenTopicTypeSet][diffusion.features.topics.fetch.types.UnfrozenTopicTypeSet]]
    """
else:
    TopicTypeSet = typing.cast(
        typing.Type[FrozenTopicTypeSet], pydantic.confrozenset(FQVTWrapper, min_items=1)
    )

ALL_TOPIC_TYPES = typing.cast(
    TopicTypeSet_Internal, frozenset(get_base_type_parameters(FetchQueryValueType))
)

ALL_TOPIC_TYPES_NOT_IVOIDFETCH = typing.cast(
    TopicTypeSet_Internal,
    frozenset(get_base_type_parameters(FetchQueryValueType_Not_IVoidFetch)),
)

ALL_TOPIC_TYPES_NOT_WILDCARD = typing.cast(
    TopicTypeSet_Internal,
    frozenset(get_base_type_parameters(FetchQueryValueType_Not_WildCard)),
)

FETCH_QUERY_WILDCARDS = typing.cast(
    TopicTypeSet_Internal,
    frozenset(get_base_type_parameters(FetchQueryValueType_WildCards)),
)

TValue = typing.TypeVar("TValue", bound=FetchQueryValueType)
"""
Value type of a fetch query
"""

TNewValue = typing.TypeVar("TNewValue", bound=FetchQueryValueType)
"""
New value type of a fetch query
"""

TValue_Not_WildCard = typing.TypeVar(
    "TValue_Not_WildCard", bound=FetchQueryValueType_Not_WildCard, covariant=True
)
"""
A Fetch Query Value type, but not a wildcard
"""

TNewValue_Not_WildCard = typing.TypeVar(
    "TNewValue_Not_WildCard", bound=FetchQueryValueType_Not_WildCard
)
"""
A new Fetch Query Value type, but not a wildcard
"""

TNewValue_Not_IVoidFetch = typing.TypeVar(
    "TNewValue_Not_IVoidFetch", bound=FetchQueryValueType_Not_IVoidFetch
)
"""
A new Fetch Query Value type, but not an IVoidFetch
"""

TNewValue_Not_WildCard_Other = typing.TypeVar(
    "TNewValue_Not_WildCard_Other", bound=FetchQueryValueType_Not_WildCard
)

"""
Another Fetch Query Value type, but not a wildcard
"""

