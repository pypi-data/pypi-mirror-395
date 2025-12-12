#  Copyright (c) 2022 - 2025 DiffusionData Ltd., All Rights Reserved.
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
import typing

import diffusion.internal.pydantic_compat.v1 as pydantic
import stringcase  # type: ignore

from typing_extensions import Literal, Any

from io import BytesIO

from diffusion.datatypes.foundation.bytesdatatype import Bytes
from diffusion.datatypes.foundation.ibytesdatatype import IBytes
from diffusion.datatypes.foundation.object import Object
from diffusion.datatypes.foundation.abstract import (
    AbstractDataType,
    Converter,
    ValueType,
    ValueType_target,
    WithProperties,
    WithProperties_Value_T,
    RealValue,
)

import diffusion.features.topics.details.topic_specification as topic_specification
from diffusion.features.topics.details.topic_specification import (
    T, T_other, ConflationPolicy
)

from diffusion.internal.utils import (
    validate_member_arguments,
)

from diffusion.datatypes.timeseries.time_series_event import EventTypeFactory, Event
from diffusion.datatypes.timeseries.types import (
    VT,
    TimeSeriesValueType,
    TimeSeriesValueType_Diffusion,
    TimeSeriesValueTypeClasses, TimeSeriesValueTypeOrRaw,
)
from diffusion.datatypes.timeseries.time_series_event_metadata import (
    EventMetadata,  # noqa: F401
)

import diffusion.datatypes


class TopicSpecification(
    typing.Generic[T],
    topic_specification.TopicSpecification[T],
):
    """
    Time Series Topic Specification class
    """

    TIME_SERIES_EVENT_VALUE_TYPE: typing.Type[TimeSeriesValueType]
    """
    Specifies the event data type for a time series topic.
    """

    TIME_SERIES_RETAINED_RANGE: typing.Optional[str] = None
    """
    Key of the topic property that specifies the range of events retained by
    a time series topic.

    When a new event is added to the time series, older events that fall
    outside of the range are discarded.

    If the property is not specified, a time series topic will retain the ten
    most recent events.

    ## Time series range expressions

    The property value is a time series <em>range expression</em> string
    composed of one or more constraint clauses. Constraints are combined to
    provide a range of events from the end of the time series.

    ## '**limit**' constraint

    A `limit` constraint specifies the maximum number of events from the
    end of the time series.

    ## '**last**' constraint

    A `last` constraint specifies the maximum duration of events from the
    end of the time series. The duration is expressed as an integer followed
    by one of the following time units.

    - `ms` - milliseconds
    - `s` - seconds
    - `h` - hours

    If a range expression contains multiple constraints, the constraint that
    selects the smallest range is used.

    | Property value     | Meaning                                                                                    |
    |--------------------|--------------------------------------------------------------------------------------------|
    | `limit 5`          | The five most recent events                                                                |
    | `last 10s`         | All events that are no more than ten seconds older than the latest event                   |
    | `last 10s limit 5` | The five most recent events that are no more than ten seconds older than the latest event  |

    Range expressions are not case sensitive:
    ```
    limit 5 last 10s
    ```
    is equivalent to

    ```
    LIMIT 5 LAST 10S
    ```.

    Since 6.8.3
    """  # NOQA: E501
    TIME_SERIES_SUBSCRIPTION_RANGE: typing.Optional[str] = None
    """
    Key of the topic property that specifies the range of time series topic
    events to send to new subscribers.

    The property value is a time series range expression, following the
    format used for
    [TIME_SERIES_RETAINED_RANGE]
    [diffusion.datatypes.timeseries.TopicSpecification.TIME_SERIES_RETAINED_RANGE].

    If the property is not specified, new subscribers will be sent the latest
    event if delta streams are enabled and no events if delta streams are
    disabled. See the description of <em>Subscription range</em> in the
    {@link TimeSeries time series feature} documentation.

    Since 6.8.3
    """

    CONFLATION: typing.Optional[
        Literal[ConflationPolicy.OFF, ConflationPolicy.UNSUBSCRIBE]
    ] = None
    """
    TimeSeries conflation policy is restricted to the above.

    See Also:
        [diffusion.features.topics.details.topic_specification.TopicSpecification.CONFLATION][]
    """

    @property
    def topic_type(self):
        # noinspection PyProtectedMember
        return TimeSeriesDataType.of(
            typing.cast(typing.Type[T], self.TIME_SERIES_EVENT_VALUE_TYPE)
        )

    # noinspection PyUnusedLocal,PyNestedDecorators
    @pydantic.validator("TIME_SERIES_EVENT_VALUE_TYPE", pre=True)
    @classmethod
    def validate_ts(
        cls,
        field_value: typing.Type[VT],
        values: typing.Dict[str, typing.Any],
        field,
        config,
    ) -> typing.Type[VT]:
        return typing.cast(
            typing.Type[VT],
            diffusion.datatypes.get(
                typing.cast(
                    diffusion.datatypes.DataTypeArgument,
                    field_value,
                )
            ),
        )

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def _spec_class(
        cls, tp: typing.Type[T_other]
    ) -> typing.Type[topic_specification.TopicSpecification[T_other]]:
        from diffusion.datatypes.conversion.default import DEFAULT_CONVERTER
        tp_final: typing.Type[AbstractDataType] = DEFAULT_CONVERTER(tp)
        class Result(TopicSpecification):
            TIME_SERIES_EVENT_VALUE_TYPE: typing.Type[
                TimeSeriesValueType_Diffusion
            ] = pydantic.Field(
                default=typing.cast(
                    typing.Type[TimeSeriesValueType_Diffusion],
                    typing.cast(TimeSeriesEventDataType, tp_final).inner_value_type(),
                )
            )

        assert isinstance(tp_final, typing.Hashable)
        return typing.cast(
            typing.Type[topic_specification.TopicSpecification[T_other]],
            topic_specification.TopicSpecification._spec_class(Result, tp_final),
        )


