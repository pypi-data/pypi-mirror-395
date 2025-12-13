from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class Shading (  InternalComplexAttribute) :
    """
    Represents a collection of Shading values for a document element.
    """
    def ClearFormatting(self):
        """
        Removes shading from the object.
        """
        GetDllLibDoc().Shading_ClearFormatting.argtypes=[c_void_p]
        CallCFunction(GetDllLibDoc().Shading_ClearFormatting,self.Ptr)


    def Equals(self ,obj:'SpireObject')->bool:
        """
        Determines whether the specified <see cref="System.Object" />, is equal to this instance.
        """
        intPtrobj:c_void_p = obj.Ptr

        GetDllLibDoc().Shading_Equals.argtypes=[c_void_p ,c_void_p]
        GetDllLibDoc().Shading_Equals.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().Shading_Equals,self.Ptr, intPtrobj)
        return ret

    def GetHashCode(self)->int:
        """
        Returns a hash code for this instance.
        """
        GetDllLibDoc().Shading_GetHashCode.argtypes=[c_void_p]
        GetDllLibDoc().Shading_GetHashCode.restype=c_int
        ret = CallCFunction(GetDllLibDoc().Shading_GetHashCode,self.Ptr)
        return ret

    @property

    def BackgroundPatternColor(self)->'Color':
        """
        Gets or sets the BackgroundPatternColor.
        """
        GetDllLibDoc().Shading_get_BackgroundPatternColor.argtypes=[c_void_p]
        GetDllLibDoc().Shading_get_BackgroundPatternColor.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().Shading_get_BackgroundPatternColor,self.Ptr)
        ret = None if intPtr==None else Color(intPtr)
        return ret

    @BackgroundPatternColor.setter
    def BackgroundPatternColor(self, value:'Color'):
        """
        Sets the BackgroundPatternColor.
        """
        GetDllLibDoc().Shading_set_BackgroundPatternColor.argtypes=[c_void_p, c_void_p]
        CallCFunction(GetDllLibDoc().Shading_set_BackgroundPatternColor, self.Ptr, value.Ptr)

    @property
    def ForegroundPatternColor(self)->'Color':
        """
        Gets or sets the ForegroundPatternColor.
        """
        GetDllLibDoc().Shading_get_ForegroundPatternColor.argtypes=[c_void_p]
        GetDllLibDoc().Shading_get_ForegroundPatternColor.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().Shading_get_ForegroundPatternColor,self.Ptr)
        ret = None if intPtr==None else Color(intPtr)
        return ret

    @ForegroundPatternColor.setter
    def ForegroundPatternColor(self, value:'Color'):
        """
        Sets the ForegroundPatternColor.
        """
        GetDllLibDoc().Shading_set_ForegroundPatternColor.argtypes=[c_void_p, c_void_p]
        CallCFunction(GetDllLibDoc().Shading_set_ForegroundPatternColor,self.Ptr, value.Ptr)

    @property
    def TextureStyle(self) -> 'TextureStyle':
        """
        Gets or sets TextureStyle.
        """
        GetDllLibDoc().Shading_get_TextureStyle.argtypes=[c_void_p]
        GetDllLibDoc().Shading_get_TextureStyle.restype=c_int
        ret = CallCFunction(GetDllLibDoc().Shading_get_TextureStyle,self.Ptr)
        objwraped = TextureStyle(ret)
        return objwraped

    @TextureStyle.setter
    def TextureStyle(self, value:'TextureStyle'):
        GetDllLibDoc().Shading_set_TextureStyle.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().Shading_set_TextureStyle,self.Ptr, value.value)

