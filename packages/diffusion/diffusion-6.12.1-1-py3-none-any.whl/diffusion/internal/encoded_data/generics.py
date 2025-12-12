#  Copyright (c) 2020 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

""" Encoded data types that contain multiple values. """

from __future__ import annotations

import typing

import io
from typing import TypeVar, Generic, Collection, Type, Union

from .abstract import EncodingType
from .exceptions import StreamExhausted, DataValidationError
from .scalars import String, Int32

T = TypeVar("T", bound=EncodingType)


class GenericSet(EncodingType[typing.Any, typing.Tuple[T, ...]], Generic[T]):
    """Generic set for multiple scalar values.

    Not technically a set, more of a collection.
    """

    internal: Type[T]
    value: typing.Tuple[T, ...]

    def __init__(self, value: Collection[T]):
        super().__init__(tuple(value) if value is not None else None)

    @classmethod
    def read(cls, stream: io.BytesIO) -> GenericSet:
        """ Read the values from a stream. """
        result = []
        length = Int32.read(stream).value
        if length:
            while True:
                try:
                    result.append(cls.internal.read(stream))
                except StreamExhausted:
                    break
        return cls(result)

    def to_bytes(self) -> bytes:
        """ Convert the values to bytes. """
        result = Int32(len(self.value)).to_bytes()
        result += b"".join(val.to_bytes() for val in self.value)
        return result

    def validate(self) -> None:
        """Validate all values.

        Raises:
            DataValidationError: If a value is considered invalid.
        """
        error_message = (
            f"{type(self)} requires an Collection of {self.internal.__name__} objects"
        )
        for val in self.value:
            if not isinstance(val, self.internal):
                raise DataValidationError(error_message)
            val.validate()


class StringSet(GenericSet[String]):
    """ Set of string values. """

    internal = String

    def __init__(self, value: Collection[Union[String, str]]):
        super().__init__([String(val) if isinstance(val, str) else val for val in value])
