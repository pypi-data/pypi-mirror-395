from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class TextFormFieldType(Enum):
    """
    Specifies the type of a text form field.
    """

    # Text form field can contain any text.
    RegularText = 0
    # Text form field can contain only numbers.
    NumberText = 1
    # Text for field can contain only a valid date value. 
    DateText = 2
    # The text form field value is the current date when the field is updated.
    CurrentDate = 3
    # The text form field value is the current time when the field is updated.
    CurrentTime = 4
    # The text form field value is calculated from the expression specified in
    Calculation = 5
