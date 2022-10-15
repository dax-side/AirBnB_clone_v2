#!/usr/bin/python3
""" Defines a Review class for HBNB clone """
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Review(BaseModel, Base):
    """ Review class definition
        Attributes:
            __tablename__
            text
            place_id
            user_id
    """
    __tablename__ = "reviews"
    text = Column(String(1024), nullable=False)
    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
