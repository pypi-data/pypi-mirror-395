from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class Frame ( OwnerHolder) :
    """
    Represents Frame object used in framed document.
    """
    @property
    def FrameAnchorLock(self)->bool:
        """
        Gets whether lock the anchor of Frame or not.
        """
        GetDllLibDoc().Frame_get_FrameAnchorLock.argtypes=[c_void_p]
        GetDllLibDoc().Frame_get_FrameAnchorLock.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().Frame_get_FrameAnchorLock,self.Ptr)
        return ret

    @FrameAnchorLock.setter
    def FrameAnchorLock(self, value:bool):
        """
        Sets whether lock the anchor of Frame or not.
        """
        GetDllLibDoc().Frame_set_FrameAnchorLock.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().Frame_set_FrameAnchorLock,self.Ptr, value)

    @property

    def FrameHorizontalAlignment(self)->'HorizontalPosition':
        """
        Gets Horizontal Alignment of Frame.
        """
        GetDllLibDoc().Frame_get_FrameHorizontalAlignment.argtypes=[c_void_p]
        GetDllLibDoc().Frame_get_FrameHorizontalAlignment.restype=c_int
        ret = CallCFunction(GetDllLibDoc().Frame_get_FrameHorizontalAlignment,self.Ptr)
        objwraped = HorizontalAlignment(ret)
        return objwraped

    @FrameHorizontalAlignment.setter
    def FrameHorizontalAlignment(self, value:'HorizontalPosition'):
        """
        Sets Horizontal Alignment of Frame.
        """
        GetDllLibDoc().Frame_set_FrameHorizontalAlignment.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().Frame_set_FrameHorizontalAlignment,self.Ptr, value.value)

    @property

    def FrameVerticalAlignment(self)->'VerticalPosition':
        """
        Gets Vertical Alignment of Frame.
        """
        GetDllLibDoc().Frame_get_FrameVerticalAlignment.argtypes=[c_void_p]
        GetDllLibDoc().Frame_get_FrameVerticalAlignment.restype=c_int
        ret = CallCFunction(GetDllLibDoc().Frame_get_FrameVerticalAlignment,self.Ptr)
        objwraped = VerticalAlignment(ret)
        return objwraped

    @FrameVerticalAlignment.setter
    def FrameVerticalAlignment(self, value:'VerticalPosition'):
        """
        Sets Vertical Alignment of Frame.
        """
        GetDllLibDoc().Frame_set_FrameVerticalAlignment.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().Frame_set_FrameVerticalAlignment,self.Ptr, value.value)



    @property
    def FrameHorizontalPosition(self)->float:
        """
        Gets Horizontal Position of Frame.
        """
        GetDllLibDoc().Frame_get_FrameHorizontalPosition.argtypes=[c_void_p]
        GetDllLibDoc().Frame_get_FrameHorizontalPosition.restype=c_int
        ret = CallCFunction(GetDllLibDoc().Frame_get_FrameHorizontalPosition,self.Ptr)
        return ret

    @FrameHorizontalPosition.setter
    def FrameHorizontalPosition(self, value:float):
        """
        Sets Horizontal Position of Frame.
        """
        GetDllLibDoc().Frame_set_FrameHorizontalPosition.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().Frame_set_FrameHorizontalPosition,self.Ptr, value)

    @property
    def FrameVerticalPosition(self)->float:
        """
        Gets Vertical Position of Frame.
        """
        GetDllLibDoc().Frame_get_FrameVerticalPosition.argtypes=[c_void_p]
        GetDllLibDoc().Frame_get_FrameVerticalPosition.restype=c_int
        ret = CallCFunction(GetDllLibDoc().Frame_get_FrameVerticalPosition,self.Ptr)
        return ret

    @FrameVerticalPosition.setter
    def FrameVerticalPosition(self, value:float):
        """
        Sets Vertical Position of Frame.
        """
        GetDllLibDoc().Frame_set_FrameVerticalPosition.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().Frame_set_FrameVerticalPosition,self.Ptr, value)
    @property

    def FrameWidthRule(self)->'FrameSizeRule':
        """
        Gets Width Rule of Frame.
        """
        GetDllLibDoc().Frame_get_FrameWidthRule.argtypes=[c_void_p]
        GetDllLibDoc().Frame_get_FrameWidthRule.restype=c_int
        ret = CallCFunction(GetDllLibDoc().Frame_get_FrameWidthRule,self.Ptr)
        objwraped = FrameSizeRule(ret)
        return objwraped

    @FrameWidthRule.setter
    def FrameWidthRule(self, value:'FrameSizeRule'):
        """
        Sets Width Rule of Frame.
        """
        GetDllLibDoc().Frame_set_FrameWidthRule.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().Frame_set_FrameWidthRule,self.Ptr, value.value)

    @property

    def FrameHeightRule(self)->'FrameSizeRule':
        """
        Gets Height Rule of Frame.
        """
        GetDllLibDoc().Frame_get_FrameHeightRule.argtypes=[c_void_p]
        GetDllLibDoc().Frame_get_FrameHeightRule.restype=c_int
        ret = CallCFunction(GetDllLibDoc().Frame_get_FrameHeightRule,self.Ptr)
        objwraped = FrameSizeRule(ret)
        return objwraped

    @FrameHeightRule.setter
    def FrameHeightRule(self, value:'FrameSizeRule'):
        """
        Sets Height Rule of Frame.
        """
        GetDllLibDoc().Frame_set_FrameHeightRule.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().Frame_set_FrameHeightRule,self.Ptr, value.value)

    @property
    def WrapFrameAround(self)->bool:
        """
        Gets wrap type of Frame.
        """
        GetDllLibDoc().Frame_get_WrapFrameAround.argtypes=[c_void_p]
        GetDllLibDoc().Frame_get_WrapFrameAround.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().Frame_get_WrapFrameAround,self.Ptr)
        return ret

    @WrapFrameAround.setter
    def WrapFrameAround(self, value:bool):
        """
        Sets wrap type of Frame.
        """
        GetDllLibDoc().Frame_set_WrapFrameAround.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().Frame_set_WrapFrameAround,self.Ptr, value)

    @property

    def FrameHorizontalOrigin(self)->'FrameHorzAnchor':
        """
        Gets relative to what the frame is positioned horizontally.
        """
        GetDllLibDoc().Frame_get_FrameHorizontalOrigin.argtypes=[c_void_p]
        GetDllLibDoc().Frame_get_FrameHorizontalOrigin.restype=c_int
        ret = CallCFunction(GetDllLibDoc().Frame_get_FrameHorizontalOrigin,self.Ptr)
        objwraped = FrameHorzAnchor(ret)
        return objwraped

    @FrameHorizontalOrigin.setter
    def FrameHorizontalOrigin(self, value:'FrameHorzAnchor'):
        """
        Sets relative to what the frame is positioned horizontally.
        """
        GetDllLibDoc().Frame_set_FrameHorizontalOrigin.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().Frame_set_FrameHorizontalOrigin,self.Ptr, value.value)

    @property
    def FrameVerticalOrigin(self) -> 'FrameVertAnchor':
        """
        Gets relative to what the frame is positioned vertically.
        """
        GetDllLibDoc().Frame_get_FrameVerticalOrigin.argtypes=[c_void_p]
        GetDllLibDoc().Frame_get_FrameVerticalOrigin.restype=c_int
        ret = CallCFunction(GetDllLibDoc().Frame_get_FrameVerticalOrigin,self.Ptr)
        objwraped = FrameVertAnchor(ret)
        return objwraped

    @FrameVerticalOrigin.setter
    def FrameVerticalOrigin(self, value:'FrameVertAnchor'):
        """
        Sets relative to what the frame is positioned vertically.
        """
        GetDllLibDoc().Frame_set_FrameVerticalOrigin.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().Frame_set_FrameVerticalOrigin,self.Ptr, value.value)

    def GetWidth(self)->float:
        """
        Gets width of this frame
        """
        GetDllLibDoc().Frame_GetWidth.argtypes=[c_void_p]
        GetDllLibDoc().Frame_GetWidth.restype=c_float
        ret = CallCFunction(GetDllLibDoc().Frame_GetWidth,self.Ptr)
        return ret


    def SetWidth(self ,value:float):
        """
        Sets width of this frame
        """
        
        GetDllLibDoc().Frame_SetWidth.argtypes=[c_void_p ,c_float]
        CallCFunction(GetDllLibDoc().Frame_SetWidth,self.Ptr, value)

    def GetHeight(self)->float:
        """
        Gets height of this frame
        """
        GetDllLibDoc().Frame_GetHeight.argtypes=[c_void_p]
        GetDllLibDoc().Frame_GetHeight.restype=c_float
        ret = CallCFunction(GetDllLibDoc().Frame_GetHeight,self.Ptr)
        return ret


    def SetHeight(self ,value:float):
        """
        Sets height of this frame
        """
        
        GetDllLibDoc().Frame_SetHeight.argtypes=[c_void_p ,c_float]
        CallCFunction(GetDllLibDoc().Frame_SetHeight,self.Ptr, value)

    def GetHorizontalPosition(self)->float:
        """
        Gets the position of the left edge of the frame
        """
        GetDllLibDoc().Frame_GetHorizontalPosition.argtypes=[c_void_p]
        GetDllLibDoc().Frame_GetHorizontalPosition.restype=c_float
        ret = CallCFunction(GetDllLibDoc().Frame_GetHorizontalPosition,self.Ptr)
        return ret


    def SetHorizontalPosition(self ,value:float):
        """
        Sets the position of the left edge of the frame
        """
        
        GetDllLibDoc().Frame_SetHorizontalPosition.argtypes=[c_void_p ,c_float]
        CallCFunction(GetDllLibDoc().Frame_SetHorizontalPosition,self.Ptr, value)

    def GetHorizontalDistanceFromText(self)->float:
        """
        Gets the distance between the document text and left or right edge of the frame.
        """
        GetDllLibDoc().Frame_GetHorizontalDistanceFromText.argtypes=[c_void_p]
        GetDllLibDoc().Frame_GetHorizontalDistanceFromText.restype=c_float
        ret = CallCFunction(GetDllLibDoc().Frame_GetHorizontalDistanceFromText,self.Ptr)
        return ret


    def SetHorizontalDistanceFromText(self ,value:float):
        """
        Sets the distance between the document text and left or right edge of the frame.
        """
        
        GetDllLibDoc().Frame_SetHorizontalDistanceFromText.argtypes=[c_void_p ,c_float]
        CallCFunction(GetDllLibDoc().Frame_SetHorizontalDistanceFromText,self.Ptr, value)

    def GetVerticalPosition(self)->float:
        """
        Gets the position of the top edge of the frame
        """
        GetDllLibDoc().Frame_GetVerticalPosition.argtypes=[c_void_p]
        GetDllLibDoc().Frame_GetVerticalPosition.restype=c_float
        ret = CallCFunction(GetDllLibDoc().Frame_GetVerticalPosition,self.Ptr)
        return ret


    def SetVerticalPosition(self ,value:float):
        """
        Sets the position of the top edge of the frame
        """
        
        GetDllLibDoc().Frame_SetVerticalPosition.argtypes=[c_void_p ,c_float]
        CallCFunction(GetDllLibDoc().Frame_SetVerticalPosition,self.Ptr, value)

    def GetVerticalDistanceFromText(self)->float:
        """
        Gets the distance between the document text and top or bottom edge of the frame.
        """
        GetDllLibDoc().Frame_GetVerticalDistanceFromText.argtypes=[c_void_p]
        GetDllLibDoc().Frame_GetVerticalDistanceFromText.restype=c_float
        ret = CallCFunction(GetDllLibDoc().Frame_GetVerticalDistanceFromText,self.Ptr)
        return ret


    def SetVerticalDistanceFromText(self ,value:float):
        """
        Sets the distance between the document text and top or bottom edge of the frame.
        """
        
        GetDllLibDoc().Frame_SetVerticalDistanceFromText.argtypes=[c_void_p ,c_float]
        CallCFunction(GetDllLibDoc().Frame_SetVerticalDistanceFromText,self.Ptr, value)

    @property
    def IsFrame(self)->bool:
        """
        Gets a value indicating whether this instance is frame.
        """
        GetDllLibDoc().Frame_get_IsFrame.argtypes=[c_void_p]
        GetDllLibDoc().Frame_get_IsFrame.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().Frame_get_IsFrame,self.Ptr)
        return ret