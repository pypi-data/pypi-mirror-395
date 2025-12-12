#  Copyright (c) 2021 - 2025 DiffusionData Ltd., All Rights Reserved.
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

from diffusion.features.control.metrics.collector import MetricCollector
from diffusion.features.control.metrics.session_metrics import SessionMetricCollector
from diffusion.features.control.metrics.topic_metrics import TopicMetricCollector
from diffusion.internal.components import Component
from diffusion.internal.utils import validate_member_arguments


class Metrics(Component):
    """
    This feature allows a client to configure metric collectors.

    Diffusion servers provide metrics which are made available in several ways:-

    - Java Management Extensions (JMX) MBeans.
    - Through the Diffusion Management Console.
    - endpoints for Prometheus.

    Metric collectors allow custom aggregation of metrics that are relevant to
    your application. There are no default metric collectors, only the ones that
    you create.

    There are two types of metric collector: Session Metric Collectors and Topic
    Metric Collectors.

    For full details regarding the configuration and operation of metric
    collectors see the user manual.

    # Session Metric Collectors

    These can be configured to record metric data for a subset of all sessions,
    specified with a session filter.

    The set of metrics recorded by each session metric collector is the same as
    those recorded for the whole server. For full details of session metrics, see
    the table in the user manual.

    If the session filters of two different session metric collectors select the
    same session, both will record metrics for that session. It is only valid to
    add the metrics of different session metric collectors if their session
    filters select distinct sets of sessions.

    You can optionally group the sessions within a collector by session
    properties.

    # Topic Metric Collectors

    These can be configured to record metric data for a subset of all topics,
    specified with a topic selector.

    You can optionally group the topics within a collector by topic type.

    The set of metrics recorded by each topic metric collector is the same as
    those recorded for the whole server. For full details of topic metrics, see
    the table in the user manual.

    If the topic selectors of two different topic metric collectors select the
    same topic, both will record metrics for that topic. It is only valid to add
    the metrics of different topic metric collectors if their topic selectors
    select distinct sets of topics.

    # Access control

    The following access control restrictions are applied:

    - To put (`put_session_metric_collector`) or
        remove (`remove_session_metric_collector`) a session metric collector, a
        session needs the `CONTROL_SERVER` global permission.
    - To put (`put_topic_metric_collector`) or
        remove (`remove_topic_metric_collector`)
        a topic metric collector, a session needs the `CONTROL_SERVER` global permission.
    - To list session metric collectors (`list_session_metric_collectors`)
        or topic metric collectors (`list_topic_metric_collectors`),
        a session needs the `VIEW_SERVER` global permission.

    # Accessing the feature

    This feature may be obtained from a `Session` as follows:

    ```pycon
    >>> metrics: Metrics = session.metrics

    ```
    """
    @validate_member_arguments
    async def put_session_metric_collector(self, collector: SessionMetricCollector) -> None:
        """
        Add a session metric collector, replacing any with the same name.

        Args:
            collector: the session metric collector

        Raises:
            InvalidSessionFilterError: if the metric collector
                session filter is invalid;
            ServerDisconnectedError:  if the session is
                disconnected.
        """
        from diffusion.internal.serialisers.specific.metrics import PutResponse

        return await self.services.PUT_SESSION_METRIC_COLLECTOR.invoke(
            self.session, request=collector, response_type=PutResponse
        )


    async def list_session_metric_collectors(
            self,
    ) -> typing.List[SessionMetricCollector]:
        """
        Retrieves the current session metric collectors.

        Returns:
            a list of current session metric collectors.

        Raises:
            ServerDisconnectedError: if the session is disconnected.
        """
        result = await self.services.LIST_SESSION_METRIC_COLLECTORS.invoke(self.session)
        return [SessionMetricCollector.from_tuple(x) for x in result[0] if x]

    @validate_member_arguments
    async def remove_session_metric_collector(self, name: str) -> None:
        """
        Removes any session metric collector with the given name, if it exists.

        Args:
            name: the session metric collector name

        Raises:
            ServerDisconnectedError: if the session is disconnected.
        """
        from diffusion.internal.serialisers.specific.metrics import (
            RemoveSessionMetricCollector,
        )

        service = self.services.REMOVE_SESSION_METRIC_COLLECTOR
        return await service.invoke(
            self.session, request=RemoveSessionMetricCollector(name)
        )

    @validate_member_arguments
    async def put_topic_metric_collector(
        self, collector: TopicMetricCollector
    ) -> None:
        """
        Add a topic metric collector, replacing any with the same name.

        A `TopicMetricCollector` instance can be created using
        TopicMetricCollectorBuilder.

        Args:
            collector: the topic metric collector

        Raises:
            ServerDisconnectedError: if the session is disconnected.
        """
        return await self.services.PUT_TOPIC_METRIC_COLLECTOR.invoke(
            self.session, request=collector
        )

    async def list_topic_metric_collectors(self) -> typing.List[TopicMetricCollector]:
        """
        Retrieves the current topic metric collectors.

        Returns:
              a list of current topic metric collectors.

        Raises:
            ServerDisconnectedError: if the session is
                disconnected.
        """
        from diffusion.internal.serialisers.specific.metrics import ListTopicMetricCollectors
        result = await self.services.LIST_TOPIC_METRIC_COLLECTORS.invoke(
            self.session, response_type=ListTopicMetricCollectors
        )
        return result.entries

    @validate_member_arguments
    async def remove_topic_metric_collector(self, name: str) -> None:
        """
        Removes any topic metric collector with the given name, if it exists.

        Args:
             name: the topic metric collector name

        Raises:
            ServerDisconnectedError: if the session is
                disconnected.
        """
        from diffusion.internal.serialisers.specific.metrics import (
            RemoveTopicMetricCollector,
        )
        service = self.services.REMOVE_TOPIC_METRIC_COLLECTOR
        return await service.invoke(self.session, request=RemoveTopicMetricCollector(name))
