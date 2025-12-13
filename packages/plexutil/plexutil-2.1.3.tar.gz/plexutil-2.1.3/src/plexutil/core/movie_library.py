from __future__ import annotations

from typing import TYPE_CHECKING

from plexutil.exception.library_op_error import LibraryOpError

if TYPE_CHECKING:
    from pathlib import Path

    from plexapi.server import PlexServer
    from plexapi.video import Movie

    from plexutil.dto.library_preferences_dto import LibraryPreferencesDTO

from plexutil.core.library import Library
from plexutil.enums.agent import Agent
from plexutil.enums.language import Language
from plexutil.enums.library_name import LibraryName
from plexutil.enums.library_type import LibraryType
from plexutil.enums.scanner import Scanner


class MovieLibrary(Library):
    def __init__(
        self,
        plex_server: PlexServer,
        locations: list[Path],
        preferences: LibraryPreferencesDTO,
        language: Language = Language.ENGLISH_US,
        name: str = LibraryName.MOVIE.value,
    ) -> None:
        super().__init__(
            plex_server,
            name,
            LibraryType.MOVIE,
            Agent.MOVIE,
            Scanner.MOVIE,
            locations,
            language,
            preferences,
        )

    def create(self) -> None:
        """
        Creates a Movie Library
        Logs a warning if a specific movie preference is rejected by the server
        Logs a warning if no Movie Preferences available

        Returns:
            None: This method does not return a value

        Raises:
            LibraryOpError: If Library already exists
        """
        op_type = "CREATE"
        if self.exists():
            description = f"Movie Library '{self.name}' already exists"
            raise LibraryOpError(
                op_type=op_type,
                library_type=LibraryType.MOVIE,
                description=description,
            )

        self.log_library(operation=op_type, is_info=False, is_debug=True)

        self.plex_server.library.add(
            name=self.name,
            type=self.library_type.value,
            agent=self.agent.value,
            scanner=self.scanner.value,
            location=[str(x) for x in self.locations],  # pyright: ignore [reportArgumentType]
            language=self.language.value,
        )

        self.inject_preferences()

    def query(self) -> list[Movie]:
        """
        Returns all movies for the current LibrarySection

        Returns:
            list[plexapi.video.Video]: Movies from the current Section
        """
        op_type = "QUERY"
        if not self.exists():
            description = f"Movie Library '{self.name}' does not exist"
            raise LibraryOpError(
                op_type=op_type,
                library_type=LibraryType.MOVIE,
                description=description,
            )
        return self.get_section().searchMovies()

    def delete(self) -> None:
        return super().delete()

    def exists(self) -> bool:
        return super().exists()
