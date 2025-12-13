import uuid

from peewee import Model, TextField, UUIDField


class MusicPlaylistEntity(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    name = TextField(null=False)

    class Meta:
        table_name = "music_playlist"
        indexes = ((("name",), True),)
