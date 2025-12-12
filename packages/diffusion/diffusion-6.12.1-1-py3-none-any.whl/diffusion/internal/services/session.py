#  Copyright (c) 2020 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

""" Services related to the local connection to server. """

import io

import structlog

from diffusion import datatypes
from diffusion.internal.serialisers import get_serialiser
from .abstract import (
    InboundService,
    OutboundService,
    InboundService_T,
)

LOG = structlog.get_logger()


class UserPing(OutboundService):
    """ User ping service. """

    service_id = 56
    name = "USER_PING"
    request_serialiser = get_serialiser("ping-request")
    response_serialiser = get_serialiser("ping-response")

    def _write_request(self, stream: io.BytesIO):
        ...  # pragma: no cover

    def _read_response(self, stream: io.BytesIO):
        self.response.set("Ping response")
        return self


class SystemPing(InboundService):
    """ System ping service. """

    service_id = 55
    name = "SYSTEM_PING"
    request_serialiser = get_serialiser("ping-request")
    response_serialiser = get_serialiser("ping-response")

    def _read_request(
        self: InboundService_T, stream: io.BytesIO
    ) -> InboundService_T:
        self.request.set("Ping request")
        return self

    async def respond(self, session) -> None:
        """Respond to a system ping."""
        self.response.set(await session.handle(type(self)))


class ChangePrincipal(OutboundService):
    """ Change principal service. """

    service_id = 5
    name = "CHANGE_PRINCIPAL"
    request_serialiser = get_serialiser("change-principal-request")
    response_serialiser = get_serialiser("boolean")

    def _read_response(self, stream: io.BytesIO):
        datatype_name, response_value = self.response_serialiser.read(stream)
        response = datatypes.get(datatype_name).from_bytes(response_value)
        self.response.set(response)
        return self
