from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class OverrideLevelFormat (  DocumentSerializable) :
    """
    Represents a class for overriding the level format in a document serialization process.
    """
