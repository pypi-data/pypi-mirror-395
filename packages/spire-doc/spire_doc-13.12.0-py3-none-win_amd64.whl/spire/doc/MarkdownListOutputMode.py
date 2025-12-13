from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class MarkdownListOutputMode(Enum):
    """
    
    """
    
    #Produce list items formatted for Markdown syntax.
    MarkdownSyntax=0

    #Produce list items formatted for plain text.
    PlainText=1