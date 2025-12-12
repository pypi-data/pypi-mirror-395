CHANGELOG
=========

[0.1.52]  December 3 2025
--------------------------
- sphinx upgraded to v9.

- New makefile target added **make version**. Prints out the name and
  the version of the package. Running this at the top level recursively
  prints out the versions of all the projects.
  
- Obsolete clean.py removed

- Added a prerequisites directory for personal, developer-specific
  files, e.g. .gitignore. These come in handy when creating new
  masterpiece modules.

- Introduced the **SupervisorThread**, a fault-tolerant supervisory system
  that monitors worker thread crashes, logs them, and automatically
  restarts failed threads.

- Added an **error queue** to the Application and MasterPieceThread
  classes, enabling structured crash reporting for supervised workers.

- Updated MasterPieceThread:
  
  * Added support for storing constructor arguments for thread recreation.
  * Implemented the ``recreate()`` method for safe thread replacement.
  * Improved crash handling and error propagation to the supervisor.

- Application now initializes and starts the SupervisorThread automatically
  in ``run()`` and ``run_forever()``.

- README.rst significantly improved:
  
  * Added clearer explanations of key features.
  * Highlighted Supervisor, MQTT, hierarchical structures, and plugin system.
  * Improved formatting and corrected terminology (e.g. **Grafana**).

- Fixed incorrect export of ``ArgsMaestro`` and replaced it with
  ``ArgMaestro`` in ``__all__``.

- Exposed ``SupervisorThread`` for public API use.

- Minor documentation fixes and enhancements across multiple modules.

- New and extended unit tests for SupervisorThread and crash handling.


  

[0.1.46]  November 15 2025
--------------------------

- Fixed wrong default topic name in MasterPieceThread class.
- Unit tests for MasterPieceThread class updated.


[0.1.36]  March 15 2025
-----------------------

- CI pipeline builds and publishes developer documentation to the `public/` directory for GitLab Pages.
- CI document building stage failed due to a bug in ci-templates, fixed.
- Workaround to sphinx path maddness (relative paths relative to sphinx conf.py file)
- MPHOME yaml variable, for inter package references
  

[0.1.34]  March 15 2025
-----------------------

Updated to comply with the new SPDX expression for packaging standards

Bug fixes:
- pages CI branch fixed
- config/sphinx.mak generates HTML documentation in the project's public folder.
- Sphinx fails to build HTML documentation unless the public/.doctrees subfolder already exists
  


[0.1.29]  March 09 2025
-----------------------

* ``ci-templates`` unified a bit
  

[0.1.28]  March 09 2025
-----------------------

* Build and install developer documentation.



[0.1.26]  March 06 2025
-----------------------

* Fixed incorrect key in to_dict() output: "_version:" (with a colon) is now correctly "_version" without a colon.


[0.1.25]  March 02 2025
-----------------------

This release attempts to fix some troublesome issues related to "Sphinx":

* Added a ``masterpiece/config`` folder for files common to all Masterpiece plugins and applications.

* The Sphinx ``docs/Makefile`` moved into ``config/sphinx.mak`` to avoid duplicating the same file across multiple
  projects. The makefile copies the standard .rst files (e.g., README.rst) to the ``docs/source/`` folder.
  The issue was that Sphinx requires all image paths to be relative to its conf.py file, which breaks the concept
  of reusable documents. 

* The configuration file ``config/sphinxconf.py`` contains definitions common to all projects built on the
  masterpiece framework. This file can be imported into the project-specific conf.py files, which now only need
  to define the project name, again avoiding brain dead copying of the same file across multiple projects.

