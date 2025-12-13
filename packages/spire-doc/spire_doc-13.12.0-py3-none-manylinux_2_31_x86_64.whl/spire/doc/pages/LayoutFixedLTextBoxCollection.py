from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc.pages import *
from spire.doc import *
from ctypes import *
import abc

class LayoutFixedLTextBoxCollection ( LayoutCollection) :
    """
    Represents a generic collection of layout entity types.
    """
    @property

    def First(self)->'FixedLayoutTextBox':
        """
        Returns the first entity in the collection.
        """
        GetDllLibDoc().LayoutFixedLTextBoxCollection_get_First.argtypes=[c_void_p]
        GetDllLibDoc().LayoutFixedLTextBoxCollection_get_First.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().LayoutFixedLTextBoxCollection_get_First,self.Ptr)
        ret = None if intPtr==None else FixedLayoutTextBox(intPtr)
        return ret



    @property

    def Last(self)->'FixedLayoutTextBox':
        """
        Returns the last entity in the collection.
        """
        GetDllLibDoc().LayoutFixedLTextBoxCollection_get_Last.argtypes=[c_void_p]
        GetDllLibDoc().LayoutFixedLTextBoxCollection_get_Last.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().LayoutFixedLTextBoxCollection_get_Last,self.Ptr)
        ret = None if intPtr==None else FixedLayoutTextBox(intPtr)
        return ret




    def get_Item(self ,index:int)->'FixedLayoutTextBox':
        """
        Retrieves the entity at the given index. 
        """
        
        GetDllLibDoc().LayoutFixedLTextBoxCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibDoc().LayoutFixedLTextBoxCollection_get_Item.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().LayoutFixedLTextBoxCollection_get_Item,self.Ptr, index)
        ret = None if intPtr==None else FixedLayoutTextBox(intPtr)
        return ret

    def IndexOf(self ,entity:'FixedLayoutTextBox')->int:
        """
        Returns the zero-based index of the specified entity.
        """
        intPtrentity:c_void_p = entity.Ptr

        GetDllLibDoc().LayoutFixedLTextBoxCollection_IndexOf.argtypes=[c_void_p ,c_void_p]
        GetDllLibDoc().LayoutFixedLTextBoxCollection_IndexOf.restype=c_int
        ret = CallCFunction(GetDllLibDoc().LayoutFixedLTextBoxCollection_IndexOf,self.Ptr, intPtrentity)
        return ret

    @property
    def Count(self)->int:
        """
        Gets the number of entities in the collection.
        """
        GetDllLibDoc().LayoutFixedLTextBoxCollection_get_Count.argtypes=[c_void_p]
        GetDllLibDoc().LayoutFixedLTextBoxCollection_get_Count.restype=c_int
        ret = CallCFunction(GetDllLibDoc().LayoutFixedLTextBoxCollection_get_Count,self.Ptr)
        return ret

