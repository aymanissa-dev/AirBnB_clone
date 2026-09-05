#!/usr/bin/python3
"""Defines the FileStorage class, a JSON-file storage engine."""
import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.state import State
from models.user import User


class FileStorage:
    """Serializes instances to a JSON file and deserializes them back.

    Private class attributes:
        __file_path: path to the JSON file used for storage.
        __objects: dictionary of all stored objects, keyed by
            <class name>.<id>.
    """

    __file_path = "file.json"
    __objects = {}

    # Maps a class name (as stored in __class__) to the actual class,
    # so reload() can reconstruct the right type of object.
    __classes = {
        "Amenity": Amenity,
        "BaseModel": BaseModel,
        "City": City,
        "Place": Place,
        "State": State,
        "User": User,
    }

    def all(self):
        """Return the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Set in __objects the obj with key <obj class name>.id."""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serialize __objects to the JSON file (__file_path)."""
        serialized = {
            key: obj.to_dict() for key, obj in FileStorage.__objects.items()
        }
        with open(FileStorage.__file_path, "w") as f:
            json.dump(serialized, f)

    def reload(self):
        """Deserialize the JSON file to __objects, if it exists.

        If the file doesn't exist, do nothing (no exception raised).
        """
        try:
            with open(FileStorage.__file_path, "r") as f:
                obj_dicts = json.load(f)
        except FileNotFoundError:
            return
        for key, obj_dict in obj_dicts.items():
            cls_name = obj_dict["__class__"]
            cls = FileStorage.__classes[cls_name]
            FileStorage.__objects[key] = cls(**obj_dict)
