from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class PropertyValueType(Enum):
    """
    Enum class that specifies the possible property value types.
    
    """

    # Specifies Value type as boolean.
    Boolean = 0
    #  Specifies Value type as date.
    Date = 1
    #  Specifies Value type as float.
    Float = 2
    #  Specifies Value type as double.
    Double = 3
    #  Specifies Value type as integer.
    Int = 4
    # Represents a 32-bit signed integer.
    Int32 = 5
    #  Specifies Value type as String.
    String = 6
    #  Specifies Value type as byte array.
    ByteArray = 7
    # The property is an array of strings.
    StringArray = 8
    # The property is an array of objects.
    ObjectArray = 9
    #  Specifies Value type as ClipData.
    ClipData = 10
    # The property is string composed of ASCII characters only.
    AsciiString = 11
    # The property is some other type.
    Other = 12
