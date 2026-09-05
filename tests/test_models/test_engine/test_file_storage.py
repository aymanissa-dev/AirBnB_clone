#!/usr/bin/python3
"""Unit tests for the FileStorage class."""
import json
import os
import unittest
from models import storage
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    """Unit tests for the FileStorage class."""

    def setUp(self):
        """Reset __objects and clear any leftover file.json."""
        FileStorage._FileStorage__objects = {}
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def tearDown(self):
        """Clean up any file.json created during a test."""
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_all_returns_dict(self):
        """all() should return a dictionary."""
        self.assertIsInstance(storage.all(), dict)

    def test_new_adds_object_with_correct_key(self):
        """new() should key the object as <ClassName>.<id>."""
        my_model = BaseModel()
        storage.new(my_model)
        key = "BaseModel.{}".format(my_model.id)
        self.assertIn(key, storage.all())
        self.assertIs(storage.all()[key], my_model)

    def test_save_creates_file(self):
        """save() should write __objects to the JSON file."""
        BaseModel()
        storage.save()
        self.assertTrue(
            os.path.exists(FileStorage._FileStorage__file_path))

    def test_save_writes_valid_json(self):
        """The saved file should contain valid, matching JSON."""
        my_model = BaseModel()
        my_model.name = "My_First_Model"
        storage.save()
        with open(FileStorage._FileStorage__file_path, "r") as f:
            data = json.load(f)
        key = "BaseModel.{}".format(my_model.id)
        self.assertIn(key, data)
        self.assertEqual(data[key]["name"], "My_First_Model")

    def test_reload_with_no_file_does_nothing(self):
        """reload() should not raise if the JSON file doesn't exist."""
        try:
            storage.reload()
        except Exception as exc:
            self.fail("reload() raised {} unexpectedly".format(exc))

    def test_reload_restores_objects(self):
        """reload() should recreate objects saved to the JSON file."""
        my_model = BaseModel()
        my_model.name = "My_First_Model"
        key = "BaseModel.{}".format(my_model.id)
        storage.save()

        FileStorage._FileStorage__objects = {}
        storage.reload()

        reloaded = storage.all()
        self.assertIn(key, reloaded)
        self.assertIsInstance(reloaded[key], BaseModel)
        self.assertEqual(reloaded[key].id, my_model.id)
        self.assertEqual(reloaded[key].name, "My_First_Model")

    def test_base_model_save_persists_to_storage(self):
        """BaseModel.save() should trigger FileStorage.save()."""
        my_model = BaseModel()
        my_model.save()
        with open(FileStorage._FileStorage__file_path, "r") as f:
            data = json.load(f)
        key = "BaseModel.{}".format(my_model.id)
        self.assertIn(key, data)


if __name__ == "__main__":
    unittest.main()
