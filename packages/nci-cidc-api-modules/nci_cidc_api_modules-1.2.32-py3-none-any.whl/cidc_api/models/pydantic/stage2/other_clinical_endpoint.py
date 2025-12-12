from .base import Base
from cidc_api.models.types import YNU, ResponseSystem, ResponseSystemVersion


class OtherClinicalEndpoint(Base):

    # The unique internal identifier for the other clinical endpoint
    other_clinical_endpoint_id: int | None = None

    # The unique internal identifier for the associated participant
    participant_id: int | None = None

    # The name of the clinical endpoint. e.g. "iPFS"
    name: str

    # Whether the event that defines the clinical endpoint occurred
    event: YNU

    # The number of days to the occurrence of the event
    days: int | None = None

    # A description of this clinical endpoint
    description: str | None = None

    # The formula used to calculate the clinical endpoint criteria
    calculation: str | None = None

    # The response system used to define the clinical endpoint criteria. e.g. "RECIST"
    response_system: ResponseSystem | None = None

    # The version of the system used to define the clinical endpoint criteria.
    response_system_version: ResponseSystemVersion | None = None
