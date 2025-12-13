from plexutil.dto.server_config_dto import ServerConfigDTO
from plexutil.model.server_config_entity import ServerConfigEntity


class ServerConfigMapper:
    def get_dto(self, entity: ServerConfigEntity) -> ServerConfigDTO:
        return ServerConfigDTO(
            host=str(entity.host) if entity.host else None,
            port=int(entity.port) if entity.port else None,  # pyright: ignore [reportArgumentType]
            token=str(entity.token) if entity.token else None,
        )

    def get_entity(self, dto: ServerConfigDTO) -> ServerConfigEntity:
        return ServerConfigEntity(
            host=dto.host, port=dto.port, token=dto.token
        )
