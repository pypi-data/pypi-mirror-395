#  Copyright (c) 2024 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

from __future__ import annotations

import ssl
import typing
import dataclasses

from diffusion.internal.validation.pydantic import MaximumResultSize

from urllib.parse import urlparse

from diffusion.internal.pydantic_compat import v1

if typing.TYPE_CHECKING:
    from diffusion.session import RetryStrategy


from diffusion.internal.encoded_data import Int32


def _no_retry_strategy():
    from diffusion.session.retry_strategy import RetryStrategy
    return RetryStrategy.no_retry()


class Endpoint(v1.StrictStr):
    pass


class Authentication(v1.StrictStr):
    pass


class ReconnectionStrategy(v1.StrictStr):
    pass


# noinspection PyMethodMayBeStatic
@dataclasses.dataclass(frozen=True)
class SessionAttributes(object):
    """
    The attributes of a [Session][diffusion.session.Session].

    Notes:
        These attributes will be set by
        [SessionFactory][diffusion.session.session_factory.SessionFactory].
        This interface does not require user implementation
        and is only used to hide implementation details.

    Notes:
        Added in 6.11
    """

    DEFAULT_MAXIMUM_MESSAGE_SIZE: typing.ClassVar[MaximumResultSize] = typing.cast(
        MaximumResultSize, Int32.max_signed_int())
    """
    The default maximum message size in bytes. The maximum message size
    limits the size of received messages. This default value is
    is [Int32.max_signed_int][diffusion.internal.validation.pydantic.Int32.max_signed_int],
    so the message size is effectively
    unlimited.

    Notes:
        Since: 6.11
    """

    initial_retry_strategy: RetryStrategy = dataclasses.field(
        default_factory=_no_retry_strategy)
    """
    Returns the initial retry strategy.

    See Also:
        [SessionFactory.initial_retry_strategy]
        [diffusion.session.session_factory.SessionFactory.initial_retry_strategy]

    Returns:
         the initial retry strategy used by the session

    Since:
        6.9
    """

    ssl_context: typing.Optional[ssl.SSLContext] = None
    """
    The SSL context for secure connections.
    Returns the SSL context for secure connections.

    See Also:
        [SessionFactory.ssl_context]
        [diffusion.session.session_factory.SessionFactory.ssl_context]

    Returns:
        the SSL context

    Since:
        6.11
    """  # NOQA: E501

    maximum_message_size: MaximumResultSize = DEFAULT_MAXIMUM_MESSAGE_SIZE
    """
    Returns the maximum message size that will be accepted by this session.

    See Also:
        SessionFactory#maximumMessageSize(int)

    Returns:
        the maximum message size

    Since:
        6.11
    """

    server_host: str = "localhost"
    """
    Returns the host name or IP of the server the session will connect to.

    See Also:
        [SessionFactory.server_host]
        [diffusion.session.session_factory.SessionFactory.server_host]

    Returns:
        the host name (or IP address)

    Since:
        6.9
    """

    def with_host(self,
                  host: v1.StrictStr) -> SessionAttributes:
        return SessionAttributes(server_host=host, **self._without_host_or_url())

    def _without_host_or_url(self):
        return {field.name: getattr(self, field.name) for field in dataclasses.fields(self) if
                field.name not in {'server_host', "_server_url"}}

    server_port: int = 8080
    """
    Returns the port of the server the session will connect to.

    See Also:
        [SessionFactory.server_port]
        [diffusion.session.session_factory.SessionFactory.server_port]

    Returns:
        the port

    Since:
        6.9
    """

    _server_url: typing.Optional[str] = None

    @property
    def server_url(self) -> str:
        """
        Returns the URL used to create the session.

        Returns:
             the URL
        """
        return self._server_url or (
            f"{'wss' if self.secure_transport else 'ws'}"
            f"://{self.server_host}:"
            f"{self.server_port}"
        )

    def with_url(self,
                 url: v1.StrictStr) -> SessionAttributes:
        try:
            parsed_host = urlparse(url).hostname
            if not isinstance(parsed_host, str):
                raise ValueError(f"Null/empty host value {parsed_host}")
        except ValueError as e:
            raise ValueError("Invalid url") from e

        return SessionAttributes(_server_url=url, server_host=parsed_host,
                                 **self._without_host_or_url())

    secure_transport: typing.Optional[bool] = None
    """
    Indicates whether the session will use transport layer security to
    connect to Diffusion.

    See Also:
        SessionFactory#secureTransport(boolean)

    Returns:
        if the session will use TLS

    Since:
        6.11
    """
