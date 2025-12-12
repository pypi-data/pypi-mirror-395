from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from cidc_api.models.db.base_orm import BaseORM
from cidc_api.models.types import AssayType, TrialOrganization, TrialFundingAgency, AgeGroup


class TrialORM(BaseORM):
    __tablename__ = "trial"
    __repr_attrs__ = ["trial_id", "version"]
    __table_args__ = {"schema": "stage2"}
    __data_category__ = "study"

    trial_id: Mapped[str] = mapped_column(primary_key=True)
    version: Mapped[str] = mapped_column(primary_key=True)

    primary_endpoint: Mapped[str | None]
    age_group: Mapped[List[AgeGroup]] = mapped_column(JSON, nullable=True)
    study_population: Mapped[str | None]
    nct_id: Mapped[str | None]
    nci_id: Mapped[str | None]
    trial_name: Mapped[str | None]
    trial_type: Mapped[str | None]
    trial_description: Mapped[str | None]
    trial_organization: Mapped[TrialOrganization | None]
    grant_or_affiliated_network: Mapped[TrialFundingAgency | None]
    biobank_institution_id: Mapped[int | None]
    justification: Mapped[str | None]
    dates_of_conduct_start: Mapped[datetime]
    dates_of_conduct_end: Mapped[datetime | None]
    schema_file_id: Mapped[int | None]
    biomarker_plan: Mapped[str | None]
    data_sharing_plan: Mapped[str | None]
    expected_assays: Mapped[List[AssayType]] = mapped_column(JSON, nullable=True)
    is_liquid_tumor_trial: Mapped[bool]
    dbgap_study_accession: Mapped[str | None]

    biobank: Mapped["InstitutionORM"] = relationship(back_populates="trial")
    schema: Mapped[Optional["FileORM"]] = relationship(back_populates="trial", viewonly=True)
    administrative_role_assignments: Mapped[List["AdministrativeRoleAssignmentORM"]] = relationship(
        back_populates="trial", cascade="all, delete", passive_deletes=True
    )
    arms: Mapped[List["ArmORM"]] = relationship(back_populates="trial", cascade="all, delete", passive_deletes=True)
    cohorts: Mapped[List["CohortORM"]] = relationship(
        back_populates="trial", cascade="all, delete", passive_deletes=True
    )
    participants: Mapped[List["ParticipantORM"]] = relationship(
        back_populates="trial", cascade="all, delete", passive_deletes=True
    )
    shipments: Mapped[List["ShipmentORM"]] = relationship(
        back_populates="trial", cascade="all, delete", passive_deletes=True
    )
    files: Mapped[List["FileORM"]] = relationship(back_populates="trial", cascade="all, delete", passive_deletes=True)
    publications: Mapped[List["PublicationORM"]] = relationship(
        back_populates="trial", cascade="all, delete", passive_deletes=True
    )
    consent_groups: Mapped[List["ConsentGroupORM"]] = relationship(
        back_populates="trial", cascade="all, delete", passive_deletes=True
    )
