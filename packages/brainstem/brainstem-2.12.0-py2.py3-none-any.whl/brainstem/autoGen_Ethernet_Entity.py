# This file was auto-generated. Do not modify.

from ._bs_c_cffi import ffi
from . import _BS_C #imported from __init__
from .Entity_Entity import *
from .result import Result
from .ffi_utils import data_to_bytearray, bytes_to_string, handle_sign, handle_sign_value, get_ffi_buffer

class Ethernet(Entity):
    
    ''' 
    IP configuration.  MAC info.  BrainD port.
    
    ''' 


    def __init__(self, module, index):
        super(Ethernet, self).__init__(module, _BS_C.cmdETHERNET, index)

    def setEnabled(self, enabled):

        '''
        Sets the Ethernet's interface to enabled/disabled.
        
        Parameters
        ----------
        enabled : bool
            1 = enabled; 0 = disabled
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.ethernet_setEnabled(self._module._id_pointer, result, self._index, enabled)
        return result.error


    def getEnabled(self):

        '''
        Gets the current enable value of the Ethernet interface.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : bool
                    1 = Fully enabled network connectivity; 0 = Ethernet MAC is disabled.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.ethernet_getEnabled(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def getNetworkConfiguration(self):

        '''
        Get the method in which IP Address is assigned to this device
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Method used.  Current methods
                      - NONE = 0
                      - STATIC = 1
                      - DHCP = 2
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.ethernet_getNetworkConfiguration(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setNetworkConfiguration(self, address_style):

        '''
        Get the method in which IP Address is assigned to this device
        
        Parameters
        ----------
        address_style : unsigned char
            Method to use.  See getNetworkConfiguration for addressStyle enumerations.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.ethernet_setNetworkConfiguration(self._module._id_pointer, result, self._index, address_style)
        return result.error


    def getStaticIPv4Address(self, buffer_length = 65536):

        '''
        Get the expected IPv4 address of this device, when networkConfiguration == STATIC
        
        Parameters
        ----------
        buffer_length : unsigned int
            size of buffer.  Should be 4.
        
        Note
        ----
            The functional IPv4 address of The Module will differ if NetworkConfiguration !=
            STATIC.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : list(unsigned char)
                    alias to an array of uint8_t[4] for returned output
        
        '''

        ffi_buffer = get_ffi_buffer(8, False, buffer_length)

        result = ffi.new("struct Result*")
        _BS_C.ethernet_getStaticIPv4Address(self._module._id_pointer, result, self._index, ffi_buffer, buffer_length)
        return_list = [handle_sign_value(ffi_buffer[i], 8, False) for i in range(result.value)]
        return Result(result.error, return_list)


    def setStaticIPv4Address(self, buffer):

        '''
        Set the desired IPv4 address of this device, if NetworkConfiguration == STATIC.
        
        Parameters
        ----------
        buffer : list(unsigned char)
            alias to an array of uint8_t[4] with an IP address
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        buffer_length = len(buffer)
        ffi_buffer = get_ffi_buffer(8, False, buffer_length)
        for x in range(buffer_length):
            ffi_buffer[x] = buffer[x]

        result = ffi.new("struct Result*")
        _BS_C.ethernet_setStaticIPv4Address(self._module._id_pointer, result, self._index, ffi_buffer, buffer_length)
        return result.error


    def getStaticIPv4Netmask(self, buffer_length = 65536):

        '''
        Get the expected IPv4 netmask of this device, when networkConfiguration == STATIC
        
        Parameters
        ----------
        buffer_length : unsigned int
            size of buffer.  Should be 4.
        
        Note
        ----
            The functional IPv4 netmask of The Module will differ if NetworkConfiguration !=
            STATIC.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : list(unsigned char)
                    alias to an array of uint8_t[4] for returned output
        
        '''

        ffi_buffer = get_ffi_buffer(8, False, buffer_length)

        result = ffi.new("struct Result*")
        _BS_C.ethernet_getStaticIPv4Netmask(self._module._id_pointer, result, self._index, ffi_buffer, buffer_length)
        return_list = [handle_sign_value(ffi_buffer[i], 8, False) for i in range(result.value)]
        return Result(result.error, return_list)


    def setStaticIPv4Netmask(self, buffer):

        '''
        Set the desired IPv4 address of this device, if NetworkConfiguration == STATIC
        
        Parameters
        ----------
        buffer : list(unsigned char)
            alias to an array of uint8_t[4] with an IP address
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        buffer_length = len(buffer)
        ffi_buffer = get_ffi_buffer(8, False, buffer_length)
        for x in range(buffer_length):
            ffi_buffer[x] = buffer[x]

        result = ffi.new("struct Result*")
        _BS_C.ethernet_setStaticIPv4Netmask(self._module._id_pointer, result, self._index, ffi_buffer, buffer_length)
        return result.error


    def getStaticIPv4Gateway(self, buffer_length = 65536):

        '''
        Get the expected IPv4 gateway of this device, when networkConfiguration == STATIC
        
        Parameters
        ----------
        buffer_length : unsigned int
            size of buffer.  Should be 4.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : list(unsigned char)
                    alias to an array of uint8_t[4] for returned output
        
        '''

        ffi_buffer = get_ffi_buffer(8, False, buffer_length)

        result = ffi.new("struct Result*")
        _BS_C.ethernet_getStaticIPv4Gateway(self._module._id_pointer, result, self._index, ffi_buffer, buffer_length)
        return_list = [handle_sign_value(ffi_buffer[i], 8, False) for i in range(result.value)]
        return Result(result.error, return_list)


    def setStaticIPv4Gateway(self, buffer):

        '''
        Set the desired IPv4 gateway of this device, if NetworkConfiguration == STATIC
        
        Parameters
        ----------
        buffer : list(unsigned char)
            alias to an array of uint8_t[4] with an IP address
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        buffer_length = len(buffer)
        ffi_buffer = get_ffi_buffer(8, False, buffer_length)
        for x in range(buffer_length):
            ffi_buffer[x] = buffer[x]

        result = ffi.new("struct Result*")
        _BS_C.ethernet_setStaticIPv4Gateway(self._module._id_pointer, result, self._index, ffi_buffer, buffer_length)
        return result.error


    def getIPv4Address(self, buffer_length = 65536):

        '''
        Get the effective IP address of this device.
        
        Parameters
        ----------
        buffer_length : unsigned int
            size of buffer.  Should be 4.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : list(unsigned char)
                    alias to an array of uint8_t[4] for returned output
        
        '''

        ffi_buffer = get_ffi_buffer(8, False, buffer_length)

        result = ffi.new("struct Result*")
        _BS_C.ethernet_getIPv4Address(self._module._id_pointer, result, self._index, ffi_buffer, buffer_length)
        return_list = [handle_sign_value(ffi_buffer[i], 8, False) for i in range(result.value)]
        return Result(result.error, return_list)


    def getIPv4Netmask(self, buffer_length = 65536):

        '''
        Get the effective IP netmask of this device.
        
        Parameters
        ----------
        buffer_length : unsigned int
            size of buffer.  Should be 4.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : list(unsigned char)
                    alias to an array of uint8_t[4] for returned output
        
        '''

        ffi_buffer = get_ffi_buffer(8, False, buffer_length)

        result = ffi.new("struct Result*")
        _BS_C.ethernet_getIPv4Netmask(self._module._id_pointer, result, self._index, ffi_buffer, buffer_length)
        return_list = [handle_sign_value(ffi_buffer[i], 8, False) for i in range(result.value)]
        return Result(result.error, return_list)


    def getIPv4Gateway(self, buffer_length = 65536):

        '''
        Get the effective IP gateway of this device.
        
        Parameters
        ----------
        buffer_length : unsigned int
            size of buffer.  Should be 4.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : list(unsigned char)
                    alias to an array of uint8_t[4] for returned output
        
        '''

        ffi_buffer = get_ffi_buffer(8, False, buffer_length)

        result = ffi.new("struct Result*")
        _BS_C.ethernet_getIPv4Gateway(self._module._id_pointer, result, self._index, ffi_buffer, buffer_length)
        return_list = [handle_sign_value(ffi_buffer[i], 8, False) for i in range(result.value)]
        return Result(result.error, return_list)


    def setStaticIPv4DNSAddress(self, buffer):

        '''
        Set IPv4 DNS Addresses (plural), if NetworkConfiguration == STATIC
        
        Parameters
        ----------
        buffer : list(unsigned char)
            alias to an array of uint8_t[N][4]
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        buffer_length = len(buffer)
        ffi_buffer = get_ffi_buffer(8, False, buffer_length)
        for x in range(buffer_length):
            ffi_buffer[x] = buffer[x]

        result = ffi.new("struct Result*")
        _BS_C.ethernet_setStaticIPv4DNSAddress(self._module._id_pointer, result, self._index, ffi_buffer, buffer_length)
        return result.error


    def getStaticIPv4DNSAddress(self, buffer_length = 65536):

        '''
        Get IPv4 DNS addresses (plural), when NetworkConfiguration == STATIC
        
        Parameters
        ----------
        buffer_length : unsigned int
            Maximum length of array, in bytes.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : list(unsigned char)
                    alias to an array of uint8_t[N][4]
        
        '''

        ffi_buffer = get_ffi_buffer(8, False, buffer_length)

        result = ffi.new("struct Result*")
        _BS_C.ethernet_getStaticIPv4DNSAddress(self._module._id_pointer, result, self._index, ffi_buffer, buffer_length)
        return_list = [handle_sign_value(ffi_buffer[i], 8, False) for i in range(result.value)]
        return Result(result.error, return_list)


    def getIPv4DNSAddress(self, buffer_length = 65536):

        '''
        Get effective IPv4 DNS addresses, for the current NetworkConfiguration
        
        Parameters
        ----------
        buffer_length : unsigned int
            Maximum length of array, in bytes.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : list(unsigned char)
                    alias to an array of uint8_t[N][4]
        
        '''

        ffi_buffer = get_ffi_buffer(8, False, buffer_length)

        result = ffi.new("struct Result*")
        _BS_C.ethernet_getIPv4DNSAddress(self._module._id_pointer, result, self._index, ffi_buffer, buffer_length)
        return_list = [handle_sign_value(ffi_buffer[i], 8, False) for i in range(result.value)]
        return Result(result.error, return_list)


    def setHostname(self, buffer):

        '''
        Set hostname that's requested when this device sends a DHCP request.
        
        Parameters
        ----------
        buffer : string
            alias to an array of uint8_t[N]
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        buffer = data_to_bytearray(buffer)
        buffer_length = len(buffer)
        ffi_buffer = get_ffi_buffer(8, False, buffer_length)
        for x in range(buffer_length):
            ffi_buffer[x] = buffer[x]

        result = ffi.new("struct Result*")
        _BS_C.ethernet_setHostname(self._module._id_pointer, result, self._index, ffi_buffer, buffer_length)
        return result.error



    def getHostname(self, buffer_length = 65536):

        '''
        Get hostname that's requested when this device sends a DHCP request.
        
        Parameters
        ----------
        buffer_length : unsigned int
            N, for N bytes.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : string
                    alias to an array of uint8_t[N]
        
        '''

        ffi_buffer = get_ffi_buffer(8, False, buffer_length)

        result = ffi.new("struct Result*")
        _BS_C.ethernet_getHostname(self._module._id_pointer, result, self._index, ffi_buffer, buffer_length)
        return_list = [handle_sign_value(ffi_buffer[i], 8, False) for i in range(result.value)]
        return Result(result.error, bytes(return_list).decode('utf-8'))


    def getMACAddress(self, buffer_length = 65536):

        '''
        Get the MAC address of the Ethernet interface.
        
        Parameters
        ----------
        buffer_length : unsigned int
            length of buffer that's writeable, should be > 6.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : list(unsigned char)
                    alias to an array of uint8_t[6]
        
        '''

        ffi_buffer = get_ffi_buffer(8, False, buffer_length)

        result = ffi.new("struct Result*")
        _BS_C.ethernet_getMACAddress(self._module._id_pointer, result, self._index, ffi_buffer, buffer_length)
        return_list = [handle_sign_value(ffi_buffer[i], 8, False) for i in range(result.value)]
        return Result(result.error, return_list)


    def setInterfacePort(self, service, port):

        '''
        Set the port of a TCPIP service on the device.
        
        Parameters
        ----------
        service : unsigned char
            The index of the service to set the port for.
        port : unsigned short
            The port to be used for the TCPIP server.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.ethernet_setInterfacePort(self._module._id_pointer, result, self._index, service, port)
        return result.error


    def getInterfacePort(self, service):

        '''
        Get the port of a TCPIP service on the device.
        
        Parameters
        ----------
        service : unsigned char
            The index of the service to get the port for.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned short
                    The port of the TCPIP server.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.ethernet_getInterfacePort(self._module._id_pointer, result, self._index, service)
        return handle_sign(Result(result.error, result.value), 16, False)


