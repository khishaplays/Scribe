
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from scribe.database.connection import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(150), nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    project_type: Mapped[str] = mapped_column(
        String(20), nullable=False, default="personal"
    )

    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="active"
    )

    github_repo_id: Mapped[int | None] = mapped_column(
        Integer, unique=True, nullable=True
    )

    github_url: Mapped[str | None] = mapped_column(
        String(500), nullable=True
    )

    github_owner: Mapped[str | None] = mapped_column(
        String(150), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self):
        return (
            f"<Project(id={self.id}, name={self.name!r}, "
            f"type={self.project_type!r})>"
        )

