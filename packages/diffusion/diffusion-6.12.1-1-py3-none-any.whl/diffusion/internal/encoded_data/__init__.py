#  Copyright (c) 2020 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

""" Low-level encoding and decoding for transmitting data. """
from inspect import isclass

from .abstract import EncodingProtocol, EncodingType
from .exceptions import DataReadError
from .generics import GenericSet, StringSet
from .scalars import Byte, Bytes, Int32, Int64, String


def is_encoder(item) -> bool:
    """ Helper method to check if an object is an EncodingType class. """
    return isclass(item) and issubclass(item, EncodingProtocol)
