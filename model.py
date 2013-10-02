from sqlalchemy import create_engine, Column, Date, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import settings
import hashlib

Base = declarative_base()

def db_connect():
    return create_engine(URL(**settings.DATABASE))

def create_table(engine):
    Base.metadata.create_all(engine)

class Dish(Base):
    __tablename__ = "dishes"

    id = Column(String, primary_key = True)
    location = Column("location", String)
    station = Column("station", String)
    title = Column("title", String)
    date = Column("date", Date)

    def generate_id(self):
        self.id = hashlib.md5(self.location + self.station + self.title + str(self.date)).hexdigest()
