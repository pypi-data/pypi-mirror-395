# This file was auto-generated. Do not modify.

from ._bs_c_cffi import ffi
from . import _BS_C #imported from __init__
from .Entity_Entity import *
from .result import Result
from .ffi_utils import data_to_bytearray, bytes_to_string, handle_sign, handle_sign_value, get_ffi_buffer

class Clock(Entity):
    
    ''' 
    Provides an interface to a real-time clock entity on a BrainStem module.
    The clock entity may be used to get and set the real time of the system.
    The clock entity has a one second resolution.
    
    ''' 


    def __init__(self, module, index):
        super(Clock, self).__init__(module, _BS_C.cmdCLOCK, index)

    def getYear(self):

        '''
        Get the four digit year value (0-4095).
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned short
                    Get the year portion of the real-time clock value.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.clock_getYear(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 16, False)


    def setYear(self, year):

        '''
        Set the four digit year value (0-4095).
        
        Parameters
        ----------
        year : unsigned short
            Set the year portion of the real-time clock value.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.clock_setYear(self._module._id_pointer, result, self._index, year)
        return result.error


    def getMonth(self):

        '''
        Get the two digit month value (1-12).
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    The two digit month portion of the real-time clock value.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.clock_getMonth(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setMonth(self, month):

        '''
        Set the two digit month value (1-12).
        
        Parameters
        ----------
        month : unsigned char
            The two digit month portion of the real-time clock value.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.clock_setMonth(self._module._id_pointer, result, self._index, month)
        return result.error


    def getDay(self):

        '''
        Get the two digit day of month value (1-28, 29, 30 or 31 depending on the month).
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    The two digit day portion of the real-time clock value.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.clock_getDay(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setDay(self, day):

        '''
        Set the two digit day of month value (1-28, 29, 30 or 31 depending on the month).
        
        Parameters
        ----------
        day : unsigned char
            The two digit day portion of the real-time clock value.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.clock_setDay(self._module._id_pointer, result, self._index, day)
        return result.error


    def getHour(self):

        '''
        Get the two digit hour value (0-23).
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    The two digit hour portion of the real-time clock value.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.clock_getHour(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setHour(self, hour):

        '''
        Set the two digit hour value (0-23).
        
        Parameters
        ----------
        hour : unsigned char
            The two digit hour portion of the real-time clock value.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.clock_setHour(self._module._id_pointer, result, self._index, hour)
        return result.error


    def getMinute(self):

        '''
        Get the two digit minute value (0-59).
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    The two digit minute portion of the real-time clock value.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.clock_getMinute(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setMinute(self, minute):

        '''
        Set the two digit minute value (0-59).
        
        Parameters
        ----------
        minute : unsigned char
            The two digit minute portion of the real-time clock value.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.clock_setMinute(self._module._id_pointer, result, self._index, minute)
        return result.error


    def getSecond(self):

        '''
        Get the two digit second value (0-59).
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    The two digit second portion of the real-time clock value.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.clock_getSecond(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setSecond(self, second):

        '''
        Set the two digit second value (0-59).
        
        Parameters
        ----------
        second : unsigned char
            The two digit second portion of the real-time clock value.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.clock_setSecond(self._module._id_pointer, result, self._index, second)
        return result.error


