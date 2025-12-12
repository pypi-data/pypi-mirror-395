Implementing Plugins
====================


Introduction
------------

The framework strongly encourages not to write applications but **plugins**.

Applications should implement the minimal infrastructure required for the application
in question.

All the features should be implemented as independent plugins, that can be installed, or
not to be installed.

Each plugin should implement one self-contained and complete feature. If you install it,
then you get a new feature in your application. If you uninstall it, then the application
will not have a single piece of information related to the feature in question.

An example of a good plugin is a new serialization format, e.g., XmlFormat. Once installed,
the user will have an option to use it:

.. code-block:: bash

  anyapp --application_serialization_format XmlFormat

This will be the topic for the next tutorial `Implementing plugins <docs/source/plugintutorial.rst>`_.

Object-Oriented Philosophy
--------------------------

Using this design, productivity increases with the size of the application because the number
of reusable components increases over time, making it faster to implement new features. 

1. **Reusable Components**: As more plugins are developed, each representing a discrete feature
   or capability, the pool of reusable components increases. This allows developers to leverage
   existing plugins when building new features, reducing the time and effort required for
   implementation.

2. **Simplified Development**: With a plugin architecture, teams can work on different plugins
   simultaneously without stepping on each other’s toes. This parallel development not only speeds
   up feature delivery but also encourages innovation, as teams can focus on specific areas of
   functionality.

3. **Easier Maintenance and Upgrades**: Since plugins are independent, updating or replacing one
   feature does not necessitate a complete overhaul of the application. This modularity makes
   maintaining and upgrading the application more manageable, which is particularly valuable in
   larger systems.

4. **Scalability**: As the application scales, the modular nature of plugins makes it easier to
   manage complexity. New features can be added incrementally, allowing for gradual enhancement
   of the application without overwhelming the development team or introducing bugs.

5. **User Customization**: Users benefit from the flexibility to choose which features they want
   to include in their application, making it easier for them to tailor the software to their
   specific needs without requiring extensive modifications.


Implementing XML Format Plugin
------------------------------

TBD
