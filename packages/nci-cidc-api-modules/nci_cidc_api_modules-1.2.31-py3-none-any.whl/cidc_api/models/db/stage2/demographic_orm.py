from pydantic import NonNegativeFloat, PositiveFloat, PositiveInt

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cidc_api.models.db.base_orm import BaseORM
from cidc_api.models.types import (
    Sex,
    Race,
    Ethnicity,
    HeightUnits,
    WeightUnits,
    BodySurfaceAreaUnits,
    Occupation,
    Education,
    AgeAtEnrollmentUnits,
)


class DemographicORM(BaseORM):
    __tablename__ = "demographic"
    __repr_attrs__ = ["demographic_id", "participant_id", "age_at_enrollment", "sex"]
    __table_args__ = {"schema": "stage2"}
    __data_category__ = "demographic"

    demographic_id: Mapped[int] = mapped_column(primary_key=True)
    participant_id: Mapped[int] = mapped_column(ForeignKey("stage2.participant.participant_id", ondelete="CASCADE"))
    age_at_enrollment: Mapped[PositiveInt | None]
    age_at_enrollment_units: Mapped[AgeAtEnrollmentUnits | None]
    age_90_or_over: Mapped[bool]
    sex: Mapped[Sex]
    race: Mapped[Race]
    ethnicity: Mapped[Ethnicity]
    height: Mapped[PositiveFloat]
    height_units: Mapped[HeightUnits]
    weight: Mapped[PositiveFloat]
    weight_units: Mapped[WeightUnits]
    body_mass_index: Mapped[PositiveFloat]
    body_surface_area: Mapped[PositiveFloat]
    body_surface_area_units: Mapped[BodySurfaceAreaUnits]
    occupation: Mapped[Occupation | None]
    income: Mapped[NonNegativeFloat | None]
    highest_level_of_education: Mapped[Education | None]

    participant: Mapped["ParticipantORM"] = relationship(back_populates="demographic", cascade="all, delete")
