#!/usr/bin/python3
""" Defines the place class """
import models
from os import getenv
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy import ForeignKey, Table
from models.amenity import Amenity
from models.review import Review
from sqlalchemy.orm import relationship

association_table = Table("place_amenity", Base.metadata,
                          Column("place_id", String(60),
                                 ForeignKey("places.id"),
                                 primary_key=True, nullable=False),
                          Column("amenity_id", String(60),
                                 ForeignKey("amenities.id"),
                                 primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0)
    number_bathrooms = Column(Integer, default=0)
    max_guest = Column(Integer, default=0)
    price_by_night = Column(Integer, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    reviews = relationship("Review", backref="place", cascade="delete")
    amenities = relationship("Amenity", secondary="place_amenity",
                             overlaps="place_amenities", viewonly=False)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE", None) != "db":
        @property
        def reviews(self):
            """Get a list of all linked reviews"""
            review_list = []
            for rev in list(models.storage.all(Review).values()):
                if rev.place_id == self.id:
                    review_list.append(rev)
            return review_list

        @property
        def amenities(self):
            """ Get/Set linked amenities"""
            amenity_list = []
            for amen in list(models.storage.all(Amenity).values()):
                if amen.id in self.amenity_ids:
                    amenity_list.append(amen)
            return amenity_list

        @amenities.setter
        def amenities(self, value):
            if type(value) == Amenity:
                self.amenity_ids.append(value.id)
