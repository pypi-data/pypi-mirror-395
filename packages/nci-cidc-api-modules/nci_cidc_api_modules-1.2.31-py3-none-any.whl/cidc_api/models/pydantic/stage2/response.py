from typing import Self

from pydantic import NonNegativeInt, model_validator

from .base import Base
from cidc_api.models.types import SurvivalStatus, YNUNA, CauseOfDeath


class Response(Base):
    __data_category__ = "response"
    __cardinality__ = "one"

    # The unique internal identifier for the response record
    response_id: int | None = None

    # The unique internal identifier for the associated participant
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=12220014%20and%20ver_nr=1
    participant_id: str | None = None

    # The response to a question that describes a participant's survival status.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2847330%20and%20ver_nr=1
    survival_status: SurvivalStatus

    # Number of days from enrollment date to death date.
    overall_survival: NonNegativeInt | None = None

    # Indicator for whether there was an abscopal effect on disease after local therapy.
    abscopal_response: YNUNA | None = None

    # Indicates if pathological complete response (pCR) occurred.
    pathological_complete_response: YNUNA | None = None

    # Number of days between enrollment date and date of death, if applicable.
    days_to_death: NonNegativeInt | None = None

    # The circumstance or condition of greatest rank or importance that results in the death of the participant
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=4783274%20and%20ver_nr=1
    cause_of_death: CauseOfDeath | None = None

    # Indicates whether participant was evaluable for toxicity (adverse events, DLT, etc.) overall.
    evaluable_for_toxicity: bool

    # Indicates whether participant was evaluable for efficacy (for example, response, PFS, OS, etc.) overall.
    evaluable_for_efficacy: bool

    # Days from enrollment date to the last time patient had follow-up.
    days_to_last_follow_up: NonNegativeInt | None = None

    @model_validator(mode="after")
    def validate_overall_survival_cr(self) -> Self:
        if self.survival_status != "Unknown" and not self.overall_survival:
            raise ValueError('If survival_status is not "Unknown" then overall_survival is required.')
        return self

    @model_validator(mode="after")
    def validate_cause_of_death_cr(self) -> Self:
        if self.survival_status == "Dead" and not self.cause_of_death:
            raise ValueError('If survival_status is "Dead" then cause_of_death is required.')
        return self

    @model_validator(mode="after")
    def validate_cause_of_death_cr2(self) -> Self:
        if self.survival_status == "Alive" and self.cause_of_death:
            raise ValueError('If survival_status is "Alive", please leave cause_of_death blank.')
        return self

    @model_validator(mode="after")
    def validate_days_to_death_cr(self) -> Self:
        if self.survival_status in ["Alive", "Unknown"] and self.days_to_death:
            raise ValueError("If survival_status does not indicate death, please leave days_to_death blank.")
        return self
