from pydantic import NonNegativeInt
from .base import Base
from cidc_api.models.types import (
    StemCellDonorType,
    AllogeneicDonorType,
    StemCellSource,
    ConditioningRegimenType,
)


class StemCellTransplant(Base):
    __data_category__ = "stem_cell_transplant"
    __cardinality__ = "many"

    # The unique internal identifier for the stem cell transplant record
    stem_cell_transplant_id: int | None = None

    # The unique internal identifier for the associated Treatment record
    treatment_id: int | None = None

    # Indicates the stem cell donor type.
    stem_cell_donor_type: StemCellDonorType

    # If "stem_cell_donor_type" is "Allogeneic", specifies the relationship and
    # compatibility of the donor relative to the receipient
    allogeneic_donor_type: AllogeneicDonorType | None = None

    # Source of the stem cells used for transplant.
    stem_cells_source: StemCellSource

    # Days from the enrollment date to the date of the stem cell transplant.
    days_to_transplant: NonNegativeInt

    # Specifies what type of conditioning regimen was used for the stem cell transplant if applicable.
    conditioning_regimen_type: ConditioningRegimenType | None = None
