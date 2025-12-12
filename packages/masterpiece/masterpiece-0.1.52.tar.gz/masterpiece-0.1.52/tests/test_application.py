"""
Author: Juha Meskanen
Date: 2024-10-26
"""

import argparse
from io import IOBase
import sys
import tempfile
import os
from typing import Type, Optional
import unittest
from unittest.mock import MagicMock, mock_open, patch
from masterpiece.format import Format
from masterpiece.jsonformat import JsonFormat
from masterpiece.masterpiece import MasterPiece, classproperty
from masterpiece.composite import Composite
from masterpiece.application import Application
from masterpiece.plugmaster import PlugMaster


# Define a mock format class with necessary attributes
class MockFormat(Format):
    file_ext = ".json"

    def __init__(self, file: IOBase) -> None:
        pass

    def serialize(self, obj: MasterPiece) -> None:
        pass

    def deserialize(self, obj: MasterPiece) -> None:
        pass

    def load_configuration(self, clazz: Type[MasterPiece]) -> None:
        pass

    def save_configuration(self, clazz: Type[MasterPiece]) -> None:
        pass

    @classproperty  # type: ignore
    def file_extension(cls) -> str:
        return cls.file_ext


class TestApplication(unittest.TestCase):
    """Unit tests for `Application` class."""

    def setUp(self) -> None:
        """Set up each test with a unique temporary directory."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.app_name = "test_app"
        self.app = Application(name=self.app_name)
        self.app.serialization_file = "test_file.json"
        self.app.serialization_format = "json"

    def tearDown(self) -> None:
        """Clean up temporary directory after each test."""
        self.temp_dir.cleanup()

    @patch("builtins.open", new_callable=mock_open)
    @patch("masterpiece.masterpiece.MasterPiece.factory")
    @patch.object(Application, "warning", new_callable=MagicMock)
    def test_deserialize_file_not_specified(
        self, mock_warning: MagicMock, mock_factory: MagicMock, mock_open: MagicMock
    ) -> None:
        """Test deserialization when no file is specified."""
        self.app.serialization_file = ""
        self.app.serialization_format = ""

        self.app.deserialize()

        mock_warning.assert_called_with(
            "No deserialization this time, --serialization_file not specified"
        )

    @patch("builtins.open", new_callable=mock_open)
    @patch("masterpiece.masterpiece.MasterPiece.factory")
    def test_deserialize_invalid_format(
        self, mock_factory: MagicMock, mock_open: MagicMock
    ) -> None:
        """Test deserialization with an invalid format."""
        mock_factory.return_value = {"invalid_format": MagicMock()}
        self.app.serialization_format = "invalid_format"

        with self.assertRaises(TypeError):
            self.app.deserialize()

    @patch("builtins.open", new_callable=mock_open)
    @patch("masterpiece.masterpiece.MasterPiece.factory")
    @patch.object(Application, "warning", new_callable=MagicMock)
    @patch.object(MockFormat, "deserialize", new_callable=MagicMock)
    @patch.object(Application, "info", new_callable=MagicMock)
    def test_deserialize_success(
        self,
        mock_info: MagicMock,
        mock_deserialize: MagicMock,
        mock_warning: MagicMock,
        mock_factory: MagicMock,
        mock_open: MagicMock,
    ) -> None:
        """Test successful deserialization."""
        # Set the factory to return the MockFormat class itself, not an instance
        mock_factory.return_value = {"json": MockFormat}

        # Call the deserialize method on the application
        self.app.deserialize()

        # Assert that the factory was called
        mock_factory.assert_called_once()

        # Assert that deserialize was called on the MockFormat instance created in the application
        mock_deserialize.assert_called_once_with(self.app)

        # Assert that the info log was called with the correct message
        mock_info.assert_called_with(
            f"File {self.app.serialization_file} successfully read"
        )

    @patch("builtins.open", new_callable=mock_open)
    @patch("masterpiece.masterpiece.MasterPiece.factory")
    @patch.object(Application, "warning", new_callable=MagicMock)
    def test_serialize_file_not_specified(
        self, mock_warning: MagicMock, mock_factory: MagicMock, mock_open: MagicMock
    ) -> None:
        """Test serialization when no file is specified."""
        self.app.serialization_file = ""

        self.app.serialize()

        mock_warning.assert_called_with(
            "No serialization this time, --serialization_file not set"
        )

    @patch("builtins.open", new_callable=mock_open)
    @patch("masterpiece.masterpiece.MasterPiece.factory")
    def test_serialize_invalid_format(
        self, mock_factory: MagicMock, mock_open: MagicMock
    ) -> None:
        """Test serialization with an invalid format."""
        mock_factory.return_value = {"invalid_format": MagicMock()}
        self.app.serialization_format = "invalid_format"

        with self.assertRaises(TypeError):
            self.app.serialize()

    def test_get_classid(self) -> None:
        """Assert that the meta-class driven class initialization works."""
        classid = Application.get_class_id()
        self.assertEqual("Application", classid)

    def test_serialization(self) -> None:
        """Test serialization with unique temp files."""
        application = Application("testapp")
        composite = Composite("mycomposite")
        child1 = MasterPiece("child1")
        composite.add(child1)
        application.add(composite)

        # Unique filename within the temporary directory
        filename = os.path.join(self.temp_dir.name, "application.json")

        # Serialize and deserialize using isolated file
        with open(filename, "w", encoding="utf-8") as f:
            json_format = JsonFormat(f)
            json_format.serialize(application)

        application2 = Application("bar")
        with open(filename, "r", encoding="utf-8") as f:
            json_format = JsonFormat(f)
            json_format.deserialize(application2)

        self.assertEqual("testapp", application2.name)
        self.assertEqual(1, len(application2.children))

    def test_register_plugin_group(self) -> None:
        """Test plugin groups"""
        app = Application("TestApp")
        initial_groups = app.plugin_groups.copy()

        app.register_plugin_group("new_group")

        self.assertIn("new_group", app.plugin_groups)
        self.assertEqual(len(app.plugin_groups), len(initial_groups) + 1)

    def test_load_plugins(self) -> None:
        """Test plugin loading"""
        app = Application("TestApp")
        magic_mock_plugmaster: MagicMock = MagicMock(
            spec=PlugMaster
        )  # Ensure it's typed as a mock of PlugMaster
        app.set_plugmaster(magic_mock_plugmaster)
        Application.plugin_groups = ["group1", "group2"]

        app.load_plugins()

        plugmaster: Optional[PlugMaster] = app.get_plugmaster()
        self.assertEqual(magic_mock_plugmaster, plugmaster)

        if plugmaster is not None:
            # Now mypy knows that `magic_mock_plugmaster` has the `assert_any_call` method
            magic_mock_plugmaster.load.assert_any_call("group1")
            magic_mock_plugmaster.load.assert_any_call("group2")
        else:
            raise AssertionError("get_plugmaster() returned None")

    @patch("masterpiece.plugmaster.PlugMaster.install")
    def test_install_plugins(self, mock_install: MagicMock) -> None:
        Application._plugmaster = PlugMaster("masterpiece")
        self.app.install_plugins()
        mock_install.assert_called_once_with(self.app)

    @patch(
        "masterpiece.plugmaster.PlugMaster.instantiate_class_by_name",
        return_value=MagicMock(spec=MasterPiece),
    )
    def test_instantiate_plugin_by_name(self, mock_instantiate: MagicMock) -> None:
        Application._plugmaster = PlugMaster("masterpiece")
        plugin = self.app.instantiate_plugin_by_name("plugin_name")
        mock_instantiate.assert_called_once_with(self.app, "plugin_name")
        self.assertIsInstance(plugin, MasterPiece)

    @patch("masterpiece.plugmaster.PlugMaster")
    def test_register_plugin_group2(self, MockPlugMaster: PlugMaster) -> None:
        Application.plugin_groups = ["masterpiece"]
        Application.register_plugin_group("new_plugin")
        self.assertIn("new_plugin", Application.plugin_groups)

    @patch("os.path.expanduser", return_value="/mocked/home")
    def test_get_configuration_filename(self, mock_expanduser: MagicMock) -> None:
        expected_path = os.path.join(
            "/mocked/home", ".masterpiece", "config", "Application"
        )
        filename = Application.get_configuration_filename("Application")
        self.assertEqual(filename, expected_path)

    @patch.object(MockFormat, "save_configuration")
    @patch("masterpiece.masterpiece.MasterPiece.factory")
    def test_save_configuration(self, mock_factory, mock_save):
        Application.serialization_format = "json"
        mock_factory.return_value = {"json": MockFormat}

        Application.save_configuration()

        mock_save.assert_called_once()


    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.expanduser", return_value="/mocked/home")
    @patch(
        "masterpiece.application.Application.get_configuration_filename",
        return_value=os.path.join(
            "/mocked/home", ".masterpiece", "config", "Application"
        ),
    )
    @patch.object(sys, "argv", [""])  # Patch sys.argv to avoid argparse issues
    def test_load_configuration(
        self,
        mock_get_filename: MagicMock,
        mock_expanduser: MagicMock,
        mock_file: MagicMock,
    ) -> None:
        Application.serialization_format = "json"

        # Normalize expected path using os.path.normpath
        expected_path = os.path.join(
            mock_expanduser.return_value,
            ".masterpiece",
            "config",
            "Application.json",
        )

        with patch("masterpiece.masterpiece.MasterPiece.factory") as mock_factory:
            mock_factory.return_value = {"json": MockFormat}

            # Call the method under test
            Application.load_configuration()

        # Normalize the path in the assertion to avoid mismatched separators
        mock_file.assert_called_once_with(expected_path, "r", encoding="utf-8")

    @patch("os.path.expanduser", return_value="/mocked/home")
    @patch("sys.argv", ["anyapp.py", "--config", "test_config", "--init"])
    def test_init_app_id(self, mock_expanduser: MagicMock) -> None:
        expected_path = os.path.join("/mocked/home", ".test_app", "test_config")

        with patch("atexit.register") as mock_atexit_register:
            # Run the method
            Application.init_app_id("test_app")

            # Verify _app_id is set correctly
            self.assertEqual(Application._app_id, "test_app")


if __name__ == "__main__":
    unittest.main()
