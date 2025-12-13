from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class CharacterSpacing(Enum):
    """
    Enum for controlling character spacing.

    """

    # Don't compress punctuation.
    doNotCompress = 0
    # Compress punctuation.
    compressPunctuation = 1
    # Compress punctuation and japanese kana.
    compressPunctuationAndJapaneseKana = 2
