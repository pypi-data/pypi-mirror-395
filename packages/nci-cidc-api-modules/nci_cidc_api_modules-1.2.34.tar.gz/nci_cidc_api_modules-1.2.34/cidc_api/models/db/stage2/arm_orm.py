from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cidc_api.models.db.base_orm import BaseORM


class ArmORM(BaseORM):
    __tablename__ = "arm"
    __repr_attrs__ = ["trial_id", "arm_name"]
    __table_args__ = (
        ForeignKeyConstraint(
            ["trial_id", "version"], ["stage2.trial.trial_id", "stage2.trial.version"], ondelete="CASCADE"
        ),
        {"schema": "stage2"},
    )

    arm_id: Mapped[int] = mapped_column(primary_key=True)
    trial_id: Mapped[str]
    version: Mapped[str]

    name: Mapped[str]

    trial: Mapped["TrialORM"] = relationship(back_populates="arms", cascade="all, delete")
