from .base import Base
from cidc_api.models.types import (
    GVHDOrgan,
    GVHDOrganAcuteStage,
)


class GVHDOrganAcute(Base):
    __data_category__ = "gvhd_organ_acute"
    __cardinality__ = "many"

    # The unique internal identifier for the GVHD Organ Acute Record
    gvhd_organ_acute_id: int | None = None

    # The unique internal identifier for the associated GVHD Diagnosis Acute record
    gvhd_diagnosis_acute_id: int | None = None

    # An organ affected by acute GVHD for which the stage is assessed as part of the overall acute GVHD evaluation.
    organ: GVHDOrgan

    # The severity level of an individual organ’s involvement in acute GVHD, usually scored from 0 (none) to 4 (severe).
    acute_stage: GVHDOrganAcuteStage
