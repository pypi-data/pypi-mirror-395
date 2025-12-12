#  Copyright (c) 2021 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

import diffusion.internal.pydantic_compat.v1 as pydantic

from diffusion.internal.encoded_data import Int32
from diffusion.internal.serialisers.pydantic import MarshalledModel


class MetricCollector(MarshalledModel):
    """
    The common base interface for metric collectors.
    """

    name: str = pydantic.Field(default="", min_length=1, alias="metric-collector-name")

    """
    The name of the metric collector.
    """
    exports_to_prometheus: bool = pydantic.Field(
        default=False, alias="exports-to-prometheus.boolean"
    )

    """
    Indicates whether the metric collector exports to Prometheus.
    """
    maximum_groups: int = pydantic.Field(
        ge=1, le=Int32.max_signed_int(), default=Int32.max_signed_int()
    )
