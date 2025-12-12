from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cidc_api.models.db.base_orm import BaseORM
from cidc_api.models.types import ECOGScore, KarnofskyScore


class BaselineClinicalAssessmentORM(BaseORM):
    __tablename__ = "baseline_clinical_assessment"
    __repr_attrs__ = ["baseline_clinical_assessment_id", "participant_id"]
    __table_args__ = {"schema": "stage2"}
    __data_category__ = "baseline_clinical_assessment"

    baseline_clinical_assessment_id: Mapped[int] = mapped_column(primary_key=True)
    participant_id: Mapped[int] = mapped_column(ForeignKey("stage2.participant.participant_id", ondelete="CASCADE"))

    ecog_score: Mapped[Optional[ECOGScore]]
    karnofsky_score: Mapped[Optional[KarnofskyScore]]

    participant: Mapped["ParticipantORM"] = relationship(
        back_populates="baseline_clinical_assessment", cascade="all, delete"
    )
