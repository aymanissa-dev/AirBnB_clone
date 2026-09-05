#!/usr/bin/python3
"""Defines the BaseModel class, the parent of all other model classes."""
import uuid
from datetime import datetime


class BaseModel:
    """Represents the base class for all models in the application.

    Defines the common attributes/methods shared by every model:
    a unique id, creation/update timestamps, and (de)serialization
    helpers.
    """

    def __init__(self):
        """Initialize a new BaseModel instance.

        Sets a unique id and the created_at/updated_at timestamps to
        the current datetime.
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __str__(self):
        """Return the string representation of the instance.

        Format: [<class name>] (<self.id>) <self.__dict__>
        """
        return "[{}] ({}) {}".format(
            type(self).__name__, self.id, self.__dict__)

    def save(self):
        """Update updated_at with the current datetime."""
        self.updated_at = datetime.now()

    def to_dict(self):
        """Return a dictionary representation of the instance.

        Includes all keys/values of __dict__, adds a __class__ key
        set to the class name, and converts created_at/updated_at
        to ISO format strings.
        """
        obj_dict = self.__dict__.copy()
        obj_dict["__class__"] = type(self).__name__
        obj_dict["created_at"] = self.created_at.isoformat()
        obj_dict["updated_at"] = self.updated_at.isoformat()
        return obj_dict
