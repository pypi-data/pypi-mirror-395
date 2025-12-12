from .base import Base


class ShipmentSpecimen(Base):
    # The unique internal identifier of the associated specimen
    specimen_id: int | None = None

    # The unique internal identifier of the associated shipment
    shipment_id: int | None = None

    # Identifier if sample shipment container includes multiple boxes for each assay. e.g. "1", "X"
    box_number: str

    # Sample location within the shipping container. e.g. "A1"
    sample_location: str
