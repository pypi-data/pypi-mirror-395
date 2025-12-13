from dataclasses import dataclass
from pathlib import Path


# Frozen=True creates an implicit hash method, eq is created by default
@dataclass(frozen=True)
class BootstrapPathsDTO:
    config_dir: Path
    log_dir: Path
    plexutil_config_file: Path
    plexutil_playlists_db_dir: Path
