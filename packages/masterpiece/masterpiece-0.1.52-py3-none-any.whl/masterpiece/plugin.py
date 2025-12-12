"""
Base classes for plugins.

Implements an abstract base class for plugins.

Author: Juha Meskanen
Date: 2024-10-26
"""

from abc import ABC, abstractmethod
from .composite import Composite
from .masterpiece import MasterPiece


class Plugin(MasterPiece, ABC):
    """Abstract base class for plugins."""

    @abstractmethod
    def install(self, app: Composite) -> None:
        """Instantiates and installs the classes in the plugin module into the given 'app' target
        object.
        This is an abstract method that the plugin classes must implement. Plugins may
        choose not to do anything here and instead leave it up to the user, or a higher level
        software layer.

        Args:
            app (Composite): application to plug into
        """
