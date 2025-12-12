from typing import Self

from pydantic import NonNegativeInt, NonNegativeFloat, PositiveFloat, model_validator

from .base import Base
from cidc_api.models.types import YNU, TherapyAgentDoseUnits


class TherapyAgentDose(Base):
    __data_category__ = "therapy_agent_dose"
    __cardinality__ = "many"

    # The unique internal identifier for the therapy agent dose record
    therapy_agent_dose_id: int | None = None

    # The unique internal identifier for the associated treatment record
    treatment_id: int | None = None

    # A numeric identifier used to indicate a specific course or cycle of treatment.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=16391085%20and%20ver_nr=1
    course_number: str | None = None

    # The full generic name of the therapeutic agent, if available, as captured in the Pharmacological
    # Substance (C1909) branch of the National Cancer Institute Thesaurus (NCIt).
    therapy_agent_name: str

    # Number of days from the enrollment date to the start date of the therapy dose.
    days_to_start: NonNegativeInt

    # Number of days from enrollment date to the end date of the therapy dose.
    days_to_end: NonNegativeInt

    # Number of individual doses the patient received of the therapy agent.
    number_of_doses: NonNegativeInt

    # The amount that represents the dose of the therapy agent received by the participant.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2182728%20and%20ver_nr=3
    received_dose: NonNegativeFloat

    # Unit of measure for the dose of the agent received by the participant.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2321160%20and%20ver_nr=4
    received_dose_units: TherapyAgentDoseUnits

    # The amount that represents the planned dose of the therapy agent to be received by the participant.
    planned_dose: PositiveFloat | None = None

    # Unit of measure for the planned dose of the agent to be received by the participant.
    # TODO: This CDE will probably be 2321160 but needs to be finalized with Janice
    planned_dose_units: TherapyAgentDoseUnits | None = None

    # Indicates if the therapy agent dose was changed, missed, or delayed.
    dose_changes_delays: YNU

    # Description of the dose changes, misses, or delays.
    changes_delays_description: str | None = None

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
