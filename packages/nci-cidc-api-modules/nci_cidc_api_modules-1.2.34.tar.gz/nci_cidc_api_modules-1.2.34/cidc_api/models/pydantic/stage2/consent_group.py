from pydantic import NonNegativeInt

from .base import Base


class ConsentGroup(Base):
    __data_category__ = "consent_group"
    __cardinality__ = "one"

    # The unique internal identifier for the consent group record
    consent_group_id: int | None = None

    # The unique internal identifier for the associated Trial record
    trial_id: int | None = None

    # The version number of the trial dataset
    version: str | None = None

    # An abbreviated name for the consent group
    consent_group_short_name: str

    # The words or acronym which describe a set of study participants
    # who have signed the same consent agreement and that will be included in the dbGaP repository.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=14534329%20and%20ver_nr=1.00
    consent_group_name: str

    # A numeral or string of numerals used to identify the set of study participants who have signed the same consent
    # agreement and that will be included in the dbGaP repository.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=14534330%20and%20ver_nr=1.00
    consent_group_number: NonNegativeInt
