from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class TextDirection(Enum):
    """
    Enum class that defines the direction of text.

    """

    # Specifies that text in the parent object shall flow from left to right horizontally,
    # then top to bottom vertically on the page.
    # This means that horizontal lines are filled before the text expands vertically.
    # TextOrientation.Horizontal
    TopToBottom = 0
    # Specifies that text in the parent object shall flow from right to left horizontally, 
    # then top to bottom vertically on the page.
    # This means that horizontal lines are filled before the text expands vertically.
    #TextOrientation.Downward
    RightToLeft = 3
    # Specifies that text in the parent object shall flow from top to bottom vertically,
    # then left to right horizontally on the page.
    # This means that horizontal lines are filled before the text expands vertically.
    # This flow is also rotated such that all text is rotated 90 degrees when displayed on a page.
    LeftToRightRotated = 5
    # Specifies that text in the parent object shall flow from bottom to top vertically,
    # then from left to right horizontally on the page.
    # TextOrientation.Upward
    LeftToRight = 2
    # Specifies that text in the parent object shall flow from left to right horizontally,
    # then top to bottom vertically on the page.
    # This means that horizontal lines are filled before the text expands vertically.
    # This flow is also rotated such that any East Asian text shall be rotated 270 degrees when displayed on a page.
    # TextOrientation.HorizontalRotatedFarEast
    TopToBottomRotated = 4
    # Specifies that text in the parent object shall flow from top to bottom vertically, 
    # then right to left horizontally on the page.
    # This means that horizontal lines are filled before the text expands vertically.
    # This flow is also rotated such that all text is rotated 90 degrees when displayed on a page.
    # TextOrientation.VerticalFarEast
    RightToLeftRotated = 1
