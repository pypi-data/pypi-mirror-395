#  Copyright (c) 2020 - 2024 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.


""" Conversations and conversation sets. """

from __future__ import annotations

import dataclasses
import typing

import asyncio
import enum
from typing import Awaitable, Callable, cast, Dict, Iterator, Optional, Union

import structlog

from .exceptions import CIDGeneratorExhaustedError, DiffusionError, NoSuchConversationError
if typing.TYPE_CHECKING:
    from ..services import ServiceValue, Service

LOG = structlog.get_logger()

MAX_CID = 2 ** 63


class ConversationID(int):
    """ Conversation identifier. """

    def __repr__(self):
        return f"<{str(self)}>"

    def __str__(self):
        return f"{self:d}"


class CIDGenerator:
    """ Iterator to create ConversationID values. """

    def __init__(self, initial: int = 1, limit: int = MAX_CID):
        self._iterator = iter(range(initial, limit))

    def __iter__(self) -> Iterator[ConversationID]:
        return self

    def __next__(self) -> ConversationID:
        try:
            return ConversationID(next(self._iterator))
        except StopIteration:
            raise CIDGeneratorExhaustedError


class Result(enum.Enum):
    """ Result of Conversation.respond(). """

    ALREADY_FINISHED = enum.auto()
    HANDLED_AND_ACTIVE = enum.auto()
    HANDLED_AND_FINISHED = enum.auto()


class State(enum.Enum):
    """ Available conversation states. """

    UNRESERVED = enum.auto()
    RESERVED = enum.auto()
    CLOSED = enum.auto()
    DISCARDED = enum.auto()
    EXCEPTION = enum.auto()

    @property
    def is_finished(self):
        """ Checks if the state is considered finished. """
        return self not in (State.UNRESERVED, State.RESERVED)


@dataclasses.dataclass
class ResponseHandler:
    # TODO: review if this can be simplified or even removed (FB23743)
    """A handler for responses received for a conversation.

    All responses received are routed to `on_response` until it returns
    `true` to close the conversation. If the conversation is discarded (for
    example, due to the session being closed), `on_discard` will be called.
    If `on_response` returns `true`, `on_discard` will not be called.

    In addition to the well-defined conversation life-cycle, ConversationSet
    implementations guarantee:

      * A response handler will not be called concurrently for the same
        conversation. A second concurrent request will be blocked until the
        first is available.
      * Calls from the handler to the conversation set are safe. They may result
        in recursive calls to the handler for the same conversation.
      * If `on_response` throws an exception, the conversation will be discarded
        and the handler will not be notified again. The exception will be
        re-thrown to the `Conversation.respond` caller.
      * If `on_discard` throws an exception, it will be logged as an error.
        If the exception is an error, it will be re-thrown.

    ### Not applicable?

    All methods provide the conversation ID for use by advanced handlers. It can
    be used to make recursive or asynchronous calls to discard, or deliver
    further responses if the handler knows the {@link ConversationSet}. Most
    usefully, it can be used to schedule a response timeout.
    """

    event: asyncio.Event = dataclasses.field(default_factory=asyncio.Event)
    conversation: Optional[Conversation] = None
    error: Optional[Exception] = None
    value: Optional[ServiceValue] = None

    async def on_response(self, value: ServiceValue) -> bool:
        """ Triggered on conversation response. """
        self.value = value
        self.event.set()
        return True

    async def on_discard(self, error: Exception) -> None:
        """ Triggered when a conversation is discarded. """
        self.error = error
        self.event.set()

    def __repr__(self):
        return (
            f"<{type(self).__name__} "
            f"cid={self.conversation.cid if self.conversation else None}>"
        )


