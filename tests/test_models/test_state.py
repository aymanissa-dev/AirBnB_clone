#!/usr/bin/python3
"""Unit tests for the State class."""
import unittest
from models.base_model import BaseModel
from models.state import State


class TestState(unittest.TestCase):
    """Unit tests for the State class."""

    def test_is_subclass_of_base_model(self):
        """State should inherit from BaseModel."""
        self.assertIsInstance(State(), BaseModel)

    def test_default_name_attribute(self):
        """name should default to an empty string."""
        state = State()
        self.assertEqual(state.name, "")
        self.assertIsInstance(state.name, str)

    def test_instance_attribute_overrides_class_attribute(self):
        """Setting name on one instance shouldn't affect another."""
        state1 = State()
        state2 = State()
        state1.name = "California"
        self.assertEqual(state2.name, "")

    def test_to_dict_contains_set_name(self):
        """to_dict() should reflect the name set on the instance."""
        state = State()
        state.name = "California"
        obj_dict = state.to_dict()
        self.assertEqual(obj_dict["name"], "California")
        self.assertEqual(obj_dict["__class__"], "State")

    def test_from_dict_round_trip(self):
        """A State rebuilt from to_dict() should match the original."""
        state = State()
        state.name = "Nevada"
        new_state = State(**state.to_dict())
        self.assertEqual(new_state.name, state.name)
        self.assertEqual(new_state.id, state.id)


if __name__ == "__main__":
    unittest.main()
