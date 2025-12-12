

from ._bs_c_cffi import ffi
from . import _BS_C #imported from __init__
from .ffi_utils import data_to_bytearray
from .result import Result
from .link import StreamStatusEntry

class Entity(object):
    """
    Base class for BrainStem Entity.

    Provides the default implementation for a functional entity within
    the BrainStem. This can include IO like GPIOs, Analogs etc. For a
    more detailed description of Entities see the `Terminology`_ section
    of the brainstem reference for more information.

    .. _Terminology:
        https://acroname.com/reference/brainstem/terms.html

    """

    def __init__(self, module, cmd, index):
        """
        Initialize an Entity object.

        :param module: The Module this entity belongs to.
        :type module: Module
        :param command The BrainStem command for the entity.
        :type command: int
        :param index The entity index for this entity instance.
        :type index: int
        """
        self._cmd = cmd
        self._index = index
        self._module = module


    @property
    def command(self):
        """int: Return the entity command."""
        return self._cmd


    @property
    def index(self):
        """int: Return the entity index"""
        return self._index


    @property
    def module(self):
        """ Module: returns the associated module object. """
        return self._module


    def call_UEI(self, option):
        """ 
        Call a set UEI on this entity.

        :param option: The command option.
        :type option: byte

        :return: An error result from the list of defined error codes in brainstem.result
        """
        result = ffi.new("struct Result*")
        _BS_C.entity_callUEI(self._module._id_pointer, result, self._cmd, self._index, option)
        return result.error
    
    
    def set_UEI8(self, option, value):
        """ 
        Call a set UEI with byte value on this entity.

        :param option: The command option.
        :type option: byte
        :param value: The byte parameter to send.
        :type value: byte

        :return: An error result from the list of defined error codes in brainstem.result
        """
        result = ffi.new("struct Result*")
        _BS_C.entity_setUEI8(self._module._id_pointer, result, self._cmd, self._index, option, value)
        return result.error
    
    
    def set_UEI8_with_subindex(self, option, subIndex, value):
        """ 
        Call a set UEI byte value with a subIndex.

        :param option: The command option.
        :type option: byte

        :param subIndex: The subIndex of the entity.
        :type subIndex: byte

        :param value: The byte parameter to send.
        :type value: byte

        :return: An error result from the list of defined error codes in brainstem.result
        """
        result = ffi.new("struct Result*")
        _BS_C.entity_setUEI8SubIndex(self._module._id_pointer, result, self._cmd, self._index, option, subIndex, value)
        return result.error
    
    
    def get_UEI8(self, option):
        """ 
        Get a UEI byte value.

        :param option: The command option.
        :type option: byte

        :return: Result object containing the requested value when the results error is set to NO_ERROR(0)
        :rtype: Result
        """
        result = ffi.new("struct Result*")
        _BS_C.entity_getUEI8(self._module._id_pointer, result, self._cmd, self._index, option)
        return Result(result.error, result.value)
    
    
    def get_UEI8_with_subindex(self, option, subIndex):
        """ 
        Call a get UEI byte value with a subIndex.

        :param option: The command option.
        :type option: byte

        :param subIndex: The subIndex of the entity.
        :type subIndex: byte

        :return: Result object containing the requested value when the results error is set to NO_ERROR(0)
        :rtype: Result
        """
        result = ffi.new("struct Result*")
        _BS_C.entity_getUEI8SubIndex(self._module._id_pointer, result, self._cmd, self._index, option, subIndex)
        return Result(result.error, result.value)
    
    
    def set_UEI16(self, option, value):
        """ 
        Call a set UEI with short value on this entity.

        :param option: The command option.
        :type option: byte

        :param value: The short parameter to send.
        :type value: short

        :return: An error result from the list of defined error codes in brainstem.result
        """
        result = ffi.new("struct Result*")
        _BS_C.entity_setUEI16(self._module._id_pointer, result, self._cmd, self._index, option, value)
        return result.error
    
    
    def set_UEI16_with_subindex(self, option, subIndex, value):
        """ 
        Call a set UEI short value with a subIndex.

        :param option: The command option.
        :type option: byte

        :param subIndex: The subIndex of the entity.
        :type subIndex: byte

        :param value: The short parameter to send.
        :type value: short

        :return: An error result from the list of defined error codes in brainstem.result
        """
        result = ffi.new("struct Result*")
        _BS_C.entity_setUEI16SubIndex(self._module._id_pointer, result, self._cmd, self._index, option, subIndex, value)
        return result.error
    
    
    def get_UEI16(self, option):
        """ 
        Get a UEI short value.

        :param option: The command option.
        :type option: byte

        :return: Result object containing the requested value when the results error is set to NO_ERROR(0)
        :rtype: Result
        """
        result = ffi.new("struct Result*")
        _BS_C.entity_getUEI16(self._module._id_pointer, result, self._cmd, self._index, option)
        return Result(result.error, result.value)
    
    
    def get_UEI16_with_subindex(self, option, subIndex):
        """ 
        Call a get UEI short value with a subIndex.

        :param option: The command option.
        :type option: byte

        :param subIndex: The subIndex of the entity.
        :type subIndex: byte

        :return: Result object containing the requested value when the results error is set to NO_ERROR(0)
        :rtype: Result
        """
        result = ffi.new("struct Result*")
        _BS_C.entity_getUEI16SubIndex(self._module._id_pointer, result, self._cmd, self._index, option, subIndex)
        return Result(result.error, result.value)
    
    
    def set_UEI32(self, option, value):
        """ 
        Call a set UEI with int value on this entity.

        :param option: The command option.
        :type option: byte

        :param value: The int parameter to send.
        :type value: int
        """
        result = ffi.new("struct Result*")
        _BS_C.entity_setUEI32(self._module._id_pointer, result, self._cmd, self._index, option, value)
        return result.error
    
    
    def set_UEI32_with_subindex(self, option, subIndex, value):
        """ 
        Call a set UEI int value with a subIndex.

        :param option: The command option.
        :type option: byte

        :param subIndex: The subIndex of the entity.
        :type subIndex: byte

        :param value: The int parameter to send.
        :type value: int

        :return: An error result from the list of defined error codes in brainstem.result
        """
        result = ffi.new("struct Result*")
        _BS_C.entity_setUEI32SubIndex(self._module._id_pointer, result, self._cmd, self._index, option, subIndex, value)
        return result.error
    
    
    def get_UEI32(self, option):
        """ 
        Get a UEI int value.

        :param option: The command option.
        :type option: byte

        :return: Result object containing the requested value when the results error is set to NO_ERROR(0)
        :rtype: Result
        """
        result = ffi.new("struct Result*")
        _BS_C.entity_getUEI32(self._module._id_pointer, result, self._cmd, self._index, option)
        return Result(result.error, result.value)
    
    
    def get_UEI32_with_subindex(self, option, subIndex):
        """ 
        Call a get UEI int value with a subIndex.

        :param option: The command option.
        :type option: byte

        :param subIndex: The subIndex of the entity.
        :type subIndex: byte

        :return: Result object containing the requested value when the results error is set to NO_ERROR(0)
        :rtype: Result
        """
        result = ffi.new("struct Result*")
        _BS_C.entity_getUEI32SubIndex(self._module._id_pointer, result, self._cmd, self._index, option, subIndex)
        return Result(result.error, result.value)
    
    
    def set_UEIBytes(self, option, buffer):
        """ 
        Call a set UEI with buffer and length of buffer on this entity.

        :param option: The command option.
        :type option: byte

        :param buffer: The buffer to be sent
        :type buffer: bytearray()

        :return: An error result from the list of defined error codes in brainstem.result
        """
        result = ffi.new("struct Result*")
        byte_array = data_to_bytearray(buffer)

        buffer_length = len(byte_array)
        ffi_buffer = ffi.new("unsigned char[]", buffer_length)
        for x in range(buffer_length):
            ffi_buffer[x] = byte_array[x]

        _BS_C.entity_setUEIBytes(self._module._id_pointer, result, self._cmd, self._index, option, ffi_buffer, buffer_length)
        return result.error
    
    
    def get_UEIBytes(self, option, buffer_length=65536):
        """ 
        Get a UEI Bytes buffer on this entity.

        :param option: The command option.
        :type option: byte

        :param buffer_length: The subIndex of the entity.
        :type buffer_length: unsigned int

        :return: Result object containing the requested value when the results error is set to NO_ERROR(0)
        :rtype: Result
        """
        result = ffi.new("struct Result*")

        ffi_buffer = ffi.new("unsigned char[]", buffer_length)

        _BS_C.entity_getUEIBytes(self._module._id_pointer, result, self._cmd, self._index, option, ffi_buffer, buffer_length)
        return_list = [ffi_buffer[i] for i in range(result.value)]

        return Result(result.error, return_list)
    
    
    def drain_UEI(self, option):
        """ 
        Drain UEI packets matching option.

        :param option: The command option.
        :type option: byte

        :return: An error result from the list of defined error codes in brainstem.result
        """
        result = ffi.new("struct Result*")
        _BS_C.entity_drainUEI(self._module._id_pointer, result, self._cmd, self._index, option)
        return result.error
    
    
    def setStreamEnabled(self, enable):
        """ 
        Enables streaming for all possible option codes within the cmd and index the entity was created for.

        :param enable: Enable (True) or disable (False) streaming.
        :type enable: bool

        :return: An error result from the list of defined error codes in brainstem.result
        """
        result = ffi.new("struct Result*")
        _BS_C.entity_setStreamEnabled(self._module._id_pointer, result, self._cmd, self._index, enable)
        return result.error
    
    
    def registerOptionCallback(self, option, enable, cb, pRef):
        """ 
        Registers a callback function based on a specific option code. Option code applies to the cmd and index of the called API.

        :param option The option code for the entities command and index.
        :type option: byte

        :param enable Enable (True) or disable (False) streaming.
        :type enable: bool 

        :param cb Callback to be executed on the provided criteria. 
        :type cb: @ffi.callback("unsigned char(aPacket*, void*)")

        :param pRef Handle to be passed to the provided callback. This handle must be kept alive by the caller. 
        :type pRef: ffi handle                  

        :return: An error result from the list of defined error codes in brainstem.result
        """
        return self._module.link.registerStreamCallback(self._module.address, self._cmd, option, self._index, enable, cb, pRef)
    

    def getStreamStatus(self, buffer_length=1024):
        """ 
        Gets all available stream values associated with the cmd and index of the called API.

        :param buffer_length: Size of the buffer to allocate
        :type buffer_length: unsigned int

        :return: An error result from the list of defined error codes in brainstem.result
        """

        result = ffi.new("struct Result*")
        data = ffi.new("struct StreamStatusEntry_CCA[]", buffer_length)
        _BS_C.entity_getStreamStatus(self._module._id_pointer, result, self._cmd, self._index, data, buffer_length)
        if result.error:
            return Result(result.error, tuple(list()))

        status_list = []
        for x in range(0, result.value):
            status_list.append(StreamStatusEntry(data[x].key, data[x].value))

        return Result(result.error, tuple(status_list))


    def resetEntityToFactoryDefaults(self):
        """ 
        Resets the Entity to factory defaults

        :param option: The command option.
        :type option: byte

        :return: An error result from the list of defined error codes in brainstem.result
        """
        result = ffi.new("struct Result*")
        _BS_C.entity_resetEntityToFactoryDefaults(self._module._id_pointer, result, self._cmd, self._index)
        return result.error
    

    def loadEntityFromSavedValues(self):
        """ 
        Load the Entity from memory. 

        :param option: The command option.
        :type option: byte

        :return: An error result from the list of defined error codes in brainstem.result
        """
        result = ffi.new("struct Result*")
        _BS_C.entity_resetEntityToFactoryDefaults(self._module._id_pointer, result, self._cmd, self._index)
        return result.error
    

    def saveEntity(self):
        """ 
        Saves the Entity.

        :param option: The command option.
        :type option: byte

        :return: An error result from the list of defined error codes in brainstem.result
        """
        result = ffi.new("struct Result*")
        _BS_C.entity_resetEntityToFactoryDefaults(self._module._id_pointer, result, self._cmd, self._index)
        return result.error

