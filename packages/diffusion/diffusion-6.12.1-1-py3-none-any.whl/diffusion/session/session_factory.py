#  Copyright (c) 2022 - 2024 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

from __future__ import annotations

import asyncio
import dataclasses
import functools
import typing
from ssl import SSLContext

import attr
import diffusion.internal.pydantic_compat.v1
from typing_extensions import TypeAlias

from diffusion.internal.protocol import ServerConnectionError
from attr import evolve
from typing import Optional

from diffusion.session.session_attributes import SessionAttributes
from diffusion.internal.validation.pydantic import MaximumResultSize

if typing.TYPE_CHECKING:
    from diffusion import Session, Credentials
from diffusion import DiffusionError
from diffusion.session.retry_strategy import RetryStrategy
from diffusion.session.session_container_factory import SessionContainerFactory
from diffusion.handlers import LOG


class SessionEstablishmentException(DiffusionError):  # NOQA: N818
    """
    Session establishment error
    """


SessionProperties: TypeAlias = typing.Mapping[str, typing.Any]
"""
Mapping of session properties
"""


@attr.s(auto_attribs=True, frozen=True)
class SessionDetails(object):
    properties: SessionProperties = {}
    principal: typing.Optional[str] = ""
    credentials: typing.Optional[Credentials] = None


@dataclasses.dataclass
class Connector(object):
    """
    Connector object.

    This can be awaited to return a connected session,
    or used as an asynchronous context manager that provides
    a connected session on entry and closes it on exit.
    This is used by the SessionFactory and is not designed for manual creation.
    """

    session_details: SessionDetails
    """
    The session details involved
    """

    container_factory: SessionContainerFactory
    """
    The factory responsible for building the session and connecting it
    """

    url: typing.Optional[str]
    """
    The URL to be connected to. If not present the session details will be used instead.
    """
    session_attributes: SessionAttributes

    def __init__(
        self,
        session_details: SessionDetails,
        container_factory: SessionContainerFactory,
        session_attributes: SessionAttributes
    ):
        """
        This is used by the SessionFactory and is not designed for manual creation.

        Args:
            session_details: the session details involved
            container_factory: responsible for building the session and connecting it
            session_attributes: the Session Attributes to use
        """
        self.session_details = session_details
        self.container_factory = container_factory
        self.session_attributes = session_attributes
        self.url = session_attributes.server_url

    async def __aenter__(self) -> Session:
        self.session = await self()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    def __await__(self) -> typing.Generator[typing.Any, None, Session]:
        return self().__await__()

    async def __call__(self) -> Session:
        attempts = 0
        retry_attempts_allowed = self.session_attributes.initial_retry_strategy.attempts or 0

        while True:
            try:
                LOG.info(f"Attempt {attempts} to connect session")
                session: Session = await self.container_factory.start_session(
                    self.url,
                    principal=self.session_details.principal,
                    credentials=self.session_details.credentials,
                    session_properties=self.session_details.properties,
                    session_attributes=self.session_attributes
                )
                return session
            except ServerConnectionError as e:
                if attempts < retry_attempts_allowed:
                    attempts += 1
                    # we could use something like the following instead of asyncio.sleep, but
                    # the increased precision of run_on_executor doesn't seem to be
                    # documented anywhere.
                    # https://textual.textualize.io/blog/2022/12/30/a-better-asyncio-sleep-for-windows-to-fix-animation/
                    # see also: tests.unit.conftest.PreciseTimeEventLoopPolicy
                    await asyncio.sleep(self.session_attributes.initial_retry_strategy.interval)
                    continue
                elif retry_attempts_allowed:
                    raise SessionEstablishmentException(
                        f"Failed to establish session after retrying "
                        f"{attempts} times at an interval of "
                        f"{self.session_attributes.initial_retry_strategy.interval} seconds"
                    ) from e
                else:
                    raise


