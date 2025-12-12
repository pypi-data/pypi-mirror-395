#  Copyright (c) 2021 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

""" Complex data type definitions. """

import typing
from typing_extensions import TypeAlias
from ..primitives.jsondatatype import JsonDataType, JsonTypes
from .recorddatatype import RecordDataType
from .unknowndatatype import UnknownDataType


JSON: TypeAlias = JsonDataType
RECORD_V2: TypeAlias = RecordDataType
UNKNOWN: TypeAlias = UnknownDataType
ComplexDataTypes = typing.Union[JSON, RECORD_V2]
"""
Complex Diffusion data types.
"""

ComplexDataTypesClasses = typing.Union[
    typing.Type[JSON],
    typing.Type[RECORD_V2],
]
"""
Classes of complex Diffusion data types.
"""
