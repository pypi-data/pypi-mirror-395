from typing import Self

from pydantic import NonPositiveInt, model_validator

from .base import Base
from cidc_api.models.types import UberonAnatomicalTerm, ICDO3MorphologicalCode, ICDO3MorphologicalTerm, MalignancyStatus


class OtherMalignancy(Base):
    __data_category__ = "other_malignancy"
    __cardinality__ = "many"

    # The unique internal identifier for the OtherMalignancy record
    other_malignancy_id: int | None = None

    # The unique internal identifier for the associated MedicalHistory record
    medical_history_id: int | None = None

    # The location within the body from where the prior malignancy originated as captured in the Uberon anatomical term.
    primary_disease_site: UberonAnatomicalTerm

    # The ICD-O-3 code which identifies the specific appearance of cells and tissues (normal and abnormal) used
    # to define the presence and nature of disease.
    morphological_code: ICDO3MorphologicalCode | None = None

    # The ICD-O-3 textual label which identifies the specific appearance of cells and tissues (normal and abnormal) used
    # to define the presence and nature of disease.
    morphological_term: ICDO3MorphologicalTerm | None = None

    # Description of the cancer type as recorded in the trial.
    malignancy_description: str | None = None

    # Number of days since original diagnosis from the enrollment date. This may be a negative number.
    days_since_diagnosis: NonPositiveInt | None = None

    # Indicates the participant’s current clinical state regarding the cancer diagnosis.
    malignancy_status: MalignancyStatus | None = None

    @model_validator(mode="after")
    def validate_code_or_term_or_description_cr(self) -> Self:
        if not self.morphological_code and not self.morphological_term and not self.malignancy_description:
            raise ValueError(
                'Please provide at least one of "morphological_code", "morphological_term" or "malignancy_description".'
            )
        return self
