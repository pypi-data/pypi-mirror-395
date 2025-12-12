#  Copyright (c) 2021 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

""" Core definitions of data types. """
from __future__ import annotations

import abc
import functools
import typing
from io import BytesIO
from typing import Any

import typing_extensions

import diffusion.internal.utils

from typing_extensions import Self

from diffusion.internal.encoder import Encoder, DefaultEncoder
from diffusion.internal.encoded_data import Int64

from .datatype import DataType

if typing.TYPE_CHECKING:
    from .ibytesdatatype import IBytes
    from diffusion.features.topics.details.topic_specification import TopicSpecification

T = typing.TypeVar("T", bound=DataType, covariant=True)
A_T = typing.TypeVar("A_T", bound="AbstractDataType")
A_T_Target = typing.TypeVar("A_T_Target", bound="AbstractDataType")


TS_T = typing.TypeVar("TS_T", bound="TopicSpecification")
TS_T_target = typing.TypeVar("TS_T_target", bound="TopicSpecification")


@typing_extensions.runtime_checkable
class ValueTypeProtocol(typing.Protocol):
    """
    A Diffusion Datatype-like value.
    """

    def __init__(self, value: typing.Any) -> None: ...

    @property
    def value(self) -> typing.Any: raise NotImplementedError()  # pragma: no cover

    def to_bytes(self) -> bytes: raise NotImplementedError()  # pragma: no cover


class ValueTypeProtocolWithConverterFrom(ValueTypeProtocol):
    @classmethod
    def converter_from(
            cls: typing.Type[ValueType],
            source_type: typing.Type[ValueType_target],
    ) -> typing.Optional[Converter[ValueType_target, ValueType]]: ...


ValueType = typing_extensions.TypeVar(
    "ValueType", bound=ValueTypeProtocol, contravariant=True, default=typing.Any
)
ValueType_target = typing_extensions.TypeVar(
    "ValueType_target", bound=ValueTypeProtocol, covariant=True, default=typing.Any
)
ValueType_target_non_co = typing_extensions.TypeVar(
    "ValueType_target_non_co", bound=ValueTypeProtocol, default=typing.Any
)


ValueType_WithConverterFrom = typing.TypeVar(
    "ValueType_WithConverterFrom",
    bound=ValueTypeProtocolWithConverterFrom,
    contravariant=True,
)
ValueType_WithConverterFrom_target = typing.TypeVar(
    "ValueType_WithConverterFrom_target",
    bound=ValueTypeProtocolWithConverterFrom,
    covariant=True,
)
ValueType_WithConverterFrom_target_non_co = typing.TypeVar(
    "ValueType_WithConverterFrom_target_non_co",
    bound=ValueTypeProtocolWithConverterFrom,
)


class Converter(typing_extensions.Protocol[ValueType, ValueType_target]):
    def __call__(self, value: ValueType) -> typing.Optional[ValueType_target]:
        pass  # pragma: no cover


class Identity(object):
    def __call__(self, value: ValueType) -> typing.Optional[ValueType]:
        return value


IDENTITY = Identity()

WithProperties_T = typing.TypeVar("WithProperties_T", bound="WithProperties")
WithProperties_Value_T = typing.TypeVar("WithProperties_Value_T", bound="AbstractDataType")

class WithProperties():
    def __get__(
        self,
        instance: typing.Optional[WithProperties_Value_T],
        owner: typing.Type[WithProperties_Value_T],
    ) -> typing.Type[TopicSpecification[WithProperties_Value_T]]:
        """
        Return a TopicSpecification class prefilled with `owner`

        Args:
            instance: the instance on which this is called
            owner: the class on which this is called

        Returns:
            Return a TopicSpecification class prefilled with `owner`
        """
        from diffusion.features.topics.details.topic_specification import TopicSpecification
        return typing.cast(
            typing.Type["TopicSpecification[WithProperties_Value_T]"],
            TopicSpecification.new_topic_specification(owner),
        )


RealValue = typing_extensions.TypeVar("RealValue", default=typing.Any, covariant=True)
"""
The embodied value type of a Diffusion Datatype.
"""

RealValue_target = typing_extensions.TypeVar("RealValue_target", default=typing.Any)
"""
A target [RealValue][diffusion.datatypes.foundation.types.RealValue].
"""

RealValue_Precise = typing_extensions.TypeVar("RealValue_Precise", covariant=True)
"""
A precise [RealValue][diffusion.datatypes.foundation.types.RealValue].
"""

