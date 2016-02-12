__author__ = 'hezhiyu'

from sqlalchemy import BigInteger, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column

Base = declarative_base()


class User(Base):

    __tablename__ = 'user'
    id = Column(BigInteger, primary_key=True)
    username = Column(Text)
    password = Column(Text)


class Entry(Base):

    __tablename__ = 'entries'
    id = Column(BigInteger, primary_key=True)
    uid = Column(BigInteger)
    title = Column(Text)
    text = Column(Text)
