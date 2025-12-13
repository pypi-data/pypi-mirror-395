from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class PdfPageLayout(Enum):
    """
    Specifies the page layout to be used when the document is opened in a PDF reader.
    """

    
    #Default display view of the PDF reader.
    Default=0
    #Display one page at a time.
    SinglePage=1
    #Display the pages in one column.
    OneColumn=2
    #Display the pages in two columns= with odd-numbered pages on the left.
    TwoColumnLeft=3
    #Display the pages in two columns= with odd-numbered pages on the right.
    TwoColumnRight=4
    #Display the pages two at a time= with odd-numbered pages on the left.
    TwoPageLeft=5
    #Display the pages two at a time= with odd-numbered pages on the right.
    TwoPageRight=6

