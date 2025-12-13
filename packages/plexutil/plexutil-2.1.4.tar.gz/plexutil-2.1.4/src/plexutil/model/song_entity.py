import uuid

from peewee import Model, TextField, UUIDField


class SongEntity(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    name = TextField(null=True, default=None, unique=True)

    class Meta:
        table_name = "music_song"
