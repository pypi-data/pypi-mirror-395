from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc.pages import *
from spire.doc import *
from ctypes import *
import abc

class FixedLayoutPage (  LayoutElement) :
    """
    Represents page of a document.
    """
    @property

    def Columns(self)->'LayoutFixedLColumnCollection':
        """
        Provides access to the columns of the page.
        """
        GetDllLibDoc().FixedLayoutPage_get_Columns.argtypes=[c_void_p]
        GetDllLibDoc().FixedLayoutPage_get_Columns.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().FixedLayoutPage_get_Columns,self.Ptr)
        from spire.doc.pages.LayoutFixedLColumnCollection import LayoutFixedLColumnCollection
        ret = None if intPtr==None else LayoutFixedLColumnCollection(intPtr)
        return ret



    @property

    def HeaderFooters(self)->'LayoutFixedLHeaderFooterCollection':
        """
        Provides access to the header and footers of the page.
        """
        GetDllLibDoc().FixedLayoutPage_get_HeaderFooters.argtypes=[c_void_p]
        GetDllLibDoc().FixedLayoutPage_get_HeaderFooters.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().FixedLayoutPage_get_HeaderFooters,self.Ptr)
        ret = None if intPtr==None else LayoutFixedLHeaderFooterCollection(intPtr)
        return ret



    @property

    def Comments(self)->'LayoutFixedLCommentCollection':
        """
        Provides access to the comments of the page.
        """
        GetDllLibDoc().FixedLayoutPage_get_Comments.argtypes=[c_void_p]
        GetDllLibDoc().FixedLayoutPage_get_Comments.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().FixedLayoutPage_get_Comments,self.Ptr)
        ret = None if intPtr==None else LayoutFixedLCommentCollection(intPtr)
        return ret



    @property

    def Section(self)->'Section':
        """
        Returns the section that corresponds to the layout entity.  
        """
        GetDllLibDoc().FixedLayoutPage_get_Section.argtypes=[c_void_p]
        GetDllLibDoc().FixedLayoutPage_get_Section.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().FixedLayoutPage_get_Section,self.Ptr)
        from spire.doc.Section import Section
        ret = None if intPtr==None else Section(intPtr)
        return ret


    @property

    def ParentNode(self)->'DocumentObject':
        """
        Provides the layout node that pertains to this particular entity.
        """
        GetDllLibDoc().FixedLayoutPage_get_ParentNode.argtypes=[c_void_p]
        GetDllLibDoc().FixedLayoutPage_get_ParentNode.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().FixedLayoutPage_get_ParentNode,self.Ptr)
        ret = None if intPtr==None else DocumentObject(intPtr)
        return ret


