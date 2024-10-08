from typing import Any

current_date: str
current_location: str
destination: Habitat
duration: Optional[int] = None
migration_id: int
migration_path: MigrationPath
migrations: dict[int, Migration] = {}
path_id: int
paths: dict[int, MigrationPath] = {}

class Migration:

    pass
