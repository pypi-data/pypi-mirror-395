from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc.pages import *
from spire.doc import *
from ctypes import *
import abc

class FixedLayoutColumn (  BodyLayoutElement) :
    """
    Represents a column of text on a page.
    """
    @property

    def Footnotes(self)->'LayoutFixedLFootnoteCollection':
        """
        Provides access to the footnotes of the page.
        """
        GetDllLibDoc().FixedLayoutColumn_get_Footnotes.argtypes=[c_void_p]
        GetDllLibDoc().FixedLayoutColumn_get_Footnotes.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().FixedLayoutColumn_get_Footnotes,self.Ptr)
        ret = None if intPtr==None else LayoutFixedLFootnoteCollection(intPtr)
        return ret



    @property

    def Endnotes(self)->'LayoutFixedLEndnoteCollection':
        """
        Provides access to the endnotes of the page.
        """
        GetDllLibDoc().FixedLayoutColumn_get_Endnotes.argtypes=[c_void_p]
        GetDllLibDoc().FixedLayoutColumn_get_Endnotes.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().FixedLayoutColumn_get_Endnotes,self.Ptr)
        ret = None if intPtr==None else LayoutFixedLEndnoteCollection(intPtr)
        return ret



    @property

    def NoteSeparators(self)->'LayoutFixedLNoteSeparatorCollection':
        """
        Provides access to the note separators of the page.
        """
        GetDllLibDoc().FixedLayoutColumn_get_NoteSeparators.argtypes=[c_void_p]
        GetDllLibDoc().FixedLayoutColumn_get_NoteSeparators.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().FixedLayoutColumn_get_NoteSeparators,self.Ptr)
        ret = None if intPtr==None else LayoutFixedLNoteSeparatorCollection(intPtr)
        return ret



    @property

    def Body(self)->'Body':
        """
        Returns the body that corresponds to the layout entity.  
        """
        GetDllLibDoc().FixedLayoutColumn_get_Body.argtypes=[c_void_p]
        GetDllLibDoc().FixedLayoutColumn_get_Body.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().FixedLayoutColumn_get_Body,self.Ptr)
        ret = None if intPtr==None else Body(intPtr)
        return ret


    @property

    def ParentNode(self)->'DocumentObject':
        """
        Provides the layout node that pertains to this particular entity.
        """
        GetDllLibDoc().FixedLayoutColumn_get_ParentNode.argtypes=[c_void_p]
        GetDllLibDoc().FixedLayoutColumn_get_ParentNode.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().FixedLayoutColumn_get_ParentNode,self.Ptr)
        ret = None if intPtr==None else DocumentObject(intPtr)
        return ret


