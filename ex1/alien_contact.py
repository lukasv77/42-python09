from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def check_rules(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC'")
        if self.contact_type == ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")
        is_telepathic = self.contact_type == ContactType.TELEPATHIC
        if is_telepathic and self.witness_count < 3:
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
            )
        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError(
                "Strong signals (> 7.0) should include received messages"
            )
        return self


def show_contact(contact: AlienContact) -> None:
    print(f"ID: {contact.contact_id}")
    print(f"Type: {contact.contact_type.value}")
    print(f"Location: {contact.location}")
    print(f"Signal: {contact.signal_strength}/10")
    print(f"Duration: {contact.duration_minutes} minutes")
    print(f"Witnesses: {contact.witness_count}")
    if contact.message_received:
        print(f"Message: '{contact.message_received}'")


def print_errors(error: ValidationError) -> None:
    for err in error.errors():
        print(err["msg"].removeprefix("Value error, "))


def main() -> None:
    print("Alien Contact Log Validation")
    print("=" * 38)

    try:
        contact = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime(2024, 3, 14, 23, 42),
            location="Area 51, Nevada",
            contact_type=ContactType.RADIO,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli",
        )
        print("Valid contact report:")
        show_contact(contact)
    except ValidationError as e:
        print_errors(e)

    print()
    print("=" * 38)
    print("Expected validation error:")
    try:
        AlienContact(
            contact_id="AC_2024_002",
            timestamp=datetime(2024, 4, 1, 3, 15),
            location="Roswell, New Mexico",
            contact_type=ContactType.TELEPATHIC,
            signal_strength=4.0,
            duration_minutes=10,
            witness_count=1,
        )
    except ValidationError as e:
        print_errors(e)

    invalid_reports = [
        {
            "contact_id": "XX_2024_003",
            "timestamp": "2024-05-10T12:00:00",
            "location": "Gdansk, Poland",
            "contact_type": "visual",
            "signal_strength": 3.0,
            "duration_minutes": 5,
            "witness_count": 2,
        },
        {
            "contact_id": "AC_2024_004",
            "timestamp": "2024-06-21T22:30:00",
            "location": "Tunguska, Siberia",
            "contact_type": "physical",
            "signal_strength": 5.5,
            "duration_minutes": 120,
            "witness_count": 4,
        },
        {
            "contact_id": "AC_2024_005",
            "timestamp": "2024-07-04T01:00:00",
            "location": "Atacama Desert, Chile",
            "contact_type": "radio",
            "signal_strength": 9.1,
            "duration_minutes": 30,
            "witness_count": 2,
        },
    ]
    for report in invalid_reports:
        try:
            AlienContact.model_validate(report)
        except ValidationError as e:
            print_errors(e)


if __name__ == "__main__":
    main()
