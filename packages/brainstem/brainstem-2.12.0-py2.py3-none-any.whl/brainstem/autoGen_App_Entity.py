# This file was auto-generated. Do not modify.

from ._bs_c_cffi import ffi
from . import _BS_C #imported from __init__
from .Entity_Entity import *
from .result import Result
from .ffi_utils import data_to_bytearray, bytes_to_string, handle_sign, handle_sign_value, get_ffi_buffer

class App(Entity):
    
    ''' 
    Used to send a cmdAPP packet to the BrainStem network.
    These commands are used for either host-to-stem or stem-to-stem interactions.
    BrainStem modules can implement a reflex origin to complete an action when a cmdAPP packet
    is addressed to the module.
    
    ''' 


    def __init__(self, module, index):
        super(App, self).__init__(module, _BS_C.cmdAPP, index)

    def execute(self, app_param):

        '''
        Execute the app reflex on the module.
        Doesn't wait for a return value from the execute call; this call returns immediately upon
        execution of the module's reflex.
        
        Parameters
        ----------
        app_param : unsigned int
            The app parameter handed to the reflex.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.app_execute(self._module._id_pointer, result, self._index, app_param)
        return result.error


    def executeAndReturn(self, app_param, ms_timeout = 1000):

        '''
        Execute the app reflex on the module.
        Waits for a return from the reflex execution for msTimeout milliseconds.
        This method will block for up to msTimeout.
        
        Parameters
        ----------
        app_param : unsigned int
            The app parameter handed to the reflex.
        ms_timeout : unsigned int
            The amount of time to wait for the return value from the reflex routine.
            The default value is 1000 milliseconds if not specified.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    The return value filled in from the result of executing the reflex routine.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.app_executeAndReturn(self._module._id_pointer, result, self._index, app_param, ms_timeout)
        return result.error


