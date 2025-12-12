#  Copyright (c) 2022 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

#
#  Use is subject to licence terms.
#
from __future__ import annotations

import datetime
import enum
import functools
import math
import typing

import attr

from diffusion.exceptions import ArgumentNoneError, ArgumentOutOfRangeError
from diffusion.features.timeseries.query.range_query_parameters import StreamStructure
from diffusion.internal.encoded_data import Int64
from diffusion.internal.utils import validate_member_arguments
from diffusion.internal.validation import (
    StrictNonNegativeInt,
    StrictNonNegativeTimedelta,
    StrictTimedelta,
)

from diffusion.internal.serialisers.pydantic import MarshalledModel
from diffusion.internal.pydantic_compat.v1 import dataclasses as dataclasses
import dataclasses as dc
from diffusion.internal.utils import BaseConfig


@dataclasses.dataclass
class Representation(object):
    main: str
    primary: str
    stream_structure: StreamStructure

    def __str__(self):
        return f".{self.main}()"

    @property
    def primary_operator(self):
        return f".{self.primary}()"


class QueryType(enum.IntEnum):
    """
    The range query type.

    Since:
        6.1
    """

    @property
    def __mapping__(self) -> typing.Mapping[QueryType, Representation]:
        from diffusion.features.timeseries.query.range_query_parameters import StreamStructure
        return {
            QueryType.VALUES: Representation(
                "edit_range", "for_values", StreamStructure.VALUE_EVENT_STREAM
            ),
            QueryType.ALL_EDITS: Representation(
                "all_edits", "for_edits", StreamStructure.EDIT_EVENT_STREAM
            ),
            QueryType.LATEST_EDITS: Representation(
                "latest_edits", "for_edits", StreamStructure.EDIT_EVENT_STREAM
            ),
        }

    def __str__(self):
        return str(self.__mapping__.get(self))

    VALUES = 0x00
    """
    Original events in view range merged with latest edits in edit range.
    """

    ALL_EDITS = 0x01
    """
    Original events in view range plus all edits in edit range.
    """
    LATEST_EDITS = 0x02
    """
    Original events in view range plus latest event in edit range.
    """

    @property
    def primary_operator(self) -> str:
        """
        Returns the primary operator of a given <see cref="QueryType"/>.
        """
        return self.__mapping__[self].primary_operator

    @property
    def edit_range_operator(self) -> str:
        """
        Returns:
            The edit range operator of the given <paramref name="type"/>.</returns>
        """
        return str(self)

    @property
    def stream_structure(self) -> StreamStructure:
        """
        Returns the stream structure of a given <see cref="QueryType"/>.

        Returns:
            The stream structure of the given `type`
        """
        return self.__mapping__[self].stream_structure


class SpanPair(typing.NamedTuple):
    anchor: typing.Optional[str]
    span: str


