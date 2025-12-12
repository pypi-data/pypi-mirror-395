from datetime import datetime

from .base import Base
from cidc_api.models.types import (
    UberonAnatomicalTerm,
    ICDO3MorphologicalCode,
    SpecimenType,
    SpecimenDescription,
    TumorType,
    CollectionProcedure,
    FixationStabilizationType,
    PrimaryContainerType,
    VolumeUnits,
    ProcessedType,
    ConcentrationUnits,
    DerivativeType,
    PBMCRestingPeriodUsed,
    MaterialUnits,
    MaterialStorageCondition,
    QCCondition,
    ReplacementRequested,
    ResidualUse,
    DiagnosisVerification,
    AssayType,
)


class Specimen(Base):
    # __data_category__ = "specimen"
    __cardinality__ = "many"

    # The unique internal identifier for the specimen record
    specimen_id: int | None = None

    # The unique internal identifier for the associated participant
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=12220014%20and%20ver_nr=1
    participant_id: str | None = None

    # The unique specimen identifier assigned by the CIMAC-CIDC Network.
    # Formatted as CTTTPPPSS.AA for trial code TTT, participant PPP, sample SS, and aliquot AA.
    cimac_id: str

    # The external identifier for the pathology report
    surgical_pathology_report_id: str | None = None

    # The external identifier for the clinical report
    clinical_report_id: str | None = None

    # The unique identifier for the specimen from which this specimen was derived
    parent_specimen_id: str | None = None

    # The unique identifier for the specimen after undergoing processing
    processed_specimen_id: str | None = None

    # The location within the body from which a specimen was originally obtained as captured in the Uberon anatomical term.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=12083894%20and%20ver_nr=1
    organ_site_of_collection: UberonAnatomicalTerm | None = None

    # ICD-O-3 code for histology and behavior. e.g. 9665/3"
    # CDE: TBD
    histology_behavior: ICDO3MorphologicalCode | None = None

    # Histology description. e.g. Hodgkin lymphoma, nod. scler., grade 1",
    histology_behavior_description: str | None = None

    # Categorical description of timepoint at which the sample was taken.
    # CDE: https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=5899851%20and%20ver_nr=1
    # Note: CIDC doesn't conform to this CDE's PVs
    collection_event_name: str | None = None

    # The type of the specimen
    specimen_type: SpecimenType | None = None

    # The type of the specimen, if not captured by specimen_type
    specimen_type_other: str | None = None

    # A general description of the specimen
    specimen_description: SpecimenDescription | None = None

    # The type of the tumor present in the specimen
    tumor_type: TumorType | None = None

    # Description of the procedure used to collect the specimen from the participant
    collection_procedure: CollectionProcedure | None = None

    # Description of the procedure used to collect the specimen from the participant, if not captured by collection_procedure
    collection_procedure_other: str | None = None

    # The biopsy core number from which the sample was taken.
    core_number: str | None = None

    # Type of specimen fixation or stabilization that was employed by the site directly after collection.
    fixation_stabilization_type: FixationStabilizationType | None = None

    # The type of container in which the specimen was shipped
    primary_container_type: PrimaryContainerType | None = None

    # The type of container in which the specimen was shipped, if not captured by primary_container_type
    primary_container_type_other: str | None = None

    # Volume of the specimen
    volume: float | None = None

    # The unit of measure of the volume of the specimen
    volume_units: VolumeUnits | None = None

    # The type of processing that was performed on the collected specimen by the biobank
    processed_type: ProcessedType | None = None

    # The volume of the specimen after being processed by the biobank
    processed_volume: float | None = None

    # The unit of measure of the volume of the specimen after being processed by the biobank
    processed_volume_units: VolumeUnits | None = None

    # The concentration of the sample after being processed by the biobank
    processed_concentration: float | None = None

    # The unit of measure of the concentration of the sample after being processed by the biobank
    processed_concentration_units: ConcentrationUnits | None = None

    # The quantity of the sample after being processed by the biobank
    processed_quantity: float | None = None

    # The type of the sample derivative
    derivative_type: DerivativeType | None = None

    # The volume of the sample derivative
    derivative_volume: float | None = None

    # The unit of measure of the volume of the sample derivative
    derivative_volume_units: VolumeUnits | None = None

    # The concentration of the sample derivative
    derivative_concentration: float | None = None

    # The unit of measure of the concentration of the sample derivative
    derivative_concentration_units: ConcentrationUnits | None = None

    # Score the percentage of tumor (including tumor bed) tissue area of the slide (e.g. vs non-malignant or normal tissue) (0-100)
    tumor_tissue_total_area_percentage: float | None = None

    # Score the percentage of viable tumor cells comprising the tumor bed area
    viable_tumor_area_percentage: float | None = None

    # Score the evaluation of stromal elements (this indicates the % area of tumor bed occupied by non-tumor cells,
    # including inflammatory cells [lymphocytes, histiocytes, etc], endothelial cells, fibroblasts, etc)
    viable_stroma_area_percentage: float | None = None

    # Score the percentage area of necrosis
    necrosis_area_percentage: float | None = None

    # Score the percentage area of Fibrosis
    fibrosis_area_percentage: float | None = None

    # Provides a DNA Integrity Number as an indication of extraction quality (values of 1-10)
    din: float | None = None

    # Provides an absorbance percentage ratio indicating purity of DNA (values of 0 to 2)
    a260_a280: float | None = None

    # Provides an absorbance percentage ratio indicating presence of contaminants (values of 0 to 3)
    a260_a230: float | None = None

    # Receiving site determines the percent recovered cells that are viable after thawing.
    pbmc_viability: float | None = None

    # Receiving site determines number for PBMCs per vial recovered upon receipt.
    pbmc_recovery: float | None = None

    # Receiving site indicates if a resting period was used after PBMC recovery.
    pbmc_resting_period_used: PBMCRestingPeriodUsed | None = None

    # Receiving site indicates how much material was used for assay purposes.
    material_used: float | None = None

    # Unit of measure for the amount of material used
    material_used_units: MaterialUnits | None = None

    # Receiving site indicates how much material remains after assay use.
    material_remaining: float | None = None

    # Unit of measure for the amount of material remaining.
    material_remaining_units: MaterialUnits | None = None

    # Storage condition of the material once it was received.
    material_storage_condition: MaterialStorageCondition | None = None

    # Final status of sample after QC and pathology review.
    qc_condition: QCCondition | None = None

    # Indication if sample replacement is/was requested.
    replacement_requested: ReplacementRequested | None = None

    # Indication if sample was sent to another location or returned back to biorepository.
    residual_use: ResidualUse | None = None

    # Additional comments on sample testing
    comments: str | None = None

    # Indicates whether the local pathology review was consistent with the diagnostic pathology report.
    diagnosis_verification: DiagnosisVerification | None = None

    # The assay that this sample is expected to be used as input for.
    intended_assay: AssayType | None = None

    # The datetime that CIDC ingested the sample/manifest
    date_ingested: datetime | None = None

    # Days from enrollment date to date specimen was collected.
    days_to_specimen_collection: int | None = None
