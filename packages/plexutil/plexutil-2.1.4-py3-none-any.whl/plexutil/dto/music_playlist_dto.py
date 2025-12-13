from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plexutil.dto.song_dto import SongDTO


# Frozen=True creates an implicit hash method, eq is created by default
@dataclass(frozen=True)
class MusicPlaylistDTO:
    name: str = ""
    songs: list[SongDTO] = field(default_factory=list)
