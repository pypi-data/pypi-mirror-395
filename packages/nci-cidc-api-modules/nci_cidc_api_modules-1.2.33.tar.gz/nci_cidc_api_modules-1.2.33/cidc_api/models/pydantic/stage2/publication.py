from .base import Base


class Publication(Base):
    # The unique internal identifier for the Publication record
    publication_id: int | None = None

    # The unique internal identifier for the associated Trial record
    trial_id: int | None = None

    # The version number of the trial dataset
    version: str | None = None

    # The digital object identifier string. www.doi.org. e.g. 10.47366/sabia.v5n1a3
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=15915370%20and%20ver_nr=1
    digital_object_id: str

    # The pubmed identifier string. pubmed.ncbi.nlm.nih.gov. e.g. 41135560
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=15915377%20and%20ver_nr=1
    pubmed_id: str | None = None

    # The full title of the publication stated exactly as it appears on the published work.
    # https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=16078531%20and%20ver_nr=1
    publication_title: str | None = None

    # A list of authors for the cited work.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=16081468%20and%20ver_nr=1
    authorship: str | None = None

    # The year in which the cited work was published.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=16081475%20and%20ver_nr=1
    year_of_publication: str | None = None

    # The name of the journal in which the cited work was published, inclusive of the citation itself in terms of
    # journal volume number, part number where applicable, and page numbers.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=16081476%20and%20ver_nr=1
    journal_citation: str | None = None
