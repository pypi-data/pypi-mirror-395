#  Copyright (c) 2020 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

""" Basic encoded data types. """
from __future__ import annotations

import ctypes
import io
import typing

from .abstract import EncodingType
from .exceptions import DataReadError, DataValidationError, StreamExhausted

if typing.TYPE_CHECKING:
    from ..validation.pydantic import StrictNonNegativeInt


class Int64(EncodingType[typing.Any, int]):
    """Encodes 64-bit integers.

    Used as the generic class for smaller integer types.
    """

    width = 64

    @classmethod
    def read(cls, stream: io.BytesIO) -> Int64:
        """ Read the encoded value from a binary stream. """
        shift = 0
        value = 0
        while shift < cls.width:
            data = stream.read(1)
            if len(data):
                byte_int = data[0]
            else:
                raise StreamExhausted("Stream exhausted")
            value |= (byte_int & 0x7F) << shift
            if byte_int & 0x80 == 0:
                return cls._from_unsigned(value)
            shift += 7
        raise DataReadError(f"Malformed integer: {value}.")

    @classmethod
    def _from_unsigned(cls, value: int) -> Int64:
        """ Constructs the instance of the class from an unsigned integer value. """
        return cls(ctypes.c_int64(value).value)

    def to_bytes(self) -> bytes:
        """ Convert the value into its bytes representation. """
        b_value = b""
        value = self.value
        while True:
            if value & ~0x7F == 0:
                b_value += bytes((value & 0xFF,))
                break
            b_value += bytes(((value & 0x7F) | 0x80,))
            value = (value % (self.max_unsigned_int()+1)) >> 7  # logical right shift
        return b_value

    def validate(self) -> None:
        """Validate the value.

        Raises:
            `DataValidationError' if a value is considered invalid.
        """
        signed_max_value = self.max_signed_int()+1
        try:
            if not -signed_max_value <= self.value < signed_max_value:
                if not 0 <= self.value <= self.max_unsigned_int():
                    raise DataValidationError(
                        f"Value `{self.value}` outside of bounds. Max width: {self.width} bits."
                    )
        except TypeError:
            raise

    @classmethod
    def max_unsigned_int(cls) -> StrictNonNegativeInt:
        """
        Returns:
            The maximum unsigned integer for this type width
        """
        return (1 << cls.width)-1  # type: ignore

    @classmethod
    def max_signed_int(cls) -> StrictNonNegativeInt:
        """
        Returns:
            The maximum signed integer for this type width
        """
        return (1 << (cls.width - 1))-1   # type: ignore


class Int32(Int64):
    """ Encodes 32-bit integers. """

    width = 32

    @classmethod
    def _from_unsigned(cls, value):
        return cls(ctypes.c_int(value).value)


class Byte(Int64):
    """ Encodes 8-bit integers. """

    width = 8

    @classmethod
    def _from_unsigned(cls, value):
        return cls(ctypes.c_byte(value).value)


class Boolean(Byte):
    def __init__(self, value: bool):
        super().__init__(int(value))

    @classmethod
    def read(cls, stream: io.BytesIO) -> Boolean:
        result = super().read(stream)
        assert result.value in {0,1}
        return Boolean(bool(result.value))


class Bytes(EncodingType[typing.Any, bytes]):
    """ Encodes bytes values. """

    @classmethod
    def read(cls, stream: io.BytesIO) -> Bytes:
        """ Read the encoded value from a binary stream. """
        length = Int32.read(stream)
        return cls(stream.read(length.value))

    def to_bytes(self) -> bytes:
        """ Convert the value into its bytes representation. """
        return Int32(len(self.value)).to_bytes() + self.value

    def validate(self) -> None:
        """Validate the value.

        Raises:
            `DataValidationError` if the value is not a bytestring.
        """
        if not isinstance(self.value, bytes):
            raise DataValidationError(f"`{self.value}` is not bytes.")


class FixedBytes(Bytes):
    """ Encodes bytes values of fixed length. """

    def __init__(self, value: bytes, length: int):
        self.length = length
        if len(value) != length:
            raise ValueError(f"The value has to be {length} bytes long.")
        super().__init__(value)

    @classmethod
    def read(cls, stream: io.BytesIO, length: int = 24) -> FixedBytes:
        """ Read the encoded value from a binary stream. """
        return cls(stream.read(length), length=length)

    def to_bytes(self) -> bytes:
        """ Convert the value into its bytes representation. """
        return self.value


class String(EncodingType[typing.Any, str]):
    """ Encodes string values. """

    @classmethod
    def read(cls, stream: io.BytesIO) -> String:
        """ Read the encoded value from a binary stream. """
        b_value = Bytes.read(stream)
        return cls(b_value.value.decode())

    def to_bytes(self) -> bytes:
        """ Convert the value into its bytes representation. """
        return Bytes(self.value.encode()).to_bytes()

    def validate(self) -> None:
        """Validate the value.

        Raises:
            DataValidationError: If the value is not a string.
        """
        if not isinstance(self.value, str):
            raise DataValidationError(f"`{self.value}` is not a string.")