class Conversation:
    """ Entity that tracks a series of exchanges with the server. """

    def __init__(
        self,
        service: Service,
        conversation_set: "ConversationSet",
        cid: Optional[ConversationID] = None,
        handler: Optional[ResponseHandler] = None,
    ):
        if handler is None:
            handler = ResponseHandler()
        self.handler = handler
        self.handler.conversation = self
        self._cset = conversation_set
        if cid is None:
            cid = next(self._cset.generator)
        self.cid = cid
        self.service = service
        self.state = State.UNRESERVED
        self._pending_discard = None
        self.data: dict = {}

    async def set_finished(self, target: State):
        """ Set the state of the conversation to a target state. """
        if not self.state.is_finished:
            self.state = target

    async def complete_exceptionally(self, reason: Exception):
        """ Complete a conversation with an exception/error. """
        LOG.debug("Application handler threw an exception.", cid=self.cid, exc_info=reason)
        await self.handler.on_discard(reason)
        await self.set_finished(State.EXCEPTION)

    async def respond(self, response: ServiceValue) -> Result:
        """ Check and handle a response. """
        old_state = self.state

        if old_state.is_finished:
            return Result.ALREADY_FINISHED

        self.state = State.RESERVED

        try:
            close = await self.handler.on_response(response)
        except Exception as ex:
            await self.complete_exceptionally(ex)
            raise

        if self.state.is_finished:
            # Finished recursively
            return Result.HANDLED_AND_FINISHED

        if close:
            self.state = State.CLOSED
            return Result.HANDLED_AND_FINISHED

        if old_state == State.UNRESERVED and self._pending_discard:
            self.state = State.DISCARDED
            await self._notify_discard()
            return Result.HANDLED_AND_FINISHED

        self.state = State.UNRESERVED
        return Result.HANDLED_AND_ACTIVE

    async def discard(self, reason):
        """ Discard the conversation with a reason. """
        old_state = self.state

        if old_state == State.RESERVED:
            self._pending_discard = reason
        else:
            self.state = State.DISCARDED

            if old_state == State.UNRESERVED:
                await self._notify_discard(reason)

    def __repr__(self):
        return (
            f"<{type(self).__name__} cid={str(self.cid)} state={self.state}"
            f" handler={self.handler} service={self.service}>"
        )

    async def _notify_discard(self, reason=None):
        if reason is None:
            reason = self._pending_discard
        try:
            await self.handler.on_discard(reason)
        except Exception as ex:
            LOG.error("Application handler threw exception.", cid=self.cid, exc_info=ex)
            if not isinstance(ex, DiffusionError):
                raise

    async def get_value(self):
        """ Retrieve a value or raise an error when the conversation is complete. """
        await self.handler.event.wait()
        if self.handler.error is not None:
            raise self.handler.error
        return self.handler.value


class ConversationSet:
    """ Collection of all conversations initiated by the session. """

    _set_id_generator = CIDGenerator()

    def __init__(self, cid_generator: Optional[CIDGenerator] = None):
        self._set_id = next(self._set_id_generator)
        self.generator = cid_generator or CIDGenerator()
        self.conversations: Dict[ConversationID, Conversation] = {}
        self._discard_all_lock = asyncio.Lock()
        self._set_discard_reason: Optional[Exception] = None

    def __contains__(self, cid: Union[ConversationID, Conversation]) -> bool:
        return getattr(cid, "cid", cid) in self.conversations

    def get_by_cid(self, cid: ConversationID):
        """ Retrieve a conversation from the set based on its ID. """
        try:
            return self.conversations[cid]
        except KeyError:
            raise NoSuchConversationError(cid)

    async def new_conversation(
        self,
        service,
        cid: Optional[ConversationID] = None,
        handler: Optional[ResponseHandler] = None,
        on_open: Optional[Callable[[Conversation], None]] = None,
    ) -> Conversation:
        """ Create a new conversation in the set. """
        conversation = Conversation(
            service=service, cid=cid, conversation_set=self, handler=handler
        )
        if on_open is not None:
            try:
                await cast(Awaitable, on_open(conversation))
            except Exception as ex:
                await conversation.complete_exceptionally(ex)
                raise
        if self._set_discard_reason:
            await conversation.discard(self._set_discard_reason)
        else:
            self.conversations[conversation.cid] = conversation
        return conversation

    async def discard_all(self, reason: Exception):
        """ Discard all the conversations in the set. """
        if not isinstance(reason, Exception):
            raise TypeError("reason must be an exception")
        async with self._discard_all_lock:
            if self._set_discard_reason:
                return
            self._set_discard_reason = reason
        for cid, conversation in self.conversations.items():
            await conversation.discard(reason)
        self.conversations = {}

    def __str__(self):
        return f"ConversationSet<{self._set_id}>"

    def __len__(self):
        return len(self.conversations)
