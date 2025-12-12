# Copyright (c) 2018 Acroname Inc. - All Rights Reserved
#
# This file is part of the BrainStem (tm) package which is released under MIT.
# See file LICENSE or go to https://acroname.com for full license details.

"""
A module that provides a Spec class for specifying a connection to a BrainStem module.

A Spec instance fully describes a connection to a brainstem module. In the case of
USB based stems this is simply the serial number of the module. For TCPIP based stems
this is an IP address and TCP port.

For more information about links and the Brainstem network
see the `Acroname BrainStem Reference`_

.. _Acroname BrainStem Reference:
    https://acroname.com/reference
"""
import socket
import struct

from ._bs_c_cffi import ffi
from . import _BS_C
from .result import Result

from .defs import (
    MODEL_MTM_IOSERIAL
)

class Status(object):
    """ Status variables represent the link status possibilities for Brainstem Links.

        Status States:
            * STOPPED (0)
            * INITIALIZING (1)
            * RUNNING (2)
            * STOPPING (3)
            * SYNCING (4)
            * INVALID_LINK_STREAM (5)
            * IO_ERROR (6)
            * UNKNOWN_ERROR (7)

    """

    STOPPED = 0
    INITIALIZING = 1
    RUNNING = 2
    STOPPING = 3
    SYNCING = 4
    INVALID_LINK_STREAM = 5
    IO_ERROR = 6
    RESETTING = 7
    UNKNOWN_ERROR = 8


class aEtherConfig(object):
    """ aEther configuration class for configuring AETHER connection types.

        Note: If localOnly == false AND networkInterface is default (0 or LOCALHOST_IP_ADDRESS)
        it will be populated with the auto-selected interface upon successful connection.

        Attributes: 
            enabled: True: Client-Server model is used; False: Direct module control is used.
            fallback: True: If connections fails it will automatically search for network connections.
            localOnly: True: Restricts access to localhost; False: Expose device to external network.
            assignedPort: Server assigned port after successful connection.
            networkInterface: Network interface to use for connections.
    """

    def __init__(self):
        self.enabled = True
        self.fallback = True
        self.localOnly = True
        self.assignedPort = 0
        self.networkInterface = _BS_C.LOCALHOST_IP_ADDRESS

    def __str__(self):
        return "aEther Config: Enabled: %d - Fallback: %d - LocalOnly: %d - AssignedPort: %d - NetworkInterface: %d" % \
               (self.enabled, self.fallback, self.localOnly, self.assignedPort, self.networkInterface)

    @staticmethod
    def cca_config_to_python_config(cca_config):
        config = aEtherConfig()
        config.enabled = cca_config.enabled
        config.fallback = cca_config.fallback
        config.localOnly = cca_config.localOnly
        config.assignedPort = cca_config.assignedPort
        config.networkInterface = cca_config.networkInterface
        return config

    @staticmethod
    def python_config_to_cca_config(config, cca_config):
        cca_config.enabled = config.enabled
        cca_config.fallback = config.fallback
        cca_config.localOnly = config.localOnly
        cca_config.assignedPort = config.assignedPort
        cca_config.networkInterface = config.networkInterface