class PointType(enum.IntEnum):
    """
    The point type.

    Since:
        6.9
    """

    ABSOLUTE_START = 0x00
    """
    The value is ignored.
    """

    ABSOLUTE_SEQUENCE = 0x01
    """
    The value is a absolute sequence number.
    """

    ABSOLUTE_TIME = 0x02
    """
    The value is a <see cref="DateTimeOffset"/>.
    """

    OFFSET_SEQUENCE = 0x03
    """
    The value is the number of terminal events of the series to skip.
    """

    OFFSET_TIME = 0x04
    """
    The value is the terminal duration in milliseconds of the series to skip.
    """

    NEXT_COUNT = 0x05
    """
    The value is a relative number of events after another point.
    """

    NEXT_TIME = 0x06
    """
    The value is a duration in milliseconds after another point.
    """

    PREVIOUS_COUNT = 0x07
    """
    The value is a relative number of events before another point.
    """

    PREVIOUS_TIME = 0x08
    """
    The value is a duration in milliseconds before another point.
    """

    @property
    def __mapping__(self) -> typing.Dict[PointType, SpanPair]:
        return {
            PointType.ABSOLUTE_START: SpanPair("from_start", "to_start"),
            PointType.ABSOLUTE_SEQUENCE: SpanPair("from", "to"),
            PointType.ABSOLUTE_TIME: SpanPair("from", "to"),
            PointType.OFFSET_SEQUENCE: SpanPair("from_last", "until_last"),
            PointType.OFFSET_TIME: SpanPair("from_last", "until_last"),
            PointType.NEXT_COUNT: SpanPair(None, "next"),
            PointType.NEXT_TIME: SpanPair(None, "next"),
            PointType.PREVIOUS_COUNT: SpanPair(None, "previous"),
            PointType.PREVIOUS_TIME: SpanPair(None, "previous"),
        }

    @property
    def anchor_operator(self) -> typing.Optional[str]:
        """
        Returns the anchor operator for a given <see cref="PointType"/>.

        Returns:
            The anchor operator for the given <paramref name="type"/>.
        """
        try:
            return self.__mapping__[self].anchor
        except KeyError:
            raise ValueError(f"No anchor operator for {type}.")

    @property
    def span_operator(self) -> str:
        """
        Returns the span operator for this `PointType`

        Returns:
            The span operator.
        """
        try:
            return self.__mapping__[self].span
        except KeyError:
            raise ValueError(f"No anchor operator for {type}.")

    def format_unit(self, value: int) -> str:
        """
        Returns the unit suffix for a given <see cref="PointType"/>.

        Returns:
            The unit suffix.
        """
        if self in {
            PointType.ABSOLUTE_TIME,
            PointType.OFFSET_TIME,
            PointType.NEXT_TIME,
            PointType.PREVIOUS_TIME,
        }:
            return f"datetime.timedelta(milliseconds={value})"
        return f"{value}"

    def validate(self, value: StrictNonNegativeInt) -> bool:
        """
        Validates a given <paramref name="value"/> based on the rules
        of this PointType.

        Args:
            value: The value to validate.

        Returns:
            `True` if the value is valid for this type
            Otherwise `False`.
        """
        return (
            self in {PointType.ABSOLUTE_START, PointType.ABSOLUTE_TIME}
            or value >= 0
        )


PointSelf = typing.TypeVar("PointSelf", bound="Point")


