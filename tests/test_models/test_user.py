#!/usr/bin/python3
"""Unit tests for the User class."""
import unittest
from models.base_model import BaseModel
from models.user import User


class TestUser(unittest.TestCase):
    """Unit tests for the User class."""

    def test_is_subclass_of_base_model(self):
        """User should inherit from BaseModel."""
        self.assertIsInstance(User(), BaseModel)

    def test_default_class_attributes(self):
        """email, password, first_name, last_name default to ''."""
        user = User()
        self.assertEqual(user.email, "")
        self.assertEqual(user.password, "")
        self.assertEqual(user.first_name, "")
        self.assertEqual(user.last_name, "")

    def test_attributes_are_strings(self):
        """The default attribute values should be strings."""
        user = User()
        self.assertIsInstance(user.email, str)
        self.assertIsInstance(user.password, str)
        self.assertIsInstance(user.first_name, str)
        self.assertIsInstance(user.last_name, str)

    def test_instance_attribute_overrides_class_attribute(self):
        """Setting an attribute on an instance shouldn't affect others."""
        user1 = User()
        user2 = User()
        user1.first_name = "Betty"
        self.assertEqual(user2.first_name, "")

    def test_to_dict_contains_set_attributes(self):
        """to_dict() should reflect attributes set on the instance."""
        user = User()
        user.email = "betty@holberton.com"
        user.first_name = "Betty"
        obj_dict = user.to_dict()
        self.assertEqual(obj_dict["email"], "betty@holberton.com")
        self.assertEqual(obj_dict["first_name"], "Betty")
        self.assertEqual(obj_dict["__class__"], "User")

    def test_from_dict_round_trip(self):
        """A User rebuilt from to_dict() should match the original."""
        user = User()
        user.email = "betty@holberton.com"
        user.password = "root"
        new_user = User(**user.to_dict())
        self.assertEqual(new_user.email, user.email)
        self.assertEqual(new_user.password, user.password)
        self.assertEqual(new_user.id, user.id)


if __name__ == "__main__":
    unittest.main()
