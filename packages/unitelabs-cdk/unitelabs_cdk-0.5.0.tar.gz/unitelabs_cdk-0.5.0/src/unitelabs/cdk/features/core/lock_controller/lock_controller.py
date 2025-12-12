# ruff: noqa: D205, D401, E501

import asyncio
import dataclasses
import datetime
import uuid

import typing_extensions as typing

from unitelabs.cdk import sila


class InvalidLockIdentifier(Exception):
    """The sent lock identifier is not valid."""


class ServerAlreadyLocked(Exception):
    """The SiLA Server can not be locked because it is already locked."""


class ServerNotLocked(Exception):
    """The SiLA Server can not be unlocked because it is not locked."""


@dataclasses.dataclass
class LockIdentifier(sila.Metadatum, errors=[InvalidLockIdentifier]):
    """The lock identifier has to be sent with every (lock protected) call in order to use the functionality of a locked SiLA Server."""

    lock_identifier: str

    @typing.override
    def intercept(self) -> None:
        if not isinstance(self.feature, LockController):
            raise RuntimeError

        if self.feature.lock is None or self.feature.lock.identifier != self.lock_identifier:
            raise InvalidLockIdentifier

        self.feature.lock.last_usage = sila.datetime.datetime.now()


@dataclasses.dataclass
class Lock:
    """A lock used for unique access to resources."""

    identifier: str = dataclasses.field(default_factory=lambda: str(uuid.uuid4()))
    """The identifier used by the client for unique access."""

    lifetime: datetime.timedelta = dataclasses.field(default_factory=datetime.timedelta)
    """The lifetime of the access token before it expires."""

    last_usage: datetime.datetime = dataclasses.field(default_factory=datetime.datetime.now)
    """Point in time when the access token was used last."""

    @property
    def is_expired(self) -> bool:
        """Whether the lock has expired."""

        return (datetime.datetime.now() - self.lifetime) > self.last_usage


class LockController(sila.Feature):
    """
    This Feature allows a SiLA Client to lock a SiLA Server for exclusive use, preventing other SiLA Clients
    from using the SiLA Server while it is locked. To lock a SiLA Server a Lock Identifier has to be set, using the
    'LockServer' command. This Lock Identifier has to be sent along with every (lock protected)
    request to the SiLA Server in order to use its functionality.

    To send the lock identifier the SiLA Client Meta Data 'LockIdentifier' has to be used.

    When locking a SiLA Server a timeout can be specified that defines the time after which the SiLA Server will
    be automatically unlocked if no request with a valid lock identifier has been received meanwhile.
    After the timeout has expired or after explicit unlock no lock identifier has to be sent any more.
    """

    def __init__(self):
        super().__init__(
            originator="org.silastandard",
            category="core",
            version="2.0",
            metadata=[LockIdentifier],
        )

        self._lock: typing.Optional[Lock] = None
        self._event = asyncio.Event()

    @property
    def lock(self) -> typing.Optional[Lock]:
        """The lock on the SiLA Server, if any."""

        if self._lock and self._lock.is_expired:
            self._event.set()
            self._lock = None

        return self._lock

    @lock.setter
    def lock(self, value: typing.Optional[Lock]) -> None:
        self._event.set()
        self._lock = value

    @sila.ObservableProperty()
    async def subscribe_is_locked(self) -> sila.Stream[bool]:
        """
        Returns true if the SiLA Server is currently locked or false else.

        This property MUST NOT be lock protected, so that any SiLA Client can query the current lock state
        of a SiLA Server.
        """

        while True:
            self._event.clear()
            yield self.lock is not None
            await self._event.wait()

    @sila.UnobservableCommand()
    def lock_server(
        self,
        lock_identifier: str,
        timeout: typing.Annotated[
            int,
            sila.constraints.Unit(label="s", components=[sila.constraints.Unit.Component(unit="Second")]),
        ],
    ) -> None:
        """
        Locks a SiLA Server for exclusive use by setting a lock identifier that has to be sent along with
        any following (lock protected) request as long as the SiLA Server is locked.
        The lock can be reset by issuing the 'Unlock Server' command.

        Args:
          LockIdentifier: The lock identifier that has to be sent along with every (lock protected) request to use the server's functionality.
          Timeout: The time (in seconds) after a SiLA Server is automatically unlocked when no request with a valid lock identifier
            has been received meanwhile. A timeout of zero seconds specifies an infinite time (no timeout).

        Raises:
          ServerAlreadyLocked: The SiLA Server can not be locked because it is already locked.
        """

        if self.lock:
            raise ServerAlreadyLocked

        self.lock = Lock(identifier=lock_identifier, lifetime=sila.datetime.timedelta(seconds=timeout))

    @sila.UnobservableCommand()
    def unlock_server(self, lock_identifier: str) -> None:
        """
        Unlocks a locked SiLA Server. No lock identifier has to be sent for any following calls until
        the server is locked again via the 'Lock Server' command.

        Args:
          LockIdentifier: The lock identifier that has been used to lock the SiLA Server.

        Raises:
          ServerNotLocked: The SiLA Server can not be unlocked because it is not locked.
          InvalidLockIdentifier: The sent lock identifier is not valid.
        """

        lock = self.lock

        if lock is None:
            raise ServerNotLocked

        if lock.identifier != lock_identifier:
            raise InvalidLockIdentifier

        self.lock = None
