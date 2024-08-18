from dbconnection import Base
from sqlalchemy import Column, Integer, String, Date, Integer, ForeignKey, Table, Float, DateTime


class City(Base):

    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Summary(Base):

    __tablename__ = 'summaries'

    id = Column(Integer, primary_key=True)
    city = Column(Integer, ForeignKey('cities.id'))
    mintemp = Column(Float(2))
    maxtemp = Column(Float(2))
    averagetemp = Column(Float(2))
    dominantweather = Column(String)
    date = Column(Date)


class TempData(Base):

    __tablename__ = 'daily'

    id = Column(Integer, primary_key=True)
    city = Column(String)
    temp = Column(Float(2))
    feels_like = Column(Float(2))
    wethercondition = Column(String)
    time = Column(DateTime)