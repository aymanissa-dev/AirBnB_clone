#!/usr/bin/python3
"""Defines the User class."""
from models.base_model import BaseModel


class User(BaseModel):
    """Represents a user of the application.

    Public class attributes:
        email (str): the user's email address.
        password (str): the user's password.
        first_name (str): the user's first name.
        last_name (str): the user's last name.
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
