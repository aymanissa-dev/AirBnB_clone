#!/usr/bin/python3
"""Defines the Review class."""
from models.base_model import BaseModel


class Review(BaseModel):
    """Represents a review left on a place.

    Public class attributes:
        place_id (str): the id of the Place being reviewed.
        user_id (str): the id of the User who wrote the review.
        text (str): the review's content.
    """

    place_id = ""
    user_id = ""
    text = ""
