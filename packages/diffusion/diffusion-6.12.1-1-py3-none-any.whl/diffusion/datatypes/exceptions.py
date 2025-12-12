#  Copyright (c) 2020 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

""" Data types exceptions. """
from diffusion.internal.exceptions import DiffusionError


class DataTypeError(DiffusionError):
    """ General data type error. """


class UnknownDataTypeError(DataTypeError):
    """ Raised if the data type identifier does not exist in the system. """


class IncompatibleDatatypeError(DataTypeError):
    """ Raised if the provided data type was different from expected. """


class InvalidDataError(DataTypeError):
    """ Error with conversion of data. """