def fake_own_type() -> typing.Type[TimeSeriesValueType_Diffusion]:
    raise NotImplementedError()  # pragma: no cover


@typing.final
class TopicSpecificationAuto(typing.Generic[T], TopicSpecification[T]):
    TIME_SERIES_EVENT_VALUE_TYPE: typing.Type[TimeSeriesValueType_Diffusion] = pydantic.Field(
        const=True, default_factory=fake_own_type
    )
    """
    Specifies the event data type for a time series topic.
    """


@typing.final
class TimeSeriesWithProperties(
    WithProperties
):
    def __get__(
        self,
        instance: typing.Optional[
            WithProperties_Value_T
        ],
        owner: typing.Type[
            WithProperties_Value_T
        ],
    ) -> typing.Type[
        TopicSpecificationAuto[
            WithProperties_Value_T
        ]
    ]:
        """
        Return a
        [TopicSpecification][diffusion.datatypes.timeseries.TopicSpecification]
        class prefilled with `owner`

        Args:
            instance: the instance on which this is called
            owner: the class on which this is called

        Returns:
            Return a TopicSpecification class prefilled with `owner`
        """
        return typing.cast(
            typing.Type[
                TopicSpecificationAuto[
                    WithProperties_Value_T
                ]
            ],
            TopicSpecificationAuto.new_topic_specification(
                typing.cast(
                    typing.Type[
                        WithProperties_Value_T
                    ],
                    owner,
                )
            ),
        )