class SessionFactory(object):
    """
    Factory for client [diffusion.session.Session][].

    Each instance is immutable, and has a number of session attributes that
    determine how sessions should be established. An initial instance of this
    factory with default values for all attributes can be obtained from
    diffusion.sessions(). Each method returns a copy of this factory, with a
    single changed attribute.

    # Establishing a session

    A new session can be created using
    [open][diffusion.session.session_factory.SessionFactory.open] specifying a
    URL that identifies the server. This returns an async context manager,
    which will provide the connected Session object.

    The server is identified by the
    [diffusion.session.session_factory.SessionFactory.server_host][] and
    [diffusion.session.session_factory.SessionFactory.server_port][]
    attributes.

    If a URL is specified, it takes precedence over the
    [diffusion.session.session_factory.SessionFactory.server_host][] and
    [diffusion.session.session_factory.SessionFactory.server_port][]
    session factory attributes.

    # URL format

    URLs should take the form <em>scheme://host:port</em>, where <em>scheme</em>
    is chosen from the following table and determines the transport protocol used
    to send Diffusion messages.

    | Scheme       | Transport Protocol                                            |
    |--------------|---------------------------------------------------------------|
    | `ws`         | WebSocket. See https://tools.ietf.org/html/rfc6455            |
    | `wss`        | WebSocket over TLS.                                           |

    We recommend using the WebSocket protocol options `ws` or
    `wss`.

    TLS is <em>Transport Layer Security</em>, commonly known as SSL. TLS-based
    protocols use cryptography to provide transport-level privacy,
    authentication, and integrity, and protects against network-sniffing and
    man-in-the-middle attacks. We recommend using the TLS variants for all
    communication. For a typical application, you should only consider
    <em>not</em> using TLS for unauthenticated ("anonymous") client sessions.

    Since:
        6.9
    """

    def __init__(
        self,
        factory: Optional[SessionContainerFactory] = None,
        details: Optional[SessionDetails] = None,
        session_attributes: Optional[SessionAttributes] = None
    ):
        self._target = details or SessionDetails()
        self._attributes = session_attributes or SessionAttributes()
        self.container_factory = factory or SessionContainerFactory()

    def _evolve(
        self,
        updated: SessionDetails,
        session_attributes: typing.Optional[SessionAttributes] = None,
    ) -> SessionFactory:
        return SessionFactory(
            factory=self.container_factory,
            details=updated,
            session_attributes=session_attributes or self._attributes,
        )

    def principal(self, principal: str) -> SessionFactory:
        """
        Sets the security principal.

        By default, this will be [diffusion.session.ANONYMOUS_PRINCIPAL][].

        Args:
            principal: the principal

        Returns:
            a new immutable instance of the factory with the principal changed
        """
        return self._evolve(evolve(self._target, principal=principal))

    def credentials(self, credentials: Credentials) -> SessionFactory:
        """
        Set credentials.

        The default is `None`.

        Args:
            credentials: the credentials

        Returns:
            a new immutable instance of the factory with the credentials changed

        """
        return self._evolve(evolve(self._target, credentials=credentials))

    def initial_retry_strategy(self, strategy: RetryStrategy) -> SessionFactory:
        """
        Sets the initial retry strategy.

        The strategy will determine whether a failure to open a session due to a
        ServerConnectionError should be retried and if
        so, at what interval and for how many attempts.

        If no initial retry strategy is set there will be no attempt to retry
        after such a failure.

        Args:
            strategy: strategy the retry strategy to use

        Returns:
            a new immutable instance of the factory with the initial retry strategy changed

        Since:
            6.9
        """
        return self._evolve(self._target, dataclasses.replace(self._attributes,
                                                              initial_retry_strategy=strategy))

    def secure_transport(self, secure_transport: bool) -> SessionFactory:
        """
        Sets whether to use secure transport or not
        If not explicitly supplied, secure transport will not be used.

        Args:
            secure_transport: whether to use secure transport

        Returns:
            a new immutable instance of the factory with the secure transport flag changed

        Since:
            6.11
        """
        return self._evolve(
            self._target,
            session_attributes=dataclasses.replace(
                self._attributes, secure_transport=secure_transport
            ),
        )

    def maximum_message_size(self, size_in_bytes: MaximumResultSize) -> SessionFactory:
        """

        Sets the maximum message size.

        This constrains the size of messages that will be accepted from the server
        and thus the size of any content that can be received.
        The limit is simply to protect against unexpectedly large messages.

        The given `size_in_bytes` must not be less than
        SessionAttributes.MAXIMUM_MESSAGE_SIZE_MIN.

        By default,
        the size of received messages is unconstrained;
        see
        [SessionAttributes.DEFAULT_MAXIMUM_MESSAGE_SIZE]
        [diffusion.session.session_attributes.SessionAttributes.DEFAULT_MAXIMUM_MESSAGE_SIZE]

        Notes:
            Added in 6.11

        Args:
            size_in_bytes: The maximum message size in bytes.
        Returns:
            A new immutable instance of this factory
        with the maximum message size changed.

        Raises:
            ValueError: size_in_bytes is not a positive integer between
                SessionAttributes.MAXIMUM_MESSAGE_SIZE_MIN and
                SessionAttributes.DEFAULT_MAXIMUM_MESSAGE_SIZE.

        Examples:

        Setting the maximum message size to 10 MiB.

        ```pycon
        >>> factory = diffusion.sessions().maximum_message_size(10000000)
        ```

        """
        return self._evolve(
            self._target,
            session_attributes=dataclasses.replace(
                self._attributes, maximum_message_size=size_in_bytes
            ),
        )

    def ssl_context(self, context: SSLContext) -> SessionFactory:
        """
        Sets the SSL Context if a secure connection is required.

        If not explicitly supplied, the [ssl.SSLContext(protocol=ssl.PROTOCOL_TLS)][ssl.SSLContext] default
        context will be used.

        Setting the SSL Context will not enable transport layer security. It must
        also be specified by the URL or
        [SessionFactory.secure_transport][diffusion.session.session_factory.SessionFactory.secure_transport].

        Returns:
            a new immutable instance of the factory with the SSL context changed

        Since:
            6.11
        """  # NOQA: E501
        return self._evolve(
            self._target,
            session_attributes=dataclasses.replace(self._attributes, ssl_context=context),
        )

    def server_host(self,
                    host: diffusion.internal.pydantic_compat.v1.StrictStr) -> SessionFactory:
        """
        Set the host name of the server to connect the session to.

        This value is only used if a URL is not provided when opening a session.

        Args:
            host: the host name of the server

        Returns:
            a new immutable instance of the factory that will use the provided host

        Raises:
            IllegalArgumentError: if the specified `host` is invalid
        """
        return self._evolve(self._target, self._attributes.with_host(host))

    def server_port(self, port: int) -> SessionFactory:
        """
        Set the port of the server to connect the session to.

        This value is only used if a URL is not provided when opening a session.
        If the port is not set using this method or a URL, the port will be
        inferred based on the transport and security configuration.

        The provided value must be within the range used for port numbers.

        Args:
            port: the port of the server

        Returns:
            a new immutable instance of the factory that will use the provided port
        Raises:
            IllegalArgumentError: if the specified `port` is invalid
        """
        return self._evolve(self._target,
                            dataclasses.replace(self._attributes, server_port=port))

    def properties(self, properties: SessionProperties) -> SessionFactory:
        """
        Sets user-defined session property values.

        Supplied session properties will be provided to the server when a session
        is created using this session factory. The supplied properties will be
        validated during authentication and may be discarded or changed.

        The specified properties will be added to any existing properties set for
        this session factory. If any of the keys have been previously declared
        then they will be overwritten with the new values.

        For details of how session properties are used see
        [diffusion.session.Session][].

        Args:
            properties: a map of user-defined session properties

        Returns:
            a new immutable instance of the factory with the supplied properties set

        Since:
            6.9
        """
        return self._evolve(evolve(self._target, properties=properties))

    def open(self, url: typing.Optional[str] = None) -> Connector:
        """
        This method returns a
        [diffusion.session.session_factory.Connector][] instance.

        Awaiting this object via `await` will open a connection
        to a server and return a new, connected Session.
        Using it as an async context manager via `async with` wil
        do the same on entry and close this Session on exit.

        It can take a URL to specify the server location,
        ignoring the [diffusion.session.session_factory.SessionFactory.server_host][] and
        [diffusion.session.session_factory.SessionFactory.server_port][]
        session factory attributes.

        Raises:
            IllegalArgumentError: if `url` is invalid

            IllegalStateError: if any of the session
                attributes are found to be inconsistent. For example, if the
                default SSL context could not be loaded

            SessionEstablishmentError: if an initial
                connection could not be established

            AuthenticationError: if the client is
                insufficiently authorized to start the session, based on the
                supplied client credentials.

        Args:
            url: the server location

        Returns:
            A [diffusion.session.session_factory.Connector][] object.

        Since:
            6.9
        """
        final_attributes = self._attributes.with_url(url) if url else self._attributes

        return Connector(
            self._target,
            container_factory=self.container_factory,
            session_attributes=final_attributes
        )


@functools.lru_cache(maxsize=None)
def sessions(
    container_factory: typing.Optional[SessionContainerFactory] = None,
) -> SessionFactory:
    """
    Returns:
        The default session factory.
    """
    return SessionFactory(factory=container_factory)
