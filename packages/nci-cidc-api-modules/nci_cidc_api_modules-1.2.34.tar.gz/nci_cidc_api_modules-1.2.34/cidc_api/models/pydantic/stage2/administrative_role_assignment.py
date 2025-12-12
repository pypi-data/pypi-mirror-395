from .base import Base
from cidc_api.models.types import AdministrativeRole


class AdministrativeRoleAssignment(Base):
    # The unique identifier for the associated trial
    trial_id: int | None = None

    # The version number of the trial dataset
    version: str | None = None

    # The unique identifier for the associated administrative person
    administrative_person_id: int

    # The role the administrative_person is performing for the associated trial
    administrative_role: AdministrativeRole
