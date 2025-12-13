from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class MarkdownLinkOutputMode(Enum):
    """
    
    """    
    #Auto-detect link export formats.
    Auto=0
    #Serialize all links using inline Markdown syntax.
    Inline=1   
    # Serialize all links using reference Markdown syntax.   
    Reference=2