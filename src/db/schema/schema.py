from sqlalchemy import MetaData, Table, create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from helpers.constants import DB_NAMING_CONVENTION

metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)

Base = declarative_base(metadata=metadata)


song_artists_association = Table('song_artists', Base.metadata,
                                 Column('song_id', Integer, ForeignKey('songs.id')),
                                 Column('artist_id', Integer, ForeignKey('artists.id'))
                                 )

song_albums_association = Table('song_albums', Base.metadata,
                                Column('song_id', Integer, ForeignKey('songs.id')),
                                Column('album_id', Integer, ForeignKey('albums.id'))
                                )

playlist_songs_association = Table('playlist_songs', Base.metadata,
                                   Column('playlist_id', Integer,
                                          ForeignKey('playlists.id')),
                                   Column('song_id', Integer, ForeignKey('songs.id'))
                                   )


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    email = Column(String(255))
    hashed_password = Column(String(255))
    avatar_url = Column(String(255))
    created_at = Column(DateTime)

    playlists = relationship('Playlist', back_populates='user',
                             cascade='all, delete-orphan')
    favorites = relationship('UserFavorite', back_populates='user',
                             cascade='all, delete-orphan')
    play_history = relationship(
        'PlayHistory', back_populates='user', cascade='all, delete-orphan')


class Song(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    release_date = Column(DateTime)
    duration = Column(Float)
    genre = Column(String(255))

    artists = relationship(
        'Artist', secondary=song_artists_association, back_populates='songs')
    albums = relationship('Album', secondary=song_albums_association)
    playlists = relationship(
        'Playlist', secondary=playlist_songs_association, back_populates='songs')
    favorites = relationship('UserFavorite', back_populates='song',
                             cascade='all, delete-orphan')
    play_history = relationship(
        'PlayHistory', back_populates='song', cascade='all, delete-orphan')


class Album(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    artist_id = Column(Integer, ForeignKey('artists.id'))
    release_date = Column(DateTime)
    cover_image_url = Column(String(255))

    artist = relationship('Artist', back_populates='albums')
    songs = relationship('Song', secondary=song_albums_association)


class Artist(Base):
    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    bio = Column(String(255))
    genre = Column(String(255))

    albums = relationship('Album', back_populates='artist')
    songs = relationship('Song', secondary=song_artists_association,
                         back_populates='artists')


class Playlist(Base):
    __tablename__ = 'playlists'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(255))
    creation_date = Column(DateTime)

    user = relationship('User', back_populates='playlists')
    songs = relationship('Song', secondary=playlist_songs_association,
                         back_populates='playlists')

class UserFavorite(Base):
    __tablename__ = 'user_favorites'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    song_id = Column(Integer, ForeignKey('songs.id'), primary_key=True)
    
    user = relationship('User', back_populates='user_favorites')
    song = relationship('Song', back_populates='user_favorites')


class PlayHistory(Base):
    __tablename__ = 'play_history'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    song_id = Column(Integer, ForeignKey('songs.id'), primary_key=True)
    timestamp = Column(DateTime)
    
    user = relationship('User', back_populates='play_history')
    song = relationship('Song', back_populates='play_history')
