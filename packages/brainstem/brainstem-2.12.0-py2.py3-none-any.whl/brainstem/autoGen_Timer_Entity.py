# This file was auto-generated. Do not modify.

from ._bs_c_cffi import ffi
from . import _BS_C #imported from __init__
from .Entity_Entity import *
from .result import Result
from .ffi_utils import data_to_bytearray, bytes_to_string, handle_sign, handle_sign_value, get_ffi_buffer

class Timer(Entity):
    
    ''' 
    The Timer Class provides access to a simple scheduler.
    The timer can set to fire only once, or to repeat at a certain interval.
    Additionally, a timer entity can execute custom Reflex routines upon firing.
    
    ''' 

    SINGLE_SHOT_MODE = 0
    REPEAT_MODE = 1
    DEFAULT_MODE = SINGLE_SHOT_MODE

    def __init__(self, module, index):
        super(Timer, self).__init__(module, _BS_C.cmdTIMER, index)

    def getExpiration(self):

        '''
        Get the currently set expiration time in microseconds.
        This is not a "live" timer. That is, it shows the expiration time originally set with
        setExpiration; it does not "tick down" to show the time remaining before expiration.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    The timer expiration duration in microseconds.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.timer_getExpiration(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


    def setExpiration(self, usec_duration):

        '''
        Set the expiration time for the timer entity.
        When the timer expires, it will fire the associated timer[index]() reflex.
        
        Parameters
        ----------
        usec_duration : unsigned int
            The duration before timer expiration in microseconds.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.timer_setExpiration(self._module._id_pointer, result, self._index, usec_duration)
        return result.error


    def getMode(self):

        '''
        Get the mode of the timer which is either single or repeat mode.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    The mode of the time. aTIMER_MODE_REPEAT or aTIMER_MODE_SINGLE.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.timer_getMode(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setMode(self, mode):

        '''
        Set the mode of the timer which is either single or repeat mode.
        
        Parameters
        ----------
        mode : unsigned char
            The mode of the timer. aTIMER_MODE_REPEAT or aTIMER_MODE_SINGLE.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.timer_setMode(self._module._id_pointer, result, self._index, mode)
        return result.error


