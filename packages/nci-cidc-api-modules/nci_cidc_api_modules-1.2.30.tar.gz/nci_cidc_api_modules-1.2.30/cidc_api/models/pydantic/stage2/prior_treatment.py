from typing import Self

from pydantic import NonPositiveInt, NonNegativeInt, model_validator

from .base import Base
from cidc_api.models.types import PriorTreatmentType, ConditioningRegimenType, StemCellDonorType


class PriorTreatment(Base):
    __data_category__ = "prior_treatment"
    __cardinality__ = "many"

    # A unique internal identifier for the prior treatment record
    prior_treatment_id: int | None = None

    # A unique internal identifier for the associated participant record
    participant_id: str | None = None

    # Number of days from the enrollment date to the first recorded administration or occurrence of
    # the treatment modality.
    days_to_start: NonPositiveInt | None = None

    # Number of days from the enrollment date to the last recorded administration or occurrence of
    # the treatment modality.
    days_to_end: NonPositiveInt | None = None

    # Specifies the category or kind of prior treatment modality a participant received.
    type: PriorTreatmentType

    # Description of the prior treatment such as its full generic name if it is a type of therapy agent,
    # radiotherapy procedure name and location, or surgical procedure name and location.
    description: str | None = None

    # Best response from any response assessment system to the prior treatment if available or applicable.
    best_response: str | None = None

    # If the prior treatment is "Conditioning therapy" received before a stem cell transplant, specifies what
    # type of conditioning regimen used.
    conditioning_regimen_type: ConditioningRegimenType | None = None

    # If prior treatment is "Stem cell transplant", indicates what stem cell donor type used.
    stem_cell_donor_type: StemCellDonorType | None = None

    # If prior treatment is "Stem cell transplant", indicates the number of days from the transplant
    # date to the start of the current treatment.
    days_from_transplant_to_treatment_initiation: NonNegativeInt | None = None

    @model_validator(mode="after")
    def validate_description_cr(self) -> Self:
        if self.type == "Other therapy" and not self.description:
            raise ValueError('If type is "Other therapy", please provide description.')
        return self
