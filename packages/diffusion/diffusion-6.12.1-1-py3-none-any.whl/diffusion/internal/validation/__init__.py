#  Copyright (c) 2022 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

import datetime
import typing

from typing_extensions import TypeAlias

from .pydantic import (
    StrictPositiveInt,
    StrictNonNegativeInt,
    StrictNonNegativeFloat,
    StrictNonNegative,
    StrictStr
)


class StrictTimedeltaClass(datetime.timedelta):
    """
    Strictly validated version of `datetime.timedelta`.
    Accepts only a `datetime.timedelta` or any subclasses thereof.
    """

    @classmethod
    def __get_validators__(cls):
        def validate(val):
            if isinstance(val, datetime.timedelta):
                return val
            raise ValueError(f"{val} is not a {cls.__base__}")

        yield validate


class StrictNonNegativeTimedeltaClass(datetime.timedelta):
    """
    Strictly validated version of `datetime.timedelta`.
    Accepts only `datetime.timedelta` or any subclasses thereof. Must be non-negative.
    """

    @classmethod
    def __get_validators__(cls):
        def validate(val):
            if isinstance(val, datetime.timedelta) and val.total_seconds() >= 0.0:
                return val
            raise ValueError(f"{val} is not a positive/zero {cls.__base__}")

        yield validate


if typing.TYPE_CHECKING:
    StrictTimedelta: TypeAlias = typing.Union[datetime.timedelta, StrictTimedeltaClass]
    """
    A `datetime.timedelta` instance.
    """
    StrictNonNegativeTimedelta: TypeAlias = typing.Union[
        datetime.timedelta, StrictNonNegativeTimedeltaClass
    ]
    """
    A non-negative `datetime.timedelta` instance.
    """
else:
    StrictTimedelta: TypeAlias = StrictTimedeltaClass
    """
    A `datetime.timedelta` instance.
    """
    StrictNonNegativeTimedelta: TypeAlias = StrictNonNegativeTimedeltaClass
    """
    A non-negative `datetime.timedelta` instance.
    """
