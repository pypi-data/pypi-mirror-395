Mastering the Piece
===================

This tutorial covers the ``examples/myapp.py`` application to help you get
started with writing world-class masterpieces.

Prerequisites
-------------

Fetch the Masterpiece core framework and the plugin:

.. code-block:: bash

    git clone https://gitlab.com/juham/masterpiece.git
    git clone https://gitlab.com/juham/masterpiece_plugin.git

Navigate to the `masterpiece/example` folder and open the example
application in your favorite editor (Emacs, anyone?):

.. code-block:: bash

    emacs examples/myhome.py


MyHome Application
------------------

The main() function of masterpiece Application is as follows:

.. code-block:: python

    from myhome import MyHome

    def main() -> None:
        # configure  classes
        MyHome.init_app_id("myhome")
        MyHome.load_plugins() 
        Application.load_configuration()

        # instantiate
        home = MyHome("home")

        # run
        home.run()



Importing Masterpiece Classes
-----------------------------

The first lines of code import the classes used as building blocks in
`myapp.py`.

.. code-block:: python

    from masterpiece import Application, MasterPiece, Composite, TreeVisualizer



Application Identifier
^^^^^^^^^^^^^^^^^^^^^^

The main function initializes the application with an appropriate
"application identifier," a string that describes the software's purpose.

.. code-block:: python

   def main() -> None:
       MyHome.init_app_id("myhome")

This identifier determines where the application reads its configuration
files and enables plugins to be written for applications.

Note: The application identifier is **not** the application name! It’s
something shared by all related applications, for example, representing a
software "family" or company if multiple applications share the same
architecture.


Loading Plugins
^^^^^^^^^^^^^^^

If desired, load plugins with:

.. code-block:: python

    MyHome.load_plugins()

The plugin discovery uses Python's `importlib.metadata` API. Every Masterpiece
project can define project entry points in its `pyproject.toml` file:

.. code-block:: python

    [project.entry-points."masterpiece.plugins"]

Then, a plugin can specify the entry-points it can expand - in its entry points in `pyproject.toml`:

.. code-block:: python

    helloworld_plugin = "masterpiece_plugin:HelloWorld"

This example shows that the `masterpiece_plugin` was written for any
Masterpiece application, relying only on core Masterpiece framework features.

Applications should (in fact, **must**) introduce application-specific
entry points to allow plugins tailored to them.


Configuring Application
^^^^^^^^^^^^^^^^^^^^^^^

Application configuration involves setting class attributes, done either
through class-specific configuration files or startup arguments, and loaded
with:

.. code-block:: python

    Application.load_configuration()

Configuration files are found in:

.. code-block:: bash

    ~/.[app_id]/[configuration]/[classname].[ext]

where `[app_id]` is the application identifier. `[configuration]` is `config`
by default but can be changed with the `--config` startup switch, allowing
different configurations (e.g., production vs. test).

Each class has a configuration file (`[classname]`) with format-specific
extension (`[ext]`), usually `JSON`. YAML is also supported, and plugins can
introduce more formats. Select the desired one with:

.. code-block:: bash

    python myapp.py --application_serialization_format 'YamlFormat'

This demonstrates the factory method pattern, where implementations are
chosen through configuration.

If there are no configuration files, the application can generate default ones
with:

.. code-block:: bash

    python myapp.py --init

This creates a new set of configuration files at `~/.myapp/config/`, using
default values.

Creating the Application
^^^^^^^^^^^^^^^^^^^^^^^^

Once classes have the desired properties, the main function can instantiate
them:

.. code-block:: python

    home = MyHome("myhome")

This creates a `MyHome` application instance named "myhome".



Running the Application
^^^^^^^^^^^^^^^^^^^^^^^

Applications perform operations in the `run()` method.

.. code-block:: python

    home.run()

For example, `myapp.py` prints out the instances in the application:

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


The Application Class
---------------------

Masterpiece is object-oriented, meaning that components should be proper
classes. For instance, `MyApp`:

.. code-block:: python

    class MyHome(Application):
        # class attributes
        solar: float = 0.0
        color: str = "yellow"

        def __init__(self, name: str = "myhome") -> None:
            super().__init__(name)
            # instance attributes
            self.create_home()
            self.install_plugins()

    [snip]

`MyHome` inherits from `Application`, gaining features like plugin support,
class attribute configuration, serialization, and startup argument handling,
just to name  a few.

Configure public class attributes (`solar` and `color`) via the
`~/.myhome/config/MyHome.json` file:

.. code-block:: text

    {
        "solar": 10.0,
        "color": "yellow"
    }

or via startup arguments:

.. code-block:: bash

    myhome --myapp_solar 20 --myapp_color "red"

Configuration priority:

1. Startup arguments, if defined
2. Configuration files, if present
3. Hard-coded values


Modeling Reality
^^^^^^^^^^^^^^^^

Real-world objects are hierarchical. The Masterpiece framework models this
with the `Composite` class, allowing `MasterPiece` or `Composite` objects to
be added as children. Application classes can also be a `Composite`.

Methods like `create_power_grid()` demonstrate this:

.. code-block:: python

    def create_power_grid(self):
        grid = MasterPiece("grid")
        self.add(grid)

The method inserts 'grid' object into the application as a children.

This creates an "ownership tree," where the application can robustly manage resources
and serialize the hierarchy.

Visualizing the Hierarchy
^^^^^^^^^^^^^^^^^^^^^^^^^

The `run()` method has two parts:

.. code-block:: python

    def run(self) -> None:
        super().run()
        self.print()

    def print(self):
        visualizer = TreeVisualizer(self.color)
        visualizer.print_tree(self)

Note that we could put the  code in print() method into the run() method, 
after all, it is just two lines of code needed to print the hierarhcy. However,
this would be bad programming practice! By putting printing specific code
into a separate print() other applications sub-classed from ours, can easily
override the print() method, if they choose to do so.

Note also that Masterpiece objects, including applications, can host "payload"
objects.  Therefore, always pass `run()` to the superclass. 


Implementing Plugins
^^^^^^^^^^^^^^^^^^^^

The framework encourages focusing on **plugins** rather than traditional
applications. Applications should implement only the minimal infrastructure
required, leaving features to be handled as plugins.

The next tutorial covers this topic in depth:
`Implementing Plugins <docs/source/plugintutorial.rst>`_
