from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class WordAttrCollection (  AttrCollection) :
    """
    Collection of attribute values that can have formatting revision.
    """
