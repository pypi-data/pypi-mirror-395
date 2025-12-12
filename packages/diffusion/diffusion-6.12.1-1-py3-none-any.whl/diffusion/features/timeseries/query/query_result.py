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

import copy
import itertools
import typing

from diffusion.datatypes.timeseries import Event, VT
from diffusion.datatypes.timeseries.time_series_event import EditEvent
from diffusion.features.timeseries.query.range_query_parameters import StreamStructure
from diffusion.internal.utils import validate_member_arguments
from diffusion.internal.validation import StrictNonNegativeInt
import attr

QueryResultSelf = typing.TypeVar("QueryResultSelf", bound="QueryResult")


T = typing.TypeVar("T")
Key = typing.TypeVar("Key")


@attr.s(auto_attribs=True, eq=True, hash=True, frozen=True)
class QueryResult(typing.Generic[VT]):
    """
    The query result providing a stream of events.

    Since:
        6.9
    """

    @classmethod
    @validate_member_arguments
    def from_events(
        cls: typing.Type[QueryResultSelf],
        selected_count: StrictNonNegativeInt,
        stream_structure: StreamStructure,
        events: typing.Collection[Event[VT]],
        read_value: typing.Callable[[Event[VT]], typing.Optional[Event[VT]]],
    ) -> QueryResultSelf:
        return cls(
            selected_count,
            len(events),
            stream_structure,
            [x for x in map(read_value, events) if x is not None],
        )

    selected_count: int
    """
    Gets the number of events selected by the query.

    Notes:
        This number may be greater than `len(stream)` due to a
        policy of the time series topic to limit the number of returned
        results, or the use of <see cref="IRangeQuery{VT}.limit(StrictNonNegativeInt)"/>.
    """

    event_count: StrictNonNegativeInt
    stream_structure: StreamStructure = StreamStructure.VALUE_EVENT_STREAM
    """
    The stream structure of the provided events.
    """

    events: typing.List[Event[VT]] = []
    """
    The events as a list.
    """

    @property
    def is_complete(self) -> bool:

        """
        Gets whether this result includes all events selected by the query.
        Returns:
            `True` if
                [QueryResult.selected_count][diffusion.features.timeseries.query.query_result.QueryResult.selected_count]
                is equal to the amount of events in
                [QueryResult.events][diffusion.features.timeseries.query.query_result.QueryResult.events].
                Otherwise `False`.
        """  # noqa: E501, W291
        return self.selected_count == self.event_count

    def merge(self, other: QueryResult[VT]) -> QueryResult[VT]:
        """
        Merges this result with `other`, combining original events and
        edit events, to produce a
        [QueryResult][diffusion.features.timeseries.query.query_result.QueryResult]
        of type
        [StreamStructure.VALUE_EVENT_STREAM][diffusion.features.timeseries.query.range_query_parameters.StreamStructure.VALUE_EVENT_STREAM]

        Notes:
            The following rules are applied to calculate the result:

        - If this result and `other` have an event with equal
        sequence numbers, the event from `other` is selected.
        - An edit event is selected in place of its original event.
        - If there are multiple edit events of an original edit, the one
                with the highest sequence is selected.

        The returned result implements <see cref="IQueryResult{VT}.IsComplete"/>
        to return true and <see cref="IQueryResult{VT}.SelectedCount"/>
        to return the count of events in the stream, regardless of whether this result is complete.

        Args:
            other: The other query result to merge with.

        Returns:
            The newly merged query result.

        Raises:
            ArgumentNoneError: other is `None`
        """  # noqa: E501, W291

        sorted_events: typing.List[Event] = sorted(
            copy.deepcopy(self.events + other.events),
            key=lambda x: (x.original_event.sequence, x.metadata.sequence),
        )
        mapped = map(
            self.replace_with_latest(self.events + other.events), sorted_events
        )
        merged = [x for x in mapped if x is not None]
        count = len(merged)

        return QueryResult(count, count, StreamStructure.VALUE_EVENT_STREAM, merged)

    @staticmethod
    def replace_with_latest(
        all_events: typing.List[Event[VT]],
    ) -> typing.Callable[[Event[VT]], Event[VT]]:
        def linq_group_by(
            source: typing.Iterable[T],
            key_selector: typing.Callable[[T], Key],
            element_selector: typing.Callable[[T], T],
            result_selector: typing.Callable[
                [Key, typing.Iterable[T]], typing.Tuple[Key, T]
            ],
        ) -> typing.Iterable[typing.Tuple[Key, T]]:
            return (
                result_selector(key, list(map(element_selector, value)))
                for key, value in itertools.groupby(source, key_selector)
            )

        latest_by_original_sequence = dict(
            linq_group_by(
                all_events,
                lambda e: e.original_event.sequence,
                lambda e: e,
                lambda key, items: (
                    key,
                    list(sorted(items, key=lambda e: e.metadata.sequence))[-1],
                ),
            )
        )

        def converter(input: Event[VT]):
            original_sequence = input.original_event.sequence
            latest = latest_by_original_sequence.get(original_sequence)
            if latest is None:
                # original has already been replaced with latest, or
                # this is a duplicate latest edit event
                return None

            if not isinstance(input, EditEvent):
                # original edit event
                del latest_by_original_sequence[original_sequence]
                return latest
            elif input.metadata.sequence == latest.metadata.sequence:
                # latest edit event without original event
                del latest_by_original_sequence[original_sequence]
                return input

            # intermediate edit
            return None

        return converter

    def __str__(self):
        return (
            f"QueryResult selected count={self.selected_count} "
            f"event count={self.event_count} structure={self.stream_structure}"
        )
