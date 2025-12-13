from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class OfficeMath (  ParagraphBase, ICompositeObject) :
    """
    Defines the Office Math class such as function, equation
    """
    @dispatch
    def __init__(self, doc:'IDocument'):
        """
        """
        intPdoc:c_void_p = doc.Ptr

        GetDllLibDoc().OfficeMath_CreateOfficeMathD.argtypes=[c_void_p]
        GetDllLibDoc().OfficeMath_CreateOfficeMathD.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().OfficeMath_CreateOfficeMathD,intPdoc)
        super(OfficeMath, self).__init__(intPtr)

    """
    Represents an OfficeMath object in a document.
    """
    @property

    def DocumentObjectType(self)->'DocumentObjectType':
        """
        Gets the type of the document object.
        :return: The type of the document object.
        """
        GetDllLibDoc().OfficeMath_get_DocumentObjectType.argtypes=[c_void_p]
        GetDllLibDoc().OfficeMath_get_DocumentObjectType.restype=c_int
        ret = CallCFunction(GetDllLibDoc().OfficeMath_get_DocumentObjectType,self.Ptr)
        objwraped = DocumentObjectType(ret)
        return objwraped

    @property

    def ParentParagraph(self)->'Paragraph':
        """
        Gets the parent paragraph.
        :return: The parent paragraph.
        """
        GetDllLibDoc().OfficeMath_get_ParentParagraph.argtypes=[c_void_p]
        GetDllLibDoc().OfficeMath_get_ParentParagraph.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().OfficeMath_get_ParentParagraph,self.Ptr)
        ret = None if intPtr==None else Paragraph(intPtr)
        return ret



    def FromMathMLCode(self ,mathCode:str):
        """
        Creates an OfficeMath object from MathML code.
        :param mathCode: The MathML code.
        """
        mathMLCodePtr = StrToPtr(mathCode)
        GetDllLibDoc().OfficeMath_FromMathMLCode.argtypes=[c_void_p ,c_char_p]
        CallCFunction(GetDllLibDoc().OfficeMath_FromMathMLCode,self.Ptr, mathMLCodePtr)


    def FromOMMLCode(self ,ommlCode:str):
        """
        Parses OMML (Office MathML) code strings and update the current object.

        ommlCode: The OMML code string.
        """
        ommlCodePtr = StrToPtr(ommlCode)
        GetDllLibDoc().OfficeMath_FromOMMLCode.argtypes=[c_void_p ,c_char_p]
        CallCFunction(GetDllLibDoc().OfficeMath_FromOMMLCode,self.Ptr, ommlCodePtr)


    def FromLatexMathCode(self ,latexMathCode:str):
        """
        Creates an OfficeMath object from LaTeX math code.
        :param latexMathCode: The LaTeX math code.
        """
        latexMathCodePtr = StrToPtr(latexMathCode)
        GetDllLibDoc().OfficeMath_FromLatexMathCode.argtypes=[c_void_p ,c_char_p]
        CallCFunction(GetDllLibDoc().OfficeMath_FromLatexMathCode,self.Ptr, latexMathCodePtr)

    @staticmethod
    def FromEqField(eqField: 'Field')->'OfficeMath':
        """
        Creates an OfficeMath object from eqField.
        """
        eqFieldPtr:c_void_p = eqField.Ptr
        GetDllLibDoc().OfficeMath_FromEqField.argtypes=[c_void_p]
        GetDllLibDoc().OfficeMath_FromEqField.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().OfficeMath_FromEqField, eqFieldPtr)
        ret = None if intPtr==None else OfficeMath(intPtr)
        return ret

    @dispatch

    def SaveImageToStream(self ,imageType: ImageType)->Stream:
        """
        Save the specified page as image return stream.
        The default is PNG format image.

        Args:
            type (ImageType): The type.

        Returns:
            Stream: The stream.
        """
        enumtype:c_int = imageType.value

        GetDllLibDoc().OfficeMath_SaveImageToStream.argtypes=[c_void_p ,c_int]
        GetDllLibDoc().OfficeMath_SaveImageToStream.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().OfficeMath_SaveImageToStream,self.Ptr, enumtype)
        ret = None if intPtr==None else Stream(intPtr)
        return ret

    def ToMathMLCode(self)->str:
        """
        Converts the OfficeMath object to MathML code.
        return: The MathML code.
        """
        GetDllLibDoc().OfficeMath_ToMathMLCode.argtypes=[c_void_p]
        GetDllLibDoc().OfficeMath_ToMathMLCode.restype=c_void_p
        ret = PtrToStr(CallCFunction(GetDllLibDoc().OfficeMath_ToMathMLCode,self.Ptr))
        return ret

    def ToOfficeMathMLCode(self)->str:
        """
        Converts the OfficeMath object to OfficeMathML code.
        return: The OfficeMathML code.
        """
        GetDllLibDoc().OfficeMath_ToOfficeMathMLCode.argtypes=[c_void_p]
        GetDllLibDoc().OfficeMath_ToOfficeMathMLCode.restype=c_void_p
        ret = PtrToStr(CallCFunction(GetDllLibDoc().OfficeMath_ToOfficeMathMLCode,self.Ptr))
        return ret


    def ToLaTexMathCode(self)->str:
        """
        Converts the current math object to LaTeX math code.

        returns: The LaTeX representation of the math object.
        """
        GetDllLibDoc().OfficeMath_ToLaTexMathCode.argtypes=[c_void_p]
        GetDllLibDoc().OfficeMath_ToLaTexMathCode.restype=c_char_p
        ret = PtrToStr(CallCFunction(GetDllLibDoc().OfficeMath_ToLaTexMathCode,self.Ptr))
        return ret

    @property

    def ChildObjects(self)->'DocumentObjectCollection':
        """
        Gets the child objects of the OfficeMath object.
        return: The child objects.
        """
        GetDllLibDoc().OfficeMath_get_ChildObjects.argtypes=[c_void_p]
        GetDllLibDoc().OfficeMath_get_ChildObjects.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().OfficeMath_get_ChildObjects,self.Ptr)
        ret = None if intPtr==None else DocumentObjectCollection(intPtr)
        return ret