#!/usr/bin/python3
""" Defines the Amenity class for HBNB clone"""
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """ Amenities class definition
        Attributes:
            __tablename__
            name
            places_amenities
    """
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    place_amenities = relationship("Place", secondary="place_amenity",
                                   viewonly=False)
