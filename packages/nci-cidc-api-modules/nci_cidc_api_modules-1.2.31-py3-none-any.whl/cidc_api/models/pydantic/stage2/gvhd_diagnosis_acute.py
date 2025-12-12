from .base import Base
from cidc_api.models.types import (
    GVHDDiagnosisAcuteAssessmentSystem,
    GVHDDiagnosisAcuteAssessmentSystemVersion,
    GVHDDiagnosisAcuteGrade,
    PreOrPostEnrollment,
)


class GVHDDiagnosisAcute(Base):
    __data_category__ = "gvhd_diagnosis_acute"
    __cardinality__ = "many"

    # The unique internal identifier for the GVHD Diagnosis Acute Record
    gvhd_diagnosis_acute_id: int | None = None

    # The unique internal identifier for the associated participant
    participant_id: str | None = None

    # The clinical grading system used to stage involvement of affected organs (skin, liver, GI tract)
    # in acute GVHD and assign an overall severity grade (I–IV) based on predefined criteria.
    acute_assessment_system: GVHDDiagnosisAcuteAssessmentSystem

    # Release version of the clinical grading system used in the evaluation of acute GVHD.
    system_version: GVHDDiagnosisAcuteAssessmentSystemVersion

    # The overall severity grade (I–IV) assigned to a patient with acute GVHD based on the extent of
    # involvement in affected organs (skin, liver, and GI tract), determined using a standardized
    # assessment system.
    acute_grade: GVHDDiagnosisAcuteGrade

    # Indicator for whether the acute GVHD diagnosis was made before or after trial enrollment.
    pre_or_post_enrollment: PreOrPostEnrollment
