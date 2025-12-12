from pydantic import NonNegativeInt
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cidc_api.models.db.base_orm import BaseORM
from cidc_api.models.types import SurgicalProcedure, UberonAnatomicalTerm, YNU


class SurgeryORM(BaseORM):
    __tablename__ = "surgery"
    __repr_attrs__ = ["surgery_id", "procedure"]
    __table_args__ = {"schema": "stage2"}
    __data_category__ = "surgery"

    surgery_id: Mapped[int] = mapped_column(primary_key=True)
    treatment_id: Mapped[int] = mapped_column(ForeignKey("stage2.treatment.treatment_id", ondelete="CASCADE"))

    procedure: Mapped[SurgicalProcedure]
    procedure_other: Mapped[Optional[str]]
    days_to_procedure: Mapped[NonNegativeInt]
    anatomical_location: Mapped[UberonAnatomicalTerm]
    therapeutic: Mapped[YNU]
    findings: Mapped[Optional[str]]
    extent_of_residual_disease: Mapped[Optional[str]]

    treatment: Mapped["TreatmentORM"] = relationship(back_populates="surgeries", cascade="all, delete")
