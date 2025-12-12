# This file was auto-generated. Do not modify.

from ._bs_c_cffi import ffi
from . import _BS_C #imported from __init__
from .Entity_Entity import *
from .result import Result
from .ffi_utils import data_to_bytearray, bytes_to_string, handle_sign, handle_sign_value, get_ffi_buffer

class UART(Entity):
    
    ''' 
    A UART is a "Universal Asynchronous Receiver/Transmitter.  Many times referred to as a COM
    (communication), Serial, or TTY (teletypewriter) port.
    The UART Class allows the enabling and disabling of the UART data lines.
    
    ''' 


    def __init__(self, module, index):
        super(UART, self).__init__(module, _BS_C.cmdUART, index)

    def setEnable(self, enabled):

        '''
        Enable the UART channel.
        
        Parameters
        ----------
        enabled : bool
            true: enabled, false: disabled.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.uart_setEnable(self._module._id_pointer, result, self._index, enabled)
        return result.error


    def getEnable(self):

        '''
        Get the enabled state of the uart.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : bool
                    true: enabled, false: disabled.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.uart_getEnable(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setBaudRate(self, rate):

        '''
        Set the UART baud rate.
        If zero, automatic baud rate selection is used.
        
        Parameters
        ----------
        rate : unsigned int
            baud rate.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.uart_setBaudRate(self._module._id_pointer, result, self._index, rate)
        return result.error


    def getBaudRate(self):

        '''
        Get the UART baud rate.
        If zero, automatic baud rate selection is used.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    Pointer variable to be filled with baud rate.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.uart_getBaudRate(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


    def setProtocol(self, protocol):

        '''
        Set the UART protocol.
        
        Parameters
        ----------
        protocol : unsigned char
            An enumeration of serial protocols.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.uart_setProtocol(self._module._id_pointer, result, self._index, protocol)
        return result.error


    def getProtocol(self):

        '''
        Get the UART protocol.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Pointer to where result is placed.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.uart_getProtocol(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setLinkChannel(self, channel):

        '''
        Set the index of another UART Entity that should be linked to this UART.
        
        If set to the index of this entity, the channel will not be linked.
        If set to the index of another UART entity, data will be sent between the two UART
        entities with no additional processing.
        
        Parameters
        ----------
        channel : unsigned char
            Index of the UART Entity to link
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.uart_setLinkChannel(self._module._id_pointer, result, self._index, channel)
        return result.error


    def getLinkChannel(self):

        '''
        Gets the index of the UART Entity that this entity is linked to.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Pointer to where result is placed.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.uart_getLinkChannel(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setStopBits(self, stop_bits):

        '''
        Set the UART stop bit configuration
        
        Parameters
        ----------
        stop_bits : unsigned char
            Stop Bits of UART Channel. Allowed options:
                - uartStopBits_1_Value
                - uartStopBits_1p5_Value
                - uartStopBits_2_Value
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.uart_setStopBits(self._module._id_pointer, result, self._index, stop_bits)
        return result.error


    def getStopBits(self):

        '''
        Set the UART stop bit configuration
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Pointer to where result is placed. Possible values:
                        - uartStopBits_1_Value
                        - uartStopBits_1p5_Value
                        - uartStopBits_2_Value
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.uart_getStopBits(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setParity(self, parity):

        '''
        Set the UART parity.
        
        Parameters
        ----------
        parity : unsigned char
            Parity of UART Channel. Allowed options:
                - uartParity_None_Value
                - uartParity_Odd_Value
                - uartParity_Even_Value
                - uartParity_Mark_Value
                - uartParity_Space_Value
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.uart_setParity(self._module._id_pointer, result, self._index, parity)
        return result.error


    def getParity(self):

        '''
        Get the UART parity.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Pointer variable to be filled with value. Possible values:
                        - uartParity_None_Value
                        - uartParity_Odd_Value
                        - uartParity_Even_Value
                        - uartParity_Mark_Value
                        - uartParity_Space_Value
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.uart_getParity(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setDataBits(self, data_bits):

        '''
        Set the number of bits per character
        
        Parameters
        ----------
        data_bits : unsigned char
            Data Bits of UART Channel.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.uart_setDataBits(self._module._id_pointer, result, self._index, data_bits)
        return result.error


    def getDataBits(self):

        '''
        Get the number of bits per character
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Pointer to where result is placed.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.uart_getDataBits(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setFlowControl(self, flow_control):

        '''
        Set the UART flow control configuration
        
        Parameters
        ----------
        flow_control : unsigned char
            Flow Control of UART Channel as a bitmask. Allowed bits:
                - uartFlowControl_RTS_CTS_Bit
                - uartFlowControl_DSR_DTR_Bit
                - uartFlowControl_XON_XOFF_Bit
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.uart_setFlowControl(self._module._id_pointer, result, self._index, flow_control)
        return result.error


    def getFlowControl(self):

        '''
        Set the UART flow control configuration
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Pointer to bitmask where result is placed. Possible bits:
                        - uartFlowControl_RTS_CTS_Bit
                        - uartFlowControl_DSR_DTR_Bit
                        - uartFlowControl_XON_XOFF_Bit
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.uart_getFlowControl(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def getCapableProtocols(self):

        '''
        Returns a bitmask containing a list of protocols that this UART entity is allowed to
        select.
        This does not guarantee that selecting a protocol with "setProtocol" will have an
        available resource.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    Bitmask containing list of protocols that may be selected.
                    The value of the uartProtocol is mapped to the bit index (e.g.
                    uartProtocol_Undefined is bit 0, uartProtocol_ExtronResponder_Value is bit 1,
                    etc.)
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.uart_getCapableProtocols(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


    def getAvailableProtocols(self):

        '''
        Returns a bitmask containing a list of protocols that this UART entity is capable of
        selecting, and has an available protocol resource to assign.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    Bitmask containing list of protocols that are available to select.
                    The value of the uartProtocol is mapped to the bit index (e.g.
                    uartProtocol_Undefined is bit 0, uartProtocol_ExtronResponder_Value is bit 1,
                    etc.)
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.uart_getAvailableProtocols(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


