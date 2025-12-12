"""
Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

import sys
import os

# pull in the default Sphinx stuff from masterpiece framework
sys.path.insert(0, os.path.join("..", "..", "config"))
from sphinxconf import *

# -- Project specific info ---
project: str = "masterpiece"
copyright: str = "2024, juha meskanen"
author: str = "juha meskanen"
