from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class MarkdownOfficeMathOutputMode(Enum):
    """
    
    """    

    #Serialize OfficeMath to plaint text.
    Text=0
    #Serialize OfficeMath to Image.
    Image=1
    #Serialize OfficeMath to MathML.
    MathML=2