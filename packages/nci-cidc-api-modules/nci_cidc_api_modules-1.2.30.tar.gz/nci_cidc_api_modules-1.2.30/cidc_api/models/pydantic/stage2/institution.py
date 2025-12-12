from .base import Base


class Institution(Base):

    # A unique internal identifier for the Institution
    institution_id: int | None = None

    # The name by which the institution is known, e.g. "MATCH Central Pathology Lab"
    name: str
