#!/usr/bin/python3
""" Defines the City subclass of the HBNB clone """
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """ The city class, contains state ID and name
        Attributes:
            __tablename__ (str): represents the table name, cities
            name (sqlalchemy String): column containing a (128 char) str
            state_id (salalchemy String): column containig (60 char) str FK.

    """
    __tablename__ = 'cities'
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    places = relationship("Place", backref="city", cascade="delete")
