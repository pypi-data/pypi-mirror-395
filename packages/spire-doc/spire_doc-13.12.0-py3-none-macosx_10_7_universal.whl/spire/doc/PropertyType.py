from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class PropertyType(Enum):
    """
    Specifies Type of the Property.
    """

    # Specifies Property Type as Summary.
    Summary = 0
    # Specifies Property Type as DocumentSummary.
    DocumentSummary = 1
    # Specifies Property Type as Custom.
    Custom = 2

