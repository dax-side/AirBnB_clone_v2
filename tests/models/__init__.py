#!/usr/bin/python3
""" Instatiates a storage object
    -> If HBNB_TYPE_STORAGE is db:
        import DBStorage class in file
        create an instance of DBStorage and store it in the
        variable storage
    -> Else:
        import FileStorage class in file
        create an instance of FileStorage and store it in the
        variable storage
"""

from os import getenv

# check environ variable to determine storage method
if getenv('HBNB_TYPE_STORAGE') == 'db':  # DBStorage selected
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
    storage.reload()

else:  # file storage selected
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
    storage.reload()
