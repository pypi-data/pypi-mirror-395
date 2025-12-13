from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class DocumentSerializableCollection (  CollectionEx, IXDLSSerializableCollection) :
    """
    Represents a collection of serializable documents.
    """
    @property

    def TagItemName(self)->str:
        """
        Gets the name of the xml item.
        """
        GetDllLibDoc().DocumentSerializableCollection_get_TagItemName.argtypes=[c_void_p]
        GetDllLibDoc().DocumentSerializableCollection_get_TagItemName.restype=c_void_p
        ret = PtrToStr(CallCFunction(GetDllLibDoc().DocumentSerializableCollection_get_TagItemName,self.Ptr))
        return ret


