from sqlalchemy import String, Text
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Credential(Base):
    """Stored credential. This corresponds to storing a private key"""

    __tablename__ = "credential"

    id: Mapped[int] = mapped_column(primary_key=True)
    actor_id: Mapped[str] = mapped_column(String(256))
    identifier: Mapped[str] = mapped_column(String(256), unique=True)
    secret: Mapped[str] = mapped_column(Text())


class InboxLocation(Base):
    """Describes the location of an inbox. Used to send
    ActivityPub Activities addressed to the actor to the
    corresponding inbox.

    This information is also collected for remote actors.
    """

    __tablename__ = "inboxlocation"

    id: Mapped[int] = mapped_column(primary_key=True)
    actor: Mapped[str] = mapped_column(String(256), unique=True)
    inbox: Mapped[str] = mapped_column(String(256))
