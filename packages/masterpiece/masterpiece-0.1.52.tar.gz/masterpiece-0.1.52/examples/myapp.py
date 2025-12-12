"""Example application demonstrating a typical masterpiece application featuring:

- Class initialization through startup arguments 
- Class configuration, with automatically created class configuration files
- Serialization/deserialization of instances
- Visualization of the instance hierarchy

Usage:
------

python myapp.py --init --myapp_serialization_format JsonFormat
python myapp.py 

"""

from masterpiece import Application, MasterPiece, Composite
from typing_extensions import override


class MyApp(Application):
    """Application demonstrating the structure of masterpiece applications.
    Also demonstrates plugin awareness and startup arguments.
    When run, the application prints out its instance hierarchy:

    Example:
        home
        ├─ grid
        ├─ downstairs
        │   └─ kitchen
        │       ├─ oven
        │       └─ fridge
        ├─ garage
        │   └─ EV charger
        └─ solar plant 5.0 kW

    If the --solar [kW] startup argument is passed with a power value, the
    "solar plant" instance is added to the hierarchy.

    """

    solar: float = 0.0

    def __init__(self, name: str = "myapp") -> None:
        """Initialize the home application with the given name.

        Instance attributes can be initialized from class attributes,
        through a serialization file, or from constructor parameters.

        Args:
            name (str): The name of the application.
        """
        super().__init__(name)
        self.create_home()
        self.install_plugins()

    def create_home(self) -> None:
        """Create a default built-in home structure, which can be overridden
        by the instance hierarchy defined in the serialization file. See --file
        startup argument.
        """
        self.create_power_grid()
        self.create_downstairs()
        self.create_garage()
        self.create_solar()

    def create_power_grid(self) -> None:
        """Create the power grid."""
        grid = MasterPiece("grid")
        self.add(grid)

    def create_solar(self) -> None:
        """Create solar plant, if configured by '~/.myapp/config/MyAppApp.json',
        or the '-s' startup argument."""
        if self.solar > 0:
            self.add(MasterPiece(f"solar plant {self.solar} kW"))

    def create_downstairs(self) -> None:
        """Create the downstairs section with a kitchen and appliances."""
        downstairs = Composite("downstairs")
        self.add(downstairs)
        kitchen = Composite("kitchen")
        downstairs.add(kitchen)
        oven = MasterPiece("oven")
        kitchen.add(oven)
        fridge = MasterPiece("fridge")
        kitchen.add(fridge)

    def create_garage(self) -> None:
        """Create the garage with an EV charger."""
        garage = Composite("garage")
        self.add(garage)
        ev_charger = MasterPiece("EV charger")
        garage.add(ev_charger)

    @override
    def run(self) -> None:
        """Start the application."""
        super().run()

        # Print out the instance hierarchy
        self.print()


def main() -> None:
    """Main function that initializes, instantiates, and runs the MyApp application."""

    # Class initialization phase so that they can be instantiated with desired properties
    # Make this app plugin-aware. See the 'masterpiece_plugin' project for a minimal plugin example.
    Application.init_app_id("myapp")
    MyApp.load_plugins()
    Application.load_configuration()

    # Create an instance of MyApp application
    home = MyApp("home")
    home.install_plugins()

    # Initialize from the serialization file if specified
    home.deserialize()

    # Start event processing or the application's main loop
    home.run()

    # Save the application's state to a serialization file (if specified)
    home.serialize()


if __name__ == "__main__":
    main()
