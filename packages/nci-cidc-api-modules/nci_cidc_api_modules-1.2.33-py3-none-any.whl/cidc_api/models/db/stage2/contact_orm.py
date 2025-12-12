from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cidc_api.models.db.base_orm import BaseORM


class ContactORM(BaseORM):
    __tablename__ = "contact"
    __table_args__ = {"schema": "stage2"}

    contact_id: Mapped[int] = mapped_column(primary_key=True)
    institution_id: Mapped[int] = mapped_column(ForeignKey("stage2.institution.institution_id", ondelete="CASCADE"))
    shipment_from_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("stage2.shipment.shipment_id", ondelete="CASCADE")
    )
    shipment_to_id: Mapped[Optional[int]] = mapped_column(ForeignKey("stage2.shipment.shipment_id", ondelete="CASCADE"))

    name: Mapped[Optional[str]]
    email: Mapped[Optional[str]]
    phone: Mapped[Optional[str]]
    street1: Mapped[Optional[str]]
    street2: Mapped[Optional[str]]
    city: Mapped[Optional[str]]
    state: Mapped[Optional[str]]
    zip: Mapped[Optional[str]]
    country: Mapped[Optional[str]]

    institution: Mapped[Optional["InstitutionORM"]] = relationship(back_populates="contacts", cascade="all, delete")
    shipment_from: Mapped["ShipmentORM"] = relationship(cascade="all, delete", foreign_keys=[shipment_from_id])
    shipment_to: Mapped["ShipmentORM"] = relationship(cascade="all, delete", foreign_keys=[shipment_to_id])
