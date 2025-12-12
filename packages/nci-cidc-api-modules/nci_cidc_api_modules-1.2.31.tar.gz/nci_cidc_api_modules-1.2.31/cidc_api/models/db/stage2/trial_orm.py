from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from cidc_api.models.db.base_orm import BaseORM
from cidc_api.models.types import AssayType, TrialOrganization, TrialFundingAgency


class TrialORM(BaseORM):
    __tablename__ = "trial"
    __repr_attrs__ = ["trial_id", "version"]
    __table_args__ = {"schema": "stage2"}
    __data_category__ = "study"

    trial_id: Mapped[str] = mapped_column(primary_key=True)
    version: Mapped[str] = mapped_column(primary_key=True)

    nct_id: Mapped[Optional[str]]
    nci_id: Mapped[Optional[str]]
    trial_name: Mapped[Optional[str]]
    trial_type: Mapped[Optional[str]]
    trial_description: Mapped[Optional[str]]
    trial_organization: Mapped[Optional[TrialOrganization]]
    grant_or_affiliated_network: Mapped[Optional[TrialFundingAgency]]
    biobank_institution_id: Mapped[Optional[int]]
    justification: Mapped[Optional[str]]
    dates_of_conduct_start: Mapped[datetime]
    dates_of_conduct_end: Mapped[Optional[datetime]]
    schema_file_id: Mapped[Optional[int]]
    biomarker_plan: Mapped[Optional[str]]
    data_sharing_plan: Mapped[Optional[str]]
    expected_assays: Mapped[Optional[List[AssayType]]] = mapped_column(JSON, nullable=True)
    is_liquid_tumor_trial: Mapped[bool]
    dbgap_study_accession: Mapped[Optional[str]]

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
