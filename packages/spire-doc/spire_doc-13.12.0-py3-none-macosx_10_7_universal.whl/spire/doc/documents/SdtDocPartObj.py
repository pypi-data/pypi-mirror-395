from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class SdtDocPartObj(SdtDocPart):
    """
    Specifies that the parent structured document tag shall be of a document part type.
    """
    @property

    def Type(self)->'SdtType':
        """
        Gets the type of the structured document tag (SDT), which is set to <see cref="SdtType.DocPartObj"/>.
        """
        GetDllLibDoc().SdtDocPartObj_get_Type.argtypes=[c_void_p]
        GetDllLibDoc().SdtDocPartObj_get_Type.restype=c_int
        ret = CallCFunction(GetDllLibDoc().SdtDocPartObj_get_Type,self.Ptr)
        objwraped = SdtType(ret)
        return objwraped