class Spec(object):
    """ Spec class for specifying connection details

        Instances of Spec represent the connection details for a brainstem link.
        The Spec class also contains constants representing the possible transport
        types for BrainStem modules.

        args:
            transport (int): One of USB, TCPIP, SERIAL or AETHER.
            serial_number (int): The module serial number.
            module: The module address on the Brainstem network.
            model: The device model number of the Brainstem module.
            **keywords: For TCPIP, SERIAL and AETHER connections. The possibilities are,

                * ip_address: (int/str) The IPV4 address for a TCPIP/AETHER connection type.
                * ip_port: (int/str) The port for a TCPIP/AETHER connection type.
                * port: (str) The serial port for a SERIAL connection type.
                * baudrate: (int/str) The baudrate for a SERIAL connection type.

    """
    INVALID = 0                         #: INVALID Undefined transport type.
    USB = 1                             #: USB transport type.
    TCPIP = 2                            #: TCPIP transport type.
    SERIAL = 3                          #: SERIAL transport type.
    AETHER = 4                           #: AETHER transport type.
    AETHER_USB = 5                       #: AETHER_USB transport type.
    AETHER_TCPIP = 6                     #: AETHER_TCPIP transport type.
    AETHER_SERIAL = 7                     #: AETHER_SERIAL transport type.

    def __init__(self, transport, serial_number, module, model, **keywords):

        self.transport = transport
        self.serial_number = serial_number
        self.module = module

        # Model was added in 2.2.0  This adds legacy support
        if model == 2:
            self.model = MODEL_MTM_IOSERIAL
        else:
            self.model = model

        for key in keywords.keys():
            if key == 'ip_address':
                if isinstance(keywords[key], int):
                    self.ip_address = keywords[key]
                else:
                    try:
                        self.ip_address = socket.inet_aton(keywords[key])
                    except socket.error:
                        raise ValueError("Failed to convert ip_address key ", keywords[key])

            elif key == 'ip_port':
                if isinstance(keywords[key], int):
                    self.ip_port = keywords[key]
                else:
                    try:
                        self.ip_port = int(keywords[key])
                    except ValueError:
                        raise ValueError("Failed to convert ip_port key ", keywords[key])

            elif key == 'port':
                if isinstance(keywords[key], str):
                    self.port = keywords[key]
                else:
                    try:
                        #This is probably a bad choice as it will ALWAYS succeed.
                        self.port = str(keywords[key])
                    except ValueError:
                        #This should never happen because every type in python can be converted to a string
                        raise ValueError("Failed to convert port key ", keywords[key])

            elif key == 'baudrate':
                if isinstance(keywords[key], int):
                    self.baudrate = keywords[key]
                else:
                    try:
                        self.baudrate = int(keywords[key])
                    except ValueError:
                        raise ValueError("Failed to convert baudrate key ", keywords[key])

            else:
                raise KeyError("Unknown keyword in Spec ", key)


    @staticmethod
    def cca_spec_to_python_spec(cca_spec):
        """ Internal: Translate cffi spec into python Spec"""
        if cca_spec.type == Spec.USB:
            return Spec(cca_spec.type, cca_spec.serial_num, cca_spec.module, cca_spec.model)
        elif cca_spec.type == Spec.SERIAL:
            return Spec(cca_spec.type, cca_spec.serial_num, cca_spec.module, cca_spec.model,
                          port=cca_spec.port, baudrate=cca_spec.baudrate)
        elif cca_spec.type == Spec.TCPIP or \
            cca_spec.type == Spec.AETHER or \
            cca_spec.type == Spec.AETHER_USB or \
            cca_spec.type == Spec.AETHER_TCPIP or \
            cca_spec.type == Spec.AETHER_SERIAL:
            return Spec(cca_spec.type, cca_spec.serial_num, cca_spec.module, cca_spec.model,
                          ip_address=cca_spec.ip_address, ip_port=cca_spec.ip_port)

        return None

    @staticmethod
    #NOTE: cca_spec is passed in because of how ffi lifetime works. 
    def python_spec_to_cca_spec(spec, cca_spec):
        cca_spec.serial_num = spec.serial_number
        cca_spec.module = spec.module
        cca_spec.type = spec.transport
        cca_spec.model = spec.model

        if cca_spec.type == Spec.USB:
            pass
        elif cca_spec.type == Spec.SERIAL:
            if hasattr(spec, "baudrate"):
                cca_spec.baudrate = spec.baudrate
            if hasattr(spec, "port"):
                CCA_SPEC_PORT_SIZE = 100
                ffi.memmove(cca_spec.port, spec.port.encode('utf-8'), CCA_SPEC_PORT_SIZE)
                cca_spec.port[CCA_SPEC_PORT_SIZE-1] = b'\0' #ensure null termination. 
        elif cca_spec.type == Spec.TCPIP or \
            cca_spec.type == Spec.AETHER or \
            cca_spec.type == Spec.AETHER_USB or \
            cca_spec.type == Spec.AETHER_TCPIP or \
            cca_spec.type == Spec.AETHER_SERIAL:
            if hasattr(spec, "ip_address"):
                cca_spec.ip_address = spec.ip_address
            if hasattr(spec, "ip_port"):
                cca_spec.ip_port = spec.ip_port


    def __str__(self):
        type_string = "USB"
        if self.transport == Spec.TCPIP:
            type_string = "TCPIP"
        elif self.transport == Spec.SERIAL:
            type_string = "SERIAL"
        elif self.transport == Spec.AETHER:
            type_string = "AETHER"
        elif self.transport == Spec.AETHER_USB:
            type_string = "AETHER_USB"
        elif self.transport == Spec.AETHER_TCPIP:
            type_string = "AETHER_TCPIP"
        elif self.transport == Spec.AETHER_SERIAL:
            type_string = "AETHER_SERIAL"

        addr, port = ('', '')
        if hasattr(self, 'ip_address'):
            addr = ", IP Address: %s" % socket.inet_ntoa(struct.pack('!I', socket.htonl(self.ip_address)))
        if hasattr(self, 'ip_port'):
            port = ", IP Port: %d" % self.ip_port
        if hasattr(self, 'port'):
            port += ", Serial Port: %s" % self.port
        if hasattr(self, 'baudrate'):
            port += ", Baudrate: %d" % self.baudrate
        return 'Model: %s LinkType: %s(serial: %08X%s%s)' % (self.model, type_string, self.serial_number, addr, port)


