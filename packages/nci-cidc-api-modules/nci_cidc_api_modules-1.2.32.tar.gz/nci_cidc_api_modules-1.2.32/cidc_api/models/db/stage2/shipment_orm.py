from datetime import datetime
from typing import Optional, List

from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cidc_api.models.db.base_orm import BaseORM
from cidc_api.models.types import AssayPriority, AssayType, Courier, ShipmentCondition, ShipmentQuality


class ShipmentORM(BaseORM):
    __tablename__ = "shipment"
    __repr_attrs__ = ["shipment_id", "institution_id", "trial_id"]
    __table_args__ = (
        ForeignKeyConstraint(
            ["trial_id", "version"], ["stage2.trial.trial_id", "stage2.trial.version"], ondelete="CASCADE"
        ),
        {"schema": "stage2"},
    )

    shipment_id: Mapped[int] = mapped_column(primary_key=True)
    institution_id: Mapped[int] = mapped_column(ForeignKey("stage2.institution.institution_id", ondelete="CASCADE"))
    trial_id: Mapped[str]
    version: Mapped[str]

    manifest_id: Mapped[str]
    assay_priority: Mapped[Optional[AssayPriority]]
    assay_type: Mapped[Optional[AssayType]]
    courier: Mapped[Optional[Courier]]
    tracking_number: Mapped[Optional[str]]
    condition: Mapped[Optional[ShipmentCondition]]
    condition_other: Mapped[Optional[str]]
    date_shipped: Mapped[Optional[datetime]]
    date_received: Mapped[Optional[datetime]]
    quality: Mapped[Optional[ShipmentQuality]]

    trial: Mapped["TrialORM"] = relationship(back_populates="shipments", cascade="all, delete")
    institution: Mapped["InstitutionORM"] = relationship(back_populates="shipments", cascade="all, delete")
    shipped_from: Mapped["ContactORM"] = relationship(
        back_populates="shipment_from", cascade="all, delete", foreign_keys="[ContactORM.shipment_from_id]"
    )
    shipped_to: Mapped["ContactORM"] = relationship(
        back_populates="shipment_to", cascade="all, delete", foreign_keys="[ContactORM.shipment_to_id]"
    )
    shipment_specimens: Mapped[List["ShipmentSpecimenORM"]] = relationship(
        back_populates="shipment", cascade="all, delete", passive_deletes=True
    )
