# This file was auto-generated. Do not modify.

from ._bs_c_cffi import ffi
from . import _BS_C #imported from __init__
from .Entity_Entity import *
from .result import Result
from .ffi_utils import data_to_bytearray, bytes_to_string, handle_sign, handle_sign_value, get_ffi_buffer

class USBSystem(Entity):
    
    ''' 
    The USBSystem class provides high level control of the lower level Port Class.
    
    ''' 


    def __init__(self, module, index):
        super(USBSystem, self).__init__(module, _BS_C.cmdUSBSYSTEM, index)

    def getUpstream(self):

        '''
        Gets the upstream port.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    The current upstream port.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usbsystem_getUpstream(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setUpstream(self, port):

        '''
        Sets the upstream port.
        
        Parameters
        ----------
        port : unsigned char
            The upstream port to set.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usbsystem_setUpstream(self._module._id_pointer, result, self._index, port)
        return result.error


    def getEnumerationDelay(self):

        '''
        Gets the inter-port enumeration delay in milliseconds.
        Delay is applied upon hub enumeration.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    the current inter-port delay in milliseconds.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usbsystem_getEnumerationDelay(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


    def setEnumerationDelay(self, ms_delay):

        '''
        Sets the inter-port enumeration delay in milliseconds.
        Delay is applied upon hub enumeration.
        
        Parameters
        ----------
        ms_delay : unsigned int
            The delay in milliseconds to be applied between port enables
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usbsystem_setEnumerationDelay(self._module._id_pointer, result, self._index, ms_delay)
        return result.error


    def getDataRoleList(self):

        '''
        Gets the data role of all ports with a single call
        Equivalent to calling PortClass::getDataRole() on each individual port.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    A bit packed representation of the data role for all ports.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usbsystem_getDataRoleList(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


    def getEnabledList(self):

        '''
        Gets the current enabled status of all ports with a single call.
        Equivalent to calling PortClass::setEnabled() on each port.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    Bit packed representation of the enabled status for all ports.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usbsystem_getEnabledList(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


    def setEnabledList(self, enabled_list):

        '''
        Sets the enabled status of all ports with a single call.
        Equivalent to calling PortClass::setEnabled() on each port.
        
        Parameters
        ----------
        enabled_list : unsigned int
            Bit packed representation of the enabled status for all ports to be applied.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usbsystem_setEnabledList(self._module._id_pointer, result, self._index, enabled_list)
        return result.error


    def getModeList(self, buffer_length = 16384):

        '''
        Gets the current mode of all ports with a single call.
        Equivalent to calling PortClass:getMode() on each port.
        
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
                value : list(unsigned int)
                    pointer to the start of a c style buffer to be filled
        
        '''

        ffi_buffer = get_ffi_buffer(32, False, buffer_length)

        result = ffi.new("struct Result*")
        _BS_C.usbsystem_getModeList(self._module._id_pointer, result, self._index, ffi_buffer, buffer_length)
        return_list = [handle_sign_value(ffi_buffer[i], 32, False) for i in range(result.value)]
        return Result(result.error, return_list)


    def setModeList(self, buffer):

        '''
        Sets the mode of all ports with a single call.
        Equivalent to calling PortClass::setMode() on each port
        
        Parameters
        ----------
        buffer : list(unsigned int)
            Pointer to the start of a c style buffer to be transferred.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        buffer_length = len(buffer)
        ffi_buffer = get_ffi_buffer(32, False, buffer_length)
        for x in range(buffer_length):
            ffi_buffer[x] = buffer[x]

        result = ffi.new("struct Result*")
        _BS_C.usbsystem_setModeList(self._module._id_pointer, result, self._index, ffi_buffer, buffer_length)
        return result.error


    def getStateList(self, buffer_length = 16384):

        '''
        Gets the state for all ports with a single call.
        Equivalent to calling PortClass::getState() on each port.
        
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
                value : list(unsigned int)
                    pointer to the start of a c style buffer to be filled
        
        '''

        ffi_buffer = get_ffi_buffer(32, False, buffer_length)

        result = ffi.new("struct Result*")
        _BS_C.usbsystem_getStateList(self._module._id_pointer, result, self._index, ffi_buffer, buffer_length)
        return_list = [handle_sign_value(ffi_buffer[i], 32, False) for i in range(result.value)]
        return Result(result.error, return_list)


    def getPowerBehavior(self):

        '''
        Gets the behavior of the power manager.
        The power manager is responsible for budgeting the power of the system, i.e. What happens
        when requested power greater than available power.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Variable to be filled with an enumerated representation of behavior.
                    Available behaviors are product specific. See the reference documentation.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usbsystem_getPowerBehavior(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setPowerBehavior(self, behavior):

        '''
        Sets the behavior of how available power is managed, i.e. What happens when requested
        power is greater than available power.
        
        Parameters
        ----------
        behavior : unsigned char
            An enumerated representation of behavior.
            Available behaviors are product specific. See the reference documentation.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usbsystem_setPowerBehavior(self._module._id_pointer, result, self._index, behavior)
        return result.error


    def getPowerBehaviorConfig(self, buffer_length = 16384):

        '''
        Gets the current power behavior configuration.
        Certain power behaviors use a list of ports to determine priority when budgeting power.
        
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
                value : list(unsigned int)
                    pointer to the start of a c style buffer to be filled
        
        '''

        ffi_buffer = get_ffi_buffer(32, False, buffer_length)

        result = ffi.new("struct Result*")
        _BS_C.usbsystem_getPowerBehaviorConfig(self._module._id_pointer, result, self._index, ffi_buffer, buffer_length)
        return_list = [handle_sign_value(ffi_buffer[i], 32, False) for i in range(result.value)]
        return Result(result.error, return_list)


    def setPowerBehaviorConfig(self, buffer):

        '''
        Sets the current power behavior configuration.
        Certain power behaviors use a list of ports to determine priority when budgeting power.
        
        Parameters
        ----------
        buffer : list(unsigned int)
            Pointer to the start of a c style buffer to be transferred.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        buffer_length = len(buffer)
        ffi_buffer = get_ffi_buffer(32, False, buffer_length)
        for x in range(buffer_length):
            ffi_buffer[x] = buffer[x]

        result = ffi.new("struct Result*")
        _BS_C.usbsystem_setPowerBehaviorConfig(self._module._id_pointer, result, self._index, ffi_buffer, buffer_length)
        return result.error


    def getDataRoleBehavior(self):

        '''
        Gets the behavior of how upstream and downstream ports are determined, i.e. How do you
        manage requests for data role swaps and new upstream connections.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Variable to be filled with an enumerated representation of behavior.
                    Available behaviors are product specific. See the reference documentation.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usbsystem_getDataRoleBehavior(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setDataRoleBehavior(self, behavior):

        '''
        Sets the behavior of how upstream and downstream ports are determined, i.e. How do you
        manage requests for data role swaps and new upstream connections.
        
        Parameters
        ----------
        behavior : unsigned char
            An enumerated representation of behavior.
            Available behaviors are product specific. See the reference documentation.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usbsystem_setDataRoleBehavior(self._module._id_pointer, result, self._index, behavior)
        return result.error


    def getDataRoleBehaviorConfig(self, buffer_length = 16384):

        '''
        Gets the current data role behavior configuration.
        Certain data role behaviors use a list of ports to determine priority host priority.
        
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
                value : list(unsigned int)
                    pointer to the start of a c style buffer to be filled
        
        '''

        ffi_buffer = get_ffi_buffer(32, False, buffer_length)

        result = ffi.new("struct Result*")
        _BS_C.usbsystem_getDataRoleBehaviorConfig(self._module._id_pointer, result, self._index, ffi_buffer, buffer_length)
        return_list = [handle_sign_value(ffi_buffer[i], 32, False) for i in range(result.value)]
        return Result(result.error, return_list)


    def setDataRoleBehaviorConfig(self, buffer):

        '''
        Sets the current data role behavior configuration.
        Certain data role behaviors use a list of ports to determine host priority.
        
        Parameters
        ----------
        buffer : list(unsigned int)
            Pointer to the start of a c style buffer to be transferred.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        buffer_length = len(buffer)
        ffi_buffer = get_ffi_buffer(32, False, buffer_length)
        for x in range(buffer_length):
            ffi_buffer[x] = buffer[x]

        result = ffi.new("struct Result*")
        _BS_C.usbsystem_setDataRoleBehaviorConfig(self._module._id_pointer, result, self._index, ffi_buffer, buffer_length)
        return result.error


    def getSelectorMode(self):

        '''
        Gets the current mode of the selector input.
        This mode determines what happens and in what order when the external selector input is
        used.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Variable to be filled with the selector mode
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usbsystem_getSelectorMode(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setSelectorMode(self, mode):

        '''
        Sets the current mode of the selector input.
        This mode determines what happens and in what order when the external selector input is
        used.
        
        Parameters
        ----------
        mode : unsigned char
            Mode to be set.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usbsystem_setSelectorMode(self._module._id_pointer, result, self._index, mode)
        return result.error


    def getUpstreamHS(self):

        '''
        Gets the USB HighSpeed upstream port.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    The current upstream port.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usbsystem_getUpstreamHS(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setUpstreamHS(self, port):

        '''
        Sets the USB HighSpeed upstream port.
        
        Parameters
        ----------
        port : unsigned char
            The upstream port to set.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usbsystem_setUpstreamHS(self._module._id_pointer, result, self._index, port)
        return result.error


    def getUpstreamSS(self):

        '''
        Gets the USB SuperSpeed upstream port.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    The current upstream port.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usbsystem_getUpstreamSS(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setUpstreamSS(self, port):

        '''
        Sets the USB SuperSpeed upstream port.
        
        Parameters
        ----------
        port : unsigned char
            The upstream port to set.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usbsystem_setUpstreamSS(self._module._id_pointer, result, self._index, port)
        return result.error


    def getOverride(self):

        '''
        Gets the current enabled overrides
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    Bit mapped representation of the current override configuration.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usbsystem_getOverride(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


    def setOverride(self, overrides):

        '''
        Sets the current enabled overrides
        
        Parameters
        ----------
        overrides : unsigned int
            Overrides to be set in a bit mapped representation.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usbsystem_setOverride(self._module._id_pointer, result, self._index, overrides)
        return result.error


    def setDataHSMaxDatarate(self, datarate):

        '''
        Sets the USB HighSpeed Max datarate
        
        Parameters
        ----------
        datarate : unsigned int
            Maximum datarate for the USB HighSpeed signals.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usbsystem_setDataHSMaxDatarate(self._module._id_pointer, result, self._index, datarate)
        return result.error


    def getDataHSMaxDatarate(self):

        '''
        Gets the USB HighSpeed Max datarate
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    Current maximum datarate for the USB HighSpeed signals.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usbsystem_getDataHSMaxDatarate(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


    def setDataSSMaxDatarate(self, datarate):

        '''
        Sets the USB SuperSpeed Max datarate
        
        Parameters
        ----------
        datarate : unsigned int
            Maximum datarate for the USB SuperSpeed signals.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usbsystem_setDataSSMaxDatarate(self._module._id_pointer, result, self._index, datarate)
        return result.error


    def getDataSSMaxDatarate(self):

        '''
        Gets the USB SuperSpeed Max datarate
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    Current maximum datarate for the USB SuperSpeed signals.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usbsystem_getDataSSMaxDatarate(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


