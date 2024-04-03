import unittest

import models
from models.engine.file_storage import FileStorage
import unittest
import json


class TestFileStorage(unittest.TestCase):
    def setUp(self) -> None:
        self.filestorage = FileStorage()
        self.model = models.base_model.BaseModel()

    def test_FileStorage_docstring(self):
        self.assertIsNotNone(models.engine.file_storage.__doc__, 'Module has no docstring')
        self.assertIsNotNone(FileStorage.__doc__, "FileStorage has no docstring")

    def test_new_and_all(self):
        models.storage.new(self.model)
        key = "{}.{}".format(
            self.model.__class__.__name__, self.model.id
        )
        all_obj = models.storage.all()

        self.assertIn(key, all_obj.keys())




        # print(key)
#
# if __name__ == '__main__':
#     unittest.TestCase()
