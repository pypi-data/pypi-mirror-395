from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class MarkdownSaveAsHtml(Enum):
    """
    
    """    

    #Output entire content using pure Markdown syntax with no HTML passthrough.
    none = 0
    #Output tables as unprocessed HTML.
    Tables=1