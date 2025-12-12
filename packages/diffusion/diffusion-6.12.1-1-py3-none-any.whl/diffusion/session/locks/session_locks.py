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
import traceback
import typing
import weakref

import diffusion.internal.pydantic_compat.v1 as pydantic

from diffusion.handlers import LOG
from diffusion.internal.protocol.conversations import ResponseHandler, ConversationID
from diffusion.internal.services import ServiceValue
from diffusion.internal.utils import validate_member_arguments, BaseConfig
from diffusion.internal.validation import StrictNonNegativeInt
from diffusion.internal.session.locks.session_lock_acquisition import (
    SessionLockAcquisition,
    SessionLockScope,
)
from diffusion.internal.serialisers.primitives import Bool
from diffusion.internal.session.locks.session_lock_request import SessionLockRequest
from diffusion.internal.session.locks.session_lock_request_cancellation import (
    SessionLockRequestCancellation,
)

if typing.TYPE_CHECKING:
    from diffusion.internal.session import InternalSession, State


T = typing.TypeVar("T")


@pydantic.dataclasses.dataclass(frozen=True, config=BaseConfig)
class SessionLock(object):
    """
    A [Session][diffusion.session.Session] lock.

    Notes:
        A session lock is a server-managed resource
        that can be used to coordinate exclusive access
        to shared resources across sessions.
        For example,
        to ensure a single session has the right to update a topic;
        to ensure at most one session responds to an event;
        or to select a single session to perform a housekeeping task.
        Session locks support general collaborative locking schemes.
        The application architect is responsible for
        designing a suitable locking scheme
        and for ensuring each application component
        follows the scheme appropriately.

        Session locks are identified by a lock name.
        Lock names are arbitrary
        and chosen at will to suit the application.
        Each lock is owned by at most one session.
        Locks are established on demand;
        there is no separate operation to create or destroy a lock.

        A session lock is acquired using the
        [Session.lock][diffusion.session.Session.lock] method.
        If no other session owns the lock,
        the server will assign the lock to the calling session immediately.
        Otherwise,
        the server will record that the session is waiting to acquire the lock.
        A session can call
        [Session.lock][diffusion.session.Session.lock]
        more than once for a given session lock
        – if the lock is acquired,
        all calls will complete successfully with equal
        [SessionLock][diffusion.session.locks.session_locks.SessionLock] values.

        If a session closes,
        the session locks it owns are automatically released.
        A session can also release a lock by calling
        [SessionLock.unlock][diffusion.session.locks.session_locks.SessionLock.unlock].
        When a session lock is released
        and other sessions are waiting to acquire the lock,
        the server will arbitrarily select one of the waiting sessions
        and notify it that it has acquired the lock.
        All of the newly selected session's pending
        [Session.lock][diffusion.session.Session.lock]
        calls will complete normally.
        Other sessions will continue to wait.

        The [Session.lock][diffusion.session.Session.lock]
        variant of this method takes a scope parameter
        that provides the further option of automatically releasing the lock
        when the session loses its connection to the server.

        # Race conditions

        This session lock API has inherent race conditions.
        Even if an application is coded correctly
        to protect a shared resource using session locks,
        there may be a period where two
        or more sessions concurrently access the resource.
        The races arise for several reasons including

        - Due to the <i>check-then-act</i>
        approach of polling <see cref="IsOwned"/>,
        the lock can be lost after the check has succeeded
        but before the resource is accessed;

        - The server can detect a session is disconnected
        and assign the lock to another session
        before the original session has detected the disconnection.

        Despite this imprecision,
        session locks provide a useful way to coordinate session actions.

        > NOTE
        > This interface does not require user implementation
        > and is only used to hide implementation details.

        Since:
            6.10
    """

    acquisition: SessionLockAcquisition
    parent: typing.Optional[weakref.ReferenceType] = dataclasses.field(default=None)
    owned: bool = pydantic.dataclasses.Field(init=False)
    lock: asyncio.Lock = pydantic.dataclasses.Field(init=False)

    @property
    def name(self: SessionLock) -> pydantic.StrictStr:
        return self.acquisition.lock_name

    @property
    def sequence(self: SessionLock) -> StrictNonNegativeInt:
        return self.acquisition.sequence

    @property
    def is_owned(self: SessionLock) -> bool:
        return self.owned

    @property
    def scope(self: SessionLock) -> SessionLockScope:
        return self.acquisition.scope

    def __init__(
            self: SessionLock,
            parent: typing.Union[InternalSession, SessionLocks],
            acquisition: SessionLockAcquisition,
    ):
        from diffusion.internal.session import InternalSession

        super().__init__()
        if isinstance(parent, (InternalSession, SessionLocks)):
            object.__setattr__(self, "parent", weakref.ref(parent))
            object.__setattr__(self, "owned", True)
        else:
            object.__setattr__(self, "owned", False)
        object.__setattr__(self, "lock", asyncio.Lock())
        object.__setattr__(self, "acquisition", acquisition)

    async def unlock(self: SessionLock) -> bool:
        """
        Releases this session lock if it is owned by the session.

        Since:
            6.10.

        Returns:
            `True` if unlocking is successful, `False` if not

        """
        async with self.lock:
            if self.owned:
                object.__setattr__(self, "owned", False)
                target = typing.cast(
                    SessionLocks, typing.cast(weakref.ReferenceType, self.parent)()
                )
                return await target.unlock(self)

        return False

    async def set_released(self: SessionLock):
        """
        Marks this lock as released.
        """
        async with self.lock:
            object.__setattr__(self, "owned", False)

    def __str__(self):
        return (
            f"{type(self).__name__}[Name={self.name}, Sequence={self.sequence},"
            f" Scope={self.scope.name}, Owned={self.is_owned}]"
        )


