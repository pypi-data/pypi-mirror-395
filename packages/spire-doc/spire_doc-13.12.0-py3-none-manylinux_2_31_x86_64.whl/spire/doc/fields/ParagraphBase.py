from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class ParagraphBase (  DocumentBase, IParagraphBase) :
    """
    Base class for paragraphs in a document.
    """
    @property

    def ChildObjects(self)->'DocumentObjectCollection':
        """
        Gets the child objects of the entity.
        """
        GetDllLibDoc().ParagraphBase_get_ChildObjects.argtypes=[c_void_p]
        GetDllLibDoc().ParagraphBase_get_ChildObjects.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ParagraphBase_get_ChildObjects,self.Ptr)
        ret = None if intPtr==None else DocumentObjectCollection(intPtr)
        return ret


    @property

    def OwnerParagraph(self)->'Paragraph':
        """
        Gets the owner paragraph.
        """
        GetDllLibDoc().ParagraphBase_get_OwnerParagraph.argtypes=[c_void_p]
        GetDllLibDoc().ParagraphBase_get_OwnerParagraph.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ParagraphBase_get_OwnerParagraph,self.Ptr)
        from spire.doc import Paragraph
        ret = None if intPtr==None else Paragraph(intPtr)
        return ret


    @property
    def IsInsertRevision(self)->bool:
        """
        Gets a value indicating whether this item was inserted to the document,
        when "Track Changes" is or was set to "true".
        """
        GetDllLibDoc().ParagraphBase_get_IsInsertRevision.argtypes=[c_void_p]
        GetDllLibDoc().ParagraphBase_get_IsInsertRevision.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().ParagraphBase_get_IsInsertRevision,self.Ptr)
        return ret

    @property
    def IsDeleteRevision(self)->bool:
        """
        Gets or sets a value indicating whether this item was deleted from the document,
        when "Track Changes" is or was set to "true".
        """
        GetDllLibDoc().ParagraphBase_get_IsDeleteRevision.argtypes=[c_void_p]
        GetDllLibDoc().ParagraphBase_get_IsDeleteRevision.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().ParagraphBase_get_IsDeleteRevision,self.Ptr)
        return ret

    @property
    def IsMoveFromRevision(self)->bool:
        """
        Gets a value indicating whether the run has a move from revision.
        """
        GetDllLibDoc().ParagraphBase_get_IsMoveFromRevision.argtypes=[c_void_p]
        GetDllLibDoc().ParagraphBase_get_IsMoveFromRevision.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().ParagraphBase_get_IsMoveFromRevision,self.Ptr)
        return ret

    @property
    def IsMoveToRevision(self)->bool:
        """
        Determines if the run properties have a move to revision.
        """
        GetDllLibDoc().ParagraphBase_get_IsMoveToRevision.argtypes=[c_void_p]
        GetDllLibDoc().ParagraphBase_get_IsMoveToRevision.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().ParagraphBase_get_IsMoveToRevision,self.Ptr)
        return ret

    @property

    def DeleteRevision(self)->'EditRevision':
        """
        Gets the delete revision for this object.
        Note: This can be null. If null, it does not have a delete revision.
        """
        GetDllLibDoc().ParagraphBase_get_DeleteRevision.argtypes=[c_void_p]
        GetDllLibDoc().ParagraphBase_get_DeleteRevision.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ParagraphBase_get_DeleteRevision,self.Ptr)
        from spire.doc import EditRevision
        ret = None if intPtr==None else EditRevision(intPtr)
        return ret


    @DeleteRevision.setter
    def DeleteRevision(self, value:'EditRevision'):
        GetDllLibDoc().ParagraphBase_set_DeleteRevision.argtypes=[c_void_p, c_void_p]
        CallCFunction(GetDllLibDoc().ParagraphBase_set_DeleteRevision,self.Ptr, value.Ptr)

    @property

    def InsertRevision(self)->'EditRevision':
        """
        Gets the insert revision for this object.
        Note: This can be null. If null, it does not have an insert revision.
        """
        GetDllLibDoc().ParagraphBase_get_InsertRevision.argtypes=[c_void_p]
        GetDllLibDoc().ParagraphBase_get_InsertRevision.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ParagraphBase_get_InsertRevision,self.Ptr)
        from spire.doc import EditRevision
        ret = None if intPtr==None else EditRevision(intPtr)
        return ret


    @InsertRevision.setter
    def InsertRevision(self, value:'EditRevision'):
        GetDllLibDoc().ParagraphBase_set_InsertRevision.argtypes=[c_void_p, c_void_p]
        CallCFunction(GetDllLibDoc().ParagraphBase_set_InsertRevision,self.Ptr, value.Ptr)

    @property

    def MoveToRevision(self)->'MoveRevision':
        """
        Gets the MoveTo revision for this objects.
        Note this can be null. If null does not have MoveTo revision.
        """
        GetDllLibDoc().ParagraphBase_get_MoveToRevision.argtypes=[c_void_p]
        GetDllLibDoc().ParagraphBase_get_MoveToRevision.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ParagraphBase_get_MoveToRevision,self.Ptr)
        ret = None if intPtr==None else MoveRevision(intPtr)
        return ret


    @MoveToRevision.setter
    def MoveToRevision(self, value:'MoveRevision'):
        GetDllLibDoc().ParagraphBase_set_MoveToRevision.argtypes=[c_void_p, c_void_p]
        CallCFunction(GetDllLibDoc().ParagraphBase_set_MoveToRevision,self.Ptr, value.Ptr)

    @property

    def MoveFromRevision(self)->'MoveRevision':
        """
        Gets the MoveFrom revision for this objects.
        Note this can be null. If null does not have MoveFrom revision.
        """
        GetDllLibDoc().ParagraphBase_get_MoveFromRevision.argtypes=[c_void_p]
        GetDllLibDoc().ParagraphBase_get_MoveFromRevision.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ParagraphBase_get_MoveFromRevision,self.Ptr)
        ret = None if intPtr==None else MoveRevision(intPtr)
        return ret


    @MoveFromRevision.setter
    def MoveFromRevision(self, value:'MoveRevision'):
        GetDllLibDoc().ParagraphBase_set_MoveFromRevision.argtypes=[c_void_p, c_void_p]
        CallCFunction(GetDllLibDoc().ParagraphBase_set_MoveFromRevision,self.Ptr, value.Ptr)

    @property

    def StyleName(self)->str:
        """
        Gets the style name.
        """
        GetDllLibDoc().ParagraphBase_get_StyleName.argtypes=[c_void_p]
        GetDllLibDoc().ParagraphBase_get_StyleName.restype=c_void_p
        ret = PtrToStr(CallCFunction(GetDllLibDoc().ParagraphBase_get_StyleName,self.Ptr))
        return ret


    @property

    def CharacterFormat(self)->'CharacterFormat':
        """
        Gets the character format.
        """
        GetDllLibDoc().ParagraphBase_get_CharacterFormat.argtypes=[c_void_p]
        GetDllLibDoc().ParagraphBase_get_CharacterFormat.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ParagraphBase_get_CharacterFormat,self.Ptr)
        from spire.doc import CharacterFormat
        ret = None if intPtr==None else CharacterFormat(intPtr)
        return ret



    def ApplyCharacterFormat(self ,charFormat:'CharacterFormat'):
        """
        Sets the character format.
        """
        intPtrcharFormat:c_void_p = charFormat.Ptr

        GetDllLibDoc().ParagraphBase_ApplyCharacterFormat.argtypes=[c_void_p ,c_void_p]
        CallCFunction(GetDllLibDoc().ParagraphBase_ApplyCharacterFormat,self.Ptr, intPtrcharFormat)


    def ApplyStyle(self ,styleName:str):
        """
        Applies the specified style to the paragraph.
        """
        styleNamePtr = StrToPtr(styleName)
        GetDllLibDoc().ParagraphBase_ApplyStyle.argtypes=[c_void_p ,c_char_p]
        CallCFunction(GetDllLibDoc().ParagraphBase_ApplyStyle,self.Ptr, styleNamePtr)


    def GetPreviousWidgetSibling(self)->'IDocumentObject':
        """
        Gets the previous widget sibling of the paragraph.
        """
        GetDllLibDoc().ParagraphBase_GetPreviousWidgetSibling.argtypes=[c_void_p]
        GetDllLibDoc().ParagraphBase_GetPreviousWidgetSibling.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ParagraphBase_GetPreviousWidgetSibling,self.Ptr)
        ret = None if intPtr==None else IDocumentObject(intPtr)
        return ret



    def GetNextWidgetSibling(self)->'IDocumentObject':
        """
        Gets the next widget sibling of the paragraph.
        """
        GetDllLibDoc().ParagraphBase_GetNextWidgetSibling.argtypes=[c_void_p]
        GetDllLibDoc().ParagraphBase_GetNextWidgetSibling.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().ParagraphBase_GetNextWidgetSibling,self.Ptr)
        ret = None if intPtr==None else IDocumentObject(intPtr)
        return ret


