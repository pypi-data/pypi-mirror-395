# This file was auto-generated. Do not modify.

from ._bs_c_cffi import ffi
from . import _BS_C #imported from __init__
from .Entity_Entity import *
from .result import Result
from .ffi_utils import data_to_bytearray, bytes_to_string, handle_sign, handle_sign_value, get_ffi_buffer

class Temperature(Entity):
    
    ''' 
    This entity is only available on certain modules, and provides a temperature reading in
    microcelsius.
    
    ''' 


    def __init__(self, module, index):
        super(Temperature, self).__init__(module, _BS_C.cmdTEMPERATURE, index)

    def getValue(self):

        '''
        Get the modules temperature in micro-C
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : int
                    The temperature in micro-Celsius (1 == 1e-6C).
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.temperature_getValue(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, True)


    def getValueMin(self):

        '''
        Get the module's minimum temperature in micro-C since the last power cycle.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : int
                    The module's minimum temperature in micro-C
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.temperature_getValueMin(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, True)


    def getValueMax(self):

        '''
        Get the module's maximum temperature in micro-C since the last power cycle.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : int
                    The module's maximum temperature in micro-C
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.temperature_getValueMax(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, True)


