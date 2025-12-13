import sys
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from plexapi.audio import Track

from jsonschema.exceptions import ValidationError
from peewee import DoesNotExist
from plexapi.server import PlexServer

from plexutil.core.movie_library import MovieLibrary
from plexutil.core.music_library import MusicLibrary
from plexutil.core.playlist import Playlist
from plexutil.core.prompt import Prompt
from plexutil.core.server_config import ServerConfig
from plexutil.core.tv_library import TVLibrary
from plexutil.dto.music_playlist_dto import MusicPlaylistDTO
from plexutil.enums.library_type import LibraryType
from plexutil.enums.user_request import UserRequest
from plexutil.exception.bootstrap_error import BootstrapError
from plexutil.exception.library_illegal_state_error import (
    LibraryIllegalStateError,
)
from plexutil.exception.library_op_error import LibraryOpError
from plexutil.exception.library_poll_timeout_error import (
    LibraryPollTimeoutError,
)
from plexutil.exception.library_section_missing_error import (
    LibrarySectionMissingError,
)
from plexutil.exception.server_config_error import ServerConfigError
from plexutil.exception.unexpected_argument_error import (
    UnexpectedArgumentError,
)
from plexutil.exception.user_error import UserError
from plexutil.plex_util_logger import PlexUtilLogger
from plexutil.service.music_playlist_service import MusicPlaylistService
from plexutil.service.song_music_playlist_composite_service import (
    SongMusicPlaylistCompositeService,
)
from plexutil.util.file_importer import FileImporter
from plexutil.util.path_ops import PathOps
from plexutil.util.plex_ops import PlexOps


