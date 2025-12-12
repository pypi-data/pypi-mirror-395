#  Copyright (c) 2020 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

""" Request-response messaging functionality. """
from __future__ import annotations

import typing
from typing import TypeVar, Protocol, Generic, Type, Any
import typing_extensions
from typing import Collection, Optional

import structlog

from diffusion import datatypes as dt
from diffusion.datatypes import DataType, DataTypeArgument, TypeCode_Bound, TypeName_Bound
from diffusion.datatypes.foundation.types import ValueTypeProtocolSpecific, \
    ValueTypeProtocolWithCodeAndName, HasRawTypes, HasRawTypesOrMore, \
    ValueTypeProtocolSpecificOrMore, ValueTypeProtocol
from diffusion.datatypes.foundation.ibytesdatatype import IBytes
from diffusion.datatypes.primitives.jsondatatype import JsonTypes_Bound
from diffusion.features.topics import TopicSpecification
from diffusion.handlers import Handler
from diffusion.internal import utils
from diffusion.internal.components import Component
from diffusion.internal.exceptions import DiffusionError
from diffusion.internal.protocol.conversations import ConversationID
from diffusion.internal.protocol.exceptions import ErrorReport
from diffusion.session import SessionProperties
from diffusion.internal.validation import StrictStr
from diffusion.internal.protocol import SessionId
from diffusion.session.exceptions import SessionError

LOG = structlog.get_logger()

ValueType_Bound = typing.Optional[typing.Union[JsonTypes_Bound, ValueTypeProtocol]]
"""
The upper bound of all request and response types.
"""

J_In = TypeVar("J_In", bound=ValueType_Bound, contravariant=True)
"""
A value to be processed by a [Callback][diffusion.messaging.Callback].
"""

J_Out_MaybeAwaitable = TypeVar(
    "J_Out_MaybeAwaitable",
    bound=typing.Union[
        ValueType_Bound, typing_extensions.Awaitable[ValueType_Bound]
    ],
    covariant=True,
)
"""
A value to be returned by a [Callback][diffusion.messaging.Callback].
"""

J_In_contra = typing_extensions.TypeVar(
    "J_In_contra",
    bound=ValueType_Bound,
    contravariant=True,
    default=Any,
)
"""
A value to be processed by a [Callback][diffusion.messaging.Callback] (contravariant).
"""

J_Out_contra = typing_extensions.TypeVar(
    "J_Out_contra",
    bound=ValueType_Bound,
    contravariant=True,
    default=Any,
)
"""
A value to be returned by a [Callback][diffusion.messaging.Callback] (contravariant).
"""


TRequest = TypeVar(
    "TRequest",
    bound=ValueType_Bound,
    covariant=True,
)
TResponse = TypeVar("TResponse", bound=ValueType_Bound, contravariant=True)

TRequest_callback = TypeVar(
    "TRequest_callback",
    bound=ValueType_Bound,
    contravariant=True,
)
TResponse_callback = TypeVar("TResponse_callback", bound=ValueType_Bound, covariant=True)


TRequest_Diff_Type = TypeVar(
    "TRequest_Diff_Type",
    bound=IBytes,
    contravariant=True,
)
TResponse_Diff_Type = TypeVar("TResponse_Diff_Type", bound=IBytes, contravariant=True)

TypeName_In = typing_extensions.TypeVar(
    "TypeName_In", bound=TypeName_Bound, default=TypeName_Bound
)
"""
The [TypeName][diffusion.datatypes.foundation.types.TypeName] of the incoming request.
"""

TypeName_Out = typing_extensions.TypeVar(
    "TypeName_Out", bound=TypeName_Bound, default=TypeName_Bound
)
"""
The [TypeName][diffusion.datatypes.foundation.types.TypeName] of the outgoing response.
"""

TypeCode_In = typing_extensions.TypeVar(
    "TypeCode_In", bound=TypeCode_Bound, default=TypeCode_Bound
)
"""
The [TypeCode][diffusion.datatypes.foundation.types.TypeCode] of the incoming request.
"""

