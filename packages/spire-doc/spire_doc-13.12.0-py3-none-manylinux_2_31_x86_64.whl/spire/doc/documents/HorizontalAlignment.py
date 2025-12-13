from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class HorizontalAlignment(Enum):
    """
    Specifies the type of horizontal alignment.
    
    """

    # Specifies alignment to the left. 
    Left = 0
    # Specifies alignment to the center. 
    Center = 1
    # Specifies alignment to the right. 
    Right = 2
    # Specifies alignment to both left and right. 
    Justify = 3
    # Specifies that the text shall be justified between both
    # of the text margins in the document.
    Distribute = 4
    # Specifies that the text shall be justified with an optimization for Thai.
    ThaiDistribute = 5
    # Specifies that the kashida length for text in the current paragraph
    # shall be extended to its wides possible length.
    HightKashida = 6
    # Specifies that the kashida length for text in the current paragraph
    # shall be exended to a slightly longer length.
    # This setting shall also be applied to Arabic text when the both setting is applied.
    LowKashida = 7
    # Specifies that the kashida length for text in the current paragraph
    # shall be extended to a medium length determined by the consumer.
    MediumKashida = 8
