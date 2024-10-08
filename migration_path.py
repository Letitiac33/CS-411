from typing import Optional

class MigrationPath:
    def __init__(self,
                 destination: Habitat,
                 duration: Optional[int] = None,
                 migration_path: 'MigrationPath' = None, 
                 path_id: int = 0,
        self.destination = destination
        self.duration = duration
        self.migration_path = migration_path
        self.migrations = migrations or {}
        self.path_id = path_id
    def get_migration_path_details(path_id) -> dict:
        pass
    def update_migration_path_details(path_id: int, **kwargs) -> None:
        pass
