from typing import Self

from pydantic import NonNegativeInt, model_validator

from .base import Base
from cidc_api.models.types import SurgicalProcedure, UberonAnatomicalTerm, YNU


class Surgery(Base):
    __data_category__ = "surgery"
    __cardinality__ = "many"

    # The unique internal identifier for the surgery record
    surgery_id: int | None = None

    # The unique internal identifier for the associated treatment record
    treatment_id: int | None = None

    # The term that describes the kind of surgical procedure administered.
    procedure: SurgicalProcedure

    # The name of surgical procedure if the value provided for procedure is "Other, specify".
    procedure_other: str | None = None

    # Number of days from enrollment date to surgical procedure date.
    days_to_procedure: NonNegativeInt

    # The Uberon identifier for the location within the body targeted by a procedure that
    # is intended to alter or stop a pathologic process.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=14980609%20and%20ver_nr=1
    anatomical_location: UberonAnatomicalTerm

    # An indication as to whether the surgical procedure in question was performed with therapeutic intent.
    therapeutic: YNU

    # A narrative description of any significant findings observed during the surgical procedure in question.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=14918773%20and%20ver_nr=1
    findings: str | None = None

    # A textual description of evidence for remaining tumor following primary treatment that is only
    # apparent using highly sensitive techniques.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=13362284%20and%20ver_nr=1
    extent_of_residual_disease: str | None = None

    @model_validator(mode="after")
    def validate_procedure_other_cr(self) -> Self:
        if self.procedure == "Other, specify" and not self.procedure_other:
            raise ValueError('If procedure is "Other, specify", please provide procedure_other.')
        return self
