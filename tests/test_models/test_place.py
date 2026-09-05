#!/usr/bin/python3
"""Unit tests for the Place class."""
import unittest
from models.base_model import BaseModel
from models.place import Place


class TestPlace(unittest.TestCase):
    """Unit tests for the Place class."""

    def test_is_subclass_of_base_model(self):
        """Place should inherit from BaseModel."""
        self.assertIsInstance(Place(), BaseModel)

    def test_default_string_attributes(self):
        """city_id, user_id, name, description default to ''."""
        place = Place()
        self.assertEqual(place.city_id, "")
        self.assertEqual(place.user_id, "")
        self.assertEqual(place.name, "")
        self.assertEqual(place.description, "")

    def test_default_int_attributes(self):
        """Numeric room/guest/price attributes default to 0."""
        place = Place()
        self.assertEqual(place.number_rooms, 0)
        self.assertEqual(place.number_bathrooms, 0)
        self.assertEqual(place.max_guest, 0)
        self.assertEqual(place.price_by_night, 0)
        self.assertIsInstance(place.number_rooms, int)

    def test_default_float_attributes(self):
        """latitude and longitude default to 0.0."""
        place = Place()
        self.assertEqual(place.latitude, 0.0)
        self.assertEqual(place.longitude, 0.0)
        self.assertIsInstance(place.latitude, float)
        self.assertIsInstance(place.longitude, float)

    def test_default_amenity_ids_is_empty_list(self):
        """amenity_ids should default to an empty list."""
        place = Place()
        self.assertEqual(place.amenity_ids, [])
        self.assertIsInstance(place.amenity_ids, list)

    def test_instance_attribute_overrides_class_attribute(self):
        """Setting name on one instance shouldn't affect another."""
        place1 = Place()
        place2 = Place()
        place1.name = "Cozy Loft"
        self.assertEqual(place2.name, "")

    def test_to_dict_contains_set_attributes(self):
        """to_dict() should reflect attributes set on the instance."""
        place = Place()
        place.name = "Cozy Loft"
        place.number_rooms = 2
        place.latitude = 37.7749
        obj_dict = place.to_dict()
        self.assertEqual(obj_dict["name"], "Cozy Loft")
        self.assertEqual(obj_dict["number_rooms"], 2)
        self.assertEqual(obj_dict["latitude"], 37.7749)
        self.assertEqual(obj_dict["__class__"], "Place")

    def test_from_dict_round_trip(self):
        """A Place rebuilt from to_dict() should match the original."""
        place = Place()
        place.name = "Cozy Loft"
        place.number_rooms = 2
        new_place = Place(**place.to_dict())
        self.assertEqual(new_place.name, place.name)
        self.assertEqual(new_place.number_rooms, place.number_rooms)
        self.assertEqual(new_place.id, place.id)


if __name__ == "__main__":
    unittest.main()
