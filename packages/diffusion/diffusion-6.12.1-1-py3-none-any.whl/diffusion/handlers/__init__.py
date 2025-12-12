#  Copyright (c) 2022 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

"""Base module for various event handlers."""
from  __future__ import annotations
import abc
import typing

import asyncio

import structlog
import typing_extensions
from typing_extensions import Protocol, runtime_checkable, TypedDict

from diffusion.internal import exceptions
from diffusion.internal.utils import coroutine
if typing.TYPE_CHECKING:
    from diffusion.features.topics.details.topic_specification import TopicSpecification
    from diffusion.features.topics import UnsubscribeReason
    # noinspection PyUnresolvedReferences
    from diffusion.datatypes import AbstractDataType
    from diffusion.internal.protocol.conversations import ConversationID
    from diffusion import SessionId

LOG: structlog.stdlib.BoundLogger = structlog.get_logger()


@runtime_checkable
class Handler(Protocol):
    """Protocol for event handlers implementation."""

    async def handle(self, event: str, **kwargs: typing.Any) -> typing.Any:
        """Implements handling of the given event.

        Args:
            event: The event identifier.
            **kwargs: Additional arguments.
        """
        ...  # pragma: no cover

    def remove(self, sub_handler: Handler) -> None:
        """
        Removes the given sub-handler from the given handler.

        Raises:
            KeyError: If the handler does not exist.
        """
        return None


HandlersMapping = typing.MutableMapping[typing.Hashable, Handler]


class UnknownHandlerError(exceptions.DiffusionError):
    """ Raised when a requested handler key has not been registered in the session. """

AT_T_contra = typing_extensions.TypeVar(
    "AT_T_contra",
    bound="AbstractDataType",
    default="AbstractDataType",
    contravariant=True,
)
"""
The type of topic values received by a Handler (contravariant).
"""

AT_T_co = typing_extensions.TypeVar(
    "AT_T_co", bound="AbstractDataType", default=typing.Any, covariant=True
)
"""
The type of topic values received by a Handler (covariant).
"""

Callback_RT = typing_extensions.TypeVar("Callback_RT", default=typing.Any, covariant=True)
"""
Callback return type.
"""

class SubHandlerArgs(typing_extensions.TypedDict, typing.Generic[AT_T_co], total=True):
    """
    Named arguments to the [diffusion.handlers.SubHandlerProtocol][]
    """

    topic_path: typing_extensions.Annotated[
        str, typing_extensions.Doc("Topic path.")
    ]
    topic_value: typing_extensions.Annotated[
        typing.Optional[AT_T_co],
        typing_extensions.Doc("Topic value."),
    ]
    topic_spec: typing_extensions.Annotated[
        TopicSpecification, typing_extensions.Doc("Topic spec.")
    ]


class UpdateArgs(
    typing_extensions.TypedDict,
    SubHandlerArgs[AT_T_co],
    total=True,
):
    """
    Inherits all parameters from [diffusion.handlers.SubHandlerArgs][].
    """

    old_value: typing_extensions.Annotated[
        typing.Optional[AT_T_co],
        typing_extensions.Doc(
            "The old topic value. "
            "Will be None for the first update callback in a stream "
            "(as there is no previous value)."),
    ]


class UnsubscribeArgs(
    typing_extensions.TypedDict,
    SubHandlerArgs[AT_T_co],
    total=True,
):
    """
    Inherits all parameters from [diffusion.handlers.SubHandlerArgs][].
    """

    reason: typing_extensions.Annotated[
        UnsubscribeReason, typing_extensions.Doc("Reason for unsubscription.")
    ]


@runtime_checkable
class SubHandlerProtocol(Protocol[AT_T_contra, Callback_RT]):
    def __call__(
        self,
        **kwargs: typing_extensions.Unpack[SubHandlerArgs[AT_T_contra]],
    ) -> Callback_RT:
        """
        Subhandler Protocol - callbacks should fulfil this interface.

        Returns:
            A value of type diffusion.handlers.Callback_RT][]
        """
        pass   # pragma: no cover

class UnsubscribeProtocol(Protocol[AT_T_contra, Callback_RT]):
    def __call__(
            self,
            **kwargs: typing_extensions.Unpack[UnsubscribeArgs[AT_T_contra]],
    ) -> Callback_RT:
        """
        Unsubscribe Callback Protocol - callbacks should fulfil this interface.

        Returns:
            A value of type diffusion.handlers.Callback_RT][]
        """
        pass   # pragma: no cover


