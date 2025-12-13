from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from plexapi.exceptions import NotFound

from plexutil.enums.agent import Agent
from plexutil.enums.language import Language
from plexutil.enums.scanner import Scanner
from plexutil.exception.library_illegal_state_error import (
    LibraryIllegalStateError,
)
from plexutil.exception.library_poll_timeout_error import (
    LibraryPollTimeoutError,
)
from plexutil.exception.library_section_missing_error import (
    LibrarySectionMissingError,
)
from plexutil.plex_util_logger import PlexUtilLogger
from plexutil.util.path_ops import PathOps
from plexutil.util.plex_ops import PlexOps

if TYPE_CHECKING:
    from pathlib import Path

    from plexapi.audio import Track
    from plexapi.library import LibrarySection
    from plexapi.server import PlexServer
    from plexapi.video import Movie, Show

    from plexutil.dto.library_preferences_dto import LibraryPreferencesDTO
    from plexutil.dto.movie_dto import MovieDTO
    from plexutil.dto.song_dto import SongDTO
    from plexutil.dto.tv_series_dto import TVSeriesDTO

from alive_progress import alive_bar

from plexutil.enums.library_type import LibraryType
from plexutil.exception.library_op_error import LibraryOpError
from plexutil.exception.library_unsupported_error import (
    LibraryUnsupportedError,
)


