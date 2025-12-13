from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class SdtType(Enum):
    """
    Specifies the type of a structured document tag (SDT) Element.
    """

    # No type is assigned to the SDT.
    # If no type element is specified, the SDT structured document tag should be a rich text box.
    none = 0
    # The SDT represents a rich text box when displayed in the document.
    RichText = 1
    # The SDT represents a bibliography entry. 
    Bibliography = 2
    # The SDT represents a citation.
    Citation = 3
    # The SDT represents a combo box when displayed in the document.
    ComboBox = 4
    # The SDT represents a drop down list when displayed in the document.
    DropDownList = 5
    # The SDT represents a picture when displayed in the document.
    Picture = 6
    # The SDT represents a plain text box when displayed in the document.
    Text = 7
    # The SDT represents an equation.
    Equation = 8
    # The SDT represents a date picker when displayed in the document.
    DatePicker = 9
    # The SDT represents a building block gallery type.
    BuildingBlockGallery = 10
    # The SDT represents a document part type.
    DocPartObj = 11
    # The SDT represents a restricted grouping when displayed in the document.
    Group = 12
    # The SDT represents a checkbox when displayed in the document.
    CheckBox = 13
    # The SDT represents a repeating section when displayed in the document.
    RepeatingSection = 14
    # The SDT represents a entity picker when displayed in the document.
    EntityPicker = 15
