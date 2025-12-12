#  Copyright (c) 2022 - 2025 DiffusionData Ltd., All Rights Reserved.
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

from diffusion.internal.encoded_data import Int64
from diffusion.internal.utils import BaseConfig
from diffusion.internal.validation.pydantic import StrictPositiveInt


class RetryStrategy(pydantic.BaseModel):
    """
    Defines a retry strategy.

    A retry strategy will be applied when an initial to attempt to open a session
    fails with a ServerConnectionError.

    The strategy is defined in terms of the number of seconds between retries and
    the maximum number of retries to attempt.

    Since:
        6.9
    """

    @classmethod
    def no_retry(cls):
        return cls.construct(interval=0, attempts=0)

    """
    The retry strategy that indicates that no retry is to be attempted.
    """

    interval: float = pydantic.Field(ge=1.0)
    """
    the number of seconds before the first retry and between subsequent retries
    """
    attempts: pydantic.StrictInt = Int64.max_unsigned_int()
    """
    The number of retry attempts
    """

    # noinspection PyUnusedLocal,PyNestedDecorators
    @pydantic.validator("attempts")
    @classmethod
    @pydantic.validate_arguments
    def validate_attempts(
            cls,
            attempts: StrictPositiveInt,
            values: typing.Dict[str, typing.Any],
            field,
            config,
    ) -> StrictPositiveInt:
        return attempts

    def __str__(self):
        if self.attempts == 0:
            return "RetryStrategy [No retry]"
        elif self.attempts == Int64.max_unsigned_int():
            return f"RetryStrategy [interval={self.interval}, attempts=unlimited]"
        else:
            return f"RetryStrategy [interval={self.interval}, attempts={self.attempts}]"

    class Config(BaseConfig):
        pass
