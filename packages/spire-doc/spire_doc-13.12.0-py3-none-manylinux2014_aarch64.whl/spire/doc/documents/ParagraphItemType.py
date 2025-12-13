from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class ParagraphItemType(Enum):
    """
    Specifies the type of the ParagraphBase.
    """

    # ParagraphBase is a text.
    TextRange = 0
    # ParagraphBase is a picture.
    Picture = 1
    # ParagraphBase is a field.
    Field = 2
    # Paragraph item is field mark.
    FieldMark = 3
    # ParagraphBase is a merge field
    MergeField = 4
    # ParagraphBase is a a form field
    FormField = 5
    # ParagraphBase is a a checkbox
    CheckBox = 6
    TextFormField = 7
    # ParagraphBase is a drop-down form field.
    DropDownFormField = 8
    # ParagraphBase is a sequence field
    SeqField = 9
    # ParagraphBase is a embedded field
    EmbedField = 10
    # Paragraph item is form control field.
    ControlField = 11
    # ParagraphBase is a start of bookmark.
    BookmarkStart = 12
    # ParagraphBase is a end of bookmark.
    BookmarkEnd = 13
    # ParagraphBase is a start of Permission
    PermissionStart = 14
    # ParagraphBase is a end of Permission.
    PermissionEnd = 15
    # ParagraphBase is a shape object.
    ShapeObject = 16
    # ParagraphBase is a group of shapes.
    ShapeGroup = 17
    # ParagraphBase is a comment.
    Comment = 18
    # Paragraph item is comment mark.
    CommentMark = 19
    # ParagraphBase is a footnote.
    Footnote = 20
    # ParagraphBase is a textbox. 
    TextBox = 21
    # PragraphItem is a break.
    Break = 22
    # ParagraphBase is a symbol.
    Symbol = 23
    # ParagraphBase is a Table of Contents
    TOC = 24
    # ParagraphBase is an OLE object
    OleObject = 25
