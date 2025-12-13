from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class SdtAppearance(Enum):
    """
    Enum class representing the appearance of an Sdt object.

    """

    # The appearance option of SDT is Bounding Box.
    BoundingBox = 0
    # The appearance option of SDT is tags.
    Tags = 1
    # The appearance option of SDT is hidden, typically not visible or accessible to user.
    Hidden = 2
    # Represents the default appearance of SDT(BoundingBox).
    Default = 0
