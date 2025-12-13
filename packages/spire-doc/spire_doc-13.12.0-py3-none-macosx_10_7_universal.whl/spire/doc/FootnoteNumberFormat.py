from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class FootnoteNumberFormat(Enum):
    """
    Specifies Numberformat of FootEndNote. 

    """

    # Arabic format (1, 2, 3, ...).
    Arabic = 0
    # Upper case Roman format (I, II, III, ...) .
    UpperCaseRoman = 1
    # Lower case Roman format (i, ii, iii, ...) .
    LowerCaseRoman = 2
    # Upper case letters format (A, B, C, ...) .
    UpperCaseLetter = 3
    # Lower case letters format (a, b, c, ...) .
    LowerCaseLetter = 4
    # Chicago manual of style.
    Chicago = 9
    # Specifies that the sequence shall consist of full-width Arabic numbering.
    DecimalFullWidth = 14
    # Specifies that the sequence shall consist of Hebrew letters from the set listed below.
    Hebrew1 = 45
    # Specifies that the sequence shall consist of the Hebrew alphabet.
    Hebrew2 = 47
    # Specifies that the sequence shall consist of one or more occurrences of 
    # a single character int the Arabic alphabet from the set listed below. 
    ArabicAlpha = 46
    # Specifies that the sequence shall consist of one or more occurrences of 
    # a single ascending Abjad numerall from the set listed below. 
    ArabicAbjad = 48
    # Specifies that the sequence shall consist of one or more occurrences of
    # a single sequential number from the Chinese simplified legal format.
    ChineseLegalSimplified = 38
    # Specifies that the sequence shall consist of one or more occurrences of
    # a single sequential number from the Chinese counting thousand system.
    ChineseCountingThousand = 39
    # Specifies that the sequence shall consist of sequential numerical traditional ideographs.
    IdeographTraditional = 30
    #  Specifies that the sequence shall consist of sequential numerical zodiac ideographs.
    IdeographZodiac = 31
    # Identical to DecimalEnclosedCircle
    DecimalEnclosedCircleChinese = 28
    # Specifies that the sequence shall consist of sequential numerical ideographs.
    IdeographEnclosedCircle = 29
    # number format is none
    none = 255

