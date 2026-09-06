#!/usr/bin/python3
"""Unit tests for the HBNB command interpreter."""
import os
import unittest
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models import storage
from models.engine.file_storage import FileStorage


class TestHBNBCommandBasics(unittest.TestCase):
    """Unit tests for quit, EOF, emptyline, and help."""

    def test_quit_exits(self):
        """quit should return True to end the cmdloop."""
        with patch("sys.stdout", new=StringIO()):
            self.assertTrue(HBNBCommand().onecmd("quit"))

    def test_EOF_exits(self):
        """EOF should return True and print a newline."""
        with patch("sys.stdout", new=StringIO()) as out:
            self.assertTrue(HBNBCommand().onecmd("EOF"))
            self.assertEqual(out.getvalue(), "\n")

    def test_emptyline_does_nothing(self):
        """An empty line should print nothing."""
        with patch("sys.stdout", new=StringIO()) as out:
            HBNBCommand().onecmd("")
            self.assertEqual(out.getvalue(), "")

    def test_help_runs_without_error(self):
        """help should list commands without raising."""
        with patch("sys.stdout", new=StringIO()) as out:
            HBNBCommand().onecmd("help")
            self.assertIn("Documented commands", out.getvalue())


class TestHBNBCommandCRUD(unittest.TestCase):
    """Unit tests for create, show, destroy, all, count, update."""

    def setUp(self):
        """Reset storage before each test."""
        FileStorage._FileStorage__objects = {}
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def tearDown(self):
        """Clean up any file created during a test."""
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def _create(self, cls_name):
        """Helper: create an instance and return its id."""
        with patch("sys.stdout", new=StringIO()) as out:
            HBNBCommand().onecmd("create {}".format(cls_name))
            return out.getvalue().strip()

    def test_create_missing_class(self):
        """create with no class name should report the error."""
        with patch("sys.stdout", new=StringIO()) as out:
            HBNBCommand().onecmd("create")
            self.assertEqual(out.getvalue(), "** class name missing **\n")

    def test_create_invalid_class(self):
        """create with an unknown class should report the error."""
        with patch("sys.stdout", new=StringIO()) as out:
            HBNBCommand().onecmd("create MyModel")
            self.assertEqual(
                out.getvalue(), "** class doesn't exist **\n")

    def test_create_persists_instance(self):
        """create should print an id that shows up in storage.all()."""
        obj_id = self._create("BaseModel")
        key = "BaseModel.{}".format(obj_id)
        self.assertIn(key, storage.all())

    def test_show_missing_class(self):
        """show with no arguments should report the error."""
        with patch("sys.stdout", new=StringIO()) as out:
            HBNBCommand().onecmd("show")
            self.assertEqual(out.getvalue(), "** class name missing **\n")

    def test_show_missing_id(self):
        """show with a class but no id should report the error."""
        with patch("sys.stdout", new=StringIO()) as out:
            HBNBCommand().onecmd("show BaseModel")
            self.assertEqual(
                out.getvalue(), "** instance id missing **\n")

    def test_show_no_instance_found(self):
        """show with a bogus id should report the error."""
        with patch("sys.stdout", new=StringIO()) as out:
            HBNBCommand().onecmd("show BaseModel 12345")
            self.assertEqual(
                out.getvalue(), "** no instance found **\n")

    def test_show_valid_instance(self):
        """show should print the instance's string representation."""
        obj_id = self._create("User")
        with patch("sys.stdout", new=StringIO()) as out:
            HBNBCommand().onecmd("show User {}".format(obj_id))
            self.assertIn(obj_id, out.getvalue())
            self.assertIn("[User]", out.getvalue())

    def test_destroy_removes_instance(self):
        """destroy should remove the instance from storage."""
        obj_id = self._create("User")
        key = "User.{}".format(obj_id)
        with patch("sys.stdout", new=StringIO()):
            HBNBCommand().onecmd("destroy User {}".format(obj_id))
        self.assertNotIn(key, storage.all())

    def test_destroy_no_instance_found(self):
        """destroy with a bogus id should report the error."""
        with patch("sys.stdout", new=StringIO()) as out:
            HBNBCommand().onecmd("destroy User 12345")
            self.assertEqual(
                out.getvalue(), "** no instance found **\n")

    def test_all_with_no_objects(self):
        """all with nothing created should print an empty list."""
        with patch("sys.stdout", new=StringIO()) as out:
            HBNBCommand().onecmd("all")
            self.assertEqual(out.getvalue().strip(), "[]")

    def test_all_filters_by_class(self):
        """all <class> should only include that class's instances."""
        self._create("User")
        self._create("State")
        with patch("sys.stdout", new=StringIO()) as out:
            HBNBCommand().onecmd("all State")
            result = out.getvalue()
            self.assertIn("[State]", result)
            self.assertNotIn("[User]", result)

    def test_all_invalid_class(self):
        """all with an unknown class should report the error."""
        with patch("sys.stdout", new=StringIO()) as out:
            HBNBCommand().onecmd("all MyModel")
            self.assertEqual(
                out.getvalue(), "** class doesn't exist **\n")

    def test_count(self):
        """count should report the number of instances of a class."""
        self._create("Amenity")
        self._create("Amenity")
        with patch("sys.stdout", new=StringIO()) as out:
            HBNBCommand().onecmd("count Amenity")
            self.assertEqual(out.getvalue().strip(), "2")

    def test_update_sets_attribute(self):
        """update should set and persist a new attribute value."""
        obj_id = self._create("State")
        with patch("sys.stdout", new=StringIO()):
            HBNBCommand().onecmd(
                'update State {} name "California"'.format(obj_id))
        obj = storage.all()["State.{}".format(obj_id)]
        self.assertEqual(obj.name, "California")

    def test_update_missing_value(self):
        """update with no value should report the error."""
        obj_id = self._create("State")
        with patch("sys.stdout", new=StringIO()) as out:
            HBNBCommand().onecmd("update State {} name".format(obj_id))
            self.assertEqual(out.getvalue(), "** value missing **\n")


