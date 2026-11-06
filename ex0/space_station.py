from datetime import datetime

from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: str | None = Field(default=None, max_length=200)


def show_station(station: SpaceStation) -> None:
    status = "Operational" if station.is_operational else "Maintenance"
    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew: {station.crew_size} people")
    print(f"Power: {station.power_level}%")
    print(f"Oxygen: {station.oxygen_level}%")
    print(f"Last maintenance: {station.last_maintenance}")
    print(f"Status: {status}")
    if station.notes:
        print(f"Notes: {station.notes}")


def main() -> None:
    print("Space Station Data Validation")
    print("=" * 40)

    valid_data = {
        "station_id": "ISS001",
        "name": "International Space Station",
        "crew_size": 6,
        "power_level": 85.5,
        "oxygen_level": 92.3,
        "last_maintenance": "2024-01-15T10:30:00",
    }
    try:
        station = SpaceStation.model_validate(valid_data)
        print("Valid station created:")
        show_station(station)
    except ValidationError as e:
        print(f"Unexpected error: {e}")

    print()
    print("=" * 40)

    invalid_data = {
        "station_id": "ISS002",
        "name": "Overcrowded Station",
        "crew_size": 25,
        "power_level": 70.0,
        "oxygen_level": 80.0,
        "last_maintenance": "2024-02-01T08:00:00",
    }
    try:
        SpaceStation.model_validate(invalid_data)
        print("This should not happen")
    except ValidationError as e:
        print("Expected validation error:")
        for error in e.errors():
            print(error["msg"])


if __name__ == "__main__":
    main()
