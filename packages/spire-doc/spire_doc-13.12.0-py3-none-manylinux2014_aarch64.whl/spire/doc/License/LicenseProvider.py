from enum import Enum
from plum import dispatch
from functools import singledispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class LicenseProvider :
    """
    
    """
    @staticmethod
    def ClearLicense():
        """
            Clear all cached license.
        """
        #GetDllLibDoc().LicenseProvider_ClearLicense.argtypes=[c_void_p]
        CallCFunction(GetDllLibDoc().LicenseProvider_ClearLicense, )

    @staticmethod
    def LoadLicense():
        """
            Load the license provided by current setting to the license cache.
        """
        #GetDllLibDoc().LicenseProvider_LoadLicense.argtypes=[c_void_p]
        CallCFunction(GetDllLibDoc().LicenseProvider_LoadLicense, )

    @singledispatch
    @staticmethod
    def SetLicense(licenseFile):
        raise TypeError("Unsupport Type")
    
    @SetLicense.register
    def _SetLicense(licenseFile:str):
        """
            Provides a license by a license file path, which will be used for loading license.
            
            Parameters:
                licenseFileFullPath:
                    License file full path.
        """
        fileFullPathPtr = StrToPtr(licenseFile)
        GetDllLibDoc().LicenseProvider_SetLicense.argtypes=[c_char_p]
        CallCFunction(GetDllLibDoc().LicenseProvider_SetLicense, fileFullPathPtr)

    @SetLicense.register
    def _SetLicense(licenseFile:Stream):
        """
            Provides a license by a license stream, which will be used for loading license.

            Parameters:
                licenseFileStream:
                    License data stream.
        """
        licenseFileStreamPtr:c_void_p = licenseFile.Ptr
        GetDllLibDoc().LicenseProvider_SetLicenseL.argtypes=[c_void_p]
        CallCFunction(GetDllLibDoc().LicenseProvider_SetLicenseL, licenseFileStreamPtr)

    @staticmethod
    def SetLicenseFileName(licenseFileName:str):
        """
            Sets the license file name, which will be used for loading license.

            Parameters:
                licenseFileName:
                    License file name.
        """
        licenseFileNamePtr = StrToPtr(licenseFileName)
        GetDllLibDoc().LicenseProvider_SetLicenseFileName.argtypes=[c_char_p]
        CallCFunction(GetDllLibDoc().LicenseProvider_SetLicenseFileName, licenseFileNamePtr)
    
    @staticmethod
    def SetLicenseKey(*args, **kwargs):
        """
            Provides a license by a license key, which will be used for loading license.

            Parameters:
                key:
                    The value of the Key attribute of the element License of you license xml file.

                useDevOrTestLicense(could be None):
                    Indicates whether to apply a development or test license.
        """
        if len(args) == 1:
            keyPtr = StrToPtr(args[0])
            GetDllLibDoc().LicenseProvider_SetLicenseKey.argtypes=[c_char_p]
            CallCFunction(GetDllLibDoc().LicenseProvider_SetLicenseKey, keyPtr)
        elif len(args) == 2:
            keyPtr = StrToPtr(args[0])
            useDevOrTestLicense = args[1]
            GetDllLibDoc().LicenseProvider_SetLicenseKeyKU.argtypes=[c_char_p, c_bool]
            CallCFunction(GetDllLibDoc().LicenseProvider_SetLicenseKeyKU, keyPtr, useDevOrTestLicense)
    

    @staticmethod
    def UnbindDevelopmentOrTestingLicenses()->bool:
        """
            Unbind development or testing licenses. Only development or testing licenses
            can be unbound, deployment licenses cannot be unbound. The approach to lifting
            development or testing licenses does not allow frequent invocation by the same
            machine code, mandating a two-hour wait period before it can be invoked again.

            Returns:
                Returns true if the unbinding operation was successful; otherwise, false.
        """
        #GetDllLibDoc().LicenseProvider_UnbindDevelopmentOrTestingLicenses.argtypes=[c_void_p]
        GetDllLibDoc().LicenseProvider_UnbindDevelopmentOrTestingLicenses.restype=c_bool
        ret = CallCFunction(GetDllLibDoc().LicenseProvider_UnbindDevelopmentOrTestingLicenses,)
        return ret