from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc.pages import *
from spire.doc import *
from ctypes import *
import abc

class BodyLayoutElement (  LayoutElement) :
    """
    Describes an object that includes both lines and rows.
    """
    @property

    def Lines(self)->'LayoutFixedLLineCollection':
        """
        Gives the ability to retrieve the individual lines comprising a body.
        """
        GetDllLibDoc().BodyLayoutElement_get_Lines.argtypes=[c_void_p]
        GetDllLibDoc().BodyLayoutElement_get_Lines.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().BodyLayoutElement_get_Lines,self.Ptr)
        from spire.doc.pages.LayoutFixedLLineCollection import LayoutFixedLLineCollection
        ret = None if intPtr==None else LayoutFixedLLineCollection(intPtr)
        return ret



    @property

    def Rows(self)->'LayoutFixedLRowCollection':
        """
        Gives the capability to access the rows contained within a table.
        """
        GetDllLibDoc().BodyLayoutElement_get_Rows.argtypes=[c_void_p]
        GetDllLibDoc().BodyLayoutElement_get_Rows.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().BodyLayoutElement_get_Rows,self.Ptr)
        from spire.doc.pages.LayoutFixedLRowCollection import LayoutFixedLRowCollection
        ret = None if intPtr==None else LayoutFixedLRowCollection(intPtr)
        return ret



