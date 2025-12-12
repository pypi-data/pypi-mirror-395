from typing import List

from pydantic import NonNegativeInt
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cidc_api.models.db.base_orm import BaseORM


class ConsentGroupORM(BaseORM):
    __tablename__ = "consent_group"
    __repr_attrs__ = ["consent_group_id", "consent_group_name"]
    __table_args__ = (
        ForeignKeyConstraint(
            ["trial_id", "version"], ["stage2.trial.trial_id", "stage2.trial.version"], ondelete="CASCADE"
        ),
        {"schema": "stage2"},
    )
    __data_category__ = "consent_group"

    consent_group_id: Mapped[int] = mapped_column(primary_key=True)
    trial_id: Mapped[str]
    version: Mapped[str]

    consent_group_short_name: Mapped[str]
    consent_group_name: Mapped[str]
    consent_group_number: Mapped[NonNegativeInt]

    trial: Mapped["TrialORM"] = relationship(back_populates="consent_groups", cascade="all, delete")
    participants: Mapped[List["ParticipantORM"]] = relationship(
        back_populates="consent_group", cascade="all, delete", passive_deletes=True
    )
