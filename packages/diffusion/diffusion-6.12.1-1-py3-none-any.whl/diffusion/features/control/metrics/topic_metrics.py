#  Copyright (c) 2021 - 2024 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

import typing

import diffusion.internal.pydantic_compat.v1 as pydantic

from diffusion.features.control.metrics import MetricCollector
from diffusion.internal.utils import BuilderBase, validate_member_arguments


class TopicMetricCollector(MetricCollector):
    """
    The definition of a topic metric collector.

    These can be configured to record metric data for a subset of all topics,
    specified with a topic selector.
    """

    topic_selector: typing.Optional[pydantic.StrictStr] = None

    groups_by_topic_type: bool = pydantic.Field(
        default=False, alias="groups-by-topic-type.boolean"
    )
    """
    Indicates whether the collector groups by topic type.
    (True if grouping by topic type)
    """

    groups_by_topic_view: typing.Optional[bool] = pydantic.Field(
        default=False, alias="groups-by-topic-view.boolean"
    )
    """
    Indicates whether the collector groups by topic view.
    """

    group_by_path_prefix_parts: pydantic.NonNegativeInt = 0
    """
    The number of leading parts of the topic path to group by.
    """

    class Config(MetricCollector.Config):
        frozen = True
        alias = "protocol25-topic-metric-collector"


class TopicMetricCollectorBuilder(BuilderBase[TopicMetricCollector]):
    """
    A topic metric collector builder.

    This creates instances of `TopicMetricCollector` that can be supplied to
    Metrics.put_topic_metric_collector.
    """

    Self = typing.TypeVar("Self", bound=BuilderBase[TopicMetricCollector])

    @validate_member_arguments
    def group_by_topic_type(self: Self, group_by_topic_type: bool) -> Self:
        """
        Specifies whether the metric collector should group by topic
        type.

        By default a topic metric collector does not group by topic type.

        Args:
            group_by_topic_type:
                True to indicate that the collector
                should group by topic type

        Returns:
            this builder
        """
        self._target = self._target.copy(
            update=dict(groups_by_topic_type=group_by_topic_type)
        )
        return self

    @validate_member_arguments
    def group_by_path_prefix_parts(self: Self, parts: pydantic.NonNegativeInt) -> Self:
        """
        Specifies the number of leading parts of the topic path the
        metric collector should use to group results.
        Since 6.8.

        By default a topic metric collector does not group by the topic
        path prefix. If a positive number of parts is specified, it
        will enable grouping.

        Args:
            parts:
                The number of leading parts of the topic path to group by.
                Set to 0 to disable grouping by path.

        Returns:
            this builder
        """
        self._target = self._target.copy(update=dict(group_by_path_prefix_parts=parts))
        return self

    def group_by_topic_view(self, group_by_topic_view: bool) -> "TopicMetricCollectorBuilder":
        """
        Specifies whether the metric collector should group by topic view.

        By default a topic metric collector does not group by topic view.

        Args:
            group_by_topic_view:
                `True` to indicate that the collector should group by topic view.

        Returns:
            This builder

        Since:
            6.10
        """
        self._target = self._target.copy(
            update=dict(groups_by_topic_view=group_by_topic_view)
        )
        return self

    @validate_member_arguments
    def export_to_prometheus(self: Self, export: bool) -> Self:
        """
        Specifies whether the metric collector should export metrics to
        Prometheus or not.

        The default is that metrics are not exported to Prometheus.

        Args:
            export:
                True to export metrics to Prometheus

        Returns:
            this builder
        """
        self._target = self._target.copy(update=dict(exports_to_prometheus=export))
        return self

    @validate_member_arguments
    def maximum_groups(self: Self, limit: pydantic.PositiveInt) -> Self:
        """
        Specify the maximum number of groups maintained by the metric collector.

        By default, the number of groups is not limited.

        Args:
            limit:
                The maximum number of groups maintained by the metric collector.

        Returns:
            this builder
        """
        self._target = self._target.copy(update=dict(maximum_groups=limit))
        return self

    def reset(self) -> "TopicMetricCollectorBuilder":
        """
        Reset the builder.

        Returns:
            this Builder
        """
        return super().reset()

    @validate_member_arguments
    def _create_delegate(
        self, name: pydantic.StrictStr, topic_selector: pydantic.StrictStr
    ) -> TopicMetricCollector:
        return super()._create(name=name, topic_selector=topic_selector)

    def create(self, name: str, topic_selector: str) -> TopicMetricCollector:
        """
        Create a new `TopicMetricCollector` using the values
        currently known to this builder.

        Args:
            name:
                the name of the TopicMetricCollector

            topic_selector:
                the selector pattern that specifies the
                topics for which metrics are to be collected

        Returns:
            a new TopicMetricCollector with all of the
                current settings of this builder
        """
        return self._create_delegate(name, topic_selector)