# Simple class which provide key and value properties for a tuple
class StreamStatusEntry(tuple):

    STREAM_KEY_MODULE_ADDRESS = 0
    STREAM_KEY_CMD = 1
    STREAM_KEY_OPTION = 2
    STREAM_KEY_INDEX = 3
    STREAM_KEY_SUBINDEX = 4


    def __new__(cls, key, value):
        return super(StreamStatusEntry, cls).__new__(cls, (key, value))
    
    def __str__(self):
        return "StreamStatusEntry - Key: %d : Value: %d" % (self.key, self.value)
    
    @property
    def key(self):
        """unsigned long long (64bit): A unique key made up of module, cmd, option, index, subindex"""
        return self[0]
    
    @property
    def value(self):
        """unsigned int (32bit): The Value associated with the key"""
        return self[1]

    @staticmethod
    def getStreamKeyElement(key, element):
        result = ffi.new("struct Result*")
        _BS_C.link_getStreamKeyElement(result, key, element)
        return Result(result.error, result.value)


# The link class manages the link to the stem. We REALLY only want one
# link to be created. Users should never directly instantiate a Link object.
class Link(object):

    def __init__(self, id):
        self.__id = id


    @property
    def id(self):
        """unsigned int: A unique identifier of the associated module"""
        return self.__id[0]


    @property
    def _id_pointer(self):
        """unsigned int*: pointer to the unique identifier."""
        return self.__id


    def enableStream(self, module_address, cmd, option, index, enable):
        """ 
        Enables streaming for the supplied criteria.

        :param module_address: Address of module on link (stem.address is yourself)
        :type module_address: unsigned byte

        :param cmd: The command code.
        :type cmd: unsigned byte

        :param option: The option code.
        :type option: unsigned byte

        :param index: The entity index.
        :type index: unsigned byte

        :param enable: Enable (True) or disable (False) streaming.
        :param enable: bool

        :return: An error result from the list of defined error codes in brainstem.result
        """
        result = ffi.new("struct Result*")
        _BS_C.link_enableStream(self._id_pointer, result, module_address, cmd, option, index, enable)
        return result.error


    def getLinkSpecifier(self):
        """
        Retrieves the current connection specification

:       return: :return: Result object containing the requested value when the results error is set to NO_ERROR(0)
        :rtype: Result containing a Spec
        """
        result = ffi.new("struct Result*")
        cspec = ffi.new("struct linkSpec_CCA*")
        _BS_C.link_getLinkSpecifier(self._id_pointer, result, cspec)
        return Result(result.error, Spec.cca_spec_to_python_spec(cspec))


    def registerStreamCallback(self, module_address, cmd, option, index, enable, cb, pRef):
        """ 
        Registers a callback function based on a specific module, cmd, option, and index.

        :param module_address: Address of module on link (stem.address is yourself)
        :type module_address: unsigned byte

        :param cmd: The command code.
        :type cmd: unsigned byte

        :param option: The option code.
        :type option: unsigned byte

        :param index: The entity index.
        :type index: unsigned byte

        :param enable: Enable (True) or disable (False) streaming.
        :param enable: bool

        :param cb Callback to be executed on the provided criteria. 
        :type cb: @ffi.callback("unsigned char(aPacket*, void*)")

        :param pRef Handle to be passed to the provided callback. This handle must be kept alive by the caller. 
        :type pRef: ffi handle    

        :return: An error result from the list of defined error codes in brainstem.result
        """
        result = ffi.new("struct Result*")
        _BS_C.link_registerStreamCallback(self._id_pointer, result, module_address, cmd, option, index, enable, cb, pRef)
        return result.error


    def getStreamStatus(self, module_address, cmd, option, index, sub_index, buffer_length=1024):
        """ 
        Gets all available stream values based on the search criteria. 0xFF can be used as a wildcard for all possible values

        :param module_address: Address of module on link (stem.address is yourself)
        :type module_address: unsigned byte

        :param cmd: The command code.
        :type cmd: unsigned byte

        :param option: The option code.
        :type option: unsigned byte

        :param index: The entity index.
        :type index: unsigned byte

        :param sub_index: The sub index.
        :type sub_index: unsigned byte

        :param buffer_length: Size of the buffer to allocate
        :type buffer_length: subIndex int

        :return: An error result from the list of defined error codes in brainstem.result
        """
        result = ffi.new("struct Result*")
        data = ffi.new("struct StreamStatusEntry_CCA[]", buffer_length)
        _BS_C.link_getStreamStatus(self._id_pointer, result, module_address, cmd, option, index, sub_index, data, buffer_length)
        if result.error:
            return Result(result.error, tuple(list()))

        status_list = []
        for x in range(0, result.value):
            status_list.append(StreamStatusEntry(data[x].key, data[x].value))

        return Result(result.error, tuple(status_list))





