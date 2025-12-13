from __future__ import annotations

from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from pathlib import Path

    from plexapi.audio import Track
    from plexapi.server import PlexServer

    from plexutil.dto.music_playlist_dto import MusicPlaylistDTO
    from plexutil.dto.song_dto import SongDTO


from plexutil.core.library import Library
from plexutil.dto.library_preferences_dto import LibraryPreferencesDTO
from plexutil.enums.agent import Agent
from plexutil.enums.language import Language
from plexutil.enums.library_name import LibraryName
from plexutil.enums.library_type import LibraryType
from plexutil.enums.scanner import Scanner
from plexutil.exception.library_op_error import LibraryOpError
from plexutil.mapper.music_playlist_mapper import MusicPlaylistMapper
from plexutil.plex_util_logger import PlexUtilLogger
from plexutil.util.plex_ops import PlexOps


class Playlist(Library):
    def __init__(
        self,
        plex_server: PlexServer,
        locations: list[Path],
        playlist_name: str,
        songs: list[SongDTO],
        name: str = LibraryName.MUSIC.value,
        library_type: LibraryType = LibraryType.MUSIC_PLAYLIST,
        language: Language = Language.ENGLISH_US,
    ) -> None:
        super().__init__(
            plex_server,
            name,
            library_type,
            Agent.MUSIC,
            Scanner.MUSIC,
            locations,
            language,
            LibraryPreferencesDTO(),
        )
        self.playlist_name = playlist_name
        self.songs = songs

    def create(self) -> None:
        if self.exists():
            info = (
                f"WARNING: Playlist '{self.playlist_name}' for "
                f"Library '{self.name}' of "
                f"type {self.library_type.value} already exists."
                f"Skipping create..."
            )
            PlexUtilLogger.get_logger().warning(info)
            return

        self.probe_library()

        debug = (
            f"Creating a Playlist: \n"
            f"Playlist Name: {self.playlist_name} \n"
            f"Library Name: {self.name}\n"
            f"Song Count: {len(self.songs)}\n"
            f"Type: {self.library_type.value}\n"
            f"Agent: {self.agent.value}\n"
            f"Scanner: {self.scanner.value}\n"
            f"Locations: {self.locations!s}\n"
            f"Language: {self.language.value}\n"
        )
        PlexUtilLogger.get_logger().debug(debug)

        self.get_section().createPlaylist(
            title=self.playlist_name, items=self.__get_filtered_tracks()
        )

    def query(self) -> list[Track]:
        op_type = "QUERY"
        if not super().exists():
            description = f"Music Library '{self.name}' does not exist"
            raise LibraryOpError(
                op_type=op_type,
                library_type=LibraryType.MUSIC,
                description=description,
            )

        return self.get_section().searchTracks()

    def delete(self) -> None:
        op_type = "DELETE"
        plex_playlists = self.get_section().playlists()

        debug = (
            "Received request to delete music playlist: \n"
            f"Playlist: {self.playlist_name!s}\n"
            f"Location: {self.locations!s}\n"
            f"Playlists available in server: {plex_playlists}"
        )
        PlexUtilLogger.get_logger().debug(debug)

        for plex_playlist in plex_playlists:
            if plex_playlist.title == self.playlist_name:
                debug = "Found playlist to delete"
                PlexUtilLogger.get_logger().debug(debug)
                plex_playlist.delete()
                return

        description = (
            f"Playlist not found in server library: {self.playlist_name}"
        )
        raise LibraryOpError(op_type, self.library_type, description)

    def exists(self) -> bool:
        plex_playlists = self.get_section().playlists()

        debug = (
            f"Checking playlist exist\n"
            f"Requested: {self.playlist_name!s}\n"
            f"In server: {plex_playlists}\n"
        )
        PlexUtilLogger.get_logger().debug(debug)

        if not plex_playlists or not self.playlist_name:
            return False

        playlist_names = [x.title for x in plex_playlists]
        exists = self.playlist_name in playlist_names

        debug = f"Playlist exists: {exists}"
        PlexUtilLogger.get_logger().debug(debug)

        return exists

    def get_all_playlists(self) -> list[MusicPlaylistDTO]:
        music_playlist_mapper = MusicPlaylistMapper()

        section = self.get_section()
        plex_playlists = section.playlists()

        playlists = []
        for plex_playlist in plex_playlists:
            music_playlist_dto = music_playlist_mapper.get_dto(
                PlexOps.get_music_playlist_entity(plex_playlist)
            )

            for track in plex_playlist.items():
                song_dto = cast(
                    "SongDTO", PlexOps.get_dto_from_plex_media(track)
                )
                music_playlist_dto.songs.append(song_dto)

            playlists.append(music_playlist_dto)

        return playlists

    def delete_songs(self) -> None:
        """
        Matches provided Songs to Plex Tracks in the playlist and deletes
        the tracks from the playlist

        Returns:
            None: This method does not return a value
        """
        filtered_tracks = self.__get_filtered_tracks(is_playlist_tracks=False)
        playlist = self.get_section().playlist(self.playlist_name)
        playlist.removeItems(filtered_tracks)

    def add_songs(self) -> None:
        """
        Matches provided Songs to Plex Tracks in the library and adds
        the tracks to the plex playlist

        Returns:
            None: This method does not return a value
        """
        self.probe_library()
        filtered_tracks = self.__get_filtered_tracks()
        playlist = self.get_section().playlist(self.playlist_name)
        playlist.addItems(filtered_tracks)

    def __get_filtered_tracks(
        self, is_playlist_tracks: bool = False
    ) -> list[Track]:
        if is_playlist_tracks:
            all_tracks = (
                self.get_section().playlist(self.playlist_name).items()
            )
        else:
            all_tracks = self.get_section().searchTracks()

        known, unknown = PlexOps.filter_plex_media(all_tracks, self.songs)
        if unknown:
            description = (
                f"WARNING: These songs were not found "
                f"in the plex server library: {self.name}\n"
            )
            for u in unknown:
                description = description + f"->{u!s}\n"

            PlexUtilLogger.get_logger().warning(description)

        filtered_tracks = []
        for track in all_tracks:
            dto = PlexOps.get_dto_from_plex_media(track)
            if dto in known:
                filtered_tracks.append(track)

        return filtered_tracks
