from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class TextFormat(Enum):
    """
    Enum for defining different text formats.
    
    """

    # No text formatting
    none = 0
    # Uppercase text formatting.
    Uppercase = 1
    # Lowercase text formatting.
    Lowercase = 2
    # First capital text formatting.
    FirstCapital = 3
    # Title case text formatting.
    Titlecase = 4
