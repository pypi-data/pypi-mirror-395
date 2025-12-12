from pydantic import NonNegativeInt, NonNegativeFloat, PositiveFloat
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cidc_api.models.db.base_orm import BaseORM
from cidc_api.models.types import (
    RadiotherapyProcedure,
    UberonAnatomicalTerm,
    RadiotherapyDoseUnits,
    YNU,
    RadiationExtent,
)


class RadiotherapyDoseORM(BaseORM):
    __tablename__ = "radiotherapy_dose"
    __repr_attrs__ = ["radiotherapy_dose_id", "procedure"]
    __table_args__ = {"schema": "stage2"}
    __data_category__ = "radiotherapy_dose"

    radiotherapy_dose_id: Mapped[int] = mapped_column(primary_key=True)
    treatment_id: Mapped[int] = mapped_column(ForeignKey("stage2.treatment.treatment_id", ondelete="CASCADE"))

    days_to_start: Mapped[NonNegativeInt]
    days_to_end: Mapped[NonNegativeInt]
    procedure: Mapped[RadiotherapyProcedure]
    anatomical_location: Mapped[Optional[UberonAnatomicalTerm]]
    is_total_dose: Mapped[bool]
    number_of_fractions: Mapped[Optional[NonNegativeInt]]
    received_dose: Mapped[NonNegativeFloat]
    received_dose_units: Mapped[RadiotherapyDoseUnits]
    planned_dose: Mapped[Optional[PositiveFloat]]
    planned_dose_units: Mapped[Optional[RadiotherapyDoseUnits]]
    dose_changes_delays: Mapped[YNU]
    changes_delays_description: Mapped[Optional[str]]
    radiation_extent: Mapped[RadiationExtent]

    treatment: Mapped["TreatmentORM"] = relationship(back_populates="radiotherapy_doses", cascade="all, delete")
