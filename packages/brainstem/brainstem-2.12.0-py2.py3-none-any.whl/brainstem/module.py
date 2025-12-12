# Copyright (c) 2018 Acroname Inc. - All Rights Reserved
#
# This file is part of the BrainStem (tm) package which is released under MIT.
# See file LICENSE or go to https://acroname.com for full license details.

"""
A module that provides base classes for BrainStem Modules and Entities.

The Module and Entity classes are designed to be extended for specific types
of BrainStem Modules and Entities. For more information about Brainstem Modules
and Entities, please see the `Terminology`_ section of the `Acroname BrainStem Reference`_

.. _Terminology:
    https://acroname.com/reference/brainstem/terms.html

.. _Acroname BrainStem Reference:
    https://acroname.com/reference
"""

from ._bs_c_cffi import ffi
from . import _BS_C #imported from __init__
from .result import Result
from .link import Link, aEtherConfig, Spec
from .Entity_Entity import * 

class Module(object):
    """
        The Module Entity provides a generic interface to a BrainStem hardware module.
        The Module Class is the parent class for all BrainStem modules. Each module
        inherits from Module and implements its hardware specific features.
    """


    def __init__(self, address, enable_auto_networking=True, model=0):
        # Internal vars
        self.__id = ffi.new("unsigned int*")
        self.__model = model
        self.__bAutoNetworking = enable_auto_networking 
        self.__link = Link(self.__id)

        result = ffi.new("struct Result*")

        # Create internal object (lib)
        _BS_C.module_createStem(self.__id, result, address, enable_auto_networking, model)


    def __del__(self):
        result = ffi.new("struct Result*")
        _BS_C.module_disconnectAndDestroyStem(self.__id, result)


    @property
    def id(self):
        """unsigned int: A unique identifier of the associated module"""
        return self.__id[0]


    @property
    def _id_pointer(self):
        """unsigned int*: pointer to the unique identifier."""
        return self.__id


    @property
    def address(self):
        """unsigned byte: Module address of the device"""
        result = self.getModuleAddress()
        if result.error == Result.NO_ERROR:
            return result.value
        else:
            return 0


    @property
    def bAutoNetworking(self):
        """ bool: Return the current networking mode. """
        return self.__bAutoNetworking


    @property
    def model(self):
        """unsigned byte: Model number of the device"""
        return self.__model


    @property
    def link(self):
        """ Link: return the current link or None. """
        return self.__link


    def getConfig(self):
        """ 
        Gets the links current aEther configuration

        :return: Result object containing the requested value when the results error is set to NO_ERROR(0)
        :rtype: Result containing a aEtherConfig
        """
        cca_config = ffi.new("struct aEtherConfig_CCA*")
        result = ffi.new("struct Result*")
        _BS_C.module_getAetherConfig(self._id_pointer, result, cca_config)
        config = aEtherConfig.cca_config_to_python_config(cca_config)

        return Result(result.error, config)
 

    def setConfig(self, config):
        """ 
        Sets the links aEther configuration.
        Note: Configuration must be set BEFORE connection.

        :param config: (aEtherConfig object): aEther configuration to be set.
        :type config: aEtherConfig

        :return: An error result from the list of defined error codes in brainstem.result
        """
        cca_config = ffi.new("struct aEtherConfig_CCA*")
        aEtherConfig.python_config_to_cca_config(config, cca_config)

        result = ffi.new("struct Result*")
        _BS_C.module_setAetherConfig(self._id_pointer, result, cca_config)
        return result.error


    def discoverAndConnect(self, transport, serial_number=0):
        """ 
        Discover and connect from the Module level.

        A discover-based connect. This member function will connect to the first
        available BrainStem found on the given transport.  If the serial number is
        passed, it will only connect to the module with that serial number.
        Passing 0 or None as the serial number will create a link to the first
        link module found on the specified transport.

        :param transport: (Spec.transport): One of USB, TCPIP, SERIAL or AETHER.
        :type transport: Spec.transport

        :param serial_number: The module serial_number to look for.
        :type serial_number: unsigned int
    
        :return: An error result from the list of defined error codes in brainstem.result
        """
        result = ffi.new("struct Result*")
        _BS_C.module_discoverAndConnect(self._id_pointer, result, transport, serial_number)
        return result.error


    def connectFromSpec(self, spec):
        """ 
        Connect to a BrainStem module with a Spec.

        :param spec: The specifier for the connection.
        :type spec: Spec

        :return: An error result from the list of defined error codes in brainstem.result
        """
        if spec is None:
            return Result.PARAMETER_ERROR

        result = ffi.new("struct Result*")
        cspec = ffi.new("struct linkSpec_CCA*")
        Spec.python_spec_to_cca_spec(spec, cspec)
        _BS_C.module_connectFromSpec(self._id_pointer, result, cspec)
        return result.error


    def disconnect(self):
        """ Disconnect from the Brainstem module."""
        result = ffi.new("struct Result*")
        _BS_C.module_disconnect(self._id_pointer, result)
        return result.error


    def connect(self, transport, serial_number):
        """ 
        Connect to a Module with a transport type and serial number.

        :param transport: (Spec.transport): One of USB, TCPIP, SERIAL or AETHER.
        :type transport: Spec.transport

        :param serial_number: The module serial_number to look for.
        :type serial_number: unsigned int

        :return: An error result from the list of defined error codes in brainstem.result
        """
        return self.discoverAndConnect(transport, serial_number)


    def isConnected(self):
        """ Returns true if the Module has an active connection or false otherwise"""
        result = ffi.new("struct Result*")
        _BS_C.module_isConnected(self._id_pointer, result)
        return True if result.value else False


    def reconnect(self):
        """ Reconnect a lost connection to a Brainstem module."""
        result = ffi.new("struct Result*")
        _BS_C.module_reconnect(self._id_pointer, result)
        return result.error


    def getStatus(self):
        """ 
        Returns the status of the BrainStem connection
        See brainstem.link.Status for the possible states.

        """
        result = ffi.new("struct Result*")
        _BS_C.module_getStatus(self._id_pointer, result)
        return result.value


    def connectThroughLinkModule(self, module):
        """ 
        Connects to a Brainstem module on a BrainStem network, through
        the module given as an argument. The module passed in must have
        an active valid connection.

        :param module: The brainstem module to connect through.
        :type module: Module

        :return: An error result from the list of defined error codes in brainstem.result
        """
        result = ffi.new("struct Result*")
        _BS_C.module_connectThroughLinkModule(self._id_pointer, module._id_pointer, result)
        return result.error


    def setModuleAddress(self, address):
        """ 
        Set the address of the module object.

        This method changes the local address of the module, not of the
        device. It is possible to set the module address of the device via
        system.setModuleSoftwareOffset().

        :param address: The module address to switch to for this module instance.
        :type address: unsigned byte

        :return: An error result from the list of defined error codes in brainstem.result
        """
        result = ffi.new("struct Result*")
        _BS_C.module_setModuleAddress(self._id_pointer, result, address)
        return result.error


    def getModuleAddress(self):
        """ 
        Get the address of the module object.

        This method changes the local address of the module, not of the
        device. It is possible to get the module address of the device via
        system.getModuleSoftwareOffset().

        :return: Result object containing the requested value when the results error is set to NO_ERROR(0)
        """
        result = ffi.new("struct Result*")
        _BS_C.module_getModuleAddress(self._id_pointer, result)
        return Result(result.error, result.value)


    def setNetworkingMode(self, mode):
        """ 
        Changes the networking mode of the stem object.  Auto mode is enabled by default
        which allows automatic adjustment of the module/stems networking configuration.
        Refer to BrainStem Networking at www.acroname.com/support

        :param mode: Mode to be set. True = Auto; False = Manual
        :type mode: bool
        
        :return: An error result from the list of defined error codes in brainstem.result
        """
        result = ffi.new("struct Result*")
        _BS_C.module_setNetworkingMode(self._id_pointer, result, mode)
        if result.error == Result.NO_ERROR:
            self.__bAutoNetworking = result.value
        return result.error


    def getBuild(self):
        """ 
        Get the modules firmware build number
        The build number is a unique hash assigned to a specific firmware.

        :return: Result object containing the requested value when the results error is set to NO_ERROR(0)
        """
        result = ffi.new("struct Result*")
        _BS_C.module_getBuild(self._id_pointer, result)
        return Result(result.error, result.value)


    def hasUEI(self, command, option, index, flags):
        """ 
        Queries the module to determine if it implements a UEI. Each
        UEI has a command, option or variant, index and flag. The hasUEI method
        queries for a fully specified UEI.
        Returns aErrNone if the variation is supported and an appropriate error
        if not. This call is blocking for up to the nMSTimeout period.

        :param command: One of the UEI commands (cmdXXX).
        :type command: unsigned byte

        :param option: The option or variant of the command.
        :type option: unsigned byte

        :param index: The entity index.
        :type index: unsigned byte

        :param flags: The flags (ueiOPTION_SET or ueiOPTION_GET).
        :type flags: unsigned byte

        :return: Result object containing the requested value when the results error is set to NO_ERROR(0)
        """
        result = ffi.new("struct Result*")
        _BS_C.module_hasUEI(self._id_pointer, result, command, option, index, flags)
        return Result(result.error, result.value)


    def classQuantity(self, command):
        """ 
        Queries the module to determine how many entities of the specified
        class are implemented by the module. Zero is a valid return value.
        For example, calling classQuantity with the command parameter of
        cmdANALOG would return the number of analog entities implemented by the module.

        :param command: One of the UEI commands (cmdXXX).
        :type command: unsigned byte

        :return: Result object containing the requested value when the results error is set to NO_ERROR(0)
        """
        result = ffi.new("struct Result*")
        _BS_C.module_classQuantity(self._id_pointer, result, command)
        return Result(result.error, result.value)


    def subClassQuantity(self, command, index):
        """ 
        Queries the module to determine how many subclass entities of the specified
        class are implemented by the module for a given entity index. This is used
        for entities which may be 2-dimensional. E.g. cmdMUX subclasses are the number
        of channels supported by a particular mux type (index); as a specific example,
        a module may support 4 UART channels, so subClassQuantity(cmdMUX, aMUX_UART...)
        could return 4.
        Zero is a valid return value.

        :param command: One of the UEI commands (cmdXXX).
        :type command: unsigned byte

        :return: Result object containing the requested value when the results error is set to NO_ERROR(0)
        """
        result = ffi.new("struct Result*")
        _BS_C.module_subClassQuantity(self._id_pointer, result, command, index)
        return Result(result.error, result.value)


    def entityGroup(self, command, index):
        """ 
        Queries the module the group assigned to an entity and index. Entities groups
        are used to specify when certain hardware features are fundamentally related. E.g.
        certain hardware modules may have some digital pins associated with an adjustable
        voltage rail; these digitals would be in the same group as the rail.
        Zero is the default group.

        :param command: One of the UEI commands (cmdXXX).
        :type command: unsigned byte

        :return: Result object containing the requested value when the results error is set to NO_ERROR(0)
        """
        result = ffi.new("struct Result*")
        _BS_C.module_entityGroup(self._id_pointer, result, command, index)
        return Result(result.error, result.value)



