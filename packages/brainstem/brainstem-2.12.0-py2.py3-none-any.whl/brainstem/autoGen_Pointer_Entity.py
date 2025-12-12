# This file was auto-generated. Do not modify.

from ._bs_c_cffi import ffi
from . import _BS_C #imported from __init__
from .Entity_Entity import *
from .result import Result
from .ffi_utils import data_to_bytearray, bytes_to_string, handle_sign, handle_sign_value, get_ffi_buffer

class Pointer(Entity):
    
    ''' 
    Allows access to the reflex scratchpad from a host computer.
    
    The Pointers access the pad which is a shared memory area on a BrainStem module.
    The interface allows the use of the BrainStem scratchpad from the host, and provides a
    mechanism for allowing the host application and BrainStem relexes to communicate.
    
    The Pointer allows access to the pad in a similar manner as a file pointer accesses the
    underlying file.
    The cursor position can be set via setOffset. A read of a character short or int can be
    made from that cursor position.
    
    In addition the mode of the pointer can be set so that the cursor position automatically
    increments or set so that it does not this allows for multiple reads of the same pad
    value, or reads of multi-record values, via an incrementing pointer.
    
    ''' 

    POINTER_MODE_STATIC = 0
    POINTER_MODE_INCREMENT = 1

    def __init__(self, module, index):
        super(Pointer, self).__init__(module, _BS_C.cmdPOINTER, index)

    def getOffset(self):

        '''
        Get the offset of the pointer
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned short
                    The value of the offset.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.pointer_getOffset(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 16, False)


    def setOffset(self, offset):

        '''
        Set the offset of the pointer
        
        Parameters
        ----------
        offset : unsigned short
            The value of the offset.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.pointer_setOffset(self._module._id_pointer, result, self._index, offset)
        return result.error


    def getMode(self):

        '''
        Get the mode of the pointer
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    The mode: aPOINTER_MODE_STATIC or aPOINTER_MODE_AUTO_INCREMENT.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.pointer_getMode(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setMode(self, mode):

        '''
        Set the mode of the pointer
        
        Parameters
        ----------
        mode : unsigned char
            The mode: aPOINTER_MODE_STATIC or aPOINTER_MODE_AUTO_INCREMENT.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.pointer_setMode(self._module._id_pointer, result, self._index, mode)
        return result.error


    def getTransferStore(self):

        '''
        Get the handle to the store.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    The handle of the store.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.pointer_getTransferStore(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setTransferStore(self, handle):

        '''
        Set the handle to the store.
        
        Parameters
        ----------
        handle : unsigned char
            The handle of the store.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.pointer_setTransferStore(self._module._id_pointer, result, self._index, handle)
        return result.error


    def initiateTransferToStore(self, transfer_length):

        '''
        Transfer data to the store.
        
        Parameters
        ----------
        transfer_length : unsigned char
            The length of the data transfer.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.pointer_initiateTransferToStore(self._module._id_pointer, result, self._index, transfer_length)
        return result.error


    def initiateTransferFromStore(self, transfer_length):

        '''
        Transfer data from the store.
        
        Parameters
        ----------
        transfer_length : unsigned char
            The length of the data transfer.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.pointer_initiateTransferFromStore(self._module._id_pointer, result, self._index, transfer_length)
        return result.error


    def getChar(self):

        '''
        Get a char (1 byte) value from the pointer at this object's index, where elements are 1
        byte long.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    The value of a single character (1 byte) stored in the pointer.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.pointer_getChar(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setChar(self, value):

        '''
        Set a char (1 byte) value to the pointer at this object's element index, where elements
        are 1 byte long.
        
        Parameters
        ----------
        value : unsigned char
            The single char (1 byte) value to be stored in the pointer.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.pointer_setChar(self._module._id_pointer, result, self._index, value)
        return result.error


    def getShort(self):

        '''
        Get a short (2 byte) value from the pointer at this objects index, where elements are 2
        bytes long
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned short
                    The value of a single short (2 byte) stored in the pointer.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.pointer_getShort(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 16, False)


    def setShort(self, value):

        '''
        Set a short (2 bytes) value to the pointer at this object's element index, where elements
        are 2 bytes long.
        
        Parameters
        ----------
        value : unsigned short
            The single short (2 byte) value to be set in the pointer.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.pointer_setShort(self._module._id_pointer, result, self._index, value)
        return result.error


    def getInt(self):

        '''
        Get an int (4 bytes) value from the pointer at this objects index, where elements are 4
        bytes long
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    The value of a single int (4 byte) stored in the pointer.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.pointer_getInt(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


    def setInt(self, value):

        '''
        Set an int (4 bytes) value from the pointer at this objects index, where elements are 4
        bytes long
        
        Parameters
        ----------
        value : unsigned int
            The single int (4 byte) value to be stored in the pointer.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.pointer_setInt(self._module._id_pointer, result, self._index, value)
        return result.error


