#  Copyright (c) 2020 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

""" Module implementing low-level connection to the server. """

from __future__ import annotations

import abc
import collections
import dataclasses
import functools
import ssl
import typing
from enum import Enum, unique
from typing import Dict, Optional

import aiohttp
import structlog
from aiohttp.connector import SSLContext

from diffusion.internal import protocol
from .credentials import Credentials
from ..protocol.exceptions import ServerDisconnectedError
from diffusion.session.session_attributes import SessionAttributes

if typing.TYPE_CHECKING:
    from . import InternalSessionListener, InternalSession

LOG = structlog.get_logger()


@dataclasses.dataclass(frozen=True)
class StateInfo(object):
    description: str
    connected: bool
    recovering: bool
    closed: bool


@unique
class State(Enum):
    """ Connection state. """

    CONNECTING = StateInfo(
        "The session is establishing its initial connection.", False, False, False
    )
    CONNECTED_ACTIVE = StateInfo(
        "An active connection with the server has been established.",
        True,
        False,
        False,
    )
    RECOVERING_RECONNECT = StateInfo(
        "Connection with server has been lost and the session is attempting reconnection.",
        False,
        True,
        False,
    )
    CLOSED_BY_CLIENT = StateInfo(
        "The session has been closed by the client.", False, False, True
    )
    CLOSED_BY_SERVER = StateInfo(
        "The session has been closed (or rejected) by the server.", False, False, True
    )
    CLOSED_FAILED = StateInfo(
        "The session has lost its connection to a server and could not be recovered.",
        False,
        False,
        True,
    )

    def __getattr__(self, item):
        if item in {x.name for x in dataclasses.fields(StateInfo)}:
            return getattr(self.value, item)
        return super().__getattribute__(item)


class AbstractConnection(abc.ABC):
    def __init__(
        self,
        principal: str,
        credentials: Credentials,
        parent: typing.Optional[InternalSession] = None,
        listeners: Optional[typing.Counter[InternalSessionListener]] = None,
    ):
        self.credentials = credentials
        self.protocol = protocol.Protocol
        self.principal = principal
        self.state: State = State.CONNECTING
        self.listeners: typing.Counter[InternalSessionListener] = (
            listeners or collections.Counter()
        )
        self.parent = parent
        self.response: Optional[protocol.ConnectionResponse] = None

    async def update_state(self, new_state: State):
        old_state = self.state
        self.state = new_state
        if old_state != new_state:
            await self.on_state_changed(old_state, new_state)

    def add_listener(self, listener: InternalSessionListener):
        self.listeners[listener] += 1

    def remove_listener(self, listener: InternalSessionListener):
        self.listeners[listener] -= 1
        if not self.listeners[listener]:
            del self.listeners[listener]

    async def on_state_changed(self, old_state: typing.Optional[State], new_state: State):
        assert self.parent
        for listener in self.listeners.elements():
            await listener.on_session_event(
                session=self.parent, new_state=new_state, old_state=old_state
            )

    @property
    def is_connected(self):
        """ Checks the connection status. """
        return self.state.connected

    @property
    def is_reconnecting(self):
        """ Checks whether the connection is in process of reconnection. """
        return self.state.reconnecting

    @property
    def is_closed(self):
        """ Checks whether the connection is closed. """
        return self.state.closed

    @abc.abstractmethod
    async def _socket_safe_connect(self, properties: typing.Mapping[str, typing.Any]): ...

    @abc.abstractmethod
    async def _socket_close(self): ...

    # TODO: implement reconnection (FB23157)
    async def connect(self, properties: Optional[Dict[str, str]] = None) -> None:
        """ Establishes a connection with the server. """
        if self.state.value.connected or self.state.value.recovering:
            raise protocol.ServerConnectionError(f"Already connecting with state {self.state}")
        if properties is None:
            properties = {}
        if self.response:
            await self.update_state(State.RECOVERING_RECONNECT)
        else:
            await self.update_state(State.CONNECTING)

        await self._socket_safe_connect(properties)
        try:
            await self._parse_response()
        except protocol.ProtocolError:
            await self.close()
            raise
        else:
            await self.update_state(State.CONNECTED_ACTIVE)
            LOG.debug("Connected.", info=self.response)

    async def _parse_response(self):
        data = await self._receive_data()
        self.response = self.protocol.parse_response(data)

    async def close(self, state=State.CLOSED_BY_CLIENT):
        """ Close the connection. """
        await self._socket_close()
        await self.update_state(state)
        self.response = None
        LOG.debug("Connection closed.", info=self.response)

    @abc.abstractmethod
    def _socket_get_data_chunks(self) -> typing.AsyncIterable[bytes]:
        pass  # pragma: no cover

    async def read_loop(self, session):
        """ Read the incoming messages and react to them. """
        async for data in self._socket_get_data_chunks():
            LOG.debug("Received bytes.", bytes=data)
            try:
                await self.protocol.listen(session, data)
            except protocol.AbortMessageError:
                LOG.error("Connection aborted by server.", server_bytes=data)
                await self.close(State.CLOSED_BY_SERVER)
                break
            except Exception as ex:
                LOG.exception(
                    f"Error occurred on data receive: {ex}.",
                    data=data,
                    error=ex,
                    exc_info=True
                )

    @abc.abstractmethod
    async def _socket_send(self, data: bytes):
        pass  # pragma: no cover

    @abc.abstractmethod
    async def _receive_data(self) -> bytes:
        pass  # pragma: no cover

    async def send(self, data: bytes) -> None:
        """ Send bytes to the server. """
        LOG.debug("Sending bytes.", bytes=data)
        if not self.is_connected:
            raise ServerDisconnectedError()
        await self._socket_send(data)


