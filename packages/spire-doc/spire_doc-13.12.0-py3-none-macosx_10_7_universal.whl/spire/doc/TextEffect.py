from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class TextEffect(Enum):
    """
    Animation effect for text.
    """

    # specifies no animation.
    none = 0
    # Specifies that this text shall be surrounded by a border consisting of a series of
    # colored lights, which constantly change colors in sequence.
    LasVegasLights = 1
    # Specifies that this text shall be surrounded by a background 
    # color which alternates between black and white.
    BlinkingBackground = 2
    # Specifies that this text shall have a background consisting of a random pattern of
    # colored lights, which constantly change colors in sequence.
    SparkleText = 3
    # Specifies that this text shall be surrounded by an animated black dashed line border.
    MarchingBlackAnts = 4
    # Specifies that this text shall be surrounded by an animated red dashed line border.
    MarchingRedAnts = 5
    # Specifies that this text shall be animated by alternating between normal and blurry states.
    Shimmer = 6