TypeCode_Out = typing_extensions.TypeVar(
    "TypeCode_Out", bound=TypeCode_Bound, default=TypeCode_Bound
)
"""
The [TypeCode][diffusion.datatypes.foundation.types.TypeCode] of the outgoing response.
"""


class RequestContext(typing.TypedDict, total=False):
    sender_session_id: typing_extensions.NotRequired[SessionId]
    """ The Session ID"""
    path: typing_extensions.NotRequired[str]
    """ The path """
    session_properties: typing_extensions.NotRequired[SessionProperties]
    """ Sesssion Properties of the session """


@typing_extensions.runtime_checkable
class Callback(Protocol[J_In, J_Out_MaybeAwaitable]):
    def __call__(
            self, request: J_In, **kwargs: typing_extensions.Unpack[RequestContext]
    ) -> J_Out_MaybeAwaitable:
        """
        Called when request is received

        Args:
            request: The received request
            kwargs: Request context information
        """

class Messaging(Component):
    """Messaging component.

    It is not supposed to be instantiated independently; an instance is available
    on each `Session` instance as `session.messaging`.

    This feature provides a client session with request-response messaging capabilities
    that can be used to implement application services.

    Request-response messaging allows a session to send requests to other sessions.
    Each receiving session provides a corresponding response, which is returned to the
    sending session. Each request and response carries an application provided value.

    The method used to send a request determines which sessions will receive it.
    Each request is routed using the provided *message path* – an application provided
    string. Two addressing schemes are provided: *unaddressed requests* and
    *addressed requests*.

    Unaddressed requests
    -------------------
    A session can provide an application service by implementing a handler and
    registering it with the server. This is somewhat similar to implementing a
    REST service, except that interactions between the sender and receiver are
    asynchronous.

    Unaddressed requests sent using send_request_async() are routed by the server
    to a handler that has been pre-registered by another session, and matches the
    message path.

    Handlers are registered with add_request_handler_async(). Each session may
    register at most one handler for a given message path. Optionally, one or more
    session property names can be provided (see ISession for a full description of
    session properties), in which case the values of the session properties for each
    recipient session will be returned along with its response. To add a request
    handler, the control client session must have REGISTER_HANDLER permission. If
    registering to receive session property values, the session must also have
    VIEW_SESSION permission.

    Routing works as follows:

    1. The session sends the request (with send_request_async()) providing the
      message path, the request value and data type, and the expected response type.
    2. The server uses the message path to apply access control. The sender must
      have the SEND_TO_MESSAGE_HANDLER path permission for the message path, or
      the request will be rejected.
    3. The server uses the message path to select a pre-registered handler and
      route the request to the appropriate recipient session. The server will
      consider all registered handlers and select one registered for the most
      specific path. If multiple sessions have registered a handler registered for
      a path, one will be chosen arbitrarily. If there is no registered handler
      matching the message path, the request will be rejected.
    4. Otherwise, the server forwards the request to one of the sessions
      registered to handle the message path. The message path is also passed to the
      recipient session, providing a hierarchical context.
    5. The recipient session processes the request and returns a response to the
      server, which forwards the response to the sending session.

    Registration works across a cluster of servers. If no matching handler is
    registered on the server to which the sending session is connected, the
    request will be routed to another server in the cluster that has one.

    Addressed requests
    ----------------
    Addressed requests provide a way to perform actions on a group of sessions,
    or to notify sessions of one-off events (for repeating streams of events, use
    a topic instead).

    An addressed request can be sent to a set of sessions using
    send_request_to_filter_async(). For the details of session filters, see ISession.
    Sending a request to a filter will match zero or more sessions. Each response
    received will be passed to the provided IFilteredRequestCallback. As a
    convenience, an addressed request can be sent to a specific session using the
    overloaded variant of send_request_async() that accepts a session id.

    Sending an addressed request requires SEND_TO_SESSION permission.

    If the sending session is connected to a server belonging to a cluster, the
    recipient sessions can be connected to other servers in the cluster. The
    filter will be evaluated against all sessions hosted by the cluster.

    To receive addressed requests, a session must set up a local request stream
    to handle the specific message path, using set_request_stream().
    When a request is received for the message path, the on_request()
    method on the stream is triggered. The session should respond using the
    provided respond() method call. Streams receive an on_close() callback when
    unregistered and an on_error() callback if the session is closed.

    If a request is sent to a session that does not have a matching stream for
    the message path, an error will be returned to the sending session.

    Accessing the feature
    -------------------
    Obtain this feature from an ISession as follows:

       messaging = session.messaging

    Since:
       6.6
    """

    def add_stream_handler(
        self,
        path: str,
        handler: RequestHandler,
        addressed: bool = False,
    ) -> None:
        """Registers a request stream handler.

        The handler is invoked when the session receives a request sent
        to the given path or session filter.

        Args:
            path: The handler will respond to the requests to this path.
            handler: A Handler instance to handle the request.
            addressed: `True` to handle the requests addressed to the session's ID or
                       using a session filter; `False` for unaddressed requests.
        """
        service_type_name = "MESSAGING_SEND" if addressed else "MESSAGING_RECEIVER_CLIENT"
        service_type = type(self.services[service_type_name])
        self.session.handlers[(service_type, path)] = handler

    def add_filter_response_handler(self, session_filter: str, handler: Handler) -> None:
        """Registers a session filter response handler.

        The handler is invoked when the session receives a response
        to a request sent to the session filter.

        Args:
            session_filter: A session filtering query.
            handler: A Handler instance to handle the request.
        """
        service_type = type(self.services.FILTER_RESPONSE)
        self.session.handlers[(service_type, session_filter)] = handler

    async def _send_request(
            self,
            path: str,
            request: DataType,
            response_type: Optional[DataTypeArgument] = None,
            session_id: Optional[SessionId] = None,
    ) -> Optional[DataType]:
        """Common functionality to send a request to one or more sessions.

        Args:
            path: The path to send a request to.
            request: The request to be sent, wrapped into the required `DataType` class.
            response_type: The type to convert the response to. If omitted, it will be
                           the same as the `request`'s data type.
            session_id: If specified, the request will only be sent to the session with
                        that ID. If omitted, the server will forward the request to one
                        of the sessions registered as handlers for the given `path`.

        Returns:
            The response value of the provided `response_type`.
        """
        from diffusion.internal.serialisers.specific.messaging import (
            MessagingSend,
            MessagingReceiverServer,
        )

        if session_id is not None:
            response = await self.services.MESSAGING_RECEIVER_SERVER.invoke(
                self.session, MessagingReceiverServer(path, request, session_id)
            )
        else:
            response = await self.services.MESSAGING_SEND.invoke(
                self.session, MessagingSend(path, request)
            )
        if response is None:
            return None
        if response_type is None:
            response_type_final = type(request)
        else:
            response_type_final = dt._get_impl(response_type)
        if response.serialised_value:
            if response.serialised_value.type_name != response_type_final.type_name:
                raise dt.InvalidDataError
            return response_type_final.from_bytes(response.serialised_value.to_bytes())  # type: ignore
        return None

    async def send_request_to_path(
        self,
        path: str,
        request: DataType,
        response_type: Optional[DataTypeArgument] = None,
    ) -> Optional[DataType]:
        """Send a request to sessions based on a path.

        Args:
            path: The path to send a request to.
            request: The request to be sent, wrapped into the required `DataType` class.
            response_type: The type to convert the response to. If omitted, it will be
                           the same as the `request`'s data type.

        Returns:
            The response value of the provided `response_type`.
        """
        return await self._send_request(path=path, request=request, response_type=response_type)

    async def add_request_handler(
        self,
        path: str,
        handler: RequestHandler,
        session_properties: Collection[str] = (),
    ) -> None:
        """Register the session as the handler for requests to a given path.

        This method is used to inform the server that any unaddressed requests to the
        given path should be forwarded to the active session. The handler to
        these requests is added at the same time, using `add_stream_handler` internally.

        Args:
            path: The handler will respond to the requests to this path.
            handler: A callable to handle the request.
            session_properties: A list of keys of session properties that should be
                                supplied with each request. To request all fixed
                                properties include `ALL_FIXED_PROPERTIES` as a key; any
                                other fixed property keys will be ignored. To request
                                all user properties include `ALL_USER_PROPERTIES` as a
                                key; any other user properties will be ignored.
        """
        from diffusion.internal.serialisers.specific.messaging import (
            MessagingReceiverControlRegistration,
        )
        self.add_stream_handler(path, handler)

        return await self.services.MESSAGING_RECEIVER_CONTROL_REGISTRATION.invoke(
            self.session,
            MessagingReceiverControlRegistration(
                self.services.MESSAGING_RECEIVER_CLIENT.service_id,
                control_group=typing.cast(StrictStr, ""),
                path=typing.cast(StrictStr, path),
                session_properties=session_properties,
            ),
        )

    async def send_request_to_filter(
        self,
        session_filter: StrictStr,
        path: StrictStr,
        request: DataType,
    ) -> int:
        """Send a request to other sessions, specified by the filter.

        Args:
            session_filter: A session filtering query.
            path: The path to send a request to.
            request: The request to be sent, wrapped into the required `DataType` class.

        Returns:
            The number of sessions that correspond to the filter, which is the number of
                responses that can be expected. When each of the responses is received, the
                handler registered for the filter will be executed.
        """
        from diffusion.internal.serialisers.specific.messaging import (
            MessagingClientFilterSendRequest,
            MessagingClientFilterSendResult, Count
        )

        raw_result = (
            await self.services.MESSAGING_FILTER_SENDER.invoke(
                self.session,
                request=MessagingClientFilterSendRequest(
                    session_filter, path, request
                ),
                response_type=MessagingClientFilterSendResult,
            )
        )
        # the other possibility raises an exception
        assert isinstance(raw_result.content, Count)
        return raw_result.content.count


    async def send_request_to_session(
        self,
        path: str,
        session_id: SessionId,
        request: DataType,
        response_type: Optional[DataTypeArgument] = None,
    ) -> Optional[DataType]:
        """Send a request to a single session.

        Args:
            path: The path to send a request to.
            session_id: The ID of the session to send the request to.
            request: The request to be sent, wrapped into the required `DataType` class.
            response_type: The type to convert the response to. If omitted, it will be
                           the same as the `request`'s data type.

        Returns:
            The response value of the provided `response_type`.
        """
        return await self._send_request(
            path=path, request=request, response_type=response_type, session_id=session_id
        )



