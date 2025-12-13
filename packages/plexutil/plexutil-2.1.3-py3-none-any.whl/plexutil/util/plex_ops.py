from __future__ import annotations

from typing import TYPE_CHECKING, cast

from plexapi.audio import Track
from plexapi.video import Movie, Show

from plexutil.dto.movie_dto import MovieDTO
from plexutil.dto.song_dto import SongDTO
from plexutil.dto.tv_series_dto import TVSeriesDTO
from plexutil.exception.library_illegal_state_error import (
    LibraryIllegalStateError,
)
from plexutil.model.music_playlist_entity import MusicPlaylistEntity
from plexutil.plex_util_logger import PlexUtilLogger
from plexutil.static import Static
from plexutil.util.path_ops import PathOps

if TYPE_CHECKING:
    from pathlib import Path

    from plexapi.server import Playlist, PlexServer

    from plexutil.dto.library_preferences_dto import LibraryPreferencesDTO


class PlexOps(Static):
    @staticmethod
    def set_server_settings(
        plex_server: PlexServer,
        library_preferences_dto: LibraryPreferencesDTO,
    ) -> None:
        """
        Sets Plex Server Settings

        Args:
            plex_server (plexapi.server.PlexServer): A Plex Server instance
            library_preferences_dto (LibraryPreferencesDTO): Library Preference


        Returns:
            None: This method does not return a value

        """
        server_settings = library_preferences_dto.plex_server_settings
        for setting_id, setting_value in server_settings.items():
            plex_server.settings.get(setting_id).set(setting_value)
        plex_server.settings.save()

    @staticmethod
    def get_music_playlist_entity(playlist: Playlist) -> MusicPlaylistEntity:
        """
        Maps a plexapi.server.Playlist to a MusicPlaylsitEntity

        Args:
            playlist (plexapi.server.Playlist): A plex playlist

        Returns:
            MusicPlaylistEntity: Mapped from playlist
        """
        return MusicPlaylistEntity(name=playlist.title)

    @staticmethod
    def normalize_dto(
        dto: SongDTO | MovieDTO | TVSeriesDTO,
        media: list[Track] | list[Movie] | list[Show],
    ) -> SongDTO | MovieDTO | TVSeriesDTO:
        """
        Adds the missing properties to a DTO based on the information
        from a Plex Media in the server

        Args:
            dto (SongDTO, MovieDTO, TVSeriesDTO): The DTO to match against
            media ([Track|Movie|Show]): The plex media objects

        Returns:
            SongDTO | MovieDTO | TVSeriesDTO: A normalized DTO
        """

        for m in media:
            location = PathOps.get_path_from_str(m.locations[0])
            if isinstance(m, Track) and isinstance(dto, SongDTO):
                name = location.stem
                if name == dto.name:
                    return SongDTO(name=dto.name, location=location)
            elif isinstance(m, Movie) and isinstance(dto, MovieDTO):
                name, year = PathOps.get_show_name_and_year_from_str(
                    str(location)
                )
                if name == dto.name and year == dto.year:
                    return MovieDTO(name=name, year=year, location=location)
            elif isinstance(m, Show) and isinstance(dto, TVSeriesDTO):
                name, year = PathOps.get_show_name_and_year_from_str(
                    str(location)
                )
                if name == dto.name and year == dto.year:
                    return TVSeriesDTO(name=name, year=year, location=location)

        description = (
            f"Could not match a provided DTO to any Plex Media:\n{dto}\n"
        )
        raise ValueError(description)

    @staticmethod
    def get_dto_from_plex_media(
        media: Track | Movie | Show,
    ) -> SongDTO | MovieDTO | TVSeriesDTO:
        """
        Converts Track,Movie,Show to a corresponding DTO

        Args:
            media (Track|Movie|Show): The plex media object

        Returns:
            SongDTO | MovieDTO | TVSeriesDTO: The converted DTO from media

        Raise:
            ValueError: If Track/Movie location is not a file
            or Show location is a dir or media is not a Track/Movie/Show
        """
        location = PathOps.get_path_from_str(media.locations[0])

        if location.is_dir() and not isinstance(media, Show):
            description = f"Expected to find a file not a dir:{location!s}"
            raise ValueError(description)
        elif location.is_file() and isinstance(media, Show):
            description = f"Expected to find a dir not a file:{location!s}"
            raise ValueError(description)

        if isinstance(media, Track):
            name = location.stem
            return SongDTO(name=name, location=location)
        elif isinstance(media, Movie):
            name, year = PathOps.get_show_name_and_year_from_str(str(location))
            return MovieDTO(name=name, year=year, location=location)
        elif isinstance(media, Show):
            name, year = PathOps.get_show_name_and_year_from_str(str(location))
            return TVSeriesDTO(name=name, year=year, location=location)
        else:
            description = f"unsupported media: {type(media)}"
            raise ValueError(description)

    @staticmethod
    def validate_local_files(
        plex_files: list[Track] | list[Show] | list[Movie],
        locations: list[Path],
    ) -> None:
        """
        Verifies that all local files match the provided plex tracks
        in the locations indicated

        Args:
            tracks ([plexapi.audio.Track]): plexapi tracks.
            locations ([Path]): local file locations.

        Returns:
            None: This method does not return a value

        Raises:
            LibraryIllegalStateError: if local files do not match plex files
            LibraryOpError: If plex_file type is not supported
        """
        if not plex_files:
            description = "Did not receive any Plex Files\n"
            raise LibraryIllegalStateError(description)

        if all(isinstance(plex_file, Track) for plex_file in plex_files):
            songs = PathOps.get_local_songs(locations)
            _, unknown = PlexOps.filter_plex_media(
                cast("list[Track]", plex_files), songs
            )
        elif all(isinstance(plex_file, Show) for plex_file in plex_files):
            tv = PathOps.get_local_tv(locations)
            _, unknown = PlexOps.filter_plex_media(
                cast("list[Show]", plex_files), tv
            )
        elif all(isinstance(plex_file, Movie) for plex_file in plex_files):
            movies = PathOps.get_local_movies(locations)
            _, unknown = PlexOps.filter_plex_media(
                cast("list[Movie]", plex_files), movies
            )
        else:
            description = "Expected to find Tracks, Movies or Shows"
            raise ValueError(description)

        if unknown:
            description = "These local files are unknown to the plex server:\n"
            for u in unknown:
                description = description + f"-> {u!s}\n"
            PlexUtilLogger.get_logger().debug(description)

            raise LibraryIllegalStateError(description)

    @staticmethod
    def filter_plex_media(
        plex_media: list[Movie] | list[Track] | list[Show],
        dtos: list[MovieDTO] | list[SongDTO] | list[TVSeriesDTO],
    ) -> tuple[
        list[MovieDTO] | list[SongDTO] | list[TVSeriesDTO],
        list[MovieDTO] | list[SongDTO] | list[TVSeriesDTO],
    ]:
        """
        Filters the provided Plex media with the provided dtos

        Args:
            plex_media ([
            plexapi.video.Movie |
            plexapi.video.Show |
            plexapi.audio.Track]): A list of plex media to compare against

            plexapi movies
            dtos ([
            MovieDTO |
            SongDTO |
            TVSeriesDTO]): Dtos to match against plex media

        Returns:
            A tuple of:
            1) DTOs that match the provided plex media
            2) DTOS that did not match to any plex media
        """
        filtered_media = []
        unknown_media = []

        plex_media_dto = [
            PlexOps.get_dto_from_plex_media(media) for media in plex_media
        ]

        for dto in dtos:
            if dto not in plex_media_dto:
                unknown_media.append(dto)
            else:
                filtered_media.append(dto)

        return filtered_media, unknown_media
