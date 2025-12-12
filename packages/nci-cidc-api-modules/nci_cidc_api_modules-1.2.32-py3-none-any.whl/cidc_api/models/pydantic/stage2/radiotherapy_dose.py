from typing import Self

from pydantic import NonNegativeInt, NonNegativeFloat, model_validator

from .base import Base
from cidc_api.models.types import (
    YNU,
    RadiotherapyProcedure,
    UberonAnatomicalTerm,
    RadiotherapyDoseUnits,
    RadiationExtent,
)


class RadiotherapyDose(Base):
    __data_category__ = "radiotherapy_dose"
    __cardinality__ = "many"

    # The unique internal identifier for the radiotherapy dose record
    radiotherapy_dose_id: int | None = None

    # The unique internal identifier for the associated treatment record
    treatment_id: int | None = None

    # Number of days from enrollment date to the start of the radiotherapy dose.
    days_to_start: NonNegativeInt

    # Number of days from enrollment date to the end of the radiotherapy dose.
    days_to_end: NonNegativeInt

    # The term that describes the kind of radiotherapy procedure administered.
    procedure: RadiotherapyProcedure

    # The Uberon anatomical term for the site of surgery.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=14461856%20and%20ver_nr=1
    anatomical_location: UberonAnatomicalTerm | None = None

    # Indicates whether the record represents the total dose for a radiotherapy treatment course (which may be either
    # a multi-fractionated or a single-fraction dose).
    is_total_dose: bool

    # The number of fractions a participant received to deliver the radiation dose.
    number_of_fractions: NonNegativeInt | None = None

    # The dose amount received by the participant.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=13433490%20and%20ver_nr=1
    received_dose: NonNegativeFloat

    # Unit of measure for the dose of the radiotherapy to be received by the participant.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=13383458%20and%20ver_nr=1
    received_dose_units: RadiotherapyDoseUnits

    # The planned dose amount for the participant.
    planned_dose: NonNegativeFloat | None = None

    # Unit of measure for the planned total dose of the radiotherapy to be received by the participant.
    planned_dose_units: RadiotherapyDoseUnits | None = None

    # Indicates if the radiotherapy dose was changed, missed, or delayed.
    dose_changes_delays: YNU

    # Description of the radiotherapy dose changes, misses, or delays.
    changes_delays_description: str | None = None

    # The extent of radiation exposure administered to the patient's body during radiation therapy.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=7063755%20and%20ver_nr=1
    radiation_extent: RadiationExtent

    @model_validator(mode="after")
    def validate_changes_delays_description_cr(self) -> Self:
        if self.dose_changes_delays == "Yes" and not self.changes_delays_description:
            raise ValueError('If dose_changes_delays is "Yes", please provide changes_delays_description.')
        return self

    @model_validator(mode="after")
    def validate_planned_dose_units_cr(self) -> Self:
        if self.planned_dose and not self.planned_dose_units:
            raise ValueError("If planned_dose is provided, please provide planned_dose_units.")
        return self
