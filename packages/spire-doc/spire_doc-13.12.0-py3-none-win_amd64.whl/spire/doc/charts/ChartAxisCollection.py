from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class ChartAxisCollection (  IEnumerable) :
    """

    """

    def get_Item(self ,index:int)->'ChartAxis':
        """

        """
        
        GetDllLibDoc().ChartAxisCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibDoc().ChartAxisCollection_get_Item.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ChartAxisCollection_get_Item,self.Ptr, index)
        from spire.doc.charts.ChartAxis import ChartAxis
        ret = None if intPtr==None else ChartAxis(intPtr)
        return ret


    @property
    def Count(self)->int:
        """

        """
        GetDllLibDoc().ChartAxisCollection_get_Count.argtypes=[c_void_p]
        GetDllLibDoc().ChartAxisCollection_get_Count.restype=c_int
        ret = CallCFunction(GetDllLibDoc().ChartAxisCollection_get_Count,self.Ptr)
        return ret


    def GetEnumerator(self)->'IEnumerator':
        """

        """
        GetDllLibDoc().ChartAxisCollection_GetEnumerator.argtypes=[c_void_p]
        GetDllLibDoc().ChartAxisCollection_GetEnumerator.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ChartAxisCollection_GetEnumerator,self.Ptr)
        ret = None if intPtr==None else IEnumerator(intPtr)
        return ret


