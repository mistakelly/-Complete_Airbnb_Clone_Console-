import json

import models.base_model
from models.base_model import BaseModel
import unittest
import inspect
from datetime import datetime


class Test_test_base_model(unittest.TestCase):
    pass


class TestBaseModel(unittest.TestCase):

    def setUp(self) -> None:
        self.model = BaseModel()

    def test_module_and_BaseModel_doc_string(self):
        self.assertIsNotNone(models.base_model.__doc__, f'Module {models.base_model} has no docstring')
        self.assertIsNotNone(BaseModel.__doc__, 'BaseModel class has no docstring')

    def test_methods_doc_string(self):
        BaseModel_method = inspect.getmembers(self.model, inspect.isfunction)
        for name, method in BaseModel_method:
            self.assertIsNotNone(method.__doc__, f"Method {name} of BaseModel has no docstring")

    def test_init_method(self):

        self.assertTrue(hasattr(self.model, 'id'), 'Attribute id does not exist')
        self.assertTrue(hasattr(self.model, 'created_at'), 'Attribute created_at does not exist')
        self.assertTrue(hasattr(self.model, 'updated_at'), 'Attribute updated_at does not exist')

        self.assertIsInstance(self.model.id, str, 'Attribute id is Not string instance')
        self.assertIsInstance(self.model.created_at, datetime, f'Attribute created_at is not a datetime instance')
        self.assertIsInstance(self.model.updated_at, datetime, f'Attribute updated_at is not a datetime instance')
        self.assertIsInstance(self.model, BaseModel, f"Object is Not an instance of {BaseModel}")

    def test_custom_init(self):
        model_json = self.model.to_dict()
        model_dict = BaseModel(**model_json)

        self.assertIsInstance(model_dict, BaseModel, "Deserialized object is not an instance of BaseModel")
        self.assertIsInstance(model_json, dict, f"Serialized model is not a dictionary")

        self.assertIsInstance(model_dict.created_at, datetime, f'created_at is not an instance of datetime')
        self.assertIsInstance(model_dict.updated_at, datetime, f'updated_at is not an instance of datetime')

        self.assertEqual(self.model.id, model_dict.id, "Ids dont match")
        self.assertEqual(self.model.created_at, model_dict.created_at, 'created_at attribute don\'t match')
        self.assertEqual(self.model.updated_at, model_dict.updated_at, 'updated_at attribute don\'t match')

    def test_str_method(self):

        expected_str = "[{}] ({}) {}".format(
            self.model.__class__.__name__,
            self.model.id,
            self.model.__dict__
        )

        self.assertEqual(self.model.__str__(), expected_str, "strings don't match")

    def test_save_method(self):
        model = BaseModel()
        all_obj = models.storage.all()

        model_updated_at = model.updated_at
        # simulate change.
        model.save()
        updated_model_time = model.updated_at
        self.assertNotEqual(model_updated_at, updated_model_time,
                            "Attribute updated_at did not update the created_at time")

        # construct key
        key = f"{model.__class__.__name__}.{model.id}"
        self.assertIn(key, all_obj, "No entry for the newly created object")
        # call all_obj in the filestorage and check if the key object key is present.

        # check if the object attribute was saved in the file_storage (file.json).
        with open("file.json", 'r') as file:
            content = json.load(file)
            self.assertIn(key, content, "save_obj did not save the object data to filestorage")

    def test_todict_method(self):
        model_json = self.model.to_dict()

        self.assertIsInstance(model_json, dict, 'Object not a dict instance')

        self.assertIn('__class__', model_json, "__class__ not present in dictionary")
        self.assertIsInstance(model_json['created_at'], str,  'Attribute created_at is not an instance of datetime')
        self.assertIsInstance(model_json['updated_at'], str,  'Attribute updated_at is not an instance of datetime')

        self.assertIsInstance(self.model.created_at, datetime,
                              f'Attribute created_at is not a datetime instance'
                              f' after the execution of to_dict method')
        self.assertIsInstance(self.model.updated_at, datetime,
                              f'Attribute updated_at is not a datetime instance'
                              f' after the execution of to_dict method')
