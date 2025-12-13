from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class OutlineLevel(Enum):
    """
    Enum defining paragraph format's outline level.
    
    """

    # Outline level: "Level 1"
    Level1 = 0
    # Outline level: "Level 2"
    Level2 = 1
    # Outline level: "Level 3"
    Level3 = 2
    # Outline level: "Level 4"
    Level4 = 3
    # Outline level: "Level 5"
    Level5 = 4
    # Outline level: "Level 6"
    Level6 = 5
    # Outline level: "Level 7"
    Level7 = 6
    # Outline level: "Level 8"
    Level8 = 7
    # Outline level: "Level 9"
    Level9 = 8
    # Outline level: "Body"
    Body = 9
