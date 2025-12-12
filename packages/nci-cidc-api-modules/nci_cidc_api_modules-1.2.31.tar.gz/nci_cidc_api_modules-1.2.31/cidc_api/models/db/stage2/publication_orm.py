from typing import Optional, List

from sqlalchemy import ForeignKeyConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cidc_api.models.db.base_orm import BaseORM
from cidc_api.models.types import PriorTreatmentType, ConditioningRegimenType, StemCellDonorType


class PublicationORM(BaseORM):
    __tablename__ = "publication"
    __repr_attrs__ = ["publication_id", "publication_title"]
    __table_args__ = (
        ForeignKeyConstraint(
            ["trial_id", "version"], ["stage2.trial.trial_id", "stage2.trial.version"], ondelete="CASCADE"
        ),
        {"schema": "stage2"},
    )

    publication_id: Mapped[int] = mapped_column(primary_key=True)
    trial_id: Mapped[str]
    version: Mapped[str]

    digital_object_id: Mapped[str]
    pubmed_id: Mapped[Optional[str]]
    publication_title: Mapped[Optional[str]]
    authorship: Mapped[Optional[str]]
    year_of_publication: Mapped[Optional[str]]
    journal_citation: Mapped[Optional[str]]

    trial: Mapped["TrialORM"] = relationship(back_populates="publications", cascade="all, delete")
