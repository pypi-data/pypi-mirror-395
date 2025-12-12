"""Streamlit App Generator - Generate complete Streamlit applications.

This package provides tools to automatically generate Streamlit applications
with authentication, database connections, and multi-page support.
"""

__version__ = "0.1.0"
__author__ = "Leandro Meyer DC"
__email__ = "lmdcorti@gmail.com"

from .generator import AppGenerator

__all__ = ["AppGenerator", "__version__"]