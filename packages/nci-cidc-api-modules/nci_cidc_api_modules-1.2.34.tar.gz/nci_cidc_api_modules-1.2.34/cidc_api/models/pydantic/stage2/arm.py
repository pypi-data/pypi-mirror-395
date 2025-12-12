from .base import Base


class Arm(Base):
    # The unique internal identifier for the arm
    arm_id: int | None = None

    # The unique identifier for the associated trial
    trial_id: int | None = None

    # The version number of the trial dataset
    version: str | None = None

    # The name of the arm, e.g. "Arm A1"
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2001626%20and%20ver_nr=3
    name: str
