# This file was auto-generated. Do not modify.

from ._bs_c_cffi import ffi
from . import _BS_C #imported from __init__
from .Entity_Entity import *
from .result import Result
from .ffi_utils import data_to_bytearray, bytes_to_string, handle_sign, handle_sign_value, get_ffi_buffer

class I2C(Entity):
    
    ''' 
    Interface the I2C buses on BrainStem modules.
    The class provides a way to send read and write commands to I2C devices on the entities
    bus.
    
    ''' 

    I2C_DEFAULT_SPEED = 0
    I2C_SPEED_100Khz = 1
    I2C_SPEED_400Khz = 2
    I2C_SPEED_1000Khz = 3

    def __init__(self, module, index):
        super(I2C, self).__init__(module, _BS_C.cmdI2C, index)

    def read(self, address, read_length):

        '''
        Read from a device on this I2C bus.
        
        Parameters
        ----------
        address : unsigned char
            The I2C address (7bit <XXXX-XXX0>) of the device to read.
        read_length : unsigned char
            The length of the data to read in bytes.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : list(unsigned char)
                    The array of bytes that will be filled with the result, upon success.
                    This array should be larger or equivalent to aBRAINSTEM_MAXPACKETBYTES - 5
        
        '''

        ffi_buffer = get_ffi_buffer(8, False, 256)

        result = ffi.new("struct Result*")
        _BS_C.i2c_read(self._module._id_pointer, result, self._index, address, read_length, ffi_buffer)
        return_list = [handle_sign_value(ffi_buffer[i], 8, False) for i in range(result.value)]
        return Result(result.error, [ffi_buffer[i] for i in range(result.value)])


    def write(self, address, buffer):

        '''
        Write to a device on this I2C bus.
        
        Parameters
        ----------
        address : unsigned char
            The I2C address (7bit <XXXX-XXX0>) of the device to write.
        buffer : unsigned char
            The data to send to the device
            This array should be no larger than aBRAINSTEM_MAXPACKETBYTES - 5
        
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
        _BS_C.i2c_write(self._module._id_pointer, result, self._index, address, buffer_length, ffi_buffer)
        return result.error


    def setPullup(self, enable):

        '''
        Set bus pull-up state.
        This call only works with stems that have software controlled pull-ups.
        Check the datasheet for more information.
        This parameter is saved when system.save is called.
        
        Parameters
        ----------
        enable : bool
            true enables pull-ups false disables them.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.i2c_setPullup(self._module._id_pointer, result, self._index, enable)
        return result.error


    def setSpeed(self, speed):

        '''
        Set I2C bus speed.
        
        This call sets the communication speed for I2C transactions through this API.
        Speed is an enumeration value which can take the following values:
            1 - 100Khz
            2 - 400Khz
            3 - 1MHz
        
        Parameters
        ----------
        speed : unsigned char
            The speed setting value.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.i2c_setSpeed(self._module._id_pointer, result, self._index, speed)
        return result.error


    def getSpeed(self):

        '''
        Get I2C bus speed.
        
        This call gets the communication speed for I2C transactions through this API.
        Speed is an enumeration value which can take the following values:
            1 - 100Khz
            2 - 400Khz
            3 - 1MHz
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    The speed setting value.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.i2c_getSpeed(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


