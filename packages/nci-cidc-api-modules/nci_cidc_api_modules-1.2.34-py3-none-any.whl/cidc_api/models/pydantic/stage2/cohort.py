from .base import Base


class Cohort(Base):
    # A unique internal identifier for the cohort
    cohort_id: int | None = None

    # The unique identifier for the associated trial
    trial_id: str | None = None

    # The version number of the trial dataset
    version: str | None = None

    # The name of the cohort, e.g. "Cohort A"
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=7979585%20and%20ver_nr=1
    name: str
