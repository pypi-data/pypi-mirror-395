# This file was auto-generated. Do not modify.

from ._bs_c_cffi import ffi
from . import _BS_C #imported from __init__
from .Entity_Entity import *
from .result import Result
from .ffi_utils import data_to_bytearray, bytes_to_string, handle_sign, handle_sign_value, get_ffi_buffer

class Store(Entity):
    
    ''' 
    The store provides a flat file system on modules that have storage capacity.
    Files are referred to as slots and they have simple zero-based numbers for access.
    Store slots can be used for generalized storage and commonly contain compiled reflex code
    (files ending in .map) or templates used by the system.
    Slots simply contain bytes with no expected organization but the code or use of the slot
    may impose a structure.
    Stores have fixed indices based on type.
    Not every module contains a store of each type. Consult the module datasheet for details
    on which specific stores are implemented, if any, and the capacities of implemented
    stores.
    
    ''' 

    INTERNAL_STORE = 0
    RAM_STORE = 1
    SD_STORE = 2
    EEPROM_STORE = 3

    def __init__(self, module, index):
        super(Store, self).__init__(module, _BS_C.cmdSTORE, index)

    def getSlotState(self, slot):

        '''
        Get slot state.
        
        Parameters
        ----------
        slot : unsigned char
            The slot number.
        
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
        _BS_C.store_getSlotState(self._module._id_pointer, result, self._index, slot)
        return handle_sign(Result(result.error, result.value), 8, False)


    def loadSlot(self, slot, buffer):

        '''
        Load the slot.
        
        Parameters
        ----------
        slot : unsigned char
            The slot number.
        buffer : unsigned char
            The data.
        
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
        _BS_C.store_loadSlot(self._module._id_pointer, result, self._index, slot, ffi_buffer, buffer_length)
        return result.error


    def unloadSlot(self, slot, buffer_length = 65536):

        '''
        Unload the slot data.
        
        Parameters
        ----------
        slot : unsigned char
            The slot number.
        buffer_length : unsigned int
            The length of buffer buffer in bytes. This is the maximum number of bytes that should
            be unloaded.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : list(unsigned char)
                    Byte array that the unloaded data will be placed into.
        
        '''

        ffi_buffer = get_ffi_buffer(8, False, buffer_length)

        result = ffi.new("struct Result*")
        _BS_C.store_unloadSlot(self._module._id_pointer, result, self._index, slot, ffi_buffer, buffer_length)
        return Result(result.error, [ffi_buffer[i] for i in range(result.value)])


    def slotEnable(self, slot):

        '''
        Enable slot.
        
        Parameters
        ----------
        slot : unsigned char
            The slot number.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.store_slotEnable(self._module._id_pointer, result, self._index, slot)
        return result.error


    def slotDisable(self, slot):

        '''
        Disable slot.
        
        Parameters
        ----------
        slot : unsigned char
            The slot number.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.store_slotDisable(self._module._id_pointer, result, self._index, slot)
        return result.error


    def getSlotCapacity(self, slot):

        '''
        Get the slot capacity.
        Returns the Capacity of the slot, i.e. The number of bytes it can hold.
        
        Parameters
        ----------
        slot : unsigned char
            The slot number.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    The slot capacity.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.store_getSlotCapacity(self._module._id_pointer, result, self._index, slot)
        return handle_sign(Result(result.error, result.value), 8, False)


    def getSlotSize(self, slot):

        '''
        Get the slot size.
        The slot size represents the size of the data currently filling the slot in bytes.
        
        Parameters
        ----------
        slot : unsigned char
            The slot number.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    The slot size.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.store_getSlotSize(self._module._id_pointer, result, self._index, slot)
        return handle_sign(Result(result.error, result.value), 8, False)


    def getSlotLocked(self, slot):

        '''
        Gets the current lock state of the slot
        Allows for write protection on a slot.
        
        Parameters
        ----------
        slot : unsigned char
            The slot number
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : bool
                    Variable to be filed with the locked state.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.store_getSlotLocked(self._module._id_pointer, result, self._index, slot)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setSlotLocked(self, slot, lock):

        '''
        Sets the locked state of the slot
        Allows for write protection on a slot.
        
        Parameters
        ----------
        slot : unsigned char
            The slot number
        lock : bool
            state to be set.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.store_setSlotLocked(self._module._id_pointer, result, self._index, slot, lock)
        return result.error


