"""
Author: Juha Meskanen
Date: 2024-10-26
"""

import argparse
import os
import sys
from queue import Queue
from threading import Thread
from typing import List, Type, Optional, Union

from typing_extensions import override

from .format import Format
from .argmaestro import ArgMaestro
from .plugmaster import PlugMaster
from .composite import Composite
from .masterpiece import MasterPiece
from .log import Log
from .treevisualizer import TreeVisualizer
from .supervisor import SupervisorThread

class Application(Composite):
    """Masterpiece application class. Implements startup argument parsing,
    plugin management and initialization of class attributes through
    class specific configuration files.

    """

    plugins: List[Type[MasterPiece]] = []
    serialization_file: str = ""
    serialization_format: str = "JsonFormat"
    plugin_groups = ["masterpiece"]  # plugin group, for Python's module discovery
    color: str = "yellow"
    log_level: int = 0

    _plugmaster: Optional[PlugMaster] = None
    _argmaestro: Optional[ArgMaestro] = None
    _init: bool = False  # initialize class configuration files
    _app_id: str = "masterpiece"  # default application id
    _config = "config"  # default configuration

    def __init__(self, name: str, payload: Optional[MasterPiece] = None) -> None:
        """Instantiates and initializes. By default, the application log
        filename is set to the same as the application name.

        Args:
            name (str): The name of the application, determining the default log filename.
            payload (MasterPiece): Playload object associated with this object.
        """
        super().__init__(name, payload)
        self.errorq : Queue[tuple[Thread, BaseException, str]] = Queue()
        self.supervisor_thread: Optional[SupervisorThread] = SupervisorThread(self.errorq)

    @classmethod
    def get_plugmaster(cls) -> Optional[PlugMaster]:
        """Fetch the plugmaster object reponsible for plugin management.

        Returns:
            PlugMaster: object
        """
        return cls._plugmaster

    @classmethod
    def set_plugmaster(cls, plugmaster: PlugMaster) -> None:
        """Set the plugmaster object reponsible for plugin management.

        Args:
            plugmaster (PlugMaster): object managing plugins
        """
        cls._plugmaster = plugmaster

    @classmethod
    def get_argmaestro(cls) -> Optional[ArgMaestro]:
        """Fetch the plugmaster object reponsible for plugin management.

        Returns:
            PlugMaster: object
        """
        return cls._argmaestro

    @classmethod
    def set_argmaestro(cls, argmaestro: ArgMaestro) -> None:
        """Set the argmaestro object reponsible for plugin management.

        Args:
            argmaestro (PlugMaster): object managing plugins
        """
        cls._argmaestro = argmaestro

    @classmethod
    def get_configuration_filename(cls, name: str) -> str:
        """Generate the user specific file name of the configuration file based on the class name.

        Args:
            name (str): object managing plugins

        """
        return os.path.join(
            os.path.expanduser("~"), "." + cls._app_id, cls._config, name
        )

    @classmethod
    def save_configuration(cls) -> None:
        """Create class configuration file, if configuration is enabled and
        if the file does not exist yet. See --config startup argument.
        """
        filename: str = "undefined"
        if cls.serialization_format == "":
            cls.log_warning(f"No serialization format specified, configuration skipped")
            return
        cls.log_info(f"Saving configuration")

        format_class: Optional[Type[MasterPiece]] = MasterPiece.factory().get(
            cls.serialization_format
        )
        if format_class is not None and issubclass(format_class, Format):
            file_ext: str = format_class.file_extension
            for name, ctor in MasterPiece.factory().items():
                if ctor is not None:
                    try:
                        filename = cls.get_configuration_filename(name) + file_ext

                        # Ensure the target directory exists
                        directory = os.path.dirname(filename)
                        if directory and not os.path.exists(directory):
                            os.makedirs(directory, exist_ok=True)

                        with open(filename, "w", encoding="utf-8") as f:
                            format = format_class(f)
                            format.save_configuration(ctor)
                            cls.log_info(f"Configuration file {filename} saved")
                    except Exception as e:
                        cls.log_error(f"Error in saving {name}:{filename} {e}")

    @classmethod
    def load_configuration(cls) -> None:
        """Load class attributes from a configuration file."""
        filename: str = "undefined"
        if cls.serialization_format == "":
            cls.log_warning(f"No serialization format specified, configuration skipped")
            return
        cls.log_info(f"Loading configuration using {cls.serialization_format}")
        cls.parse_args()
        format_class: Type[MasterPiece] = MasterPiece.factory()[
            cls.serialization_format
        ]
        if format_class is not None and issubclass(format_class, Format):
            file_ext: str = format_class.file_extension
            for name, ctor in MasterPiece.factory().items():
                if ctor is not None:
                    filename = cls.get_configuration_filename(name) + file_ext
                    try:
                        with open(filename, "r", encoding="utf-8") as f:
                            format = format_class(f)
                            format.load_configuration(ctor)
                            cls.log_info(f"Configuration file {filename} loaded")
                    except Exception as e:
                        # cls.log_error(f"Error reading {filename}, {e}")
                        # not an error if file does not exist yet
                        pass

    @classmethod
    def parse_args(cls) -> None:
        """Register classes with ArgMaestro."""
        cls._argmaestro = ArgMaestro()
        for c, clazz in MasterPiece.factory().items():
            if clazz is not None:
                cls._argmaestro.add_class_arguments(clazz)
            else:
                cls.log_error(f"None entry in the class factory for {c}")
        cls._argmaestro.parse_args()

    @classmethod
    def init_app_id(cls, app_id: str = "myapp") -> None:
        """
        Initialize application id. Parses initial startup that depend on application id.
        Must be called before any classes are instanced.

        Arguments:
            -a, --app (str): Application ID.
            -c, --config (str): Configuration name, empty string for no configuration
            -i, --init (bool): Whether to create class configuration files if not already created.
        """
        Application._app_id = app_id
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("-a", "--app", type=str, help="Application ID")
        parser.add_argument("-c", "--config", type=str, help="Configuration")
        parser.add_argument(
            "-l",
            "--log_level",
            type=str,
            help="Log level - DEBUG, INFO,  WARNING, ERROR",
        )
        parser.add_argument(
            "-i",
            "--init",
            action="store_true",
            help="Create class configuration files",
        )
        args, remaining_argv = parser.parse_known_args()
        sys.argv = [sys.argv[0]] + remaining_argv
        MasterPiece.set_log(Log(app_id, Log.parse_level(args.log_level)))
        if args.config:
            Application._config = args.config
        if args.app:
            Application._app_id = args.app
        if args.init:
            Application._init = args.init
            cls.log_info("--init requested, creating class configuration files")
        cls.log_info(f"Configuration files in  ~/.{cls._app_id}/{cls._config}")

        if cls._init:
            cls.log_info(
                "--init specified, class configuration files will be created upon exit"
            )


    @classmethod
    def register_plugin_group(cls, name: str) -> None:
        """Registers a new plugin group within the application. Only plugins that match
        the registered groups will be loaded. By default, all 'masterpiece' plugins
        are included. Frameworks and apps built on the MasterPiece framework can define
        more group names, enabling plugins to be developed for any
        those as well.


        Args:
            name (str): The name of the plugin group to be registered
        """

        if not name in cls.plugin_groups:
            cls.plugin_groups.append(name)

    @classmethod
    def load_plugins(cls) -> None:
        """Loads and initializes all plugins for instantiation. This method
        corresponds to importing Python modules with import clauses."""
        if cls._plugmaster is None:
            cls._plugmaster = PlugMaster(cls.get_app_id())

        for g in cls.plugin_groups:
            cls._plugmaster.load(g)

    
    def instantiate_plugin_by_name(self, name: str) -> Union[MasterPiece, None]:
        """Installs the plugin by name, that is, instantiates the plugin class
        and inserts the instance as child to the application.
        Args:
            name (str): name of the plugin class
        """
        if self._plugmaster is None:
            return None
        return self._plugmaster.instantiate_class_by_name(self, name)

    def install_plugins(self) -> None:
        """Installs plugins into the application by invoking the `install()` method
        of each loaded plugin module.
        **Note:** This method is intended for testing and debugging purposes only.
        In a typical use case, the application should handle the instantiation of classes and
        manage their attributes as needed.
        """
        if self._plugmaster is None:
            self._plugmaster = PlugMaster(self.get_app_id())
        self._plugmaster.install(self)

    def deserialize(self) -> None:
        """Deserialize instances from the startup file specified by 'serialization_file'
        class attribute, or '--file' startup argument.
        """
        if self.serialization_file != "" and self.serialization_format != "":
            self.info(
                f"Deserializing masterpieces from {self.serialization_file} using {self.serialization_format}"
            )
            format_class: Type[MasterPiece] = MasterPiece.factory()[
                self.serialization_format
            ]
            if issubclass(format_class, Format):
                with open(self.serialization_file, "r", encoding="utf-8") as f:
                    format = format_class(f)
                    format.deserialize(self)
                    self.info(f"File {self.serialization_file} successfully read")
            else:
                raise TypeError(
                    f"{self.serialization_format} is not a subclass of Format"
                )
        else:
            self.warning(
                f"No deserialization this time, --serialization_file not specified"
            )

    def serialize(self) -> None:
        """Serialize application state to the file specified by 'serialization_file'
        class attribute'.
        """
        if self.serialization_file != "":
            self.info(
                f"Saving masterpieces to {self.serialization_file} of type {self.serialization_format}"
            )
            format_class: Type[MasterPiece] = MasterPiece.factory()[
                self.serialization_format
            ]
            if issubclass(format_class, Format):
                with open(self.serialization_file, "w", encoding="utf-8") as f:
                    format = format_class(f)
                    format.serialize(self)
                    self.info(f"File {self.serialization_file} successfully written")
            else:
                raise TypeError(
                    f"{self.serialization_format} is not a subclass of Format"
                )
        else:
            self.warning("No serialization this time, --serialization_file not set")

    @classmethod
    def get_app_id(cls) -> str:
        """Fetch the application id.  Application id determines the folder
        in which the configuration files for classes are held. Note that
        a single package can ship with more than just one executable application,
        all with the same application id.

        ..todo: Application id '_app_id' is prefixed with '_' to signal that it is a
        private attribute (python) and that should not be serialized (masterpiece).
        Isn't there something like @transient in Python? App id needs to be accessed
        outside, which is why this get_app_id() method is needed.

        Returns:
            str: application id determign application registry for class attribute serialization
        """
        return cls._app_id

    @override
    def run(self) -> None:
        if self._init:
            self.save_configuration()
        else:
            if( self.supervisor_thread is not None):
                self.supervisor_thread.start() 
            super().run()

    @override
    def run_forever(self) -> None:
        if self._init:
            self.save_configuration()
        else:
            if( self.supervisor_thread is not None):
                self.supervisor_thread.start() 
            super().run_forever()

    def print(self) -> None:
        """
        Print the instance hierarchy of the application using
        `TreeVisualizer`
        """
        visualizer1 = TreeVisualizer(self.color)
        visualizer1.print_tree(self)
