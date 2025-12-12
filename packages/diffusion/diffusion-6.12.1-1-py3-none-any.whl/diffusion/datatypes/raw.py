#  Copyright (c) 2024 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

import typing

RawDataTypes = typing.Union[float, int, str, bytes]
"""
Raw data types that are used to populate Diffusion datatypes
"""

RawDataTypes_T = typing.TypeVar("RawDataTypes_T", bound=RawDataTypes)
