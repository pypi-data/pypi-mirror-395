from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class DocumentObjectType(Enum):
    """
    Specifies the type of a Document object type.
    """

    # Represents a document
    Document = 0
    # Section of document
    Section = 1
    # Body of document
    Body = 2
    # The header and footer of a document
    HeaderFooter = 3
    # The text body items
    Paragraph = 4
    #  Represents a structured document tag in a Word document, which is used to mark up content for custom XML data storage, form controls, or other structured data purposes.
    StructureDocumentTag = 5
    # Represents an inline-level structured document tag
    StructureDocumentTagInline = 6
    # Represents a row-level structured document tag
    StructureDocumentTagRow = 7
    # Represents a cell-level structured document tag
    StructureDocumentTagCell = 8
    # Block-Level Structure Document Tag Content
    SDTBlockContent = 9
    # Inline-Level Structure Document Tag Content
    SDTInlineContent = 10
    # Row-Level Structure Document Tag Content
    SDTRowContent = 11
    # Cell-Level Structure Document Tag Content
    SDTCellContent = 12
    # Represents a table structure that can store and manage data in rows and columns.
    Table = 13
    # Represents a row in a Table.
    TableRow = 14
    # Represents a cell in a table row.
    TableCell = 15
    # The range of text
    TextRange = 16
    # Represents a picture or image,
    Picture = 17
    # Represents the starting position of a field in a document.
    FieldStart = 18
    # Represents a field in a document.
    Field = 19
    # Represents a marker or indicator used to highlight or denote specific fields within a document
    FieldMark = 20
    # Represents the separator of a composite field.
    FieldSeparator = 21
    # Represents the end position of a field in a document.
    FieldEnd = 22
    # Represents a merge field in a document, which is a placeholder for data that will be inserted during a mail merge operation.
    MergeField = 23
    # Represents a field within a sequence, often used for unmbering.
    SeqField = 24
    # Represents an embedded field
    EmbededField = 25
    # Represents a control field
    ControlField = 26
    # Represents a text input form field
    TextFormField = 27
    # Represents a form field that allows users to select a value from a dropdown list.
    DropDownFormField = 28
    # Represents a checkbox from field
    CheckBox = 29
    # Represents the starting of a bookmark within a document
    BookmarkStart = 30
    # Represents the end of a bookmark in a document.
    BookmarkEnd = 31
    # The start of a region whose move source contents are part of a single named move.
    MoveFromRangeStart = 32
    # The end of a region whose move source contents are part of a single named move.
    MoveFromRangeEnd = 33
    # The start of a region whose move destination contents are part of a single named move.
    MoveToRangeStart = 34
    # The end of a region whose move destination contents are part of a single named move.
    MoveToRangeEnd = 35
    # Represents the start of a permission block
    PermissionStart = 36
    # Represents the end of a permission block
    PermissionEnd = 37
    # Represents shape object
    Shape = 38
    # Represents a group of shapes that can be manipulated together as a single unit.
    ShapeGroup = 39
    # Represents a line shape
    ShapeLine = 40
    # Represents a path that can be used to define the outline or boundary of a shape.
    ShapePath = 41
    # Represents a rectangle shape
    ShapeRect = 42
    # Represents a comment annotation.
    Comment = 43
    # Represents a footnote in a document
    Footnote = 44
    # Represents a text box
    TextBox = 45
    # Represents a break, such as page berak or column break
    Break = 46
    # Represents a special symbol character
    Symbol = 47
    # Table of Contents
    TOC = 48
    # Represents an XML paragraph item
    XmlParaItem = 49
    # Represents an undefined or unspecified object.
    Undefined = 50
    # Represents a comment mark.
    CommentMark = 51
    # Represents an OLE (Object Linking and Embedding) object
    OleObject = 52
    # Represents a custom XML data in a document
    CustomXml = 53
    # Represents a smart tag
    SmartTag = 54
    # Represents a mathematical object in a document, such as an equation or formula.
    OfficeMath = 55
    # Reserved for internal use by Spire.Words.
    System = 56
    # Phonetic Guide
    Ruby = 57
    # Indicates all Element types. Allows to select all children.
    Any = 58
    # Represents sub document
    SubDocument = 59
    # Represents a special character
    SpecialChar = 60
    # Represents glossary document.
    GlossaryDocument = 61
    # Represents a building block
    BuildingBlock = 62
    # Represents a form field
    FormField = 63
