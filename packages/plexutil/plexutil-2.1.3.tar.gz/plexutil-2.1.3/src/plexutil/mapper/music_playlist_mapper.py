from plexutil.dto.music_playlist_dto import MusicPlaylistDTO
from plexutil.model.music_playlist_entity import MusicPlaylistEntity


class MusicPlaylistMapper:
    def get_dto(self, entity: MusicPlaylistEntity) -> MusicPlaylistDTO:
        return MusicPlaylistDTO(name=str(entity.name), songs=[])

    def get_entity(self, dto: MusicPlaylistDTO) -> MusicPlaylistEntity:
        return MusicPlaylistEntity(name=str(dto.name))
