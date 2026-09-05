#!/usr/bin/python3
"""Defines the State class."""
from models.base_model import BaseModel


class State(BaseModel):
    """Represents a state.

    Public class attributes:
        name (str): the name of the state.
    """

    name = ""