@dataclasses.dataclass(frozen=True, config=BaseConfig)
class Point(object):
    """
    The query point for a range.

    Since:
        6.9
    """

    @classmethod
    @functools.lru_cache(maxsize=None)
    def at_start(cls):
        """
        Returns a point representing an absolute sequence.
        """
        return Point(0, PointType.ABSOLUTE_START)

    def __iter__(self):
        return iter(dc.astuple(self))

    def __reversed__(self):
        return iter(reversed(dc.astuple(self)))

    @classmethod
    @validate_member_arguments
    def at(
        cls: typing.Type[PointSelf],
        time: typing.Union[StrictNonNegativeInt, StrictTimedelta],
    ) -> PointSelf:
        """
        Returns a point representing an absolute time or sequence number.

        Args:
            time: The absolute time (as a `datetime.timedelta`)
                or the sequence offset (as a non-negative `int`)

        Returns:
            The point representing an absolute time.
        """
        if isinstance(time, datetime.timedelta):
            return cls(
                int(math.ceil(time.total_seconds() * 1000)),
                PointType.ABSOLUTE_TIME,
            )
        return cls(time, PointType.ABSOLUTE_SEQUENCE)

    @classmethod
    @validate_member_arguments
    def offset(
        cls: typing.Type[PointSelf],
        offset: typing.Union[StrictNonNegativeInt, StrictNonNegativeTimedelta],
    ) -> PointSelf:
        """
        Returns a point representing a sequence offset from the end of the time series.
        Args:
            offset: The sequence offset (as a non-negative `int`)
                or the time span (as a `datetime.timedelta`)

        Returns:
            The point representing the offset from the end of the time series.
        """

        if isinstance(offset, datetime.timedelta):
            return cls.offset_milliseconds(
                int(math.ceil(offset.total_seconds() * 1000))
            )
        return cls(offset, PointType.OFFSET_SEQUENCE)

    @classmethod
    @validate_member_arguments
    def offset_milliseconds(
        cls: typing.Type[PointSelf], milliseconds: StrictNonNegativeInt
    ) -> PointSelf:
        """
        Returns a point representing a duration from the end of the time series.
        Args:
            milliseconds: The time span in milliseconds.

        Returns:
            The point representing a duration from the end of the time series.
        """
        return cls(milliseconds, PointType.OFFSET_TIME)

    @classmethod
    @validate_member_arguments
    def next(
        cls: typing.Type[PointSelf],
        offset: typing.Union[StrictNonNegativeInt, StrictNonNegativeTimedelta],
    ) -> PointSelf:
        """
        Returns a relative point at <paramref name="count"/> events after the anchor.

        Args:
            offset: either the time span of events following the anchor to select (as a
                [StrictNonNegativeTimedelta][diffusion.internal.validation.StrictNonNegativeTimedelta])
                or the end of the range of events to select following the anchor (as a
                [StrictNonNegativeInt][diffusion.internal.validation.StrictNonNegativeInt])

        Returns:
            The relative point at `offset` events or `offset` after the anchor.
        """
        if isinstance(offset, datetime.timedelta):
            return cls.next_milliseconds(
                int(math.ceil(offset.total_seconds() * 1000))
            )
        return cls(offset, PointType.NEXT_COUNT)

    @classmethod
    @validate_member_arguments
    def next_milliseconds(
        cls: typing.Type[PointSelf], milliseconds: StrictNonNegativeInt
    ) -> PointSelf:
        """
        Returns a relative point at <paramref name="milliseconds"/> after the anchor.

        Args:
            milliseconds: The time span in milliseconds.
        Returns:
            The relative point at <paramref name="milliseconds"/> after the anchor.
        """
        return cls(milliseconds, PointType.NEXT_TIME)

    @classmethod
    @validate_member_arguments
    def previous(
        cls: typing.Type[PointSelf],
        offset: typing.Union[StrictNonNegativeInt, StrictNonNegativeTimedelta],
    ) -> PointSelf:
        """
        Returns a relative point at <paramref name="count"/> events before the anchor.

        Args:
            offset:
                - The end of the range of events to select preceding the anchor (as a
                [StrictNonNegativeInt][diffusion.internal.validation.StrictNonNegativeInt]) or
                - The time span of events preceding the anchor to select (as a
                [StrictNonNegativeTimedelta][diffusion.internal.validation.StrictNonNegativeTimedelta])
        Returns:
            The relative point at <paramref name="count"/> events before the anchor.
        """
        if isinstance(offset, datetime.timedelta):
            return cls.previous_milliseconds(
                int(math.ceil(offset.total_seconds() * 1000))
            )

        return cls(offset, PointType.PREVIOUS_COUNT)

    @classmethod
    @validate_member_arguments
    def previous_milliseconds(
        cls: typing.Type[PointSelf], milliseconds: StrictNonNegativeInt
    ) -> PointSelf:
        """
        Returns the relative point at <paramref name="milliseconds"/> before the anchor.

        Args:
            milliseconds: The time span in milliseconds.
        Returns:
            The relative point at <paramref name="milliseconds"/> before the anchor.
        """
        return cls(milliseconds, PointType.PREVIOUS_TIME)

    value: int
    """
    The value.
    """

    tp: PointType
    """
    The point type.
    """

    def __post_init__(self):
        if not self.tp.validate(self.value):
            @validate_member_arguments
            def check(value: StrictNonNegativeInt):
                pass
            check(self.value)

    @property
    def is_absolute(self) -> bool:
        """
        Gets whether the current point is absolute or not.
        Returns:
            Whether the current point is absolute.
        """
        return self.tp.anchor_operator is not None

    def operator_description(self, op: typing.Optional[str] = "") -> str:
        sb = ""
        sb += f".{op}("

        if self.tp != PointType.ABSOLUTE_START:
            quantity = self.tp.format_unit(value=self.value)
            sb += quantity

        sb += ")"
        return sb

    def anchor_description(self) -> str:
        """
        Returns:
             the anchor description for the current <see cref="Point"/>.
        """
        return self.operator_description(self.tp.anchor_operator)

    def span_description(self) -> str:
        """
        Returns the span description for the current <see cref="Point"/>.
        Returns:
            The span description.
        """
        return self.operator_description(self.tp.span_operator)

    def __str__(self):
        return f"{self.tp} {self.value}"


