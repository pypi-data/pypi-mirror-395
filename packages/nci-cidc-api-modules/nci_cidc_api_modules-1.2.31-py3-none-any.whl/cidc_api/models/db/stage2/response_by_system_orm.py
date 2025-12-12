from pydantic import PositiveInt
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cidc_api.models.db.base_orm import BaseORM
from cidc_api.models.types import ResponseSystem, ResponseSystemVersion, BestOverallResponse, YNUNA


class ResponseBySystemORM(BaseORM):
    __tablename__ = "response_by_system"
    __repr_attrs__ = ["response_by_system_id", "participant_id"]
    __table_args__ = {"schema": "stage2"}
    __data_category__ = "response_by_system"

    response_by_system_id: Mapped[int] = mapped_column(primary_key=True)
    participant_id: Mapped[int] = mapped_column(ForeignKey("stage2.participant.participant_id", ondelete="CASCADE"))
    response_system: Mapped[ResponseSystem] = mapped_column(String)
    response_system_version: Mapped[ResponseSystemVersion] = mapped_column(String)
    best_overall_response: Mapped[BestOverallResponse] = mapped_column(String)
    response_duration: Mapped[PositiveInt | None]
    durable_clinical_benefit: Mapped[bool | None]
    days_to_first_response: Mapped[PositiveInt | None]
    days_to_best_response: Mapped[PositiveInt | None]
    progression: Mapped[YNUNA]
    days_to_disease_progression: Mapped[PositiveInt | None]
    progression_free_survival_event: Mapped[YNUNA]
    progression_free_survival: Mapped[PositiveInt | None]

    participant: Mapped["ParticipantORM"] = relationship(back_populates="response_by_systems", cascade="all, delete")
