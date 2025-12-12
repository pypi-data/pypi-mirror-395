import struct
from . import _BS_C, str_or_bytes_to_bytearray
from .module import Entity
from .result import Result
from ._bs_c_cffi import ffi
from .ffi_utils import data_to_bytearray


class _Factory(Entity):
    """ For internal use only.

    """
    MATCH_MASK = (~((1 << _BS_C.factoryError_Bit) |
                    (1 << _BS_C.factoryStart_Bit) |
                    (1 << _BS_C.factoryEnd_Bit) |
                    (1 << _BS_C.factorySet_Bit)) & 0xFF)

    def __init__(self, module, index):
        """Store initializer"""
        super(_Factory, self).__init__(module, _BS_C.cmdFACTORY, index)

    def getFactoryData(self, command, buffer_length=65536):

        result = ffi.new("struct Result*")

        ffi_buffer = ffi.new("unsigned char[]", buffer_length)
        
        _BS_C.factory_getData(self._module._id_pointer, result, self._index, command, ffi_buffer, len(ffi_buffer))
        return_list = [ffi_buffer[i] for i in range(result.value)]

        #Note: None preserves existing behavior.
        return Result(result.error, tuple(return_list) if result.error == Result.NO_ERROR else None)


    def setFactoryData(self, command, buffer):
        result = ffi.new("struct Result*")
        byte_array = data_to_bytearray(buffer)

        buffer_length = len(byte_array)
        ffi_buffer = ffi.new("unsigned char[]", buffer_length)
        for x in range(buffer_length):
            ffi_buffer[x] = byte_array[x]

        _BS_C.factory_setData(self._module._id_pointer, result, self._index, command, ffi_buffer, buffer_length)
        return result.error

