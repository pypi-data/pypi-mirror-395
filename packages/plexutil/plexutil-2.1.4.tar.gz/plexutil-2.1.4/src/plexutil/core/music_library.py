from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from plexapi.audio import Track
    from plexapi.server import PlexServer

    from plexutil.dto.library_preferences_dto import LibraryPreferencesDTO

from plexutil.core.library import Library
from plexutil.enums.agent import Agent
from plexutil.enums.language import Language
from plexutil.enums.library_name import LibraryName
from plexutil.enums.library_type import LibraryType
from plexutil.enums.scanner import Scanner
from plexutil.exception.library_op_error import LibraryOpError
from plexutil.plex_util_logger import PlexUtilLogger
from plexutil.util.query_builder import QueryBuilder


class MusicLibrary(Library):
    def __init__(
        self,
        plex_server: PlexServer,
        locations: list[Path],
        preferences: LibraryPreferencesDTO,
        name: str = LibraryName.MUSIC.value,
        language: Language = Language.ENGLISH_US,
    ) -> None:
        super().__init__(
            plex_server,
            name,
            LibraryType.MUSIC,
            Agent.MUSIC,
            Scanner.MUSIC,
            locations,
            language,
            preferences,
        )

    def create(self) -> None:
        """
        Creates a Music Library
        This operation is expensive as it waits for all the music files
        to be recognized by the server

        Returns:
            None: This method does not return a value

        Raises:
            LibraryOpError: If Library already exists
            or when failure to create a Query
        """
        op_type = "CREATE"
        if self.exists():
            description = f"Music Library '{self.name}' already exists"
            raise LibraryOpError(
                op_type=op_type,
                library_type=LibraryType.TV,
                description=description,
            )

        self.log_library(operation=op_type, is_info=False, is_debug=True)

        part = ""

        query_builder = QueryBuilder(
            "/library/sections",
            name=self.name,
            the_type="music",
            agent=Agent.MUSIC.value,
            scanner=Scanner.MUSIC.value,
            language=self.language.value,
            importFromiTunes="",
            enableAutoPhotoTags="",
            location=self.locations,
            prefs=self.preferences.music,
        )

        part = query_builder.build()

        debug = f"Query: {part}\n"

        PlexUtilLogger.get_logger().debug(debug)

        # This posts a music library
        if part:
            self.plex_server.query(
                part,
                method=self.plex_server._session.post,
            )
        else:
            description = "Query Builder has not built a part!"
            raise LibraryOpError(
                op_type="CREATE",
                library_type=self.library_type,
                description=description,
            )

        self.probe_library()

    def query(self) -> list[Track]:
        """
        Returns all tracks for the current LibrarySection

        Returns:
            list[plexapi.audio.Audio]: Tracks from the current Section
        """
        op_type = "QUERY"
        if not self.exists():
            description = f"Music Library '{self.name}' does not exist"
            raise LibraryOpError(
                op_type=op_type,
                library_type=LibraryType.MUSIC,
                description=description,
            )

        return self.get_section().searchTracks()

    def delete(self) -> None:
        return super().delete()

    def exists(self) -> bool:
        return super().exists()
