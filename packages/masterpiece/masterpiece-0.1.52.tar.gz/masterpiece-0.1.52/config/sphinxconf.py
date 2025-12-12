"""
Common definitions for the Sphinx documentation builder. Define all
project specific settings in the actual project specific conf.py files

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

import sys
import os
import sphinx_bootstrap_theme


# sphinx path hell begins

print("=== DEBUG: sphinxconf.py START ===")
print(f"sphinxconf.py location: {__file__}")
print(f"initial sys.path:")
for p in sys.path:
    print("   ", p)


# sphinx path hell ends
    
master_doc = "index"

html_static_path: list[str] = ["_static"]


extensions = [
    "sphinx.ext.napoleon",  # For support of Google and NumPy style docstrings
    "sphinx.ext.autodoc",  # For automatic generation of API documentation from docstrings
    "sphinx.ext.intersphinx",  # For cross-referencing to external documentation
    "sphinx.ext.todo",  # For TODO list management
    "sphinx.ext.viewcode",  # For links to the source code
    "sphinx.ext.autosummary",  # For automatic generation of summary tables of contents
    "sphinx.ext.doctest",  # For running doctests in docstrings
    "sphinx.ext.ifconfig",  # For conditional content based on configuration values
    "sphinx.ext.githubpages",  # For publishing documentation to GitHub Pages
    "sphinx.ext.coverage",  # For measuring documentation coverage
    "sphinx.ext.mathjax",  # For rendering math via MathJax
    "sphinx.ext.imgmath",  # For rendering math via LaTeX and dvipng
    "sphinx.ext.inheritance_diagram",  # UML diagrams,
    "sphinxcontrib.mermaid",  # for UML diagrams
]


autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "member-order": "groupwise",  # Keep attributes and methods separate
    "inherited-members": False,   # Avoid duplicates from inherited classes
    "special-members": "__init__", # Ensure constructor is documented
    "exclude-members": "__weakref__",  # Avoid unnecessary special attributes
}

napoleon_include_private_with_doc : bool = False
napoleon_include_special_with_doc : bool = False
napoleon_attr_annotations : bool = True
graphviz_output_format: str = "svg"  # for UML diagrams
napoleon_google_docstring: bool = True
napoleon_numpy_docstring: bool = False
autodoc_inherit_docstrings: bool = False
templates_path: list[str] = ["_templates"]
exclude_patterns: list[str] = []
todo_include_todos: bool = True
pygments_style: str = "sphinx"  # Default syntax highlighting style
highlight_language: str = "python"  # Default language for code blocks


html_theme: str = "bootstrap"
html_theme_path: list[str] = sphinx_bootstrap_theme.get_html_theme_path()

html_css_files = [
    "masterpiece.css",
]

