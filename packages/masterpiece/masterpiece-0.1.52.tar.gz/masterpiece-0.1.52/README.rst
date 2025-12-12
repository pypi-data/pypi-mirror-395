Masterpiece™
============

**Masterpiece** is a Python framework designed for the rapid development of Python applications of any kind.

It emerged from the unification of numerous diverse applications and projects, consolidating their shared
functionality into a single, cohesive structure. By standardizing classes across different applications
and extracting the common core, Masterpiece provides a robust foundation that can be adapted to any
use case.


At its heart, Masterpiece is a tree-based container system for modeling real-world systems, with features needed
by all applications, features e.g. serialization, configuration, startup argument parsing, just to name a few. 



Key Features
------------

Masterpiece integrates a rich set of features essential for modern application development, including:

* Seamless **plug-in** architecture - enabling recursive extension and development of custom modules for any application.

* **Supervisor** for monitoring crashes, logging them, and automatically restarting the crashed threads

* **Hierarchical data structures** – A flexible tree container for organizing objects.

* **Serialization** support – Save and load hierarchical objects efficiently.

* **Factory Method** pattern – Dynamically create instances of registered classes.

* **Configuration** management – Automated class attribute configuration through various serialiation formats, e.g. JSon.

* Event and network loops – Support for asynchronous workflows and network-driven applications.

* General purpose – Designed to be adaptable to various domains and use cases.

* File system oriented object identification / resolving through 'object paths'

* Multi-threading, based on the assumption that Python community will get the **global lock** issue sorted out.

* **MQTT** Communication: Enables seamless communication between components using the MQTT protocol, ideal for distributed systems.

* Time series support using databases e.g. **Influx**

* Built-in documentation framework based on **Sphinx**
  


Design Concepts and Features
----------------------------

- **Pythonic Purity**: Adheres to Python conventions, ensuring idiomatic, readable, and maintainable code.
- **First-Time Excellence**: Designed to be reliable, correct, and efficient from the start—while keeping things fun!
- **Completeness**: A minimal yet robust zero redundancy API that gives developers total control over all aspects of their applications.
- **Productivity**: Highly modular and reusable codebase to achieve maximum functionality with minimal effort. Productivity grows with the size of the project.
- **Proper Abstraction**: Provides clean abstractions for essential third-party libraries, shielding application code from underlying framework changes.


Project Status and Current State
--------------------------------

Here’s what’s currently available in Masterpiece™:

- **Absolutely Bug-free Status!**: Just kidding—there are no *known* bugs (so far).
- **Wiki**: The initial Wiki pages are under construction. Visit the `Masterpiece Wiki <https://gitlab.com/juham/masterpiece/-/wikis/home>`_.
- **Tutorial**: A `tutorial <docs/source/tutorial.rst>`_ to help you get started with building your masterpieces.
- **Package Infrastructure**: The Python package setup is finalized, using `pyproject.toml`.
- **Classes**: Existing classes have been finalized and tested in a production environment.
- **Example Application**: A sample application (`examples/myapp.py`) prints out its instance structure when run. 
  Despite its simplicity, it demonstrates the structure of a typical scalable and fully configurable software.
- **Plugin Projects**: Several plugin examples, such as `masterpiece_plugin`, which adds a "Hello World" greeting to `myapp.py`, 
  demonstrate minimal yet functional plugin implementations.
- **MQTT**: Enables communication between all Masterpiece™ objects.
- **InfluxDB V3 Time Series**: Supports writing and reading from time-series databases.
- **Serialization**: Built-in support for JSON serialization, with options to extend to other formats via plugins.
- **CI Pipelines**: For both frameworks and plugins.
- **...**: And probably more features I’ve forgotten while writing this.

Here's what's **NOT** ready:

- **GUI**: no graphical user interface of any kind. The current projects rely on 3rd party tools, e.g. **Grafana** for visualization.


Projects
--------

Masterpiece comes in a set of Python projects:

1. **Masterpiece (core framework)**:

  This is the core framework for building plugin-aware, multi-threaded applications. It includes a simple yet 
  fully functional application to help you get started and serves as a plugin-aware reference application 
  that can be scaled up to any size.

