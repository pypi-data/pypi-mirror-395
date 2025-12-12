# This file was auto-generated. Do not modify.

from ._bs_c_cffi import ffi
from . import _BS_C #imported from __init__
from .Entity_Entity import *
from .result import Result
from .ffi_utils import data_to_bytearray, bytes_to_string, handle_sign, handle_sign_value, get_ffi_buffer

class Mux(Entity):
    
    ''' 
    A MUX is a multiplexer that takes one or more similar inputs (bus, connection, or signal)
    and allows switching to one or more outputs.
    An analogy would be the switchboard of a telephone operator.
    Calls (inputs) come in and by re-connecting the input to an output, the operator
    (multiplexer) can direct that input to on or more outputs.
    One possible output is to not connect the input to anything which essentially disables
    that input's connection to anything.
    Not every MUX has multiple inputs; some may simply be a single input that can be enabled
    (connected to a single output) or disabled (not connected to anything).
    
    ''' 

    UPSTREAM_STATE_ONBOARD = 0
    UPSTREAM_STATE_EDGE = 1
    UPSTREAM_MODE_AUTO = 0
    UPSTREAM_MODE_ONBOARD = 1
    UPSTREAM_MODE_EDGE = 2
    DEFAULT_MODE = UPSTREAM_MODE_AUTO

    def __init__(self, module, index):
        super(Mux, self).__init__(module, _BS_C.cmdMUX, index)

    def getEnable(self):

        '''
        Get the mux enable/disable status
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : bool
                    true: mux is enabled, false: the mux is disabled.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.mux_getEnable(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setEnable(self, enable):

        '''
        Enable the mux.
        
        Parameters
        ----------
        enable : bool
            true: enables the mux for the selected channel.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.mux_setEnable(self._module._id_pointer, result, self._index, enable)
        return result.error


    def getChannel(self):

        '''
        Get the current selected mux channel.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Indicates which chanel is selected.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.mux_getChannel(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setChannel(self, channel):

        '''
        Set the current mux channel.
        
        Parameters
        ----------
        channel : unsigned char
            mux channel to select.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.mux_setChannel(self._module._id_pointer, result, self._index, channel)
        return result.error


    def getChannelVoltage(self, channel):

        '''
        Get the voltage of the indicated mux channel.
        
        Parameters
        ----------
        channel : unsigned char
            The channel in which voltage was requested.
        
        Note
        ----
            Not all modules provide 32 bits of accuracy; Refer to the module's datasheet to
            determine the analog bit depth and reference voltage.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : int
                    32 bit signed integer (in microvolts) based on the board's ground and
                    reference voltages.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.mux_getChannelVoltage(self._module._id_pointer, result, self._index, channel)
        return handle_sign(Result(result.error, result.value), 32, True)


    def getConfiguration(self):

        '''
        Get the configuration of the mux.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : int
                    integer representing the mux configuration either default, or split-mode.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.mux_getConfiguration(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, True)


    def setConfiguration(self, config):

        '''
        Set the configuration of the mux.
        
        Parameters
        ----------
        config : int
            integer representing the mux configuration either muxConfig_default, or
            muxConfig_splitMode.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.mux_setConfiguration(self._module._id_pointer, result, self._index, config)
        return result.error


    def getSplitMode(self):

        '''
        Get the current split mode mux configuration.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : int
                    integer representing the channel selection for each sub-channel within the
                    mux.
                    See the data-sheet for the device for specific information.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.mux_getSplitMode(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, True)


    def setSplitMode(self, split_mode):

        '''
        Sets the mux's split mode configuration.
        
        Parameters
        ----------
        split_mode : int
            integer representing the channel selection for each sub-channel within the mux.
            See the data-sheet for the device for specific information.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.mux_setSplitMode(self._module._id_pointer, result, self._index, split_mode)
        return result.error


