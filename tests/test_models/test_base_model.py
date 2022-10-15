#!/usr/bin/python3
""" """
import unittest
from datetime import datetime
from models.base_model import BaseModel
import pep8
import os
from models.engine.file_storage import FileStorage


class test_basemodel(unittest.TestCase):
    """unittest for testing the BaseModel class """

    @classmethod
    def setUpClass(cls):
        """setup for the test """
        try:
            os.rename("file.json", "temp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
        cls.storage = FileStorage()
        cls.base = BaseModel()

    @classmethod
    def tearDown(cls):
        " test BaseModel teardown"
        del cls.base

    def tearDown(self):
        "tear down"
        try:
            os.remove('file.json')
        except Exception:
            pass

    @unittest.skipIf(os.getenv("HBNB_ENV") is not None, "Testing DBStorage")
    def test_save(self):
        """ Test if the save works"""
        old = self.base.updated_at
        self.base.save()
        self.assertLess(old, self.base.updated_at)
        with open("file.json", "r") as f:
            self.assertIn("BaseModel.{}".format(self.base.id), f.read())
