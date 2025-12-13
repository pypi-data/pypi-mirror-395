from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class DocumentSerializable (  OwnerHolder) :
    """
    Represents a base class for document serializable objects, inheriting from OwnerHolder and implementing IDocumentSerializable.
    """


