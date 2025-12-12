from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cidc_api.models.db.base_orm import BaseORM
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


class SpecimenORM(BaseORM):
    __tablename__ = "specimen"
    __repr_attrs__ = ["specimen_id", "participant_id", "cimac_id"]
    __table_args__ = {"schema": "stage2"}

    specimen_id: Mapped[int] = mapped_column(primary_key=True)
    participant_id: Mapped[int] = mapped_column(ForeignKey("stage2.participant.participant_id", ondelete="CASCADE"))

    cimac_id: Mapped[str]
    surgical_pathology_report_id: Mapped[str | None]
    clinical_report_id: Mapped[str | None]
    parent_specimen_id: Mapped[str | None]
    processed_specimen_id: Mapped[str | None]
    organ_site_of_collection: Mapped[UberonAnatomicalTerm | None]
    histology_behavior: Mapped[ICDO3MorphologicalCode | None]
    histology_behavior_description: Mapped[str | None]
    collection_event_name: Mapped[str | None]
    specimen_type: Mapped[SpecimenType | None]
    specimen_type_other: Mapped[str | None]
    specimen_description: Mapped[SpecimenDescription | None]
    tumor_type: Mapped[TumorType | None]
    collection_procedure: Mapped[CollectionProcedure | None]
    collection_procedure_other: Mapped[str | None]
    core_number: Mapped[str | None]
    fixation_stabilization_type: Mapped[FixationStabilizationType | None]
    primary_container_type: Mapped[PrimaryContainerType | None]
    primary_container_type_other: Mapped[str | None]
    volume: Mapped[float | None]
    volume_units: Mapped[VolumeUnits | None]
    processed_type: Mapped[ProcessedType | None]
    processed_volume: Mapped[float | None]
    processed_volume_units: Mapped[VolumeUnits | None]
    processed_concentration: Mapped[float | None]
    processed_concentration_units: Mapped[ConcentrationUnits | None]
    processed_quantity: Mapped[float | None]
    derivative_type: Mapped[DerivativeType | None]
    derivative_volume: Mapped[float | None]
    derivative_volume_units: Mapped[VolumeUnits | None]
    derivative_concentration: Mapped[float | None]
    derivative_concentration_units: Mapped[ConcentrationUnits | None]
    tumor_tissue_total_area_percentage: Mapped[float | None]
    viable_tumor_area_percentage: Mapped[float | None]
    viable_stroma_area_percentage: Mapped[float | None]
    necrosis_area_percentage: Mapped[float | None]
    fibrosis_area_percentage: Mapped[float | None]
    din: Mapped[float | None]
    a260_a280: Mapped[float | None]
    a260_a230: Mapped[float | None]
    pbmc_viability: Mapped[float | None]
    pbmc_recovery: Mapped[float | None]
    pbmc_resting_period_used: Mapped[PBMCRestingPeriodUsed | None]
    material_used: Mapped[float | None]
    material_used_units: Mapped[MaterialUnits | None]
    material_remaining: Mapped[float | None]
    material_remaining_units: Mapped[MaterialUnits | None]
    material_storage_condition: Mapped[MaterialStorageCondition | None]
    qc_condition: Mapped[QCCondition | None]
    replacement_requested: Mapped[ReplacementRequested | None]
    residual_use: Mapped[ResidualUse | None]
    comments: Mapped[str | None]
    diagnosis_verification: Mapped[DiagnosisVerification | None]
    intended_assay: Mapped[AssayType | None]
    date_ingested: Mapped[datetime | None]
    days_to_specimen_collection: Mapped[int | None]

    participant: Mapped["ParticipantORM"] = relationship(back_populates="specimens", cascade="all, delete")
    shipment_specimen: Mapped["ShipmentSpecimenORM"] = relationship(
        back_populates="specimen", cascade="all, delete", passive_deletes=True
    )
