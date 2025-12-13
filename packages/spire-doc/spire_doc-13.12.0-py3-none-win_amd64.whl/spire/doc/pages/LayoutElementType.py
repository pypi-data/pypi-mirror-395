from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc.pages import *
from spire.doc import *
from ctypes import *
import abc

class LayoutElementType(Enum):
    """
    Types of the layout entities.
    """

    # Default value.
    none = 0
    # Represents page of a document.
    # Page may have <see cref="Column" />, <see cref="HeaderFooter" /> and <see cref="Comment" /> child entities.
    Page = 1
    # Represents a column of text on a page.
    # Column may have the same child entities as <see cref="Cell" />, plus <see cref="Footnote" />,
    # <see cref="Endnote" /> and <see cref="NoteSeparator" /> entities.
    Column = 2
    # Represents a table row.
    # Row may have <see cref="Cell" /> as child entities.
    Row = 8
    # Represents a table cell.
    # Cell may have <see cref="Line" /> and <see cref="Row" /> child entities.
    Cell = 16
    # Represents line of characters of text and inline objects.
    # Line may have <see cref="Span" /> child entities.
    Line = 32
    # Represents one or more characters in a line.
    # This include special characters like field start/end markers, bookmarks and comments.
    # Span may not have child entities.
    Span = 64
    # Represents placeholder for footnote content.
    # Footnote may have <see cref="Line" /> and <see cref="Row" /> child entities.
    Footnote = 256
    # Represents placeholder for endnote content.
    # Endnote may have <see cref="Line" /> and <see cref="Row" /> child entities.
    Endnote = 512
    # Represents placeholder for header/footer content on a page.
    # HeaderFooter may have <see cref="Line" /> and <see cref="Row" /> child entities.
    HeaderFooter = 1024
    # Represents text area inside of a shape.
    # Textbox may have <see cref="Line" /> and <see cref="Row" /> child entities.
    TextBox = 2048
    # Represents placeholder for comment content.
    # Comment may have <see cref="Line" /> and <see cref="Row" /> child entities.
    Comment = 4096
    # Represents footnote/endnote separator.
    # NoteSeparator may have <see cref="Line" /> and <see cref="Row" /> child entities.
    NoteSeparator = 8192