class RequestHandler(
    Handler,
    Generic[
        J_In_contra,
        J_Out_contra,
        TypeCode_In,
        TypeName_In,
        TypeCode_Out,
        TypeName_Out,
    ],
):
    """
    Class which specifies a request handler to receive request notifications.
    """

    callback: Callback[J_In_contra, typing_extensions.Awaitable[J_Out_contra]]
    request_type: Type[
        ValueTypeProtocolWithCodeAndName[J_In_contra, TypeCode_In, TypeName_In]
    ]
    response_type: Type[
        ValueTypeProtocolWithCodeAndName[
            J_Out_contra, TypeCode_Out, TypeName_Out
        ]
    ]

    def __init__(
        self,
        callback: typing.Union[
            Callback[J_In_contra, typing_extensions.Awaitable[J_Out_contra]],
            Callback[J_In_contra, J_Out_contra],
        ],
        request_type: typing.Union[
            TypeName_In,
            TypeCode_In,
            Type[IBytes[Any, Any, J_In_contra]],
            Type[HasRawTypes[J_In_contra]],
            TopicSpecification[IBytes[Any, Any, J_In_contra]],
            TopicSpecification[ValueTypeProtocolSpecific[J_In_contra]],
        ],
        response_type: typing.Union[
            TypeName_Out,
            TypeCode_Out,
            Type[IBytes[Any, Any, J_Out_contra]],
            Type[HasRawTypesOrMore[J_Out_contra]],
            TopicSpecification[IBytes[Any, Any, J_Out_contra]],
            TopicSpecification[ValueTypeProtocolSpecificOrMore[J_Out_contra]],
        ],
    ) -> None:
        """
        Initialise the RequestHandler.

        Args:
            callback: the callback to call with the raw value of the request
            request_type: the Diffusion datatype of the request
            response_type: the Diffusion datatype of the response
        """
        self.__init_real__(
            callback, request_type=request_type, response_type=response_type
        )

    async def handle(
        self, event: str = "request", **kwargs
    ) -> ValueTypeProtocolWithCodeAndName[J_Out_contra, TypeCode_Out, TypeName_Out]:
        """Execute the callback."""
        request: ValueTypeProtocolWithCodeAndName[
            J_In_contra, TypeCode_In, TypeName_In
        ] = kwargs.pop("request")
        if not isinstance(request, self.request_type):
            raise dt.IncompatibleDatatypeError(
                "Incompatible request data type: "
                f"required: {self.request_type.__name__}; \
                submitted: {type(request).__name__}"
            )
        response_raw = await self.callback(request.value, **kwargs)
        try:
            response = self.response_type(response_raw)
            assert isinstance(response, DataType)
        except dt.DataTypeError as ex:
            error_message = self._get_response_error(
                response_raw, request, **kwargs
            )
            raise dt.IncompatibleDatatypeError(error_message) from ex
        return response


    def _get_response_error(
        self,
        response_raw: typing.Any,
        request: ValueTypeProtocolWithCodeAndName[
            J_In_contra, TypeCode_In, TypeName_In
        ],
        **kwargs,
    ) -> str:
        return (
            f"{self}: {self._get_function_desc(request, **kwargs)} returned "
            f"{repr(response_raw)}: This could not be materialised into the response type "
            f"'{self._get_type_name(self.response_type)}'"
        )


    def _get_function_desc(
        self,
        request: ValueTypeProtocolWithCodeAndName[
            J_In_contra, TypeCode_In, TypeName_In
        ],
        function: typing.Optional[typing.Callable] = None,
        **kwargs,
    ):
        function = function or self.callback
        function_name = getattr(
            function,
            "__qualname__",
            getattr(function, "__name__", repr(function)),
        )
        extra_args = f", **{kwargs}" if kwargs else ""
        function_desc = f"({function_name})({repr(request.value)}{extra_args})"
        return function_desc

    @staticmethod
    def _get_type_name(
        response_type: typing.Type[
            ValueTypeProtocolWithCodeAndName[J_Out_contra, TypeCode_Out, TypeName_Out]
        ],
    ):
        return getattr(
            response_type,
            "__qualname__",
            getattr(response_type, "__name__", repr(response_type)),
        )

    def __init_real__(
        self,
        callback: Any,
        request_type: Any,
        response_type: Any,
    ) -> RequestHandler[
        J_In_contra,
        J_Out_contra,
        TypeCode_In,
        TypeName_In,
        TypeCode_Out,
        TypeName_Out
    ]:
        req_t = dt.get(request_type)
        assert issubclass(req_t, IBytes)
        self.request_type = typing.cast(
            Type[ValueTypeProtocolWithCodeAndName[J_In_contra, Any, Any]], req_t
        )
        res_t = dt.get(response_type)
        assert issubclass(res_t, IBytes)
        self.response_type = typing.cast(
            Type[ValueTypeProtocolWithCodeAndName[J_Out_contra, TypeCode_Out, TypeName_Out]],
            res_t,
        )
        self.callback = utils.coroutine(callback)
        return typing.cast(
            RequestHandler[
                J_In_contra,
                J_Out_contra,
                TypeCode_In,
                TypeName_In,
                TypeCode_Out,
                TypeName_Out,
            ],
            self,
        )


class MessagingError(DiffusionError):
    """ The generic messaging error. """

class InvalidFilterError(SessionError):
    """
    The exception used to report a filter expression is invalid.
    """

    default_description = "{message}: {reports}"

    def __init__(self, message: str, reports: typing.List[ErrorReport]):
        self.reports = reports
        super(InvalidFilterError, self).__init__(message, reports=reports)

class InvalidFilterMessagingError(MessagingError, InvalidFilterError):
    def __init__(self, message: str, reports: typing.List[ErrorReport]):
        MessagingError.__init__(self, message, reports=reports)
        InvalidFilterError.__init__(self, message, reports)
