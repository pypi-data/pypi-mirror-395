from pydantic import NonNegativeInt
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cidc_api.models.db.base_orm import BaseORM
from cidc_api.models.types import StemCellDonorType, AllogeneicDonorType, StemCellSource, ConditioningRegimenType


class StemCellTransplantORM(BaseORM):
    __tablename__ = "stem_cell_transplant"
    __repr_attrs__ = ["stem_cell_transplant_id"]
    __table_args__ = {"schema": "stage2"}
    __data_category__ = "stem_cell_transplant"

    stem_cell_transplant_id: Mapped[int] = mapped_column(primary_key=True)
    treatment_id: Mapped[int] = mapped_column(ForeignKey("stage2.treatment.treatment_id", ondelete="CASCADE"))

    stem_cell_donor_type: Mapped[StemCellDonorType]
    allogeneic_donor_type: Mapped[AllogeneicDonorType]
    stem_cells_source: Mapped[StemCellSource]
    days_to_transplant: Mapped[NonNegativeInt]
    conditioning_regimen_type: Mapped[Optional[ConditioningRegimenType]]

    treatment: Mapped["TreatmentORM"] = relationship(back_populates="stem_cell_transplants", cascade="all, delete")
