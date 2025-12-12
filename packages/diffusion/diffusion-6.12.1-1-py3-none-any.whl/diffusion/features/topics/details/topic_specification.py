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

import enum
import functools
import typing
from collections.abc import Hashable

from diffusion.internal.pydantic_compat.v1 import generics as pydantic_v1_generics
from diffusion.internal.pydantic_compat.v1 import BaseConfig
from typing_extensions import TypeAlias

from diffusion.datatypes.foundation.abstract import ValueTypeProtocol
from diffusion.internal.mapping import ImmutableMapping

T = typing.TypeVar("T", covariant=True, bound=ValueTypeProtocol)
T_other = typing.TypeVar("T_other", covariant=True, bound=ValueTypeProtocol)

"""
A [DataType][diffusion.datatypes.foundation.datatype.DataType] type variable.
"""

class WithProperties(typing.Generic[T]):
    def __get__(
            self,
            instance: typing.Optional[TopicSpecification[T]],
            owner: typing.Type[TopicSpecification[T]],
    ) -> typing.Type[TopicSpecification[T]]:
        """
        Return a TopicSpecification class prefilled with `owner`

        Args:
            instance: the instance on which this is called
            owner: the class on which this is called

        Returns:
            Return a TopicSpecification class prefilled with `owner`
        """
        return owner


class CompressionPolicy(str, enum.Enum):
    """
    Compression Level
    """

    OFF = "off"
    """
    Disables compression completely for the topic and requires no additional CPU.
    """
    LOW = "low"
    """
    Low compression.

    Generally some compression is beneficial, so the default value for this
    property is this.
    """
    MEDIUM = "medium"
    """
    Medium compression.
    """
    HIGH = "high"
    """
    Compresses the topic messages to the smallest number of bytes, but has the highest CPU cost.
    """


class TopicDeliveryPriority(str, enum.Enum):
    """ Topic Delivery Priority """

    LOW = "low"
    """
    Low priority.
    """
    DEFAULT = "default"
    """
    Default priority.
    """
    HIGH = "high"
    """
    High priority.
    """


class ConflationPolicy(str, enum.Enum):
    """ Conflation Policy """

    OFF = "off"
    """
    Disables conflation for the topic. This policy
    disables all conflation for the topic, so topic updates will never be
    merged or discarded.
    """
    CONFLATE = "conflate"
    """
    Automatically conflates topic updates when
    back pressure is detected by the server.
    """
    UNSUBSCRIBE = "unsubscribe"
    """
    Automatically unsubscribes the topic when
    back pressure is detected by the server. The unsubscription is not
    persisted to the cluster. If a session fails over to a different server
    it will be resubscribed to the topic.
    """
    ALWAYS = "always"
    """
    Automatically conflates topic updates as they
    are queued for the session. This is an eager policy that ensures only the
    latest update is queued for the topic, minimising the server memory and
    network bandwidth used by the session.
    """


