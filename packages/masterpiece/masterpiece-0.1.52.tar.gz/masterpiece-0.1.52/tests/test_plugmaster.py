"""
Author: Juha Meskanen
Date: 2024-10-26
"""

from typing import Any, Optional
from typing_extensions import override
import unittest
from unittest.mock import patch, MagicMock
from masterpiece.plugmaster import PlugMaster
from masterpiece.plugin import Plugin
from masterpiece.composite import Composite
from masterpiece.masterpiece import MasterPiece


class TestPluginFoo(Plugin):
    """Mock plugin class to simulate plugin behavior."""

    def __init__(self, name: str) -> None:
        super().__init__(name)
        # self.install = MagicMock()  # Mock the install method

    @override
    def install(self, app: Composite) -> None:
        app.add(self)
        print(f"plugin {self.name} installed to {app}")


class TestPlugMaster(unittest.TestCase):

    def setUp(self) -> None:
        self.app_name = "test_app"
        self.plugmaster = PlugMaster(self.app_name)
        self.app = Composite(self.app_name)
        self.app.add = MagicMock()  # Mock the add method

        # Define the TestPlugin class
        class Test2Plugin(Plugin):

            def install(self, app: Composite) -> None:
                app.add(self)  # Simulate adding the plugin to the app

        # Add the class to the plugmaster's plugins
        Test2Plugin.__name__ = "Test2Plugin"  # Define __name__ attribute

        self.plugmaster.plugins["TestPlugin"] = Test2Plugin

    @patch("importlib.metadata.entry_points")
    def test_load_plugins(self, mock_entry_points: Any) -> None:
        # Create a mock plugin class
        mock_plugin_class = MagicMock()
        mock_plugin_class.__name__ = "Test2Plugin"  # Define __name__ attribute
        mock_plugin_instance = mock_plugin_class.return_value  # Instance of the plugin
        mock_plugin_instance.install = MagicMock()  # Mock the install method

        # Create a mock entry point
        mock_entry_point = MagicMock()
        mock_entry_point.load.return_value = mock_plugin_class

        # Ensure that entry_points returns a list with our mock entry point
        mock_entry_points.return_value.select.return_value = [mock_entry_point]

        # Call the load method
        self.plugmaster.load("test_app.plugins")

        # Verify that the plugin was added
        self.assertIn("TestPlugin", self.plugmaster.plugins)

    def test_find_class_by_name(self) -> None:
        mock_class = MagicMock(spec=MasterPiece)
        self.plugmaster.plugins["TestPlugin"] = mock_class

        found_class = self.plugmaster.find_class_by_name("TestPlugin")
        self.assertEqual(found_class, mock_class)

        not_found_class = self.plugmaster.find_class_by_name("NonExistentPlugin")
        self.assertIsNone(not_found_class)

    def test_instantiate_class_by_name(self) -> None:
        obj = self.plugmaster.instantiate_class_by_name(self.app, "TestPlugin")
        self.assertIsNotNone(obj)

        # Ensure the add method is called
        self.app.add.assert_called()

    def test_instantiate_class_by_name_with_plugin(self) -> None:
        class MockPlugin(Plugin):
            @override
            def install(self, app: Composite) -> None:
                app.add(self)  # Simulate adding the plugin to the app

        # Add MockPlugin class to the plugmaster
        self.plugmaster.plugins["TestPlugin"] = MockPlugin

        obj: Optional[MasterPiece] = self.plugmaster.instantiate_class_by_name(
            self.app, "TestPlugin"
        )
        self.assertIsNotNone(obj)

        # Verify that install is called on the plugin instance
        obj.install(self.app)  # Simulate calling install
        self.assertTrue(self.app.add.called)

    def test_install_plugins(self) -> None:
        # Call the install method, which should invoke the install method of the plugin class
        self.plugmaster.install(self.app)
        self.assertTrue(self.app.add.called)  # Ensure add was called

    def test_get_plugins(self) -> None:
        mock_class = MagicMock(spec=MasterPiece)
        self.plugmaster.plugins["TestPlugin"] = mock_class

        plugins = self.plugmaster.get()
        self.assertIn("TestPlugin", plugins)
        self.assertEqual(plugins["TestPlugin"], mock_class)

    def test_plugin_install(self) -> None:
        mock_app = MagicMock(spec=Composite)
        plugin = TestPluginFoo("test plugin")

        # Call the install method
        plugin.install(mock_app)

        # Verify the install method was called with the mock app
        self.assertTrue(mock_app.add.called)  # Ensure add was called


if __name__ == "__main__":
    unittest.main()
