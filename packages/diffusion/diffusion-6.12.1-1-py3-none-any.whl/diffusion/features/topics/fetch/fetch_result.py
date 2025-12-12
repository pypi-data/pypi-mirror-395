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

import functools
import traceback
import typing
from collections.abc import Hashable
from typing import Optional, List

from diffusion.datatypes.foundation.datatype import TypeName_Bound
import diffusion.internal.pydantic_compat.v1 as pydantic
import stringcase  # type: ignore[import-untyped]
import typing_extensions

from diffusion.datatypes.foundation.object import Object
from diffusion.datatypes.conversion.default import DEFAULT_CONVERTER
from diffusion.internal.pydantic_compat.v1 import dataclasses as pydantic_dataclasses

import diffusion.datatypes
from diffusion.datatypes.foundation.abstract import (
    AbstractDataType,
)
from diffusion.datatypes.conversion import GenericConverter
from diffusion.datatypes.foundation.ibytesdatatype import IBytes
from diffusion.datatypes.foundation.bytesdatatype import Bytes
from diffusion.datatypes.timeseries import (
    TimeSeriesDataType,
    TimeSeriesEventDataType,
    TimeSeriesValueType,
)
from diffusion.features.topics.details.topic_specification import (
    PropertyMap,
    TopicSpecification,
)
from diffusion.features.topics.fetch.fetch_common import IVoidFetch
from diffusion.features.topics.fetch.types import (
    TNewValue,
    TNewValue_Not_WildCard,
    FetchQueryValueType_Diffusion,
    FetchQueryValueType_Not_WildCard,
    TValue,
    FetchQueryValueType_WildCards,
    FetchQueryValueType,
    TValue_Not_WildCard,
    TNewValue_Not_WildCard_Other,
    ALL_TOPIC_TYPES_NOT_WILDCARD,
)
from diffusion.features.topics.fetch.fetch_query_result import StringMap

from diffusion.handlers import LOG

if typing.TYPE_CHECKING:  # pragma: no cover
    from diffusion.features.topics.fetch.fetch_query_result import FetchQueryResult
from diffusion.internal.utils import BaseConfig


@pydantic_dataclasses.dataclass(frozen=True, config=BaseConfig, validate_on_init=True)
class TopicResult(typing.Generic[TValue_Not_WildCard]):
    """
    The result of a [FetchRequest.fetch][diffusion.features.topics.fetch.fetch_result.FetchResult] invocation for a single selected topic.
    """  # noqa: E501
    tp_: typing.ClassVar[type]
    path: str
    """
    The topic path.
    """

    specification: TopicSpecification
    """
    The topic specification.

    Notes:
        If the request specified [FetchRequest.with_properties][diffusion.features.topics.fetch.fetch_request.FetchRequest.with_properties], the result reflects the topic's
        specification and can be used to create an identical topic. If the request did not specify
        [FetchRequest.with_properties][diffusion.features.topics.fetch.fetch_request.FetchRequest.with_properties], the specification's property map will be empty.
    """  # noqa: E501
    value: typing.Optional[TValue_Not_WildCard]
    """
    The topic value or <c>None</c> if none available.
    """

    @property
    def type(self) -> typing.Type[TValue_Not_WildCard]:
        """
        Gets the topic type.

        Returns:
            The topic type.
        """
        return self.specification.topic_type

    @property
    def properties(self) -> PropertyMap:
        return self.specification.properties

    @classmethod
    def create(
        cls,
        path: pydantic.StrictStr,
        specification: TopicSpecification,
        value: typing.Optional[TValue_Not_WildCard],
    ) -> TopicResult[TValue_Not_WildCard]:
        try:
            return cls(path, specification, value)
        except Exception as e:
            LOG.error(f"Got {e}: {traceback.format_exc()}")
            raise

    def __repr__(self):
        """"""
        return (
            f"{type(self).__name__}(path='{self.path}', type={self.type}, "
            f"value={repr(self.value)}, specification={self.specification})"
        )

    @classmethod
    def of(
        cls, tp: typing.Type[TNewValue_Not_WildCard]
    ) -> typing.Type[TopicResult[TNewValue_Not_WildCard]]:
        assert isinstance(tp, typing.Hashable)
        return cls._of(tp)

    @classmethod
    @functools.lru_cache(maxsize=None)
    def _of(cls, tp):
        return typing.cast(
            typing.Type[TopicResult[TNewValue_Not_WildCard]],
            type(stringcase.pascalcase(f"{tp}{cls.__name__}"), (cls,), dict(tp_=tp)),
        )


