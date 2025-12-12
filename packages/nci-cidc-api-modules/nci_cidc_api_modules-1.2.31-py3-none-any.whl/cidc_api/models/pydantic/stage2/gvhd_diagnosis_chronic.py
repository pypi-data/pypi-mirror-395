from .base import Base
from cidc_api.models.types import (
    GVHDDiagnosisChronicAssessmentSystem,
    GVHDDiagnosisChronicAssessmentSystemVersion,
    GVHDDiagnosisChronicGlobalSeverity,
    PreOrPostEnrollment,
)


class GVHDDiagnosisChronic(Base):
    __data_category__ = "gvhd_diagnosis_chronic"
    __cardinality__ = "many"

    # The unique internal identifier for the GVHD chronic diagnosis
    gvhd_diagnosis_chronic_id: int | None = None

    # The unique internal identifier for the associated participant
    participant_id: str | None = None

    # The standardized clinical system used to evaluate and grade the extent and severity
    # of organ involvement in chronic GVHD, resulting in an overall disease severity score.
    chronic_assessment_system: GVHDDiagnosisChronicAssessmentSystem

    # Release version of the clinical grading system used in the evaluation of chronic GVHD.
    system_version: GVHDDiagnosisChronicAssessmentSystemVersion

    # An overall score reflecting the combined severity of chronic graft-versus-host disease
    # across all affected organs, summarizing the participant’s total disease burden.
    chronic_global_severity: GVHDDiagnosisChronicGlobalSeverity

    # Indicator for whether the chronic GVHD diagnosis was made before or after trial enrollment.
    pre_or_post_enrollment: PreOrPostEnrollment
