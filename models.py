from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Prototype(Base):
    __tablename__ = 'prototypes'

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, index=True)
    engine_type = Column(String)
    horsepower = Column(Integer)
    weight = Column(Float)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    # test for alembic fuction
    is_active = Column(Boolean, default=True)
    # other test
    phone = Column(String, nullable=True)
