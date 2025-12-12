#  Copyright (c) 2020 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

""" Exceptions for encoded data. """

from diffusion.internal.exceptions import DiffusionError


class DataError(DiffusionError):
    """ General error with data encoding. """


class DataValidationError(DataError):
    """ Validation error. """


class DataWriteError(DataError):
    """ Error when writing data. """


class DataReadError(DataError):
    """ Error when reading data. """


class StreamExhausted(DataReadError):  # NOQA: N818
    """
    Error for unexpectedly reaching the end of a stream.
    """