class SessionLocks(object):

    failover_detection_id: typing.Optional[ConversationID]

    async def on_session_event(
        self: SessionLocks,
        *,
        session: InternalSession,
        old_state: typing.Optional[State],
        new_state: State,
    ):
        from diffusion.internal.session.connection import State

        if new_state == State.RECOVERING_RECONNECT:
            # This client has detected connection loss.
            async with self.locker:
                for session_lock in self.locks.values():
                    if session_lock.scope == SessionLockScope.UNLOCK_ON_CONNECTION_LOSS:
                        await session_lock.set_released()

                        # There could be pending duplicate acquisitions
                        # that will arrive after reconnection. We leave
                        # lock in locks so we can filter these when they
                        # arrive.

            # Abuse a conversation set to detect failover and release the locks.
            # Relies on the RECONNECTED_WITH_MESSAGE_LOSS handling to discard all
            # current conversations.

            async with self.swap_lock:

                class LockInitHandler(ResponseHandler):
                    def __init__(
                        self,
                        parent: SessionLocks,
                    ):
                        super().__init__()
                        self.parent = parent

                    async def on_response(self, value: ServiceValue) -> bool:
                        """Triggered on conversation response."""
                        return True

                    async def on_discard(self, error: Exception) -> None:
                        """Triggered when a conversation is discarded."""
                        await self.parent.release_all_locks()

                self.failover_detection_id = (
                    await self.internal_session.conversations.new_conversation(
                        service=None, cid=None, handler=LockInitHandler(self)
                    )
                ).cid
        elif new_state == State.CONNECTED_ACTIVE:
            async with self.swap_lock:
                if self.failover_detection_id is not None:
                    old = self.failover_detection_id
                    self.internal_session.conversations.get_by_cid(old)
                    self.failover_detection_id = None
        elif new_state.value.closed:
            await self.release_all_locks()

    def __init__(self: SessionLocks, internal_session: InternalSession):
        """
        Initializes a new [SessionLocks][diffusion.session.locks.session_locks.SessionLocks]

        Args:
            internal_session: The internal session.
        """
        self.locker = asyncio.Lock()
        self.locks: typing.Dict[str, SessionLock] = dict()
        self.failover_detection_id = None
        self.next_request_id: int = 0
        self.internal_session: InternalSession = internal_session
        if internal_session is None:
            raise ValueError("internal_session")
        service_locator = internal_session.services
        self.acquire_lock = service_locator.ACQUIRE_SESSION_LOCK
        self.cancel_lock_request = service_locator.CANCEL_ACQUIRE_SESSION_LOCK
        self.release_lock = service_locator.RELEASE_SESSION_LOCK
        self.swap_lock: asyncio.Lock = asyncio.Lock()
        internal_session.add_listener(self)

    async def release_all_locks(self):
        async with self.locker:
            for lock in self.locks.values():
                await lock.set_released()
            self.locks.clear()

    async def _init_lock(self, lock_name: str) -> typing.Union[int, SessionLock]:
        async with self.locker:
            existing_lock = self.locks.get(lock_name)
            if existing_lock and existing_lock.is_owned:
                return existing_lock
            request_id = self.next_request_id
            self.next_request_id += 1
        return request_id

    @validate_member_arguments
    async def lock(
        self, lock_name: pydantic.StrictStr, scope: SessionLockScope
    ) -> "SessionLock":
        """
        Sends a lock request to the server.

        Notes:
            If the operation completes successfully, the result will be a new
            [SessionLock][diffusion.session.locks.session_locks.SessionLock].

        Args:
            lock_name: The name of the lock.
            scope: The scope of the lock.
        Returns:
            A session lock object.

        """
        if lock_name is None:
            raise ValueError("lock_name")
        if scope is None:
            raise ValueError(f"Invalid session lock scope {scope}")

        lock_or_request_id = await self._init_lock(lock_name)

        if isinstance(lock_or_request_id, SessionLock):
            return lock_or_request_id
        else:
            request_id = lock_or_request_id

        request = SessionLockRequest(
            lock_name=lock_name, request_id=request_id, scope=scope
        )

        session_lock: typing.Optional[SessionLock] = None

        async def get_lock() -> SessionLock:
            nonlocal session_lock
            acquisition = await self.acquire_lock.invoke(
                self.internal_session,
                request=request,
                response_type=SessionLockAcquisition,
            )

            async with self.locker:
                old = self.locks.get(lock_name, None)
                if old:
                    if old.sequence != acquisition.sequence:
                        await old.set_released()
                        session_lock = SessionLock(self, acquisition)
                        self.locks[lock_name] = session_lock
                    else:
                        session_lock = old
                else:
                    session_lock = SessionLock(self, acquisition)
                    self.locks[lock_name] = session_lock

            await asyncio.shield(self.post_commit())

            return session_lock

        try:
            try:
                return await asyncio.shield(get_lock())
            except asyncio.CancelledError:
                LOG.error(
                    f"Got: {traceback.format_exc()} - "
                    f"Cancelling {lock_name}, with {request_id}"
                )
                cancellation_request = SessionLockRequestCancellation(
                    lock_name=lock_name, request_id=request_id
                )
                await self.cancel_lock_request.invoke(
                    self.internal_session, request=cancellation_request
                )
                raise
        except BaseException:
            if session_lock:
                await session_lock.unlock()
            raise

    async def post_commit(self):
        """
        Hook that runs immediately after internal lock committal.

        Primarily used for testing.
        """

        pass

    async def unlock(self: SessionLocks, session_lock: SessionLock) -> bool:
        """
        Sends an unlock request to the server and releases the given session lock.

        Notes:
            If the operation completes successfully, the result will be a
            `bool` indicating whether the server released the given
            [SessionLock][diffusion.session.locks.session_locks.SessionLock].

        Args:
            session_lock: The session lock to release.
        Returns:
            `True` if successful, otherwise `False`.
        """
        try:
            result = await self.release_lock.invoke(
                typing.cast(
                    SessionLocks, typing.cast(weakref.ReferenceType, session_lock.parent)()
                ).internal_session,
                request=session_lock.acquisition,
                response_type=Bool,
            )
        finally:
            async with self.locker:
                current_lock = self.locks.get(session_lock.name)
                if current_lock == session_lock:
                    del self.locks[session_lock.name]
        return result
