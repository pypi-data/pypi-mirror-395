from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class TableTextAlignment(Enum):
    """
    The alignment of the text of the table.
    """
    
    #Default alignment for table text.
    Auto=0       
    #The table text is aligned to the Left.
    Left=1       
    #The table text is aligned to the Center.
    Center=2        
    #The table text is aligned to the Right.
    Right=3
    
