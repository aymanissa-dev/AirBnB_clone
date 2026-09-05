#!/usr/bin/python3
"""Unit tests for the Review class."""
import unittest
from models.base_model import BaseModel
from models.review import Review


class TestReview(unittest.TestCase):
    """Unit tests for the Review class."""

    def test_is_subclass_of_base_model(self):
        """Review should inherit from BaseModel."""
        self.assertIsInstance(Review(), BaseModel)

    def test_default_attributes(self):
        """place_id, user_id, text should default to ''."""
        review = Review()
        self.assertEqual(review.place_id, "")
        self.assertEqual(review.user_id, "")
        self.assertEqual(review.text, "")
        self.assertIsInstance(review.text, str)

    def test_instance_attribute_overrides_class_attribute(self):
        """Setting text on one instance shouldn't affect another."""
        review1 = Review()
        review2 = Review()
        review1.text = "Great stay!"
        self.assertEqual(review2.text, "")

    def test_to_dict_contains_set_attributes(self):
        """to_dict() should reflect attributes set on the instance."""
        review = Review()
        review.place_id = "123"
        review.text = "Great stay!"
        obj_dict = review.to_dict()
        self.assertEqual(obj_dict["place_id"], "123")
        self.assertEqual(obj_dict["text"], "Great stay!")
        self.assertEqual(obj_dict["__class__"], "Review")

    def test_from_dict_round_trip(self):
        """A Review rebuilt from to_dict() should match the original."""
        review = Review()
        review.text = "Great stay!"
        new_review = Review(**review.to_dict())
        self.assertEqual(new_review.text, review.text)
        self.assertEqual(new_review.id, review.id)


if __name__ == "__main__":
    unittest.main()
