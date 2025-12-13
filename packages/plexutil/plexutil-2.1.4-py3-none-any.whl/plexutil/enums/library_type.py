from __future__ import annotations

from enum import Enum

from plexapi.library import (
    LibrarySection,
    MovieSection,
    MusicSection,
    ShowSection,
)


class LibraryType(Enum):
    MUSIC = "music"
    TV = "show"
    MOVIE = "movie"
    MUSIC_PLAYLIST = "audio"

    @staticmethod
    def is_eq(
        library_type: LibraryType, library_section: LibrarySection
    ) -> bool:
        return (
            (
                isinstance(library_section, MovieSection)
                and library_type is LibraryType.MOVIE
            )
            or (
                isinstance(library_section, MusicSection)
                and library_type is LibraryType.MUSIC
            )
            or (
                isinstance(library_section, ShowSection)
                and library_type is LibraryType.TV
            )
        )

    @staticmethod
    def get_from_section(library_section: LibrarySection) -> LibraryType:
        match library_section:
            case MovieSection():
                return LibraryType.MOVIE
            case MusicSection():
                return LibraryType.MUSIC
            case ShowSection():
                return LibraryType.TV
            case _:
                return LibraryType.MUSIC
