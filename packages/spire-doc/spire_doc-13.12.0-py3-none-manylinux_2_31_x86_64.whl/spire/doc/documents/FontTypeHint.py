from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class FontTypeHint(Enum):
    """
    Enumeration that defines the font type hint.
    
    """

    # Use sprmCRgLid0 (or sprmCRgLid0_80) for language. 
    # Use sprmCRgFtc0 for font if the character is between 0x0020 and 0x007F, inclusive. 
    # Otherwise, use sprmCRgFtc2. Use sprmCHps for size, sprmCFBold for bold, and sprmCFItalic for italic.
    # High ANSI Font.
    Default = 0
    # Use sprmCRgLid1 (or sprmCRgLid1_80) for language, sprmCRgFtc1 for font, sprmCHps for size, 
    # sprmCFBold for bold, and sprmCFItalic for italic.
    # East Asian Font.
    EastAsia = 1
    # Use sprmCLidBi for language, sprmCFtcBi for font, sprmCHpsBi for size, sprmCFBoldBi for bold,
    # and sprmCFItalicBi for italic.
    # Complex Script Font.
    ComplexScript = 2
