from .base import Base
from cidc_api.models.types import (
    GVHDOrgan,
    GVHDOrganChronicScore,
)


class GVHDOrganChronic(Base):
    __data_category__ = "gvhd_organ_chronic"
    __cardinality__ = "many"

    # The unique internal identifier for the GVHD Organ Chronic Record
    gvhd_organ_chronic_id: int | None = None

    # The unique internal identifier for the associated GVHD Diagnosis Chronic record
    gvhd_diagnosis_chronic_id: int | None = None

    # An organ affected by chronic GVHD identified by its Uberon ontology ID
    # and evaluated for severity as part of the overall chronic GVHD assessment.
    organ: GVHDOrgan

    # The severity score for an individual organ affected by chronic GVHD based on clinical criteria.
    chronic_score: GVHDOrganChronicScore
