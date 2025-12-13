from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class SdtDataBinding (SpireObject) :
    """
    Specifies the information which shall be used to Eschertablish a mapping between the parent
    structured document tag and an XML element stored within a Custom XML Data part in the current
    WordprocessingML document.
    """
    def Delete(self):
        """
        Deletes mapping to XML data.
        """
        GetDllLibDoc().SdtDataBinding_Delete.argtypes=[c_void_p]
        CallCFunction(GetDllLibDoc().SdtDataBinding_Delete,self.Ptr)