class Connection(AbstractConnection):
    """Connection to the server."""

    def __init__(
        self,
        url: str,
        principal: str,
        credentials: Credentials,
        parent: typing.Optional[InternalSession] = None,
        listeners: typing.Optional[typing.Counter[InternalSessionListener]] = None,
        session_attributes: typing.Optional[SessionAttributes] = None
    ):
        session_attributes = session_attributes or SessionAttributes()
        super().__init__(principal, credentials, parent=parent, listeners=listeners)
        self.url = url
        self._ws: Optional[aiohttp.ClientWebSocketResponse] = None
        self._ssl_context = session_attributes.ssl_context or SSLContext(
            protocol=ssl.PROTOCOL_TLS
        )

    @functools.cached_property
    def _client(self):
        return aiohttp.ClientSession()

    async def _receive_data(self) -> bytes:
        response = await typing.cast(aiohttp.ClientWebSocketResponse, self._ws).receive()
        return response.data

    async def _socket_safe_connect(self, properties: typing.Mapping[str, typing.Any]):
        try:
            capabilities: protocol.Capabilities = (
                    protocol.Capabilities.ZLIB
                    | protocol.Capabilities.UNIFIED
            )

            params = protocol.ConnectionParams(
                version=self.protocol.VERSION,
                url=self.url,
                principal=self.principal,
                password=self.credentials.password,
                session_properties=properties,
                capabilities=capabilities.value,
            )
            LOG.debug("Connecting.", url=params.url, headers=params.headers)
            self._ws = await self._client.ws_connect(
                url=params.url, headers=params.headers, ssl=self._ssl_context
            )
        except aiohttp.ClientError as ex:
            LOG.warning("Connection error! Is the server online?", error=ex)
            raise protocol.ServerConnectionError(
                "The session failed to be established. No further operations are possible"
            ) from ex

    async def _socket_send(self, data: bytes):
        await self._ws.send_bytes(data)  # type: ignore

    def _socket_get_data_chunks(self) -> typing.AsyncIterable[bytes]:
        async def iterable() -> typing.AsyncIterable[bytes]:
            assert self._ws
            async for msg in self._ws:
                if msg.type in (aiohttp.WSMsgType.BINARY, aiohttp.WSMsgType.TEXT):
                    yield msg.data.encode() if msg.type == aiohttp.WSMsgType.TEXT else msg.data
        return iterable()

    async def _socket_close(self):
        if self._ws:
            await self._ws.close()
        await self._client.close()
