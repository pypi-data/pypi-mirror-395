from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class HorizontalOrigin(Enum):
    """
    Enum class for specifying object's horizontal origin.
    
    """

    # The object is positioned relative to the left side of the column.
    Column = 2
    # Specifies that the horizontal positioning shall be relative to the page margins.
    Margin = 0
    # The object is positioned relative to the left edge of the page.
    Page = 1
    # The object is positioned relative to the left side of the paragraph.
    Character = 3
    # Specifies that the horizontal positioning shall be relative to the left margin of the page.
    LeftMarginArea = 4
    # Specifies that the horizontal positioning shall be relative to the right margin of the page.
    RightMarginArea = 5
    # Specifies that the horizontal positioning shall be relative to the inside margin of the 
    # current page (the left margin on odd pages, right on even pages).
    InnerMarginArea = 6
    # Specifies that the horizontal positioning shall be relative to the outside margin of the 
    # current page (the right margin on odd pages, left on even pages).
    OuterMarginArea = 7
    # Default value is <see cref="Column"/>.
    Default = 2
