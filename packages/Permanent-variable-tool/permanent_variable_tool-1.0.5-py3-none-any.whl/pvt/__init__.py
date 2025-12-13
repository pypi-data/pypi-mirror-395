"""
Permanent Variable Tool (PVT)
=============================
 
A lightweight Python library for persistent variable storage using file-based serialization.
"""
 
from .new import new 
from .read import read 
from .delete import delete 
from .find import find
from .list import list
from .copy import copy

import os
 
__version__ = "1.0.5"
__author__ = ""
__email__ = "q111911111q@outlook.com" 
 
__all__ = ["new", "read", "delete", "find", "list", "copy"]

data = "C:\\pvt_data"
if not os.path.exists(data): 
    os.makedirs(data) 