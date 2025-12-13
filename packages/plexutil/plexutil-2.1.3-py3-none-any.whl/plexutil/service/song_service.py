from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


from plexutil.model.song_entity import SongEntity
from plexutil.service.db_manager import db_manager


class SongService:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path

    def get(self, entity: SongEntity) -> SongEntity:
        with db_manager(self.db_path, [SongEntity]):
            return (
                SongEntity.select().where(SongEntity.name == entity.name).get()
            )

    def get_many(self, entities: list[SongEntity]) -> list[SongEntity]:
        with db_manager(self.db_path, [SongEntity]):
            names = [x.name for x in entities]
            return SongEntity.select().where(SongEntity.name.in_(names))

    def save(self, entity: SongEntity) -> SongEntity:
        force_insert = not self.exists(entity)

        with db_manager(self.db_path, [SongEntity]):
            filtered_fields = [
                k for k, v in entity.__data__.items() if v and k != "id"
            ]
            return entity.save(force_insert=force_insert, only=filtered_fields)

    def exists(self, entity: SongEntity) -> bool:
        return (
            SongEntity.select().where(SongEntity.name == entity.name).exists()
        )

    def add_many(self, entities: list[SongEntity]) -> None:
        with db_manager(self.db_path, [SongEntity], is_atomic=True):
            bulk = [(song.name,) for song in entities]

            for idx in range(0, len(bulk), 100):
                SongEntity.insert_many(
                    bulk[idx : idx + 100],
                    fields=[SongEntity.name],
                ).execute()
