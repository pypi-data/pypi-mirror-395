from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class ListStyle (  Style, IStyle) :
    """
    Represents a list style.
    """
    @property

    def StyleType(self)->'StyleType':
        """
        Gets the type of the style.

        Returns:
            StyleType: The type of the style.
        """
        GetDllLibDoc().ListStyle_get_StyleType.argtypes=[c_void_p]
        GetDllLibDoc().ListStyle_get_StyleType.restype=c_int
        ret = CallCFunction(GetDllLibDoc().ListStyle_get_StyleType,self.Ptr)
        objwraped = StyleType(ret)
        return objwraped

    @property

    def ListRef(self)->'ListDefinitionReference':
        """
        Gets the list reference.
        """
        GetDllLibDoc().ListStyle_get_ListRef.argtypes=[c_void_p]
        GetDllLibDoc().ListStyle_get_ListRef.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ListStyle_get_ListRef,self.Ptr)
        from spire.doc.documents.ListDefinitionReference import ListDefinitionReference
        ret = None if intPtr==None else ListDefinitionReference(intPtr)
        return ret


    @property

    def BaseStyle(self)->'ListStyle':
        """
        Gets a base style of paragraph.
        """
        GetDllLibDoc().ListStyle_get_BaseStyle.argtypes=[c_void_p]
        GetDllLibDoc().ListStyle_get_BaseStyle.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ListStyle_get_BaseStyle,self.Ptr)
        ret = None if intPtr==None else ListStyle(intPtr)
        return ret



    def Clone(self)->'ListStyle':
        """
        Clones the list style.

        Returns:
            IStyle: The cloned list style.
        """
        GetDllLibDoc().ListStyle_Clone.argtypes=[c_void_p]
        GetDllLibDoc().ListStyle_Clone.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ListStyle_Clone,self.Ptr)
        ret = None if intPtr==None else ListStyle(intPtr)
        return ret