@pydantic_dataclasses.dataclass(frozen=True, config=BaseConfig)
class FetchResult(typing.Generic[TValue]):
    """
    The [FetchResult[TValue]][diffusion.features.topics.fetch.fetch_result.FetchResult] implementation.
    """  # NOQA: E501
    @classmethod
    def time_series_data_type(cls) -> typing.Type[TimeSeriesEventDataType[Bytes]]:
        return TimeSeriesDataType.of(Bytes)

    @classmethod
    def create(
        cls: typing.Type[FetchResult],
        tp_raw: typing.Type[TNewValue],
        result: FetchQueryResult,
        generic_converter: Optional[GenericConverter] = None
    ) -> FetchResult[TNewValue]:
        """
        Creates a [FetchResult[TNewValue]]
        [diffusion.features.topics.fetch.fetch_result.FetchResult].

        Args:
            tp_raw: The type of the result.
            result: The fetch query result.
            generic_converter: Custom type converter.

        Returns:
            The newly created fetch result.
        """

        generic_converter = generic_converter or DEFAULT_CONVERTER
        tp = typing.cast(typing.Type[TNewValue], generic_converter(tp_raw))
        if result is None:
            raise ValueError("result")
        properties = result.properties
        result_list: List[TopicResult[FetchQueryValueType_Not_WildCard]] = []
        for topic_result in result.results:
            bytes_value = topic_result.value
            properties_map: StringMap = (
                StringMap()
                if len(properties) == 0
                else properties[topic_result.properties_index]
            )
            topic_tp: typing.Type[FetchQueryValueType_Not_WildCard]
            value_type_concrete: typing.Optional[
                typing.Type[FetchQueryValueType_Not_WildCard]
            ]
            value: typing.Optional[FetchQueryValueType_Not_WildCard]
            try:
                value, value_type_concrete, topic_tp = cls.read_as_typed(
                    typing.cast(
                        typing.Type[
                            typing.Union[
                                FetchQueryValueType_Not_WildCard,
                                FetchQueryValueType_WildCards,
                            ]
                        ],
                        tp,
                    ),
                    Bytes.maybe_from_bytes(bytes_value),
                    topic_result.type,
                    properties_map,
                    generic_converter,
                )
            except ValueError as e:
                LOG.error(f"Got {e}: {traceback.format_exc()}")
                continue
            spec = typing.cast(
                typing.Type[AbstractDataType], value_type_concrete
            ).with_properties(**dict(properties_map))

            def apply_addition(
                dest_tp: typing.Type[TNewValue_Not_WildCard_Other],
            ) -> TopicResult[TNewValue_Not_WildCard_Other]:
                topic_result_type = typing.cast(
                    typing.Type[TopicResult[TNewValue_Not_WildCard_Other]],
                    TopicResult.of(dest_tp),
                )
                return topic_result_type.create(
                    topic_result.path,
                    spec,
                    typing.cast(typing.Optional[TNewValue_Not_WildCard_Other], value),
                )

            result_list.append(apply_addition(topic_tp))
        return cls.of(tp)(
            tuple(
                typing.cast(
                    typing.Iterable[TopicResult[FetchQueryValueType_Not_WildCard]],
                    result_list,
                )
            ),
            result.has_more,
        )

    @classmethod
    def get_timeseries_type(
        cls,
        tp: typing.Type[FetchQueryValueType],
        properties_map: StringMap,
    ) -> typing.Type[TimeSeriesEventDataType[TimeSeriesValueType]]:
        return cls.normalise_as_timeseries_type(tp)

    @classmethod
    def normalise_as_timeseries_type(
        cls, tp: typing.Type[FetchQueryValueType]
    ) -> typing.Type[TimeSeriesEventDataType[TimeSeriesValueType]]:
        if issubclass(tp, TimeSeriesEventDataType):
            topic_tp = TimeSeriesDataType.of(cls.get_concrete_type(tp.inner_value_type()))
        else:
            topic_tp = TimeSeriesDataType.of(cls.get_concrete_type(tp))
        return topic_tp

    @classmethod
    def get_concrete_type(cls, tp):
        return {IBytes: Bytes, Object: Bytes, IVoidFetch: Bytes}.get(tp, tp)

    @classmethod
    def of(cls, tp: typing.Type[TNewValue]) -> typing.Type[FetchResult[TNewValue]]:
        assert isinstance(tp, Hashable)
        return cls._of(tp)

    @classmethod
    @functools.lru_cache(maxsize=None)
    def _of(cls, tp: typing.Type[TNewValue]) -> typing.Type[FetchResult[TNewValue]]:
        return typing.cast(
            typing.Type[FetchResult[TNewValue]],
            type(
                stringcase.pascalcase(f"{tp.__name__}{cls.__name__}"),
                (cls,),
                dict(_tp=tp),
            ),
        )

    @classmethod
    def from_time_series(
        cls,
        value_type: typing.Type[FetchQueryValueType],
        value_type_of_timeseries: typing.Type[TimeSeriesEventDataType[TimeSeriesValueType]],
        bytes_value: bytes,
    ) -> typing.Tuple[
        typing.Optional[FetchQueryValueType_Not_WildCard],
        typing.Optional[typing.Type[FetchQueryValueType_Not_WildCard]],
    ]:
        value_internal: typing.Optional[FetchQueryValueType_Not_WildCard]
        value_type_concrete: typing.Optional[
            typing.Type[FetchQueryValueType_Not_WildCard]
        ] = None


        try:

            assert value_type_of_timeseries is not None
            materialised: TimeSeriesEventDataType[
                TimeSeriesValueType
            ] = value_type_of_timeseries.from_bytes(bytes_value)
            if issubclass(value_type, (TimeSeriesEventDataType, Object)):
                value_type_concrete = value_type_of_timeseries
                value_internal = materialised
            else:
                value_type_concrete = materialised.inner_value_type()
                assert value_type_concrete in ALL_TOPIC_TYPES_NOT_WILDCARD | {Bytes}
                value_internal = typing.cast(
                    typing.Optional[FetchQueryValueType_Not_WildCard],
                    materialised.value.value if materialised.value else None
                )

        except Exception as exc:
            raise ValueError(
                f"Incompatible value of type {value_type_concrete}."
            ) from exc
        return value_internal, value_type_concrete

    @classmethod
    def infer_value_type_if_timeseries(
            cls,
            value_type: typing.Type[FetchQueryValueType],
            data_type: typing.Type[TimeSeriesEventDataType[TimeSeriesValueType]],
    ) -> typing.Type[TimeSeriesEventDataType[TimeSeriesValueType]]:
        if value_type in {Object, IVoidFetch}:
            if data_type.inner_value_type() in {Object, IVoidFetch}:
                return TimeSeriesDataType.of(Bytes)
            return typing.cast(
                typing.Type[TimeSeriesEventDataType[TimeSeriesValueType]], data_type
            )
        elif issubclass(value_type, TimeSeriesEventDataType):
            if value_type.inner_value_type() in {Object}:
                return TimeSeriesDataType.of(Bytes)
            return TimeSeriesDataType.of(cls.get_concrete_type(value_type.inner_value_type()))
        else:
            return TimeSeriesDataType.of(cls.get_concrete_type(value_type))

    @classmethod
    @typing_extensions.overload
    def read_as(
        cls,
        value_type: typing.Type[TNewValue_Not_WildCard],
        bytes_value: typing.Optional[bytes],
        data_type: typing.Type[FetchQueryValueType_Not_WildCard],
        generic_converter: typing.Optional[GenericConverter] = None,
    ) -> typing.Optional[TNewValue_Not_WildCard]:
        pass  # pragma: no cover

    @classmethod
    @typing_extensions.overload
    def read_as(
        cls,
        value_type: typing.Type[FetchQueryValueType_WildCards],
        bytes_value: typing.Optional[bytes],
        data_type: typing.Type[FetchQueryValueType_Not_WildCard],
        generic_converter: typing.Optional[GenericConverter] = None,
    ) -> typing.Optional[FetchQueryValueType_Not_WildCard]:
        pass  # pragma: no cover

    @classmethod
    def read_as(
        cls,
        value_type: typing.Type[
            typing.Union[TNewValue_Not_WildCard, FetchQueryValueType_WildCards]
        ],
        bytes_value: typing.Optional[bytes],
        data_type: typing.Type[FetchQueryValueType_Not_WildCard],
        generic_converter: typing.Optional[GenericConverter] = None,
    ) -> typing.Optional[
        FetchQueryValueType_Not_WildCard
    ]:
        """
        Args:
            value_type:
            bytes_value:
            data_type:
            generic_converter:
        """
        value, value_type_concrete, topic_tp = cls.read_as_typed(
            value_type,
            Bytes.maybe_from_bytes(bytes_value),
            data_type,
            generic_converter=generic_converter
        )
        return typing.cast(
            typing.Optional[
                typing.Union[TNewValue_Not_WildCard, FetchQueryValueType_Not_WildCard]
            ],
            value,
        )

    @classmethod
    @typing_extensions.overload
    def read_as_typed(
        cls,
        value_type: typing.Type[
            FetchQueryValueType_WildCards
        ],
        bytes_value: typing.Optional[IBytes],
        topic_tp_raw: typing.Type[FetchQueryValueType_Not_WildCard],
        properties_map: typing.Optional[StringMap] = None,
        generic_converter: typing.Optional[GenericConverter] = None
    ) -> typing.Tuple[
        typing.Optional[
            FetchQueryValueType_Not_WildCard
        ],
        typing.Optional[typing.Type[FetchQueryValueType_Not_WildCard]],
        typing.Type[FetchQueryValueType_Not_WildCard]
    ]: ...  # pragma: no cover

    @classmethod
    @typing_extensions.overload
    def read_as_typed(
        cls,
        value_type: typing.Type[
            TNewValue_Not_WildCard
        ],
        bytes_value: typing.Optional[IBytes],
        topic_tp_raw: typing.Type[FetchQueryValueType_Not_WildCard],
        properties_map: typing.Optional[StringMap] = None,
        generic_converter: typing.Optional[GenericConverter] = None
    ) -> typing.Tuple[
        typing.Optional[
            TNewValue_Not_WildCard
        ],
        typing.Optional[typing.Type[TNewValue_Not_WildCard]],
        typing.Type[FetchQueryValueType_Not_WildCard]
    ]: ...  # pragma: no cover

    @classmethod
    def read_as_typed(
        cls,
        value_type: typing.Type[
            typing.Union[TNewValue_Not_WildCard, FetchQueryValueType_WildCards]
        ],
        bytes_value: typing.Optional[IBytes],
        topic_tp_raw: typing.Type[FetchQueryValueType_Not_WildCard],
        properties_map: typing.Optional[StringMap] = None,
        generic_converter: typing.Optional[GenericConverter] = None
    ) -> typing.Union[
        typing.Tuple[
            typing.Optional[
                FetchQueryValueType_Not_WildCard
            ],
            typing.Optional[typing.Type[FetchQueryValueType_Not_WildCard]],
            typing.Type[FetchQueryValueType_Not_WildCard]
        ],
        typing.Tuple[
            typing.Optional[
                TNewValue_Not_WildCard
            ],
            typing.Optional[typing.Type[TNewValue_Not_WildCard]],
            typing.Type[FetchQueryValueType_Not_WildCard]
        ]
    ]:
        generic_converter = generic_converter or DEFAULT_CONVERTER
        properties_map = properties_map or StringMap()

        value: typing.Optional[FetchQueryValueType_Not_WildCard]
        value_type_concrete: typing.Optional[typing.Type[FetchQueryValueType_Not_WildCard]]
        data_type: typing.Type[FetchQueryValueType_Not_WildCard]
        data_type_as_timeseries: typing.Optional[
            typing.Type[TimeSeriesEventDataType[TimeSeriesValueType]]
        ]
        converted_raw_type = typing.cast(
            typing.Type[FetchQueryValueType_Diffusion],
            generic_converter(topic_tp_raw),
        )
        converted_value_type = typing.cast(
            typing.Type[FetchQueryValueType_Diffusion],
            generic_converter(value_type))

        data_type, data_type_as_timeseries = cls.infer_topic_type_precise(
            converted_raw_type, converted_value_type, properties_map
        )

        if bytes_value is None:
            if value_type in {Object, IVoidFetch}:
                value_type_concrete = data_type
            else:
                value_type_concrete = typing.cast(
                    typing.Type[FetchQueryValueType_Not_WildCard], value_type
                )

            value = cls.get_default(value_type_concrete)
        elif issubclass(topic_tp_raw, diffusion.datatypes.TIME_SERIES):
            try:
                assert data_type_as_timeseries is not None
                value, value_type_concrete = cls.from_time_series(
                    value_type,
                    data_type_as_timeseries,
                    bytes_value.to_bytes()
                )
            except Exception as e:
                LOG.error(f"Got {e}: {traceback.format_exc()}")
                raise
        else:
            if value_type in {Object, IBytes}:
                value_type_concrete = data_type
            else:
                value_type_concrete = typing.cast(
                    typing.Type[FetchQueryValueType_Not_WildCard], value_type
                )
            try:
                value = typing.cast(
                    FetchQueryValueType_Not_WildCard,
                    data_type.read_as(
                        typing.cast(
                            typing.Type[FetchQueryValueType_Not_WildCard],
                            value_type_concrete,
                        ),
                        bytes_value,
                    ),
                )
            except Exception as e:
                raise ValueError(f"Incompatible value of type {value_type}.") from e
        if value and value_type_concrete:
            assert isinstance(value, value_type_concrete)
        return value, value_type_concrete, data_type

    @classmethod
    def infer_topic_type_precise(
        cls,
        topic_type: typing.Type[FetchQueryValueType_Not_WildCard],
        value_type: typing.Type[FetchQueryValueType],
        properties_map: StringMap,
    ) -> typing.Tuple[
        typing.Type[FetchQueryValueType_Not_WildCard],
        typing.Optional[typing.Type[TimeSeriesEventDataType[TimeSeriesValueType]]],
    ]:
        data_type: typing.Type[FetchQueryValueType_Not_WildCard]
        value_type_if_timeseries: typing.Optional[
            typing.Type[TimeSeriesEventDataType[TimeSeriesValueType]]
        ] = None
        if issubclass(topic_type, TimeSeriesEventDataType):

            data_type_as_timeseries = cls.get_timeseries_type(
                value_type, properties_map
            )
            value_type_if_timeseries = cls.infer_value_type_if_timeseries(
                value_type, data_type_as_timeseries
            )
            if issubclass(value_type, TimeSeriesEventDataType):
                data_type = data_type_as_timeseries
            else:
                data_type = topic_type
        else:
            LOG.info(f"{topic_type} is already determined")
            data_type = topic_type
        return (
            typing.cast(typing.Type[FetchQueryValueType_Diffusion], data_type),
            value_type_if_timeseries,
        )

    @classmethod
    def get_default(
        cls, value_type: typing.Optional[typing.Type[FetchQueryValueType]]
    ) -> typing.Optional[FetchQueryValueType_Not_WildCard]:
        default_func = getattr(value_type, "default", None)
        value = default_func() if default_func else None
        return value

    @property
    def count(self):
        return len(self.results)

    @property
    def is_empty(self):
        return len(self.results) == 0

    results: typing.Tuple[TopicResult[FetchQueryValueType_Not_WildCard], ...]
    """
    The results
    """

    has_more: bool
    """
    Whether there are more results
    """

    def __repr__(self):
        return (
            f"{type(self).__name__}(has_more={self.has_more}, results={self.results})"
        )

    def __len__(self):
        return len(self.results)


class DecodedFetchResult(FetchResult[TValue], typing.Generic[TValue]):
    @classmethod
    def get_timeseries_type(
        cls,
        tp: typing.Type[FetchQueryValueType],
        properties_map: StringMap,
    ) -> typing.Type[TimeSeriesEventDataType[TimeSeriesValueType]]:
        tsv = dict(properties_map).pop("TIME_SERIES_EVENT_VALUE_TYPE", None)
        inner_value_type = (
            diffusion.datatypes.get(
                typing.cast(TypeName_Bound, tsv)
            )
            if tsv
            else None
        )

        if not inner_value_type:
            topic_tp = cls.normalise_as_timeseries_type(tp)
        else:
            topic_tp = TimeSeriesDataType.of(
                typing.cast(typing.Type[TimeSeriesValueType], inner_value_type)
            )
            LOG.info(f"Already got type {topic_tp}")
        return topic_tp
