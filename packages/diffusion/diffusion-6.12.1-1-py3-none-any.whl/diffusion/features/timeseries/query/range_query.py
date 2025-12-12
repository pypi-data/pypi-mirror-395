#  Copyright (c) 2022 - 2024 DiffusionData Ltd., All Rights Reserved.
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

import stringcase  # type: ignore[import-untyped]
import typing

from typing_extensions import TypeAlias
import attr
import diffusion.internal.pydantic_compat.v1 as pydantic

from diffusion.internal.timeseries.query.range_query import RangeQueryMode, RangeQueryBase

from diffusion.exceptions import InvalidOperationError
from diffusion.internal.timeseries.query.range_query_parameters import (
    RangeQueryParameters,
    Range,
    QueryType,
)
from diffusion.internal.timeseries.query.range_query_request import (
    RangeQueryRequest,
)
from diffusion.internal.session import InternalSession
from diffusion.datatypes.timeseries.types import VT, VT_other
from diffusion.internal.utils import validate_member_arguments
from diffusion.internal.validation import (
    StrictNonNegativeInt,
    StrictNonNegativeTimedelta,
    StrictTimedelta,
)
from diffusion.features.timeseries.query.query_result import QueryResult

QuerySelf = typing.TypeVar("QuerySelf", bound="RangeQuery")
"""
A [RangeQuery][diffusion.features.timeseries.query.range_query.RangeQuery]
or instance of a subclass thereof (used when passing the same type back).
"""

RangeQueryType: TypeAlias = "RangeQuery"


