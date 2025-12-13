from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class ShapeAdjustHandles (SpireObject) :
    """
    This class contains methods for adjusting the preset geometric shapes.
    The user interface can be made to transform only certain parts of the shape
    by using the special points (can alse be called adjust handles), similar
    functionality can be implemented using this class. 
    """
    def GetRoundRectangleCornerRadius(self)->float:
        """
        Gets the corner radius of the round rectangle shape.
        """
        GetDllLibDoc().ShapeAdjustHandles_GetRoundRectangleCornerRadius.argtypes=[c_void_p]
        GetDllLibDoc().ShapeAdjustHandles_GetRoundRectangleCornerRadius.restype=c_double
        ret = CallCFunction(GetDllLibDoc().ShapeAdjustHandles_GetRoundRectangleCornerRadius,self.Ptr)
        return ret


    def AdjustRoundRectangle(self ,cornerRadius:float):
        """
        Adjusts the corner radius of the round rectangle shape.
        The maximum corner radius is half the smaller dimension
        of the length and width of the rectangle.
        """
        
        GetDllLibDoc().ShapeAdjustHandles_AdjustRoundRectangle.argtypes=[c_void_p ,c_double]
        CallCFunction(GetDllLibDoc().ShapeAdjustHandles_AdjustRoundRectangle,self.Ptr, cornerRadius)

