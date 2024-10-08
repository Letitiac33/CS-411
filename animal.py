from typing import Any, List, Optional

class Animal:
    def __init__(self,
                 animal_id: int,
                 species: str,
                 age: Optional[int] = None,
                 health_status: Optional[str] = None,
                 start_date: str,
                 start_location: Habitat,
                 status: str = "Scheduled") -> None:
        self.animal_id = animal_id
        self.species = species
        self.age = age
        self.health_status = health_status
        self.start_date = start_date
        self.start_location = start_location
        self.status = status

    def get_animal_details(self, animal_id: int) -> dict[str, Any]:
        pass
    def update_animal_details(self, animal_id: int, **kwargs: Any) -> None:
        pass

    pass
