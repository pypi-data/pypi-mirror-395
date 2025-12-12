from typing import Optional

from pydantic import NonPositiveInt, NonNegativeInt
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cidc_api.models.db.base_orm import BaseORM
from cidc_api.models.types import PriorTreatmentType, ConditioningRegimenType, StemCellDonorType


class PriorTreatmentORM(BaseORM):
    __tablename__ = "prior_treatment"
    __repr_attrs__ = ["prior_treatment_id", "type"]
    __table_args__ = {"schema": "stage2"}
    __data_category__ = "prior_treatment"

    prior_treatment_id: Mapped[int] = mapped_column(primary_key=True)
    participant_id: Mapped[int] = mapped_column(ForeignKey("stage2.participant.participant_id", ondelete="CASCADE"))

    days_to_start: Mapped[Optional[NonPositiveInt]]
    days_to_end: Mapped[Optional[NonPositiveInt]]
    type: Mapped[PriorTreatmentType]
    description: Mapped[Optional[str]]
    best_response: Mapped[Optional[str]]
    conditioning_regimen_type: Mapped[Optional[ConditioningRegimenType]]
    stem_cell_donor_type: Mapped[Optional[StemCellDonorType]]
    days_from_transplant_to_treatment_initiation: Mapped[Optional[NonNegativeInt]]

    participant: Mapped["ParticipantORM"] = relationship(back_populates="prior_treatments", cascade="all, delete")
