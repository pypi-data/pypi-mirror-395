from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class ListTemplate(Enum):
    """
    List template styles
    """

    #Default bullet style
    BulletDefault = 0
    #Bullet disk style (alias for BulletDefault)
    BulletDisk = 0
    #Bullet circle style
    BulletCircle = 1
    #Bullet square style
    BulletSquare = 2
    #Bullet diamonds style
    BulletDiamonds = 5
    #Bullet arrow head style
    BulletArrowHead = 6
    #Bullet tick style (checkmark)
    BulletTick = 7
    #Default number style
    NumberDefault = 8
    #Number Arabic dot style (alias for NumberDefault)
    NumberArabicDot = 8
    #Number Arabic parenthesis style
    NumberArabicParenthesis = 9
    #Uppercase Roman numeral with dot style
    NumberUppercaseRomanDot = 10
    #Uppercase letter with dot style
    NumberUppercaseLetterDot = 11
    #Lowercase letter with parenthesis style
    NumberLowercaseLetterParenthesis = 12
    #Lowercase letter with dot style
    NumberLowercaseLetterDot = 13
    #Lowercase Roman numeral with dot style
    NumberLowercaseRomanDot = 14
    #Outline numbers style
    OutlineNumbers = 15
    #Legal outline style
    OutlineLegal = 16
    #Bullet outline style
    OutlineBullets = 17
    #Article/section heading outline style
    OutlineHeadingsArticleSection = 18
    #Legal heading outline style
    OutlineHeadingsLegal = 19
    #Numbered heading outline style
    OutlineHeadingsNumbers = 20
    #Chapter heading outline style
    OutlineHeadingsChapter = 21
    
