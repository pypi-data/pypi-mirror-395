"""
   ____        _       __              __    
  / __ \____  | |     / /___  _________/ /____
 / / / / __ \ | | /| / / __ \/ ___/ __  / ___/
/ /_/ / / / / | |/ |/ / /_/ / /  / /_/ (__  ) 
\____/_/ /_/  |__/|__/\____/_/   \__,_/____/  

Onwords - Gate Control Package
https://ostapi.onwords.in
"""

__version__ = "0.2.0"
__author__ = "Onwords"

from .controller import control, Controller
from .api import configure, get_products, OnwordsAPI

__all__ = [
    # Core functions
    "configure",
    "get_products", 
    "control",
    # Classes
    "Controller",
    "OnwordsAPI",
    # Meta
    "__version__"
]
