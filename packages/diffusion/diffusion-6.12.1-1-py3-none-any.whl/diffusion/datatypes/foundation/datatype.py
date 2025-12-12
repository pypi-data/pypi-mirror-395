#  Copyright (c) 2021 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

from __future__ import annotations
import io
import typing
import typing_extensions
from abc import abstractmethod, ABCMeta
from typing import Optional


TypeCode_Bound = typing.Literal[14, 15, 16, 17, 18, 19, 20, 21]
"""
Available Diffusion Datatype codes.
"""

TypeName_Bound = typing.Literal[
    "string",
    "int64",
    "json",
    "double",
    "binary",
    "record_v2",
    "time_series",
    "unknown",
]
"""
Available Diffusion Datatype names.
"""

TypeCode_target = typing_extensions.TypeVar(
    "TypeCode_target", bound=TypeCode_Bound, default=typing.Any
)
"""
A target [TypeCode][diffusion.datatypes.foundation.types.TypeCode].
"""

TypeName_target = typing_extensions.TypeVar(
    "TypeName_target", bound=TypeName_Bound, default=typing.Any
)
"""
A target [TypeName][diffusion.datatypes.foundation.types.TypeName]
"""


TypeCode = typing_extensions.TypeVar(
    "TypeCode", bound=TypeCode_Bound, default=typing.Any
)
"""
An instance of [TypeCode_Bound][diffusion.datatypes.foundation.types.TypeCode_Bound].
"""

TypeName = typing_extensions.TypeVar(
    "TypeName", bound=TypeName_Bound, default=typing.Any
)
"""
An instance of [TypeName_Bound][diffusion.datatypes.foundation.types.TypeName_Bound]
"""


@typing_extensions.runtime_checkable
class HasCodeAndName(typing_extensions.Protocol[TypeCode, TypeName]):
    """
    Type having a [type_code] and type_name
    """

    type_code: TypeCode
    """
    The type code
    """

    type_name: TypeName
    """
    The type name
    """


T = typing.TypeVar('T')


class DataTypeMeta(typing.Generic[TypeCode, TypeName], ABCMeta):
    def __repr__(cls) -> TypeName:
        return typing.cast(TypeName, getattr(cls, "type_name", cls.__name__))

    def __int__(cls) -> TypeCode:
        return typing.cast(TypeCode, getattr(cls, "type_code"))

    def __hash__(cls):
        return super().__hash__()

    type_code: TypeCode
    """ Globally unique numeric identifier for the data type. """
    type_name: TypeName
    """ Globally unique identifier for the data type."""


class DataType(typing.Generic[TypeCode, TypeName], metaclass=DataTypeMeta):
    """ Generic parent class for all data types implementations. """

    def __init__(self, value: typing.Any) -> None:
        """
        Initialise the datatype value

        Args:
            value: the value to initialise the datatype with
        """
        self._value = value
        self.validate()

    @property
    @abstractmethod
    def value(self):
        """ Current value of the instance. """

    @value.setter
    def value(self, value) -> None:
        raise NotImplementedError()  # pragma: no cover

    @classmethod
    def read_value(cls, stream: io.BytesIO) -> Optional['typing_extensions.Self']:
        """Read the value from a binary stream.

        Args:
            stream: Binary stream containing the serialised data.

        Returns:
            An initialised instance of the DataType.
        """
        raise NotImplementedError()  # pragma: no cover

    def validate(self) -> None:
        """Check the current value for correctness.

        Raises:
            `InvalidDataError`: If the value is invalid. By default there is no validation.
        """

    @abstractmethod
    def __eq__(self, other) -> bool:
        pass

    @abstractmethod
    def __bytes__(self) -> bytes:
        pass

    @classmethod
    def from_bytes(cls: typing.Type[T], data: bytes) -> Optional[T]:
        raise NotImplementedError()  # pragma: no cover
