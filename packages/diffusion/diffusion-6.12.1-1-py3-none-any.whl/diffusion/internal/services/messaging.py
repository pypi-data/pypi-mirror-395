#  Copyright (c) 2020 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

""" Messaging service module. """

from __future__ import annotations

import io
import typing
from typing import TYPE_CHECKING

import structlog
from diffusion import datatypes

from diffusion.internal import protocol
from diffusion.internal.serialisers import get_serialiser
from .abstract import InboundService, OutboundService, OutboundService_T

if TYPE_CHECKING:  # pragma: no cover
    from diffusion.internal.session import InternalSession
    from diffusion.internal.services.abstract import Service_T

LOG = structlog.get_logger()

CONTROL_GROUP_DEFAULT = "default"

MessagingSend_T = typing.TypeVar(
    "MessagingSend_T", bound="MessagingSend"
)


class MessagingSend(OutboundService, InboundService):
    """Request-Response service."""

    service_id = 85
    name = "MESSAGING_SEND"
    request_serialiser = get_serialiser(
        "messaging-send-request"
    )
    response_serialiser = get_serialiser(
        "messaging-response"
    )

    def _read_response(
        self: MessagingSend_T, stream: io.BytesIO
    ) -> MessagingSend_T:
        (
            datatype_name,
            response_value,
        ) = self.response_serialiser.read(stream)
        response = datatypes.get(datatype_name).from_bytes(
            response_value
        )
        self.response = self.response.evolve(response)
        return self.evolve(response=self.response)

    def _read_request(
        self: MessagingSend_T, stream: io.BytesIO
    ) -> MessagingSend_T:
        (
            path,
            datatype_name,
            response_value,
        ) = self.request_serialiser.read(stream)
        message = datatypes.get(datatype_name).from_bytes(
            response_value
        )
        self.request.set(path, message)
        return self

    async def consume(
        self: MessagingSend_T,
        stream: io.BytesIO,
        session: InternalSession,
    ) -> MessagingSend_T:
        """Receive a request or response from the server."""
        if (
            self.message_type
            is protocol.message_types.ServiceRequestMessage
        ):
            return self._read_request(stream)
        else:
            return self._read_response(stream)

    async def produce(
        self, stream: io.BytesIO, session: InternalSession
    ) -> None:
        """Send the request to the server."""
        if self.response.serialised_value is None:
            self._write_request(stream)
        else:
            self._write_response(stream)

    async def respond(self, session: InternalSession):
        """Send a response to a received message."""
        handler_key = (
            type(self),
            self.request["message-path"],
        )
        response = await session.handle(
            handler_key,
            request=self.request.serialised_value,
        )
        self.response.set(response)


class MessagingReceiverServer(OutboundService):
    """Request-Response service - for sending requests to clients by session ID."""

    service_id = 86
    name = "MESSAGING_RECEIVER_SERVER"
    request_serialiser = get_serialiser(
        "messaging-client-send-request"
    )
    response_serialiser = get_serialiser(
        "messaging-response"
    )

    def _read_response(
        self: Service_T, stream: io.BytesIO
    ) -> Service_T:
        (
            datatype_name,
            response_value,
        ) = self.response_serialiser.read(stream)
        response = datatypes.get(datatype_name).from_bytes(
            response_value
        )
        self.response.set(response)
        return self

class MessagingReceiverClient(InboundService):
    """Request-Response service - for receiving requests from other clients."""

    service_id = 88
    name = "MESSAGING_RECEIVER_CLIENT"
    request_serialiser = get_serialiser("messaging-client-forward-send-request")
    response_serialiser = get_serialiser("messaging-response")

    async def respond(self, session: InternalSession):
        """Send a response to a received message."""
        from diffusion.internal.serialisers.specific.messaging import \
            MessagingClientForwardSendRequestSerializer
        from ...session.exceptions import RejectedRequestError
        request = MessagingClientForwardSendRequestSerializer.from_service_value(self.request)
        handler_key = (type(self), request.context['path'])
        try:
            response = await session.handle(
                handler_key, request=request.value, **request.context
            )
            self.response.set(response)
        except BaseException as e:
            raise RejectedRequestError("Callback threw error") from e


class MessagingReceiverControlRegistration(OutboundService):
    """ Request receiver control client registration. """

    service_id = 97
    name = "MESSAGING_RECEIVER_CONTROL_REGISTRATION"
    request_serialiser = get_serialiser("message-receiver-control-registration-request")
    response_serialiser = get_serialiser()


class MessagingFilterSender(OutboundService):
    """Request-Response service - for sending requests to clients by session ID."""

    service_id = 102
    name = "MESSAGING_FILTER_SENDER"
    request_serialiser = get_serialiser(
        "messaging-client-filter-send-request"
    )
    response_serialiser = get_serialiser(
        "count-or-parser-errors2"
    )

    def _read_response(
        self: OutboundService_T, stream: io.BytesIO
    ) -> OutboundService_T:
        response, *_ = self.response_serialiser.read(stream)
        self.response.set(response)
        return self


class FilterResponse(InboundService):
    """ Response to a session filtered request. """

    service_id = 103
    name = "FILTER_RESPONSE"
    request_serialiser = get_serialiser("filter-response")
    response_serialiser = get_serialiser()

    async def respond(self, session: InternalSession) -> None:
        """ Respond to a filter message response. """
        conversation = session.get_conversation(self.request["conversation-id"])
        conversation.data["received"] += 1
        error, *response = self.request["filter-response"]
        if error:
            code, description = response[0]
            LOG.warning("Error reason.", code=code, description=description)
            kwargs = {"code": code, "description": description}
            handler_key: tuple = (type(self), conversation.data["filter"], "error")
        else:
            datatype, value = response
            response = datatypes.get(datatype).from_bytes(value)
            LOG.debug(f"Received response: {response}")
            kwargs = {
                "response": response,
                "session_id": protocol.SessionId(*self.request["session-id"]),
            }
            kwargs.update(conversation.data)
            handler_key = (type(self), conversation.data["filter"])
        await session.handle(handler_key, event="response", **kwargs)
        LOG.debug("Received {received} of {expected} message(s).".format(**conversation.data))
