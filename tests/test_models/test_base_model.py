#!/usr/bin/python3
"""Unit tests for the BaseModel class."""
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """Unit tests for the BaseModel class."""

    def test_id_is_string(self):
        """id should be a string."""
        my_model = BaseModel()
        self.assertIsInstance(my_model.id, str)

    def test_id_is_unique(self):
        """Two instances should never share the same id."""
        model1 = BaseModel()
        model2 = BaseModel()
        self.assertNotEqual(model1.id, model2.id)

    def test_created_at_is_datetime(self):
        """created_at should be a datetime instance."""
        my_model = BaseModel()
        self.assertIsInstance(my_model.created_at, datetime)

    def test_updated_at_is_datetime(self):
        """updated_at should be a datetime instance."""
        my_model = BaseModel()
        self.assertIsInstance(my_model.updated_at, datetime)

    def test_created_at_and_updated_at_close_on_creation(self):
        """created_at and updated_at should start (almost) equal."""
        my_model = BaseModel()
        self.assertAlmostEqual(
            my_model.created_at.timestamp(),
            my_model.updated_at.timestamp(),
            delta=0.01,
        )

    def test_str_representation(self):
        """__str__ should follow [ClassName] (id) {dict} format."""
        my_model = BaseModel()
        expected = "[BaseModel] ({}) {}".format(
            my_model.id, my_model.__dict__)
        self.assertEqual(str(my_model), expected)

    def test_save_updates_updated_at(self):
        """save() should refresh updated_at to a later datetime."""
        my_model = BaseModel()
        old_updated_at = my_model.updated_at
        sleep(0.01)
        my_model.save()
        self.assertGreater(my_model.updated_at, old_updated_at)

    def test_to_dict_is_dict(self):
        """to_dict() should return a dict."""
        my_model = BaseModel()
        self.assertIsInstance(my_model.to_dict(), dict)

    def test_to_dict_contains_class_key(self):
        """to_dict() should add a __class__ key with the class name."""
        my_model = BaseModel()
        self.assertEqual(my_model.to_dict()["__class__"], "BaseModel")

    def test_to_dict_datetimes_are_strings(self):
        """created_at/updated_at should be ISO format strings."""
        my_model = BaseModel()
        obj_dict = my_model.to_dict()
        self.assertIsInstance(obj_dict["created_at"], str)
        self.assertIsInstance(obj_dict["updated_at"], str)
        self.assertEqual(
            obj_dict["created_at"], my_model.created_at.isoformat())
        self.assertEqual(
            obj_dict["updated_at"], my_model.updated_at.isoformat())

    def test_to_dict_contains_added_attributes(self):
        """to_dict() should include dynamically added attributes."""
        my_model = BaseModel()
        my_model.name = "My_First_Model"
        my_model.my_number = 89
        obj_dict = my_model.to_dict()
        self.assertEqual(obj_dict["name"], "My_First_Model")
        self.assertEqual(obj_dict["my_number"], 89)


if __name__ == "__main__":
    unittest.main()
