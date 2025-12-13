from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class LineDashing(Enum):
    """
    Enum class representing different line dashing styles.

    """

    # Solid (continuous) pen.
    Solid = 0
    # PS_DASH system dash style.
    Dash = 1
    # PS_DOT system dash style.
    Dot = 2
    # PS_DASHDOT system dash style.
    DashDot = 3
    # PS_DASHDOTDOT system dash style.
    DashDotDot = 4
    # Square dot style.
    DotGEL = 5
    # Dash style.
    DashGEL = 6
    # Long dash style.
    LongDashGEL = 7
    # Dash short dash.
    DashDotGEL = 8
    # Long dash short dash.
    LongDashDotGEL = 9
    # Long dash short dash short dash.
    LongDashDotDotGEL = 10
    # Same as <see cref="Solid"/>.
    Default = 0
