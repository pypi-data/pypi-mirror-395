import uuid

from peewee import CompositeKey, Model, TextField, UUIDField


class PlexUtilLibraryConfigEntity(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    name = TextField(null=False)
    library_type = TextField(null=False)
    location = TextField(null=False)

    class Meta:
        table_name = "library_config"
        primary_key = CompositeKey("name", "library_type")
