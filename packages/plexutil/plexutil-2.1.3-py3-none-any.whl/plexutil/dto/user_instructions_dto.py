from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from plexutil.dto.server_config_dto import ServerConfigDTO
from plexutil.enums.language import Language

if TYPE_CHECKING:
    from pathlib import Path

    from plexutil.enums.library_type import LibraryType
    from plexutil.enums.user_request import UserRequest


def create_server_config() -> ServerConfigDTO:
    return ServerConfigDTO()


# Frozen=True creates an implicit hash method, eq is created by default
@dataclass(frozen=True)
class UserInstructionsDTO:
    request: UserRequest
    library_type: LibraryType
    library_name: str
    playlist_name: str
    server_config_dto: ServerConfigDTO = field(
        default_factory=create_server_config
    )
    is_show_configuration: bool = False
    is_show_configuration_token: bool = False
    language: Language = Language.ENGLISH_US
    locations: list[Path] = field(default_factory=list)
    songs: list[str] = field(default_factory=list)
