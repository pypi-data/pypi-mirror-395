#  Copyright (c) 2020 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

""" Base exceptions module. """
import typing

class DiffusionMetaError(type):
    def __hash__(cls):
        return hash(repr(cls))

class DiffusionError(Exception, metaclass=DiffusionMetaError):
    """ Base exception class for all Diffusion errors. """
    default_description = "{message}"

    def __init__(self, message: typing.Optional[str] = "", *args, **kwargs):
        super().__init__(self.description(message=message, **kwargs), *args)

    @classmethod
    def description(cls, message: typing.Optional[str] = "", **kwargs):
        return message or cls.default_description.format(message=message, **kwargs)
