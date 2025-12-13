from sqlalchemy import String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class RemoteIdentity(Base):
    """Stored information about a public identifier in the database."""

    __tablename__ = "cattle_grid_auth_remote_identity"

    id: Mapped[int] = mapped_column(primary_key=True)

    key_id: Mapped[str] = mapped_column(String(512), unique=True)
    controller: Mapped[str] = mapped_column(String(512))
    public_key: Mapped[str] = mapped_column(String(1024))
