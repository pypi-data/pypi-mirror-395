"""
Classes for loading and managing plugins. 

See also the 'plugin' module.

Note: Referring to 'MasterPiece' modules as plugins may not fully do them justice, 
as the term 'plugin' could imply that plugin classes are somehow less capable than 
core, built-in classes. However, this is far from the case. Don't let the terminology 
mislead you — plugin classes are not second-class citizens.

The only difference between plugin modules and the core set of MasterPiece modules is that 
plugins are dynamic by nature.  They can be added or removed without altering a single 
line of code in the main application. Plugin modules have the same level of control and 
capability as the core classes, offering 100% control over the application.

Author: Juha Meskanen
Date: 2024-10-26
"""

import sys
from typing import Type, Dict, Union, Optional
import importlib.metadata

from .masterpiece import MasterPiece
from .composite import Composite
from .plugin import Plugin


class PlugMaster(MasterPiece):
    """
    The `Plugmaster` class is responsible for managing and loading plugins into an application.

    The `Plugmaster` is designed to work with plugins that are `Masterpiece` objects or subclasses
    thereof. Plugins can optionally be derived from  the `Plugin` class.

    If a plugin implements the `Plugin` interface, it is responsible for determining what objects
    should be added to the application.

    If a plugin is not a `Plugin` class, it is simply loaded, and it is the responsibility
    of the application configuration file or the application code to determine how to utilize
    the plugin.

    """

    def __init__(self, name: str) -> None:
        """Instantiates and initializes the Plugmaster for the given application name. This
        name refers to the list of plugins, as defined in the application 'pyproject.toml'.
        For more information on 'pyproject.toml' consult the Python documentation.

        Args:
            name (str): Name determining the plugins to be loaded.
        """
        super().__init__(name)
        # self.plugins: List[Type[MasterPiece]] = []
        self.plugins: Dict[str, Type[MasterPiece]] = {}
        self.app: Optional[Composite] = None

    def load(self, name: str) -> None:
        """Fetch the entry points associated with the 'name', call their 'load()' methods
        and insert to the list of plugins.
        Note: Python's 'importlib.metadata' API has been redesigned
        a couple of times in the past. The current implementation has been tested with
        Python 3.8, 3.9 and 3.12.

        Args:
            name (str): Name determining the plugins to be loaded.

        """

        if sys.version_info >= (3, 10):
            entry_points = importlib.metadata.entry_points().select(
                group=f"{name}.plugins"
            )
        elif sys.version_info >= (3, 9):
            # TODO: pylint error if python version different
            entry_points = importlib.metadata.entry_points().get(f"{name}.plugins", [])
        else:
            # For Python 3.8 and below
            entry_points = importlib.metadata.entry_points()[f"{name}.plugins"]

        for entry_point in entry_points:
            try:
                entry = entry_point.load()
                self.plugins[entry.__name__] = entry
                self.info(f"Plugin {entry.__name__} loaded")

            except Exception as e:
                self.error(f"Failed to load plugin {entry_point.name}: {e}")

    def find_class_by_name(self, name: str) -> Union[Type[MasterPiece], None]:
        """Find and return a plugin class by its name.

        Returns:
            plugin class  (MasterPiece) or none if not found
        """
        return self.plugins.get(name)

    def instantiate_class_by_name(
        self, app: Composite, name: str
    ) -> Union[MasterPiece, None]:
        """Instantiate and add the plugin into the application.

        Args:
            app (Composite) : parent object, for hosting the instances createdby the plugin.
            name (str) : name of the plugin to be instantiated
        """
        entry = self.find_class_by_name(name)
        if entry is not None:

            # install to host application
            if issubclass(entry, Plugin):
                obj: Plugin = entry()
                obj.install(app)
                self.info(
                    f"Plugin {obj.name}:{str(type(obj))} plugged in to {app.name}"
                )
                return obj
            else:
                self.info(f"Class {entry.__name__} imported  into {app.name}")
                return entry()
        return None

    def install(self, app: Composite) -> None:
        """Instantiate and add all the registered plugins to the application.

        Typically is up to the application or the configuration to define the instances
        to be added. This method is provided for testing purposes only.

        Args:
            app (Composite) : parent object (application), for hosting the instances
            created by the plugin.

        """
        for name, entry in self.plugins.items():
            # install to host application
            if issubclass(entry, Plugin):
                plugin: Plugin = entry()
                plugin.install(app)
                self.info(
                    f"Plugin {name} {plugin.name}:{str(type(plugin))} added to {app.name}"
                )
            else:
                self.info(f"Class {entry.__name__} imported to {app.name}")

    def get(self) -> Dict[str, Type[MasterPiece]]:
        """Fetch the list of plugins classes.

        Returns:
            List[Type[MasterPiece]]: List of plugins
        """
        return self.plugins
