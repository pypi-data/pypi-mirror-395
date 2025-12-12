from typing import List

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cidc_api.models.db.base_orm import BaseORM
from cidc_api.models.types import (
    GVHDDiagnosisChronicAssessmentSystem,
    GVHDDiagnosisChronicAssessmentSystemVersion,
    GVHDDiagnosisChronicGlobalSeverity,
    PreOrPostEnrollment,
)


class GVHDDiagnosisChronicORM(BaseORM):
    __tablename__ = "gvhd_diagnosis_chronic"
    __table_args__ = (
        UniqueConstraint(
            "participant_id", "pre_or_post_enrollment", name="unique_ix_gvhd_diagnosis_chronic_pre_or_post"
        ),
        {"schema": "stage2"},
    )
    __repr_attrs__ = ["gvhd_diagnosis_chronic_id", "pre_or_post_enrollment"]
    __data_category__ = "gvhd_diagnosis_chronic"

    gvhd_diagnosis_chronic_id: Mapped[int] = mapped_column(primary_key=True)
    participant_id: Mapped[int] = mapped_column(ForeignKey("stage2.participant.participant_id", ondelete="CASCADE"))
    chronic_assessment_system: Mapped[GVHDDiagnosisChronicAssessmentSystem]
    system_version: Mapped[GVHDDiagnosisChronicAssessmentSystemVersion]
    chronic_global_severity: Mapped[GVHDDiagnosisChronicGlobalSeverity]
    pre_or_post_enrollment: Mapped[PreOrPostEnrollment]

    participant: Mapped["ParticipantORM"] = relationship(
        back_populates="gvhd_diagnosis_chronics", cascade="all, delete"
    )
    organs: Mapped[List["GVHDOrganChronicORM"]] = relationship(
        back_populates="diagnosis", cascade="all, delete", passive_deletes=True
    )
