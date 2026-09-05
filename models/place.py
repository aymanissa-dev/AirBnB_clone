#!/usr/bin/python3
"""Defines the Place class."""
from models.base_model import BaseModel


class Place(BaseModel):
    """Represents a place to stay.

    Public class attributes:
        city_id (str): the id of the City this place is in.
        user_id (str): the id of the User who owns this place.
        name (str): the name of the place.
        description (str): a description of the place.
        number_rooms (int): number of rooms.
        number_bathrooms (int): number of bathrooms.
        max_guest (int): maximum number of guests.
        price_by_night (int): price per night.
        latitude (float): latitude coordinate.
        longitude (float): longitude coordinate.
        amenity_ids (list): list of Amenity ids for this place.
    """

    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
