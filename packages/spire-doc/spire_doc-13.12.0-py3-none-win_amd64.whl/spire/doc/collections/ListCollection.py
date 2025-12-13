from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class ListCollection (  DocumentSerializableCollection) :
    """
    Represents a collection of list reference.
    """

    def get_Item(self ,index:int)->'ListDefinitionReference':
        """
        Gets the <see cref="Spire.Doc.ListStyle"/> at the specified index.
        """
        
        GetDllLibDoc().ListCollection_get_Item.argtypes=[c_void_p ,c_int]
        GetDllLibDoc().ListCollection_get_Item.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ListCollection_get_Item,self.Ptr, index)
        ret = None if intPtr==None else ListDefinitionReference(intPtr)
        return ret



    def Add(self ,template:'ListTemplate')->'ListDefinitionReference':
        """
        Creates a new list using the specified template and returns a reference to it.

        args:
            template">The template used to create the new list.

        returns:
            A reference to the newly created list.
        """
        enumtemplate:c_int = template.value

        GetDllLibDoc().ListCollection_Add.argtypes=[c_void_p ,c_int]
        GetDllLibDoc().ListCollection_Add.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ListCollection_Add,self.Ptr, enumtemplate)
        ret = None if intPtr==None else ListDefinitionReference(intPtr)
        return ret



    def AddSingleLevelList(self ,listTemplate:'ListTemplate')->'ListDefinitionReference':
        """
        Creates a single-level list using the specified list template and adds it to the current context.
        
        Args:
            listTemplate:The list template used to create the single level list.
            
        returns:
            A ListReference representing the newly created single level list.
        """
        enumlistTemplate:c_int = listTemplate.value

        GetDllLibDoc().ListCollection_AddSingleLevelList.argtypes=[c_void_p ,c_int]
        GetDllLibDoc().ListCollection_AddSingleLevelList.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ListCollection_AddSingleLevelList,self.Ptr, enumlistTemplate)
        ret = None if intPtr==None else ListDefinitionReference(intPtr)
        return ret



    def FindByName(self ,listDefName:str)->'ListDefinitionReference':
        """
        Finds list style by name.

        Args:
            listDefName">The name to search for in the list definitions.
        """
        listDefNamePtr=StrToPtr(listDefName)
        GetDllLibDoc().ListCollection_FindByName.argtypes=[c_void_p ,c_char_p]
        GetDllLibDoc().ListCollection_FindByName.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ListCollection_FindByName,self.Ptr, listDefNamePtr)
        ret = None if intPtr==None else ListDefinitionReference(intPtr)
        return ret


