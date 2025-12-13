from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class ChangeItemsType(Enum):
    """
    Specifies Item DocumentObject type.
    """

    #Add entity type.
    Add = 0
    #Remove DocumentObject type.
    Remove = 1
    #Clear DocumentObject type.
    Clear = 2