class Library(ABC):
    def __init__(
        self,
        plex_server: PlexServer,
        name: str,
        library_type: LibraryType,
        agent: Agent,
        scanner: Scanner,
        locations: list[Path],
        language: Language,
        preferences: LibraryPreferencesDTO,
    ) -> None:
        self.plex_server = plex_server
        self.name = name
        self.library_type = library_type
        self.agent = agent
        self.scanner = scanner
        self.locations = locations
        self.language = language
        self.preferences = preferences

        section = None
        try:
            section = self.get_section()
        except LibrarySectionMissingError:
            # No need to continue if not an existing library
            return

        if section:
            self.locations = section.locations
            self.agent = Agent.get_from_str(section.agent)
            self.scanner = Scanner.get_from_str(section.scanner)
            self.locations = [
                PathOps.get_path_from_str(location)
                for location in section.locations
            ]
            self.language = Language.get_from_str(section.language)

    @abstractmethod
    def create(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self) -> None:
        """
        Generic Library Delete

        Returns:
            None: This method does not return a value.

        Raises:
            LibraryOpError: If Library isn't found

        """
        op_type = "DELETE"
        self.log_library(operation=op_type, is_info=False, is_debug=True)

        try:
            self.get_section().delete()
        except LibrarySectionMissingError as e:
            description = f"Does not exist: {self.name}"
            raise LibraryOpError(
                op_type=op_type,
                description=description,
                library_type=self.library_type,
            ) from e

    @abstractmethod
    def exists(self) -> bool:
        """
        Generic LibrarySection Exists

        Returns:
            bool: If LibrarySection exists

        """
        self.log_library(
            operation="CHECK EXISTS", is_info=False, is_debug=True
        )

        try:
            section = self.get_section()
            if not section:
                description = "Does not exist\n"
                PlexUtilLogger.get_logger().debug(description)
                return False

        except LibrarySectionMissingError:
            description = "Does not exist\n"
            PlexUtilLogger.get_logger().debug(description)
            return False

        description = "Exists\n"
        PlexUtilLogger.get_logger().debug(description)
        return True

    def poll(
        self,
        requested_attempts: int = 0,
        expected_count: int = 0,
        interval_seconds: int = 0,
    ) -> None:
        """
        Performs a query based on the supplied parameters

        Args:
            requested_attempts (int): Amount of times to poll
            expected_count (int): Polling terminates when reaching this amount
            interval_seconds (int): timeout before making a new attempt

        Returns:
            None: This method does not return a value

        Raises:
            LibraryPollTimeoutError: If expected_count not reached
        """
        current_count = len(self.query())
        init_offset = abs(expected_count - current_count)

        debug = (
            f"Requested attempts: {requested_attempts!s}\n"
            f"Interval seconds: {interval_seconds!s}\n"
            f"Current count: {current_count!s}\n"
            f"Expected count: {expected_count!s}\n"
            f"Net change: {init_offset!s}\n"
        )

        PlexUtilLogger.get_logger().debug(debug)

        with alive_bar(init_offset) as bar:
            attempts = 0
            display_count = 0
            offset = init_offset

            while attempts < requested_attempts:
                updated_current_count = len(self.query())
                offset = abs(updated_current_count - current_count)
                current_count = updated_current_count

                for _ in range(offset):
                    display_count = display_count + 1
                    bar()

                if current_count == expected_count:
                    break

                if current_count > expected_count:
                    description = (
                        f"Expected {expected_count} items in the library "
                        f"but Plex Server has {current_count}"
                    )
                    raise LibraryIllegalStateError(description)

                time.sleep(interval_seconds)
                attempts = attempts + 1
                if attempts >= requested_attempts:
                    description = (
                        "Did not reach the expected"
                        f"library count: {expected_count}"
                    )
                    raise LibraryPollTimeoutError(description)

    @abstractmethod
    def query(self) -> list[Track] | list[Show] | list[Movie]:
        raise NotImplementedError

    def log_library(
        self,
        operation: str,
        is_info: bool = True,
        is_debug: bool = False,
        is_console: bool = False,
    ) -> None:
        """
        Private logging template to be used by methods of this class

        Args:
            opration (str): The type of operation i.e. CREATE DELETE
            is_info (bool): Should it be logged as INFO
            is_debug (bool): Should it be logged as DEBUG
            is_console (bool): Should it be logged with console handler

        Returns:
            None: This method does not return a value.
        """
        library = self.plex_server.library
        library_id = library.key if library else ""
        info = (
            f"{operation} {self.library_type} library: \n"
            f"ID: {library_id}\n"
            f"Name: {self.name}\n"
            f"Type: {self.library_type.value}\n"
            f"Agent: {self.agent.value}\n"
            f"Scanner: {self.scanner.value}\n"
            f"Locations: {self.locations!s}\n"
            f"Language: {self.language.value}\n"
            f"Movie Preferences: {self.preferences.movie}\n"
            f"Music Preferences: {self.preferences.music}\n"
            f"TV Preferences: {self.preferences.tv}\n"
        )
        if not is_console:
            if is_info:
                PlexUtilLogger.get_logger().info(info)
            if is_debug:
                PlexUtilLogger.get_logger().debug(info)
        else:
            PlexUtilLogger.get_console_logger().info(info)

    def get_section(self) -> LibrarySection:
        """
        Gets an up-to-date Plex Server Library Section
        Gets the first occuring Section, does not have conflict resolution

        Returns:
            LibrarySection: A current LibrarySection

        Raises:
            LibrarySectionMissingError: If no library of the same
            type and name exist
        """

        sections = self.plex_server.library.sections()

        filtered_sections = [
            section
            for section in sections
            if LibraryType.is_eq(self.library_type, section)
        ]

        for filtered_section in filtered_sections:
            if filtered_section.title == self.name:
                return filtered_section

        if self.name:
            description = f"Library not found: {self.name}"
        else:
            description = "Library Name (-libn) not specified, see -h"
        raise LibrarySectionMissingError(description)

    def __get_local_files(
        self,
    ) -> list[SongDTO] | list[MovieDTO] | list[TVSeriesDTO]:
        """
        Private method to get local files

        Returns:
            [SongDTO | MovieDTO | TVEpisodeDTO]: Local files

        Raises:
            LibraryUnsupportedError: If Library Type not of MUSIC,
            MUSIC_PLAYLIST, TV or MOVIE
        """
        library = self.get_section()

        if LibraryType.is_eq(LibraryType.MUSIC, library) | LibraryType.is_eq(
            LibraryType.MUSIC_PLAYLIST, library
        ):
            local_files = PathOps.get_local_songs(self.locations)
        elif LibraryType.is_eq(LibraryType.TV, library):
            local_files = PathOps.get_local_tv(self.locations)
        elif LibraryType.is_eq(LibraryType.MOVIE, library):
            local_files = PathOps.get_local_movies(self.locations)
        else:
            op_type = "Get Local Files"
            raise LibraryUnsupportedError(
                op_type,
                LibraryType.get_from_section(library),
            )

        return local_files

    def probe_library(self) -> None:
        """
        Verifies local files match server files, if not then it issues a
        library update, polls for 1000s or until server matches local files

        Returns:
            None: This method does not return a value.

        Raises:
            LibraryIllegalStateError: If local files do not match server
            LibraryUnsupportedError: If Library Type isn't supported
        """
        local_files = self.__get_local_files()
        plex_files = self.query()
        try:
            PlexOps.validate_local_files(plex_files, self.locations)
        except LibraryIllegalStateError:
            description = (
                "Plex Server does not match local files\n"
                "A server update is necessary\n"
                "This process may take several minutes\n"
            )
            PlexUtilLogger.get_logger().info(description)

        expected_count = len(local_files)
        self.get_section().update()

        self.poll(100, expected_count, 10)
        plex_files = self.query()
        PlexOps.validate_local_files(plex_files, self.locations)

    def inject_preferences(self) -> None:
        """
        Sets Library Section Preferences
        Logs a warning if preferences dont't exist or library type
        not of movie,tv,music

        Returns:
            None: This method does not return a value
        """

        if not self.preferences:
            description = "WARNING: Did not receive any Library Preferences"
            PlexUtilLogger.get_logger().warning(description)
            return

        section_preferences = None

        if (
            LibraryType.is_eq(LibraryType.MOVIE, self.get_section())
            or LibraryType.is_eq(LibraryType.TV, self.get_section())
            or LibraryType.is_eq(LibraryType.MUSIC, self.get_section())
        ):
            section_preferences = self.preferences.movie

        if not section_preferences:
            description = "WARNING: Did not receive any Library Preferences"
            PlexUtilLogger.get_logger().warning(description)
            return

        for key, value in section_preferences.items():
            try:
                section = self.get_section()
                section.editAdvanced(**{key: value})
            except NotFound:
                description = (
                    f"WARNING: Preference not accepted by the server: {key}\n"
                    f"Skipping -> {key}:{value}"
                )
                PlexUtilLogger.get_logger().warning(description)
                continue
