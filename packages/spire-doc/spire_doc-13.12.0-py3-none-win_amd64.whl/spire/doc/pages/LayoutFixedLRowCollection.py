from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc.pages import *
from spire.doc import *
from ctypes import *
import abc

class LayoutFixedLRowCollection (LayoutCollection) :
    """
    Represents a generic collection of layout entity types.
    """
    @property

    def First(self)->'FixedLayoutRow':
        """
        Returns the first entity in the collection.
        """
        GetDllLibDoc().LayoutFixedLRowCollection_get_First.argtypes=[c_void_p]
        GetDllLibDoc().LayoutFixedLRowCollection_get_First.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().LayoutFixedLRowCollection_get_First,self.Ptr)
        ret = None if intPtr==None else FixedLayoutRow(intPtr)
        return ret



    @property

    def Last(self)->'FixedLayoutRow':
        """
        Returns the last entity in the collection.
        """
        GetDllLibDoc().LayoutFixedLRowCollection_get_Last.argtypes=[c_void_p]
        GetDllLibDoc().LayoutFixedLRowCollection_get_Last.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().LayoutFixedLRowCollection_get_Last,self.Ptr)
        ret = None if intPtr==None else FixedLayoutRow(intPtr)
        return ret




    def get_Item(self ,index:int)->'FixedLayoutRow':
        """
        Retrieves the entity at the given index. 
        """
        
        GetDllLibDoc().LayoutFixedLRowCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibDoc().LayoutFixedLRowCollection_get_Item.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().LayoutFixedLRowCollection_get_Item,self.Ptr, index)
        ret = None if intPtr==None else FixedLayoutRow(intPtr)
        return ret

    def IndexOf(self ,entity:'FixedLayoutRow')->int:
        """
        Returns the zero-based index of the specified entity.
        """
        intPtrentity:c_void_p = entity.Ptr

        GetDllLibDoc().LayoutFixedLRowCollection_IndexOf.argtypes=[c_void_p ,c_void_p]
        GetDllLibDoc().LayoutFixedLRowCollection_IndexOf.restype=c_int
        ret = CallCFunction(GetDllLibDoc().LayoutFixedLRowCollection_IndexOf,self.Ptr, intPtrentity)
        return ret

    @property
    def Count(self)->int:
        """
        Gets the number of entities in the collection.
        """
        GetDllLibDoc().LayoutFixedLRowCollection_get_Count.argtypes=[c_void_p]
        GetDllLibDoc().LayoutFixedLRowCollection_get_Count.restype=c_int
        ret = CallCFunction(GetDllLibDoc().LayoutFixedLRowCollection_get_Count,self.Ptr)
        return ret

