from sqlalchemy import TEXT, MetaData, Column, ForeignKey, Integer, String, Float, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text
from sqlalchemy.dialects.mysql import LONGTEXT

from helpers.constants import DB_NAMING_CONVENTION, Gender

metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)
Base = declarative_base(metadata=metadata)

class BaseModel(Base):
    __abstract__ = True

class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    avatar_url = Column(String(255))
    alias = Column(String(256))
    created_at = Column(DateTime, default=text("current_timestamp"))
    last_play_id = Column(Integer, ForeignKey("songs.id"))

    last_play = relationship(
        "Song", primaryjoin="User.last_play_id == Song.id", backref="songs")
    playlists = relationship("Playlist", back_populates="user", lazy='joined')
    favorites = relationship("Song", secondary="user_favorites",
                             back_populates="favorites_owner", lazy='joined')


class Song(BaseModel):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    duration = Column(Float)
    genre = Column(String(255))

    artists = relationship("Artist", secondary="song_artists",
                           back_populates="songs")
    albums = relationship("Album", secondary="song_albums", back_populates="songs")
    playlists = relationship(
        "Playlist", secondary="playlist_songs", back_populates="songs")
    favorites_owner = relationship(
        "User", secondary="user_favorites", back_populates="favorites")


class Album(BaseModel):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    release_date = Column(DateTime)

    artist_id = Column(Integer, ForeignKey("artists.id"))
    artist = relationship("Artist", back_populates="albums")

    songs = relationship("Song", secondary="song_albums", back_populates="albums")


class Artist(BaseModel):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    bio = Column(String(4294000000))
    genre = Column(String(255))
    gender = Column(Enum(Gender))

    albums = relationship("Album", back_populates="artist")
    songs = relationship("Song", secondary="song_artists", back_populates="artists")


class Playlist(BaseModel):
    __tablename__ = "playlists"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    creation_date = Column(DateTime, default=text("current_timestamp"))
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="playlists")
    songs = relationship("Song", secondary="playlist_songs", back_populates="playlists")


class PlaylistSongAssociation(BaseModel):
    __tablename__ = "playlist_songs"

    playlist_id = Column(Integer, ForeignKey("playlists.id"), primary_key=True)
    song_id = Column(Integer, ForeignKey("songs.id"), primary_key=True)


class UserFavorite(BaseModel):
    __tablename__ = "user_favorites"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    song_id = Column(Integer, ForeignKey("songs.id"), primary_key=True)


class SongArtistAssociation(BaseModel):
    __tablename__ = "song_artists"

    song_id = Column(Integer, ForeignKey("songs.id"), primary_key=True)
    artist_id = Column(Integer, ForeignKey("artists.id"), primary_key=True)


class SongAlbumAssociation(BaseModel):
    __tablename__ = "song_albums"

    song_id = Column(Integer, ForeignKey("songs.id"), primary_key=True)
    album_id = Column(Integer, ForeignKey("albums.id"), primary_key=True)
