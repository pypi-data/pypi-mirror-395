"""
Elementary class implementing hierarchy.

Author: Juha Meskanen
Date: 2024-10-26
"""

from __future__ import annotations
from typing import Callable, Any, Dict, List, Optional, cast
from typing_extensions import override
from .url import URL
from .masterpiece import MasterPiece


class Composite(MasterPiece):
    """Class implementing hierarchy. Objects of this class can consist of children.

    This class can be used for grouping masterpieces into larger entities to model
    any real world apparatus. Hierarchical entities can be manipulated exactly the
    same way as the most primitive objects, e.g. copied, serialized, or manipulated
    via do() method:

    Example:
    ::

        sensors = Composite("motionsensors")
        sensors.add(ShellyMotionSensor("downstairs"))
        sensors.add(ShellyMotionSensor("upstairs"))

        def some_action(node: MasterPiece, context : MyContext) -> bool:
            ...
            return 1 # continue traversal

        # Run traversal
        sensors.do(some_action, my_context)

    """

    def __init__(
        self,
        name: str = "group",
        payload: Optional[MasterPiece] = None,
        children: Optional[list[MasterPiece]] = None,
        parent: Optional[MasterPiece] = None,  # New parameter
    ) -> None:
        super().__init__(name, payload)
        self.children: List[MasterPiece] = children or []
        self.role: str = "union"
        self.parent = parent
        for child in self.children:
            child.parent = self

    @override
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["_group"] = {
            "role": self.role,
            "children": [child.to_dict() for child in self.children],
        }
        return data

    @override
    def from_dict(self, data: Dict[str, Any]) -> None:
        """Recursively deserialize the group from a dictionary, including its
        children.

        Args:
            data (dict): data to deserialize from.
        """
        super().from_dict(data)
        for key, value in data.get("_group", {}).items():
            if key == "children":
                for child_dict in value:
                    child = MasterPiece.instantiate(child_dict["_class"])
                    self.add(child)
                    child.from_dict(child_dict)
            else:
                setattr(self, key, value)

    @override
    def do(
        self,
        action: Callable[["MasterPiece", Dict[str, Any]], bool],
        context: Dict[str, Any],
    ) -> bool:
        """
        Recursively traverses the tree, from root to leaf, left to right direction,
        calling the provided `action` on each node.

        :param action: A callable that takes (node, context) and returns a boolean.
        :param context: Any context data that the action may use.
        :returns: None
        """
        if not super().do(action, context):
            return False
        for child in self.children:
            if not child.do(action, context):
                return False
        return True

    @override
    def root(self) -> Composite:
        root: Composite = cast(
            Composite, super().root()
        )  # Explicitly cast to Composite
        return root

    @override
    def resolve_url(self, url: URL) -> Optional[MasterPiece]:
        # First, run the common find method from MasterPiece
        result = super().resolve_url(url)
        if result:
            return result

        segments = url.segments

        if len(segments) == 0:
            return self  # If URL is empty, return the current object

        if segments[0] == ".":
            # Current object, continue search with the rest of the segments
            return self.resolve_url(URL("/".join(segments[1:])))

        if segments[0] == "..":
            # Parent object, move to the parent and strip the ".."
            if self.parent:
                return self.parent.resolve_url(URL("/".join(segments[1:])))
            return None  # No parent to traverse up

        # Handle child objects (search through children for the first segment)
        for child in self.children:
            if child.name == segments[0]:
                # If the first segment matches the child, recurse into it
                return child.resolve_url(URL("/".join(segments[1:])))

        return None  # No match found in the children

    @override
    def run_forever(self) -> None:
        """
        Dispatches first the call to all children and then to the super class.
        It is up to the sub classes to implement the actual functionality
        for this method.
        """

        self.start_children()
        super().run_forever()
        self.shutdown_children()

    @override
    def run(self) -> None:
        """
        Dispatches first the call to all children and then to the super class.
        It is up to the sub classes to implement the actual functionality
        for this method.
        """
        self.start_children()
        super().run()
        self.shutdown_children()

    @override
    def shutdown(self) -> None:
        """Shuts down the object. First, it dispatches the call to all child objects,
        then calls the superclass method to stop the associated payload object, if one exists.
        """
        self.shutdown_children()
        super().shutdown()

    def add(self, h: Optional[MasterPiece]) -> None:
        """Add new object as children. The object to be inserted
        must be derived from MasterPiece base class.

        Args:
            h (T): object to be inserted.
        """
        if h:
            self.children.append(h)
            h.parent = self
        else:
            raise ValueError(f"None cannot be inserted to {self.name}")

    def start_children(self) -> None:
        """Start  all children."""
        i: int = 0
        for s in self.children:
            self.info(f"Starting up {i} {s.name}")
            s.run()
            i = i + 1
        self.info(f"All {i} children successfully started")

    def shutdown_children(self) -> None:
        """Shuts down the children."""
        i: int = 0
        self.info("Shutting down children")
        for s in self.children:
            self.info(f"Shutting down thread {i} {s.name}")
            s.shutdown()
            i = i + 1
        self.info(f"All {i} children successfully shut down")
