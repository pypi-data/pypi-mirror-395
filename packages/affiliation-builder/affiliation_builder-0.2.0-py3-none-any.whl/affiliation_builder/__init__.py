"""
Affiliation Builder

Build bipartite affiliation networks from JSON data using NetworkX.

This package provides tools for creating bipartite networks where one set of nodes
(e.g., events) connects to another set (e.g., persons and organizations) through
affiliation relationships.
"""

__version__ = "0.1.0"
__author__ = "Timo Frühwirth"
__license__ = "MIT"

from .core import build

__all__ = ["build"]