class TestHBNBCommandDotSyntax(unittest.TestCase):
    """Unit tests for <class>.<command>(<args>) syntax."""

    def setUp(self):
        """Reset storage before each test."""
        FileStorage._FileStorage__objects = {}
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def tearDown(self):
        """Clean up any file created during a test."""
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def _create(self, cls_name):
        """Helper: create an instance and return its id."""
        with patch("sys.stdout", new=StringIO()) as out:
            HBNBCommand().onecmd("create {}".format(cls_name))
            return out.getvalue().strip()

    def test_all_dot_syntax(self):
        """User.all() should behave like all User."""
        self._create("User")
        with patch("sys.stdout", new=StringIO()) as out:
            HBNBCommand().onecmd("User.all()")
            self.assertIn("[User]", out.getvalue())

    def test_count_dot_syntax(self):
        """User.count() should behave like count User."""
        self._create("User")
        with patch("sys.stdout", new=StringIO()) as out:
            HBNBCommand().onecmd("User.count()")
            self.assertEqual(out.getvalue().strip(), "1")

    def test_show_dot_syntax(self):
        """User.show(id) should behave like show User id."""
        obj_id = self._create("User")
        with patch("sys.stdout", new=StringIO()) as out:
            HBNBCommand().onecmd('User.show("{}")'.format(obj_id))
            self.assertIn(obj_id, out.getvalue())

    def test_destroy_dot_syntax(self):
        """User.destroy(id) should behave like destroy User id."""
        obj_id = self._create("User")
        with patch("sys.stdout", new=StringIO()):
            HBNBCommand().onecmd('User.destroy("{}")'.format(obj_id))
        self.assertNotIn("User.{}".format(obj_id), storage.all())

    def test_update_dot_syntax_attr_value(self):
        """User.update(id, attr, value) should set the attribute."""
        obj_id = self._create("User")
        with patch("sys.stdout", new=StringIO()):
            HBNBCommand().onecmd(
                'User.update("{}", "first_name", "Betty")'.format(obj_id))
        obj = storage.all()["User.{}".format(obj_id)]
        self.assertEqual(obj.first_name, "Betty")

    def test_update_dot_syntax_dict(self):
        """User.update(id, {dict}) should set every key in the dict."""
        obj_id = self._create("User")
        with patch("sys.stdout", new=StringIO()):
            HBNBCommand().onecmd(
                'User.update("{}", '.format(obj_id) +
                '{"first_name": "Betty", "age": 25})')
        obj = storage.all()["User.{}".format(obj_id)]
        self.assertEqual(obj.first_name, "Betty")
        self.assertEqual(obj.age, 25)

    def test_unknown_dot_command(self):
        """An unrecognized dot-command should print the syntax error."""
        with patch("sys.stdout", new=StringIO()) as out:
            HBNBCommand().onecmd("User.frobnicate()")
            self.assertIn("Unknown syntax", out.getvalue())


if __name__ == "__main__":
    unittest.main()
