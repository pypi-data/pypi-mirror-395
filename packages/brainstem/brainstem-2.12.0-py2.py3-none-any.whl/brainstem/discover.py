# Copyright (c) 2018 Acroname Inc. - All Rights Reserved
#
# This file is part of the BrainStem (tm) package which is released under MIT.
# See file LICENSE or go to https://acroname.com for full license details.

"""
A module that provides methods for discovering brainstem modules over USB and TPCIP.

The discovery module provides an interface for locating BrainStem modules accross
multiple transports. It provides a way to find all modules for a give transport
as well as specific modules by serial number, or first found. The result of a call
to one of the discovery functions is either a list of brainstem.link.Spec objects,
or a single brainstem.link.Spec.

The Discovery module allows users to find specific brainstem devices via their
serial number, or a list of all devices connected to the host via usb or on the
same subnet via TCP/IP. In all cases a :doc:`Spec <link>` object is returned with
connection details for the device. In addition do connection details, the BrainStem
model is returned. This model is one of a list of BrainStem device model numbers
which are accessible via the :doc:`defs <defs>` module.

A typical interactive python session finding all connected USB modules might look
like the following.

    >> import brainstem
    >> module_list = brainstem.discover.findAllModules(brainstem.link.Spec.USB)
    >> print [str(s) for s in module_list]
    ['Model: 4 LinkType: USB(serial: 0xCB4A3B25, module: 0)', 'Model: 13 LinkType: USB(serial: 0x40F5849A, module: 0)']

For an overview of links, discovery and the Brainstem network
see the `Acroname BrainStem Reference`_

.. _Acroname BrainStem Reference:
    https://acroname.com/reference
"""

from . import _BS_C, ffi
from .link import Spec, aEtherConfig
from .result import Result

def findModule(transports, serial_number, network_interface=_BS_C.LOCALHOST_IP_ADDRESS):
    """ 
    Return the Spec for the module with the given serial number.

    Transports can be presented as a list. TCPIP modules
    take a little longer to find due to the Multicast and gather
    necessary for finding modules on the local network segment.

    :param transports: A list of transports or a single transport.
    :type transports: int or list(int)
    :param serial_number: The module serial_number to look for.
    :type serial_number: unsigned int
    :param network_interface: The network interface to use for the discovery.
    :type network_interface: unsigned int

    :return: The connection spec for the module whose serial number is given in the args.
    """
    if not hasattr(transports, '__iter__'):
        transports = [transports]

    for trans in transports:

        cspec = ffi.new("struct linkSpec_CCA*")
        result = ffi.new("struct Result*")
        fake_id = ffi.new("unsigned int*")
        fake_id[0] = 0
        _BS_C.module_findModule(fake_id, result, cspec, serial_number, network_interface, trans)
        
        if result.error == Result.NO_ERROR:
            return Spec.cca_spec_to_python_spec(cspec)

    return None


def findFirstModule(transports, network_interface=_BS_C.LOCALHOST_IP_ADDRESS):
    """ 
    Return the Spec for the first module found on the given transport.

    :param transports: A list of transports or a single transport.
    :type transports: int or list(int)
    :param network_interface: The network interface to use for the discovery.
    :type network_interface: unsigned int

    :return: The connection spec of the first module found on the given transport.
    :rtype: Spec
    """
    if not hasattr(transports, '__iter__'):
        transports = [transports]

    for trans in transports:

        cspec = ffi.new("struct linkSpec_CCA*")
        result = ffi.new("struct Result*")
        fake_id = ffi.new("unsigned int*") #signature required, but not used. 
        fake_id[0] = 0
        _BS_C.module_findFirstModule(fake_id, result, cspec, network_interface, trans)
        
        if result.error == Result.NO_ERROR:
            return Spec.cca_spec_to_python_spec(cspec)

    return None


