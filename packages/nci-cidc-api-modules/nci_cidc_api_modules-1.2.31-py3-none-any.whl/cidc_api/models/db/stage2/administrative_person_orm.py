from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cidc_api.models.db.base_orm import BaseORM


class AdministrativePersonORM(BaseORM):
    __tablename__ = "administrative_person"
    __repr_attrs__ = ["first_name", "last_name"]
    __table_args__ = {"schema": "stage2"}

    administrative_person_id: Mapped[int] = mapped_column(primary_key=True)
    institution_id: Mapped[int] = mapped_column(ForeignKey("stage2.institution.institution_id", ondelete="CASCADE"))
    first_name: Mapped[str]
    middle_name: Mapped[str | None]
    last_name: Mapped[str]
    email: Mapped[str | None]
    phone_number: Mapped[str | None]

    institution: Mapped["InstitutionORM"] = relationship(back_populates="administrative_people", cascade="all, delete")
    administrative_role_assignments: Mapped[List["AdministrativeRoleAssignmentORM"]] = relationship(
        back_populates="administrative_person", cascade="all, delete", passive_deletes=True
    )
