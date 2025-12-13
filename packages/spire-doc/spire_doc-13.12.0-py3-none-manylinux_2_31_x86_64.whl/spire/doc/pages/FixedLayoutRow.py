from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc.pages import *
from spire.doc import *
from ctypes import *
import abc

class FixedLayoutRow (  LayoutElement) :
    """
    Represents a table row.
    """
    @property

    def Cells(self)->'LayoutFixedLCellCollection':
        """
        Provides access to the cells of the table row.
        """
        GetDllLibDoc().FixedLayoutRow_get_Cells.argtypes=[c_void_p]
        GetDllLibDoc().FixedLayoutRow_get_Cells.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().FixedLayoutRow_get_Cells,self.Ptr)
        ret = None if intPtr==None else LayoutFixedLCellCollection(intPtr)
        return ret



    @property

    def Row(self)->'TableRow':
        """
        Returns the row that corresponds to the layout entity.  
        """
        GetDllLibDoc().FixedLayoutRow_get_Row.argtypes=[c_void_p]
        GetDllLibDoc().FixedLayoutRow_get_Row.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().FixedLayoutRow_get_Row,self.Ptr)
        ret = None if intPtr==None else TableRow(intPtr)
        return ret


    @property

    def Table(self)->'Table':
        """
        Returns the table that corresponds to the layout entity.  
        """
        GetDllLibDoc().FixedLayoutRow_get_Table.argtypes=[c_void_p]
        GetDllLibDoc().FixedLayoutRow_get_Table.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().FixedLayoutRow_get_Table,self.Ptr)
        from spire.doc import Table
        ret = None if intPtr==None else Table(intPtr)
        return ret


    @property

    def ParentNode(self)->'DocumentObject':
        """
        Provides the layout node that pertains to this particular entity.
        """
        GetDllLibDoc().FixedLayoutRow_get_ParentNode.argtypes=[c_void_p]
        GetDllLibDoc().FixedLayoutRow_get_ParentNode.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().FixedLayoutRow_get_ParentNode,self.Ptr)
        ret = None if intPtr==None else DocumentObject(intPtr)
        return ret