def findAllModules(transports, network_interface=_BS_C.LOCALHOST_IP_ADDRESS, buffer_length=128):
    """ 
    Return a list of Specs for all modules found on the transports given.

    Transports can be presented as a list, and the results would be
    a list of all modules found for those transports. TCPIP modules
    take a little longer to find due to the Multicast and gather
    necessary for finding modules on the local network segment.

    :param transports: A list of transports or a single transport.
    :type transports: int or list(int)
    :param network_interface: The network interface to use for the discovery.
    :type network_interface: unsigned int
    :param buffer_length: The length of the buffer to use for the discovery.
    :type buffer_length: unsigned int

    :return: A list of the Spec objects for all modules found.
    :rtype: list(Spec)
    """
    if not hasattr(transports, '__iter__'):
        transports = [transports]

    return_list = []
    for trans in transports:

        ffi_buffer = ffi.new("struct linkSpec_CCA[]", buffer_length)
        result = ffi.new("struct Result*")
        fake_id = ffi.new("unsigned int*")
        fake_id[0] = 0
        _BS_C.module_sDiscover(fake_id, result, ffi_buffer, buffer_length, network_interface, trans)
        return_list += [Spec.cca_spec_to_python_spec(ffi_buffer[i]) for i in range(result.value)]

    return return_list


def getIPv4Interfaces(list_length=30):
    """ 
    Populates a list with all of the available IPv4 Interfaces.

    :param list_length: Size of list to allocate for. 
    :type list_length: unsigned int

    :return: A tuple of IPv4 interfaces.
    :rtype: tuple(unsigned int)
    """
    result = ffi.new("struct Result*")
    data = ffi.new("unsigned int[]", list_length)
    _BS_C.module_GetIPv4Interfaces(result, data, list_length)
    
    device_list = []
    if result.error == Result.NO_ERROR:
        for x in range(0, result.value):
            device_list.append(data[x])

    return tuple(device_list)


class DeviceNode(object):
    """
    Python representation of DeviceNode_t (C structure)
        - hub_serial_number (uint32_t): Serial number of the Acroname hub where the device was found.
        - hub_port (uint8_t): Port of the Acroname hub where the device was found.
        - id_vendor (uint16_t): Manufactures Vendor ID of the downstream device.
        - id_product (uint16_t): Manufactures Product ID of the downstream device.
        - speed (enumeration): The devices downstream device speed.
            - Unknown (0)
            - Low Speed (1)
            - Full Speed (2)
            - High Speed (3)
            - Super Speed (4)
            - Super Speed Plus (5)
        - product_name (string): USB string descriptor.
        - manufacture (string): USB string descriptor.
        - serial_number (string): USB string descriptor.
    """
    def __init__(self):

        self.hub_serial_number = 0
        self.hub_port = 0

        self.id_vendor = 0
        self.id_product = 0
        self.speed = 0
        self.product_name = ""
        self.manufacture = ""
        self.serial_number = ""

    def __str__(self):
        ret = "\n"
        ret = ret + "SN: 0x%08X\n" % self.hub_serial_number
        ret = ret + "Port: %d\n" % self.hub_port
        ret = ret + "\tVendor ID: 0x%04X\n" % self.id_vendor
        ret = ret + "\tProduct ID: 0x%04X\n" % self.id_product
        ret = ret + "\tSpeed: %d\n" % self.speed
        ret = ret + "\tProduct Name: %s\n" % self.product_name
        ret = ret + "\tManufacture: %s\n" % self.manufacture
        ret = ret + "\tSerial Number: %s\n" % self.serial_number
        return ret

    def __repr__(self):
        return self.__str__()


def getDownstreamDevices(list_length=128):
    """
    Gets downstream device USB information for all Acroname hubs.
    
    :param list_length: The amount of memory to provide for the lower level C call.
            
    :return: Result object containing NO_ERROR and a tuple of DeviceNode's containing the detected downstream devices::
        - **aErrParam**: Passed in values are not valid (NULL, size, etc).
        - **aErrMemory**: No more room in the list.
        - **aErrNotFound**: No Acroname devices were found.
    :rtype: Result
    """

    data = ffi.new("struct DeviceNode_CCA[]", list_length)
    result = ffi.new("struct Result*")
    _BS_C.portMapping_getDownstreamDevices(result, data, list_length)
    if result.error:
        return Result(result.error, tuple(list()))

    device_list = []
    for x in range(0, result.value):
        node = DeviceNode()
        node.hub_serial_number = data[x].hubSerialNumber
        node.hub_port = data[x].hubPort
        node.id_vendor = data[x].idVendor
        node.id_product = data[x].idProduct
        node.speed = data[x].speed
        node.product_name = ffi.string(data[x].productName)
        node.manufacture = ffi.string(data[x].manufacturer)
        node.serial_number = ffi.string(data[x].serialNumber)
        device_list.append(node)

    return Result(result.error, tuple(device_list))


