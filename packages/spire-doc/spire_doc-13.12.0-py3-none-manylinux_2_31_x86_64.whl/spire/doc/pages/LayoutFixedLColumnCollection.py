from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc.pages import *
from spire.doc import *
from ctypes import *
import abc

class LayoutFixedLColumnCollection ( LayoutCollection) :
    """
    Represents a generic collection of layout entity types.
    """
    @property

    def First(self)->'FixedLayoutColumn':
        """
        Returns the first entity in the collection.
        """
        GetDllLibDoc().LayoutFixedLColumnCollection_get_First.argtypes=[c_void_p]
        GetDllLibDoc().LayoutFixedLColumnCollection_get_First.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().LayoutFixedLColumnCollection_get_First,self.Ptr)
        ret = None if intPtr==None else FixedLayoutColumn(intPtr)
        return ret



    @property

    def Last(self)->'FixedLayoutColumn':
        """
        Returns the last entity in the collection.
        """
        GetDllLibDoc().LayoutFixedLColumnCollection_get_Last.argtypes=[c_void_p]
        GetDllLibDoc().LayoutFixedLColumnCollection_get_Last.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().LayoutFixedLColumnCollection_get_Last,self.Ptr)
        ret = None if intPtr==None else FixedLayoutColumn(intPtr)
        return ret

    def IndexOf(self ,entity:'FixedLayoutColumn')->int:
        """
        Returns the zero-based index of the specified entity.

        Args:
            entity(IDocumentObject): The document object.

        """
        intPtrentity:c_void_p = entity.Ptr

        GetDllLibDoc().LayoutFixedLColumnCollection_IndexOf.argtypes=[c_void_p ,c_void_p]
        GetDllLibDoc().LayoutFixedLColumnCollection_IndexOf.restype=c_int
        ret = CallCFunction(GetDllLibDoc().LayoutFixedLColumnCollection_IndexOf,self.Ptr, intPtrentity)
        return ret
    
    def get_Item(self ,index:int)->'FixedLayoutColumn':
        """
        Retrieves the entity at the given index. 
        """
        
        GetDllLibDoc().LayoutFixedLColumnCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibDoc().LayoutFixedLColumnCollection_get_Item.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().LayoutFixedLColumnCollection_get_Item,self.Ptr, index)
        ret = None if intPtr==None else FixedLayoutColumn(intPtr)
        return ret



    @property
    def Count(self)->int:
        """
        Gets the number of entities in the collection.
        """
        GetDllLibDoc().LayoutFixedLColumnCollection_get_Count.argtypes=[c_void_p]
        GetDllLibDoc().LayoutFixedLColumnCollection_get_Count.restype=c_int
        ret = CallCFunction(GetDllLibDoc().LayoutFixedLColumnCollection_get_Count,self.Ptr)
        return ret