class TimeSeriesEventDataType(
    IBytes[
        TopicSpecification[
            "TimeSeriesEventDataType[VT]"
        ],
        Event[VT],
        Event[VT],
    ],
    typing.Generic[VT]
):
    """
    A data type for time series events
    """

    _inner_value_type: typing.ClassVar[type]
    type_code = 16

    _value: Event[VT]

    def __init__(self, value: Event[VT]):
        """
        Initialise a TimeSeriesEventDataType

        Args:
            value: the Event[VT]
                to set as the value of this instance
        """

        super(TimeSeriesEventDataType, self).__init__(value)

    def write_value(self, stream: BytesIO) -> BytesIO:
        if self.value is None:
            raise ValueError(f"{repr(self)}.value is None, cannot write")
        return self.value.write_value(stream)

    @classmethod
    def from_bytes(
        cls: typing.Type[TimeSeriesEventDataType[VT]], input: bytes
    ) -> TimeSeriesEventDataType[VT]:
        return cls(cls.real_value_type().from_bytes(input))

    @classmethod
    def decode(cls, data: bytes) -> typing.Any:
        return cls.from_bytes(data).value

    @classmethod
    def encode(cls, value: Any) -> bytes:
        with BytesIO() as stream:
            cls(value).write_value(stream)
            stream.seek(0)
            return stream.read()

    def validate(self):
        # no-op: validates on read
        pass

    @classmethod
    def can_read_as(
        cls: typing.Type[TimeSeriesEventDataType[VT]],
        result_type: typing.Type[AbstractDataType],
    ) -> bool:
        if cls.is_wildcard(result_type):
            return True
        cls_iv_type = typing.cast(
            typing.Type[TimeSeriesValueType_Diffusion], cls.inner_value_type()
        )
        if issubclass(result_type, TimeSeriesEventDataType):
            result_iv_type = typing.cast(
                TimeSeriesEventDataType[TimeSeriesValueType], result_type
            ).inner_value_type()

            return cls_iv_type.can_read_as(
                typing.cast(typing.Type[TimeSeriesValueType], result_iv_type)
            )
        else:
            return cls_iv_type.can_read_as(result_type)

    @classmethod
    def real_value_type(cls) -> typing.Type[Event[VT]]:
        return typing.cast(
            typing.Type[Event[VT]],
            EventTypeFactory.of(Event, cls.inner_value_type()),
        )

    @classmethod
    def _converter_from(
        cls: typing.Type[TimeSeriesEventDataType[VT]],
        source_type: typing.Type[ValueType_target],
    ) -> typing.Optional[
        Converter[ValueType_target, Event[VT]]
    ]:
        if issubclass(source_type, Event):
            inner_vt_converter = typing.cast(
                typing.Type[VT], cls.inner_value_type()
            ).converter_from(source_type.held_value_type())
            if inner_vt_converter:

                def converter(
                    input_event: Event,
                ) -> typing.Optional[Event[VT]]:
                    raw_value = (
                        inner_vt_converter(input_event.value)
                        if input_event and input_event.value
                        else None
                    )
                    return (
                        input_event.with_value(
                            typing.cast(VT, raw_value),
                            cls.inner_value_type(),
                        )
                        if input_event
                        else None
                    )

                return typing.cast(
                    typing.Optional[
                        Converter[
                            ValueType_target, Event[VT]
                        ]
                    ],
                    converter,
                )

        return None

    @classmethod
    def inner_value_type(
        cls,
    ) -> typing.Type[VT]:
        return typing.cast(
            typing.Type[VT],
            getattr(cls, "_inner_value_type", Bytes)
        )



    with_properties: typing.ClassVar[TimeSeriesWithProperties] = (
        TimeSeriesWithProperties()
    )

    """
    Returns a Topic Specification class filled with this type
    and accepting the relevant parameters
    """


