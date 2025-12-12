"""
PyFrameX - Next-Generation Native DataFrame for Python
======================================================

A revolutionary DataFrame engine that is:
- Simple like Excel
- Powerful like SQL  
- Smart like AI
- Pure Python implementation

Author: Idriss Bado
Email: idrissbadoolivier@gmail.com
Version: 0.1.0
License: MIT
"""

from .frame import Frame
from .columns import IntColumn, FloatColumn, StringColumn, DateColumn, BoolColumn
from .query import QueryPlanner
from .ml import AutoML

__version__ = "0.1.0"
__author__ = "Idriss Bado"
__email__ = "idrissbadoolivier@gmail.com"

__all__ = [
    "Frame",
    "IntColumn",
    "FloatColumn", 
    "StringColumn",
    "DateColumn",
    "BoolColumn",
    "QueryPlanner",
    "AutoML"
]
