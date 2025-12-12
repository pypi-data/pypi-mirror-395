#  Copyright (c) 2020 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

""" Errors related to Diffusion services. """

from diffusion.internal.exceptions import DiffusionError


class ServiceError(DiffusionError):
    """ Error in a service. """


class UnknownServiceError(ServiceError):
    """ Raised when an undefined service was requested. """


class UnknownHandlerError(ServiceError):
    """ Raised when a requested handler key has not been registered in a session. """