2. **Masterpiece Plugin (plugin example)**:

  This is a basic plugin example that demonstrates how to create third-party plugins for applications built 
  using Masterpiece. It’s as simple as saying **"Hello, World!"**, literally.

3. **Masterpiece XML Format plugin:**:

  Plugin that adds XML serialization format support to Masterpiece. 

4. **Masterpiece Yaml Format plugin:**:

  Another format plugin. Adds Yaml support to Masterpiece.

5. **Masterpiece Influx:**:

  Support for InfluxDB V3 time series database.

6. **Masterpiece Paho MQTT:**:

  Support for Paho Mosquitto MQTT.





Installing Masterpiece
----------------------

**Step 1**: Install Masterpiece and run the example application
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To install the core framework:

.. code-block:: bash

    pip install masterpiece

Then, navigate to the example folder and run the application:

.. code-block:: bash

    python examples/myapp.py

The application will print out its instance hierarchy. This is a simple example application to demonstrate the
basic structure of any multi-threaded, plugin-based, scalable MasterPiece applications.

**Example output**:

.. code-block:: text

    home
        ├─ grid
        ├─ downstairs
        │   └─ kitchen
        │       ├─ oven
        │       └─ fridge
        └─ garage
            └─ EV charger


**Step 2**: Install the desired Masterpiece Plugins
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To extend the application with the say **masterpiece_plugin**:

.. code-block:: bash

    pip install masterpiece_plugin

Run the application again:

.. code-block:: bash

    python examples/myapp.py

You'll now see a new object in the instance hierarchy, along with a friendly "Hello, World!" object.

**Example output**:

.. code-block:: text

    home
        ├─ grid
        ├─ downstairs
        │   └─ kitchen
        │       ├─ oven
        │       └─ fridge
        ├─ garage
        │   └─ EV charger
        └─ Hello World - A Plugin


**Step 3**: Configurating
^^^^^^^^^^^^^^^^^^^^^^^^^

The application also demonstrates the usage of startup arguments. Run the application again:

.. code-block:: text

    examples/myapp.py --init --solar 10 --color red

and new 'Solar plant 10 kW' object appears in the tree.

- The ``--init`` argument tells the application to save its current configuration to a configuration files. 
- The ``--solar`` argument creates an instance of a solar power plant with a specified peak power of 10 kW.
- The ``--color`` argument can be used for setting the color for the tree diagram.

The above class properties (and many more) can also be defined in the class configuration files. By default, 
the configuration files are created in the ``~/.myapp/config`` folder, as determined by the ``application identifier`` 
and ``--config [anyname]``.

For example, ``--config temp`` will use the configuration files stored in the ``~/.myapp/temp/`` 
folder.


What's next
-----------

Congratulations! You've successfully installed Masterpiece, extended it with a plugin, and explored its configuration system. 
But what is all this for? 

That part is up to your imagination. Here's what you can explore next:

- Write Plugins: Develop your own plugins to extend Masterpiece with domain-specific functionality.
  Use the masterpiece_plugin as a starting point for inspiration.

- Leverage Configurations: Take advantage of configuration files to fine-tune your application's behavior 
  without changing the code. Experiment with the --config argument to manage multiple configurations for 
  different scenarios.

- Design a Custom Application: Build a unique application that fits your needs by combining existing plugins, 
  creating new objects in the instance hierarchy, and integrating external services or data sources.

- Contribute to the Community: Share your plugins or improvements with the Masterpiece community. 

Masterpiece provides the building blocks. Where you go from here is entirely up to you. Happy coding!


Contributing
------------

Please check out the `Masterpiece Issue Board <https://gitlab.com/juham/masterpiece/-/boards>`_ for tracking progress 
and tasks.


Developer Documentation
-----------------------

For full documentation and usage details, see the full documentation at `Documentation Index <docs/build/html/index.html>`_ 
(The docs may look rough; I’m still unraveling Sphinx's mysteries).


Special Thanks
--------------

Big thanks to the generous support of [Mahi.fi](https://mahi.fi) for helping bring this framework to life.
