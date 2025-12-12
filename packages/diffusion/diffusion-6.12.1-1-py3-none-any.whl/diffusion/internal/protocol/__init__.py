#  Copyright (c) 2020 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

""" Implementation of Diffusion communications protocol. """

from __future__ import annotations

import enum
import io
import struct
import ctypes
import typing
from typing import Dict, TYPE_CHECKING
from urllib.parse import urljoin

import attr
import structlog

from .exceptions import (
    AbortMessageError,
    ProtocolError,
    ServerConnectionError,
    ServerConnectionResponseError,
)
from .message_types import read_stream, ServiceRequestMessage
from .properties import Transform

if TYPE_CHECKING:  # pragma: no cover
    from diffusion.internal.session import InternalSession

LOG = structlog.get_logger()


class Protocol:
    """ Diffusion protocol implementation. """

    PROTOCOL_BYTE: int = ord("#")
    VERSION = 25

    @classmethod
    def parse_response(cls, response: bytes) -> ConnectionResponse:
        """ Parse the connection response from the server. """
        response_code = cls._parse_response_header(response)
        if response_code is not ResponseCode.OK:
            raise ServerConnectionResponseError(response_code)
        session_id = SessionId.from_binary(response[3:19])
        token = SessionToken(response[19:43])
        ping_period, maximum_message_size, *_ = struct.unpack(">QL", response[43:])
        return ConnectionResponse(
            response_code, session_id, token, ping_period, maximum_message_size
        )

    @classmethod
    async def listen(cls, session: InternalSession, data: bytes) -> None:
        """ Listen and respond to messages from server. """
        await read_stream(io.BytesIO(data), session)

    @classmethod
    def _parse_response_header(cls, response: bytes) -> ResponseCode:
        protocol_byte, protocol_version, response_code_byte = struct.unpack(
            ">BBB", response[:3]
        )
        if protocol_byte != cls.PROTOCOL_BYTE:
            raise ProtocolError(f"Unexpected protocol byte: {protocol_byte}")
        if protocol_version != cls.VERSION:
            raise ProtocolError(
                f"Unexpected server protocol version: {protocol_version}: "
                f"Client version: {cls.VERSION}. "
                "Client should be downgraded to use server compatible "
                "version, or server upgraded to client version in use.")
        return ResponseCode(response_code_byte)

    @classmethod
    async def prepare_request(cls, conversation) -> bytes:
        """ Prepare request message. """
        return await ServiceRequestMessage.prepare(
            cid=conversation.cid, service=conversation.service
        )


@attr.s(auto_attribs=True, eq=True, frozen=True)
class SessionId:
    """Session ID as assigned by the server.

    Consists of the server identifier and the client session identifier.
    """

    server: int
    value: int

    def __attrs_post_init__(self):
        object.__setattr__(self, 'server', ctypes.c_uint64(self.server).value)
        object.__setattr__(self, 'value', ctypes.c_uint64(self.value).value)

    def __str__(self):
        return f"{self.server:016x}-{self.value:016x}"

    def __iter__(self):
        yield self.server
        yield self.value

    @classmethod
    def from_binary(cls, binary_session_id):
        """ Create a new session ID from a binary representation. """
        session_id_server, session_id_value = struct.unpack(">QQ", binary_session_id)
        return cls(session_id_server, session_id_value)


class SessionToken(bytes):
    """Server-allocated session token.

    The session token is a fixed value, allocated by the server from a secure
    random source.

    In contrast to the public `session_id`, a session token is only exchanged
    with the client that owns the session. It is supplied by polling transports
    and during reconnection to identify a session.

    ### Security

    Knowledge of the token value is sufficient to gain access to the session.

      * It should be treated as private to the client session, and protected
        accordingly - e.g. by using TLS where there is a danger of network sniffing.
      * It is currently not logged anywhere.
      * It is currently not made available through client APIs.
    """

    def __str__(self):
        return self.decode("ascii")

    def __repr__(self):
        return str(self)


@enum.unique
class ResponseCode(enum.Enum):
    """ Connection response codes. """

    OK = 100
    DOWNGRADE = 102
    RECONNECTED = 105
    RECONNECTED_WITH_MESSAGE_LOSS = 106
    REJECTED = 111  # Unexpected, protocol 4 only
    LICENSE_EXCEEDED = 113
    RECONNECTION_UNSUPPORTED = 114
    CONNECTION_PROTOCOL_ERROR = 115
    AUTHENTICATION_FAILED = 116
    UNKNOWN_SESSION = 117
    RECONNECTION_FAILED_MESSAGE_LOSS = 118


def _url_converter(url: str) -> str:
    """ Converter for url; completes the base diffusion server name. """
    return urljoin(base=url, url="diffusion")


class Capabilities(enum.IntFlag):
    NONE = 0
    ZLIB = 0b0010
    UNIFIED = 0b1000


@attr.s
class ConnectionParams:
    """ All the settable connection parameters. """

    HEADER_KEY = "__header_key"
    CLIENT_TYPE = "PY"

    url = attr.ib(type=str, converter=_url_converter)
    version = attr.ib(type=int, metadata={HEADER_KEY: "v"})
    session_token = attr.ib(type=SessionToken, default=None, metadata={HEADER_KEY: "c"})
    capabilities = attr.ib(type=int, default=0, metadata={HEADER_KEY: "ca"})
    principal = attr.ib(type=str, default="", metadata={HEADER_KEY: "username"})
    reconnect_timeout = attr.ib(
        type=int, default=Capabilities.NONE.value, metadata={HEADER_KEY: "r"}
    )
    password = attr.ib(type=str, default=None, metadata={HEADER_KEY: "password"})
    available_client_sequence = attr.ib(type=int, default=None, metadata={HEADER_KEY: "cs"})
    last_server_sequence = attr.ib(type=int, default=None, metadata={HEADER_KEY: "ss"})
    type = attr.ib(type=str, default=CLIENT_TYPE, metadata={HEADER_KEY: "ty"})
    session_properties = attr.ib(
        type=typing.Mapping[str, str], default=None, metadata={HEADER_KEY: "sp"}
    )
    server_name = attr.ib(type=str, default=None, metadata={HEADER_KEY: "svn"})

    @classmethod
    def serialise(cls, field, value):
        """ Convert a field value to string. """
        if field.name == "session_properties":
            return Transform.map_to_string(value)
        return str(value)

    @property
    def headers(self):
        """ Extract connection params ready to be inserted into HTTP headers. """
        fields = attr.fields_dict(type(self))
        exclude = attr.filters.exclude(fields["url"])
        return {
            fields[key].metadata[self.HEADER_KEY]: self.serialise(fields[key], value)
            for key, value in attr.asdict(self, filter=exclude).items()
            if value is not None
        }


@attr.s(frozen=True, auto_attribs=True, repr=False)
class ConnectionResponse:
    """ Details about a connection. """

    response_code: ResponseCode
    session_id: SessionId
    token: SessionToken
    ping_period: int
    maximum_message_size: int

    def __repr__(self):
        values = (
            "=".join((key, str(value))) for key, value in vars(self).items() if key != "token"
        )
        return f"<{type(self).__name__} {' '.join(values)}>"
