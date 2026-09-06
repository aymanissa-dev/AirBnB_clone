#!/usr/bin/python3
"""Defines the HBNB command interpreter."""
import ast
import cmd
import shlex
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class HBNBCommand(cmd.Cmd):
    """Command interpreter for the AirBnB clone project."""

    prompt = "(hbnb) "

    __classes = {
        "Amenity": Amenity,
        "BaseModel": BaseModel,
        "City": City,
        "Place": Place,
        "Review": Review,
        "State": State,
        "User": User,
    }

    def emptyline(self):
        """Do nothing on an empty input line."""
        pass

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def _parse_args(self, arg):
        """Split arg respecting quotes; return [] on malformed input."""
        try:
            return shlex.split(arg)
        except ValueError:
            return []

    def do_create(self, arg):
        """Create a new instance of a class, save it, print its id.

        Usage: create <class name>
        """
        args = self._parse_args(arg)
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        new_instance = HBNBCommand.__classes[args[0]]()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """Print the string representation of an instance.

        Usage: show <class name> <id>
        """
        args = self._parse_args(arg)
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        obj = storage.all().get(key)
        if obj is None:
            print("** no instance found **")
            return
        print(obj)

    def do_destroy(self, arg):
        """Delete an instance based on the class name and id.

        Usage: destroy <class name> <id>
        """
        args = self._parse_args(arg)
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        if key not in storage.all():
            print("** no instance found **")
            return
        del storage.all()[key]
        storage.save()

    def do_all(self, arg):
        """Print all string representations of instances.

        Usage: all [<class name>]
        """
        args = self._parse_args(arg)
        objs = storage.all()
        if len(args) == 0:
            print([str(obj) for obj in objs.values()])
            return
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        print([str(obj) for key, obj in objs.items()
               if key.split(".")[0] == args[0]])

    def do_count(self, arg):
        """Print the number of instances of a class.

        Usage: count <class name>
        """
        args = self._parse_args(arg)
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        count = sum(1 for key in storage.all()
                    if key.split(".")[0] == args[0])
        print(count)

    def do_update(self, arg):
        """Update an instance attribute value and save the change.

        Usage: update <class name> <id> <attribute name> "<value>"
        """
        args = self._parse_args(arg)
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        obj = storage.all().get(key)
        if obj is None:
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        attr_name = args[2]
        attr_value = args[3]
        if hasattr(obj, attr_name):
            attr_type = type(getattr(obj, attr_name))
            try:
                attr_value = attr_type(attr_value)
            except (TypeError, ValueError):
                pass
        setattr(obj, attr_name, attr_value)
        obj.save()

    def default(self, line):
        """Handle <class name>.<command>(<args>) syntax."""
        try:
            cls_name, rest = line.split(".", 1)
            command, args_str = rest.split("(", 1)
            args_str = args_str.rstrip(")")
        except ValueError:
            print("*** Unknown syntax: {}".format(line))
            return

        handlers = {
            "all": lambda: self.do_all(cls_name),
            "count": lambda: self.do_count(cls_name),
            "show": lambda: self.do_show(
                "{} {}".format(cls_name, self._strip_quotes(args_str))),
            "destroy": lambda: self.do_destroy(
                "{} {}".format(cls_name, self._strip_quotes(args_str))),
            "update": lambda: self._default_update(cls_name, args_str),
        }
        handler = handlers.get(command)
        if handler is None:
            print("*** Unknown syntax: {}".format(line))
            return
        handler()

    @staticmethod
    def _strip_quotes(value):
        """Strip a single layer of matching quotes from value."""
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            return value[1:-1]
        return value

    def _default_update(self, cls_name, args_str):
        """Handle <class>.update(id, attr, value) or (id, {dict})."""
        parts = args_str.split(",", 1)
        obj_id = self._strip_quotes(parts[0])
        if obj_id == "":
            print("** instance id missing **")
            return
        if len(parts) < 2:
            self.do_update("{} {}".format(cls_name, obj_id))
            return
        remainder = parts[1].strip()
        if remainder.startswith("{") and remainder.endswith("}"):
            self._update_from_dict(cls_name, obj_id, remainder)
        else:
            attr_parts = [self._strip_quotes(p)
                          for p in remainder.split(",")]
            attr_name = attr_parts[0] if len(attr_parts) > 0 else ""
            attr_value = attr_parts[1] if len(attr_parts) > 1 else ""
            self.do_update('{} {} {} "{}"'.format(
                cls_name, obj_id, attr_name, attr_value))

    def _update_from_dict(self, cls_name, obj_id, dict_literal):
        """Apply every key/value in dict_literal to the target object."""
        try:
            attr_dict = ast.literal_eval(dict_literal)
        except (ValueError, SyntaxError):
            print("*** Unknown syntax: bad dictionary")
            return
        key = "{}.{}".format(cls_name, obj_id)
        obj = storage.all().get(key)
        if obj is None:
            print("** no instance found **")
            return
        for attr_name, attr_value in attr_dict.items():
            setattr(obj, attr_name, attr_value)
        obj.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
