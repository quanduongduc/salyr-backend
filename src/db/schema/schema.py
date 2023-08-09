from sqlalchemy import (
    ForeignKey,
    MetaData,
    Table,
    create_engine,
    Column,
    Integer,
    String,
    Float,
    DateTime,
)
from sqlalchemy.ext.declarative import declarative_base

from helpers.constants import DB_NAMING_CONVENTION

metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)

Base = declarative_base(metadata=metadata)


song_artists_association = Table(
    "song_artists",
    Base.metadata,
    Column("song_id", Integer, ForeignKey("songs.id", ondelete="CASCADE")),
    Column("artist_id", Integer, ForeignKey("artists.id", ondelete="CASCADE")),
)

song_albums_association = Table(
    "song_albums",
    Base.metadata,
    Column("song_id", Integer, ForeignKey("songs.id", ondelete="CASCADE")),
    Column("album_id", Integer, ForeignKey("albums.id", ondelete="CASCADE")),
)

playlist_songs_association = Table(
    "playlist_songs",
    Base.metadata,
    Column("playlist_id", Integer, ForeignKey("playlists.id", ondelete="CASCADE")),
    Column("song_id", Integer, ForeignKey("songs.id", ondelete="CASCADE")),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    email = Column(String(255))
    hashed_password = Column(String(255))
    avatar_url = Column(String(255))
    created_at = Column(DateTime)


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    release_date = Column(DateTime)
    duration = Column(Float)
    genre = Column(String(255))


class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    bio = Column(String(255))
    genre = Column(String(255))


class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    artist_id = Column(Integer, ForeignKey("artists.id", ondelete="CASCADE"))
    release_date = Column(DateTime)
    cover_image_url = Column(String(255))


class Playlist(Base):
    __tablename__ = "playlists"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    title = Column(String(255))
    creation_date = Column(DateTime)


class UserFavorite(Base):
    __tablename__ = "user_favorites"

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    song_id = Column(
        Integer, ForeignKey("songs.id", ondelete="CASCADE"), primary_key=True
    )


class PlayHistory(Base):
    __tablename__ = "play_history"

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    song_id = Column(
        Integer, ForeignKey("songs.id", ondelete="CASCADE"), primary_key=True
    )
    timestamp = Column(DateTime)
