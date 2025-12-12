from sqlalchemy import ForeignKeyConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cidc_api.models.db.base_orm import BaseORM
from cidc_api.models.types import AdministrativeRole


class AdministrativeRoleAssignmentORM(BaseORM):
    __tablename__ = "administrative_role_assignment"
    __repr_attrs__ = ["trial_id", "administrative_person_id", "administrative_role"]
    __table_args__ = (
        ForeignKeyConstraint(
            ["trial_id", "version"], ["stage2.trial.trial_id", "stage2.trial.version"], ondelete="CASCADE"
        ),
        {"schema": "stage2"},
    )

    trial_id: Mapped[str] = mapped_column(primary_key=True)
    version: Mapped[str] = mapped_column(primary_key=True)
    administrative_person_id: Mapped[int] = mapped_column(
        ForeignKey("stage2.administrative_person.administrative_person_id", ondelete="CASCADE"), primary_key=True
    )
    administrative_role: Mapped[AdministrativeRole] = mapped_column(primary_key=True)

    trial: Mapped["TrialORM"] = relationship(back_populates="administrative_role_assignments", cascade="all, delete")
    administrative_person: Mapped["AdministrativePersonORM"] = relationship(
        back_populates="administrative_role_assignments", cascade="all, delete"
    )
