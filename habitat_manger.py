from typing import Optional, List
from wildlife_tracker.habitat_management.habitat import Habitat

class HabitatManager:   
    def __init__(self) -> None:
        habitats: dict[int, Habitat] = {}


