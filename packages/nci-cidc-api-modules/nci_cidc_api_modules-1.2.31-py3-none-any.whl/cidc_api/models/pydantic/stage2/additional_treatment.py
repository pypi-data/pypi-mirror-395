from pydantic import NonNegativeInt
from .base import Base


class AdditionalTreatment(Base):
    __data_category__ = "additional_treatment"
    __cardinality__ = "many"

    # The unique internal identifier for the AdditionalTreatment record
    additional_treatment_id: int | None = None

    # The unique internal identifier for the associated Participant record
    participant_id: str | None = (
        None  # TODO: fix all stage2 models for participant_id to not be nullable, after s1 models are complete
    )

    # Number of days from the enrollment date to the first recorded administration or occurrence of the treatment modality.
    days_to_start: NonNegativeInt | None = None

    # Number of days from the enrollment date to the last recorded administration or occurrence of the treatment modality.
    days_to_end: NonNegativeInt | None = None

    # Description of the prior treatment such as its full generic name if it is a type of therapy agent, radiotherapy procedure
    # name and location, or surgical procedure name and location.
    description: str
