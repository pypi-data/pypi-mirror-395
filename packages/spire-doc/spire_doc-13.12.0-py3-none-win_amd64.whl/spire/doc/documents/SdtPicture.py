from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class SdtPicture (  SdtControlProperties) :
    """
    Represents a picture control in a document.
    """
#
#    def ReplaceImage(self ,image:'Byte[]'):
#        """
#    <summary>
#         Replaces the image.
#    </summary>
#    <param name="image">The image.</param>
#        """
#        #arrayimage:ArrayTypeimage = ""
#        countimage = len(image)
#        ArrayTypeimage = c_void_p * countimage
#        arrayimage = ArrayTypeimage()
#        for i in range(0, countimage):
#            arrayimage[i] = image[i].Ptr
#
#
#        GetDllLibDoc().SdtPicture_ReplaceImage.argtypes=[c_void_p ,ArrayTypeimage]
#        GetDllLibDoc().SdtPicture_ReplaceImage(self.Ptr, arrayimage)


    @property

    def Type(self)->'SdtType':
        """
        Gets the type of the object, which is set to Picture.
        """
        GetDllLibDoc().SdtPicture_get_Type.argtypes=[c_void_p]
        GetDllLibDoc().SdtPicture_get_Type.restype=c_int
        ret = CallCFunction(GetDllLibDoc().SdtPicture_get_Type,self.Ptr)
        objwraped = SdtType(ret)
        return objwraped

