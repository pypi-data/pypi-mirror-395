from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class ListLevelOverride (  DocumentSerializable) :
    """
    Represents a class for overriding the level format in a document serialization process.
    """
    def GetHashCode(self)->int:
        """
        Gets the hash code for the current object.
        """
        GetDllLibDoc().ListLevelOverride_GetHashCode.argtypes=[c_void_p]
        GetDllLibDoc().ListLevelOverride_GetHashCode.restype=c_int
        ret = CallCFunction(GetDllLibDoc().ListLevelOverride_GetHashCode,self.Ptr)
        return ret

