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
from typing_extensions import TypeAlias

from diffusion.internal import encoded_data


class StrictPositiveIntClass(pydantic.StrictInt):
    """
    Strictly validated version of `int`.
    Accepts only `int` or any subclasses thereof. Must be positive.
    """
    ge = 1


class StrictNonNegativeIntClass(pydantic.StrictInt):
    """
    Strictly validated version of `int`.
    Accepts only `int` or any subclasses thereof. Must be non-negative.
    """
    ge = 0


class StrictNonNegativeFloatClass(pydantic.StrictFloat):
    """
    Strictly validated version of `float`.
    Accepts only `int` or any subclasses thereof. Must be non-negative.
    """
    ge = 0.0


if typing.TYPE_CHECKING:
    StrictPositiveInt = typing.Union[StrictPositiveIntClass, pydantic.StrictInt]
    """
    A positive `int`
    """
    StrictNonNegativeInt = typing.Union[StrictNonNegativeIntClass, pydantic.StrictInt, int]
    """
    A non-negative `int`
    """
    StrictNonNegativeFloat = typing.Union[StrictNonNegativeFloatClass, pydantic.StrictFloat]
    """
    A non-negative float
    """
    StrictStr = typing.Union[str, pydantic.StrictStr]
    """
    A string
    """
    StrictInt = typing.Union[int, pydantic.StrictInt]
    """
    An `int``
    """
else:
    StrictPositiveInt: TypeAlias = StrictPositiveIntClass
    """
    A positive `int`
    """
    StrictNonNegativeInt: TypeAlias = StrictNonNegativeIntClass
    """
    A non-negative `int`
    """
    StrictNonNegativeFloat: TypeAlias = StrictNonNegativeFloatClass
    """
    A non-negative float
    """
    StrictStr: TypeAlias = pydantic.StrictStr
    """
    A string
    """
    StrictInt: TypeAlias = pydantic.StrictInt
    """
    An `int``
    """

StrictNonNegative = typing.Union[StrictNonNegativeInt, StrictNonNegativeFloat]
"""
A non-negative `int` or `float`
"""

STRICT_INT_T = typing.TypeVar("STRICT_INT_T", bound="MinMaxStrictInt")


class Int32(encoded_data.Int32):
    @classmethod
    def max_unsigned_int(cls) -> StrictNonNegativeInt:
        """
        Returns:
            The maximum unsigned integer for this type width
        """
        return super().max_unsigned_int()


    @classmethod
    def max_signed_int(cls) -> StrictNonNegativeInt:
        """
        Returns:
            The maximum signed integer for this type width
        """
        return super().max_signed_int()


class Int64(encoded_data.Int64):
    @classmethod
    def max_unsigned_int(cls) -> StrictNonNegativeInt:
        """
        Returns:
            The maximum unsigned integer for this type width
        """
        return super().max_unsigned_int()


    @classmethod
    def max_signed_int(cls) -> StrictNonNegativeInt:
        """
        Returns:
            The maximum signed integer for this type width
        """
        return super().max_signed_int()


class MinMaxStrictInt(pydantic.StrictInt):
    """
    A constrained integer
    """
    ge: typing.Optional[int] = None
    le: typing.Optional[int] = None

    @classmethod
    def max(cls: typing.Type[STRICT_INT_T]) -> STRICT_INT_T:
        """
        Maximum value of this type
        """
        return cls(typing.cast(int, cls.le))

    @classmethod
    def min(cls: typing.Type[STRICT_INT_T]) -> STRICT_INT_T:
        """
        Minimum value of this type
        """
        return cls(typing.cast(int, cls.ge))


class UnsignedInt32(MinMaxStrictInt):
    """
    An unsigned 32 bit integer
    """

    ge = 0
    le = Int32.max_unsigned_int()

class SignedInt32(MinMaxStrictInt):
    """
    A signed 32 bit integer
    """

    ge = -Int32.max_signed_int()
    le = Int32.max_signed_int()


class NonNegativeSignedInt32(MinMaxStrictInt):
    """
    An non-negative signed 32 bit integer
    """

    ge = 0
    le = Int32.max_signed_int()


class UnsignedInt64(MinMaxStrictInt):
    """
    An unsigned 64 bit integer
    """

    ge = 0
    le = Int64.max_unsigned_int()


class SignedInt64(MinMaxStrictInt):
    """
    A signed 64 bit integer
    """

    ge = -Int64.max_signed_int()
    le = Int64.max_signed_int()


class NonNegativeSignedInt64(MinMaxStrictInt):
    """
    A non-negative signed 64 bit integer
    """

    ge = 0
    le = Int64.max_signed_int()


MaximumResultSize: TypeAlias = UnsignedInt32
"""
The maximum result size
"""
