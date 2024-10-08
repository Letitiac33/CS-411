from typing import Any, Optional

age: Optional[int] = None
animal_id: int
animals: dict[int, Animal] = {}
animals: List[int] = []
health_status: Optional[str] = None
species: str
start_date: str
start_location: Habitat
status: str = "Scheduled"

class Animal:

    pass
