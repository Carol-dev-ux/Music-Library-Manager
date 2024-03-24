from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Artist(Base):
    __tablename__ = 'artists'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Album(Base):
    __tablename__ = 'albums'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    artist_id = Column(Integer, ForeignKey('artists.id'))
    artist = relationship('Artist', backref='albums', cascade='all, delete')

class Song(Base):
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    genre = Column(String)
    release_year = Column(Integer)
    duration = Column(Integer)
    album_id = Column(Integer, ForeignKey('albums.id'))
    album = relationship('Album', backref='songs', cascade='all, delete')


