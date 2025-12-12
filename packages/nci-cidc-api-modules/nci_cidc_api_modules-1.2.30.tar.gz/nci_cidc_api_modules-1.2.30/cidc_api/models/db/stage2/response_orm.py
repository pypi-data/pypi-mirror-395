from pydantic import NonNegativeInt

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cidc_api.models.db.base_orm import BaseORM
from cidc_api.models.types import SurvivalStatus, YNUNA, CauseOfDeath


class ResponseORM(BaseORM):
    __tablename__ = "response"
    __repr_attrs__ = ["response_id", "participant_id"]
    __table_args__ = {"schema": "stage2"}
    __data_category__ = "response"

    response_id: Mapped[int] = mapped_column(primary_key=True)
    participant_id: Mapped[int] = mapped_column(ForeignKey("stage2.participant.participant_id", ondelete="CASCADE"))
    survival_status: Mapped[SurvivalStatus]
    overall_survival: Mapped[NonNegativeInt | None]
    abscopal_response: Mapped[YNUNA | None]
    pathological_complete_response: Mapped[YNUNA | None]
    days_to_death: Mapped[NonNegativeInt | None]
    cause_of_death: Mapped[CauseOfDeath | None]
    evaluable_for_toxicity: Mapped[bool]
    evaluable_for_efficacy: Mapped[bool]
    days_to_last_follow_up: Mapped[NonNegativeInt | None]

    participant: Mapped["ParticipantORM"] = relationship(back_populates="response", cascade="all, delete")
