import sqlalchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    normal_title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)
