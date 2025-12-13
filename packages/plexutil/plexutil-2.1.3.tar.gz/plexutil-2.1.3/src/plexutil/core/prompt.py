from __future__ import annotations

import argparse
import pathlib
import sys
from argparse import RawTextHelpFormatter
from importlib.metadata import PackageNotFoundError, version

from plexutil.dto.server_config_dto import ServerConfigDTO
from plexutil.dto.user_instructions_dto import UserInstructionsDTO
from plexutil.enums.language import Language
from plexutil.enums.library_type import LibraryType
from plexutil.enums.user_request import UserRequest
from plexutil.exception.unexpected_argument_error import (
    UnexpectedArgumentError,
)
from plexutil.plex_util_logger import PlexUtilLogger
from plexutil.static import Static
from plexutil.util.file_importer import FileImporter


class Prompt(Static):
    @staticmethod
    def get_user_instructions_dto() -> UserInstructionsDTO:
        parser = argparse.ArgumentParser(
            description="Plexutil", formatter_class=RawTextHelpFormatter
        )

        request_help_str = "Supported Requests: \n"

        for request in UserRequest.get_all():
            request_help_str += "-> " + request.value + "\n"

        parser.add_argument(
            "request",
            metavar="Request",
            type=str,
            nargs="?",
            help=request_help_str,
        )

        parser.add_argument(
            "-s",
            "--songs",
            metavar="songs",
            nargs="+",
            help=(
                "Songs to be passed to a musical request, "
                'i.e create_music_playlist --songs "path/to/song"'
                '" path_to_song"'
            ),
            default=[],
        )

        parser.add_argument(
            "-pn",
            "--playlist_name",
            metavar="Playlist Name",
            type=str,
            nargs="+",
            help=("Name of the playlist"),
            default=[],
        )

        parser.add_argument(
            "-loc",
            "--locations",
            metavar="Library Locations",
            type=pathlib.Path,
            nargs="+",
            help="Library Locations",
            default=[],
        )

        parser.add_argument(
            "-libn",
            "--library_name",
            metavar="Library Name",
            type=str,
            nargs="+",
            help="Library Name",
            default=[],
        )

        parser.add_argument(
            "-l",
            "--language",
            metavar="Library Language",
            type=str,
            nargs="?",
            help="Library Language",
            default=Language.ENGLISH_US.value,
        )

        parser.add_argument(
            "-host",
            "--plex_server_host",
            metavar="Plex Server Host",
            type=str,
            nargs="?",
            help="Plex server host e.g. localhost",
        )

        parser.add_argument(
            "-port",
            "--plex_server_port",
            metavar="Plex Server Port",
            type=int,
            nargs="?",
            help="Plex server port e.g. 32400",
        )

        parser.add_argument(
            "-token",
            "--plex_server_token",
            metavar="Plex Server Token",
            type=str,
            nargs="?",
            help=(
                "Fetch the token by listening for an"
                "(X-Plex-Token) query parameter"
            ),
        )

        parser.add_argument(
            "-sc",
            "--show_configuration",
            action="store_true",
            help=("Displays host,port"),
        )

        parser.add_argument(
            "-sct",
            "--show_configuration_token",
            action="store_true",
            help=("Displays host,port,token"),
        )

        parser.add_argument(
            "-v",
            "--version",
            action="store_true",
            help=("Displays version"),
        )

        args, unknown = parser.parse_known_args()

        if unknown:
            raise UnexpectedArgumentError(unknown)

        request = args.request
        songs = args.songs
        playlist_name = args.playlist_name
        is_version = args.version
        is_show_configuration = args.show_configuration
        is_show_configuration_token = args.show_configuration_token
        language = Language.get_from_str(args.language)
        plex_server_host = args.plex_server_host
        plex_server_port = args.plex_server_port
        plex_server_token = args.plex_server_token
        locations = args.locations
        library_type = LibraryType.MUSIC
        if request:
            library_type = UserRequest.get_library_type_from_request(
                UserRequest.get_user_request_from_str(args.request)
            )
        library_name = args.library_name

        playlist_name = " ".join(playlist_name) if playlist_name else ""
        library_name = " ".join(library_name) if library_name else ""

        if is_version:
            plexutil_version = ""

            try:
                plexutil_version = version("plexutil")

            except PackageNotFoundError:
                pyproject = FileImporter.get_pyproject()
                plexutil_version = pyproject["project"]["version"]

            PlexUtilLogger.get_logger().info(plexutil_version)
            sys.exit(0)

        if request:
            request = UserRequest.get_user_request_from_str(request)

        server_config_dto = ServerConfigDTO(
            host=plex_server_host,
            port=plex_server_port,
            token=plex_server_token,
        )

        debug = (
            "Received a User Request:\n"
            f"Request: {request.value if request else None}\n"
            f"Songs: {songs!s}\n"
            f"Playlist Name: {playlist_name}\n"
            f"Host: {plex_server_host}\n"
            f"Port: {plex_server_port}\n"
            f"show config: {is_show_configuration!s}\n"
            f"show config token: {is_show_configuration_token!s}\n"
            f"Language: {language.value}\n"
            f"Locations: {locations!s}\n"
            f"Library Name: {library_name}\n"
            f"Library Type: {library_type.value}\n"
        )
        PlexUtilLogger.get_logger().debug(debug)

        return UserInstructionsDTO(
            request=request,
            is_show_configuration=is_show_configuration,
            is_show_configuration_token=is_show_configuration_token,
            library_type=library_type,
            library_name=library_name,
            playlist_name=playlist_name,
            songs=songs,
            locations=locations,
            server_config_dto=server_config_dto,
            language=language,
        )
