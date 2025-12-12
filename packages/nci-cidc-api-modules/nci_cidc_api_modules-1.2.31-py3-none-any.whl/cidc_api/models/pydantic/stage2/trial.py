from datetime import datetime
from typing import List

from .base import Base
from cidc_api.models.types import TrialOrganization, TrialFundingAgency, AssayType


class Trial(Base):
    __data_category__ = "study"
    __cardinality__ = None

    # The unique identifier for the clinical trial. e.g. "GU16-287","BACCI"
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=5054234%20and%20ver_nr=1
    trial_id: str | None = None  # TODO: Fix stage2 trial_id to not be nullable, once stage 1 models are complete

    # The version number of the trial dataset. e.g. "1.0"
    version: str | None = None

    # ClinicalTrials.gov identifier. e.g. "NCT03731260"
    # TODO need cde from janice, they will make one
    nct_id: str | None = None

    # NCI Trial Identifier. e.g. NCI22345
    # TODO need cde from janice, they will make one
    nci_id: str | None = None

    # The short name for the trial
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=11459810%20and%20ver_nr=4
    trial_name: str | None = None

    # The type of clinical trial conducted
    trial_type: str | None = None

    # The long description of the trial name and purpose. e.g. "BACCI: A Phase II Randomized, Double-Blind,
    # Placebo-Controlled Study of Capecitabine Bevacizumab plus Atezolizumab versus Capecitabine Bevacizumab
    # plus Placebo in Patients with Refractory Metastatic Colorectal Cancer"
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=16188024%20and%20ver_nr=1
    trial_description: str | None = None

    # Name of the primary organization that oversees the clinical trial. e.g. "ECOG-ACRIN", "SWOG"
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=3938773%20and%20ver_nr=2
    trial_organization: TrialOrganization | None = None

    # The primary organization providing grant funding and supporting the trial.
    # e.g. "Duke University - Duke Cancer Institute LAO"
    grant_or_affiliated_network: TrialFundingAgency | None = None

    # The id of the primary organization responsible for storing biospecimens from this study.
    biobank_institution_id: int | None = None

    # A description of the reasons why this study could provide insight into molecular biomarkers of immunotherapy.
    justification: str | None = None

    # The official day that study activity began
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=16333702%20and%20ver_nr=1
    dates_of_conduct_start: datetime

    # The official day that study activity ended
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=16333703%20and%20ver_nr=1
    dates_of_conduct_end: datetime | None = None

    # The image of the trial data schema
    schema_file_id: int | None = None

    # The description of the objectives and hypotheses for the proposed biomarkers.
    biomarker_plan: str | None = None

    # The description of the rules governing data sharing and publications.
    data_sharing_plan: str | None = None

    # The list of assays that CIDC expects to receive for this trial.
    expected_assays: List[AssayType] = []

    # Is the cancer studying a liquid tumor type?
    is_liquid_tumor_trial: bool = False

    # The dbgap study accession number associated with the trial.
    dbgap_study_accession: str | None = None

    # The internal version identifier for this specific trial dataset.
    version: str
