#  Copyright (c) 2020 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

from __future__ import annotations

from enum import IntEnum


class UpdateConstraintType(IntEnum):

    UNCONSTRAINED_CONSTRAINT = 0
    CONJUNCTION_CONSTRAINT = 1
    BINARY_VALUE_CONSTRAINT = 2
    NO_VALUE_CONSTRAINT = 3
    LOCKED_CONSTRAINT = 4
    NO_TOPIC_CONSTRAINT = 5
    PARTIAL_JSON_CONSTRAINT = 6
