from __future__ import annotations
from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class ListFormat (  WordAttributeBase) :
    """
    Represents the formatting of a list in a document.
    """
    @property
    def ListLevelNumber(self)->int:
        """
        Returns or sets the list nesting level.
        """
        GetDllLibDoc().ListFormat_get_ListLevelNumber.argtypes=[c_void_p]
        GetDllLibDoc().ListFormat_get_ListLevelNumber.restype=c_int
        ret = CallCFunction(GetDllLibDoc().ListFormat_get_ListLevelNumber,self.Ptr)
        return ret

    @ListLevelNumber.setter
    def ListLevelNumber(self, value:int):
        GetDllLibDoc().ListFormat_set_ListLevelNumber.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().ListFormat_set_ListLevelNumber,self.Ptr, value)

    @property

    def ListType(self)->'ListType':
        """
        Gets the type of the list.
        """
        GetDllLibDoc().ListFormat_get_ListType.argtypes=[c_void_p]
        GetDllLibDoc().ListFormat_get_ListType.restype=c_int
        ret = CallCFunction(GetDllLibDoc().ListFormat_get_ListType,self.Ptr)
        objwraped = ListType(ret)
        return objwraped

    @property

    def CurrentListRef(self)->'ListDefinitionReference':
        """
		Gets or sets the current list reference. If the list Id is zero, returns null.
        """
        GetDllLibDoc().ListFormat_get_CurrentListRef.argtypes=[c_void_p]
        GetDllLibDoc().ListFormat_get_CurrentListRef.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ListFormat_get_CurrentListRef,self.Ptr)
        ret = None if intPtr==None else ListDefinitionReference(intPtr)
        return ret


    @CurrentListRef.setter
    def CurrentListRef(self, value:'ListDefinitionReference'):
        GetDllLibDoc().ListFormat_set_CurrentListRef.argtypes=[c_void_p, c_void_p]
        CallCFunction(GetDllLibDoc().ListFormat_set_CurrentListRef,self.Ptr, value.Ptr)

    @property

    def CurrentListLevel(self)->'ListLevel':
        """
        Gets the paragraph's ListLevel.
        """
        GetDllLibDoc().ListFormat_get_CurrentListLevel.argtypes=[c_void_p]
        GetDllLibDoc().ListFormat_get_CurrentListLevel.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ListFormat_get_CurrentListLevel,self.Ptr)
        from spire.doc import ListLevel
        ret = None if intPtr==None else ListLevel(intPtr)
        return ret


    def IncreaseIndentLevel(self):
        """
        Increase the level of indentation.
        """
        GetDllLibDoc().ListFormat_IncreaseIndentLevel.argtypes=[c_void_p]
        CallCFunction(GetDllLibDoc().ListFormat_IncreaseIndentLevel,self.Ptr)

    def DecreaseIndentLevel(self):
        """
        Decrease the level of indentation.
        """
        GetDllLibDoc().ListFormat_DecreaseIndentLevel.argtypes=[c_void_p]
        CallCFunction(GetDllLibDoc().ListFormat_DecreaseIndentLevel,self.Ptr)

    def ContinueListNumbering(self):
        """
        Continue the last list.
        """
        GetDllLibDoc().ListFormat_ContinueListNumbering.argtypes=[c_void_p]
        CallCFunction(GetDllLibDoc().ListFormat_ContinueListNumbering,self.Ptr)

    @dispatch

    def ApplyStyle(self ,styleName:str):
        """
        Apply a list style.

        Args:
            styleName: The name of the list style.
        """
        styleNamePtr = StrToPtr(styleName)
        GetDllLibDoc().ListFormat_ApplyStyle.argtypes=[c_void_p ,c_char_p]
        CallCFunction(GetDllLibDoc().ListFormat_ApplyStyle,self.Ptr, styleNamePtr)

    @dispatch

    def ApplyStyle(self ,listStyle:'ListStyle'):
        """

        """
        intPtrlistStyle:c_void_p = listStyle.Ptr

        GetDllLibDoc().ListFormat_ApplyStyleL.argtypes=[c_void_p ,c_void_p]
        CallCFunction(GetDllLibDoc().ListFormat_ApplyStyleL,self.Ptr, intPtrlistStyle)

    def ApplyBulletStyle(self):
        """
        Apply the default bullet style for the current paragraph.
        """
        GetDllLibDoc().ListFormat_ApplyBulletStyle.argtypes=[c_void_p]
        CallCFunction(GetDllLibDoc().ListFormat_ApplyBulletStyle,self.Ptr)

    def ApplyNumberedStyle(self):
        """
        Apply the default numbered style for the current paragraph.
        """
        GetDllLibDoc().ListFormat_ApplyNumberedStyle.argtypes=[c_void_p]
        CallCFunction(GetDllLibDoc().ListFormat_ApplyNumberedStyle,self.Ptr)


    def ApplyListRef(self ,list:'ListDefinitionReference',leverNumber:int):
        """
        Applies a style to a list by setting its identifier and level number.
        
        list:The list reference to which the style is applied.
        leverNumber:The level number of the list item.
        """
        intPtrlist:c_void_p = list.Ptr

        GetDllLibDoc().ListFormat_ApplyListRef.argtypes=[c_void_p ,c_void_p,c_int]
        CallCFunction(GetDllLibDoc().ListFormat_ApplyListRef,self.Ptr, intPtrlist,leverNumber)

    def RemoveList(self):
        """
        Remove the list from the current paragraph.
        """
        GetDllLibDoc().ListFormat_RemoveList.argtypes=[c_void_p]
        CallCFunction(GetDllLibDoc().ListFormat_RemoveList,self.Ptr)

