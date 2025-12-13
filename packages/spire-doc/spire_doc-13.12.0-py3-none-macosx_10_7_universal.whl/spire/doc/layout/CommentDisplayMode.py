from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class CommentDisplayMode(Enum):
    """
    Specifies the rendering mode for document comments.
    """

    # No document comments are rendered.
    Hide = 0
    # Renders document comments in balloons in the margin. This is the default value.
    ShowInBalloons = 1
    # Renders document comments in annotations. This is only available for Pdf format.
    ShowInAnnotations = 2

