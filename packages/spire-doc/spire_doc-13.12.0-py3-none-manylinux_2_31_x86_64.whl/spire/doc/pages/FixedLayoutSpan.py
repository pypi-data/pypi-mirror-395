from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc.pages import *
from spire.doc import *
from ctypes import *
import abc

class FixedLayoutSpan (  LayoutElement) :
    """
        Represents one or more characters in a line.
    """
    @property

    def Kind(self)->str:
        """
        Gets kind of the span. This cannot be null.
        """
        GetDllLibDoc().FixedLayoutSpan_get_Kind.argtypes=[c_void_p]
        GetDllLibDoc().FixedLayoutSpan_get_Kind.restype=c_void_p
        ret = PtrToStr(CallCFunction(GetDllLibDoc().FixedLayoutSpan_get_Kind,self.Ptr))
        return ret


    @property

    def Text(self)->str:
        """
        Exports the contents of the entity into a string in plain text format.
        """
        GetDllLibDoc().FixedLayoutSpan_get_Text.argtypes=[c_void_p]
        GetDllLibDoc().FixedLayoutSpan_get_Text.restype=c_void_p
        ret = PtrToStr(CallCFunction(GetDllLibDoc().FixedLayoutSpan_get_Text,self.Ptr))
        return ret


    @property

    def ParentNode(self)->'DocumentObject':
        """
        Provides the layout node that pertains to this particular entity.
        """
        GetDllLibDoc().FixedLayoutSpan_get_ParentNode.argtypes=[c_void_p]
        GetDllLibDoc().FixedLayoutSpan_get_ParentNode.restype=IntPtrWithTypeName
        intPtr = CallCFunction(GetDllLibDoc().FixedLayoutSpan_get_ParentNode,self.Ptr)
        ret = None if intPtr==None else self._create(intPtr)
        return ret

    def _create(self, intPtrWithTypeName:IntPtrWithTypeName)->'DocumentObject':
        ret= None
        if intPtrWithTypeName.typeName == None :
            return ret
        intPtr = intPtrWithTypeName.intPtr[0] + (intPtrWithTypeName.intPtr[1]<<32)
        strName = PtrToStr(intPtrWithTypeName.typeName)
        if (strName == "Spire.Doc.Documents.Paragraph"):
            from spire.doc import Paragraph
            ret = Paragraph(intPtr)
        elif(strName == "Spire.Doc.PictureWatermark"):
            from spire.doc import PictureWatermark
            ret = PictureWatermark(intPtr)
        elif (strName == "Spire.Doc.TextWatermark"):
            from spire.doc import TextWatermark
            ret = TextWatermark(intPtr)
        elif (strName == "Spire.Doc.Fields.TextRange"):
            from spire.doc import TextRange
            ret = TextRange(intPtr)
        #elif (strName == "Spire.Doc.BodyRegion"):
        #  ret = BodyRegion(intPtr)
        elif (strName == "Spire.Doc.Body"):
            from spire.doc import Body
            ret = Body(intPtr)
        elif (strName == "Spire.Doc.HeaderFooter"):
            from spire.doc import HeaderFooter
            ret = HeaderFooter(intPtr)
        elif (strName == "Spire.Doc.Section"):
            from spire.doc import Section
            ret = Section(intPtr)
        elif (strName == "Spire.Doc.Table"):
            from spire.doc import Table
            ret = Table(intPtr)
        elif (strName == "Spire.Doc.TableCell"):
            from spire.doc import TableCell
            ret = TableCell(intPtr)
        elif (strName == "Spire.Doc.TableRow"):
            from spire.doc import TableRow
            ret = TableRow(intPtr)
        elif (strName == "Spire.Doc.BookmarkEnd"):
            from spire.doc import BookmarkEnd
            ret = BookmarkEnd(intPtr)
        elif (strName == "Spire.Doc.BookmarkStart"):
            from spire.doc import BookmarkStart
            ret = BookmarkStart(intPtr)
        elif (strName == "Spire.Doc.Break"):
            from spire.doc import Break
            ret = Break(intPtr)
        elif (strName == "Spire.Doc.PermissionStart"):
            from spire.doc import PermissionStart
            ret = PermissionStart(intPtr)
        elif (strName == "Spire.Doc.PermissionEnd"):
            from spire.doc import PermissionEnd
            ret = PermissionEnd(intPtr)
        elif (strName == "Spire.Doc.Fields.OMath.OfficeMath"):
            from spire.doc import OfficeMath
            ret = OfficeMath(intPtr)
        elif (strName == "Spire.Doc.Fields.ShapeGroup"):
            from spire.doc import ShapeGroup
            ret = ShapeGroup(intPtr)
        elif (strName == "Spire.Doc.Fields.DocOleObject"):
            from spire.doc import DocOleObject
            ret = DocOleObject(intPtr)
        elif (strName == "Spire.Doc.Fields.ShapeObject"):
            from spire.doc import ShapeObject
            ret = ShapeObject(intPtr)
        elif (strName == "Spire.Doc.Fields.TableOfContent"):
            from spire.doc import TableOfContent
            ret = TableOfContent(intPtr)
        elif (strName == "Spire.Doc.Fields.CheckBoxFormField"):
            from spire.doc import CheckBoxFormField
            ret = CheckBoxFormField(intPtr)
        elif (strName == "Spire.Doc.Fields.Comment"):
            from spire.doc import Comment
            ret = Comment(intPtr)
        elif (strName == "Spire.Doc.Documents.CommentMark"):
            from spire.doc import CommentMark
            ret = CommentMark(intPtr)
        elif (strName == "Spire.Doc.Fields.DropDownFormField"):
            from spire.doc import DropDownFormField
            ret = DropDownFormField(intPtr)
        elif (strName == "Spire.Doc.Fields.ControlField"):
            from spire.doc import ControlField
            ret = ControlField(intPtr)
        elif (strName == "Spire.Doc.Fields.Field"):
            from spire.doc import Field
            ret = Field(intPtr)
        elif (strName == "Spire.Doc.Fields.FieldMark"):
            from spire.doc import FieldMark
            ret = FieldMark(intPtr)
        elif (strName == "Spire.Doc.Fields.Footnote"):
            from spire.doc import Footnote
            ret = Footnote(intPtr)
        elif (strName == "Spire.Doc.Fields.IfField"):
            from spire.doc import IfField
            ret = IfField(intPtr)
        elif (strName == "Spire.Doc.Fields.MergeField"):
            from spire.doc import MergeField
            ret = MergeField(intPtr)
        elif (strName == "Spire.Doc.Fields.DocPicture"):
            from spire.doc import DocPicture
            ret = DocPicture(intPtr)
        elif (strName == "Spire.Doc.Fields.SequenceField"):
            from spire.doc import SequenceField
            ret = SequenceField(intPtr)
        elif (strName == "Spire.Doc.Fields.Symbol"):
            from spire.doc import Symbol
            ret = Symbol(intPtr)
        elif (strName == "Spire.Doc.Fields.TextBox"):
            from spire.doc import TextBox
            ret = TextBox(intPtr)
        elif (strName == "Spire.Doc.Fields.TextFormField"):
            from spire.doc import TextFormField
            ret = TextFormField(intPtr)
        elif (strName == "Spire.Doc.Documents.SDTContent"):
            from spire.doc import SDTContent
            ret = SDTContent(intPtr)
        elif (strName == "Spire.Doc.Documents.SDTInlineContent"):
            from spire.doc import SDTInlineContent
            ret = SDTInlineContent(intPtr)
        elif (strName == "Spire.Doc.Documents.StructureDocumentTag"):
            from spire.doc import StructureDocumentTag
            ret = StructureDocumentTag(intPtr)
        elif (strName == "Spire.Doc.Documents.StructureDocumentTagRow"):
            from spire.doc import StructureDocumentTagRow
            ret = StructureDocumentTagRow(intPtr)
        elif (strName == "Spire.Doc.Documents.StructureDocumentTagCell"):
            from spire.doc import StructureDocumentTagCell
            ret = StructureDocumentTagCell(intPtr)
        elif (strName == "Spire.Doc.Documents.StructureDocumentTagInline"):
            from spire.doc import StructureDocumentTagInline
            ret = StructureDocumentTagInline(intPtr)
        else:
            from spire.doc import DocumentObject
            ret = DocumentObject(intPtr)

        return ret

