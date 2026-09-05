#!/usr/bin/python3
"""Defines the Amenity class."""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """Represents an amenity.

    Public class attributes:
        name (str): the name of the amenity.
    """

    name = ""
