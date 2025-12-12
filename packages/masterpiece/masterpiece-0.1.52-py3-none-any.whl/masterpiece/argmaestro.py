"""
Automated class configuration through startup arguments.

Author: Juha Meskanen
Date: 2024-10-26
"""

import argparse
from typing import Type, Union, get_type_hints

from .masterpiece import MasterPiece


class ArgMaestro:
    """
    Automated class configuration through startup arguments.
    ArgMaestro manages startup argument creation and parsing for the class attribute initialization
    of the registered classes. Each startup argument is of form '--[app]_[class]_[attr]'.
    Note: currently supports only int, str, bool and float types.
    """

    def __init__(self) -> None:
        """Construct ArgMaestro with a single argument parser"""
        self.parser = argparse.ArgumentParser(description="Application arguments")
        self.args: dict[str, Type[MasterPiece]] = {}

    def add_class_arguments(self, clazz: Type[MasterPiece]) -> None:
        """Create startup arguments for a class's attributes.

        Args:
            clazz (class): The class to generate arguments for.
        """
        type_hints = get_type_hints(clazz)
        self.args[clazz.__name__] = clazz  # Store the class for future use

        # Filter attributes to ensure only class-specific ones are considered
        for attr, attr_type in type_hints.items():
            try:
                if not attr.startswith("_") and not callable(
                    getattr(clazz, attr, None)
                ):
                    # Skip attributes that are not in the class's own __dict__
                    if attr not in clazz.__dict__:
                        continue

                    # Check attribute type and set default if necessary
                    default_value = getattr(clazz, attr, None)
                    if default_value is None:
                        # Assign logical defaults if None is found
                        if attr_type is float:
                            default_value = 0.0
                        elif attr_type is int:
                            default_value = 0
                        elif attr_type is str:
                            default_value = ""

                    # Argument type handling
                    arg_type: Type[Union[int, float, bool, str]]
                    if attr_type is int:
                        arg_type = int
                    elif attr_type is float:
                        arg_type = float
                    elif attr_type is bool:
                        self.parser.add_argument(
                            f"--{clazz.__name__.lower()}_{attr}",
                            action="store_true",
                            help=f"Enable or disable {attr} in {clazz.__name__}",
                        )
                        print(f"--{clazz.__name__.lower()}_{attr}")
                        continue  # Boolean flag added without needing a default or type
                    else:
                        arg_type = str  # Default to string for unspecified types

                    self.parser.add_argument(
                        f"--{clazz.__name__.lower()}_{attr}",
                        type=arg_type,
                        default=default_value,
                        help=f"Set {attr} in {clazz.__name__} (type: {attr_type.__name__})",
                    )
                    print(
                        f"--{clazz.__name__.lower()}_{attr}, type:{arg_type} default: {default_value}"
                    )
            except Exception as e:
                print(f"Error {e} in parsing argument {attr}")

    def parse_args(self) -> None:
        """Parse arguments and assign values to each class's attributes."""
        # print(self.parser.format_help())
        args = self.parser.parse_args()
        args_dict = vars(args)

        for class_name, clazz in self.args.items():
            # Assign parsed values to class attributes
            for arg, value in args_dict.items():
                prefix = class_name.lower() + "_"
                if arg.startswith(prefix):
                    attr = arg[len(prefix) :]
                    setattr(clazz, attr, value)
