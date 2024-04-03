import unittest

import models
from models.engine.file_storage import FileStorage
import unittest
import json


class TestFileStorage(unittest.TestCase):
    def setUp(self) -> None:
        self.model = models.base_model.BaseModel()
        self.key = "{}.{}".format(
            self.model.__class__.__name__, self.model.id
        )

    def test_FileStorage_docstring(self):
        self.assertIsNotNone(models.engine.file_storage.__doc__, 'Module has no docstring')
        self.assertIsNotNone(FileStorage.__doc__, "FileStorage has no docstring")

    def test_new_and_all(self):
        models.storage.new(self.model)

        all_obj = models.storage.all()

        self.assertIsInstance(all_obj, dict, 'Datastructure not an dict instance')
        self.assertIn(self.key, all_obj)

    def test_save(self):
        models.storage.new(self.model)

        models.storage.save_obj()
        with open('file.json', 'r') as file:
            content = json.load(file)
            for k, v in content.items():
                self.assertIn('__class__', v, '__class__ not found')
            self.assertIn(self.key, content, 'save_obj did not save the object')

    def test_reload_obj(self):
        pass
 git add tests/test_basemodel_and_filestorage/test_filestorage.py
  597  git commit -m "unittest for new_and_all method"
