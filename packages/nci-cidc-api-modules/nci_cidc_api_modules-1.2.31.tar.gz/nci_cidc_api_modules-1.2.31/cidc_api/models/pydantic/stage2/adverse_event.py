from typing import Self

from pydantic import NonNegativeInt, model_validator

from .base import Base
from cidc_api.reference.ctcae import is_ctcae_other_term
from cidc_api.models.types import (
    CTCAEEventTerm,
    CTCAEEventCode,
    SeverityGradeSystem,
    SeverityGradeSystemVersion,
    SeverityGrade,
    SystemOrganClass,
    AttributionCause,
    AttributionLikelihood,
    YNU,
)


class AdverseEvent(Base):
    __data_category__ = "adverse_event"
    __cardinality__ = "many"

    # The unique internal identifier of the adverse event
    adverse_event_id: int | None = None

    # The unique internal identifier of the associated participant
    participant_id: str | None = None

    # The unique internal identifier of the attributed treatment, if any
    treatment_id: int | None = None

    # Text that represents the Common Terminology Criteria for Adverse Events low level term name for an adverse event.
    event_term: CTCAEEventTerm | None = None

    # A MedDRA code mapped to a CTCAE low level name for an adverse event.
    event_code: CTCAEEventCode | None = None

    # System used to define and report adverse event severity grade.
    severity_grade_system: SeverityGradeSystem

    # The version of the adverse event grading system.
    severity_grade_system_version: SeverityGradeSystemVersion

    # Numerical grade indicating the severity of an adverse event.
    severity_grade: SeverityGrade

    # A brief description that sufficiently details the event.
    event_other_specify: str | None = None

    # The highest level of the MedDRA hierarchy, distinguished by anatomical or physiological system, etiology (disease origin) or purpose.
    system_organ_class: SystemOrganClass | None = None

    # Indicator to identify whether a participant exited the study prematurely due to the adverse event being described.
    discontinuation_due_to_event: bool

    # Days from enrollment date to date of onset of the adverse event.
    days_to_onset_of_event: NonNegativeInt

    # Days from enrollment date to date of resolution of the adverse event.
    days_to_resolution_of_event: NonNegativeInt | None = None

    # Indicates whether the adverse event was a serious adverse event (SAE).
    serious_adverse_event: YNU

    # Indicates whether the adverse event was a dose-limiting toxicity (DLT).
    dose_limiting_toxicity: YNU

    # Indicates if the adverse was attributable to the protocol as a whole or to an individual treatment.
    attribution_cause: AttributionCause

    # The code that indicates whether the adverse event is related to the treatment/intervention.
    attribution_likelihood: AttributionLikelihood

    # The individual therapy (therapy agent, radiotherapy, surgery, stem cell transplant) in the treatment that is attributed to the adverse event.
    individual_therapy: str | None = None

    @model_validator(mode="after")
    def validate_term_and_code_cr(self) -> Self:
        if not self.event_term and not self.event_code:
            raise ValueError("Please provide event_term or event_code or both")
        return self

    @model_validator(mode="after")
    def validate_event_other_specify_cr(self) -> Self:
        if (
            self.severity_grade_system == "CTCAE"
            and is_ctcae_other_term(self.event_term)
            and not self.event_other_specify
        ):
            raise ValueError(
                'If severity_grade_system is "CTCAE" and the event_code or event_term are of type "Other, specify", please provide event_other_specify'
            )
        return self

    @model_validator(mode="after")
    def validate_system_organ_class_cr(self) -> Self:
        if self.event_other_specify and not self.system_organ_class:
            raise ValueError("If event_other_specify is provided, please provide system_organ_class.")
        return self
