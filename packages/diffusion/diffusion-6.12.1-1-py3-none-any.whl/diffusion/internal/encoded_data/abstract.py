#  Copyright (c) 2020 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

""" Abstract definition for encoded data. """

from __future__ import annotations

import typing_extensions

import inspect
import io
import typing
from abc import ABCMeta, abstractmethod
from typing import Any, Type, TypeVar, Union

from typing_extensions import Protocol, runtime_checkable

from diffusion.internal.hashable_dict import StrictHashable

if typing.TYPE_CHECKING:
    from diffusion.internal.serialisers import Serialiser, Resolver


SpecType = typing.TypeVar("SpecType", contravariant=True)
SpecType_co  = typing.TypeVar("SpecType_co", covariant=True)

EncodingProtocolVar = typing.TypeVar("EncodingProtocolVar", bound="EncodingProtocol")

@runtime_checkable
class EncodingProtocol(Protocol[SpecType]):
    """General protocol for encoded data.

    Must be implemented for all classes which can be used to serialise
    and deserialise the data over the wire, even if they don't extend
    `EncodingType` directly. In other words, it allows for duck-typing
    serialisation/deserialisation.
    """

    def __hash__(self) -> int:
        raise NotImplementedError()

    @classmethod
    def read(cls, stream: io.BytesIO) -> typing_extensions.Self:
        """Read the encoded value from a binary stream.

        It converts the read value to the correct type and constructs a new
        instance of the encoding type.
        """
        raise NotImplementedError()

    def write(self, stream: io.BytesIO) -> io.BytesIO:
        """ Write the bytes representation of a value into a binary stream. """
        raise NotImplementedError()

    def to_bytes(self) -> bytes:
        """ Convert the value into its bytes representation. """
        raise NotImplementedError()

    @classmethod
    def create(
        cls,
        spec: "SpecType",
        name: str,
        parents: typing.Optional[typing.Tuple[str, ...]] = None,
        resolver: typing.Optional["Resolver"] = None,
    ) -> typing.Type[typing_extensions.Self]:
        raise NotImplementedError()


Hashable_T = typing_extensions.TypeVar("Hashable_T", bound= StrictHashable, default=Any)


class EncodingTypeMeta(typing.Generic[SpecType, Hashable_T], ABCMeta):
    """ Metaclass for `EncodingType`, implementing functionalities on its subclasses. """

    def __repr__(cls):
        return f"encoded_data.{cls.__name__}"

EncodingType_T = typing.TypeVar("EncodingType_T", bound="EncodingType")

class EncodingType(typing.Generic[SpecType, Hashable_T], metaclass=EncodingTypeMeta):
    """ Base class for low-level encoding types. """

    value: Hashable_T

    def __init__(self, value: Hashable_T):
        self.value = value
        self.validate()

    @classmethod
    def get_serialiser_names(cls) -> typing.Mapping[typing.Hashable, str]:
        return dict()

    @classmethod
    @abstractmethod
    def read(cls, stream: io.BytesIO) -> typing_extensions.Self:
        """Read the encoded value from a binary stream.

        It converts the read value to the correct type and constructs a new
        instance of the encoding type.
        """

    def __hash__(self) -> int:
        return hash(self.value)

    @abstractmethod
    def to_bytes(self) -> bytes:
        """ Convert the value into its bytes representation. """

    def write(self, stream: io.BytesIO) -> io.BytesIO:
        """ Write the bytes representation of a value into a binary stream. """
        stream.write(self.to_bytes())
        return stream

    def validate(self) -> None:
        """Validate the value.

        Raises:
            DataValidationError: If a value is considered invalid.
                                 By default there is no validation.
        """

    def __repr__(self):
        return f"{type(self).__name__}({repr(self.value)})"

    @classmethod
    def extract_from(
        cls,
        encoder_or_serialiser: typing.Union[typing.Type[typing_extensions.Self], Serialiser],
    ) -> typing.Type[typing_extensions.Self]:
        from diffusion.internal.serialisers.base import Serialiser

        if inspect.isclass(encoder_or_serialiser) and issubclass(
            typing.cast(typing.Type[typing_extensions.Self], encoder_or_serialiser),
            cls,
        ):
            return typing.cast(typing.Type[typing_extensions.Self], encoder_or_serialiser)
        assert isinstance(encoder_or_serialiser, Serialiser)
        return encoder_or_serialiser.to_encoder(cls)

    @classmethod
    def as_tuple(cls, item):
        raise NotImplementedError()

    @classmethod
    def create(
            cls,
            spec: "SpecType",
            name: str,
            parents: typing.Optional[typing.Tuple[str, ...]] = None,
            resolver: typing.Optional["Resolver"] = None,
    ) -> typing.Type[typing_extensions.Self]:
        raise NotImplementedError()

Enc_MetaType = Type[EncodingType]
Enc_MetaType_Str = Union[str, Enc_MetaType]
EncodingTypeVar = TypeVar("EncodingTypeVar", bound=EncodingProtocol)
EncodingTypeOrProtocol = typing.Union[EncodingType, EncodingProtocol]
EncodingTypeOrProtocolType = typing.Type[typing.Union[EncodingType, EncodingProtocol]]
EncodingTypeConcreteVar = TypeVar("EncodingTypeConcreteVar", bound=EncodingType)
EncodingTypeOrProtocolVar = TypeVar(
    "EncodingTypeOrProtocolVar", bound=EncodingTypeOrProtocol
)

Enc_K = TypeVar('Enc_K', bound=EncodingType)
Enc_V = TypeVar('Enc_V', bound=EncodingType)
