from peewee import IntegerField, Model, TextField


class ServerConfigEntity(Model):
    id = IntegerField(primary_key=True, default=1)
    host = TextField(null=True, default=None)
    port = IntegerField(null=True, default=None)
    token = TextField(null=True, default=None)

    class Meta:
        table_name = "server_config"
