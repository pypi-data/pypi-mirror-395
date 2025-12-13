from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class Borders (  DocumentSerializable, IEnumerable) :
    """
    Represents a collection of four borders. <see cref="!:Spire.Doc.Border" />
    """
    def ClearFormatting(self):
        """
        Clears formatting for each border in the borders.
        """
        GetDllLibDoc().Borders_ClearFormatting.argtypes=[c_void_p]
        CallCFunction(GetDllLibDoc().Borders_ClearFormatting,self.Ptr)


    def GetEnumerator(self)->'IEnumerator':
        """
        Returns an enumerator that iterates through a borders.
        """
        GetDllLibDoc().Borders_GetEnumerator.argtypes=[c_void_p]
        GetDllLibDoc().Borders_GetEnumerator.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().Borders_GetEnumerator,self.Ptr)
        ret = None if intPtr==None else IEnumerator(intPtr)
        return ret



    def SetBordersAttribute(self ,borderType:'BorderStyle',lineWidth:float,color:'Color'):
        """
        Sets the border attributes for the specified border type, line width, and color.
        
        Args:
            borderType: The type of border to set
            lineWidth: The width of the border line
            color: The color of the border
        """
        enumborderType:c_int = borderType.value
        intPtrcolor:c_void_p = color.Ptr

        GetDllLibDoc().Borders_SetBordersAttribute.argtypes=[c_void_p ,c_int,c_float,c_void_p]
        CallCFunction(GetDllLibDoc().Borders_SetBordersAttribute,self.Ptr, enumborderType,lineWidth,intPtrcolor)

    @dispatch

    def get_Item(self ,borderPos:BorderPositions)->Border:
        """

        """
        enumborderPos:c_int = borderPos.value

        GetDllLibDoc().Borders_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibDoc().Borders_get_Item.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().Borders_get_Item,self.Ptr, enumborderPos)
        ret = None if intPtr==None else Border(intPtr)
        return ret


    @dispatch

    def get_Item(self ,index:int)->Border:
        """

        """
        
        GetDllLibDoc().Borders_get_ItemI.argtypes=[c_void_p ,c_int]
        GetDllLibDoc().Borders_get_ItemI.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().Borders_get_ItemI,self.Ptr, index)
        ret = None if intPtr==None else Border(intPtr)
        return ret


    @property

    def Left(self)->'Border':
        """
		Gets left border.
        """
        GetDllLibDoc().Borders_get_Left.argtypes=[c_void_p]
        GetDllLibDoc().Borders_get_Left.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().Borders_get_Left,self.Ptr)
        ret = None if intPtr==None else Border(intPtr)
        return ret


    @property

    def Right(self)->'Border':
        """
		Gets right border.
        """
        GetDllLibDoc().Borders_get_Right.argtypes=[c_void_p]
        GetDllLibDoc().Borders_get_Right.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().Borders_get_Right,self.Ptr)
        ret = None if intPtr==None else Border(intPtr)
        return ret


    @property

    def Top(self)->'Border':
        """
		Gets top border.
        """
        GetDllLibDoc().Borders_get_Top.argtypes=[c_void_p]
        GetDllLibDoc().Borders_get_Top.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().Borders_get_Top,self.Ptr)
        ret = None if intPtr==None else Border(intPtr)
        return ret


    @property

    def Bottom(self)->'Border':
        """
		Gets bottom border.
        """
        GetDllLibDoc().Borders_get_Bottom.argtypes=[c_void_p]
        GetDllLibDoc().Borders_get_Bottom.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().Borders_get_Bottom,self.Ptr)
        ret = None if intPtr==None else Border(intPtr)
        return ret


    @property

    def Horizontal(self)->'Border':
        """
        Gets horizontal border.
        """
        GetDllLibDoc().Borders_get_Horizontal.argtypes=[c_void_p]
        GetDllLibDoc().Borders_get_Horizontal.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().Borders_get_Horizontal,self.Ptr)
        ret = None if intPtr==None else Border(intPtr)
        return ret


    @property

    def Vertical(self)->'Border':
        """
        Gets vertical border.
        """
        GetDllLibDoc().Borders_get_Vertical.argtypes=[c_void_p]
        GetDllLibDoc().Borders_get_Vertical.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().Borders_get_Vertical,self.Ptr)
        ret = None if intPtr==None else Border(intPtr)
        return ret


    @property

    def DiagonalUp(self)->'Border':
        """
        Gets diagonal border from bottom left corner to top right corner.
        """
        GetDllLibDoc().Borders_get_DiagonalUp.argtypes=[c_void_p]
        GetDllLibDoc().Borders_get_DiagonalUp.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().Borders_get_DiagonalUp,self.Ptr)
        ret = None if intPtr==None else Border(intPtr)
        return ret


    @property

    def DiagonalDown(self)->'Border':
        """
		Gets diagonal border from top left corner to bottom right corner.
        """
        GetDllLibDoc().Borders_get_DiagonalDown.argtypes=[c_void_p]
        GetDllLibDoc().Borders_get_DiagonalDown.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().Borders_get_DiagonalDown,self.Ptr)
        ret = None if intPtr==None else Border(intPtr)
        return ret


    @property
    def Count(self)->int:
        """
        Gets the total number of possible border positions available for this borders.
        """
        GetDllLibDoc().Borders_get_Count.argtypes=[c_void_p]
        GetDllLibDoc().Borders_get_Count.restype=c_int
        ret = CallCFunction(GetDllLibDoc().Borders_get_Count,self.Ptr)
        return ret

    @property
    def LineWidth(self)->float:
        """
        Gets or sets width of the borders.
        """
        GetDllLibDoc().Borders_get_LineWidth.argtypes=[c_void_p]
        GetDllLibDoc().Borders_get_LineWidth.restype=c_float
        ret = CallCFunction(GetDllLibDoc().Borders_get_LineWidth,self.Ptr)
        return ret

    @LineWidth.setter
    def LineWidth(self, value:float):
        GetDllLibDoc().Borders_set_LineWidth.argtypes=[c_void_p, c_float]
        CallCFunction(GetDllLibDoc().Borders_set_LineWidth,self.Ptr, value)

    @property

    def BorderType(self)->'BorderStyle':
        """
        Gets or Sets style of the borders.
        """
        GetDllLibDoc().Borders_get_BorderType.argtypes=[c_void_p]
        GetDllLibDoc().Borders_get_BorderType.restype=c_int
        ret = CallCFunction(GetDllLibDoc().Borders_get_BorderType,self.Ptr)
        objwraped = BorderStyle(ret)
        return objwraped

    @BorderType.setter
    def BorderType(self, value:'BorderStyle'):
        GetDllLibDoc().Borders_set_BorderType.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().Borders_set_BorderType,self.Ptr, value.value)

    @property

    def Color(self)->'Color':
        """
        Gets or sets color of the borders.
        """
        GetDllLibDoc().Borders_get_Color.argtypes=[c_void_p]
        GetDllLibDoc().Borders_get_Color.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().Borders_get_Color,self.Ptr)
        ret = None if intPtr==None else Color(intPtr)
        return ret


    @Color.setter
    def Color(self, value:'Color'):
        GetDllLibDoc().Borders_set_Color.argtypes=[c_void_p, c_void_p]
        CallCFunction(GetDllLibDoc().Borders_set_Color,self.Ptr, value.Ptr)

    @property
    def NoBorder(self)->bool:
        """
		Gets whether the border exists
        """
        GetDllLibDoc().Borders_get_NoBorder.argtypes=[c_void_p]
        GetDllLibDoc().Borders_get_NoBorder.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().Borders_get_NoBorder,self.Ptr)
        return ret

    @property
    def Space(self)->float:
        """
        Gets or sets the width of space to maintain between borders and text within borders.
        """
        GetDllLibDoc().Borders_get_Space.argtypes=[c_void_p]
        GetDllLibDoc().Borders_get_Space.restype=c_float
        ret = CallCFunction(GetDllLibDoc().Borders_get_Space,self.Ptr)
        return ret

    @Space.setter
    def Space(self, value:float):
        GetDllLibDoc().Borders_set_Space.argtypes=[c_void_p, c_float]
        CallCFunction(GetDllLibDoc().Borders_set_Space,self.Ptr, value)

    @property
    def IsShadow(self)->bool:
        """
        Gets or sets whether borders are drawn with shadow.
        """
        GetDllLibDoc().Borders_get_IsShadow.argtypes=[c_void_p]
        GetDllLibDoc().Borders_get_IsShadow.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().Borders_get_IsShadow,self.Ptr)
        return ret

    @IsShadow.setter
    def IsShadow(self, value:bool):
        GetDllLibDoc().Borders_set_IsShadow.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().Borders_set_IsShadow,self.Ptr, value)

