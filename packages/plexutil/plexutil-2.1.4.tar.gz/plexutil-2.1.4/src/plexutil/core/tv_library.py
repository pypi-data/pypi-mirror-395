from __future__ import annotations

from typing import TYPE_CHECKING

from plexutil.exception.library_op_error import LibraryOpError

if TYPE_CHECKING:
    from pathlib import Path

    from plexapi.server import PlexServer
    from plexapi.video import Show, Video

    from plexutil.dto.library_preferences_dto import LibraryPreferencesDTO
    from plexutil.dto.tv_language_manifest_dto import TVLanguageManifestDTO

from plexutil.core.library import Library
from plexutil.enums.agent import Agent
from plexutil.enums.language import Language
from plexutil.enums.library_name import LibraryName
from plexutil.enums.library_type import LibraryType
from plexutil.enums.scanner import Scanner
from plexutil.plex_util_logger import PlexUtilLogger


class TVLibrary(Library):
    def __init__(
        self,
        plex_server: PlexServer,
        locations: list[Path],
        preferences: LibraryPreferencesDTO,
        tv_language_manifest_dto: list[TVLanguageManifestDTO],
        agent: Agent = Agent.TV,
        scanner: Scanner = Scanner.TV,
        name: str = LibraryName.TV.value,
        language: Language = Language.ENGLISH_US,
    ) -> None:
        super().__init__(
            plex_server,
            name,
            LibraryType.TV,
            agent,
            scanner,
            locations,
            language,
            preferences,
        )
        self.tv_language_manifest_dto = tv_language_manifest_dto

    def create(self) -> None:
        """
        Creates a TV Library
        Logs a warning if a specific tv preference is rejected by the server
        Logs a warning if no TV Preferences available
        This operation is expensive as it waits for all the tv files
        to be recognized by the server

        Returns:
            None: This method does not return a value

        Raises:
            LibraryOpError: If Library already exists
        """
        op_type = "CREATE"

        if self.exists():
            description = f"TV Library '{self.name}' already exists"
            raise LibraryOpError(
                op_type=op_type,
                library_type=LibraryType.TV,
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

        manifests_dto = self.tv_language_manifest_dto
        debug = f"Manifests: {manifests_dto}\n"
        PlexUtilLogger.get_logger().debug(debug)

        self.probe_library()

        for manifest_dto in manifests_dto:
            language = manifest_dto.language
            ids = manifest_dto.ids
            if not ids:
                continue

            description = f"Language override {language.value} for: {ids}"
            PlexUtilLogger.get_logger().debug(description)
            for show in self.get_shows_by_tvdb(ids):
                show.editAdvanced(languageOverride=language.value)

    def query(self) -> list[Show]:
        op_type = "QUERY"
        if not self.exists():
            description = f"TV Library '{self.name}' does not exist"
            raise LibraryOpError(
                op_type=op_type,
                library_type=LibraryType.TV,
                description=description,
            )
        return self.get_section().searchShows()

    def get_shows_by_tvdb(self, tvdb_ids: list[int]) -> list[Video]:
        shows = self.get_section().searchShows()

        tvdb_prefix = "tvdb://"

        if not tvdb_ids:
            return []

        id_shows = {}
        shows_filtered = []

        for show in shows:
            for guid in show.guids:
                _id = guid.id
                if tvdb_prefix in _id:
                    tvdb = _id.replace(tvdb_prefix, "")
                    id_shows[int(tvdb)] = show

        for tvdb_id in tvdb_ids:
            if tvdb_id in id_shows:
                shows_filtered.append(id_shows[tvdb_id])
            else:
                description = (
                    "WARNING: No show in server matches "
                    f"the supplied TVDB ID: {tvdb_id!s} in language manifest"
                )
                PlexUtilLogger.get_logger().warning(description)

        return shows_filtered

    def delete(self) -> None:
        return super().delete()

    def exists(self) -> bool:
        return super().exists()
