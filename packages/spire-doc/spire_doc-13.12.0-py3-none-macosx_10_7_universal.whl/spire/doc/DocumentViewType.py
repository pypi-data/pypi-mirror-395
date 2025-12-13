from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class DocumentViewType(Enum):
    """
    Enum class that specifies view mode in Microsoft Word.

    """

    # Specifies that the document will be rendered in the default view of the application.
    none = 0
    # Everything that will appear in the printed document appears on the screen.
    PrintLayout = 1
    # Shows the headings and subheadings in the word document.
    OutlineLayout = 3
    # Document appears with a dotted line separating the pages and/or document sections.
    # Columns, drawings, headers/footers, footnotes/endnotes, and comments do not appear. 
    NormalLayout = 4
    # Designed to show the word document will look as a web page.
    WebLayout = 5
