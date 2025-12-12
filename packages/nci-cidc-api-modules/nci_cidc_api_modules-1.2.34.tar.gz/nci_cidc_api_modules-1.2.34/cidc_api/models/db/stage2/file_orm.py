from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKeyConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cidc_api.models.db.base_orm import BaseORM
from cidc_api.models.types import ChecksumType, FileFormat


class FileORM(BaseORM):
    __tablename__ = "file"
    __table_args__ = (
        ForeignKeyConstraint(
            ["trial_id", "version"], ["stage2.trial.trial_id", "stage2.trial.version"], ondelete="CASCADE"
        ),
        {"schema": "stage2"},
    )

    file_id: Mapped[int] = mapped_column(primary_key=True)
    trial_id: Mapped[str]
    version: Mapped[str]

    creator_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("stage2.institution.institution_id", ondelete="CASCADE")
    )
    description: Mapped[Optional[str]]
    uuid: Mapped[str]
    file_name: Mapped[str]
    object_url: Mapped[str]
    uploaded_timestamp: Mapped[datetime]
    file_size_bytes: Mapped[int]
    checksum_value: Mapped[str]
    checksum_type: Mapped[ChecksumType]
    file_format: Mapped[FileFormat]

    trial: Mapped["TrialORM"] = relationship(back_populates="files", cascade="all, delete")
    creator: Mapped[Optional["InstitutionORM"]] = relationship(back_populates="files", cascade="all, delete")
