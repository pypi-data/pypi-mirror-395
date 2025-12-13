from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class SdtControlProperties(SpireObject):
    """
    Base class for all Structured Document Tags control-specific properties.
    Encapsulates all differences between Sdt controls, allowing to define additional
    properties and methods in descendant classes.
    """
    @property

    def Type(self)->'SdtType':
        """
        Gets the type of the structured data type.
        """
        GetDllLibDoc().SdtControlProperties_get_Type.argtypes=[c_void_p]
        GetDllLibDoc().SdtControlProperties_get_Type.restype=c_int
        ret = CallCFunction(GetDllLibDoc().SdtControlProperties_get_Type,self.Ptr)
        objwraped = SdtType(ret)
        return objwraped

