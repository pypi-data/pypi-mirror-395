from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class HeaderFooterType(Enum):
    """
    Specifies type of the Header/Footer.
    """

    # Header for even numbered pages.
    HeaderEven = 0
    # Header for odd numbered pages.
    HeaderOdd = 1
    # Footer for even numbered pages.
    FooterEven = 2
    # Footer for odd numbered pages.
    FooterOdd = 3
    # Header for the first page of the section. 
    HeaderFirstPage = 4
    # Footer for the first page of the section. 
    FooterFirstPage = 5

