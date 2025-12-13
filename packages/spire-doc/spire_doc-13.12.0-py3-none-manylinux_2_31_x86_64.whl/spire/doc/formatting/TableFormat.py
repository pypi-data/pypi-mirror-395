from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class TableFormat (  WordAttributeBase) :
    """
    Represents the formatting of a row in a table.
    """
    @property
    def LayoutType(self)->'LayoutType':
        """
        Gets or sets the layout type of the row.
        """
        GetDllLibDoc().TableFormat_get_LayoutType.argtypes=[c_void_p]
        GetDllLibDoc().TableFormat_get_LayoutType.restype=c_int
        ret = CallCFunction(GetDllLibDoc().TableFormat_get_LayoutType,self.Ptr)
        objwraped = LayoutType(ret)
        return objwraped

    @LayoutType.setter
    def LayoutType(self, value:'LayoutType'):
        """
        Sets the layout type of the row.
        """
        GetDllLibDoc().TableFormat_set_LayoutType.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().TableFormat_set_LayoutType,self.Ptr, value.value)

    @property
    def Borders(self)->'Borders':
        """
        Gets the borders of the row.
        """
        GetDllLibDoc().TableFormat_get_Borders.argtypes=[c_void_p]
        GetDllLibDoc().TableFormat_get_Borders.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().TableFormat_get_Borders,self.Ptr)
        from spire.doc import Borders
        ret = None if intPtr==None else Borders(intPtr)
        return ret

    @property
    def Paddings(self)->'Paddings':
        """
        Gets the paddings of the row.
        """
        GetDllLibDoc().TableFormat_get_Paddings.argtypes=[c_void_p]
        GetDllLibDoc().TableFormat_get_Paddings.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().TableFormat_get_Paddings,self.Ptr)
        from spire.doc import Paddings
        ret = None if intPtr==None else Paddings(intPtr)
        return ret

    @property
    def CellSpacing(self)->float:
        """
        Gets or sets the spacing between cells in the row.
        The value must be between 0 pt and 264.5 pt.
        The value will not be applied if it is out of range.
        The property will be cleared if the value is less than 0.
        """
        GetDllLibDoc().TableFormat_get_CellSpacing.argtypes=[c_void_p]
        GetDllLibDoc().TableFormat_get_CellSpacing.restype=c_float
        ret = CallCFunction(GetDllLibDoc().TableFormat_get_CellSpacing,self.Ptr)
        return ret

    @CellSpacing.setter
    def CellSpacing(self, value:float):
        """
        Sets the spacing between cells in the row.
        """
        GetDllLibDoc().TableFormat_set_CellSpacing.argtypes=[c_void_p, c_float]
        CallCFunction(GetDllLibDoc().TableFormat_set_CellSpacing,self.Ptr, value)

    @property
    def LeftIndent(self)->float:
        """
        Gets or sets the left indent of the row.
        """
        GetDllLibDoc().TableFormat_get_LeftIndent.argtypes=[c_void_p]
        GetDllLibDoc().TableFormat_get_LeftIndent.restype=c_float
        ret = CallCFunction(GetDllLibDoc().TableFormat_get_LeftIndent,self.Ptr)
        return ret

    @LeftIndent.setter
    def LeftIndent(self, value:float):
        """
        Sets the left indent of the row.
        """
        GetDllLibDoc().TableFormat_set_LeftIndent.argtypes=[c_void_p, c_float]
        CallCFunction(GetDllLibDoc().TableFormat_set_LeftIndent,self.Ptr, value)

    @property
    def Bidi(self)->bool:
        """
        Gets or sets a value indicating whether the table is right to left.
        """
        GetDllLibDoc().TableFormat_get_Bidi.argtypes=[c_void_p]
        GetDllLibDoc().TableFormat_get_Bidi.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().TableFormat_get_Bidi,self.Ptr)
        return ret

    @Bidi.setter
    def Bidi(self, value:bool):
        """
        Sets a value indicating whether the table is right to left.
        """
        GetDllLibDoc().TableFormat_set_Bidi.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().TableFormat_set_Bidi,self.Ptr, value)

    @property
    def HorizontalAlignment(self)->'RowAlignment':
        """
        Gets or sets the horizontal alignment of the row.
        """
        GetDllLibDoc().TableFormat_get_HorizontalAlignment.argtypes=[c_void_p]
        GetDllLibDoc().TableFormat_get_HorizontalAlignment.restype=c_int
        ret = CallCFunction(GetDllLibDoc().TableFormat_get_HorizontalAlignment,self.Ptr)
        objwraped = RowAlignment(ret)
        return objwraped

    @HorizontalAlignment.setter
    def HorizontalAlignment(self, value:'RowAlignment'):
        """
        Sets the horizontal alignment of the row.
        """
        GetDllLibDoc().TableFormat_set_HorizontalAlignment.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().TableFormat_set_HorizontalAlignment,self.Ptr, value.value)

    @property
    def WrapTextAround(self)->bool:
        """
        Gets or sets a value indicating whether to wrap text around the row.
        """
        GetDllLibDoc().TableFormat_get_WrapTextAround.argtypes=[c_void_p]
        GetDllLibDoc().TableFormat_get_WrapTextAround.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().TableFormat_get_WrapTextAround,self.Ptr)
        return ret

    @WrapTextAround.setter
    def WrapTextAround(self, value:bool):
        """
        Sets a value indicating whether to wrap text around the row.
        """
        GetDllLibDoc().TableFormat_set_WrapTextAround.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().TableFormat_set_WrapTextAround,self.Ptr, value)

    @property
    def AllowAutoFit(self)->bool:
        """
        Gets or sets a value indicating whether to wrap text around the row.
        """
        GetDllLibDoc().TableFormat_get_AllowAutoFit.argtypes=[c_void_p]
        GetDllLibDoc().TableFormat_get_AllowAutoFit.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().TableFormat_get_AllowAutoFit,self.Ptr)
        return ret

    @AllowAutoFit.setter
    def AllowAutoFit(self, value:bool):
        """
        Sets a value indicating whether to wrap text around the row.
        """
        GetDllLibDoc().TableFormat_set_AllowAutoFit.argtypes=[c_void_p, c_bool]
        CallCFunction(GetDllLibDoc().TableFormat_set_AllowAutoFit,self.Ptr, value)

    @property
    def Positioning(self)->'TablePositioning':
        """
        Gets the positioning of the row.
        """
        GetDllLibDoc().TableFormat_get_Positioning.argtypes=[c_void_p]
        GetDllLibDoc().TableFormat_get_Positioning.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().TableFormat_get_Positioning,self.Ptr)
        from spire.doc import TablePositioning
        ret = None if intPtr==None else TablePositioning(intPtr)
        return ret

    def ClearBackground(self):
        """
        Clears the background of the cell.
        """
        GetDllLibDoc().TableFormat_ClearBackground.argtypes=[c_void_p]
        CallCFunction(GetDllLibDoc().TableFormat_ClearBackground,self.Ptr)

    def ClearFormatting(self):
        """
        Clears the background of the cell.
        """
        GetDllLibDoc().TableFormat_ClearFormatting.argtypes=[c_void_p]
        CallCFunction(GetDllLibDoc().TableFormat_ClearFormatting,self.Ptr)


    @property

    def PreferredWidth(self)->'PreferredWidth':
        """
        Gets or sets the preferred width of the table.
        """
        GetDllLibDoc().TableFormat_get_PreferredWidth.argtypes=[c_void_p]
        GetDllLibDoc().TableFormat_get_PreferredWidth.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().TableFormat_get_PreferredWidth,self.Ptr)
        ret = None if intPtr==None else PreferredWidth(intPtr)
        return ret


    @PreferredWidth.setter
    def PreferredWidth(self, value:'PreferredWidth'):
        GetDllLibDoc().TableFormat_set_PreferredWidth.argtypes=[c_void_p, c_void_p]
        CallCFunction(GetDllLibDoc().TableFormat_set_PreferredWidth,self.Ptr, value.Ptr)

    def Equals(self ,obj:'SpireObject')->bool:
        """
        Determines whether the current object is equal to another object.
        """
        intPtrobj:c_void_p = obj.Ptr

        GetDllLibDoc().TableFormat_Equals.argtypes=[c_void_p ,c_void_p]
        GetDllLibDoc().TableFormat_Equals.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().TableFormat_Equals,self.Ptr, intPtrobj)
        return ret

