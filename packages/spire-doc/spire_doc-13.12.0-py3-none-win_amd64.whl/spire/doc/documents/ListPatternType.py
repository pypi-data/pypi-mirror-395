from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class ListPatternType(Enum):
    """
    Specifies type of the list numbering format.
    """

    # Specifies default numbering format.
    # Arabic numbering (1, 2, 3, ...)
    Arabic = 0
    # Specifies UppRoman numbering format.
    # Upper case Roman (I, II, III, ...)
    UpRoman = 1
    # Specifies LowRoman numbering format.
    #  Lower case Roman (i, ii, iii, ...)
    LowRoman = 2
    # Specifies UpLetter numbering format.
    # Upper case Letter (A, B, C, ...)
    UpLetter = 3
    # Specifies LowLetter numbering format.
    #  Lower case letter (a, b, c, ...)
    LowLetter = 4
    # Specifies Ordinal numbering format.
    # Ordinal (1st, 2nd, 3rd, ...)
    Ordinal = 5
    # Specifies Cardinal Text numbering format.
    #  Numbered (One, Two, Three, ...)
    CardinalText = 6
    # Specifies Ordinal Text numbering format.
    # Ordinal (text) (First, Second, Third, ...)
    OrdinalText = 7
    # Chicago manual of style.
    Chicago = 9
    # Specifies that the sequence shall consist of full-width Arabic numbering.
    DecimalFullWidth = 14
    # Specifies that the sequence shall consist of half-width Arabic numbering.
    DecimalHalfWidth = 15
    # Specifies that the sequence shall consist of Hebrew letters from the set listed below.
    Hebrew1 = 45
    # Specifies that the sequence shall consist of one or more occurrences of 
    # a single character int the Arabic alphabet from the set listed below. 
    ArabicAlpha = 46
    # Specifies that the sequence shall consist of the Hebrew alphabet.
    Hebrew2 = 47
    # Specifies that the sequence shall consist of one or more occurrences of 
    # a single ascending Abjad numerall from the set listed below. 
    ArabicAbjad = 48
    # Specifies that the sequence shall consist of sequential numbers from
    # the Japanese counting system.
    JapaneseCounting = 11
    # Specifies that the sequence shall consist of sequential numbers from
    # the Japanese legal counting system.
    JapaneseLegal = 16
    # Specifies that the sequence shall consist of sequential numbers from
    # the Japanese digital the thousand counting system.
    JapaneseDigitalTenThousand = 17
    # Specifies that the sequence shall consist of sequential numbering enclosed
    # in a circle,using the enclosed character.
    DecimalEnclosedCircle = 18
    DecimalFullWidth2 = 19
    # Specifies LeadingZero numbering format.
    LeadingZero = 22
    # Specifies Bullet numbering format.
    Bullet = 23
    # Decimal numbers followed by a period.
    # Specifies that the sequence shall consist of decimal numbering followed
    # by a period,using the appropriate character,as described below.
    DecimalEnclosedFullstop = 26
    # Decimal numbers enclosed in parenthesis.
    # Specifies that the sequence shall consist of decimal numbering enclosed in parentheses.
    DecimalEnclosedParen = 27
    # Identical to DecimalEnclosedCircle
    DecimalEnclosedCircleChinese = 28
    # Korean Digital Counting System.
    # Specifies that the sequence shall consist of sequential numbers from
    # the Korean digital counting system.
    KoreanDigital = 41
    # Korean Counting System.
    # Specifies that the sequence shall consist of sequential numbers from
    # the Korean counting system.
    KoreanCounting = 42
    # Korean Legal numbering.
    # Specifies that the sequence shall consist of sequential numbers from
    # the Korean legal numbering system.
    KoreanLegal = 43
    # Korean Digital Counting System Alternate.
    # Specifies that the sequence shall consist of sequential numbers from
    # the Korean digital counting system. 
    KoreanDigital2 = 44
    # Specifies that the sequence shal consist of one or more occurrences of a single
    # full-width katakana character,in the traditonal a-i-u-e-o order.
    AiueoFullWidth = 20
    # <para>Specifies that the sequence shall consist of one or more occurrences of a single </para>
    # <para>half-width katakana character from the set listed below, in the traditional</para>
    # <para>a-i-u-e-o order.</para>
    Aiueo = 12
    # Specifies that the sequence shall consist of the iroha.
    Iroha = 13
    # Specifies that the sequence shall consist of sequential numerical ideographs, using the appropriate character,
    # as described below.
    IdeographDigital = 10
    # Specifies that the sequence shall consist of the full-width forms of the iroha.
    IrohaFullWidth = 21
    # Specifies that the sequence shall consist of sequential numerical traditonal ideographs.
    IdeographTraditional = 30
    # Specifies that the sequence shall consist of sequential numerical zodiac ideographs.
    IdeographZodiac = 31
    # Specifies that the sequence shall consist of sequential numerical ideographs.
    IdeographEnclosedCircle = 29
    # Specifies that the sequence shall consist of sequential traditional zodiac ideographs.
    IdeographZodiacTraditional = 32
    #Specifies that the sequence shall consist of sequential numbers from the Taiwanese counting system.
    TaiwaneseCounting = 33
    # Specifies that the sequence shall consist of sequential numerical traditional legal ideographs.
    IdeographLegalTraditional = 34
    # Specifies that the sequence shall consist of sequential numbers from the Taiwanese counting thousand system.
    TaiwaneseCountingThousand = 35
    # Specifies that the sequence shall consist of sequential numbers from the Taiwanese digital counting system.
    TaiwaneseDigital = 36
    # Specifies that the sequence shall consist of one or more occurrences of
    # a single ascending number from the chinese counting system.
    ChineseCounting = 37
    # Specifies that the sequence shall consist of one or more occurrences of
    # a single sequential number from the Chineses simplified legal format.
    ChineseLegalSimplified = 38
    # Specifies that the sequence shall consist of one or more occurrences of
    # a single sequential number from the Chineses counting thousand system.
    ChineseCountingThousand = 39
    Special = 58
    # Page number format
    NumberInDash = 57
    # Specifies None numbering format.
    none = 255
    # Specifies custom format.
    CustomType = 65280

