"""
The elementary base class of everything.

Author: Juha Meskanen
Date: 2024-10-26
"""

from __future__ import annotations

import inspect
import logging
from threading import Thread
from queue import Queue
from typing import Any, Callable, Optional, Type, Union, cast
from .url import URL


class classproperty:
    """
    A decorator that allows you to define class-level properties.
    Replaces the deprecated combination of @classmethod and @property.
    """

    def __init__(self, func: Callable[[Type[Any]], Any]) -> None:
        """
        Initialize the classproperty with the function to decorate.

        Args:
            func: A callable that accepts a class type and returns any value.
        """
        self.func = func

    def __get__(self, instance: Any, owner: Type[Any]) -> Any:
        """
        Get the class property value by calling the decorated function with the class.

        Args:
            instance: The instance of the class (not used here).
            owner: The class that owns this property.

        Returns:
            The result of calling the decorated function with the class.
        """
        return self.func(owner)


class MasterPiece:
    """An object with a name. Base class of everything. Serves as the
    foundational base class for any real-world object that can be a part of
    a hierarchy.

    """

    # non-serializable private class attributes
    _log: Optional[logging.Logger] = None
    _factory: dict[str, Type[MasterPiece]] = {}

    def __init_subclass__(cls, **kwargs: dict[str, Any]) -> None:
        """Called when a new sub-class is created.

        Automatically registers the sub class by calling its register()
        method. For more information on this method consult Python
        documentation.
        """
        super().__init_subclass__(**kwargs)
        cls.register()

    @classmethod
    def classattrs_to_dict(cls) -> dict[str, Any]:
        """Convert the class's own attributes to a dictionary, excluding inherited and private ones."""
        return {
            attr: value
            for attr, value in cls.__dict__.items()
            if not callable(value)  # Exclude regular methods
            and not isinstance(
                value, (classmethod, staticmethod, classproperty)
            )  # Exclude class/staticmethods
            and not attr.startswith("__")  # Exclude special attributes like __module__
            and not attr.startswith("_")  # Exclude private/protected attributes
        }

    @classmethod
    def classattrs_from_dict(cls, attributes: dict[str, Any]) -> None:
        """Set only the class's own attributes from a dictionary."""
        # Get the set of attributes defined in this class itself
        own_class_attrs = set(cls.__dict__.keys())

        for key, value in attributes.items():
            # Only set attributes that belong directly to this class (not inherited)
            if key in own_class_attrs:
                setattr(cls, key, value)

    @classmethod
    def has_class_method_directly(cls, method_name: str) -> bool:
        """
        Check if the method is defined directly in the class (not inherited).
        """
        method = getattr(cls, method_name, None)
        # Ensure that the method is callable and check its defining class
        if callable(method):
            # Check if the method's class is the same as the one we are querying
            return cast(bool, method.__qualname__.split(".")[0] == cls.__name__)
        return False

    @classmethod
    def factory(cls) -> dict[str, Type[MasterPiece]]:
        """Fetch the dictionary holding class names and associated classes.

        Returns:
            factory: with class names and associated classes
        """
        return cls._factory

    @classmethod
    def register(cls) -> None:
        """Register the class.

        Called immediately upon class initialization, right before the class attributes
        are loaded from the class specific configuration files.

        Subclasses can extend this with custom register functionality:

        .. code-block:: python

            class MyMasterPiece(MasterPiece):

                @classmethod
                def register(cls):
                    super().register()  # Don't forget
                    cls._custom_field = True
        """
        cls.init_class(cls)

    @classmethod
    def init_class(cls, clazz: Type[MasterPiece]) -> None:
        """Initialize class.  Registers the class into the
        class factory .

        Args:
            clazz (class): class to be initialized
        """
        if clazz.__name__ not in cls._factory:
            if inspect.isabstract(clazz):
                cls.log_info(f"Abstract {clazz.__name__} skipped")
            else:
                cls._factory[clazz.__name__] = clazz
                cls.log_info(f"Class {clazz.__name__} initialized")

    @classmethod
    def set_log(cls, l: logging.Logger) -> None:
        """Set logger.

        Args:
            l (logger): logger object
        """

        cls._log = l

    @classmethod
    def get_class_id(cls) -> str:
        """Return the class id of the class. Each class has an unique
        name that can be used for instantiating the class via
        :meth:`Object.instantiate` method.

        Args:
            cls (class): class

        Returns:
            id (str): unique class identifier through which the class can be
            instantiated by factory method pattern.
        """
        return cls.__name__

    def __init__(
        self,
        name: str = "noname",
        payload: Optional[MasterPiece] = None,
        parent: Optional[MasterPiece] = None,
    ):
        """
        Initialize a MasterPiece object.

        Args:
            name (str): The name of the object.
            payload (MasterPiece, optional): Optional payload data associated with the object. Defaults to None.
            parent (MasterPiece, optional): The parent object in the hierarchy. Defaults to None.
        """
        self.name = name
        self.payload = payload
        self.parent = parent
        self._elapsed: float = 0.0
        self._num_updates: int = 0
        self.errorq : Optional[Queue[tuple[MasterPiece, BaseException, str]]] = None

    @classmethod
    def log_debug(cls, msg: str, details: str = "") -> None:
        """Logs the given debug message to the application log.

        Args:
            msg (str): The  message to be logged.
            details (str): Additional detailed information for the message to be logged
        """
        full_message = f"{cls.__name__} : {msg}"
        if details:
            full_message += f" - {details}"
        if cls._log is not None:
            cls._log.debug(full_message)
        else:
            print(full_message)

    @classmethod
    def log_warning(cls, msg: str, details: str = "") -> None:
        """Logs the given debug message to the application log.

        Args:
            msg (str): The  message to be logged.
            details (str): Additional detailed information for the message to be logged
        """
        full_message = f"{cls.__name__} : {msg}"
        if details:
            full_message += f" - {details}"
        if cls._log is not None:
            cls._log.warning(full_message)
        else:
            print(full_message)

    @classmethod
    def log_info(cls, msg: str, details: str = "") -> None:
        """Logs the given  message to the application log.

        Args:
            msg (str): The  message to be logged.
            details (str): Additional detailed information for the message to be logged
        """
        full_message = f"{cls.__name__} : {msg}"
        if details:
            full_message += f" - {details}"
        if cls._log is not None:
            cls._log.info(full_message)
        else:
            print(full_message)

    @classmethod
    def log_error(cls, msg: str, details: str = "") -> None:
        """Logs the given  message to the application log.

        Args:
            msg (str): The  message to be logged.
            details (str): Additional detailed information for the message to be logged
        """
        full_message = f"{cls.__name__} : {msg}"
        if details:
            full_message += f" - {details}"
        if cls._log is not None:
            cls._log.error(full_message)
        else:
            print(full_message)

    def error_queue(self) ->  Optional[Queue[tuple["MasterPiece", BaseException, str]]]:
        """Fetch the error queue associated with the object, for reporting crashes

        Returns:
            Queue[tuple["MasterPiece", BaseException, str]]: error queue
        """
        if self.errorq is not None:
            return self.errorq
        if self.parent:
            return self.parent.error_queue()
        return None


    def debug(self, msg: str, details: str = "") -> None:
        """Logs the given debug message to the application log.

        Args:
            msg (str): The information message to be logged.
            details (str): Additional detailed information for the message to be logged
        """
        self.log_debug(f"{self.name} : {msg}", details)

    def info(self, msg: str, details: str = "") -> None:
        """Logs the given information message to the application log.

        Args:
            msg (str): The information message to be logged.
            details (str): Additional detailed information for the message to be logged
        """
        self.log_info(f"{self.name} : {msg}", details)

    def warning(self, msg: str, details: str = "") -> None:
        """Logs the given warning message to the application log.

        Args:
            msg (str): The message to be logged.
            details (str): Additional detailed information for the message to be logged
        """
        self.log_warning(f"{self.name} : {msg}", details)

    def error(self, msg: str, details: str = "") -> None:
        """Logs the given error message to the application log.

        Args:
            msg (str): The message to be logged.
            details (str): Additional detailed information for the message to be logged
        """
        self.log_error(f"{self.name} : {msg}", details)

    def to_dict(self) -> dict[str, Any]:
        """Convert instance attributes to a dictionary."""

        return {
            "_class": self.get_class_id(),  # the real class
            "_version": 0,
            "_object": {
                "name": self.name,
                "payload": (
                    self.payload.to_dict() if self.payload is not None else None
                ),
            },
        }

    def from_dict(self, data: dict[str, Any]) -> None:
        """Update instance attributes from a dictionary."""

        if self.get_class_id() != data["_class"]:
            raise ValueError(
                f"Class mismatch, expected:{self.get_class_id()}, actual:{data['_class']}"
            )
        for key, value in data["_object"].items():
            if key == "payload":
                if value is not None:
                    self.payload = MasterPiece.instantiate(value["_class"])
                    self.payload.from_dict(value)
                else:
                    self.payload = None
            else:
                setattr(self, key, value)

    def copy(self) -> MasterPiece:
        """Create and return a copy of the current object.

        This method serializes the current object to a dictionary using the `to_dict` method,
        creates a new instance of the object's class, and populates it with the serialized data
        using the `from_dict` method.

        This method uses class identifier based instantiation (see factory method pattern) to
        create a new instance of the object, and 'to_dict' and 'from_dict'  methods to initialize
        object's state.

        Returns:
            A new instance of the object's class with the same state as the original object.

        Example:
        ::

            clone_of_john = john.copy()
        """

        data = self.to_dict()
        copy_of_self = MasterPiece.instantiate(self.get_class_id())
        copy_of_self.from_dict(data)
        return copy_of_self

    def do(
        self,
        action: Callable[["MasterPiece", dict[str, Any]], bool],
        context: dict[str, Any],
    ) -> bool:
        """
        Execute the given action to the object, by calling the provided `action`.

        Args:
            action(Callable[["MasterPiece", dict[str, Any]], bool]): A callable that takes
            (node, context) and returns a boolean.
            context (dict[str, Any]): Any context data that the action may use.

        Returns:
            The return value from the executed action.
        """
        return action(self, context)

    def run(self) -> None:
        """Run the masterpiece.  Dispatches the call to `payload` object and
        returns  the control to the caller.
        """
        if self.payload is not None and isinstance(self.payload, MasterPiece):
            self.payload.run()

    def run_forever(self) -> None:
        """Run the payload forever. This method will return only when violently
        terminated. If the object does not have playload object, or it is not
        instance of 'MasterPiece' class then returns immediately and this method has
        no effect.
        """
        if self.payload is not None and isinstance(self.payload, MasterPiece):
            try:
                self.payload.run_forever()
                print("Newtorking loop exit without exception")
            except KeyboardInterrupt:
                print("Application interrupted by user.")
            except (ValueError, IOError) as e:
                print(f"Specific error occurred: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")

    def shutdown(self) -> None:
        """Shutdown the payload object. If the payload object is None, or is not instance of MasterPiece,
        then the call has no effect.
        """
        if self.payload is not None and isinstance(self.payload, MasterPiece):
            self.payload.shutdown()

    @classmethod
    def instantiate(cls, class_id: str, *args: Any) -> MasterPiece:
        """Create an instance of the class corresponding to the given class identifier.

        Args:
            class_id (str): Identifier of the class to instantiate.
            *args: Optional arguments to pass to the class constructor.

        Returns:
            MasterPiece: An instance of the class corresponding to the given class identifier.
        """
        if class_id in cls._factory:
            m : MasterPiece = cls._factory[class_id](*args)
            return m
        raise ValueError(f"Attempting to instantiate unregistered class {class_id}")

    @classmethod
    def find_class(cls, class_id: str) -> Union[Type[MasterPiece], None]:
        """Create an instance of the class corresponding to the given class identifier.

        Args:
            class_id (str): Identifier of the class to instantiate.
            *args: Optional arguments to pass to the class constructor.

        Returns:
            MasterPiece: An instance of the class corresponding to the given class identifier.
        """
        if class_id in cls._factory:
            return cls._factory[class_id]
        return None

    @property
    def parent(self) -> Optional[MasterPiece]:
        return self._parent

    @parent.setter
    def parent(self, value: Optional[MasterPiece]) -> None:
        self._parent = value

    def make_url(self) -> URL:
        """Generate the URL for the composite, including all children."""
        if self.parent:
            parent_url = self.parent.make_url()
            return URL(f"{parent_url}/{self.name}")
        return URL(f"/{self.name}")

    def root(self) -> MasterPiece:
        """Fetch the root object

        Returns:
            MasterPiece: root object
        """
        if self.parent:
            return self.parent.root()
        return self

    def resolve_url(self, url: URL) -> Optional["MasterPiece"]:
        """Find a MasterPiece in the hierarchy matching the URL."""
        segments = url.segments

        if len(segments) == 0:
            return self  # Base case: if URL is empty, return self (root)

        if segments[0] == ".":
            # Current object, continue search with the rest of the segments
            return self.resolve_url(URL("/".join(segments[1:])))

        if segments[0] == "..":
            # Parent object, move to the parent (if exists)
            if self.parent:
                # Remove the ".." segment before passing the rest to the parent
                return self.parent.resolve_url(URL("/".join(segments[1:])))
            return None  # No parent to traverse up

        # Regular segment comparison (matching this object's name)
        if segments[0] == self.name:
            if len(segments) == 1:
                return self  # Found a match for the current segment
            # Continue search in parent, remove the first segment from the URL
            if self.parent:
                return self.parent.resolve_url(URL("/".join(segments[1:])))

        return None  # If nothing matches, return None

    def update_metrics(self, elapsed: float) -> None:
        """Updates the number of `update()` methods calld, and time spent in the method.
        This method is called internally from the `update()` method.

        Args:
            elapsed (float): elapsed seconds.
        """
        self._elapsed += elapsed
        self._num_updates += 1

    def acquire_time_spent(self) -> float:
        """Reads off the average time the thread has spent in its `update()` method since
        the last call, and resets the statistics for the next measurement cycle. This method can be used
        for monitoring healtiness of the thread.

        Returns:
            elapsed (float): elapsed seconds.
        """
        if self._num_updates > 0:
            time_spent: float = self._elapsed * 1000.0 / self._num_updates
            self._num_updates = 0
            self._elapsed = 0.0
            return time_spent
        else:
            return 0.0


# Register MasterPiece manually since __init_subclass__() won't be called on it.
MasterPiece.register()
