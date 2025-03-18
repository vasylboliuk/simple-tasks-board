"""Alembic Models model."""

import os
from typing import Optional

from dotenv import load_dotenv
from sqlalchemy import ForeignKey, String, create_engine
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship, sessionmaker

load_dotenv()

Base = declarative_base()

# Build database URL using environment variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class User(Base):
    """Represents User db model."""

    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"))
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    role: Mapped[str] = mapped_column(String(30))
    auth_token: Mapped[str] = mapped_column(String(1000))

    def __repr__(self):
        """Convert model to string."""
        return (
            f"User(id={self.id!r}, task_id={self.task_id!r}, "
            f"name={self.name!r}, fullname={self.fullname!r}, role={self.role!r})"
        )


class Task(Base):
    """Represents Task db model."""

    __tablename__ = "task"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(500))
    priority: Mapped[str] = mapped_column(String(20))
    assignee: Mapped[str] = mapped_column(String(50))
    created_by: Mapped["User"] = relationship(back_populates="user")
    status: Mapped[str] = mapped_column(String(20))

    def __repr__(self) -> str:
        """Convert model to string."""
        return (
            f"Task(id={self.id!r}, "
            f"name={self.name!r}, "
            f"description={self.description!r}, "
            f"priority={self.priority!r}, "
            f"created_by={self.created_by!r}, "
            f"assignee={self.assignee!r}, "
            f"status={self.status!r}"
            f")"
        )
