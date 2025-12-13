from plexutil.dto.bootstrap_paths_dto import BootstrapPathsDTO
from plexutil.dto.server_config_dto import ServerConfigDTO
from plexutil.mapper.server_config_mapper import ServerConfigMapper
from plexutil.plex_util_logger import PlexUtilLogger
from plexutil.service.server_config_service import ServerConfigService
from plexutil.util.token_manager import TokenManager


class ServerConfig:
    def __init__(
        self,
        bootstrap_paths_dto: BootstrapPathsDTO,
        server_config_dto: ServerConfigDTO,
    ) -> None:
        self.server_config_dto = server_config_dto
        self.service = ServerConfigService(
            bootstrap_paths_dto.config_dir / "config.db"
        )
        self.mapper = ServerConfigMapper()

    def get(self) -> ServerConfigDTO:
        server_config_dto = self.mapper.get_dto(self.service.get())
        if server_config_dto.token:
            token = TokenManager.decrypt(server_config_dto.token)
        else:
            token = None

        return ServerConfigDTO(
            host=server_config_dto.host,
            port=server_config_dto.port,
            token=token,
        )

    def save(self) -> ServerConfigDTO:
        if not self.service.exists():
            description = (
                f"No current Server Config exists.\n"
                f"Received a request to create a ServerConfig:\n"
                f"Host: {self.server_config_dto.host}\n"
                f"Port: {self.server_config_dto.port}\n"
                f"Token supplied: "
                f"{'YES' if self.server_config_dto.token else 'NO'}\n"
            )
            PlexUtilLogger.get_logger().debug(description)

        if self.server_config_dto.token:
            encrypted_token = TokenManager.encrypt(
                self.server_config_dto.token
            )
        else:
            encrypted_token = None

        dto = ServerConfigDTO(
            host=self.server_config_dto.host,
            port=self.server_config_dto.port,
            token=encrypted_token,
        )

        self.service.save(self.mapper.get_entity(dto))

        entity = self.service.get()
        server_config_dto = self.mapper.get_dto(entity)

        if server_config_dto.token:
            decrypted_token = TokenManager.decrypt(server_config_dto.token)
        else:
            decrypted_token = None

        dto = ServerConfigDTO(
            host=server_config_dto.host,
            port=server_config_dto.port,
            token=decrypted_token,
        )
        description = (
            f"Loaded a server config:\n"
            f"Host: {server_config_dto.host}\n"
            f"Port: {server_config_dto.port}\n"
            f"Token supplied: {'YES' if server_config_dto.token else 'NO'}\n"
        )
        PlexUtilLogger.get_logger().debug(description)

        return dto
