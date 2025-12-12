from pydantic import NonNegativeInt
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cidc_api.models.db.base_orm import BaseORM


class AdditionalTreatmentORM(BaseORM):
    __tablename__ = "additional_treatment"
    __repr_attrs__ = ["additional_treatment_id", "participant_id", "description"]
    __table_args__ = {"schema": "stage2"}
    __data_category__ = "additional_treatment"

    additional_treatment_id: Mapped[int] = mapped_column(primary_key=True)
    participant_id: Mapped[int] = mapped_column(ForeignKey("stage2.participant.participant_id", ondelete="CASCADE"))

    days_to_start: Mapped[Optional[NonNegativeInt]]
    days_to_end: Mapped[Optional[NonNegativeInt]]
    description: Mapped[str]

    participant: Mapped["ParticipantORM"] = relationship(back_populates="additional_treatments", cascade="all, delete")
