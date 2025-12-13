from dataclasses import dataclass, field


# Frozen=True creates an implicit hash method, eq is created by default
@dataclass(frozen=True)
class LibraryPreferencesDTO:
    music: dict = field(default_factory=dict)
    movie: dict = field(default_factory=dict)
    tv: dict = field(default_factory=dict)
    plex_server_settings: dict = field(default_factory=dict)
