#!/usr/bin/python3
"""Unit tests for the models package's storage singleton."""
import unittest
from models import storage
from models.engine.file_storage import FileStorage


class TestModelsInit(unittest.TestCase):
    """Unit tests verifying models/__init__.py wiring."""

    def test_storage_is_file_storage_instance(self):
        """storage should be an instance of FileStorage."""
        self.assertIsInstance(storage, FileStorage)

    def test_storage_is_a_singleton(self):
        """Re-importing models should yield the same storage object."""
        from models import storage as storage_again
        self.assertIs(storage, storage_again)

    def test_all_returns_a_dict_on_import(self):
        """storage.all() should already be a dict right after import."""
        self.assertIsInstance(storage.all(), dict)


if __name__ == "__main__":
    unittest.main()