* CI ``ci-master/*yaml`` scripts define the MPHOME environment variable, allowing projects built on top of the
  Masterpiece framework to refer to the config files.



[0.1.22]  February 2 2025
--------------------------

* ``ci-templates/master-ci.yml`` checks whether ``examples/myapp.py`` exists before trying to build it. 



[0.1.21]  February 18 2025
--------------------------

* Fixed an issue where startup arguments and configuration files were loaded twice.

* Added a missing install_plugins() call to the examples/myhome.app example application.

* Resolved several mypy warnings in unit tests.





[0.1.20]  February 16 2025
--------------------------

* ``--init --config [dir]`` failed if the directory did not already exist, and execution was terminated with
  cannot write config file errors. Now, the application class checks if the directory exists and creates it if it doesn't.


[0.1.19]  February 14 2025
--------------------------

* Timezone bug in ``timeutils.timestamptostr()`` fixed.



[0.1.18]  February 08 2025
--------------------------

* A few log messages have been removed, the code works and  the logs provide no additional value.


[0.1.17]  January 26 2025
-------------------------

* **Makefile:** Projects now have ``Makefile`` at their fingertips. There is a new file ``scripts/project.mak`` containing 
  commonly needed project level targets, e.g. mypy, package, install and upload.


[0.1.16]  January 19 2025
-------------------------

* **ci-templates:** Two template pipelines defined: master-ci.yml and master-plugin-ci.yml, to define common 
  CI pipelines for all the projects built on the framework, and to eliminate copy & pasting the same code through
  numerous packages.
* **UML Diagram:** The UML diagram defined in ``docs/source/index.rst`` updated. It now contains all the relevant
  masterpiece classes.
* **Namespace-packaging:**. All the classes are now exposed via ``__init__.py``. This makes it easier for users
  to import directly from the package itself, rather than having to navigate through submodules.


[0.1.12]  12.1.2025
-------------------

* Useless "Loading plugin ..." logging message fixed, it shows now the actual name of the loaded plugin class.
* Redundant "pyyaml" dependency removed from 'pyproject.toml'.



[0.1.11]  11.1.2025
-------------------

* New method `read_last_value()` added. Retrieves the most recent data point from a specified
  time series measurement. The method allows the software to easily query its last known state
  from the time series database, simplifying state recovery and continuity 
  across application restarts.



[0.1.10]  5.1.2025
------------------

Nothing spectacular in this release—just a few minor bug fixes and improvements. The code appears to run
fine as part of my home automation project, with no issues detected. However, there's still a lot to be done
with type hinting and documentation.

* Fixed intermittent issues with VSCode and Sphinx integration. Added a sphinx target to the root 'Makefile'
  as a workaround for when VSCode reports incorrect errors. Also removed some docstrings that appeared
  perfectly fine to me but not to Sphinx (find myself wasting too much time searching for Sphinx/rst format-related bugs)
* Corrected syntax errors in .rst files. Linked the orphan tutorial.rst and plugintutorial.rst to the root document.
* Refactored the MasterPieceThread class for better modularity and code clarity.
* Fixed a few mypy warnings in unit tests.




[0.1.9]  3.1.2025
-----------------

* A couple of Pypi warnings sorted out.
* `MasterPieceThread` class supports Built-in tests (system-status).


[0.1.8]  30.12.2024
-------------------

**First 'Alpha' release:**

- Version elevated to 0.1.8 and Python Development Status elevated to 3 - Alpha.
- Obsolete Yaml dependencies removed from 'pyproject.toml'


[0.1.7]  30.12.2024
-------------------

**MasterPieceThread:** class added with. This class is both a `Thread` and  `MasterPiece`, with
optional MQTT client for communication.



[0.1.6]  29.12.2024
-------------------

**Logging Level control :**

- Configuration files were read twice, fixed.

- Logging level can be controlled through -l (--log-level) startup arguments. accepts the
  standard log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL



**Interface to MQTT:**

- Added an interface to MQTT. The module `mqtt.py` implements two abstract base classes: `Mqtt` and `MqttMsg`.
  These abstractions allow integration with any Mqtt pub-sub implementation, such as Paho Mosquitto.

  Example of the API:

  To publish:

  .. code-block:: python

    m = {
      "tmp": {"value": 22.5},  # Room temperature value
      "sensor": {
        "vibration": True,  # Vibration status
        "motion": False,  # Motion status
      },
        "unixtime": int(time.time()),
      }

    self.publish("mytopic", json.dumps(m), 1, True)

  To subscribe:

  .. code-block:: python

    mqtt.subscribe("mytopic")


**Interface to Time Series:**

- Added an interface to time series databases. The module `timeseries.py` implements two abstract base classes:
  `TimeSeries` and `Measurement`. These abstractions allow integration with any time series implementation, such as InfluxDB.

  Example of the API:

  .. code-block:: python

    point = (
      self.measurement("motion")
        .tag("sensor", "livingroom")
        .field("motion", motion)
        .field("vibration", vibration)
        .field("roomtemp", roomtemperature)
        .time(epoc2utc(timestamp))  # Converts epoch to UTC timestamp
    )
    self.write(point)

  Alternatively, you can use the `dict` data structure to record measurements:

  .. code-block:: python

    measurement: dict[str, Any] = {
      "measurement": "motion",
      "tag": {"sensor": "livingroom"},
      "field": {
        "motion": motion,
        "vibration": vibration,
        "roomtemp": roomtemperature
      },
      "time" : epoc2utc(timestamp),
    }
    self.write(measurement)



[0.1.4]  17.12.2024
-------------------

**stable-0.1.4:** New stable release with minor improvements and bug fixes:

- **Type-hinting:** completed and `py.typed` file added to indicate 
  that the package supports PEP 561 type hints.

- **PluginManager:** The `add()` method of the `Composite` class now accepts `None` as
  a parameter. In such cases, it raises a `ValueException`.
  For example, calling `self.add(self.instantiate_plugin_by_name("SomePlugin"))` will
  now properly terminate the application if the plugin is not installed.

- **@override:** decorator imported from `typing_extensions` rather than from `typing`,
  for Python 3.9 backward compatibility.

- **YamlFormat:** The YAML serialization format functionality has been removed from the core framework
  and implemented as a separate plugin project, `masterpiece_yaml`.

- **Traversing the hierarchy:**

  `URL` class: A new class for instance name-based identification of objects within hierarchical
    tree structures.

  `make_url()` Method: Generates hierarchical paths for any object in the instance hierarchy.

  `resolve_url()` Method: Locates objects by their URL.

- **print():**

  Method visualizing the instance hierarchy moved from the `example/myapp.py` to `application.py` base class. Originally initiated as a demonstrative piece of code, but turned out to be a valueble feature for any MasterPiece application.



[0.1.3] - 4.11.2024
-------------------

- **stable-0.1.3:** First release tagged with `stable` prefix. When a Git tag is prefixed
  with stable, the masterpiece CD/CI pipeline deploys the package to the PyPI repository.

- **Development Status :: 2 - Pre-Alpha:** PyPi classifier elevated from Planning to Pre-Alpha


[0.1.0] - 3.11.2024
-------------------

- **Version elevated to 0.1.0:** The plugin API has been successfully tested with two separate plugins 
  and confirmed to work. Hooray!

- **classattrs_to_dict():** Who knew iterating over class attributes in Python could be so tricky? 
  Fixed—yes, really!


[0.0.9] - 2.11.2024
-------------------
- **Tutorial:** - Exceptionally well written world-class `tutorial <docs/source/tutorial.rst>`_
  covering the basics and essential features, I hope.

- **Bug Fixes:** 
  - PlugMaster class attempted to instantiate classes not subclassed from the Plugin class. 
  - Exception when issubclass() was called with class that was not registered.
  - several bugs fixed in both load_configuration() and save_configuration().
  - save_configuration() failed to save because it opened the file for reading, fixed.
  - is_abstract() class method removed, use inspect.isabstract() instead.


[0.0.7] - 1st 11.2024
---------------------

- **Milestone Achieved**: Despite the modest version increment, this release 
  brings substantial structural, architectural, and functional improvements. 
  With the release of version 0.0.7, I’ve completed my first two major milestones 
  for the project — definitely a cause for celebration!

- **Directory Structure Finalized**: Removed the ``core`` directory; all
  classes are now organized under ``masterpiece/masterpiece/*.py``.
  (Feeling like I’m evolving from a C++ boomer to a proper Pythonista!)

- **@classproperty**: A decorator class implemented as a replacement 
  for Python's decision to deprecate the combination of ``@classmethod`` and 
  ``@property``. This decorator addresses the fundamental principle of object-oriented 
  programming: any software is essentially composed of code and data (attributes 
  and methods), which can be either class-specific or instance-specific. Given this, 
  it is logical to have `@property` for instance-specific attributes and 
  `@classproperty` for class-specific attributes.

- **Serialization API Finalized**: Decoupled hard-coded JSON serialization,
  implementing it as a separate ``JsonFormat`` class. This is the default
  serialization format for the ``Application`` class decoupling also the format
  from the stream: any data can be formatted to any stream.

- **YamlFormat Added**: Implemented YAML serialization format, which can be selected
  with the startup option ``--application_serialization_form YamlFormat``.

- **Logging Improved**: Supports both class and instance methods, enabling
  both ``Foo.log_error(...)`` and ``foo.error(...)`` syntax.

- **Unit Tests Enhanced**: Coverage significantly improved, now reaching
  approximately 90%.



[0.0.6] - 26.10.2024
--------------------

- **Code and Data Decoupling**: Hardcoded `print()` methods have been removed
  from core classes and re-implemented using the new `do()` method.

- **ArgMaestro**: A class for fully automated class attribute initialization
  through startup arguments. Allows any public class attribute to be
  initialized using the `--classname_attributename [value]` convention.
  The class name is admittedly ridiculous, consider changing it.

- **Unit Test Coverage Improved**: Unit tests have been enhanced to a level
  where they provide meaningful test coverage.

- **Logging Typos Fixed**: All strings have been proofread and typos corrected.


[0.0.5] - 20.10.2024
--------------------

- **New startup argument --init**: If given, all classes in the application
  will create configuration files for their class attributes, if those files
  don't already exist. These configuration files allow users to define custom
  values for all public class attributes.

- **Rotating Logs**: The FileHandler has been replaced with
  TimedRotatingFileHandler, initialized with parameters `when='midnight'`,
  `interval=1`, and `backupCount=7` to rotate the log file daily and keep 7
  backup files. This change resolves the issue of log files growing
  indefinitely, which could eventually lead to the system running out of
  disk space.

- **Documentation Refactored**: All .rst files have been moved from Sphinx's
  docs/source directory to the project root folder for GitLab compatibility.

- **Time Functions**: The methods `epoc2utc()`, `timestamp()`, `epoc2utc()`
  and a few others removed. These were not actually methods of the Masterpiece
  class since they did not require any instance attributes. More importantly,
  this change aims to keep the Masterpiece framework focused on its core
  functionality.


[0.0.4] - October 18, 2024
--------------------------

- **MasterPiece**: Undefined class attribute `_class_id`, added.
- **MetaMasterPiece Refactored**: Replaced with a more lightweight
  `__init_subclass__()` solution, with special thanks to Mahi for his
  contribution.
- **Plugin Class Abstracted**: The plugin class is now subclassed from `ABC`
  to formally implement an abstract base class.
- **Pylint Warnings Resolved**: Fixed issues such as long lines, which have
  been split for better readability.
- **Docstrings Improved**: Added more comprehensive documentation with a
  professional tone for several methods.


[0.0.3] - October 12, 2024
--------------------------

- **From C++ boomer to Python professional**: Directory structure simplified:

  - `src` folder removed
  - `masterpiece/base` folder renamed to `masterpiece/core`
  - `plugins` folder moved outside the project, will be implemented as a
    separate project (one project - one repository principle)
  - Minor additions and improvements to Docstrings.


[0.0.2] - October 10, 2024
--------------------------

- **GitLab Ready**: Revised documentation tone slightly to reflect a more
  professional and serious nature. Removed excessive humor that may have
  detracted from the perceived professionalism of the toolkit.


[0.0.1] - August 4, 2024
------------------------

Pip release with Python pip package uploaded.

New Features and Improvements:

- **Trademark**: Cool (not?) slogan: Masterpiece - Quite a piece of work
- **Plugin API**: Enhanced the plugin API with two classes: `Plugin` and
  `PlugMaster` with compatibility with Python versions 3.8 and later.
  The most recent version tested is 3.12.
- **Meta-Class Automation**: Per-class bureaucracy automated using Python's
  meta-class concept.
- **Folder Structure**: Redesigned for future expansion. There is now separate
  root folders for core and plugin modules.
- **Base Class**: Added new base class for MasterPiece applications in
  `base/application.py`.
- **Example Application**: Added `examples/myhome.py` to demonstrate the
  general structure of MasterPiece applications.
- **Startup Argument Parsing**: Added API for parsing startup arguments.
- **Serialization API**: Fully featured serialization with backward
  compatibility support implemented.
- **Documentation**: Added comprehensive docstrings to numerous classes,
  aiming for fully documented professional Python code.
- **Type Annotations**: Added type annotations to numerous previously
  non-typed method arguments, moving towards a fully typed Python code.
- **Sphinx conf.py**: Created default Sphinx `conf.py` file in the
  `masterpiece/sphinx` folder.
- **Bug Fixes and Improvements**:

  - Added `encoding="utf-8"` to `open()` calls
  - Added `exclude __pycache__` to MANIFEST.in, to avoid including the folders
    with the setup.


[0.0.0] - May 31, 2024
----------------------

Initial, private release (minimal set of classes unified from the RTE and
JUHAM Python applications).

- **Base Class Draft**: Initial version of the `MasterPiece` and `Composite`
  classes.
- **Python Packaging**: Python package infrastructure setup using
  `pyproject.toml`, installable via pip.
- **Documentation**:

  - Added LICENSE, README, and other standard files in .rst format.
  - Developer documentation autogenerated with Sphinx toolset. Support for
    Doxygen dropped.
- **Project Name**: Named the project 'MasterPiece™', with a note that 'M'
  currently stands for mission rather than masterpiece.
- **Miscellaneous**: Some unconventional use of the Python programming
  language.
