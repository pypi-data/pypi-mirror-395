from __future__ import annotations

import typing

from typing_extensions import Protocol

import typing_extensions

from .abstract import ValueTypeProtocol, RealValue_Precise

from .datatype import HasCodeAndName, TypeCode, TypeName

@typing_extensions.runtime_checkable
class HasRawTypes(typing_extensions.Protocol[RealValue_Precise]):
    """
    Protocol describing an object with  the given raw datatype
    """
    @classmethod
    def get_raw_types(cls) -> typing.Type[RealValue_Precise]: ...


@typing_extensions.runtime_checkable
class HasRawTypesOrMore(
    HasRawTypes[typing.Union[RealValue_Precise, typing.Any]],
    typing_extensions.Protocol[RealValue_Precise],
):
    """
    Protocol describing an object with at least the given raw datatype
    """


@typing_extensions.runtime_checkable
class ValueTypeProtocolSpecific(
    ValueTypeProtocol,
    HasRawTypes[RealValue_Precise],
    Protocol[RealValue_Precise],
):
    """
    Protocol describing a Diffusion Datatype-like-object with at least the given raw datatype
    """


@typing_extensions.runtime_checkable
class ValueTypeProtocolSpecificOrMore(
    ValueTypeProtocol,
    HasRawTypesOrMore[RealValue_Precise],
    Protocol[RealValue_Precise],
):
    """
    Protocol describing a Diffusion Datatype-like-object with the given raw datatype
    """


ValueType_Specific_T = typing_extensions.TypeVar(
    "ValueType_Specific_T",
    bound=ValueTypeProtocolSpecific,
    contravariant=True,
    default=typing.Any,
)


@typing_extensions.runtime_checkable
class ValueTypeProtocolWithCodeAndName(
    ValueTypeProtocol,
    HasCodeAndName[TypeCode, TypeName],
    typing_extensions.Protocol[RealValue_Precise, TypeCode, TypeName],
): ...


ValueTypeProtocolWithCodeAndName_T = typing_extensions.TypeVar(
    "ValueTypeProtocolWithCodeAndName_T",
    bound=ValueTypeProtocolWithCodeAndName,
    covariant=True,
)
