from sqlalchemy import Column, Integer, String, Float
from database import Base


class Prototype(Base):
    __tablename__ = 'prototypes'

    id = Column(Integer, primary_key=True)
    model_name = Column(String, unique=True)
    engine_type = Column(String)
    horsepower = Column(Integer)
    weight = Column(Float)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
