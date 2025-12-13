from enum import StrEnum, auto
from sqlalchemy import JSON, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils.types import UUIDType

from cattle_grid.model.account import EventType


from .activity_pub import Base


class ActorStatus(StrEnum):
    """Status actors can have for an account"""

    active = auto()
    deleted = auto()


class Account(Base):
    """Represents an account"""

    __tablename__ = "account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256))
    password_hash: Mapped[str] = mapped_column(String(256))
    meta_information: Mapped[dict] = mapped_column(JSON(), default={})

    actors: Mapped[list["ActorForAccount"]] = relationship(viewonly=True)
    permissions: Mapped[list["Permission"]] = relationship(viewonly=True)


class ActorForAccount(Base):
    """Represents the actor associated with an account"""

    __tablename__ = "actorforaccount"
    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(
        ForeignKey("account.id", ondelete="CASCADE")
    )
    account: Mapped[Account] = relationship(lazy="joined")

    actor: Mapped[str] = mapped_column(String(256))
    name: Mapped[str] = mapped_column(
        String(256),
        default="NO NAME",
    )
    status: Mapped[ActorStatus] = mapped_column(String(10), default=ActorStatus.active)

    groups: Mapped[list["ActorGroup"]] = relationship(viewonly=True)


class AuthenticationToken(Base):
    """Tokens used for the frontend api access"""

    __tablename__ = "authenticationtoken"
    token: Mapped[str] = mapped_column(String(65), primary_key=True)
    account_id: Mapped[int] = mapped_column(
        ForeignKey("account.id", ondelete="CASCADE")
    )
    account: Mapped[Account] = relationship(lazy="joined")


class Permission(Base):
    """Permissions associated with the account"""

    __tablename__ = "permission"
    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(
        ForeignKey("account.id", ondelete="CASCADE")
    )
    account: Mapped[Account] = relationship(lazy="joined")

    name: Mapped[str] = mapped_column(String(256))


class ActorGroup(Base):
    """Groups the actor is part of"""

    __tablename__ = "actorgroup"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256))
    actor_id: Mapped[int] = mapped_column(
        ForeignKey("actorforaccount.id", ondelete="CASCADE")
    )
    actor: Mapped[ActorForAccount] = relationship(lazy="joined")


class EventHistoryStatus(StrEnum):
    read = auto()
    unread = auto()


class EventHistory(Base):
    """Stores a record of the event for the account"""

    __tablename__ = "account_event_history"

    id: Mapped[bytes] = mapped_column(UUIDType(binary=True), primary_key=True)
    account_id: Mapped[int] = mapped_column(
        ForeignKey("account.id", ondelete="CASCADE")
    )
    account: Mapped[Account] = relationship(lazy="joined")

    event_type: Mapped[EventType] = mapped_column(String(10))
    data: Mapped[dict] = mapped_column(JSON())
    actor: Mapped[str] = mapped_column()

    status: Mapped[EventHistoryStatus] = mapped_column(
        String(10), default=EventHistoryStatus.unread
    )
