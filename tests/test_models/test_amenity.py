#!/usr/bin/python3
"""Unit tests for the Amenity class."""
import unittest
from models.base_model import BaseModel
from models.amenity import Amenity


class TestAmenity(unittest.TestCase):
    """Unit tests for the Amenity class."""

    def test_is_subclass_of_base_model(self):
        """Amenity should inherit from BaseModel."""
        self.assertIsInstance(Amenity(), BaseModel)

    def test_default_name_attribute(self):
        """name should default to an empty string."""
        amenity = Amenity()
        self.assertEqual(amenity.name, "")
        self.assertIsInstance(amenity.name, str)

    def test_instance_attribute_overrides_class_attribute(self):
        """Setting name on one instance shouldn't affect another."""
        amenity1 = Amenity()
        amenity2 = Amenity()
        amenity1.name = "Wifi"
        self.assertEqual(amenity2.name, "")

    def test_to_dict_contains_set_name(self):
        """to_dict() should reflect the name set on the instance."""
        amenity = Amenity()
        amenity.name = "Wifi"
        obj_dict = amenity.to_dict()
        self.assertEqual(obj_dict["name"], "Wifi")
        self.assertEqual(obj_dict["__class__"], "Amenity")

    def test_from_dict_round_trip(self):
        """An Amenity rebuilt from to_dict() should match the original."""
        amenity = Amenity()
        amenity.name = "Pool"
        new_amenity = Amenity(**amenity.to_dict())
        self.assertEqual(new_amenity.name, amenity.name)
        self.assertEqual(new_amenity.id, amenity.id)


if __name__ == "__main__":
    unittest.main()
