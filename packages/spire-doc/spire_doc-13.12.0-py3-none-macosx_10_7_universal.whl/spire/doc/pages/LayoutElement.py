from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc.pages import *
from spire.doc import *
from ctypes import *
import abc

class LayoutElement (SpireObject) :
    """
    The class serves as the foundation for elements in a document that have been rendered.
    """
    @property
    def PageIndex(self)->int:
        """
        Gets the index of a page in which rendered object. starting from 1.
        """
        GetDllLibDoc().LayoutElement_get_PageIndex.argtypes=[c_void_p]
        GetDllLibDoc().LayoutElement_get_PageIndex.restype=c_int
        ret = CallCFunction(GetDllLibDoc().LayoutElement_get_PageIndex,self.Ptr)
        return ret

    @property

    def Rectangle(self)->'RectangleF':
        """
        Returns bounding rectangle of the entity relative to the page top left corner (in points).
        """
        GetDllLibDoc().LayoutElement_get_Rectangle.argtypes=[c_void_p]
        GetDllLibDoc().LayoutElement_get_Rectangle.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().LayoutElement_get_Rectangle,self.Ptr)
        ret = None if intPtr==None else RectangleF(intPtr)
        return ret


    @property

    def Type(self)->'LayoutElementType':
        """
        Gets the type of this layout entity.
        """
        GetDllLibDoc().LayoutElement_get_Type.argtypes=[c_void_p]
        GetDllLibDoc().LayoutElement_get_Type.restype=c_int
        ret = CallCFunction(GetDllLibDoc().LayoutElement_get_Type,self.Ptr)
        from spire.doc import LayoutElementType
        objwraped = LayoutElementType(ret)
        return objwraped

    @property

    def Text(self)->str:
        """
        Outputs the entity's contents as a plain text string.
        """
        GetDllLibDoc().LayoutElement_get_Text.argtypes=[c_void_p]
        GetDllLibDoc().LayoutElement_get_Text.restype=c_void_p
        ret = PtrToStr(CallCFunction(GetDllLibDoc().LayoutElement_get_Text,self.Ptr))
        return ret


    @property

    def Parent(self)->'LayoutElement':
        """
        Gets the parent of this entity.
        """
        GetDllLibDoc().LayoutElement_get_Parent.argtypes=[c_void_p]
        GetDllLibDoc().LayoutElement_get_Parent.restype= IntPtrWithTypeName
        intPtr = CallCFunction(GetDllLibDoc().LayoutElement_get_Parent,self.Ptr)
        ret = None if intPtr==None else self._createLayoutElement(intPtr)
        return ret

    def _createLayoutElement(self, intPtrWithTypeName:IntPtrWithTypeName)->'LayoutElement':
		
        ret= None
        if intPtrWithTypeName == None :
            return ret
        intPtr = intPtrWithTypeName.intPtr[0] + (intPtrWithTypeName.intPtr[1]<<32)
        strName = PtrToStr(intPtrWithTypeName.typeName)
		
        if (strName == "Spire.Doc.Pages.FixedLayoutCell"):
            from spire.doc import FixedLayoutCell
            ret = FixedLayoutCell(intPtr)
        elif (strName == "Spire.Doc.Pages.FixedLayoutColumn"):
            from spire.doc import FixedLayoutColumn
            ret = FixedLayoutColumn(intPtr)
        elif (strName == "Spire.Doc.Pages.FixedLayoutComment"):
            from spire.doc import FixedLayoutComment
            ret = FixedLayoutComment(intPtr)
        elif (strName == "Spire.Doc.Pages.FixedLayoutDocument"):
            from spire.doc import FixedLayoutDocument
            ret = FixedLayoutDocument(intPtr)
        elif (strName == "Spire.Doc.Pages.FixedLayoutEndnote"):
            from spire.doc import FixedLayoutEndnote
            ret = FixedLayoutEndnote(intPtr)
        elif (strName == "Spire.Doc.Pages.FixedLayoutFootnote"):
            from spire.doc import FixedLayoutFootnote
            ret = FixedLayoutFootnote(intPtr)
        elif (strName == "Spire.Doc.Pages.FixedLayoutHeaderFooter"):
            from spire.doc import FixedLayoutHeaderFooter
            ret = FixedLayoutHeaderFooter(intPtr)
        elif (strName == "Spire.Doc.Pages.FixedLayoutLine"):
            from spire.doc import FixedLayoutLine
            ret = FixedLayoutLine(intPtr)
        elif (strName == "Spire.Doc.Pages.FixedLayoutNoteSeparator"):
            from spire.doc import FixedLayoutNoteSeparator
            ret = FixedLayoutNoteSeparator(intPtr)
        elif (strName == "Spire.Doc.Pages.FixedLayoutPage"):
            from spire.doc import FixedLayoutPage
            ret = FixedLayoutPage(intPtr)
        elif (strName == "Spire.Doc.Pages.FixedLayoutRow"):
            from spire.doc import FixedLayoutRow
            ret = FixedLayoutRow(intPtr)
        elif (strName == "Spire.Doc.Pages.FixedLayoutSpan"):
            from spire.doc import FixedLayoutSpan
            ret = FixedLayoutSpan(intPtr)
        elif (strName == "Spire.Doc.Pages.FixedLayoutTextBox"):
            from spire.doc import FixedLayoutTextBox
            ret = FixedLayoutTextBox(intPtr)
        else:
            ret = LayoutElement(intPtr)
        return ret
    @property

    def ParentNode(self)->'DocumentObject':
        """
        Provides the layout node that pertains to this particular entity.
        """
        GetDllLibDoc().LayoutElement_get_ParentNode.argtypes=[c_void_p]
        GetDllLibDoc().LayoutElement_get_ParentNode.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().LayoutElement_get_ParentNode,self.Ptr)
        ret = None if intPtr==None else DocumentObject(intPtr)
        return ret



    def GetChildEntities(self ,type:'LayoutElementType',isDeep:bool)->'LayoutCollection':
        """
        Obtains a group of child entities that are of a specific type.
        Args:
            type: Specifies the type of entities to select.
            isDeep: True to select from all child entities recursively.
        
        False to select only among immediate children
        """
        enumtype:c_int = type.value

        GetDllLibDoc().LayoutElement_GetChildEntities.argtypes=[c_void_p ,c_int,c_bool]
        GetDllLibDoc().LayoutElement_GetChildEntities.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().LayoutElement_GetChildEntities,self.Ptr, enumtype,isDeep)
        from spire.doc.pages.LayoutCollection import LayoutCollection
        ret = None if intPtr==None else LayoutCollection(intPtr)
        return ret