RangeSelf = typing.TypeVar("RangeSelf", bound="Range")


@attr.s(auto_attribs=True, eq=True, hash=True, frozen=True, slots=True)
class Range(object):
    """
    The query range.

    Since:
        6.9
    """

    # noinspection PyPep8Naming
    @classmethod
    @functools.lru_cache(maxsize=None)
    def DEFAULT_RANGE(cls: typing.Type[RangeSelf]) -> RangeSelf:  # NOQA: N802
        """
        The default range with Point.at_start() as
        anchor and Point.offset(0) as span.
        """
        return cls()

    def __copy__(self):
        return self

    def __deepcopy__(self, memodict=None):
        return self.__copy__()

    anchor: Point = Point.at_start()
    """
    The anchor point.
    """

    span: Point = Point.offset(0)
    """
    The span point.
    """

    @classmethod
    @validate_member_arguments
    def create(
        cls: typing.Type[RangeSelf], anchor: Point, span: Point
    ) -> RangeSelf:
        """
        Creates a new
        [Range][diffusion.features.timeseries.query.range_query_parameters.Range]
        instance.

        Args:
            anchor: The anchor point.
            span: The span point.

        Returns:
            New range
        """

        if not anchor.is_absolute:
            raise ValueError("Anchor point is not absolute.")
        return cls(anchor=anchor, span=span)

    def __attrs_post_init__(self):
        """
        Initialises a new
        [Range][diffusion.features.timeseries.query.range_query_parameters.Range]
        instance.
        """

        if self.anchor is None:
            raise ArgumentNoneError(f"Anchor is {self.anchor}")

        if not self.anchor.is_absolute:
            raise ArgumentOutOfRangeError("Anchor point is not absolute.")

        if not self.span:
            raise ArgumentNoneError(f"Span is {self.span}")

    def from_start(self) -> Range:
        """
        Copies the current
        [Range][diffusion.features.timeseries.query.range_query_parameters.Range]
        with a new anchor point.

        Returns:
            The copy of the current
                [Range][diffusion.features.timeseries.query.range_query_parameters.Range]
                with a new anchor point.
        """
        return attr.evolve(self, anchor=Point.at_start())

    @validate_member_arguments
    def from_(
        self: RangeSelf,
        time: typing.Union[StrictNonNegativeInt, StrictTimedelta],
    ) -> RangeSelf:
        """
        Copies the current
        [Range][diffusion.features.timeseries.query.range_query_parameters.Range]
        with a new anchor point.

        Args:
            time: The sequence number (as a non-negative `int`) or
                the absolute time (as a `datetime.timedelta`)

        Returns:
            The copy of the current
                [Range][diffusion.features.timeseries.query.range_query_parameters.Range]
                with a new anchor point.
        """
        return attr.evolve(self, anchor=Point.at(time))

    @validate_member_arguments
    def from_last(
        self: RangeSelf,
        offset: typing.Union[StrictNonNegativeInt, StrictNonNegativeTimedelta],
    ) -> RangeSelf:
        """
        Copies the current
        [Range][diffusion.features.timeseries.query.range_query_parameters.Range]
        with a new anchor point.
        Args:
            offset: The offset (as a
                [StrictNonNegativeInt][diffusion.internal.validation.StrictNonNegativeInt]) or
                a time (as a
                [StrictNonNegativeTimedelta][diffusion.internal.validation.StrictNonNegativeTimedelta])

        Returns:
            The copy of the current
                [Range][diffusion.features.timeseries.query.range_query_parameters.Range]
                with a new anchor point.
        """
        return attr.evolve(self, anchor=Point.offset(offset))

    @validate_member_arguments
    def from_last_milliseconds(
        self: RangeSelf, milliseconds: StrictNonNegativeInt
    ) -> RangeSelf:
        """
        Copies the current
        [Range][diffusion.features.timeseries.query.range_query_parameters.Range]
        with a new anchor point.

        Args:
            milliseconds: The time offset in milliseconds.

        Returns:
            The copy of the current
                [Range][diffusion.features.timeseries.query.range_query_parameters.Range]
                with a new anchor point.
        """
        return attr.evolve(self, anchor=Point.offset_milliseconds(milliseconds))

    def to_start(self) -> Range:
        """
        Copies the current
        [Range][diffusion.features.timeseries.query.range_query_parameters.Range]
        with a new span point.

        Returns:
            The copy of the current
                [Range][diffusion.features.timeseries.query.range_query_parameters.Range]
                with a new span point.
        """
        return attr.evolve(self, span=Point.at_start())

    @validate_member_arguments
    def to(
        self: RangeSelf,
        time: typing.Union[StrictNonNegativeInt, StrictTimedelta],
    ) -> RangeSelf:
        """
        Create a copy of the current
        [Range][diffusion.features.timeseries.query.range_query_parameters.Range]
        with a new span point.

        Args:
            time: The absolute time (as a `datetime.timedelta`) or
                the sequence offset (as a non-negative `int`)

        Returns:
            The copy of the current
                [Range][diffusion.features.timeseries.query.range_query_parameters.Range]
                with a new span point.
        """
        return attr.evolve(self, span=Point.at(time))

    @validate_member_arguments
    def until_last(
        self: RangeSelf,
        offset: typing.Union[StrictNonNegativeInt, StrictNonNegativeTimedelta],
    ) -> RangeSelf:
        """
        Copies the current
        [Range][diffusion.features.timeseries.query.range_query_parameters.Range]
        with a new span point.

        Args:
            offset: The offset from the end of the time series as:
                - time span (as a `datetime.timedelta`) or
                 - sequence count (as a non-negative `int`)

        Returns:
            The copy of the current
                [Range][diffusion.features.timeseries.query.range_query_parameters.Range]
                with a new span point.
        """
        return attr.evolve(self, span=Point.offset(offset))

    @validate_member_arguments
    def until_last_milliseconds(
        self: RangeSelf, milliseconds: StrictNonNegativeInt
    ) -> RangeSelf:
        """
        Copies the current
        [Range][diffusion.features.timeseries.query.range_query_parameters.Range]
        with a new span point.

        Args:
            milliseconds: The time span offset in milliseconds.

        Returns:
            The copy of the current
                [Range][diffusion.features.timeseries.query.range_query_parameters.Range]
                with a new span point.
        """
        return attr.evolve(self, span=Point.offset_milliseconds(milliseconds))

    @validate_member_arguments
    def next(
        self: RangeSelf,
        offset: typing.Union[StrictNonNegativeInt, StrictNonNegativeTimedelta],
    ) -> "RangeSelf":
        """
        Copies the current
        [Range][diffusion.features.timeseries.query.range_query_parameters.Range]
        with a new span point.

        Args:
            offset: either the time span of events following the anchor to select (as a
                [StrictNonNegativeTimedelta][diffusion.internal.validation.StrictNonNegativeTimedelta])
                or the end of the range of events to select following the anchor (as a
                [StrictNonNegativeInt][diffusion.internal.validation.StrictNonNegativeInt])
        Returns:
            The copy of the current
                [Range][diffusion.features.timeseries.query.range_query_parameters.Range]
                with a new span point.
        """  # noqa: E501, W291
        return attr.evolve(self, span=Point.next(offset))

    @validate_member_arguments
    def next_milliseconds(
        self: RangeSelf, milliseconds: StrictNonNegativeInt
    ) -> RangeSelf:
        """
        Copies the current
        [Range][diffusion.features.timeseries.query.range_query_parameters.Range]
        with a new span point.
        Args:
            milliseconds: The next time span in milliseconds.

        Returns:
            The copy of the current
                [Range][diffusion.features.timeseries.query.range_query_parameters.Range]
                with a new span point.
        """
        return attr.evolve(self, span=Point.next_milliseconds(milliseconds))

    @validate_member_arguments
    def previous(
        self: RangeSelf,
        offset: typing.Union[StrictNonNegativeInt, StrictNonNegativeTimedelta],
    ) -> RangeSelf:
        """
        Copies the current
        [Range][diffusion.features.timeseries.query.range_query_parameters.Range]
        with a new span point.

        Args:
            offset:
                - The end of the range of events to select preceding the anchor (as a
                [StrictNonNegativeInt][diffusion.internal.validation.StrictNonNegativeInt]) or
                - The time span of events preceding the anchor to select (as a
                [StrictNonNegativeTimedelta][diffusion.internal.validation.StrictNonNegativeTimedelta])
        Returns:
            The copy of the current
                [Range][diffusion.features.timeseries.query.range_query_parameters.Range]
                with a new span point.
        """
        return attr.evolve(self, span=Point.previous(offset))

    @validate_member_arguments
    def previous_milliseconds(
        self: RangeSelf, milliseconds: StrictNonNegativeInt
    ) -> RangeSelf:
        """
        Copies the current
        [Range][diffusion.features.timeseries.query.range_query_parameters.Range]
        with a new span point.

        Args:
            milliseconds: The previous time span in milliseconds.

        Returns:
            The copy of the current
                [Range][diffusion.features.timeseries.query.range_query_parameters.Range]
                with a new span point.
        """

        return attr.evolve(self, span=Point.previous_milliseconds(milliseconds))

    def __str__(self):
        sb = ""

        if self.anchor != self.DEFAULT_RANGE().anchor:
            sb += self.anchor.anchor_description()

        if self.span != self.DEFAULT_RANGE().span:
            sb += self.span.span_description()

        return sb


