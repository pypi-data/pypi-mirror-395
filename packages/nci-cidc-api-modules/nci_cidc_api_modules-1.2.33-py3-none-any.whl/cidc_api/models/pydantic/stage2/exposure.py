from typing import Self

from pydantic import model_validator

from .base import Base
from cidc_api.models.types import YNU, ExposureType


class Exposure(Base):
    __data_category__ = "exposure"
    __cardinality__ = "many"

    # A unique internal identifier for the exposure
    exposure_id: int | None = None

    # The unique identifier for the associated participant
    participant_id: str | None = None

    # An indication of whether the subject was exposed to any chemical, biological or physical agents
    # that increase the risk of neoplasms in humans or animals.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=5205578%20and%20ver_nr=3
    carcinogen_exposure: YNU

    # The type of potentially harmful environmental agents to which an individual was exposed.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=15753203%20and%20ver_nr=1
    exposure_type: ExposureType | None = None

    @model_validator(mode="after")
    def validate_exposure_type_cr(self) -> Self:
        if self.carcinogen_exposure in ["No", "Unknown"] and self.exposure_type:
            raise ValueError("If carcinogen_exposure indicates non exposure, please leave exposure_type blank.")
        return self
