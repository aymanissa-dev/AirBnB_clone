#!/usr/bin/python3
"""Defines the City class."""
from models.base_model import BaseModel


class City(BaseModel):
    """Represents a city.

    Public class attributes:
        state_id (str): the id of the State this city belongs to.
        name (str): the name of the city.
    """

    state_id = ""
    name = ""
