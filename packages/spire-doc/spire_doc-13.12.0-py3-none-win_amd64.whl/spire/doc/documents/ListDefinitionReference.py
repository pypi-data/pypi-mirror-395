from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class ListDefinitionReference (  DocumentSerializable) :
    """
    Represents a reference to a list definition within a document.
    """
    @dispatch

    def CompareTo(self ,obj:SpireObject)->int:
        """
        Compares the current instance with another object of the same type.
        """
        intPtrobj:c_void_p = obj.Ptr

        GetDllLibDoc().ListDefinitionReference_CompareTo.argtypes=[c_void_p ,c_void_p]
        GetDllLibDoc().ListDefinitionReference_CompareTo.restype=c_int
        ret = CallCFunction(GetDllLibDoc().ListDefinitionReference_CompareTo,self.Ptr, intPtrobj)
        return ret

    @dispatch

    def CompareTo(self ,obj:'ListDefinitionReference')->int:
        """
        Compares the current instance with another ListDefinitionReference object based on their ListId values.
        """
        intPtrobj:c_void_p = obj.Ptr

        GetDllLibDoc().ListDefinitionReference_CompareToO.argtypes=[c_void_p ,c_void_p]
        GetDllLibDoc().ListDefinitionReference_CompareToO.restype=c_int
        ret = CallCFunction(GetDllLibDoc().ListDefinitionReference_CompareToO,self.Ptr, intPtrobj)
        return ret


    def HasSameTemplate(self ,other:'ListDefinitionReference')->bool:
        """
        Checks if the current list definition reference has the same template as another list definition reference.
        """
        intPtrother:c_void_p = other.Ptr

        GetDllLibDoc().ListDefinitionReference_HasSameTemplate.argtypes=[c_void_p ,c_void_p]
        GetDllLibDoc().ListDefinitionReference_HasSameTemplate.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().ListDefinitionReference_HasSameTemplate,self.Ptr, intPtrother)
        return ret

    @property

    def Levels(self)->'ListLevelCollection':
        """
        Gets a collection of levels from the terminal list definition.
        """
        GetDllLibDoc().ListDefinitionReference_get_Levels.argtypes=[c_void_p]
        GetDllLibDoc().ListDefinitionReference_get_Levels.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ListDefinitionReference_get_Levels,self.Ptr)
        from spire.doc.collections.ListLevelCollection import ListLevelCollection
        ret = None if intPtr==None else ListLevelCollection(intPtr)
        return ret


    @property
    def ListId(self)->int:
        """
        Gets the identifier for the list.
        """
        GetDllLibDoc().ListDefinitionReference_get_ListId.argtypes=[c_void_p]
        GetDllLibDoc().ListDefinitionReference_get_ListId.restype=c_int
        ret = CallCFunction(GetDllLibDoc().ListDefinitionReference_get_ListId,self.Ptr)
        return ret

    @property
    def IsMultiLevel(self)->bool:
        """
        Indicates whether the list has multiple levels.
        """
        GetDllLibDoc().ListDefinitionReference_get_IsMultiLevel.argtypes=[c_void_p]
        GetDllLibDoc().ListDefinitionReference_get_IsMultiLevel.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().ListDefinitionReference_get_IsMultiLevel,self.Ptr)
        return ret

    @property
    def IsListStyleDefinition(self)->bool:
        """
        Gets a value indicating whether this is a list style definition.
        """
        GetDllLibDoc().ListDefinitionReference_get_IsListStyleDefinition.argtypes=[c_void_p]
        GetDllLibDoc().ListDefinitionReference_get_IsListStyleDefinition.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().ListDefinitionReference_get_IsListStyleDefinition,self.Ptr)
        return ret

    @property
    def IsListStyleReference(self)->bool:
        """
        Gets a value indicating whether the list style is a reference.
        """
        GetDllLibDoc().ListDefinitionReference_get_IsListStyleReference.argtypes=[c_void_p]
        GetDllLibDoc().ListDefinitionReference_get_IsListStyleReference.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().ListDefinitionReference_get_IsListStyleReference,self.Ptr)
        return ret

    @property

    def Style(self)->'Style':
        """
        Gets the style associated with the list definition.
        """
        GetDllLibDoc().ListDefinitionReference_get_Style.argtypes=[c_void_p]
        GetDllLibDoc().ListDefinitionReference_get_Style.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ListDefinitionReference_get_Style,self.Ptr)
        ret = None if intPtr==None else Style(intPtr)
        return ret


    @property

    def Name(self)->str:
        """
        Gets the name from the list definition object.
        """
        GetDllLibDoc().ListDefinitionReference_get_Name.argtypes=[c_void_p]
        GetDllLibDoc().ListDefinitionReference_get_Name.restype=c_void_p
        ret = PtrToStr(CallCFunction(GetDllLibDoc().ListDefinitionReference_get_Name,self.Ptr))
        return ret


