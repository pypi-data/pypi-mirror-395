# This file was auto-generated. Do not modify.

from ._bs_c_cffi import ffi
from . import _BS_C #imported from __init__
from .Entity_Entity import *
from .result import Result
from .ffi_utils import data_to_bytearray, bytes_to_string, handle_sign, handle_sign_value, get_ffi_buffer

class RCServo(Entity):
    
    ''' 
    Interface to servo entities on BrainStem modules.
    Servo entities are built upon the digital input/output pins and therefore can also be
    inputs or outputs.
    Please see the product datasheet on the configuration limitations.
    
    ''' 

    SERVO_DEFAULT_POSITION = 128
    SERVO_DEFAULT_MIN = 64
    SERVO_DEFAULT_MAX = 192

    def __init__(self, module, index):
        super(RCServo, self).__init__(module, _BS_C.cmdSERVO, index)

    def setEnable(self, enable):

        '''
        Enable the servo channel
        
        Parameters
        ----------
        enable : bool
            The state to be set.
            0 is disabled, 1 is enabled.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.rcservo_setEnable(self._module._id_pointer, result, self._index, enable)
        return result.error


    def getEnable(self):

        '''
        Get the enable status of the servo channel.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : bool
                    The current enable status of the servo entity.
                    0 is disabled, 1 is enabled.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.rcservo_getEnable(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setPosition(self, position):

        '''
        Set the position of the servo channel
        
        Parameters
        ----------
        position : unsigned char
            The position to be set.
            Default 64 = a 1ms pulse and 192 = a 2ms pulse.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.rcservo_setPosition(self._module._id_pointer, result, self._index, position)
        return result.error


    def getPosition(self):

        '''
        Get the position of the servo channel
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    The current position of the servo channel.
                    Default 64 = a 1ms pulse and 192 = a 2ms pulse.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.rcservo_getPosition(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setReverse(self, reverse):

        '''
        Set the output to be reversed on the servo channel
        
        Parameters
        ----------
        reverse : bool
            Reverses the value set by "setPosition".
            For example, if the position is set to 64 (1ms pulse) the output will now be 192 (2ms
            pulse), however "getPostion" will return the set value of 64.
            0 = not reversed, 1 = reversed.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.rcservo_setReverse(self._module._id_pointer, result, self._index, reverse)
        return result.error


    def getReverse(self):

        '''
        Get the reverse status of the servo channel
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : bool
                    The current reverse status of the servo entity.
                    0 = not reversed, 1 = reversed.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.rcservo_getReverse(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