class AbstractDataType(DataType, typing.Generic[TS_T, ValueType, RealValue]):
    encoder: Encoder = DefaultEncoder()
    raw_types: typing.Type[RealValue]

    def __init__(self, value: RealValue) -> None:
        super().__init__(value)

    @classmethod
    def default(cls: typing.Type[A_T]) -> typing.Optional[A_T]:
        return None

    def write_value(self, stream: BytesIO) -> BytesIO:
        """Write the value into a binary stream.

        Args:
            stream: Binary stream to serialise the value into.
        """
        stream.write(self.encode(self.value))
        return stream

    @classmethod
    def codec_read_bytes(cls, stream: BytesIO) -> typing.Optional[Self]:
        length = Int64.read(stream).value
        if length == 0:
            return None
        return cls.from_bytes(stream.read(length))

    def codec_write_bytes(self, stream: BytesIO) -> BytesIO:
        payload = self.to_bytes()
        return self.codec_write_arbitrary_bytes(payload, stream)

    @classmethod
    def codec_write_arbitrary_bytes(cls, payload, stream):
        Int64(len(payload)).write(stream)
        stream.write(payload)
        return stream

    @typing.final
    def to_bytes(self) -> bytes:
        """Convert the value into the binary representation.

        Convenience method, not to be overridden"""

        return self.encode(self.value)

    @classmethod
    def read_value(cls, stream: BytesIO) -> typing.Optional[Self]:
        """Read the value from a binary stream.

        Args:
            stream: Binary stream containing the serialised data.

        Returns:
            An initialised instance of the DataType.
        """
        return cls.from_bytes(stream.read())

    @property
    def value(
        self
    ) -> RealValue:
        """Current value of the instance."""
        return self._value

    @value.setter
    def value(self, value: typing.Union[bytes, RealValue]) -> None:
        if isinstance(value, bytes):
            value = self.decode(value)
        self._value = value

    @classmethod
    def from_bytes(cls, data: bytes) -> typing.Optional[Self]:
        """Convert a binary representation into the corresponding value.

        Args:
            data: Serialised binary representation of the value.

        Returns:
            An initialised instance of the DataType.
        """
        value = cls.decode(data)
        if value is None:
            return None
        return cls(value)

    @classmethod
    @typing.final
    def maybe_from_bytes(
        cls, bytes_value: typing.Optional[bytes]
    ) -> typing.Optional[Self]:
        return cls.from_bytes(bytes_value) if bytes_value is not None else None

    @property
    def serialised_value(self) -> dict:
        """Return the sequence of values ready to be serialised.

        It is assumed that the serialisation will use the
        `serialised-value` serialiser.
        """
        return {"data-type-name": type(self).type_name, "bytes": self.encode(self.value)}

    @classmethod
    @abc.abstractmethod
    def encode(cls, value: Any) -> bytes:
        """Convert a value into the corresponding binary representation.

        Args:
            value:
                Native value to be serialised

        Returns:
            Serialised binary representation of the value.
        """

    @classmethod
    @abc.abstractmethod
    def decode(cls, data: bytes) -> RealValue:
        """Convert a binary representation into the corresponding value.

        Args:
            data: Serialised binary representation of the value.

        Returns:
            Deserialised value.
        """

    def set_from_bytes(self, data: bytes) -> None:
        """Convert bytes and set the corresponding value on the instance."""
        self.value = self.decode(data)

    def __eq__(self, other) -> bool:
        return (type(self) is type(other) and self.value == other.value) or (
            self.value == other
        )

    def __hash__(self):
        return hash(self.value)

    def __repr__(self) -> str:
        return f"<{type(self).__name__} value={self.value}>"

    def __str__(self) -> str:
        return str(self.value)

    def __bytes__(self):
        return self.to_bytes()

    @classmethod
    @functools.lru_cache(maxsize=None)
    def _get_base_type_parameters(cls) -> typing.KeysView:
        if not hasattr(cls, 'raw_types'):
            return {}.keys()
        dfp_dict = diffusion.internal.utils.get_base_type_parameters(cls.raw_types)
        return dfp_dict.keys()

    @classmethod
    def validate_raw_type(cls, source_type: type) -> bool:
        final_raw_types = cls._get_base_type_parameters()
        return issubclass(source_type, (*final_raw_types, type(None)))

    @classmethod
    def can_read_as(
        cls,
        result_type: typing.Type[AbstractDataType],
    ) -> bool:
        """
        Checks whether this data type is compatible with the given `result_type`

        This means that any valid binary representation of this data type can be read as an instance of the given
        `result_type`

        Any value type can be read as an [OBJECT][diffusion.datatypes.OBJECT].

        Args:
            result_type: The type to check for compatibility.

        Returns:
            True if the data type is compatible with the given `result_type`. Otherwise false.

        Raises:
            ValueError: The given `result_type` isn't a valid result type.

        """  # noqa: E501, W291
        effective_result_type = cls.get_effective_result_type(result_type)
        return (
            issubclass(cls, effective_result_type)
            or cls.converter_to(effective_result_type) is not None
        )

    @classmethod
    def get_effective_result_type(
        cls, result_type: typing.Type[typing.Any]
    ) -> typing.Type[ValueTypeProtocol]:
        from .object import Object

        effective_result_type = {object: Object}.get(
            result_type, result_type
        )
        return effective_result_type

    @classmethod
    @typing.final
    def is_wildcard(cls, result_type: typing.Type[AbstractDataType]) -> bool:
        from .object import Object
        from ...features.topics.fetch.fetch_common import IVoidFetch
        from .ibytesdatatype import IBytes
        return cls.get_effective_result_type(result_type) in {IBytes, Object, IVoidFetch}

    @classmethod
    @typing.final
    def converter_to(
        cls: typing.Type[ValueType],
        result_type: typing.Type[ValueType_target],
    ) -> typing.Optional[Converter[ValueType, ValueType_target]]:
        # noinspection PyProtectedMember
        return typing.cast(typing.Type[Self], cls)._converter_to_cached(
            result_type=result_type
        )

    @classmethod
    @functools.lru_cache(maxsize=None)
    @typing.final
    def _converter_to_cached(
        cls: typing.Type[ValueType],
        result_type: typing.Type[ValueType_WithConverterFrom_target],
    ) -> typing.Optional[Converter[ValueType, ValueType_WithConverterFrom_target]]:
        return typing.cast(
            Converter[ValueType, ValueType_WithConverterFrom_target],
            result_type.converter_from(
                typing.cast(
                    typing.Type[ValueType],
                    typing.cast(typing.Type[Self], cls).real_value_type(),
                )
            ),
        )

    @classmethod
    @typing.final
    def converter_from(
            cls: typing.Type[ValueType],
            source_type: typing.Type[ValueType_target],
    ) -> typing.Optional[Converter[ValueType_target, ValueType]]:
        # noinspection PyProtectedMember
        return typing.cast(typing.Type[Self], cls)._converter_from_cached(source_type)

    @classmethod
    @functools.lru_cache(maxsize=None)
    @typing.final
    def _converter_from_cached(
            cls: typing.Type[ValueType],
            source_type: typing.Type[ValueType_target],
    ) -> typing.Optional[Converter[ValueType_target, ValueType]]:
        # noinspection PyProtectedMember
        return typing.cast(typing.Type[Self], cls)._converter_from(source_type)

    @classmethod
    def _converter_from(
        cls: typing.Type[ValueType],
        source_type: typing.Type[ValueType_target],
    ) -> typing.Optional[Converter[ValueType_target, ValueType]]:
        if cls == source_type:
            return typing.cast(Converter[ValueType_target, ValueType], IDENTITY)
        return None

    with_properties: typing.ClassVar[WithProperties] = WithProperties()
    """
    A class property that returns the type of this class's appropriate TopicSpecification class,
    ready for instantiation with the relevant parameters.

    See Also:
        [WithProperties][diffusion.datatypes.foundation.abstract.WithProperties]
    """

    @classmethod
    def read_as(
        cls,
        result_type: typing.Type[A_T_Target],
        input_bytes: IBytes
    ) -> typing.Optional[A_T_Target]:

        converter = cls.converter_to(result_type)
        if not (
            converter
            and cls.can_read_as(
                typing.cast(typing.Type[AbstractDataType], result_type)
            )
        ):
            raise ValueError(f"Incompatible value of type {result_type}.")
        materialised = cls.from_bytes(input_bytes.to_bytes())
        if materialised:
            wrapped_result = typing.cast(
                typing.Optional[A_T_Target],
                converter(typing.cast(ValueType, materialised)),
            )
        else:
            return None
        return wrapped_result

    @classmethod
    def real_value_type(cls) -> typing.Type[RealValue]:
        return typing.cast(typing.Type[RealValue], cls)


