#!/usr/bin/python3
""" This module creates a new engine DBStorage"""

from os import getenv
from models.base_model import Base
from models.base_model import BaseModel
from models.amenity import Amenity
from models.state import State
from models.city import City
from models.user import User
from models.review import Review
from models.place import Place
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


class DBStorage():
    """ Defines a database storage class
            Private class attribute:
                __engine: set to None
                __Session: set to None
            Public instance methods:
                __init__(self):
                all(self, cls=None):
                new(self, obj):
                save(self):
                delete(Self, obj=None):
                reload(self):
    """
    __engine = None
    __session = None

    def __init__(self):
        """ Initializes the ne DBStorage instance"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(getenv('HBNB_MYSQL_USER'),
                                             getenv('HBNB_MYSQL_PWD'),
                                             getenv('HBNB_MYSQL_HOST'),
                                             getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ query on the current database session all objects of a given class
            if cls=None, query all types of objects

            Return: A dictionary format <class name>.<object id> = obj.
        """
        if cls is None:
            objs = self.__session.query(State).all()
            objs.extend(self.__session.query(User).all())
            objs.extend(self.__session.query(City).all())
            objs.extend(self.__session.query(Place).all())
            objs.extend(self.__session.query(Review).all())
            objs.extend(self.__session.query(Amenity).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            objs = self.__session.query(cls)
        return {"{}.{}".format(type(o).__name__, o.id): o for o in objs}

    def new(self, obj):
        """ Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """ Commit all changes of the current DB session"""
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete from the current DB session obj if Not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """ Create all tables in the database and initialise new session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """ Close the working SQLALCHEMY session."""
        self.__session.close()
