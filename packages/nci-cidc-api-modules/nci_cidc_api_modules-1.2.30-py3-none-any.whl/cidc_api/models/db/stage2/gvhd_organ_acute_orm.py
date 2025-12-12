from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cidc_api.models.db.base_orm import BaseORM
from cidc_api.models.types import GVHDOrgan, GVHDOrganAcuteStage


class GVHDOrganAcuteORM(BaseORM):
    __tablename__ = "gvhd_organ_acute"
    __repr_attrs__ = ["gvhd_organ_acute_id", "organ"]
    __table_args__ = {"schema": "stage2"}
    __data_category__ = "gvhd_organ_acute"

    gvhd_organ_acute_id: Mapped[int] = mapped_column(primary_key=True)
    gvhd_diagnosis_acute_id: Mapped[int] = mapped_column(
        ForeignKey("stage2.gvhd_diagnosis_acute.gvhd_diagnosis_acute_id", ondelete="CASCADE")
    )
    organ: Mapped[GVHDOrgan]
    acute_stage: Mapped[GVHDOrganAcuteStage]

    diagnosis: Mapped["GVHDDiagnosisAcuteORM"] = relationship(back_populates="organs", cascade="all, delete")
