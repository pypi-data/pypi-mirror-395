from .base import Base
from cidc_api.models.types import ECOGScore, KarnofskyScore


class BaselineClinicalAssessment(Base):
    __data_category__ = "baseline_clinical_assessment"
    __cardinality__ = "one"

    # A unique internal identifier for the baseline clinical assessment
    baseline_clinical_assessment_id: int | None = None

    # The unique identifier for the associated participant
    participant_id: str | None = None

    # The numerical score that represents the functional capabilities of a participant at the
    # enrollment date using the Eastern Cooperative Oncology Group Performance Status assessment.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=88%20and%20ver_nr=5.1
    ecog_score: ECOGScore | None = None

    # Score from the Karnofsky Performance status scale, representing the functional capabilities of a participant
    # at the enrollment date.
    # CDE: 	https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2003853%20and%20ver_nr=4.2
    karnofsky_score: KarnofskyScore | None = None