class TopicSpecification(typing.Generic[T], pydantic_v1_generics.GenericModel):
    """
    Topic specifications provide the information required to create a topic.
    Topics can be created from a topic specification using
    [add_topic][diffusion.features.topics.Topics.add_topic].

    Topic specifications allow an application to introspect the type and
    capabilities of a topic. Topic specifications are provided to
    [ValueStream value streams][diffusion.features.topics.streams.ValueStreamHandler] and
    [TopicNotifications topic notification listeners][diffusion.features.topics.streams.ValueStreamHandler]

    A topic specification has a [topic type][diffusion.datatypes.foundation.datatype.DataType] and a map of
    property settings which define the behavior of the topic. A

    Topic specification types can be derived from any datatype using its
    [with_properties][diffusion.datatypes.foundation.abstract.AbstractDataType.with_properties] member.
    This will return a
    [TopicSpecification][diffusion.features.topics.details.topic_specification.TopicSpecification]
    type ready for instantiation with the relevant parameters.

    Topic specifications with
    different properties can be derived from any instance using
    [with_properties]
    [diffusion.features.topics.details.topic_specification.TopicSpecification.with_properties].

    # Topic Properties

    Depending on the topic type, some properties must be included in the
    specification when creating a topic and some properties have no effect. The
    required and optional properties for each the topic type are set out in the
    following table. Properties unsupported by the topic type are ignored.

    | Default when optional                                                                                                                     | [STRING][diffusion.datatypes.STRING] [JSON][diffusion.datatypes.JSON] [BINARY][diffusion.datatypes.BINARY]                                               | [DOUBLE][diffusion.datatypes.DOUBLE] [INT64][diffusion.datatypes.INT64]   | [RECORD_V2][diffusion.datatypes.RECORD_V2]   | [TIME_SERIES][diffusion.datatypes.TIME_SERIES]   
    | ----------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- -------- | ------------------------------------------------------------------------- | -------------------------------------------- | ------------------------------------------------ 
    | [COMPRESSION][diffusion.features.topics.details.topic_specification.TopicSpecification.COMPRESSION]                                       | [CompressionPolicy.LOW][diffusion.features.topics.details.topic_specification.CompressionPolicy.LOW]                                                     | Optional                                                                  | —                                            | Optional                                         
    | [CONFLATION][diffusion.features.topics.details.topic_specification.TopicSpecification.CONFLATION]                                         | [ConflationPolicy.CONFLATE][diffusion.features.topics.details.topic_specification.ConflationPolicy.CONFLATE]                                             | Optional                                                                  | Optional                                     | Optional                                         
    | [DONT_RETAIN_VALUE][diffusion.features.topics.details.topic_specification.TopicSpecification.DONT_RETAIN_VALUE]                           | `False`                                                                                                                                                  | Optional                                                                  | Optional                                     | Optional                                         
    | [OWNER][diffusion.features.topics.details.topic_specification.TopicSpecification.OWNER]                                                   | Optional                                                                                                                                                 | Optional                                                                  | Optional                                     | Optional                                         
    | [PERSISTENT][diffusion.features.topics.details.topic_specification.TopicSpecification.PERSISTENT]                                         | `True`                                                                                                                                                   | Optional                                                                  | Optional                                     | Optional                                         
    | [PRIORITY][diffusion.features.topics.details.topic_specification.TopicSpecification.PRIORITY]                                             | [TopicDeliveryPriority.DEFAULT][diffusion.features.topics.details.topic_specification.TopicDeliveryPriority.DEFAULT]                                     | Optional                                                                  | Optional                                     | Optional                                         
    | [PUBLISH_VALUES_ONLY][diffusion.features.topics.details.topic_specification.TopicSpecification.PUBLISH_VALUES_ONLY]                       | `False`                                                                                                                                                  | Optional                                                                  | —                                            | Optional                                         
    | [REMOVAL][diffusion.features.topics.details.topic_specification.TopicSpecification.REMOVAL]                                               | Optional                                                                                                                                                 | Optional                                                                  | Optional                                     | Optional                                         
    | [SCHEMA][diffusion.features.topics.details.topic_specification.TopicSpecification.SCHEMA]                                                 | —                                                                                                                                                        | —                                                                         | Optional                                     | —                                                
    | [TIDY_ON_UNSUBSCRIBE][diffusion.features.topics.details.topic_specification.TopicSpecification.TIDY_ON_UNSUBSCRIBE]                       | `False`                                                                                                                                                  | Optional                                                                  | Optional                                     | Optional                                         
    | [TIME_SERIES_EVENT_VALUE_TYPE][diffusion.datatypes.timeseries.TopicSpecification.TIME_SERIES_EVENT_VALUE_TYPE]                            | —                                                                                                                                                        | —                                                                         | —                                            | Required                                         
    | [TIME_SERIES_RETAINED_RANGE][diffusion.datatypes.timeseries.TopicSpecification.TIME_SERIES_RETAINED_RANGE]                                | `limit 10`                                                                                                                                               | —                                                                         | —                                            | —                                                
    | [TIME_SERIES_SUBSCRIPTION_RANGE][diffusion.datatypes.timeseries.TopicSpecification.TIME_SERIES_SUBSCRIPTION_RANGE]                        | [TIME_SERIES_SUBSCRIPTION_RANGE][diffusion.datatypes.timeseries.TopicSpecification.TIME_SERIES_SUBSCRIPTION_RANGE] As documented                         |                                                                           |                                              |                                                  
    | [VALIDATE_VALUES][diffusion.features.topics.details.topic_specification.TopicSpecification.VALIDATE_VALUES]                               | `False`                                                                                                                                                  | Optional                                                                  | Optional                                     | Optional                                         

    †
    [TIME_SERIES][diffusion.datatypes.TIME_SERIES] topics have restricted values for the
    [CONFLATION][diffusion.features.topics.details.topic_specification.TopicSpecification.CONFLATION] property.
    They are only allowed to have the values
    [OFF][diffusion.features.topics.details.topic_specification.ConflationPolicy.OFF] or
    [UNSUBSCRIBE][diffusion.features.topics.details.topic_specification.ConflationPolicy.UNSUBSCRIBE].
    """  # noqa: E501, W291

    _tp: typing.ClassVar[type]

    @property
    def topic_type(self) -> typing.Type[T]:
        """
        The topic datatype.

        Returns:
            The topic datatype.
        """
        return typing.cast(typing.Type[T], self._tp)

    @classmethod
    def new_topic_specification(
            cls, tp: typing.Type[T_other]
    ) -> typing.Type[TopicSpecification[T_other]]:
        """
        Return a TopicSpecification class with datatype `tp`,
        ready for instantiation.

        This is for internal use - to get a TopicSpecification for
        a given DataType you should use its
        [with_properties]
        [diffusion.datatypes.foundation.abstract.AbstractDataType.with_properties] member,
        which will return an appropriate TopicSpecification type ready for instantiation
        with the relevant parameters.

        Args:
            tp: the datatype
        Returns:
            A new TopicSpecification with the given type
        """
        assert isinstance(tp, Hashable)
        return typing.cast(
            typing.Type[TopicSpecification[T_other]],
            cls._spec_class(cls, tp))

    with_properties: typing.ClassVar[
        WithProperties
    ] = WithProperties()
    """
    Class property providing a TopicSpecification subtype ready for instantiation.
    """

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def _spec_class(
        cls, tp: typing.Type[T_other]
    ) -> typing.Type[TopicSpecification[T_other]]:
        from diffusion.datatypes.conversion.default import DEFAULT_CONVERTER
        return typing.cast(
            typing.Type[TopicSpecification[T_other]],
            type(
                f"{tp.__name__}TopicSpecification",
                (cls,),
                {"_tp": DEFAULT_CONVERTER(tp)},
            ),
        )

    PUBLISH_VALUES_ONLY: typing.Optional[bool] = None
    """
    Key of the topic property that specifies whether a topic should publish
    only values.

    By default, a topic that supports delta streams will publish the
    difference between two values (a delta) when doing so is more efficient
    than publishing the complete new value. Subscribing sessions can use a
    [ValueStream value stream][diffusion.features.topics.streams.ValueStreamHandler]
    to automatically apply the delta to a
    local copy of the topic value to calculate the new value.

    Setting
    [PUBLISH_VALUES_ONLY]
    [diffusion.features.topics.details.topic_specification.TopicSpecification.PUBLISH_VALUES_ONLY]
    to `True` disables this
    behavior so that deltas are never published. Doing so is usually not
    recommended because it will result in more data being transmitted, less
    efficient use of network resources, and increased transmission latency.
    On the other hand, calculating deltas can require significant CPU from
    the server or, if update streams are used, from the updating client. The
    CPU cost will be higher if there are many differences between successive
    values, in which case delta streams confer fewer benefits. If successive
    values are unrelated to each other, consider setting
    [PUBLISH_VALUES_ONLY]
    [diffusion.features.topics.details.topic_specification.TopicSpecification.PUBLISH_VALUES_ONLY]
    to `True`.
    Also consider setting
    [PUBLISH_VALUES_ONLY]
    [diffusion.features.topics.details.topic_specification.TopicSpecification.PUBLISH_VALUES_ONLY]
    to `True`
    if the network capacity is
    high and the bandwidth savings of deltas are not required.

    See also:
    [DONT_RETAIN_VALUE][diffusion.features.topics.details.topic_specification.TopicSpecification.DONT_RETAIN_VALUE]
    """
    VALIDATE_VALUES: typing.Optional[bool] = None
    """
    Key of the topic property indicating whether a topic should validate
    inbound values.

    By default, the server does not validate received values before sending
    them on to client sessions. Invalid or corrupt values will be stored in
    the topic and passed on to sessions. If this property is set to `True`,
    the server will perform additional validation on values to check that
    they are valid instances of the data type, and if it is not then it will
    return an error to the updater and not update the topic.

    If this value is not set (or set to something other than `True`), no
    server validation of inbound values is performed. This is the recommended
    setting as there is a performance overhead to validation and a session
    using Topic Update cannot send invalid values anyway.
    """
    TIDY_ON_UNSUBSCRIBE: typing.Optional[bool] = None

    """
    Key of the topic property that specifies the 'tidy on unsubscribe' option
    for a topic.

    By default, if a session unsubscribes from a topic, it will receive any
    updates for that topic that were previously queued but not sent.

    If this property is set to "True", when a session unsubscribes from the
    topic, any updates for the topic that are still queued for the session
    are removed. There is a performance overhead to using this option as the
    client queue must be scanned to find topic updates to remove, however it
    may prove useful for preventing unwanted data being sent to sessions.

    Since 6.8.3
    """

    SCHEMA: typing.Optional[str] = None
    """
    Key of the topic property that specifies a schema which constrains topic
    values.

    This property is only used by [RECORD_V2][diffusion.datatypes.RECORD_V2]
    topics.

    Since 6.8.3
    """
    DONT_RETAIN_VALUE: typing.Optional[bool] = None

    """
    Key of the topic property that specifies a topic should not retain its
    last value.

    By default, a topic will retain its
    latest value. The latest value will be sent to new subscribers. Setting
    this property to `True` disables this behavior. New subscribers
    will not be sent an initial value. No value will be returned for fetch
    operations that select the topic. This is useful for data streams where
    the values are only transiently valid.

    Setting
    [DONT_RETAIN_VALUE][diffusion.features.topics.details.topic_specification.TopicSpecification.DONT_RETAIN_VALUE] to
    `True` also disables delta
    streams, regardless of the
    [PUBLISH_VALUES_ONLY]
    [diffusion.features.topics.details.topic_specification.TopicSpecification.PUBLISH_VALUES_ONLY] value. If
    subsequent values are likely to be related, delta streams usually provide
    performance benefits (see
    [PUBLISH_VALUES_ONLY]
    [diffusion.features.topics.details.topic_specification.TopicSpecification.PUBLISH_VALUES_ONLY]). Consider leaving
    [DONT_RETAIN_VALUE][diffusion.features.topics.details.topic_specification.TopicSpecification.DONT_RETAIN_VALUE]
    set to `False` to benefit from delta streams, even if there is no other requirement to retain the last value.

    Bearing in mind the performance trade-offs of disabling delta streams,
    there are two reasons to consider setting
    [DONT_RETAIN_VALUE][diffusion.features.topics.details.topic_specification.TopicSpecification.DONT_RETAIN_VALUE] to
    `True`. First, it stops the server and each subscribed client from
    keeping a copy of the value, reducing their memory requirements. Second,
    when a topic has a high update rate and is replicated across a cluster,
    it can significantly improve throughput because the values need not be
    persisted to the cluster.

    Time series topics ignore this property and always retain the latest
    value.

    Since 6.8.3
    """  # NOQA: E501
    PERSISTENT: typing.Optional[bool] = None

    """
    Key of the topic property that can be used to prevent a topic from being
    persisted when the server is configured to enable persistence.
    <P>
    By default, a topic will be persisted if persistence is enabled at the
    server and the topic type supports persistence.
    Setting PERSISTENT to `false` will prevent the topic from being
    persisted.

    Since 6.8.3
    """
    REMOVAL: typing.Optional[str] = None
    """
    Key of the topic property that specifies a removal policy for automatic
    removal of the topic (and/or other topics).
    This property is specified as an expression which defines one or more
    conditions that are to be satisfied before automatic removal occurs.
    The expression takes the form:
    <code>
    when <i>conditions</i> [remove "<i>selector</i>"]
    </code>
    At least one condition must be supplied. If more than one is supplied,
    they must be separated by logical operators (`and` or `or`).
    The natural evaluation order of the operators may be changed by
    surrounding with parentheses (e.g. (<i>condition</i> `and`
    <i>condition</i>)).
    The `remove` clause is optional. It provides a
    [Topic Selector][diffusion.features.topics.selectors.Selector] expression representing the topics to be removed.
    If a `remove` clause is specified, the topic with the removal
    policy will only be removed if its path matches the selector expression.
    The selector must be surrounded by either double or single quotes.
    When many topics have the same removal policy, it is better to
    set the
    [REMOVAL]
    [diffusion.features.topics.details.topic_specification.TopicSpecification.REMOVAL]
    property for one of them, using a `remove`
    clause that selects all of the topics. This is more efficient because it
    allows the server to avoid evaluating the same condition many times.

    The permissions that are applied at the time of removal are those defined
    by the roles of the principal that created the topic at the time of
    creation. The roles of that principal may therefore change before the
    removal with no effect, but if the permissions given to the roles change
    it may have an effect upon the final removal.
    Only one occurrence of each of the following condition types may be
    included within the expression:
    <table>
    <tr>
    <th style="text-align:left;">Condition&nbsp;Type</th>
    <th style="text-align:left;">Format</th>
    <th style="text-align:left;">Usage</th>
    </tr>
    <tr style="vertical-align:top">
    <th style="text-align:left;"><b>time&nbsp;after</b></th>
    <td><code>time&nbsp;after&nbsp;<i>absoluteTime</i></code></td>
    <td>Removal should occur after a specified absolute time. Absolute time
    may be specified as a number of milliseconds since the epoch (00:00:00 on
    1 January 1970) <b>or</b> as a quoted date and time formatted in <a href=
    "https://docs.oracle.com/javase/8/docs/api/java/time/format/DateTimeFormatter.html#RFC_1123_DATE_TIME">RFC_1123
    date time format</a>. Either single or double quotes may be used.</td>
    </tr>
    <tr style="vertical-align:top">
    <th style=
    "text-align:left;"><b>subscriptions&nbsp;less&nbsp;than</b></th>
    <td><code>
    [local]&nbsp;subscriptions&nbsp;&lt;&nbsp;<i>n</i>&nbsp;for&nbsp;
    <i>forPeriod</i>&nbsp;[after&nbsp;<i>afterPeriod</i>]
    </code></td>
    <td>Removal should occur when the topic has had less than the specified
    number (<i>n</i>) of subscriptions for a given period (<i>forPeriod</i>)
    of time. Optionally, an initial period (<i>afterPeriod</i>) may be
    specified by which to delay the initial checking of this condition. See
    below for period formats.
    The optional <code>local</code> keyword restricts evaluation to only count
    subscriptions from sessions belonging to the local server or cluster,
    ignoring subscriptions from sessions belonging to downstream remote servers that
    host fanout replicas of the topic.</td>
    </tr>
    <tr style="vertical-align:top">
    <th style="text-align:left;"><b>no&nbsp;updates&nbsp;for</b></th>
    <td><code>no&nbsp;updates&nbsp;for&nbsp;<i>forPeriod</i>&nbsp;[after&nbsp;<i>afterPeriod</i>]</code></td>
    <td>Removal should occur when the topic has had no updates for a given
    period (<i>forPeriod</i>) of time. Optionally, an initial period
    (<i>afterPeriod</i>) may be specified by which to delay the initial
    checking of this condition. See below for period formats.</td>
    </tr>
    </table>
    Multiple occurrences of the following condition types may be included
    within the expression:

    | Condition&nbsp;Type           | Format                                                                                                                                                           | Usage                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
    |-------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | no&nbsp;session&nbsp;has      | no&nbsp;[local]&nbsp;session&nbsp;has&nbsp;"criteria"&nbsp;[for&nbsp;forPeriod]&nbsp;[after&nbsp;afterPeriod]                                                    | Removal should occur when there are no sessions satisfying certain criteria. Optionally the criteria can be required to be satisfied for a period of time (forPeriod). Optionally, an initial period (afterPeriod) can be specified to delay the initial check of the criteria. Session selection criteria are specified as defined in [session filters][diffusion.session.Session] and must be surrounded by single or double quotes. See below for period formats. The optional local keyword restricts evaluation to sessions belonging to the local server or cluster, ignoring sessions belonging to downstream remote servers that host fanout replicas of the topic. |
    | this&nbsp;session&nbsp;closes | This is a shorthand form of `no local session has` that may be used to indicate that the topic is to be removed when the session that created it closes. |

    Time periods are specified as a number followed (with no intermediate
    space) by a single letter representing the time unit. The time unit may
    be `s` (seconds), `m` (minutes), `h` (hours) or
    `d` (days). For example, 10 minutes would be specified as `10m`.
    If quotes or backslashes `\\` are required within quoted values
    such as selectors or session criteria then they may be escaped by
    preceding with `\\`.
    The expression is validated only by the server and therefore if
    an invalid expression is specified it will be reported as an
    [InvalidTopicSpecificationError][diffusion.session.exceptions.InvalidTopicSpecificationError].

    ** Examples: **
    ```
    when time after 1518780068112
    ```
    The topic will be removed when the date and time indicated by the
    specified number of milliseconds since the epoch has passed.
    ```
    when time after "Tue, 3 Jun 2018 11:05:30 GMT"
    ```
    The topic will be removed when the specified date and time has passed.
    ```
    when time after "Tue, 3 Jun 2018 11:05:30 GMT" remove "*alpha/beta//"
    ```
    The topic alpha/beta and all topics subordinate to it will be removed
    when the specified date and time has passed.

    ```
    when subscriptions < 1 for 20m
    ```

    The topic will be removed when it has had no subscriptions for a
    continuous period of 20 minutes.

    ```
    when subscriptions < 2 for 20m after 1h
    ```

    The topic will be removed when it has had less than 2 subscriptions for a
    continuous period of 20 minutes after one hour has passed since its
    creation.

    ```
    when no updates for 3h
    ```

    The topic will be removed when it has had no updates for a continuous
    period of 3 hours.

    ```
    when no updates for 15m after 1d
    ```

    The topic will be removed when it has had no updates for a continuous
    period of 15 minutes after one day has passed since its creation.
    ```
    when this session closes
    ```
    The topic will be removed when the session creating it closes.
    ```
    when no session has '$Principal is "Alice"'
    ```
    The topic will be removed when there are no sessions with the principal
    'Alice'.
    ```
    when no session has '$Principal is "Alice"' for 10m
    ```
    The topic will be removed when there are no sessions with the principal
    'Alice' for a continuous period of 10 minutes.
    ```
    when no session has 'Department is "Accounts"' for 30m after 2h
    ```
    The topic will be removed when there have been no sessions from the
    Accounts department for a continuous period of 30 minutes after 2 hours
    have passed since its creation.
    ```
    when time after "Tue, 3 Jun 2018 11:05:30 GMT" and subscriptions < 1 for 30m
    ```
    The topic will be removed when the specified date and time has passed and
    the topic has had no subscriptions for a continuous period of 30 minutes
    after that time.
    ```
    when time after "Tue, 3 Jun 2018 11:05:30 GMT" and subscriptions < 2 for 10m after 1h
    ```
    The topic will be removed when the specified date and time has passed and
    the topic has had less than 2 subscriptions for a continuous period of 10
    minutes after that time plus one hour.
    ```
    when time after "Tue, 3 Jun 2018 11:05:30 GMT" or subscriptions < 2 for 10m after 1h
    ```
    The topic will be removed when the specified date and time has passed or
    the topic has had less than 2 subscriptions for a continuous period of 10
    minutes after one hour from its creation.
    ```
    when time after "Tue, 3 Jun 2018 11:05:30 GMT" and (subscriptions < 2 for 10m after 1h or no updates for 20m)
    ```
    The topic will be removed when the specified date and time has passed and
    either the topic has had less than 2 subscriptions for a continuous
    period of 10 minutes after that time plus one hour or it has had no
    updates for a continuous period of 20 minutes. Note that the parentheses
    are significant here as without them the topic would be removed if it had
    had no updates for 20 minutes regardless of the time and subscriptions
    clause.

    **Notes and restrictions on use**

    The `after` time periods refer to the period since the topic was
    created or restored from persistence store after a server is restarted.
    They are designed as a 'grace' period after the topic comes into
    existence before the related condition starts to be evaluated. When not
    specified the conditions start to be evaluated as soon as the topic is
    created or restored.
    The server will evaluate conditions on a periodic basis (every few
    seconds) so the exact removal time will not be precise for low periodic
    granularity.
    The meaning of the `for` period in a `no session has`
    condition is subtly different from its use in other conditions. It does
    not guarantee that there has been no session satisfying the condition at
    some point between evaluations, only that when evaluated the given period
    of time has passed since it was last evaluated and found to have no
    matching sessions.
    Subscriptions is the number of subscriptions to a topic.
    Automatic topic removal is supported for a topic that is replicated
    across the local cluster, and for a topic with with fanout replicas on
    downstream remote servers. A `subscriptions less than` condition
    will be evaluated against the total number of subscriptions across the
    cluster and on all fanout replicas on downstream remote servers. A
    `no session has` condition will consider all sessions hosted across
    the cluster and all sessions hosted by downstream remote servers that
    have a fanout replica of the topic. The `local` keyword can be used
    to restrict evaluation to the local cluster, ignoring fanout replicas.

    Since 6.8.3
    """  # NOQA: E501
    CONFLATION: typing.Optional[ConflationPolicy] = None
    """

    The conflation policy of the topic. The policy specifies how the server manages queued topic updates.
    Conflation is applied individually to each session queue.
    Conflation is the process of merging or discarding topic updates queued
    for a session to reduce the server memory footprint and network data. The
    server will conflate sessions that have a large number of queued messages
    to meet configured queue size targets. The sessions with the largest
    queues are typically slow consumers or have been disconnected – both will
    benefit from conflation. This property allows conflation behavior to be
    tuned on a topic-by-topic basis.

    The supported policies are:

    - [OFF][diffusion.features.topics.details.topic_specification.ConflationPolicy.OFF]
    - [CONFLATE][diffusion.features.topics.details.topic_specification.ConflationPolicy.CONFLATE]
    - [UNSUBSCRIBE][diffusion.features.topics.details.topic_specification.ConflationPolicy.UNSUBSCRIBE]
    - [ALWAYS][diffusion.features.topics.details.topic_specification.ConflationPolicy.ALWAYS]

    The default policy used when the property is not specified and the
    topic type is not time series is
    [CONFLATE][diffusion.features.topics.details.topic_specification.ConflationPolicy.CONFLATE].
    The default policy
    used when the property is not specified and the topic type is time
    series is [OFF][diffusion.features.topics.details.topic_specification.ConflationPolicy.OFF].

    See [ConflationPolicy][diffusion.features.topics.details.topic_specification.ConflationPolicy] for more.

    The [CONFLATE][diffusion.features.topics.details.topic_specification.ConflationPolicy.CONFLATE] and
    [UNSUBSCRIBE][diffusion.features.topics.details.topic_specification.ConflationPolicy.UNSUBSCRIBE]
    policies are applied when
    the server detects back pressure for a session. The server configuration
    places limits on the data queued for each session. If these limits are
    breached, the server will conflate the session queue to attempt to reducee
    its size. If the session queue still exceeds the limits after conflation,
    the session will be terminated.
    Conflation can be
    disabled on a session-by-session basis.
    If conflation is disabled for a
    session the policy will not be applied to topic updates queued for the
    session but will be for other sessions that have conflation enabled.
    The policies [CONFLATE][diffusion.features.topics.details.topic_specification.ConflationPolicy.CONFLATE] and
    [ALWAYS][diffusion.features.topics.details.topic_specification.ConflationPolicy.ALWAYS] are not supported for
    time series topics as they would cause missing events. Attempts to enable
    these policies with time series topics will cause the creation of the
    topic to fail, reporting that the specification is invalid.

    Since 6.8.3
    """  # NOQA: E501

    OWNER: typing.Optional[str] = None
    """
    Key of the topic property that allows the creator of a topic to extend
    READ_TOPIC, MODIFY_TOPIC, and UPDATE_TOPIC permissions to a specific
    principal, in addition to the permissions granted by the authorisation
    rules in the security store.
    A session that has authenticated using the principal can update and
    remove the topic, so the principal can be considered the topic owner. To
    fetch or subscribe to the topic, the principal must also be granted
    the SELECT_TOPIC permission by the security store rules.
    This may be used in the following cases:<br>
    1) A session creates a topic and makes its own principal the owner.<br>
    2) A session creates a topic and makes another principal the owner.
    The format of the property value is: <code>$Principal is <i>name</i> </code>
    where *name* is the name of the principal. Single quotes may be used
    instead of double quotes and special characters can be escaped.
    The purpose of this property is to allow a client to create topics on
    behalf of other users. This can be used in conjunction with the
    [REMOVAL][diffusion.features.topics.details.topic_specification.TopicSpecification.REMOVAL]
    property so that such topics are removed when there are
    no longer any sessions for the named principal.
    For example:

    ```pycon
    >>> import diffusion.datatypes
    >>> specification = diffusion.datatypes.JSON
    >>> specification.with_properties(OWNER="$Principal is 'myPrincipal'", REMOVAL="when no session has '$Principal is \"myPrincipal\"' for 5s")
    ```

    Since 6.8.3
    """  # NOQA: E501
    COMPRESSION: typing.Optional[typing.Union[CompressionPolicy, bool]] = None
    """
    Key of the topic property that allows the compression policy to be set
    on a per-topic basis.

    Compression reduces the bandwidth required to broadcast topic updates to
    subscribed sessions, at the cost of increased server CPU.

    Changes to a topic's value are published to each subscribed session as a
    sequence of topic messages. A topic message can carry the latest value or
    the difference between the latest value and the previous value (a delta).
    The compression policy determines if and how published topic messages
    are compressed. Topic messages are not exposed through the client API;
    the client library handles decompression and decodes deltas
    automatically, passing reconstructed values to the application.

    The compression policy for a topic is specified by setting this property
    to one of several values:

    - [OFF][diffusion.features.topics.details.topic_specification.CompressionPolicy.OFF]
    - [LOW][diffusion.features.topics.details.topic_specification.CompressionPolicy.LOW]
    - [MEDIUM][diffusion.features.topics.details.topic_specification.CompressionPolicy.MEDIUM]
    - [HIGH][diffusion.features.topics.details.topic_specification.CompressionPolicy.HIGH]

    The policies are listed in the order of increasing compression and
    increasing CPU cost.

    See Also:
        [CompressionPolicy][diffusion.features.topics.details.topic_specification.CompressionPolicy]

    Prior to version 6.4, only two values were allowed: `True`
    (equivalent to [MEDIUM]
    [diffusion.features.topics.details.topic_specification.CompressionPolicy.MEDIUM],
    and the previous default policy) and
    `False` (equivalent to [OFF]
    [diffusion.features.topics.details.topic_specification.CompressionPolicy.OFF]). These values are still
    supported.

    This property is only one factor that determines whether a topic message
    will be compressed. Other factors include:

    - Compression must be enabled in the server configuration.
    - The client library must support the server's compression scheme. In
    this release, the server supports zlib compression, and also allows
    compression to be disabled on a per-connector basis. From 6.4, all client
    libraries are capable of zlib compression. A JavaScript client may or may
    not support zlib compression, depending on whether the zlib library can
    be loaded. The zlib library is packaged separately to reduce the download
    size of the core library.

    Since 6.8.3
    """  # NOQA: E501
    PRIORITY: typing.Optional[TopicDeliveryPriority] = None
    """
    Key of the topic property that specifies the topic delivery priority.
    The supported delivery priorities are:

    - [LOW][diffusion.features.topics.details.topic_specification.TopicDeliveryPriority.LOW]
    - [DEFAULT][diffusion.features.topics.details.topic_specification.TopicDeliveryPriority.DEFAULT]
    - [HIGH][diffusion.features.topics.details.topic_specification.TopicDeliveryPriority.HIGH]

    The delivery priority affects the order of topic updates sent to a
    subscribed client session. When there are multiple topic updates for
    topics with different priorities in a session's outbound queue, updates
    for [HIGH]
    [diffusion.features.topics.details.topic_specification.TopicDeliveryPriority.HIGH]
    priority topics will be delivered first, followed by
    updates for [DEFAULT]
    [diffusion.features.topics.details.topic_specification.TopicDeliveryPriority.DEFAULT]
    priority topics, followed by updates for
    [LOW]
    [diffusion.features.topics.details.topic_specification.TopicDeliveryPriority.LOW]
    priority topics. Topic subscription and unsubscription
    notifications are also delivered according to the topic delivery
    priority.

    Using different delivery priorities is most beneficial when there is a
    large backlog of queued updates to deliver to a client session. On
    lightly loaded systems, updates typically remain in the outbound queue
    for a few milliseconds and so there is a lower chance of topic updates
    being reordered based on their priority. The backlog will be larger if
    the topic update rate is higher; the server or the client are more
    heavily loaded; the client session becomes temporarily disconnected; or
    if there is poor network connectivity between the server and the client.

    Messages from the server to the client that are not topic updates, for
    example [ping][diffusion.session.Session.ping_server] requests and responses, are queued with the
    [DEFAULT][diffusion.features.topics.details.topic_specification.TopicDeliveryPriority.DEFAULT] delivery priority.

    Since 6.8.3
    """  # NOQA: E501

    class Config(BaseConfig):
        allow_mutation = False
        frozen = True
        use_enum_values = True
        alias = "protocol14-topic-specification"

    def __eq__(self, other):
        return type(self) is type(other) and super().__eq__(other) and self._tp is other._tp

    def __hash__(self):
        return hash((self.topic_type, tuple(self.dict().items())))

    def properties_as_json(self) -> typing.Mapping[str, str]:
        return {
            k: str(v)
            for k, v in self.dict(exclude_none=True, exclude=set("_tp")).items()
        }

    def __int__(self):
        return self.topic_type.type_code

    @property
    def properties(self) -> PropertyMap:
        return PropertyMap(self.dict(exclude_none=True, exclude=set("_tp")))

    def __repr__(self):
        return f"{type(self).__name__}({self.properties})"

    def __str__(self):
        return repr(self)


PropertyMap: TypeAlias = ImmutableMapping[str, typing.Any]
