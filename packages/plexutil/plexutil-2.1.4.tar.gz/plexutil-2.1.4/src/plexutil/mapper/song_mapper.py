from plexutil.dto.song_dto import SongDTO
from plexutil.model.song_entity import SongEntity


class SongMapper:
    def get_dto(self, song_entity: SongEntity) -> SongDTO:
        return SongDTO(
            name=str(song_entity.name),
        )

    def get_entity(self, song_dto: SongDTO) -> SongEntity:
        return SongEntity(
            name=song_dto.name,
        )
