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

import datetime
import typing
import typing_extensions

from diffusion.datatypes.foundation.ibytesdatatype import IBytes
from diffusion.datatypes.timeseries import (
    EventMetadata,
    TimeSeriesEventDataType,
    TimeSeriesDataType, validate_ts_typed,
)
from diffusion.datatypes.timeseries.types import (
    TimeSeriesValueTypeClasses,
    TimeSeriesValueType,
    TimeSeriesValueTypeOrRaw,
    VT
)
from diffusion.handlers import LOG
from diffusion.internal.components import Component
from diffusion.internal.serialisers.timeseries import (
    TimeSeriesAppendRequest,
    TimeSeriesTimestampAppendRequest,
    TimeSeriesEditRequest,
)
from diffusion.internal.utils import (
    validate_member_arguments,
)
if typing.TYPE_CHECKING:
    from diffusion.features.timeseries.query.range_query import RangeQuery
import diffusion.datatypes
from diffusion.internal.validation import StrictNonNegativeInt


@validate_member_arguments
def get_val(
    value: TimeSeriesValueTypeOrRaw,
    value_type_final: TimeSeriesValueTypeClasses,
) -> TimeSeriesValueType:
    value_final: TimeSeriesValueType
    try:
        if not isinstance(value, value_type_final):
            value_final = value_type_final(value)  # type: ignore
        else:
            value_final = value  # type: ignore
    except Exception as e:  # pragma: no cover
        LOG.error(f"Got exception {e}")
        raise

    return value_final


