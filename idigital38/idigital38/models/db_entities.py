from dataclasses import dataclass

from sqlalchemy import String, BigInteger, SmallInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


@dataclass
class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(
        BigInteger(),
        primary_key=True,
        autoincrement=True
    )


@dataclass
class Event(Base):
    __tablename__ = 'events'

    name: Mapped[str] = mapped_column(
        String(100)
    )
    date: Mapped[int] = mapped_column(
        BigInteger()
    )
    image_uri: Mapped[str] = mapped_column(
        String(150),
        nullable=True
    )
    ref: Mapped[str] = mapped_column(
        String(150)
    )


@dataclass
class Organizer(Base):
    __tablename__ = 'organizers'

    name: Mapped[str] = mapped_column(
        String(100)
    )
    image_uri: Mapped[str] = mapped_column(
        String(150),
        nullable=True
    )
    role: Mapped[str] = mapped_column(
        String(100)
    )
    additional_role: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )
    order: Mapped[int] = mapped_column(
        SmallInteger()
    )