class TimeSeriesDataType(object):
    """ Time series data type implementation. """

    type_name = "time_series"
    ts_datatypes: typing.Dict[
        str, typing.Type[TimeSeriesEventDataType[typing.Any]]
    ] = {}

    @classmethod
    def of(cls, val_type: typing.Type[VT]) -> typing.Type[TimeSeriesEventDataType[VT]]:
        """
        Provide a Time Series datatype with the given Event[VT] value type.

        Please use [TimeSeries.of][diffusion.features.timeseries.TimeSeries.of] rather
        than this function to obtain Time Series datatypes.

        Args:
            val_type: the type of value that events will contain.

        Returns:
            The relevant Time Series data type.
        """
        return cls._of(val_type)

    @classmethod
    def _of(
        cls, val_type: typing.Type[VT]
    ) -> typing.Type[TimeSeriesEventDataType[VT]]:
        from diffusion.datatypes.conversion.default import DEFAULT_CONVERTER
        val_type = typing.cast(typing.Type[VT], DEFAULT_CONVERTER(val_type))
        type_name = repr(val_type)
        if type_name not in cls.ts_datatypes:
            fresh_type = typing.cast(
                typing.Type["TimeSeriesEventDataType[VT]"],
                type(
                    f"TimeSeriesEventDataType_{stringcase.pascalcase(type_name)}",
                    (TimeSeriesEventDataType,),
                    {
                        "type_name": f"timeseriesevent-{type_name}",
                        "_inner_value_type": val_type
                    },
                ),
            )
            cls.ts_datatypes[type_name] = fresh_type
        else:
            fresh_type = cls.ts_datatypes[type_name]
        return typing.cast(
            typing.Type["TimeSeriesEventDataType[VT]"],
            fresh_type
        )


class TimeSeriesValidator(object):
    def validate_ts(
        self, field_value: TimeSeriesValueType
    ) -> TimeSeriesValueType_Diffusion:
        return typing.cast(TimeSeriesValueType_Diffusion, self.validate_ts_typed(
            field_value,
            typing.cast(typing.Type[TimeSeriesValueType], type(field_value)),
        ))

    def validate_ts_typed(
        self,
        field_value: TimeSeriesValueTypeOrRaw,
        field_value_type: typing.Type[TimeSeriesValueType],
    ) -> TimeSeriesValueType_Diffusion:
        field_type: typing.Type[TimeSeriesValueType_Diffusion] = self.validate_ts_type(
            field_value_type
        )
        field_value_candidate = self.ensure_type(field_type, field_value)

        assert isinstance(field_value_candidate, field_type)
        return field_value_candidate

    # noinspection PyMethodMayBeStatic
    def ensure_type(
        self,
        field_type: typing.Type[TimeSeriesValueType_Diffusion],
        field_value: TimeSeriesValueTypeOrRaw,
    ) -> TimeSeriesValueType_Diffusion:

        field_value_candidate: TimeSeriesValueType_Diffusion

        self.ensure_ts(field_type)
        if isinstance(field_value, field_type):
            field_value_candidate = typing.cast(TimeSeriesValueType_Diffusion, field_value)
        else:
            constructed = field_type(field_value)  # type: ignore
            field_value_candidate = typing.cast(TimeSeriesValueType_Diffusion, constructed)

        @validate_member_arguments
        def ensure_ts_value(val: TimeSeriesValueType) -> TimeSeriesValueType:
            return val

        ensure_ts_value(field_value_candidate)
        return field_value_candidate

    @validate_member_arguments
    def ensure_ts(
        self,
        val: TimeSeriesValueTypeClasses
    ) -> TimeSeriesValueTypeClasses:
        return val

    def validate_ts_type(
        self, field_value_type
    ) -> typing.Type[TimeSeriesValueType_Diffusion]:
        field_type_final = self.ensure_ts(
            typing.cast(typing.Type[TimeSeriesValueType_Diffusion], field_value_type)
        )
        return field_type_final


TIME_SERIES_VALIDATOR = TimeSeriesValidator()

validate_ts = TIME_SERIES_VALIDATOR.validate_ts
validate_ts_type = TIME_SERIES_VALIDATOR.validate_ts_type
validate_ts_typed = TIME_SERIES_VALIDATOR.validate_ts_typed
