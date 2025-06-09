from datetime import datetime, UTC, timezone
from typing import List

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

class Base(DeclarativeBase):
    pass

class UserORM(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    date_of_birth: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    bio: Mapped[str]

    book: Mapped[List["BookORM"]] = relationship(back_populates="author")


class BookORM(TimestampMixin, Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    title: Mapped[str]
    author_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    description: Mapped[str]

    author: Mapped[UserORM | None]= relationship(back_populates="book", uselist=False)

