from typing import Self

from pydantic import model_validator

from .base import Base
from cidc_api.models.types import YNU
from cidc_api.models.types import OffStudyReason


class Participant(Base):
    __data_category__ = "participant"
    __cardinality__ = "one"

    # The unique internal identifier for the participant
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=12220014%20and%20ver_nr=1
    participant_id: str | None = None

    # The participant identifier assigned by the clinical trial team overseeing the study
    native_participant_id: str | None = None

    # The globally unique participant identifier assigned by the CIMAC network. e.g. C8P29A7
    cimac_participant_id: str | None = None

    # The unique identifier for the associated trial that the participant is participating in
    trial_id: int | None = None

    # Indicates if the individual is no longer actively participating in the clinical trial.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=14834973%20and%20ver_nr=1
    off_study: YNU

    # An explanation describing why an individual is no longer participating in the clinical trial.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=13362265%20and%20ver_nr=1
    off_study_reason: OffStudyReason | None = None

    # Additional information if "Other" is selected for off_study_reason. e.g. "Transfer to another study"
    off_study_reason_other: str | None = None

    @model_validator(mode="after")
    def off_study_reason_cr(self) -> Self:
        if self.off_study == "Yes" and not self.off_study_reason:
            raise ValueError('If "off_study" is "Yes" then "off_study_reason" is required.')
        return self

    @model_validator(mode="after")
    def off_study_reason_other_cr(self) -> Self:
        if self.off_study_reason == "Other" and not self.off_study_reason_other:
            raise ValueError('If "off_study_reason" is "Other" then "off_study_reason_other" is required.')
        return self
