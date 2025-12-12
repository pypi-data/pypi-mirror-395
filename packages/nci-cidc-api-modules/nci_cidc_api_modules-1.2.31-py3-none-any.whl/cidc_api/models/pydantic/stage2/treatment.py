from typing import Self

from pydantic import model_validator

from .base import Base
from cidc_api.models.types import YNU, OffTreatmentReason


class Treatment(Base):
    __data_category__ = "treatment"
    __cardinality__ = "many"

    # The unique internal identifier for the Treatment record
    treatment_id: int | None = None

    # The unique internal identifier for the associated Participant record
    participant_id: str | None = None

    # The unique internal identifier for the associated Arm record
    arm_id: int | None = None

    # The unique internal identifier for the associated Cohort record
    cohort_id: int | None = None

    # A unique identifier used to describe a distinct, specific intervention or
    # treatment that a group or subgroup of participants in a clinical trial receives.
    treatment_description: str

    # Indicates if the participant has stopped receiving this particular treatment at
    # the time of data submission.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=16391087%20and%20ver_nr=1
    off_treatment: YNU

    # An explanation describing why an individual is no longer receiving this particular treatment.
    off_treatment_reason: OffTreatmentReason | None = None

    # If "Other" is selected for "off_treatment_reason", provide a description of the reason.
    off_treatment_reason_other: str | None = None

    @model_validator(mode="after")
    def validate_off_treatment_reason_cr(self) -> Self:
        if self.off_treatment == "Yes" and not self.off_treatment_reason:
            raise ValueError('If off_treatment is "Yes", please provide off_treatment_reason.')
        return self

    @model_validator(mode="after")
    def validate_off_treatment_reason_other_cr(self) -> Self:
        if self.off_treatment_reason == "Other" and not self.off_treatment_reason_other:
            raise ValueError('If off_treatment_reason is "Other", please provide off_treatment_reason_other.')
        return self
