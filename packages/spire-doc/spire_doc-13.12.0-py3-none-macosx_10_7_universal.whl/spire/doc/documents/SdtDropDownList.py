from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class SdtDropDownList (  SdtDropDownListBase) :
    """
    Represents a drop-down list in a document.
    """
    @dispatch
    def __init__(self):
        """
        Initializes a new instance of the SdtDropDownList class.
        """
        GetDllLibDoc().SdtDropDownList_CreateSdtDropDownList.restype = c_void_p
        intPtr = CallCFunction(GetDllLibDoc().SdtDropDownList_CreateSdtDropDownList,)
        super(SdtDropDownList, self).__init__(intPtr)

    @property

    def Type(self)->'SdtType':
        """
        Gets the type of the structured document tag (SDT), which is a drop-down list.
        """
        GetDllLibDoc().SdtDropDownList_get_Type.argtypes=[c_void_p]
        GetDllLibDoc().SdtDropDownList_get_Type.restype=c_int
        ret = CallCFunction(GetDllLibDoc().SdtDropDownList_get_Type,self.Ptr)
        objwraped = SdtType(ret)
        return objwraped
