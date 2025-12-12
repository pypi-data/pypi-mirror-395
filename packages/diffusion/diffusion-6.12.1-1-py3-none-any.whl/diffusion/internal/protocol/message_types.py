#  Copyright (c) 2020 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

""" Module implementing service message types. """

from __future__ import annotations

import io
import typing
import zlib
from typing import Optional, TYPE_CHECKING

import structlog
from typing_extensions import Protocol, runtime_checkable

from diffusion.internal import encoded_data, services, utils, topics
from diffusion.internal.session.exception_handler import ErrorReasonException, ErrorReason
from .conversations import ConversationID, Conversation
from .exceptions import AbortMessageError
from ... import DiffusionError

# noinspection DuplicatedCode
if TYPE_CHECKING:  # pragma: no cover
    from diffusion.internal.session import InternalSession
    from diffusion.internal.topics import Topic
    from diffusion.internal.services import Service


LOG = structlog.get_logger()


@runtime_checkable
class MessageProtocol(Protocol):
    """ Protocol for implementation of message types. """

    type: int
    description: str

    @classmethod
    async def prepare(cls, session: Optional[InternalSession] = None, **kwargs) -> bytes:
        """ Serialise the message to be sent as bytes. """
        ...  # pragma: no cover

    @classmethod
    async def process(
        cls, stream: io.BytesIO, session: InternalSession, compressed: bool = False
    ) -> None:
        """ Process a received message. """
        ...  # pragma: no cover


class ServiceMessage(MessageProtocol):
    """ Common implementation of service message types. """

    @classmethod
    def _prepare_args(cls, **kwargs) -> tuple:
        cid: ConversationID = kwargs["cid"]
        service: services.Service = kwargs["service"]
        return cid, service


class ServiceRequestMessage(ServiceMessage):
    """ Service request message. """

    type = 0
    description = "SERVICE_REQUEST"

    @classmethod
    async def prepare(cls, session: Optional[InternalSession] = None, **kwargs) -> bytes:
        """ Serialise the message to be sent as bytes. """
        cid, service = cls._prepare_args(**kwargs)
        stream = io.BytesIO()
        stream.write(bytes((cls.type,)))
        encoded_data.Int32(service.service_id).write(stream)
        encoded_data.Int64(cid).write(stream)
        await service.produce(stream, session)
        return stream.getvalue()

    @classmethod
    async def process(
        cls, stream: io.BytesIO, session: InternalSession, compressed: bool = False
    ) -> None:
        """Process a received message."""
        from ..session.error_reason import GenericErrorReason

        service_type_id = encoded_data.Int32.read(stream).value
        service_type = services.get_by_id(service_type_id)
        service = service_type(incoming_message_type=cls)
        cid = ConversationID(encoded_data.Int64.read(stream).value)
        await service.consume(stream, session)
        LOG.debug(
            "Service request.", service=service, cid=cid, request=service.request
        )
        try:
            await service.respond(session)
        except Exception as ex:
            error_reason = ErrorReasonException.from_exception(
                typing.cast(DiffusionError, ex)
            )
            if not error_reason:
                error_reason = ErrorReason(
                    reason_code=GenericErrorReason.CALLBACK_EXCEPTION.value,
                    description=str(ex),
                )
            response = error_reason.Config.as_service_value(
                error_reason, service.error_serializer
            )
            service.response = response
            service.outgoing_message_type = ServiceErrorMessage

        response_message = await service.outgoing_message_type.prepare(
            cid=cid, service=service, session=session
        )
        await session.connection.send(response_message)


class ServiceResponseMessage(ServiceMessage):
    """ Service response message. """

    type = 6
    description = "SERVICE_RESPONSE"

    @classmethod
    async def prepare(cls, session: Optional[InternalSession] = None, **kwargs) -> bytes:
        """ Serialise the message to be sent as bytes. """
        cid, service = cls._prepare_args(**kwargs)
        stream = io.BytesIO()
        stream.write(bytes((cls.type,)))
        encoded_data.Int64(cid).write(stream)
        await cls.prepare_specific(service, session, stream)
        return stream.getvalue()

    class HeaderResponse(typing.NamedTuple):
        cid: ConversationID
        conversation: Conversation
        service: Service

    @classmethod
    def _read_header(cls, stream: io.BytesIO, session: InternalSession) -> HeaderResponse:
        cid = ConversationID(encoded_data.Int64.read(stream).value)
        conversation = session.get_conversation(cid)
        service = conversation.service
        return cls.HeaderResponse(cid, conversation, service)

    @classmethod
    async def prepare_specific(cls, service, session, stream):
        await service.produce(stream, session)

    @classmethod
    async def process(
        cls, stream: io.BytesIO, session: InternalSession, compressed: bool = False
    ) -> None:
        """ Process a received message. """
        cid, conversation, service = cls._read_header(stream, session)
        responded_service: Service = await service.consume(stream, session)
        LOG.debug("Service response.", service=service, cid=cid, response=service.response)
        await conversation.respond(responded_service.response)


