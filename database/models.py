from sqlalchemy import Column, Integer, String
from database.connector import Base


class TestTable(Base):
    __tablename__ = 'tc'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)


class ABC2(Base):
    __tablename__ = 'abc2'
    id = Column(Integer, primary_key=True, autoincrement=True)