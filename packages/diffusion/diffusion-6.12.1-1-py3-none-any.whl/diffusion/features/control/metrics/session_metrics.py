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

from diffusion.features.control.metrics.collector import MetricCollector
from diffusion.internal.utils import BuilderBase, validate_member_arguments


class SessionMetricCollector(MetricCollector):
    """
    The definition of a session metric collector.

    These can be configured to record metric data for a subset of all
    sessions, specified with a session filter.
    """

    removes_metrics_with_no_matches: typing.Optional[bool] = pydantic.Field(
        default=False, alias="removes-metrics-with-no-matches.boolean"
    )
    """
    `True` if metrics with no matches should be removed.
    """

    session_filter: typing.Optional[pydantic.StrictStr] = None
    """
    Session filter.
    """

    group_by_properties: typing.List[pydantic.StrictStr] = pydantic.Field(
        default=[], alias="session-property-keys"
    )
    """
    List of properties to group by.
    """
    class Config(MetricCollector.Config):
        alias = "session-metric-collector"


class SessionMetricCollectorBuilder(BuilderBase[SessionMetricCollector]):
    """
    A session metric collector builder.

    It is used to create instances of
    `SessionMetricCollector` that can be supplied to
    `Metrics.put_session_metric_collector`.
    """
    Self = typing.TypeVar("Self", bound=BuilderBase[SessionMetricCollector])

    @validate_member_arguments
    def export_to_prometheus(self: Self, export: bool) -> Self:
        """
        Specifies whether the metric collector should export metrics to
        Prometheus or not.

        The default is that metrics are not exported to Prometheus.

        Args:
            export: True to export metrics to Prometheus

        Returns:
            this builder
        """
        self._target.exports_to_prometheus = export
        return self

    @validate_member_arguments
    def group_by_property(self: Self, property_name: str) -> Self:
        """
        Adds the name of a session property to group by to the list known
        to this builder.

        By default a builder will initially have no session properties to
        group by set.

        Args:
            property_name: the name of the session property. See
                `Session` for details of session properties

        Returns:
            this builder
        """
        self._target.group_by_properties += [property_name]
        return self

    @validate_member_arguments
    def group_by_properties(self: Self, *property_names: str) -> Self:
        """
        Specifies a list of session property names to group by, replacing
        any current list known to this builder.

        Args:
            *property_names: a list of session property names. See
                `Session` for details of session properties

        Returns:
            this builder
        """
        self._target.group_by_properties = list(property_names)
        return self

    @validate_member_arguments
    def remove_metrics_with_no_matches(self: Self, remove: bool) -> Self:
        """
        Specifies whether the metric collector should remove any metrics
        that have no matches.

        The default is that the metric collector will not remove metrics
        with no matches.

        Args:
            remove: True to indicate that metrics with no matches
                should be removed

        Returns:
            this builder
        """
        self._target.removes_metrics_with_no_matches = remove
        return self

    @validate_member_arguments
    def maximum_groups(self, limit: pydantic.PositiveInt):
        self._target.maximum_groups = limit
        return self

    @validate_member_arguments
    def create(self, name: str, session_filter: str) -> SessionMetricCollector:
        """
        Create a new
        [SessionMetricCollector][diffusion.features.control.metrics.session_metrics.SessionMetricCollector]
        using the values currently known to this builder.

        Args:
            name: the name of the
                [SessionMetricCollector][diffusion.features.control.metrics.session_metrics.SessionMetricCollector]

            session_filter: the session filter indicating the sessions
                this collector should apply to. The format of a session
                property filter is documented in [Session][diffusion.session.Session]

        Returns:
            a new
                [SessionMetricCollector][diffusion.features.control.metrics.session_metrics.SessionMetricCollector]
                with all of the current settings of this builder
        """
        return super()._create(name=name, session_filter=session_filter)

    def reset(self) -> 'SessionMetricCollectorBuilder':
        return super(SessionMetricCollectorBuilder, self).reset()