class TimeSeries(Component):
    """
    This feature allows a session to update and query time series topics.

    # Time series topics

    A *time series* is a sequence of events. Each event contains a value
    and has server-assigned metadata comprised of a sequence number, timestamp,
    and author. Events in a time series are ordered by increasing sequence
    number. Sequence numbers have values between `0`  and
    `Number.MAX_INTEGER`  and are contiguous: an event with sequence number
    `n`  will be followed by one with sequence number `n + 1` . Two
    events with the same sequence number will be equal &ndash; having the same
    timestamp, author, and value.

    A time series topic allows sessions to access a time series that is
    maintained by the server. A time series topic has an associated
    [DataType event data type][diffusion.datatypes.foundation.datatype.DataType],
    such as `Binary`, `String`, or `JSON`,
    that determines the type of value associated with each event.

    This feature provides a historic query API for time series topics, allowing a
    session to query arbitrary sub-sequences of a time series.

    To create a Time Series type, use the
    [TimeSeries.of][diffusion.features.timeseries.TimeSeries.of]
    method.

    The [Session.topics][diffusion.session.Session.topics] and
    [Topics.add_value_stream][diffusion.features.topics.Topics.add_value_stream]
    features complete the API, providing ways to create and subscribe
    to a time series topic using this type.

    The API presents a time series as an append-only data structure of immutable
    events that is only changed by adding new events.

    ## Edit events

    Although a time series is append-only, an event can be overridden by
    appending an *edit event*. An edit event is a special type of event
    that overrides an earlier event in the time series (referred to as the
    *original event*) with a new value. When an edit event is added to a
    time series, the server retains both the original event and the edit event,
    allowing subscription and query results to reflect the edit.

    For example, suppose a time series has two events with the values `A`
    and `B` , and the first event has been overridden by a later edit event
    that provides a new value of `X` . The server has the following
    information about the time series.

    Sequence  |  value  |  tp
    --------- | ------- | -------
    0         | A       | *original event*
    1         | B       | *original event*
    2         | X       | *edit of sequence 0*

    The current value of the event with sequence number 0 is `X` .

    If an original event has several edit events, the latest edit event (the one
    with the highest sequence number) determines its current value. Each edit
    event refers to an original event, never to another edit event.

    Extending the example by appending a further edit event to the time series:

    Sequence  |  value  |  tp
    --------- | ------- | -------
    3         | Y       | *second edit of sequence 0*

    The current value of the event with sequence number 0 is now `Y` .

    ### Retained range

    A time series topic retains a range of the most recent events. When a new
    event is added to the time series, older events that fall outside of the
    range are discarded. By default, this range includes the ten most recent
    events. A different range can be configured by setting the
    [TIME_SERIES_RETAINED_RANGE]
    [diffusion.datatypes.timeseries.TopicSpecification.TIME_SERIES_RETAINED_RANGE] property.

    ## Subscribing to a time series topic

    A session can select a time series topic and
    [add a value stream][diffusion.features.topics.Topics.add_value_stream]
    to receive updates about events
    appended to the time series. Events are represented by
    [Event][diffusion.datatypes.timeseries.time_series_event]
    instances. Each event has a value and
    [metadata][diffusion.datatypes.timeseries.time_series_event_metadata.EventMetadata]. An edit
    event has two sets of metadata &ndash; its own metadata and that of the
    original event that it replaces.

    ### Subscription range

    New subscribers are sent a range of events from the end of the time series.
    This is known as the *subscription range*. Configuring a subscription
    range is a convenient way to provide new subscribers with an appropriate
    subset of the latest events.

    The default subscription range depends on whether the topic is configured to
    publish delta streams. If delta streams are enabled, new subscribers are sent
    the latest event if one exists. If delta streams are disabled, new
    subscribers are sent no events. Delta streams are enabled by default and can
    be disabled by setting the
    [PUBLISH_VALUES_ONLY]
    [diffusion.features.topics.details.topic_specification.TopicSpecification.PUBLISH_VALUES_ONLY]
    property to `true`.

    A larger subscription range can be configured by setting the
    [TIME_SERIES_SUBSCRIPTION_RANGE]
    [diffusion.datatypes.timeseries.TopicSpecification.TIME_SERIES_SUBSCRIPTION_RANGE]
    property. Regardless of this property, if delta streams are
    enabled, new subscribers will be sent at least the latest event if one
    exists.

    If the range of events is insufficient, the subscribing session can use a
    [range query][diffusion.features.timeseries.TimeSeries.range_query] to retrieve older events.

    When configuring a non-default subscription range for a time series topic,
    register value streams before subscribing to the topic. The session only
    maintains a local cache if the latest value received for a topic, not the
    full subscription range. If a value stream is added after a session has
    subscribed to a matching time series topic, the new stream will only be
    notified of the latest value.

    ## Updating a time series topic

    A session can use
    [append][diffusion.features.timeseries.TimeSeries.append]
    to submit a value
    to be added to a time series. The server will add an event to the end of the
    time series based on the supplied value, with a new sequence number,
    timestamp, and the author set to the authenticated principal of the session.

    Providing a number as fourth argument to
    [append][diffusion.features.timeseries.TimeSeries.append]
    allows a session to submit a value and supplied time. This provides control
    over the timestamp of the event. The supplied instant must be synchronous to
    or more recent than the latest event stored by the time series topic. There
    are no other restrictions.

    A session can use [edit][diffusion.features.timeseries.TimeSeries.edit] to submit an edit to
    an original time series event, identified by its sequence number. The server
    will add an edit event to the end of the time series based on the supplied
    value, with a new sequence number, timestamp, and the author set to the
    authenticated principal of the session.

    Time series topics can also be updated using the functionality provided by
    the [Topic Update][diffusion.features.topics.Topics] feature.
    This includes [set_topic][diffusion.features.topics.Topics.set_topic]
    and `Update Stream`s. This usage performs an append operation with the added
    benefits of `Update Constraint`s, topic creation when updating (upsert),
    and delta streams. When using methods from [Topic Update][diffusion.features.topics.Topics] the sequence
    number, timestamp and author metadata will be generated using the same rules
    as [TimeSeries.append][diffusion.features.timeseries.TimeSeries.append] but the associated
    [EventMetadata][diffusion.datatypes.timeseries.time_series_event_metadata.EventMetadata]
    will not be returned to the caller.

    ## Changes to a time series made outside the API

    The API presents a time series as an append-only data structure of immutable
    events that is only changed by adding new events. The API does not allow
    events to be deleted or edited.

    There are circumstances in which events can be removed from a time series by
    server operations outside the API. For example, a time series topic can be
    configured to discard or archive older events to save storage space; or the
    time series may be held in memory and lost if the server restarts. Subscribed
    sessions are not notified when events are removed in this way, but a session
    can infer the removal of events that are no longer included in query results.
    Similarly, an event's value can be changed on the server. For example, if an
    administrator changes its value to redact sensitive data. Again, subscribed
    sessions are not notified when events are modified, but a session can infer
    this has happened from query results.

    Whether such changes can happen for a particular time series topic depends on
    the topic specification, and the administrative actions that are allowed. To
    write a robust application, do not rely on two Event instances with the same
    sequence number but obtained though different API calls, being equal; nor
    that there are no sequence number gaps between events in query results.

    ## Access control

    The session must have the READ_TOPIC topic
    permission for a topic to query a time series topic. The
    QUERY_OBSOLETE_TIME_SERIES_EVENTS
    path permission is additionally required
    to evaluate an edit range query, or a value range query with an edit range.

    The session must have the `UPDATE_TOPIC`
    path permission for a topic to [append][diffusion.features.timeseries.TimeSeries.append] a new event
    to a time series topic. The
    `EDIT_TIME_SERIES_EVENTS` path permission is additionally required to
    [submit an edit][diffusion.features.timeseries.TimeSeries.edit] to any time series event. The more
    restrictive `EDIT_OWN_TIME_SERIES_EVENTS`
    path permission allows a session to submit
    edits to time series topic events that are authored by the principal of the
    calling session.

    Since 6.8.3
    """  # noqa: E501, W291

    async def edit(
        self,
        topic_path: str,
        original_sequence: int,
        value: TimeSeriesValueTypeOrRaw,
        value_type: TimeSeriesValueTypeClasses,
    ) -> EventMetadata:
        """
        Update a time series topic by appending a new value that overrides the
        value of an existing event.

        The existing event is identified by its sequence number and must be an
        original event.

        The server will add an edit event to the end of the time series based on
        the supplied value, with a new sequence number, timestamp, and the author
        set to the authenticated principal of the session.

        Args:
            topic_path:         the path of the time series topic to update
            original_sequence:  the sequence number of the original event to edit
            value:              the event value
            value_type:         the type of the supplied value. This must match
                the value type of the
                [DataType][diffusion.datatypes.foundation.datatype.DataType]
                configured as the time series topic's
                [TIME_SERIES_EVENT_VALUE_TYPE]
                [diffusion.datatypes.timeseries.TopicSpecification.TIME_SERIES_EVENT_VALUE_TYPE]
                event value type}.

        Returns:
            a result that completes when a response is received from the server.
        """
        value_final = validate_ts_typed(value, value_type)
        request = TimeSeriesEditRequest(
            topic_path=topic_path,
            value_type=str(value_type),
            original_sequence=original_sequence,
            value=bytes(value_final),
        )
        return await self.session.services.TIME_SERIES_EDIT.invoke(
            self.session, request, response_type=EventMetadata
        )

    async def append(
        self,
        topic_path: str,
        value: TimeSeriesValueTypeOrRaw,
        value_type: typing.Type[TimeSeriesValueType],
        timestamp: typing.Optional[
            typing.Union[datetime.datetime, StrictNonNegativeInt]
        ] = None,
    ) -> EventMetadata:
        """
        Update a time series topic by appending a new value.

        The server will add an event to the end of the time series based on the
        supplied value, with a new sequence number, timestamp, and the author set
        to the authenticated principal of the session.

        Args:
            topic_path: the path of the time series topic to update
            value:  the event value
            value_type:  the type of the supplied value.
                This must match the value type of the
                [DataType][diffusion.datatypes.foundation.datatype.DataType]
                configured as the time series topic's
                [TIME_SERIES_EVENT_VALUE_TYPE]
                [diffusion.datatypes.timeseries.TopicSpecification.TIME_SERIES_EVENT_VALUE_TYPE]
                event value type.
            timestamp: an optional timestamp. The timestamp must be greater or
                equal to that of the most recent event appended to the topic.
                If specifying this as a `datetime.datetime` it should be timezone-aware,
                otherwise UTC will be assumed.
        Returns:
            a result that completes when a response is received from the server.
        """
        value_final = validate_ts_typed(typing.cast(TimeSeriesValueType, value), value_type)

        request: TimeSeriesAppendRequest
        args = dict(
            topic_path=topic_path,
            value_type=str(value_type),
            value=value_final,
        )
        if timestamp is not None:
            if isinstance(timestamp, datetime.datetime):
                if not timestamp.tzinfo:
                    # Naive datetime, we can only assume UTC.
                    # We may be able to type-annotate this in future:
                    # https://github.com/pydantic/pydantic/discussions/3477
                    LOG.warning(
                        f"Timestamp {timestamp} without timezone provided, assuming UTC"
                    )
                timestamp = int(timestamp.astimezone(datetime.timezone.utc).timestamp() * 1000)

            service = self.session.services.TIME_SERIES_TIMESTAMP_APPEND
            request = TimeSeriesTimestampAppendRequest(
                **args,
                timestamp=timestamp,
            )
        else:
            request = TimeSeriesAppendRequest(**args)
            service = self.session.services.TIME_SERIES_APPEND

        return await service.invoke(self.session, request, response_type=EventMetadata)

    @classmethod
    def of(
        cls,
        val_type: typing.Type[
            typing.Union[
                VT
            ]
        ],
    ) -> typing.Type[
        TimeSeriesEventDataType[VT]
    ]:
        """
        Provide a Time Series datatype with the given
        inner value type.

        Args:
            val_type: the type of value that events will contain.

        Returns:
            The relevant Time Series data type.
        """

        return TimeSeriesDataType.of(val_type)

    @typing_extensions.overload
    def range_query(
        self, tp: typing.Type[VT]
    ) -> RangeQuery[VT]:
        ...

    @typing_extensions.overload
    def range_query(self) -> RangeQuery[IBytes]:
        ...

    def range_query(
        self,
        tp: typing.Type[
            typing.Union[VT, IBytes]
        ] = IBytes,
    ) -> typing.Union[
        RangeQuery[VT], RangeQuery[IBytes]
    ]:
        """
        Return the default Range Query.

        Args:
            tp: the type of the query

        Returns:
            The default range query for the given type.
        """
        from diffusion.features.timeseries.query.range_query import RangeQuery

        return RangeQuery.create_default(
            self.session,
            tp=typing.cast(
                typing.Type[typing.Union[VT, IBytes]],
                tp,
            ),
        )
