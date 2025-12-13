from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class ChartAxisTitle (SpireObject) :
    """
    Represents the title of an axis in a chart.
    """
    @property
    def Show(self)->bool:
        """
        Gets or sets a value indicating whether the title is visible.
        """
        GetDllLibDoc().ChartAxisTitle_get_Show.argtypes=[c_void_p]
        GetDllLibDoc().ChartAxisTitle_get_Show.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().ChartAxisTitle_get_Show,self.Ptr)
        return ret

    @Show.setter
    def Show(self, value:bool):
        GetDllLibDoc().ChartAxisTitle_set_Show.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().ChartAxisTitle_set_Show,self.Ptr, value)

    @property

    def Text(self)->str:
        """
        Gets or sets the text of the axis title.
        """
        GetDllLibDoc().ChartAxisTitle_get_Text.argtypes=[c_void_p]
        GetDllLibDoc().ChartAxisTitle_get_Text.restype=c_void_p
        ret = PtrToStr(CallCFunction(GetDllLibDoc().ChartAxisTitle_get_Text,self.Ptr))
        return ret


    @Text.setter
    def Text(self, value:str):
        valuePtr=StrToPtr(value)
        GetDllLibDoc().ChartAxisTitle_set_Text.argtypes=[c_void_p, c_char_p]
        CallCFunction(GetDllLibDoc().ChartAxisTitle_set_Text,self.Ptr, valuePtr)

    @property
    def Overlay(self)->bool:
        """
        Gets or sets a value indicating whether the title is overlaid on the chart.

        true if the title is overlaid; otherwise, false.
        """
        GetDllLibDoc().ChartAxisTitle_get_Overlay.argtypes=[c_void_p]
        GetDllLibDoc().ChartAxisTitle_get_Overlay.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().ChartAxisTitle_get_Overlay,self.Ptr)
        return ret

    @Overlay.setter
    def Overlay(self, value:bool):
        GetDllLibDoc().ChartAxisTitle_set_Overlay.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().ChartAxisTitle_set_Overlay,self.Ptr, value)


    def GetCharacterFormat(self)->'CharacterFormat':
        """
        Gets the font format used for the axis title.

        returns:
            The font of the axis title.
        """
        GetDllLibDoc().ChartAxisTitle_GetCharacterFormat.argtypes=[c_void_p]
        GetDllLibDoc().ChartAxisTitle_GetCharacterFormat.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ChartAxisTitle_GetCharacterFormat,self.Ptr)
        from spire.doc.formatting.CharacterFormat import CharacterFormat
        ret = None if intPtr==None else CharacterFormat(intPtr)
        return ret


