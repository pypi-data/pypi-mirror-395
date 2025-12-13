from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class WidthType(Enum):
    """
    The TableWidthType enum specifies how the preferred width for a table,
    table indent, table cell, cell margin, or cell spacing is defined.
    """

    # No Preffered Width
    none = 0
    # No preferred width is specified.
    # The width is derived from other table measurements where a preferred size is specified, 
    # as well as from the size of the table contents, and the constraining size of the
    # container of the table.
    Auto = 1
    # When specifying the preferred width of a portion of a table,
    # such as a cell, spacing or indent, the percentage is relative
    # to the width of the entire table.
    # When specifying the preferred width of an entire table, 
    # the percentage is relative to the width of the page, 
    # less any margin or gutter space. Alternatively, 
    # if the table is nested inside another table, 
    # the percentage is relative to the width of the cell 
    # in the containing table, less cell margins.
    Percentage = 2
    # The preferred width of the table, indent, cell, 
    # cell margin, or cell spacing is an absolute width measured in twips.
    Twip = 3