@attr.s(auto_attribs=True, eq=True, hash=True, slots=True, frozen=True)
class RangeQuery(typing.Generic[VT], RangeQueryBase[VT]):
    """
    The builder for queries that select a range of events from a time series.

    Notes:

    See [diffusion.features.timeseries.TimeSeries][] for an overview of the various types of range query:

    - value range queries
    - latest edits edit range queries
    - all edits edit range queries

    [RangeQuery.create_default][diffusion.features.timeseries.query.range_query.RangeQuery.create_default] returns a default
    [RangeQuery][diffusion.features.timeseries.query.range_query.RangeQuery].
    Further queries with different parameters can be configured using the methods of
    this interface.
    [RangeQuery][diffusion.features.timeseries.query.range_query.RangeQuery]
    instances are immutable. Each method returns a copy of this query with a modified setting. Method calls can be
    chained together in a fluent manner to create a query.

    # Creating value range queries

    A value range query returns a merged view of part of a time series. This
    is the most common time series query and appropriate for most
        applications.

    A value range query begins with the [RangeQuery.for_values][diffusion.features.timeseries.query.range_query.RangeQuery.for_values] operator,
    followed by the _view range_. The view range determines the range
    of original events the time series that are of interest. See
    [Range expressions][diffusion.features.timeseries.query.range_query.RangeQuery--range-expressions]
    below for the various ways to specify a range.

    The events returned by the query are constrained by an optional <i>edit range</i>, introduced by the
    [RangeQuery.edit_range][diffusion.features.timeseries.query.range_query.RangeQuery.edit_range]
    operator. An event will only be included in the result if it is in the edit range. Let's
    consider some examples to see how the view range and the edit range
    interact.

    | query                                                                | Meaning                                                                                                                                                                                                                                                                                                     |
    |----------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | `RangeQuery.for_values()`                                            | For each original event in the time series, either return the latest edit event or if it has no edit events, return the original event.                                                                                                                                                                     |
    | `RangeQuery.for_values().from_(100).to(150)`                         | For each original event with a sequence number between 100 and 150 (inclusive), either return the latest edit event or if it has no edit events, return the original event.                                                                                                                                 |
    | `RangeQuery.for_values().from_(100).to(150).edit_range().from_(400)` | For each original event with a sequence number between 100 and 150 (inclusive), return the latest edit event with a sequence number greater than or equal to 400.<br/> The result of this query will not include any original events because there is no overlap between the view range and the edit range. |

    value range queries can be further refined using the [RangeQuery.limit][diffusion.features.timeseries.query.range_query.RangeQuery.limit]
    and <see cref="As{TNewValue}"/> operators.

    # Creating edit range queries

    An edit range query returns an unmerged view of a time series than can
    include both original events and the edit events that replace them. Edit
    range queries are rarely needed - value range queries satisfy most
    use cases.

    An edit range query begins with the [RangeQuery.for_edits][diffusion.features.timeseries.query.range_query.RangeQuery.for_edits] operator,
    followed by the _view range_. The view range determines the range
    of original events the time series that are of interest. The result will
    only contain original events that are in the view range, and edit events
    for original events in the view range. See
    [Range expressions][diffusion.features.timeseries.query.range_query.RangeQuery--range-expressions]
    below for the various ways to specify a range.

    The events returned by the query are constrained by an optional _edit
    range_, introduced by the
    [RangeQuery.latest_edits][diffusion.features.timeseries.query.range_query.RangeQuery.latest_edits] or
    [RangeQuery.all_edits][diffusion.features.timeseries.query.range_query.RangeQuery.all_edits]
    operators. An event will only be included in the result if it is in the edit range.
    Let's consider some example edit range queries.

    | query                                                              | Meaning                                                                                                                                                                                                                                                                                               |
    |--------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | `RangeQuery.for_edits()`                                           | Return all events in a time series.                                                                                                                                                                                                                                                                   |
    | `RangeQuery.for_edits().from_(100).to(150)`                        | Return the original events with a sequence number between 100 and 150 (inclusive) and all edit events in the time series that refer to the original events.                                                                                                                                           |
    | `RangeQuery.for_edits().from_(100).to(150).latest_edits()`         | Return the original events with a sequence number between 100 and 150 (inclusive) and the latest edit events in the time series that refer to the original events.                                                                                                                                    |
    | `RangeQuery.for_edits().from_(100).to(150).all_edits().from_(400)` | For each original event with a sequence number between 100 and 150, (inclusive) return all edit events with a sequence number greater than or equal to 400.<br/> The result of this query will not include any original events because there is no overlap between the view range and the edit range. |

    Edit range queries can be further refined using the
    [RangeQuery.limit][diffusion.features.timeseries.query.range_query.RangeQuery.limit] and
    [RangeQuery.as_][diffusion.features.timeseries.query.range_query.RangeQuery.as_] operators.

    # Range expressions

    Range expressions are used to specify the view and edit ranges in value
    range and edit range queries. Each range expression has an
    _anchor_ that determines where to start, and a _span_ that
    determines where the range ends. Both anchor and span are
    _inclusive_ - if an anchor or span falls on an event, the
    event is included in the result.


    Both anchor and the span are optional. If the anchor is unspecified, the
    range begins at the start of the time series. If the span is unspecified,
    the range continues until the end of the time series.

    ## Anchors

    There are five ways to specify an anchor.

    | Anchor                                                                                         | Meaning                                                                                                                                                                                                     |
    |------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | [RangeQuery.from_][diffusion.features.timeseries.query.range_query.RangeQuery.from_]           | Sets the anchor at an absolute sequence number.                                                                                                                                                             |
    | [RangeQuery.from_start][diffusion.features.timeseries.query.range_query.RangeQuery.from_start] | Sets the anchor at the start of the time series.                                                                                                                                                            |
    | [RangeQuery.from_][diffusion.features.timeseries.query.range_query.RangeQuery.from_]           | Sets the anchor at an absolute time.                                                                                                                                                                        |
    | [RangeQuery.from_last][diffusion.features.timeseries.query.range_query.RangeQuery.from_last]   | Sets the anchor at a relative offset before the end of the time series. For value range queries, count is the number of original events. For edit range queries, count is the number of events of any type. |
    | [RangeQuery.from_last][diffusion.features.timeseries.query.range_query.RangeQuery.from_last]   | Sets the anchor at a relative time before the timestamp of the last event of the time series.                                                                                                               |

    An anchor point can be before the start or after the end of the time
    series.

    ## Spans

    There are nine ways to specify a span.

    | Span                                                                                           | Meaning                                                                                                                                                                                                                               |
    |------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | [RangeQuery.to][diffusion.features.timeseries.query.range_query.RangeQuery.to]                 | The range ends at an absolute sequence number. The `sequence` argument may be before or after the anchor.                                                                                                                             |
    | [RangeQuery.to_start][diffusion.features.timeseries.query.range_query.RangeQuery.to_start]     | The range ends at the start of the time series.                                                                                                                                                                                       |
    | [RangeQuery.to][diffusion.features.timeseries.query.range_query.RangeQuery.to]                 | The range ends at an absolute time. The `time_span` argument may be before or after the anchor.                                                                                                                                       |
    | [RangeQuery.next][diffusion.features.timeseries.query.range_query.RangeQuery.next]             | The range ends at an event that is a relative number of events after the anchor. For value range queries, count is the number of original events. For edit range queries, count is the number of events of any type.                  |
    | [RangeQuery.next][diffusion.features.timeseries.query.range_query.RangeQuery.next]             | The range ends at an event that is a relative time after the anchor.                                                                                                                                                                  |
    | [RangeQuery.previous][diffusion.features.timeseries.query.range_query.RangeQuery.previous]     | The range ends at an event that is a relative number of events before the anchor. For value range queries, count is the number of original events. For edit range queries, count is the number of events of any type.                 |
    | [RangeQuery.previous][diffusion.features.timeseries.query.range_query.RangeQuery.previous]     | The range ends at an event that is a relative time before the anchor.                                                                                                                                                                 |
    | [RangeQuery.until_last][diffusion.features.timeseries.query.range_query.RangeQuery.until_last] | The range ends at an event that is a relative number of events before the end of the time series. For value range queries, count is the number of original events. For edit range queries, count is the number of events of any type. |
    | [RangeQuery.until_last][diffusion.features.timeseries.query.range_query.RangeQuery.until_last] | The range ends at an event that is a relative time before the timestamp of the last event of the time series.                                                                                                                         |

    A span can specify an end point that is before the start or after the end
    of the time series.

    If the span specifies an end point after the anchor, the range includes
    the first event at or following the anchor and ends at the last event at
    or preceding the end point. If the span specifies an end point before the
    anchor, the range includes the first event at or preceding the anchor and
    ends at the last event at or after the end point.

    # Using the builder methods

    RangeQuery builder methods - those that return another
    RangeQuery - can be applied in any order with the
        following exceptions:

    - [RangeQuery.edit_range][diffusion.features.timeseries.query.range_query.RangeQuery.edit_range]
        only applies to value range queries, so cannot follow
        [RangeQuery.for_edits][diffusion.features.timeseries.query.range_query.RangeQuery.for_edits]
        without an intervening
        [RangeQuery.for_values][diffusion.features.timeseries.query.range_query.RangeQuery.for_values].

    - [RangeQuery.latest_edits][diffusion.features.timeseries.query.range_query.RangeQuery.latest_edits]
        and [RangeQuery.all_edits][diffusion.features.timeseries.query.range_query.RangeQuery.all_edits]
        only apply to edit range queries, so cannot follow
        [RangeQuery.for_values][diffusion.features.timeseries.query.range_query.RangeQuery.for_values]
        without an intervening
        [RangeQuery.for_edits][diffusion.features.timeseries.query.range_query.RangeQuery.for_edits].

    Each method overrides some configuration of the RangeQuery to which it is
    applied, as summarized in the following table.

    | Builder method                                                                                                                                                                                                                                                                                                                                                   | Operator type    | Overriden configuration                                                                                                                                                                                                               |
    |------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | [RangeQuery.for_values][diffusion.features.timeseries.query.range_query.RangeQuery.for_values]                                                                                                                                                                                                                                                                                     | value range      | Overrides the existing query type to create a new value range query. Overrides the existing view range with a new view range that selects the entire time series. The existing edit range is copied unchanged.                        |
    | [RangeQuery.for_edits][diffusion.features.timeseries.query.range_query.RangeQuery.for_edits]                                                                                                                                                                                                                                                                                       | value range      | Overrides the existing query type to create a new edit range query that includes all edits. Overrides the existing view range with a new view range that selects the entire time series. The existing edit range is copied unchanged. |
    | [RangeQuery.edit_range][diffusion.features.timeseries.query.range_query.RangeQuery.edit_range]                                                                                                                                                                                                                                                                                     | Edit range       | Overrides the existing edit range with a new edit range that selects the entire time series. The existing view range is copied unchanged.                                                                                             |
    | [RangeQuery.latest_edits][diffusion.features.timeseries.query.range_query.RangeQuery.latest_edits], [RangeQuery.all_edits][diffusion.features.timeseries.query.range_query.RangeQuery.all_edits]                                                                                                                                                                                                     | Edit range       | Overrides the existing edit range with a new edit range that selects the entire time series. The existing view range is copied unchanged.                                                                                             |
    | [RangeQuery.from_][diffusion.features.timeseries.query.range_query.RangeQuery.from_], [RangeQuery.from_start][diffusion.features.timeseries.query.range_query.RangeQuery.from_start] [RangeQuery.from_last][diffusion.features.timeseries.query.range_query.RangeQuery.from_last]                                                                                                                                      | Anchor           | Overrides the anchor of the current range.                                                                                                                                                                                            |
    | [RangeQuery.to][diffusion.features.timeseries.query.range_query.RangeQuery.to], [RangeQuery.to_start][diffusion.features.timeseries.query.range_query.RangeQuery.to_start], [RangeQuery.next][diffusion.features.timeseries.query.range_query.RangeQuery.next], [RangeQuery.previous][diffusion.features.timeseries.query.range_query.RangeQuery.previous], [RangeQuery.until_last][diffusion.features.timeseries.query.range_query.RangeQuery.until_last] | Span             | Overrides the span of the current range.                                                                                                                                                                                              |
    | [RangeQuery.limit][diffusion.features.timeseries.query.range_query.RangeQuery.limit]                                                                                                                                                                                                                                                                                               | Limit            | Overrides the limit.                                                                                                                                                                                                                  |
    | [RangeQuery.as_][diffusion.features.timeseries.query.range_query.RangeQuery.as_]                                                                                                                                                                                                                                                                                                   | query value type | Overrides the query value type.                                                                                                                                                                                                       |

    Added in version 6.9.

    See Also:
        [timeseries.TimeSeries][diffusion.features.timeseries.TimeSeries]
        [timeseries.RangeQuery][diffusion.features.timeseries.query.range_query.RangeQuery]
    """  # noqa: E501, W291

    @classmethod
    def create_default(
        cls,
        session: InternalSession,
        tp: typing.Type[VT],
    ) -> RangeQuery[VT]:
        """
        Create the default Range Query for the given type
        Args:
            session: session from which this query will invoke select operations.
            tp: initial value type of query

        Returns:
            The according default Range Query object.
        """

        @validate_member_arguments
        def checked_result(session: InternalSession, tp: typing.Type[VT]):
            return typing.cast(
                RangeQuery[VT],
                cls(
                    session,
                    RangeQueryParameters.DEFAULT_RANGE_QUERY(),
                    RangeQueryMode.VIEW_RANGE,
                    tp
                )
            )

        return checked_result(session, tp)

    @classmethod
    @functools.lru_cache(maxsize=None)
    def of(
        cls, item: typing.Type[VT]
    ) -> typing.Type[RangeQuery[VT]]:
        @validate_member_arguments
        def raw_class(item: typing.Type[VT]) -> typing.Type[RangeQuery[VT]]:
            return typing.cast(
                "typing.Type[RangeQuery[VT]]",
                type(
                    stringcase.pascalcase(f"{item}{cls.__name__}"),
                    (cls,),
                    dict(value_type=item),
                ),
            )
        return raw_class(item)

    def for_values(self: QuerySelf) -> QuerySelf:
        """
        Returns a copy of this
        [RangeQuery][diffusion.features.timeseries.query.range_query.RangeQuery]
        configured to perform a value range query with the view range set to
        the entire time series.

        Notes:
            <b>Operator type:</b> value range

        Returns:
            The copy of this range query configured to perform a view range
                query with a new view range that selects the entire time series.
        """
        return attr.evolve(
            self,
            parameters=self.parameters.with_query_type(
                QueryType.VALUES
            ).with_view_range(Range.DEFAULT_RANGE()),
            mode=RangeQueryMode.VIEW_RANGE,
        )

    def for_edits(self: QuerySelf) -> QuerySelf:
        """
        Returns a copy of this
        [RangeQuery][diffusion.features.timeseries.query.range_query.RangeQuery]
        configured to perform an edit range query with the view range set to the
        entire time series.

        Notes:
            <b>Operator type:</b> value range

        Returns:
            The copy of this range query configured to perform an edit
                range query with a new view range that selects the entire time series.
        """
        return attr.evolve(
            self,
            parameters=self.parameters.with_query_type(
                QueryType.ALL_EDITS
            ).with_view_range(Range.DEFAULT_RANGE()),
            mode=RangeQueryMode.VIEW_RANGE,
        )

    def edit_range(self: QuerySelf) -> QuerySelf:
        """
        Returns a copy of this
        [RangeQuery][diffusion.features.timeseries.query.range_query.RangeQuery]
        configured to perform a value range query with the edit range set to the
        entire time series.

        Notes:
            This operator can only be applied to value range queries. The default
            query returned by
            [RangeQuery][diffusion.features.timeseries.query.range_query.RangeQuery]
            is a value range query. The
            [RangeQuery.for_values][diffusion.features.timeseries.query.range_query.RangeQuery.for_values]
            operator can be used to create a value range query from an edit range query.

            <b>Operator type:</b> edit range

        Returns:
            The copy of this range query configured to perform a view range
                query with a new edit range that selects the entire time series.

        Raises:
            InvalidOperationException: The current range query is not a value range query.
        """
        if self.parameters.query_type != QueryType.VALUES:
            raise InvalidOperationError(
                f".edit_range() cannot be applied to this edit range query: {self}."
            )

        return attr.evolve(self, mode=RangeQueryMode.EDIT_RANGE)

    def all_edits(self: QuerySelf) -> QuerySelf:
        """
        Returns a copy of this
        [RangeQuery][diffusion.features.timeseries.query.range_query.RangeQuery]
        configured to perform an edit range query with the edit range that
        selects all edits in the entire time series.

        Notes:
            This operator can only be applied to edit range queries. The default
            query returned by
            [RangeQuery][diffusion.features.timeseries.query.range_query.RangeQuery]
            is a value range query. The
            [RangeQuery.for_edits][diffusion.features.timeseries.query.range_query.RangeQuery.for_edits]
            operator can be used to create an edit range query from a value range query.

            <b>Operator type:</b> edit range

        Returns:
            The copy of this range query configured to perform an edit
                range query with a new edit range that selects all edits in
                the entire time series.

        Raises:
            InvalidOperationException: The current range query is not an edit range query.
        """
        if self.parameters.query_type == QueryType.VALUES:
            raise InvalidOperationError(
                f".all_edits() cannot be applied to this value range query: {self}."
            )

        return attr.evolve(
            self,
            parameters=self.parameters.with_query_type(QueryType.LATEST_EDITS),
            mode=RangeQueryMode.EDIT_RANGE,
        )

    def latest_edits(self: QuerySelf) -> QuerySelf:
        """
        Returns a copy of this
        [RangeQuery][diffusion.features.timeseries.query.range_query.RangeQuery]
        configured to perform an edit range query with the edit range that
        selects the latest edits in the entire time series.

        Notes:
            This operator can only be applied to edit range queries. The default
            query returned by
            [RangeQuery][diffusion.features.timeseries.query.range_query.RangeQuery]
            is a value range query. The
            [RangeQuery.for_edits][diffusion.features.timeseries.query.range_query.RangeQuery.for_edits]
            operator can be used to create an edit range query from a value range query.

            <b>Operator type:</b> edit range

        Returns:
            The copy of this range query configured to perform an edit
                range query with a new edit range that selects the latest
                edits in the entire time series.

        Raises:
            InvalidOperationError: The current range query is not an edit range query.
        """
        if self.parameters.query_type == QueryType.VALUES:
            raise InvalidOperationError(
                f".latest_edits() cannot be applied to this value range query: {self}."
            )

        return attr.evolve(
            self,
            parameters=self.parameters.with_query_type(QueryType.LATEST_EDITS),
            mode=RangeQueryMode.EDIT_RANGE,
        )

    def with_current_range(
        self: QuerySelf, range_selector: typing.Callable[[Range], Range]
    ) -> QuerySelf:
        """
        Creates a copy of the current query with a modified range.
        <param name="rangeSelector">The range selector function.</param>
        <returns>The new range query.</returns>

        Args:
            range_selector:

        Returns:
            The copy of this range query with a new transformed range.
        """
        return attr.evolve(
            self,
            parameters=self.mode.change_current_range(
                self.parameters, range_selector
            ),
        )

    def from_(
        self: QuerySelf,
        anchor: typing.Union[StrictNonNegativeInt, StrictTimedelta],
    ) -> QuerySelf:
        """
        Returns a copy of this
        [RangeQuery][diffusion.features.timeseries.query.range_query.RangeQuery]
        with the anchor of the current range configured to be an absolute time.

        Notes:
            <b>Operator type:</b> anchor

        Args:
            anchor: Absolute time specifying the anchor of the range (as a
                `datetime.timedelta` from the epoch) or the absolute sequence number
                specifying the anchor of the returned range.

        Returns:
            The copy of this range query with a new anchor.
        """
        return self.with_current_range(lambda r: r.from_(anchor))

    def from_start(self: QuerySelf) -> QuerySelf:
        """
        Return a copy of this
        [RangeQuery][diffusion.features.timeseries.query.range_query.RangeQuery]
        with the anchor of the current range configured to be the start of the
        time series.

        Notes:
            There is a difference between
            [from_start][diffusion.features.timeseries.query.range_query.RangeQuery.from_start]
            and
            [RangeQuery.from_][diffusion.features.timeseries.query.range_query.RangeQuery.from_](0)
            if the range also ends before the first event of the time series. For
            example, `from_start().to_start()` is always empty, but `from_(0).to_start()`
            includes the event with sequence number `0`.

            *Operator type*: anchor

        Returns:
            The copy of this range query with a new anchor.
        """  # noqa: E501, W291
        return self.with_current_range(lambda r: r.from_start())

    def from_last(
        self: QuerySelf,
        offset: typing.Union[StrictNonNegativeInt, StrictNonNegativeTimedelta],
    ) -> QuerySelf:
        """
        Returns a copy of this
        [RangeQuery][diffusion.features.timeseries.query.range_query.RangeQuery]
        with the anchor of the current range configured to be a relative time
        from the timestamp of the last event in the time series.

        Notes:
            <b>Operator type:</b> anchor

            Takes only one argument - time_span and count are mutually exclusive.

        Args:
            offset:
                The anchor as:
                the time-span relative to the timestamp of the latest event in the time series
                (as a [StrictNonNegativeInt][diffusion.internal.validation.StrictNonNegativeInt])
                or
                the number of events before the end of the time series (as a
                [StrictNonNegativeTimedelta][diffusion.internal.validation.StrictNonNegativeTimedelta])

        Returns:
            The copy of this range query with a new anchor.

        See Also:
            [RangeQuery.from_last_milliseconds][diffusion.features.timeseries.query.range_query.RangeQuery.from_last_milliseconds]
        """  # noqa: E501, W291
        return self.with_current_range(lambda r: r.from_last(offset))

    def from_last_milliseconds(
        self: QuerySelf, milliseconds: StrictNonNegativeInt
    ) -> QuerySelf:
        """
        Returns a copy of this
        [RangeQuery][diffusion.features.timeseries.query.range_query.RangeQuery]
        with the anchor of the current range configured to be a relative time from the
        timestamp of the last event in the time series.
        Notes:
            <b>Operator type:</b> anchor

        Args:
            milliseconds:
                The milliseconds relative to the timestamp of the latest event in
                    the time series.

        Returns:
            The copy of this range query with a new anchor.

        See Also:
            [RangeQuery.from_last][diffusion.features.timeseries.query.range_query.RangeQuery.from_last]
        """  # noqa: E501, W291
        return self.with_current_range(
            lambda r: r.from_last_milliseconds(milliseconds)
        )

    def to(
        self: QuerySelf,
        time: typing.Union[StrictNonNegativeInt, StrictTimedelta],
    ) -> QuerySelf:
        """
        Returns a copy of this
        [RangeQuery][diffusion.features.timeseries.query.range_query.RangeQuery]
        with the span of the current range configured to end at an absolute sequence number.

        Notes:
            <b>Operator type:</b> span

        Args:
            time:
                Either:
                    - the absolute sequence number specifying the end of the returned range (as a
                [StrictNonNegativeInt][diffusion.internal.validation.StrictNonNegativeInt] or
                    - the absolute time specifying the end of the range (as a
                [StrictTimedelta][diffusion.internal.validation.StrictTimedelta])

        Returns:
            The copy of this range query with a new span.
        """  # noqa: E501, W291
        return self.with_current_range(lambda x: x.to(time))

    def to_start(self: QuerySelf) -> QuerySelf:
        """
        Returns a copy of this
        [RangeQuery][diffusion.features.timeseries.query.range_query.RangeQuery]
        with the span of the current range configured to end at the start of the time series.

        Notes:
            There is a difference between to_start() and `to(0)` if
            the range also starts before the first event of the time series. For
            example, `from_start().to_start()` is always empty, but
            `from_start().to(0)` includes the event with sequence number `0`.

            <b>Operator type:</b> span

        Returns:
            The copy of this range query with a new span.
        """
        return self.with_current_range(lambda x: x.to_start())

    def until_last(
        self: QuerySelf,
        offset: typing.Union[
            StrictNonNegativeInt, StrictNonNegativeTimedelta
        ],
    ) -> QuerySelf:
        """
        Returns a copy of this
        [RangeQuery][diffusion.features.timeseries.query.range_query.RangeQuery]
        with the span of the current range configured to end at a relative point from the
        last event in the time series.

        Notes:
            <b>Operator type:</b> span

        Args:
            offset: The offset from the end of the time series as:
                - time span (as a `datetime.timedelta`) or
                - sequence count (as a non-negative `int`)

        Returns:
            The copy of this range query with a new span.

        See Also:
            [RangeQuery.until_last_milliseconds][diffusion.features.timeseries.query.range_query.RangeQuery.until_last_milliseconds]
        """  # noqa: E501, W291
        return self.with_current_range(lambda x: x.until_last(offset))

    def until_last_milliseconds(
        self: QuerySelf, milliseconds: StrictNonNegativeInt
    ) -> QuerySelf:
        """
        Returns a copy of this
        [RangeQuery][diffusion.features.timeseries.query.range_query.RangeQuery]
        with the span of the current range configured to end at a relative time from the
        timestamp of the last event in the time series.

        Notes:
            <b>Operator type:</b> span

        Args:
            milliseconds:
                The end of the range of events to select as a number of milliseconds
                relative to the timestamp of the latest event in the time series.

        Returns:
            The copy of this range query with a new span.

        See Also:
            [RangeQuery.until_last][diffusion.features.timeseries.query.range_query.RangeQuery.until_last]
        """  # noqa: E501, W291
        return self.with_current_range(
            lambda r: r.until_last_milliseconds(milliseconds)
        )

    def next(
        self: QuerySelf,
        offset: typing.Union[StrictNonNegativeInt, StrictNonNegativeTimedelta],
    ) -> QuerySelf:
        """
        Return a copy of this [RangeQuery][diffusion.features.timeseries.query.range_query.RangeQuery] with the span of
        the current range configured to select either a temporal or sequential range of events following the anchor.

        Notes:
            <b>Operator type:</b> span

        Args:
            offset: either the time span of events following the anchor to select (as a
                [StrictNonNegativeTimedelta][diffusion.internal.validation.StrictNonNegativeTimedelta])
                or the end of the range of events to select following the anchor (as a
                [StrictNonNegativeInt][diffusion.internal.validation.StrictNonNegativeInt])

        Returns:
            The copy of this range query with a new span.

        See Also:
            [RangeQuery.next_milliseconds][diffusion.features.timeseries.query.range_query.RangeQuery.next_milliseconds]
        """  # noqa: E501, W291
        return self.with_current_range(lambda x: x.next(offset))

    def next_milliseconds(
        self: QuerySelf, milliseconds: StrictNonNegativeInt
    ) -> QuerySelf:
        """
        Returns a copy of this [RangeQuery][diffusion.features.timeseries.query.range_query.RangeQuery] with the span of
        the current range configured to select a temporal range of events following the anchor.

        Notes:
            <b>Operator type:</b> span

        Args:
            milliseconds:
                The time span in milliseconds of events following the anchor to select.

        Returns:
            The copy of this range query with a new next milliseconds value.

        See Also:
            [RangeQuery.next][diffusion.features.timeseries.query.range_query.RangeQuery.next]
        """  # noqa: E501, W291
        return self.with_current_range(
            lambda x: x.next_milliseconds(milliseconds)
        )

    def previous(
        self: QuerySelf,
        offset: typing.Union[StrictNonNegativeInt, StrictNonNegativeTimedelta],
    ) -> QuerySelf:
        """
        Returns a copy of this [RangeQuery][diffusion.features.timeseries.query.range_query.RangeQuery] with the span of
        the current range configured to select a range of events preceding the anchor.

        Notes:
            For value range queries, `count` is the
            number of original events.For edit range queries, <paramref name="count"/>
            is the number of events of any type.

            <b>Operator type:</b> span

        Args:
            offset:
                - The end of the range of events to select preceding the anchor (as a
                [StrictNonNegativeInt][diffusion.internal.validation.StrictNonNegativeInt]) or
                - The time span of events preceding the anchor to select (as a
                [StrictNonNegativeTimedelta][diffusion.internal.validation.StrictNonNegativeTimedelta])

        Returns:
            The copy of this range query with a new span.
        """  # noqa: E501, W291
        return self.with_current_range(lambda x: x.previous(offset))

    def previous_milliseconds(
        self: QuerySelf, milliseconds: StrictNonNegativeInt
    ) -> QuerySelf:
        """
        Returns a copy of this [RangeQuery][diffusion.features.timeseries.query.range_query.RangeQuery] with the span of
        the current range configured to select a temporal range of events preceding the anchor.

        Notes:
            <b>Operator type:</b> span

        Args:
            milliseconds:
                The time span in milliseconds of events preceding the anchor to select.

        Returns:
            The copy of this range query with a new span.

        See Also:
            [RangeQuery.previous][diffusion.features.timeseries.query.range_query.RangeQuery.previous]

        """  # noqa: E501, W291
        return self.with_current_range(
            lambda x: x.previous_milliseconds(milliseconds)
        )

    def limit(self: QuerySelf, count: StrictNonNegativeInt) -> QuerySelf:
        """
        Returns a copy of this [RangeQuery][diffusion.features.timeseries.query.range_query.RangeQuery] that returns at most count events.

        Notes:
            If the query would otherwise select more than <paramref name="count"/> events,
            only the latest <paramref name="count"/> values (those with the highest sequence numbers)
            are returned.

            This is most useful when a temporal span has been configured with [RangeQuery.next][diffusion.features.timeseries.query.range_query.RangeQuery.next]
            or [RangeQuery.previous][diffusion.features.timeseries.query.range_query.RangeQuery.previous], where the potential number of returned events is unknown.

            <see cref="IQueryResult{VT}.IsComplete"/> can be used to determine
            whether a query has returned an incomplete result.

            <b>Operator type:</b> limit

        Args:
            count: The maximum number of events to return.

        Returns:
            The copy of this range query with a new limit.
        """   # noqa: E501, W291
        return attr.evolve(self, parameters=self.parameters.with_limit(count))

    def as_(self, tp: typing.Type[VT_other]) -> RangeQuery[VT_other]:
        """
        Returns a copy of this
        [RangeQuery][diffusion.features.timeseries.query.range_query.RangeQuery]
        with a different query value type.

        Notes:
            A query can only be evaluated successfully against time series topics with a compatible
            event data type. If a query method is called for a time series topic with an incompatible
            event data type, the query will complete exceptionally.

        If the event data type of the time series topic is known, compatibility of a particular
        value type can be checked using `AbstractDataType.can_read_as`. The
        default
        [timeseries.RangeQuery][diffusion.features.timeseries.query.range_query.RangeQuery] has
        a query value type of [IBytes][diffusion.datatypes.foundation.ibytesdatatype.IBytes],
        which is compatible with all time series value data types.

        <b>Operator type:</b> query value type

        Args:
            tp: The new value type.

        Returns:
            The copy of this range query with a new query value type.
        """  # noqa: E501, W291
        @validate_member_arguments
        def raw_class(tp: typing.Type[VT_other]) -> RangeQuery[VT_other]:
            return typing.cast(
                "RangeQuery[VT_other]",
                attr.evolve(self, tp=typing.cast(typing.Type[VT], tp)),
            )

        return raw_class(tp)

    def __str__(self):
        return f"range_query({repr(self.tp)}){self.parameters.__str__()}"

    @validate_member_arguments
    async def select_from(self, topic_path: pydantic.StrictStr) -> QueryResult[VT]:
        """
        Evaluates this query for a time series topic.

        Notes:
            The calling session must have the `.PathPermission.READ_TOPIC`
            topic permission for `topic_path` to evaluate the query.
            The `PathPermission.QUERY_OBSOLETE_TIME_SERIES_EVENTS`
            topic permission is also required if this is a
            [RangeQuery.for_edits][diffusion.features.timeseries.query.range_query.RangeQuery.for_edits]
            range query, or a
            [RangeQuery.for_values][diffusion.features.timeseries.query.range_query.RangeQuery.for_values]
            range query with an
            [RangeQuery.edit_range][diffusion.features.timeseries.query.range_query.RangeQuery.edit_range].

        Args:
            topic_path: The path of the time series topic to query.

        Returns:
            An object providing the results.

        Raises:
            NoSuchTopicError: There is no topic bound to `topic_path`.
            IncompatibleTopicError: The [value type][diffusion.datatypes.timeseries.types.VT]
                does not match the event data type of the time series topic bound to
                `topic_path`, or the topic bound to `topic_path` is not a time series topic.
            InvalidQueryError: The range query is not valid for the time series.
            SessionSecurityError: The calling session does not have `PathPermission.READ_TOPIC`
                permission for `topic_path`.
                The calling session does not have
                `PathPermission.QUERY_OBSOLETE_TIME_SERIES_EVENTS`
                permission for `topic_path` and this is a
                [RangeQuery.for_edits][diffusion.features.timeseries.query.range_query.RangeQuery.for_edits]
                range query, or a
                [RangeQuery.for_values][diffusion.features.timeseries.query.range_query.RangeQuery.for_values]
                range query with an
                [RangeQuery.edit_range][diffusion.features.timeseries.query.range_query.RangeQuery.edit_range].
            SessionClosedError: The calling session is closed.
        """  # noqa: E501, W291
        from diffusion.internal.timeseries.query.range_query_result import RangeQueryResult

        request = RangeQueryRequest(topic_path=topic_path, parameters=self.parameters)

        result = await self.session.services.RANGE_QUERY.invoke(
            self.session, request, RangeQueryResult
        )
        return result.to_query_result(
            self.tp, self.parameters.query_type.stream_structure
        )
