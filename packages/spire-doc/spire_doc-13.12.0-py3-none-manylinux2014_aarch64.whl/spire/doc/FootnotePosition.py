from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class FootnotePosition(Enum):
    """
    Enum class that specifies the position of a footnote.
    
    """

    # Endnotes are output at the end of the section.
    PrintAsEndOfSection = 0
    # Footnotes are output at the bottom of each page. 
    PrintAtBottomOfPage = 1
    # Footnotes are output beneath text on each page. 
    PrintImmediatelyBeneathText = 2
    # Endnotes are output at the end of the document. Valid for endnotes only.
    PrintAsEndOfDocument = 3
