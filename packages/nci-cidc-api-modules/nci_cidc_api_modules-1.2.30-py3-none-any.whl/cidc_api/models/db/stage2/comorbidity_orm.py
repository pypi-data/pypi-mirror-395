from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cidc_api.models.db.base_orm import BaseORM
from cidc_api.models.types import ICD10CMCode, ICD10CMTerm


class ComorbidityORM(BaseORM):
    __tablename__ = "comorbidity"
    __repr_attrs__ = ["comorbidity_id", "comorbidity_term"]
    __table_args__ = {"schema": "stage2"}
    __data_category__ = "comorbidity"

    comorbidity_id: Mapped[int] = mapped_column(primary_key=True)
    medical_history_id: Mapped[int] = mapped_column(
        ForeignKey("stage2.medical_history.medical_history_id", ondelete="CASCADE")
    )

    comorbidity_code: Mapped[Optional[ICD10CMCode]]
    comorbidity_term: Mapped[Optional[ICD10CMTerm]]
    comorbidity_other: Mapped[Optional[str]]

    medical_history: Mapped["MedicalHistoryORM"] = relationship(back_populates="comorbidities", cascade="all, delete")
