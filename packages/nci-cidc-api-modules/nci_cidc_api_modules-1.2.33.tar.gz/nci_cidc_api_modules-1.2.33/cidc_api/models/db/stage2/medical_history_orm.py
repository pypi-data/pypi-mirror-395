from typing import Optional, List

from pydantic import NonNegativeInt, PositiveFloat
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cidc_api.models.db.base_orm import BaseORM
from cidc_api.models.types import TobaccoSmokingStatus


class MedicalHistoryORM(BaseORM):
    __tablename__ = "medical_history"
    __repr_attrs__ = ["medical_history_id"]
    __table_args__ = {"schema": "stage2"}
    __data_category__ = "medical_history"

    medical_history_id: Mapped[int] = mapped_column(primary_key=True)
    participant_id: Mapped[int] = mapped_column(ForeignKey("stage2.participant.participant_id", ondelete="CASCADE"))

    tobacco_smoking_status: Mapped[Optional[TobaccoSmokingStatus]]
    pack_years_smoked: Mapped[Optional[PositiveFloat]]
    num_prior_systemic_therapies: Mapped[Optional[NonNegativeInt]]

    participant: Mapped["ParticipantORM"] = relationship(back_populates="medical_history", cascade="all, delete")
    other_malignancies: Mapped[List["OtherMalignancyORM"]] = relationship(
        back_populates="medical_history", cascade="all, delete", passive_deletes=True
    )
    comorbidities: Mapped[List["ComorbidityORM"]] = relationship(
        back_populates="medical_history", cascade="all, delete", passive_deletes=True
    )