RQPSelf = typing.TypeVar("RQPSelf", bound="RangeQueryParameters")


class RangeQueryParameters(MarshalledModel):
    """
    The range query parameters.

    Since:
        6.9
    """
    class Config(MarshalledModel.Config):
        alias = "range-query-parameters"
        frozen = True

    # noinspection PyPep8Naming
    @classmethod
    @functools.lru_cache(maxsize=None)
    def DEFAULT_RANGE_QUERY(cls) -> RangeQueryParameters:  # NOQA: N802
        return cls()

    query_type: QueryType = QueryType.VALUES
    """ The query type """

    view_range: Range = Range.DEFAULT_RANGE()
    """ The view range """

    edit_range: Range = Range.DEFAULT_RANGE()
    """ The edit range """

    limit: StrictNonNegativeInt = Int64.max_signed_int()

    @property
    def is_historic_query(self):
        """
        Gets whether the current query parameters are a historic query or not.
        """
        return (
            self.query_type != QueryType.VALUES
            or self.edit_range != Range.DEFAULT_RANGE()
        )

    @validate_member_arguments
    def with_view_range(self: RQPSelf, range: Range) -> RQPSelf:
        """
        Creates a copy of the current <see cref="RangeQueryParameters"/>
        with a new view range.

        Args:
            range: The new view range.

        Returns:
            The copy of the current
                [RangeQueryParameters][diffusion.features.timeseries.query.range_query_parameters.RangeQueryParameters]
                with a new view `range`.
        """  # noqa: E501, W291
        return self.copy(update=dict(view_range=range))

    @validate_member_arguments
    def with_edit_range(self: RQPSelf, range: Range) -> RQPSelf:
        return self.copy(update=dict(edit_range=range))

    @validate_member_arguments
    def with_limit(self: RQPSelf, count: StrictNonNegativeInt) -> RQPSelf:
        return self.copy(update=dict(limit=count))

    @validate_member_arguments
    def with_query_type(self: RQPSelf, type: QueryType) -> RQPSelf:
        """
        Creates a copy of the current <see cref="RangeQueryParameters"/>
        with a new query type.

        Args:
            type: The new query type.

        Returns:
            The copy of the current
                [RangeQueryParameters][diffusion.features.timeseries.query.range_query_parameters.RangeQueryParameters]
                with a new `type`.
        """  # noqa: E501, W291
        return self.copy(update=dict(query_type=type))

    def __str__(self):
        sb = ""

        if self.query_type != QueryType.VALUES:
            sb += self.query_type.primary_operator

        if self.view_range != self.DEFAULT_RANGE_QUERY().view_range:
            sb += str(self.view_range)

        if self.edit_range != self.DEFAULT_RANGE_QUERY().edit_range:
            sb += f"{self.query_type.edit_range_operator}{self.edit_range}"
        elif self.query_type == QueryType.LATEST_EDITS:
            sb += QueryType.LATEST_EDITS.edit_range_operator

        if self.limit != self.DEFAULT_RANGE_QUERY().limit:
            sb += f".limit({self.limit})"

        return sb
