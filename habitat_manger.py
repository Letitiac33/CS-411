from typing import Optional, List
from wildlife_tracker.habitat_management.habitat import Habitat

class HabitatManager:   
    def __init__(self) -> None:
        habitats: dict[int, Habitat] = {}
        pass
     def create_habitat(self, habitat_id: int, geographic_area: str, size: int, environment_type: str) -> Habitat:
        pass

    def get_habitat_by_id(self, habitat_id: int) -> Habitat:
        pass


