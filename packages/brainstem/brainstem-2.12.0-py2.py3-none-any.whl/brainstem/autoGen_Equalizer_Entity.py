# This file was auto-generated. Do not modify.

from ._bs_c_cffi import ffi
from . import _BS_C #imported from __init__
from .Entity_Entity import *
from .result import Result
from .ffi_utils import data_to_bytearray, bytes_to_string, handle_sign, handle_sign_value, get_ffi_buffer

class Equalizer(Entity):
    
    ''' 
    Provides receiver and transmitter gain/boost/emphasis settings for some of Acroname's
    products.
    Please see product documentation for further details.
    
    ''' 


    def __init__(self, module, index):
        super(Equalizer, self).__init__(module, _BS_C.cmdEQUALIZER, index)

    def setReceiverConfig(self, channel, config):

        '''
        Sets the receiver configuration for a given channel.
        
        Parameters
        ----------
        channel : unsigned char
            The equalizer receiver channel.
        config : unsigned char
            Configuration to be applied to the receiver.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.equalizer_setReceiverConfig(self._module._id_pointer, result, self._index, channel, config)
        return result.error


    def getReceiverConfig(self, channel):

        '''
        Gets the receiver configuration for a given channel.
        
        Parameters
        ----------
        channel : unsigned char
            The equalizer receiver channel.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Configuration of the receiver.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.equalizer_getReceiverConfig(self._module._id_pointer, result, self._index, channel)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setTransmitterConfig(self, config):

        '''
        Sets the transmitter configuration
        
        Parameters
        ----------
        config : unsigned char
            Configuration to be applied to the transmitter.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.equalizer_setTransmitterConfig(self._module._id_pointer, result, self._index, config)
        return result.error


    def getTransmitterConfig(self):

        '''
        Gets the transmitter configuration
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Configuration of the Transmitter.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.equalizer_getTransmitterConfig(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


