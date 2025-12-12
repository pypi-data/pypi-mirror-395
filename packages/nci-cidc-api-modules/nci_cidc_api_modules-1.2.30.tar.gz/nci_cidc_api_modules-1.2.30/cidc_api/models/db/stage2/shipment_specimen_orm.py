from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cidc_api.models.db.base_orm import BaseORM


class ShipmentSpecimenORM(BaseORM):
    __tablename__ = "shipment_specimen"
    __repr_attrs__ = ["specimen_id", "shipment_id"]
    __table_args__ = {"schema": "stage2"}

    specimen_id: Mapped[int] = mapped_column(
        ForeignKey("stage2.specimen.specimen_id", ondelete="CASCADE"), primary_key=True
    )
    shipment_id: Mapped[int] = mapped_column(
        ForeignKey("stage2.shipment.shipment_id", ondelete="CASCADE"), primary_key=True
    )
    box_number: Mapped[str]
    sample_location: Mapped[str]

    specimen: Mapped["SpecimenORM"] = relationship(back_populates="shipment_specimen", cascade="all, delete")
    shipment: Mapped["ShipmentORM"] = relationship(back_populates="shipment_specimens", cascade="all, delete")
