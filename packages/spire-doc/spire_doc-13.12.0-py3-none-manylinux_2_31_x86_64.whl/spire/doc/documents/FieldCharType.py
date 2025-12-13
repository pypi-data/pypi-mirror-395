from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class FieldCharType(Enum):
    """
    Enum class representing the types of field characters.
    """

    # The character is a start character, which defines the start of a complex field.
    Begin = 0
    # The character is a separator character, which defines the end of the field codes and the start of the field result for a complex field.
    Seperate = 1
    # The character is a end character, which defines the end of a complex field.
    End = 2
    # Unknown
    Unknown = 3
    # Simple field.
    SimpleField = 4