def main() -> None:
    try:
        bootstrap_paths_dto = FileImporter.bootstrap()
        FileImporter.populate_sample(bootstrap_paths_dto)

        config_dir = bootstrap_paths_dto.config_dir

        instructions_dto = Prompt.get_user_instructions_dto()

        request = instructions_dto.request
        songs = instructions_dto.songs
        playlist_name = instructions_dto.playlist_name
        language = instructions_dto.language
        library_name = instructions_dto.library_name
        locations = instructions_dto.locations
        library_type = instructions_dto.library_type
        server_config_dto = instructions_dto.server_config_dto

        config = ServerConfig(bootstrap_paths_dto, server_config_dto)

        songs_dto = []
        music_playlist_dto = MusicPlaylistDTO()
        if (
            library_type is LibraryType.MUSIC
            or library_type is LibraryType.MUSIC_PLAYLIST
        ):
            song_paths = [PathOps.get_path_from_str(x) for x in songs]
            songs_dto = PathOps.get_local_songs(song_paths)

            music_playlist_dto = MusicPlaylistDTO(
                name=playlist_name,
                songs=songs_dto,
            )

        if request == UserRequest.CONFIG:
            server_config_dto = config.save()
            sys.exit(0)
        else:
            try:
                server_config_dto = config.get()
            except DoesNotExist:
                description = "No Server Config found"
                PlexUtilLogger.get_logger().debug(description)

        host = server_config_dto.host
        port = server_config_dto.port
        token = server_config_dto.token

        if (
            instructions_dto.is_show_configuration
            | instructions_dto.is_show_configuration_token
        ):
            if request:
                description = (
                    f"Received a request: '{request.value}' but also a call "
                    f"to show configuration?\n"
                    f"plexutil -sc OR plexutil -sct to show the token\n"
                )

                raise UserError(description)  # noqa: TRY301

            description = (
                "\n=====Server Configuration=====\n"
                "To update the configuration: plexutil config -token ...\n\n"
                f"Host: {host}\n"
                f"Port: {port}\n"
                f"Token: "
            )
            if instructions_dto.is_show_configuration_token:
                description = (
                    description + f"{token if token else 'NOT SUPPLIED'}\n"
                )
            else:
                description = (
                    description + "\n\nINFO: To show token use"
                    "--show_configuration_token\n"
                )

            PlexUtilLogger.get_console_logger().info(description)

            sys.exit(0)

        if not token:
            description = (
                "Plex Token has not been supplied, cannot continue\n"
                "Set a token -> plexutil config -token ..."
            )
            raise ServerConfigError(description)  # noqa: TRY301

        preferences_dto = FileImporter.get_library_preferences_dto(
            config_dir,
        )

        tv_language_manifest_dto = FileImporter.get_tv_language_manifest(
            config_dir,
        )

        baseurl = f"http://{host}:{port}"
        plex_server = PlexServer(baseurl, token)
        library = None

        match library_type:
            case LibraryType.MUSIC:
                library = MusicLibrary(
                    plex_server=plex_server,
                    language=language,
                    preferences=preferences_dto,
                    name=library_name,
                    locations=locations,
                )
            case LibraryType.MUSIC_PLAYLIST:
                library = Playlist(
                    plex_server=plex_server,
                    language=language,
                    songs=music_playlist_dto.songs,
                    library_type=LibraryType.MUSIC,
                    name=library_name,
                    playlist_name=music_playlist_dto.name,
                    locations=locations,
                )
            case LibraryType.MOVIE:
                library = MovieLibrary(
                    plex_server=plex_server,
                    language=language,
                    preferences=preferences_dto,
                    name=library_name,
                    locations=locations,
                )
            case LibraryType.TV:
                library = TVLibrary(
                    plex_server=plex_server,
                    language=language,
                    name=library_name,
                    preferences=preferences_dto,
                    tv_language_manifest_dto=tv_language_manifest_dto,
                    locations=locations,
                )
            case _:
                description = "Didn't receive a request"
                PlexUtilLogger.get_logger().error(description)
                sys.exit(1)

        match request:
            case (
                UserRequest.CREATE_MUSIC_LIBRARY
                | UserRequest.CREATE_MOVIE_LIBRARY
                | UserRequest.CREATE_TV_LIBRARY
                | UserRequest.CREATE_MUSIC_PLAYLIST
            ):
                library.create()

            case (
                UserRequest.DELETE_MOVIE_LIBRARY
                | UserRequest.DELETE_TV_LIBRARY
                | UserRequest.DELETE_MUSIC_LIBRARY
                | UserRequest.DELETE_MUSIC_PLAYLIST
            ):
                library.delete()

            case UserRequest.SET_SERVER_SETTINGS:
                PlexOps.set_server_settings(plex_server, preferences_dto)

            case UserRequest.EXPORT_MUSIC_PLAYLIST:
                # Remove existing playlist.db file
                bootstrap_paths_dto.plexutil_playlists_db_dir.unlink(
                    missing_ok=True
                )

                music_playlist_dtos = cast(
                    "Playlist", library
                ).get_all_playlists()
                service = SongMusicPlaylistCompositeService(
                    bootstrap_paths_dto.plexutil_playlists_db_dir
                )
                service.add_many(music_playlist_dtos)

            case UserRequest.IMPORT_MUSIC_PLAYLIST:
                composite_service = SongMusicPlaylistCompositeService(
                    bootstrap_paths_dto.plexutil_playlists_db_dir
                )
                playlist_service = MusicPlaylistService(
                    bootstrap_paths_dto.plexutil_playlists_db_dir
                )
                music_playlist_dtos = composite_service.get(
                    entities=playlist_service.get_all(),
                    tracks=cast("list[Track]", library.query()),
                )

                for dto in music_playlist_dtos:
                    library = Playlist(
                        plex_server=plex_server,
                        language=language,
                        songs=dto.songs,
                        library_type=LibraryType.MUSIC,
                        name=library_name,
                        playlist_name=dto.name,
                        locations=locations,
                    )
                    library.create()

            case UserRequest.ADD_SONGS_TO_MUSIC_PLAYLIST:
                cast("Playlist", library).add_songs()

            case UserRequest.DELETE_SONGS_FROM_MUSIC_PLAYLIST:
                cast("Playlist", library).delete_songs()

    except SystemExit as e:
        if e.code == 0:
            description = "Successful System Exit"
            PlexUtilLogger.get_logger().debug(description)
        else:
            description = f"\n=====Unexpected Error=====\n{e!s}"
            PlexUtilLogger.get_logger().exception(description)
            raise

    except ServerConfigError as e:
        sys.tracebacklimit = 0
        description = f"\n=====Server Config Error=====\n{e!s}"
        PlexUtilLogger.get_logger().error(description)
        sys.exit(1)

    except UserError as e:
        sys.tracebacklimit = 0
        description = f"\n=====User Error=====\n{e!s}"
        PlexUtilLogger.get_logger().error(description)
        sys.exit(1)

    except LibraryIllegalStateError as e:
        sys.tracebacklimit = 0
        description = f"\n=====Library Illegal State Error=====\n{e!s}"
        PlexUtilLogger.get_logger().error(description)
        sys.exit(1)

    except LibraryOpError as e:
        sys.tracebacklimit = 0
        description = f"\n=====Library Operation Error=====\n{e!s}"
        PlexUtilLogger.get_logger().error(description)
        sys.exit(1)

    except LibraryPollTimeoutError as e:
        sys.tracebacklimit = 0
        description = f"\n=====Library Poll Tiemout Error=====\n{e!s}"
        PlexUtilLogger.get_logger().error(description)
        sys.exit(1)

    except LibrarySectionMissingError as e:
        sys.tracebacklimit = 0
        description = f"\n=====Library Not Found Error=====\n{e!s}"
        PlexUtilLogger.get_logger().error(description)
        sys.exit(1)

    except UnexpectedArgumentError as e:
        sys.tracebacklimit = 0
        description = (
            "\n=====User Argument Error=====\n"
            "These arguments are unrecognized: \n"
        )
        for argument in e.args[0]:
            description += "-> " + argument + "\n"
        PlexUtilLogger.get_logger().error(description)
        sys.exit(1)

    except ValidationError as e:
        sys.tracebacklimit = 0
        description = f"\n=====Invalid Schema Error=====\n{e!s}"
        PlexUtilLogger.get_logger().error(description)

    # No regular logger can be expected to be initialized
    except BootstrapError as e:
        description = f"\n=====Program Initialization Error=====\n{e!s}"
        e.args = (description,)
        raise

    except Exception as e:  # noqa: BLE001
        description = f"\n=====Unexpected Error=====\n{e!s}"
        PlexUtilLogger.get_logger().exception(description)


if __name__ == "__main__":
    main()