class ServiceErrorMessage(ServiceResponseMessage):
    """ Service error message. """

    type = 7
    description = "SERVICE_ERROR"

    @classmethod
    async def prepare_specific(
        cls, service: Service, session: InternalSession, stream: io.BytesIO
    ) -> None:
        service.response.write(stream)

    @classmethod
    async def process(
        cls, stream: io.BytesIO, session: InternalSession, compressed: bool = False
    ) -> None:
        """ Process a received message. """
        cid, conversation, service = cls._read_header(stream, session)
        message_data = encoded_data.String.read(stream)
        message = message_data.value
        conversation = session.conversations.get_by_cid(cid)
        LOG.error("Service error.", message=message, cid=cid, service=service)
        await cls.process_exception(stream, conversation, message)

    @classmethod
    async def process_exception(
        cls,
        stream: io.BytesIO,
        conversation: Conversation,
        message: typing.Optional[str],
    ):
        reason = ErrorReasonException.read(stream, message)
        LOG.error("Service error reason", reason=reason)
        await conversation.complete_exceptionally(reason)


class AbortMessage(MessageProtocol):
    """ Abort message. """

    type = 28
    description = "ABORT"

    @classmethod
    async def prepare(cls, session: Optional[InternalSession] = None, **kwargs) -> bytes:
        """ Serialise the message to be sent as bytes. """
        return b""

    @classmethod
    async def process(
        cls, stream: io.BytesIO, session: InternalSession, compressed: bool = False
    ) -> None:
        """ Process a received message. """
        raise AbortMessageError


class TopicMessage(MessageProtocol):
    """ Common functionality for topic messages. """

    is_delta: bool

    def __init__(self, topic_id: int, session: InternalSession):
        self.topic_id = topic_id
        self.session = session

    @classmethod
    async def prepare(cls, session: Optional[InternalSession] = None, **kwargs) -> bytes:
        """ Serialise the message to be sent as bytes. """
        return b""

    @classmethod
    async def process(
        cls, stream: io.BytesIO, session: InternalSession, compressed: bool = False
    ) -> None:
        """ Read a message from a binary stream. """
        topic_id = int.from_bytes(stream.read(4), "big", signed=True)
        topic: "Topic" = session.data[topics.Topic][topic_id]
        body = stream.read()
        if compressed:
            body = zlib.decompress(body)
        old_value = topic.value
        topic.update(body, is_delta=cls.is_delta)
        await topic.handle("update", old_value=old_value)


class TopicValueMessage(TopicMessage):
    """ Topic value message. """

    type = 4
    description = "TOPIC_VALUE"
    is_delta = False


class TopicDeltaMessage(TopicMessage):
    """ Topic delta message. """

    type = 5
    description = "TOPIC_DELTA"
    is_delta = True


MESSAGE_TYPES = {
    mt.type: mt for mt in utils.get_all_subclasses(MessageProtocol) if hasattr(mt, "type")
}


async def read_stream(stream: io.BytesIO, session: InternalSession) -> None:
    """Read and process an incoming message.

    Selects the corresponding message type based on the initial byte.
    The top bit of the message type byte is borrowed to indicate whether
    the body is compressed, which is communicated to the message type

    Args:
        stream: The binary stream containing the incoming message.
        session: The current internal session.
    """
    # TODO: Implement graceful failure on an unknown message/service type (FB23156)
    message_type_id = stream.read(1)[0]
    compressed = message_type_id >= 0b10000000
    if compressed:
        message_type_id ^= 0b10000000
    message_type = MESSAGE_TYPES[message_type_id]
    LOG.debug("Received message type.", message_type=message_type)
    await message_type.process(stream, session, compressed=compressed)
