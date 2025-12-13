from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

from peewee import SqliteDatabase


@contextmanager
def db_manager(
    db_path: Path, entities: list, is_atomic: bool = False
) -> Generator[SqliteDatabase, None, None]:
    db = SqliteDatabase(db_path, pragmas={"foreign_keys": 1})
    db.bind(entities)
    db.create_tables(entities)

    if is_atomic:
        with db.atomic() as transaction:
            yield transaction
    else:
        with db:
            yield db
