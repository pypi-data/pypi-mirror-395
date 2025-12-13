"""
FHIL Python Utils

A collection of general utility functions for Python data analysis and visualization, including SVM-based classification
and plotting tools for various data types.

This package provides tools for:
- SVM feature analysis and classification
- Confusion matrix visualization
- Grid plotting for multiple AnnData objects
- Cluster annotation and consensus calling
"""

from ._version import version as __version__

# Import submodules so they're accessible via dir() and direct access
from . import svm
from . import plotting
from . import sc
from . import spatial

__all__ = [
    '__version__',
    'svm',
    'plotting',
    'sc',
    'spatial',
]
