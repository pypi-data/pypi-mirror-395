from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class ListType(Enum):
    """
    Specifies type of the list format.
    """

    # Specifies numbered list. 
    Numbered = 0
    # Specifies bulleted list.
    Bulleted = 1
    # No numbering.
    NoList = 2

