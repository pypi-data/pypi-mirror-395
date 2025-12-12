# This file was auto-generated. Do not modify.

from ._bs_c_cffi import ffi
from . import _BS_C #imported from __init__
from .Entity_Entity import *
from .result import Result
from .ffi_utils import data_to_bytearray, bytes_to_string, handle_sign, handle_sign_value, get_ffi_buffer

class HDBaseT(Entity):
    
    ''' 
    This entity is only available on certain modules, and provides information on HDBaseT
    extenders.
    
    ''' 


    def __init__(self, module, index):
        super(HDBaseT, self).__init__(module, _BS_C.cmdHDBASET, index)

    def getSerialNumber(self, buffer_length = 65536):

        '''
        Gets the serial number of the HDBaseT device (6 bytes)
        
        Parameters
        ----------
        buffer_length : unsigned int
            Length of the buffer to be filed
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : list(unsigned char)
                    pointer to the start of a c style buffer to be filled
        
        '''

        ffi_buffer = get_ffi_buffer(8, False, buffer_length)

        result = ffi.new("struct Result*")
        _BS_C.hdbaset_getSerialNumber(self._module._id_pointer, result, self._index, ffi_buffer, buffer_length)
        return_list = [handle_sign_value(ffi_buffer[i], 8, False) for i in range(result.value)]
        return Result(result.error, return_list)


    def getFirmwareVersion(self):

        '''
        Gets the firmware version of the HDBaseT device
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    A bit packet representation of the firmware version
                    Major: Bits 24-31; Minor: Bits 16-23; Patch: Bits 8-15; Build: Bits 0-7
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.hdbaset_getFirmwareVersion(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


    def getState(self):

        '''
        Gets the current state of the HDBaseT link
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    Bit packeted representation of the state.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.hdbaset_getState(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


    def getCableLength(self):

        '''
        Gets the perceived cable length
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    Cable length in micro-meters
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.hdbaset_getCableLength(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


    def getMSEA(self):

        '''
        Gets the Mean Squared Error (MSE) for channel A
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : int
                    The current MSE for channel A in micro-dB
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.hdbaset_getMSEA(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, True)


    def getMSEB(self):

        '''
        Gets the Mean Squared Error (MSE) for channel B
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : int
                    The current MSE for channel B in micro-dB
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.hdbaset_getMSEB(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, True)


    def getRetransmissionRate(self):

        '''
        Gets the number of successful messages between retransmission
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    Instantaneous number of successful messages between retransmission.
                    To be interpreted as: 1 / retransmissionRate for rate interpretation.
                    If the value is 0, there have been no retransmissions, otherwise higher is
                    better..
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.hdbaset_getRetransmissionRate(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


    def getLinkUtilization(self):

        '''
        Gets the current link utilization
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    Utilization in milli-percent
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.hdbaset_getLinkUtilization(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


    def getEncodingState(self):

        '''
        Gets the current encoding state.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Signal modulation encoding type.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.hdbaset_getEncodingState(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def getUSB2DeviceTree(self, buffer_length = 65536):

        '''
        Gets the USB2 tree at the HDBaseT device.
        
        Parameters
        ----------
        buffer_length : unsigned int
            Length of the buffer to be filed
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : list(unsigned char)
                    pointer to the start of a c style buffer to be filled
        
        '''

        ffi_buffer = get_ffi_buffer(8, False, buffer_length)

        result = ffi.new("struct Result*")
        _BS_C.hdbaset_getUSB2DeviceTree(self._module._id_pointer, result, self._index, ffi_buffer, buffer_length)
        return_list = [handle_sign_value(ffi_buffer[i], 8, False) for i in range(result.value)]
        return Result(result.error, return_list)


    def getUSB3DeviceTree(self, buffer_length = 65536):

        '''
        Gets the USB3 tree at the HDBaseT device.
        
        Parameters
        ----------
        buffer_length : unsigned int
            Length of the buffer to be filed
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : list(unsigned char)
                    pointer to the start of a c style buffer to be filled
        
        '''

        ffi_buffer = get_ffi_buffer(8, False, buffer_length)

        result = ffi.new("struct Result*")
        _BS_C.hdbaset_getUSB3DeviceTree(self._module._id_pointer, result, self._index, ffi_buffer, buffer_length)
        return_list = [handle_sign_value(ffi_buffer[i], 8, False) for i in range(result.value)]
        return Result(result.error, return_list)


    def getLinkRole(self):

        '''
        Gets the current link role
        In the case of "Auto" the getState API will provide the current role.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Link role
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.hdbaset_getLinkRole(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setLinkRole(self, role):

        '''
        Sets the active link role
        
        Parameters
        ----------
        role : unsigned char
            The role to be set.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.hdbaset_setLinkRole(self._module._id_pointer, result, self._index, role)
        return result.error


