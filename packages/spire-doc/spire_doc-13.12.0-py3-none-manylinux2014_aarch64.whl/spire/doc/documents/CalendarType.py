from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class CalendarType(Enum):
    """
    Enum class representing different calendar types.
    """

    # Used as default value in Docx. Equals <see cref="Gregorian"/>.
    Default = 0
    # This calendar should be localized into the appropriate language.
    Gregorian = 0
    # The values for this calendar should be presented in Arabic.
    GregorianArabic = 1
    # The values for this calendar should be presented in Middle East French.
    GregorianMiddleEastFrench = 2
    # The values for this calendar should be presented in English.
    GregorianEnglish = 3
    # The values for this calendar should be the representation of the English strings in the corresponding Arabic characters 
    # (the Arabic transliteration of the English for the Gregorian calendar).
    GregorianTransliteratedEnglish = 4
    # The values for this calendar should be the representation of the French strings in the corresponding Arabic characters 
    # (the Arabic transliteration of the French for the Gregorian calendar).
    GregorianTransliteratedFrench = 5
    # Specifies that the Hebrew lunar calendar, as described by the Gauss formula for Passover [CITATION] 
    # and The Complete Restatement of Oral Law (Mishneh Torah),shall be used.
    Hebrew = 6
    # Specifies that the Hijri lunar calendar, as described by the Kingdom of Saudi Arabia, 
    # Ministry of Islamic Affairs, Endowments, Dawah and Guidance, shall be used.
    Hijri = 7
    # Specifies that the Japanese Emperor Era calendar, as described by 
    # Japanese Industrial Standard JIS X 0301, shall be used.
    Japan = 8
    # Specifies that the Korean Tangun Era calendar, 
    # as described by Korean Law Enactment No. 4, shall be used.
    Korean = 9
    # Specifies that no calendar should be used.
    none = 10
    # Specifies that the Saka Era calendar, as described by the Calendar Reform Committee of India, 
    # as part of the Indian Ephemeris and Nautical Almanac, shall be used.
    Saka = 11
    # Specifies that the Taiwanese calendar, as defined by the Chinese National Standard CNS 7648, shall be used.
    Taiwan = 12
    # Specifies that the Thai calendar, as defined by the Royal Decree of H.M. King Vajiravudh (Rama VI) in 
    # Royal Gazette B. E. 2456 (1913 A.D.) and by the decree of Prime Minister Phibunsongkhram (1941 A.D.) to 
    # start the year on the Gregorian January 1 and to map year zero to Gregorian year 543 B.C., shall be used.
    Thai = 13
