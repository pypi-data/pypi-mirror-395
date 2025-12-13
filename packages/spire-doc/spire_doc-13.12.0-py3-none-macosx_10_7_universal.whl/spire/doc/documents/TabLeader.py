from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class TabLeader(Enum):
    """
    Enum class that specifies the tab leader.
    
    """

    # No leader.
    NoLeader = 0
    # Dotted leader.
    Dotted = 1
    # Hyphenated leader.
    Hyphenated = 2
    # Single line leader. 
    Single = 3
    # Heavy line leader.
    Heavy = 4
    # The leader line is made up from middle-dots.
    MiddleDot = 5