class UpdateProtocol(Protocol[AT_T_contra, Callback_RT]):
    def __call__(
            self,
            **kwargs: typing_extensions.Unpack[UpdateArgs[AT_T_contra]],
    ) -> Callback_RT:
        """
        Update Callback Protocol - callbacks should fulfil this interface.

        Returns:
            A value of type diffusion.handlers.Callback_RT][]
        """
        pass   # pragma: no cover

# fallback for tooling that doesn't support Callable Protocols
SubHandler = typing.Union[
    SubHandlerProtocol, typing.Callable, typing.Callable[[typing.Any], typing.Any]
]


class SimpleHandler(Handler):
    """ Wraps a callable into a Handler protocol instance. """

    def __init__(self, callback: SubHandler):
        self._callback = coroutine(callback)

    async def handle(self, event: str = "", **kwargs: typing.Any) -> typing.Any:
        """Implements handling of the given event.

        Args:
            event: The event identifier.
            **kwargs: Additional arguments.
        """
        return await self._callback(**kwargs)


class AbstractHandlerSet(Handler, typing.Iterable[Handler], abc.ABC):
    async def handle(self, event: str = "", **kwargs: typing.Any) -> typing.Any:
        """Implements handling of the given event.

        Args:
            event: The event identifier.
            **kwargs: Additional arguments.

        Returns:
            Aggregated list of returned values.
        """
        return await asyncio.gather(
            *[handler.handle(event=event, **kwargs) for handler in self]
        )


class HandlerSet(set, AbstractHandlerSet):
    """ A collection of handlers to be invoked together. """


class SubHandlerDict(TypedDict, total=False):
    subscribe: SubHandler


class OptionalDict(SubHandlerDict, total=False):
    pass


class ErrorHandler(Protocol[Callback_RT]):
    def __call__(self, code: int, description: str, **kwargs) -> Callback_RT:
        """
        Handle an error.

        Args:
            code: the error code
            description: the error description.
        """
        pass    # pragma: no cover


SubHandlerDictType = typing.TypeVar("SubHandlerDictType", bound=SubHandlerDict)

class FilterResponseArg(typing.TypedDict, total=True):
    conversation_id: ConversationID
    sender_session_id: SessionId
    path: str
    expected: int
    received: int

class FilterResponseProtocol(typing.Protocol[AT_T_contra, Callback_RT]):
    def __call__(
        self,
        response: typing.Optional[AT_T_contra],
        **kwargs: typing_extensions.Unpack[FilterResponseArg]
    ) -> Callback_RT: ...

class EventStreamHandler(Handler, typing.Generic[AT_T_co, Callback_RT]):
    """Generic handler of event streams.

    Each keyword argument is a callable which will be converted to coroutine
    and awaited to handle the event matching the argument keyword.
    """
    _handlers: SubHandlerDict

    def __init__(
        self,
        *,
        error: typing.Optional[ErrorHandler] = None,
        response: typing.Optional[FilterResponseProtocol[AT_T_co, Callback_RT]] = None,
        **kwargs: typing.Optional[SubHandlerProtocol]
    ):
        """

        Args:
            on_error: error handler callback
            **kwargs: other subhandlers
        """
        all_args = typing.cast(typing.Dict[str, typing.Any], kwargs)
        all_args.update(error=error, response=response)
        self._handlers: SubHandlerDict = typing.cast(
            SubHandlerDict,
            {
                event: coroutine(callback)
                for event, callback in all_args.items()
                if callback
            },
        )

    async def handle(self, event: str, **kwargs: typing.Any) -> typing.Any:
        """Implements handling of the given event.

        Args:
            event: The event identifier.
            **kwargs: Additional arguments.
        """
        try:
            handler = (typing.cast(typing.Mapping[str, typing.Callable], self._handlers))[event]
        except KeyError:
            LOG.debug("No handler registered for event.", stream_event=event, **kwargs)
        else:
            return await handler(**kwargs)

    def __str__(self):
        return f"{type(self)} with handlers {self._handlers}"

    def __repr__(self):
        return str(self)
