from __future__ import annotations

from enum import Enum

from plexutil.enums.library_type import LibraryType


class UserRequest(Enum):
    CONFIG = "config"
    SET_SERVER_SETTINGS = "set_server_settings"
    CREATE_MOVIE_LIBRARY = "create_movie_library"
    DELETE_MOVIE_LIBRARY = "delete_movie_library"
    CREATE_TV_LIBRARY = "create_tv_library"
    DELETE_TV_LIBRARY = "delete_tv_library"
    CREATE_MUSIC_LIBRARY = "create_music_library"
    DELETE_MUSIC_LIBRARY = "delete_music_library"
    CREATE_MUSIC_PLAYLIST = "create_music_playlist"
    DELETE_MUSIC_PLAYLIST = "delete_music_playlist"
    EXPORT_MUSIC_PLAYLIST = "export_music_playlist"
    IMPORT_MUSIC_PLAYLIST = "import_music_playlist"
    ADD_SONGS_TO_MUSIC_PLAYLIST = "add_songs_to_music_playlist"
    DELETE_SONGS_FROM_MUSIC_PLAYLIST = "delete_songs_from_music_playlist"

    @staticmethod
    # Forward Reference used here in type hint
    def get_all() -> list[UserRequest]:
        return list(UserRequest)

    @staticmethod
    def get_user_request_from_str(
        user_request_candidate: str,
    ) -> UserRequest:
        requests = UserRequest.get_all()
        user_request_candidate = user_request_candidate.lower()

        for request in requests:
            if (
                user_request_candidate == request.value
                or user_request_candidate.replace("_", " ") == request.value
            ):
                return request

        raise ValueError("Request not supported: " + user_request_candidate)

    @staticmethod
    def get_library_type_from_request(
        user_request: UserRequest,
    ) -> LibraryType:
        match user_request:
            case (
                UserRequest.CREATE_MOVIE_LIBRARY
                | UserRequest.DELETE_MOVIE_LIBRARY
            ):
                return LibraryType.MOVIE
            case UserRequest.CREATE_TV_LIBRARY | UserRequest.DELETE_TV_LIBRARY:
                return LibraryType.TV
            case (
                UserRequest.CREATE_MUSIC_LIBRARY
                | UserRequest.DELETE_MUSIC_LIBRARY
            ):
                return LibraryType.MUSIC
            case (
                UserRequest.IMPORT_MUSIC_PLAYLIST
                | UserRequest.CREATE_MUSIC_PLAYLIST
                | UserRequest.DELETE_MUSIC_PLAYLIST
                | UserRequest.EXPORT_MUSIC_PLAYLIST
                | UserRequest.ADD_SONGS_TO_MUSIC_PLAYLIST
                | UserRequest.DELETE_SONGS_FROM_MUSIC_PLAYLIST
            ):
                return LibraryType.MUSIC_PLAYLIST
            case _:
                return LibraryType.MUSIC
