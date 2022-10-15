#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is not None:
            if type(cls) == str:
                cls = eval(cls)
            cls_dict = {}
            for key, value in self.__objects.items():
                if type(value) == cls:
                    cls_dict[key] = value
            return cls_dict
        return self.__objects

    def new(self, obj):
        """sets __object to given obj"""
        self.__objects["{}.{}".format(type(obj).__name__, obj.id)] = obj

    def save(self):
        """Serialize the file to JSON file path"""
        odict = {o: self.__objects[o].to_dict() for o in self.__objects.keys()}
        with open(self.__file_path, 'w', encoding="UTF-8") as f:
            json.dump(odict, f)

    def reload(self):
        """deserialize the file path to JSON file path"""
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                for i in json.load(f).values():
                    name = i["__class__"]
                    del i["__class__"]
                    self.new(eval(name)(**i))
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """delete obj from __objects if pressent"""
        try:
            del self.__objects["{}.{}".format(type(obj).__name__, obj.id)]
        except (AttributeError, KeyError):
            pass

    def close(self):
        """ Call the reload method."""
        self.reload()
