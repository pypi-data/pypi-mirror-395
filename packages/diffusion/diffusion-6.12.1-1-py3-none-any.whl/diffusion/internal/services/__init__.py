#  Copyright (c) 2020 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

""" Diffusion services package. """
from __future__ import annotations

from typing import Type

from .abstract import Service, InboundService, OutboundService, ServiceValue
from .exceptions import ServiceError, UnknownServiceError
from .messaging import MessagingSend, MessagingReceiverControlRegistration
from .session import SystemPing, UserPing
from .topics import Subscribe


def get_by_id(service_id: int) -> Type[Service]:
    """ Retrieve a service class based on its ID number. """
    return Service.get_by_id(service_id)


def get_by_name(service_name: str) -> Type[Service]:
    """ Retrieve a service class based on its name. """
    return Service.get_by_name(service_name)
