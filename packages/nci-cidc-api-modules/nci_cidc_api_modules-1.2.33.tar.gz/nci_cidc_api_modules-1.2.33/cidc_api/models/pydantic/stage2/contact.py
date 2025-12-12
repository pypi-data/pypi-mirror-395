from .base import Base


class Contact(Base):
    contact_id: int | None = None
    institution_id: int | None = None
    shipment_from_id: int | None = None
    shipment_to_id: int | None = None

    # The name of the contact
    name: str | None = None

    # The email address of the contact
    email: str | None = None

    # The phone number of the contact
    phone: str | None = None

    # Line 1 of the street address of the contact
    street1: str | None = None

    # Line 2 of the street address of the contact
    street2: str | None = None

    # The city where the contact is located
    city: str | None = None

    # The state where the contact is located
    state: str | None = None

    # The zip code where the contact is located
    zip: str | None = None

    # The country where the contact is located
    country: str | None = None
