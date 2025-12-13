from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class SdtComboBox (  SdtDropDownListBase) :
    """
    Represents a combo box control.

    Args:
        None

    Returns:
        None
    """
    @dispatch
    def __init__(self):
        """
        Initializes a new instance of the SdtComboBox class.

        Args:
            None

        Returns:
            None
        """
        GetDllLibDoc().SdtComboBox_CreateSdtComboBox.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().SdtComboBox_CreateSdtComboBox,)
        super(SdtComboBox, self).__init__(intPtr)

    @property

    def Type(self)->'SdtType':
        """
        Gets the type of the structured document tag (SDT), which is specified as a ComboBox.
        """
        GetDllLibDoc().SdtComboBox_get_Type.argtypes=[c_void_p]
        GetDllLibDoc().SdtComboBox_get_Type.restype=c_int
        ret = CallCFunction(GetDllLibDoc().SdtComboBox_get_Type,self.Ptr)
        objwraped = SdtType(ret)
        return objwraped

