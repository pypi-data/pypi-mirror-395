from typing import List, Optional

from pydantic import NonPositiveInt
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from cidc_api.models.db.base_orm import BaseORM
from cidc_api.models.types import (
    TumorGrade,
    CancerStageSystem,
    CancerStageSystemVersion,
    CancerStage,
    TCategory,
    NCategory,
    MCategory,
    UberonAnatomicalTerm,
    ICDO3MorphologicalCode,
    ICDO3MorphologicalTerm,
    YNU,
)
from sqlalchemy import String


class DiseaseORM(BaseORM):
    __tablename__ = "disease"
    __repr_attrs__ = [
        "disease_id",
        "participant_id",
    ]
    __table_args__ = {"schema": "stage2"}
    __data_category__ = "disease"

    disease_id: Mapped[int] = mapped_column(primary_key=True)
    participant_id: Mapped[int] = mapped_column(ForeignKey("stage2.participant.participant_id", ondelete="CASCADE"))
    primary_disease_site: Mapped[UberonAnatomicalTerm]
    morphological_code: Mapped[ICDO3MorphologicalCode | None]
    morphological_term: Mapped[ICDO3MorphologicalTerm | None]
    cancer_type_description: Mapped[str | None]
    days_since_original_diagnosis: Mapped[NonPositiveInt | None]
    tumor_grade: Mapped[TumorGrade | None]
    cancer_stage_system: Mapped[CancerStageSystem]
    cancer_stage_system_version: Mapped[CancerStageSystemVersion | None] = mapped_column(String, nullable=True)
    cancer_stage: Mapped[CancerStage | None] = mapped_column(String)
    t_category: Mapped[TCategory | None]
    n_category: Mapped[NCategory | None]
    m_category: Mapped[MCategory | None]
    metastatic_organ: Mapped[List[UberonAnatomicalTerm] | None] = mapped_column(JSON, nullable=True)
    solely_extramedullary_disease: Mapped[YNU]
    extramedullary_organ: Mapped[List[UberonAnatomicalTerm]] = mapped_column(JSON, nullable=True)

    participant: Mapped["ParticipantORM"] = relationship(back_populates="diseases", cascade="all, delete")
