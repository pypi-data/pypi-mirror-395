from peewee import CompositeKey, ForeignKeyField, Model

from plexutil.model.music_playlist_entity import MusicPlaylistEntity
from plexutil.model.song_entity import SongEntity


class SongMusicPlaylistEntity(Model):
    playlist = ForeignKeyField(
        MusicPlaylistEntity, backref="songs", on_delete="CASCADE"
    )
    song = ForeignKeyField(
        SongEntity, backref="playlists", on_delete="CASCADE"
    )

    class Meta:
        table_name = "song_music_playlist"
        primary_key = CompositeKey("playlist", "song")
