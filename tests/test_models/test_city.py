#!/usr/bin/python3
"""Unit tests for the City class."""
import unittest
from models.base_model import BaseModel
from models.city import City


class TestCity(unittest.TestCase):
    """Unit tests for the City class."""

    def test_is_subclass_of_base_model(self):
        """City should inherit from BaseModel."""
        self.assertIsInstance(City(), BaseModel)

    def test_default_attributes(self):
        """state_id and name should default to empty strings."""
        city = City()
        self.assertEqual(city.state_id, "")
        self.assertEqual(city.name, "")
        self.assertIsInstance(city.state_id, str)
        self.assertIsInstance(city.name, str)

    def test_instance_attribute_overrides_class_attribute(self):
        """Setting name on one instance shouldn't affect another."""
        city1 = City()
        city2 = City()
        city1.name = "San Francisco"
        self.assertEqual(city2.name, "")

    def test_to_dict_contains_set_attributes(self):
        """to_dict() should reflect attributes set on the instance."""
        city = City()
        city.state_id = "CA"
        city.name = "San Francisco"
        obj_dict = city.to_dict()
        self.assertEqual(obj_dict["state_id"], "CA")
        self.assertEqual(obj_dict["name"], "San Francisco")
        self.assertEqual(obj_dict["__class__"], "City")

    def test_from_dict_round_trip(self):
        """A City rebuilt from to_dict() should match the original."""
        city = City()
        city.state_id = "CA"
        city.name = "San Francisco"
        new_city = City(**city.to_dict())
        self.assertEqual(new_city.state_id, city.state_id)
        self.assertEqual(new_city.name, city.name)
        self.assertEqual(new_city.id, city.id)


if __name__ == "__main__":
    unittest.main()
