from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class PdfDigitalSignatureTimestampConfiguration (SpireObject) :
    """
    Represents the configuration settings for a timestamp service used in a digital signature of a PDF document.
    """
    @dispatch
    def __init__(self, serverUrl: str, userName: str, password: str):
        """
        Initializes a new instance of the PdfDigitalSignatureTimestampConfiguration class.

        Returns:
            None
        """
        serverUrlPtr = StrToPtr(serverUrl)
        userNamePtr = StrToPtr(userName)
        passwordPtr = StrToPtr(password)

        GetDllLibDoc().PdfDigitalSignatureTimestampConfiguration_CreatePdfDigitalSignatureTimestampConfigurationSUP.argtypes=[c_char_p,c_char_p,c_char_p,]
        GetDllLibDoc().PdfDigitalSignatureTimestampConfiguration_CreatePdfDigitalSignatureTimestampConfigurationSUP.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().PdfDigitalSignatureTimestampConfiguration_CreatePdfDigitalSignatureTimestampConfigurationSUP,serverUrlPtr, userNamePtr, passwordPtr)
        super(PdfDigitalSignatureTimestampConfiguration, self).__init__(intPtr)

    @property

    def ServerUrl(self)->str:
        """
        Gets the URL of the timestamp server.
        """
        GetDllLibDoc().PdfDigitalSignatureTimestampConfiguration_get_ServerUrl.argtypes=[c_void_p]
        GetDllLibDoc().PdfDigitalSignatureTimestampConfiguration_get_ServerUrl.restype=c_void_p
        ret = PtrToStr(CallCFunction(GetDllLibDoc().PdfDigitalSignatureTimestampConfiguration_get_ServerUrl,self.Ptr))
        return ret


    @property

    def UserName(self)->str:
        """
        Gets the username used to authenticate to the timestamp server.
        """
        GetDllLibDoc().PdfDigitalSignatureTimestampConfiguration_get_UserName.argtypes=[c_void_p]
        GetDllLibDoc().PdfDigitalSignatureTimestampConfiguration_get_UserName.restype=c_void_p
        ret = PtrToStr(CallCFunction(GetDllLibDoc().PdfDigitalSignatureTimestampConfiguration_get_UserName,self.Ptr))
        return ret


    @property

    def Password(self)->str:
        """
        Gets the password used to authenticate to the timestamp server.
        """
        GetDllLibDoc().PdfDigitalSignatureTimestampConfiguration_get_Password.argtypes=[c_void_p]
        GetDllLibDoc().PdfDigitalSignatureTimestampConfiguration_get_Password.restype=c_void_p
        ret = PtrToStr(CallCFunction(GetDllLibDoc().PdfDigitalSignatureTimestampConfiguration_get_Password,self.Ptr))
        return ret


    @property

    def Timeout(self)->'TimeSpan':
        """
        Gets the timeout period for the timestamp request.
        """
        GetDllLibDoc().PdfDigitalSignatureTimestampConfiguration_get_Timeout.argtypes=[c_void_p]
        GetDllLibDoc().PdfDigitalSignatureTimestampConfiguration_get_Timeout.restype=c_void_p
        intPtr = CallCFunction(GetDllLibDoc().PdfDigitalSignatureTimestampConfiguration_get_Timeout,self.Ptr)
        ret = None if intPtr==None else TimeSpan(intPtr)
        return ret


