#  Copyright (c) 2020 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

""" Diffusion data types. """

from __future__ import annotations

import sys
import typing

from inspect import isclass
from typing import cast, Mapping, Type, Union, overload
import typing_extensions

from . import complex, primitives
from .foundation.abstract import AbstractDataType, ValueType
from .foundation.types import ValueTypeProtocolWithCodeAndName, \
    ValueTypeProtocolWithCodeAndName_T
from .foundation.datatype import TypeCode_Bound, TypeName_Bound, TypeCode, TypeName
from .foundation.object import Object
from diffusion.features.topics.details.topic_specification import TopicSpecification

from .foundation.datatype import DataType

from .exceptions import (
    DataTypeError,
    IncompatibleDatatypeError,
    InvalidDataError,
    UnknownDataTypeError,
)
from .primitives.jsondatatype import JsonTypes

from .timeseries import TimeSeriesDataType, TimeSeriesEventDataType
DataTypeArgument = Union[
    TypeName_Bound, TypeCode_Bound, Type[ValueType], TopicSpecification
]

# datatype aliases for convenience
BINARY = primitives.BinaryDataType
"""
Binary datatype alias, points to
[BinaryDataType][diffusion.datatypes.primitives.BinaryDataType]
"""
DOUBLE = primitives.DoubleDataType
"""
Double datatype alias, points to
[DoubleDataType][diffusion.datatypes.primitives.DoubleDataType]
"""
INT64 = primitives.Int64DataType
"""
Int64 datatype alias, points to
[Int64DataType][diffusion.datatypes.primitives.Int64DataType]
"""
STRING = primitives.StringDataType
"""
String datatype alias, points to
[StringDataType][diffusion.datatypes.primitives.StringDataType]
"""
JSON: typing_extensions.TypeAlias = typing.cast(  # type: ignore[no-redef]
    typing.Type[complex.JsonDataType[JsonTypes]], complex.JsonDataType
)
"""
Json datatype alias, points to
[JsonDataType][diffusion.datatypes.complex.JsonDataType]
"""
RECORD_V2 = complex.RecordDataType
"""
Record V2 datatype alias, points to
[RecordDataType][diffusion.datatypes.complex.RecordDataType]
"""
TIME_SERIES = TimeSeriesEventDataType
"""
TimeSeries datatype alias, points to
[TimeSeriesEventDataType][diffusion.datatypes.timeseries.TimeSeriesEventDataType]
"""
UNKNOWN = complex.UnknownDataType
"""
Unknown datatype alias, points to
[UnknownDataType][diffusion.datatypes.complex.UnknownDataType]
"""
OBJECT = Object
"""
Object datatype - effectively a token indicating types should not be converted
"""

_dt_module = sys.modules[__name__]  # this module

# index and cache the implemented data types by type codes
_indexed_data_types: Mapping[int, Type[AbstractDataType]] = {
    item.type_code: item
    for item in vars(_dt_module).values()
    if isclass(item) and issubclass(item, AbstractDataType) and hasattr(item, 'type_code')
}

def _get_impl(data_type: DataTypeArgument) -> typing.Type[AbstractDataType]:
    if isinstance(data_type, str):
        data_type_final = getattr(_dt_module, data_type.strip().upper(), None)
    elif isinstance(data_type, int):
        data_type_final = _indexed_data_types.get(data_type)
    else:
        data_type_final = data_type
    if isinstance(data_type, TopicSpecification):
        return data_type.topic_type
    if isclass(data_type_final) and issubclass(data_type_final, DataType):  # type: ignore
        return cast(Type[AbstractDataType], data_type_final)
    raise UnknownDataTypeError(f"Unknown data type '{data_type}'.")


class Getter():
    @overload
    def __call__(self, data_type: typing.Union[
        typing_extensions.Literal['string'], typing_extensions.Literal[17]]) -> \
    typing_extensions.Type[primitives.StringDataType]:
        ...

    @overload
    def __call__(self, data_type: typing_extensions.Literal['int64', 18]) -> \
    typing_extensions.Type[primitives.Int64DataType]:
        ...

    @overload
    def __call__(self, data_type: typing_extensions.Literal['json', 15]) -> \
    typing_extensions.Type[complex.JSON]:
        ...

    @overload
    def __call__(self, data_type: typing_extensions.Literal['double', 19]) -> \
    typing_extensions.Type[primitives.doubledatatype.DoubleDataType]:
        ...

    @overload
    def __call__(self, data_type: typing_extensions.Literal['binary', 14]) -> \
    typing_extensions.Type[primitives.binarydatatype.BinaryDataType]:
        ...

    @overload
    def __call__(self, data_type: typing_extensions.Literal['record_v2', 20]) -> \
    typing_extensions.Type[complex.recorddatatype.RecordDataType]:
        ...

    @overload
    def __call__(self, data_type: typing_extensions.Literal['time_series', 16]) -> \
    typing_extensions.Type[TimeSeriesEventDataType]:
        ...

    @overload
    def __call__(self, data_type: typing_extensions.Literal['unknown', 21]) -> \
    typing_extensions.Type[complex.UnknownDataType]:
        ...

    @overload
    def __call__(
        self, data_type: TopicSpecification[ValueTypeProtocolWithCodeAndName_T]
    ) -> typing.Type[ValueTypeProtocolWithCodeAndName_T]: ...


    @overload
    def __call__(
        self, data_type: typing.Type[ValueTypeProtocolWithCodeAndName_T]
    ) -> typing.Type[ValueTypeProtocolWithCodeAndName_T]: ...


    def __call__(
        self, data_type: DataTypeArgument
    ) -> typing.Type[ValueTypeProtocolWithCodeAndName]:
        """Helper function to retrieve a datatype based on its name or a `DataTypes` value.

        Args:
            data_type: Either a string that corresponds to the `type_name` attribute
                       of a `DataType` subclass, or an integer that corresponds to the
                       `type_code` of a `DataType` subclass. It also accepts an actual
                       `DataType` subclass, which is returned unchanged.

        Raises:
            `UnknownDataTypeError`: If the corresponding data type was not found.

        Examples:
            >>> get('string')
            <class 'diffusion.datatypes.primitives.stringdatatype.StringDataType'>
            >>> get(INT64)
            <class 'diffusion.datatypes.primitives.int64datatype.Int64DataType'>
            >>> get(15)
            <class 'diffusion.datatypes.complex.jsondatatype.JsonDataType'>
        """
        return typing.cast(
            typing.Type[ValueTypeProtocolWithCodeAndName], _get_impl(data_type)
        )

get: Getter = Getter()
