#!/usr/bin/python3
"""Defines the BaseModel class, the parent of all other model classes."""
import uuid
from datetime import datetime

import models


class BaseModel:
    """Represents the base class for all models in the application.

    Defines the common attributes/methods shared by every model:
    a unique id, creation/update timestamps, and (de)serialization
    helpers.
    """

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel instance.

        Args:
            *args: unused.
            **kwargs: if not empty, each key/value pair is set as an
                instance attribute. created_at and updated_at, given
                as ISO format strings, are converted back into
                datetime objects. __class__ is ignored since it is
                not a real attribute. If kwargs is empty, a brand
                new instance is created: a unique id is generated and
                created_at/updated_at are set to the current
                datetime.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                if key in ("created_at", "updated_at"):
                    value = datetime.strptime(
                        value, "%Y-%m-%dT%H:%M:%S.%f")
                setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """Return the string representation of the instance.

        Format: [<class name>] (<self.id>) <self.__dict__>
        """
        return "[{}] ({}) {}".format(
            type(self).__name__, self.id, self.__dict__)

    def save(self):
        """Update updated_at with the current datetime and persist."""
        self.updated_at = datetime.now()
        models.storage.save()

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
