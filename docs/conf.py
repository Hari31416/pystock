# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "pystock"
copyright = "2023, Harikesh Kushwaha"
author = "Harikesh Kushwaha"

version = "0.1.0"
release = "0.1.0"

import os
import sys

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath(".."))

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.napoleon",  # Supports Google / Numpy docstring
    "sphinx.ext.autodoc",  # Documentation from docstrings
    "sphinx.ext.doctest",  # Test snippets in documentation
    "sphinx.ext.todo",  # to-do syntax highlighting
    "sphinx.ext.ifconfig",  # Content based configuration
    "m2r2",  # Markdown support
]
source_suffix = [".rst", ".md"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "classic"
html_static_path = ["_static"]
