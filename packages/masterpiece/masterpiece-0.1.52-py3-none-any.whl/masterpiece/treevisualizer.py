"""
TreeVisualizer, for rendering instance hierarchy.

Author: Juha Meskanen
Date: 2024-10-26
"""

from typing import Any
from colorama import Fore, Style, init

from .composite import Composite
from .masterpiece import MasterPiece

# Initialize Colorama
init(autoreset=True)


class TreeVisualizer:
    """
    The `TreeVisualizer` class is designed to visually represent hierarchical structures
    using ASCII art and colors, making it easy to understand the relationships between
    nodes in a tree. It is particularly useful for visualizing instances of the
    `MasterPiece` and `Composite` classes, which represent elements in a tree structure.

    Features:
    ---------

    - Supports customizable colors for node representation using the Colorama library.
    - Prints the hierarchy of nodes with clear visual indicators (├─, └─, and │) to represent parent-child relationships.
    - Automatically resets colors after each print to maintain consistent output.

    Usage:
    ------
    To use the `TreeVisualizer`, first create an instance by specifying the desired color.
    Then, call the `print_tree` method with the root node of your tree.

    Example:
    --------
    .. code-block:: python

        from masterpiece.core import TreeVisualizer, MasterPiece, Composite

        # Create a sample hierarchy
        parent = Composite("parent")
        child1 = MasterPiece("child1")
        child2 = MasterPiece("child2")
        parent.add(child1)
        parent.add(child2)

        # Initialize the visualizer with a specified color
        visualizer = TreeVisualizer("green")

        # Print the hierarchy
        visualizer.print_tree(parent)
    """

    def __init__(self, color: str):
        """Initialize the TreeVisualizer with a color.

        Args:
            color (str): The color to use for visualizing the tree.
        """
        self.color = color

    def get_color(self) -> Any:
        """Return the corresponding Colorama color code for the specified color."""
        colors = {
            "red": Fore.RED,
            "green": Fore.GREEN,
            "yellow": Fore.YELLOW,
            "blue": Fore.BLUE,
            "magenta": Fore.MAGENTA,
            "cyan": Fore.CYAN,
            "white": Fore.WHITE,
            "reset": Style.RESET_ALL,
        }
        return colors.get(
            self.color.lower(), Fore.WHITE
        )  # Default to white if color not found

    def print_tree(
        self, node: MasterPiece, prefix: str = "", is_last: bool = True
    ) -> None:
        """Print the hierarchy of the node using ├─, └─, and │ with the specified color.

        Args:
            node (MasterPiece): The root node to print.
            prefix (str, optional): The prefix for the current level.
            is_last (bool, optional): Whether this node is the last child.
        """
        # Get the color code for the current node
        color_code = self.get_color()

        # Print the current node's name with the color
        print(prefix, end="")
        if prefix:
            print(f"{color_code}└─ " if is_last else f"{color_code}├─ ", end="")
        print(f"{color_code}{node.name}{Style.RESET_ALL}")  # Reset color after printing

        # Prepare the new prefix for the child nodes
        if prefix:
            prefix += "    " if is_last else f"{color_code}│   "
        else:
            prefix = "    " if is_last else f"{color_code}│   "

        # Recursively print all the children
        if isinstance(node, Composite):
            for i, child in enumerate(node.children):
                is_last_child = i == len(node.children) - 1
                self.print_tree(child, prefix, is_last_child)
