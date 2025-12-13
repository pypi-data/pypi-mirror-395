from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class SdtCitation(SdtControlProperties):
    """
    Sdt of type citation.
    """
    @property

    def Type(self)->'SdtType':
        """
        Gets the type of the object, which is set to <see cref="SdtType.Citation"/>.
        """
        GetDllLibDoc().SdtCitation_get_Type.argtypes=[c_void_p]
        GetDllLibDoc().SdtCitation_get_Type.restype=c_int
        ret = CallCFunction(GetDllLibDoc().SdtCitation_get_Type,self.Ptr)
        objwraped = SdtType(ret)
        return objwraped

