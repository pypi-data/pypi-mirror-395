from typing import Optional

from pydantic import NonPositiveInt
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cidc_api.models.db.base_orm import BaseORM
from cidc_api.models.types import UberonAnatomicalTerm, ICDO3MorphologicalCode, ICDO3MorphologicalTerm, MalignancyStatus


class OtherMalignancyORM(BaseORM):
    __tablename__ = "other_malignancy"
    __repr_attrs__ = ["other_malignancy_id", "primary_disease_site"]
    __table_args__ = {"schema": "stage2"}
    __data_category__ = "other_malignancy"

    other_malignancy_id: Mapped[int] = mapped_column(primary_key=True)
    medical_history_id: Mapped[int] = mapped_column(
        ForeignKey("stage2.medical_history.medical_history_id", ondelete="CASCADE")
    )

    primary_disease_site: Mapped[UberonAnatomicalTerm]
    morphological_code: Mapped[Optional[ICDO3MorphologicalCode]]
    morphological_term: Mapped[Optional[ICDO3MorphologicalTerm]]
    malignancy_description: Mapped[Optional[str]]
    days_since_diagnosis: Mapped[Optional[NonPositiveInt]]
    malignancy_status: Mapped[Optional[MalignancyStatus]]

    medical_history: Mapped["MedicalHistoryORM"] = relationship(
        back_populates="other_malignancies", cascade="all, delete"
    )
