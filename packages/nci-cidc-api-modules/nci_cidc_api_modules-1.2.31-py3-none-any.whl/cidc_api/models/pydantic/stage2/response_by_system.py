from typing import Self

from pydantic import PositiveInt, model_validator

from .base import Base
from cidc_api.models.types import ResponseSystem, ResponseSystemVersion, BestOverallResponse, YNUNA


negative_response_values = [
    "Progressive Disease",
    "Stable Disease",
    "immune Unconfirmed Progressive Disease",
    "immune Confirmed Progressive Disease",
    "immune Stable Disease",
    "Not available",
    "Not assessed",
]


class ResponseBySystem(Base):
    __data_category__ = "response_by_system"
    __cardinality__ = "many"

    # The unique internal identifier for this ResponseBySystem record
    response_by_system_id: int | None = None

    # The unique internal identifier for the associated participant
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=12220014%20and%20ver_nr=1
    participant_id: str | None = None

    # A standardized method used to evaluate and categorize the participant’s clinical response to treatment based on predefined criteria.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=13381490%20and%20ver_nr=1
    response_system: ResponseSystem

    # The release version of the clinical assessment system used to evaluate a participant’s response to treatment.
    response_system_version: ResponseSystemVersion

    # Confirmed best overall response to study treatment by the corresponding response system.
    best_overall_response: BestOverallResponse

    # Days from first response to progression.
    response_duration: PositiveInt | None = None

    # Indicates whether a patient achieved a durable clinical benefit.
    durable_clinical_benefit: bool | None = None

    # Number of days between enrollment date and the date of first response to trial treatment.
    days_to_first_response: PositiveInt | None = None

    # Number of days between enrollment date and the date of the best response to trial treatment.
    days_to_best_response: PositiveInt | None = None

    # Indicates whether a participant's disease progressed.
    progression: YNUNA

    # Number of days between enrollment date and date of disease progression.
    days_to_disease_progression: PositiveInt | None = None

    # Indicator to identify whether a patient had a Progression-Free Survival (PFS) event.
    progression_free_survival_event: YNUNA

    # The number of days from the date the patient was enrolled in the study to the date the patient was last verified to be free of progression.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=5143957%20and%20ver_nr=1
    progression_free_survival: PositiveInt | None = None

    @model_validator(mode="after")
    def validate_response_duration_cr(self) -> Self:
        if self.best_overall_response in negative_response_values and self.response_duration:
            raise ValueError(
                "If best_overall_response does not indicate a positive response, "
                "please leave response_duration blank."
            )
        return self

    @model_validator(mode="after")
    def validate_days_to_first_response_cr(self) -> Self:
        if self.best_overall_response in negative_response_values and self.days_to_first_response:
            raise ValueError(
                "If best_overall_response does not indicate a positive response, "
                "please leave days_to_first_response blank."
            )
        return self

    @model_validator(mode="after")
    def validate_days_to_best_response_cr(self) -> Self:
        if self.best_overall_response in negative_response_values and self.days_to_best_response:
            raise ValueError(
                "If best_overall_response does not indicate a positive response, \
                please leave days_to_best_response blank."
            )
        return self

    @model_validator(mode="after")
    def validate_days_to_disease_progression_cr(self) -> Self:
        if self.progression in ["No", "Unknown", "Not Applicable"] and self.days_to_disease_progression:
            raise ValueError(
                "If progression does not indicate confirmed progression of the disease, \
                please leave days_to_disease_progress blank."
            )
        return self

    @model_validator(mode="after")
    def validate_progression_free_survival_cr(self) -> Self:
        if self.progression_free_survival_event in ["Unknown", "Not Applicable"] and self.progression_free_survival:
            raise ValueError(
                "If progression_free_survival_event is not known, \
                please leave progression_free_survival blank."
            )
        return self
