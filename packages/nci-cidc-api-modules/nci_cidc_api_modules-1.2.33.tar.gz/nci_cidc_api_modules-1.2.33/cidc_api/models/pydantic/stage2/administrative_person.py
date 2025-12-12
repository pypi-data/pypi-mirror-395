from .base import Base


class AdministrativePerson(Base):

    # The unique internal identifier for the administrative person
    administrative_person_id: int | None = None

    # The internal identifier for the Institution the administrative person belongs to
    institution_id: int | None = None

    # The word or group of words indicating a person's first (personal or given) name, e.g. "John"
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2179589%20and%20ver_nr=2
    first_name: str

    # The word or group of worlds indicating a person's middle name, e.g. "Alan"
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2179590%20and%20ver_nr=2
    middle_name: str | None = None

    # The means of identifying an individual by using a word or group of words indicating a person's last (family) name, e.g. "Smith"
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2179591%20and%20ver_nr=2
    last_name: str

    # The string of characters that represents the electronic mail address of a person.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2517550%20and%20ver_nr=1
    email: str | None = None

    # The string of digits that represent a telephone number that can be used to contact the person.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2179593%20and%20ver_nr=3
    phone_number: str | None = None
