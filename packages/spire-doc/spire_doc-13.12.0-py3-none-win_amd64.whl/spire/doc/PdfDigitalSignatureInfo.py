from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class PdfDigitalSignatureInfo (SpireObject) :
    """
    Represents the details required for a digital signature in a PDF document.
    """
    @dispatch
    def __init__(self, certificatePath: str, securePassword: str, reason: str, location: str):
        """
        Initializes a new instance of the PdfDigitalSignatureInfo class.

        Returns:
            None
        """

        certificatePathPtr = StrToPtr(certificatePath)
        securePasswordPtr = StrToPtr(securePassword)
        reasonPtr = StrToPtr(reason)
        locationPtr = StrToPtr(location)

        GetDllLibDoc().PdfDigitalSignatureInfo_CreatePdfDigitalSignatureInfoPCSRL.argtypes=[c_char_p,c_char_p,c_char_p,c_char_p]
        GetDllLibDoc().PdfDigitalSignatureInfo_CreatePdfDigitalSignatureInfoPCSRL.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().PdfDigitalSignatureInfo_CreatePdfDigitalSignatureInfoPCSRL,certificatePathPtr, securePasswordPtr, reasonPtr, locationPtr)
        super(PdfDigitalSignatureInfo, self).__init__(intPtr)

    @property

    def Reason(self)->str:
        """
        Gets or sets the reason for the digital signature.
        """
        GetDllLibDoc().PdfDigitalSignatureInfo_get_Reason.argtypes=[c_void_p]
        GetDllLibDoc().PdfDigitalSignatureInfo_get_Reason.restype=c_void_p
        ret = PtrToStr(CallCFunction(GetDllLibDoc().PdfDigitalSignatureInfo_get_Reason,self.Ptr))
        return ret


    @Reason.setter
    def Reason(self, value:str):
        valuePtr=StrToPtr(value)
        GetDllLibDoc().PdfDigitalSignatureInfo_set_Reason.argtypes=[c_void_p, c_char_p]
        CallCFunction(GetDllLibDoc().PdfDigitalSignatureInfo_set_Reason,self.Ptr, valuePtr)

    @property

    def Location(self)->str:
        """
        Gets or sets the location where the digital signature is applied.
        """
        GetDllLibDoc().PdfDigitalSignatureInfo_get_Location.argtypes=[c_void_p]
        GetDllLibDoc().PdfDigitalSignatureInfo_get_Location.restype=c_void_p
        ret = PtrToStr(CallCFunction(GetDllLibDoc().PdfDigitalSignatureInfo_get_Location,self.Ptr))
        return ret


    @Location.setter
    def Location(self, value:str):
        valuePtr=StrToPtr(value)
        GetDllLibDoc().PdfDigitalSignatureInfo_set_Location.argtypes=[c_void_p, c_char_p]
        CallCFunction(GetDllLibDoc().PdfDigitalSignatureInfo_set_Location,self.Ptr, valuePtr)

    @property

    def SignatureDate(self)->'DateTime':
        """
        Gets or sets the date of the signature, stored in UTC time.
        """
        GetDllLibDoc().PdfDigitalSignatureInfo_get_SignatureDate.argtypes=[c_void_p]
        GetDllLibDoc().PdfDigitalSignatureInfo_get_SignatureDate.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().PdfDigitalSignatureInfo_get_SignatureDate,self.Ptr)
        ret = None if intPtr==None else DateTime(intPtr)
        return ret


    @SignatureDate.setter
    def SignatureDate(self, value:'DateTime'):
        GetDllLibDoc().PdfDigitalSignatureInfo_set_SignatureDate.argtypes=[c_void_p, c_void_p]
        CallCFunction(GetDllLibDoc().PdfDigitalSignatureInfo_set_SignatureDate,self.Ptr, value.Ptr)

    @property

    def HashAlgorithm(self)->'PdfDigitalSignatureHashAlgorithm':
        """
        Gets or sets the hash algorithm used for the digital signature.
        """
        GetDllLibDoc().PdfDigitalSignatureInfo_get_HashAlgorithm.argtypes=[c_void_p]
        GetDllLibDoc().PdfDigitalSignatureInfo_get_HashAlgorithm.restype=c_int
        ret = CallCFunction(GetDllLibDoc().PdfDigitalSignatureInfo_get_HashAlgorithm,self.Ptr)
        objwraped = PdfDigitalSignatureHashAlgorithm(ret)
        return objwraped

    @HashAlgorithm.setter
    def HashAlgorithm(self, value:'PdfDigitalSignatureHashAlgorithm'):
        GetDllLibDoc().PdfDigitalSignatureInfo_set_HashAlgorithm.argtypes=[c_void_p, c_int]
        CallCFunction(GetDllLibDoc().PdfDigitalSignatureInfo_set_HashAlgorithm,self.Ptr, value.value)

    @property

    def TimestampConfiguration(self)->'PdfDigitalSignatureTimestampConfiguration':
        """
        Gets or sets the timestamp configuration for the digital signature.
        """
        GetDllLibDoc().PdfDigitalSignatureInfo_get_TimestampConfiguration.argtypes=[c_void_p]
        GetDllLibDoc().PdfDigitalSignatureInfo_get_TimestampConfiguration.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().PdfDigitalSignatureInfo_get_TimestampConfiguration,self.Ptr)
        ret = None if intPtr==None else PdfDigitalSignatureTimestampConfiguration(intPtr)
        return ret


    @TimestampConfiguration.setter
    def TimestampConfiguration(self, value:'PdfDigitalSignatureTimestampConfiguration'):
        GetDllLibDoc().PdfDigitalSignatureInfo_set_TimestampConfiguration.argtypes=[c_void_p, c_void_p]
        CallCFunction(GetDllLibDoc().PdfDigitalSignatureInfo_set_TimestampConfiguration,self.Ptr, value.Ptr)

