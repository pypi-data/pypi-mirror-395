from typing import Self

from pydantic import NonNegativeInt, PositiveFloat, model_validator

from .base import Base
from cidc_api.models.types import TobaccoSmokingStatus


class MedicalHistory(Base):
    __data_category__ = "medical_history"
    __cardinality__ = "one"

    # A unique internal identifier for the medical history
    medical_history_id: int | None = None

    # The unique identifier for the associated participant
    participant_id: str | None = None

    # Text representation of a person's status relative to smoking tobacco in the form of cigarettes,
    # based on questions about current and former use of cigarettes.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=16333929%20and%20ver_nr=1
    tobacco_smoking_status: TobaccoSmokingStatus | None = None

    # Average number of packs of cigarettes smoked per day multiplied by number of years the participant has smoked.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=6841869%20and%20ver_nr=1
    pack_years_smoked: PositiveFloat | None = None

    # Number of prior systemic therapies.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=16089302%20and%20ver_nr=1
    num_prior_systemic_therapies: NonNegativeInt | None = None

    @model_validator(mode="after")
    def validate_pack_years_smoked_cr(self) -> Self:
        if self.tobacco_smoking_status in ["Never Smoker", "Unknown", "Not reported"] and self.pack_years_smoked:
            raise ValueError("If tobacco_smoking_status indicates non-smoker, please leave pack_years_smoked blank.")
        return self
