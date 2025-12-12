from datetime import datetime

from .base import Base
from cidc_api.models.types import AssayPriority, AssayType, Courier, ShipmentCondition, ShipmentQuality


class Shipment(Base):
    # The unique internal identifier for the shipment record.
    shipment_id: int | None = None

    # The unique internal identifier for the associated institution.
    institution_id: int | None = None

    # The unique internal identifier for the associated trial.
    trial_id: int | None = None

    # The version number of the trial dataset
    version: str | None = None

    # The identifier of the manifest used to ship this sample. e.g. "E4412_PBMC"
    manifest_id: str

    # Priority of the assay as it appears on the intake form. e.g. "10"
    assay_priority: AssayPriority | None = None

    # The type of assay used. e.g. "Olink"
    assay_type: AssayType | None = None

    # Courier utilized for shipment. e.g. "FedEx"
    courier: Courier | None = None

    # Air bill number assigned to shipment. e.g. "4567788343"
    tracking_number: str | None = None

    # The environmental conditions of the shipment. e.g. "Frozen Dry Ice"
    condition: ShipmentCondition | None = None

    # Details of shipping condition when condition is "Other"
    condition_other: str | None = None

    # Date the shipment was posted
    date_shipped: datetime | None = None

    # Date the shipment was received
    date_received: datetime | None = None

    # Indication of the quality/condition of the specimens after receipt. e.g. "Damaged"
    quality: ShipmentQuality | None = None
