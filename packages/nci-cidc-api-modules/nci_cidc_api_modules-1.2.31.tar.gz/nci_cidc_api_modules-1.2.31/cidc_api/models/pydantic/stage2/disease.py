from pydantic import NonPositiveInt, model_validator, BeforeValidator
from typing import List, Self, Annotated, get_args

from .base import Base
from cidc_api.models.types import (
    TumorGrade,
    CancerStageSystem,
    CancerStageSystemVersion,
    CancerStageSystemVersionAJCC,
    CancerStageSystemVersionRISS,
    CancerStageSystemVersionFIGO,
    CancerStage,
    TCategory,
    NCategory,
    MCategory,
    UberonAnatomicalTerm,
    ICDO3MorphologicalCode,
    ICDO3MorphologicalTerm,
    YNU,
)


class Disease(Base):
    __data_category__ = "disease"
    __cardinality__ = "many"

    # The unique internal identifier for this disease record
    disease_id: int | None = None

    # The unique internal identifier for the associated participant
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=12220014%20and%20ver_nr=1
    participant_id: str | None = None

    # The location within the body from where the disease of interest originated as captured in the Uberon identifier. e.g. "lung"
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=14883047%20and%20ver_nr=1
    primary_disease_site: UberonAnatomicalTerm

    # The ICD-O-3 morphology code that describes the tumor's histology, behavior, and grade-differentiation. e.g. "8480/6"
    # CDE: TBD
    morphological_code: ICDO3MorphologicalCode | None

    # The ICD-O-3 morphology term that describes the tumor's type. e.g. "Mucinous adenoma"
    # CDE: TBD
    morphological_term: ICDO3MorphologicalTerm | None

    # Words that broadly describe the cancer's characteristics and type. e.g. "Inflitrating Ductal Carcinoma"
    # CDE: TBD
    cancer_type_description: str | None = None

    # The number of days elapsed since the participant was first diagnosed with this condition.
    days_since_original_diagnosis: NonPositiveInt | None

    # Words that express the degree of abnormality of cancer cells as a measure of differentiation and aggressiveness. e.g. "G1 Low Grade"
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=11325685%20and%20ver_nr=2
    tumor_grade: TumorGrade | None = None

    # The name of the staging system used in the evaluation of the disease. e.g. "AJCC"
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=7429602%20and%20ver_nr=1
    cancer_stage_system: CancerStageSystem

    # Release version of the staging system used in the evaluation of the disease. e.g. "8" (for AJCC)
    cancer_stage_system_version: CancerStageSystemVersion | None = None

    # Stage of the cancer at enrollment date as determined by the specific staging system. e.g. "Stage 0" (for AJCC)
    # CDE(AJCC): https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=3440332%20and%20ver_nr=1
    # CDE(FIGO): TBD
    # CDE(RISS): TBD
    cancer_stage: CancerStage | None = None

    # Extent of the primary cancer based on evidence obtained from clinical assessment parameters determined prior to treatment. e.g. "T0"
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=3440328%20and%20ver_nr=1
    # TODO: Verify this CDE
    t_category: TCategory | None = None

    # Extent of the regional lymph node involvement for the cancer based on evidence obtained from clinical assessment parameters
    # determined prior to treatment. e.g. "N0"
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=3440330%20and%20ver_nr=1
    # TODO: Verify this CDE
    n_category: NCategory | None = None

    # Extent of the distant metastasis for the cancer based on evidence obtained from clinical assessment parameters determined
    # prior to treatment. e.g. "M0"
    # CDE: https://teams.microsoft.com/l/message/19:1c292b63-5df1-4f29-b177-86aed53f393d_f224ae83-209b-4cd9-a7ef-83d9d2120a27@unq.gbl.spaces/1758827414202?context=%7B%22contextType%22%3A%22chat%22%7D
    # TODO: Verify this CDE
    m_category: MCategory | None = None

    # The organ site where a tumor develops outside of the bone marrow as specified in the Uberon antatomical term.
    metastatic_organ: Annotated[List[UberonAnatomicalTerm] | None, BeforeValidator(Base.split_list)] = []

    # Indicates if participant has a hematological malignancy that is only extramedullary. e.g. "Yes"
    solely_extramedullary_disease: YNU

    extramedullary_organ: Annotated[List[UberonAnatomicalTerm] | None, BeforeValidator(Base.split_list)] = []

    @model_validator(mode="after")
    def validate_code_or_term_or_description_cr(self) -> Self:
        if not self.morphological_code and not self.morphological_term and not self.cancer_type_description:
            raise ValueError(
                'Please provide at least one of "morphological_code", "morphological_term" or "cancer_type_description".'
            )
        return self

    @model_validator(mode="after")
    def validate_cancer_stage_system_version(self) -> Self:
        msg = f"{self.cancer_stage_system_version} is not applicable to {self.cancer_stage_system}"
        if self.cancer_stage_system == "AJCC" and self.cancer_stage_system_version not in get_args(
            CancerStageSystemVersionAJCC
        ):
            raise ValueError(msg)
        elif self.cancer_stage_system == "RISS" and self.cancer_stage_system_version not in get_args(
            CancerStageSystemVersionRISS
        ):
            raise ValueError(msg)
        elif self.cancer_stage_system == "FIGO" and self.cancer_stage_system_version not in get_args(
            CancerStageSystemVersionFIGO
        ):
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def validate_cancer_stage_system_version_cr(self) -> Self:
        if self.cancer_stage_system != "Not Applicable" and not self.cancer_stage_system_version:
            raise ValueError(
                f'Please provide cancer_stage_system_version when cancer_stage_system is "{self.cancer_stage_system}"'
            )
        return self

    @model_validator(mode="after")
    def validate_cancer_stage_cr(self) -> Self:
        if self.cancer_stage_system != "Not Applicable" and not self.cancer_stage:
            raise ValueError(f'Please provide cancer_stage when cancer_stage_system is "{self.cancer_stage_system}"')
        return self

    @model_validator(mode="after")
    def validate_t_category_cr(self) -> Self:
        if self.cancer_stage_system == "AJCC" and not self.t_category:
            raise ValueError(f'Please provide t_category when cancer_stage_system is "{self.cancer_stage_system}"')
        return self

    @model_validator(mode="after")
    def validate_n_category_cr(self) -> Self:
        if self.cancer_stage_system == "AJCC" and not self.n_category:
            raise ValueError(f'Please provide n_category when cancer_stage_system is "{self.cancer_stage_system}"')
        return self

    @model_validator(mode="after")
    def validate_m_category_cr(self) -> Self:
        if self.cancer_stage_system == "AJCC" and not self.m_category:
            raise ValueError(f'Please provide m_category when cancer_stage_system is "{self.cancer_stage_system}"')
        return self

    @model_validator(mode="after")
    def validate_extramedullary_organ_cr(self) -> Self:
        if self.solely_extramedullary_disease in ["No", "Unknown"] and self.extramedullary_organ:
            raise ValueError(
                "If solely_extramedullary_disease indicates no disease, please leave extramedullary_organ blank."
            )
        return self
