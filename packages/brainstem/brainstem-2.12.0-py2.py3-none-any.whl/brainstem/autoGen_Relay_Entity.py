# This file was auto-generated. Do not modify.

from ._bs_c_cffi import ffi
from . import _BS_C #imported from __init__
from .Entity_Entity import *
from .result import Result
from .ffi_utils import data_to_bytearray, bytes_to_string, handle_sign, handle_sign_value, get_ffi_buffer

class Relay(Entity):
    
    ''' 
    Interface to relay entities on BrainStem modules.
    Relay entities can be set, and the voltage read.
    Other capabilities may be available, please see the product datasheet.
    
    ''' 

    VALUE_LOW = 0
    VALUE_HIGH = 1

    def __init__(self, module, index):
        super(Relay, self).__init__(module, _BS_C.cmdRELAY, index)

    def setEnable(self, enable):

        '''
        Set the enable/disable state.
        
        Parameters
        ----------
        enable : bool
            False or 0 = Disabled, True or 1 = Enabled
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.relay_setEnable(self._module._id_pointer, result, self._index, enable)
        return result.error


    def getEnable(self):

        '''
        Get the state.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : bool
                    False or 0 = Disabled, True or 1 = Enabled
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.relay_getEnable(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def getVoltage(self):

        '''
        Get the scaled micro volt value with reference to ground.
        
        Note
        ----
            Not all modules provide 32 bits of accuracy. Refer to the module's datasheet to
            determine the analog bit depth and reference voltage.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : int
                    32 bit signed integer (in micro Volts) based on the boards ground and
                    reference voltages.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.relay_getVoltage(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, True)


