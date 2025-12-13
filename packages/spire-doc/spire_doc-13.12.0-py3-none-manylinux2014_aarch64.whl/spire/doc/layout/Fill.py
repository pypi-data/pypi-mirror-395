from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class Fill (SpireObject) :
    """
    Represents a class for filling data.
    """
    @property

    def Color(self)->'Color':
        """
        Gets or sets the color.
        """
        GetDllLibDoc().Fill_get_Color.argtypes=[c_void_p]
        GetDllLibDoc().Fill_get_Color.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().Fill_get_Color,self.Ptr)
        ret = None if intPtr==None else Color(intPtr)
        return ret


    @Color.setter
    def Color(self, value:'Color'):
        GetDllLibDoc().Fill_set_Color.argtypes=[c_void_p, c_void_p]
        CallCFunction(GetDllLibDoc().Fill_set_Color,self.Ptr, value.Ptr)

    @property
    def Opacity(self)->float:
        """
        Gets or sets the opacity of the element.
        """
        GetDllLibDoc().Fill_get_Opacity.argtypes=[c_void_p]
        GetDllLibDoc().Fill_get_Opacity.restype=c_double
        ret = CallCFunction(GetDllLibDoc().Fill_get_Opacity,self.Ptr)
        return ret

    @Opacity.setter
    def Opacity(self, value:float):
        GetDllLibDoc().Fill_set_Opacity.argtypes=[c_void_p, c_double]
        CallCFunction(GetDllLibDoc().Fill_set_Opacity,self.Ptr, value)

    @property
    def On(self)->bool:
        """
        Gets or sets a value indicating whether the Fill is currently on.
        """
        GetDllLibDoc().Fill_get_On.argtypes=[c_void_p]
        GetDllLibDoc().Fill_get_On.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().Fill_get_On,self.Ptr)
        return ret

    @On.setter
    def On(self, value:bool):
        GetDllLibDoc().Fill_set_On.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().Fill_set_On,self.Ptr, value)

#    @property
#
#    def ImageBytes(self)->List['Byte']:
#        """
#
#        """
#        GetDllLibDoc().Fill_get_ImageBytes.argtypes=[c_void_p]
#        GetDllLibDoc().Fill_get_ImageBytes.restype=IntPtrArray
#        intPtrArray = CallCFunction(GetDllLibDoc().Fill_get_ImageBytes,self.Ptr)
#        ret = GetVectorFromArray(intPtrArray, Byte)
#        return ret


    @dispatch
    def Solid(self):
        """

        """
        GetDllLibDoc().Fill_Solid.argtypes=[c_void_p]
        CallCFunction(GetDllLibDoc().Fill_Solid,self.Ptr)

    @dispatch

    def Solid(self ,color:'Color'):
        """

        """
        intPtrcolor:c_void_p = color.Ptr

        GetDllLibDoc().Fill_SolidC.argtypes=[c_void_p ,c_void_p]
        CallCFunction(GetDllLibDoc().Fill_SolidC,self.Ptr, intPtrcolor)

