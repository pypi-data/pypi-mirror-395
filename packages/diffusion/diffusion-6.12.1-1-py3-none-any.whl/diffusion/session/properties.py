#  Copyright (c) 2024 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

from __future__ import annotations

ALL_FIXED_PROPERTIES = "*F"
""" This constant can be used instead of a property key in requests for
    session property values to indicate that *all* fixed session
    properties are required.
"""

ALL_USER_PROPERTIES = "*U"
""" This constant can be used instead of a property key in requests for
    session property values to indicate that *all* user defined session
    properties are required.
"""
