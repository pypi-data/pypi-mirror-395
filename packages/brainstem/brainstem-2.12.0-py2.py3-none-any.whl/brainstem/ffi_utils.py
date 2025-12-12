# Copyright (c) 2018 Acroname Inc. - All Rights Reserved
#
# This file is part of the BrainStem (tm) package which is released under MIT.
# See file LICENSE or go to https://acroname.com for full license details.

""" Provides version access utilities. """

from ._bs_c_cffi import ffi
from .result import Result


def data_to_bytearray(data):
    if isinstance(data, bytearray):
        return data
    
    elif isinstance(data, str):
        return bytearray(data.encode('utf-8'))

    elif hasattr(data, '__iter__'):
        if len(data) == 0: #This provides index safety of the below elif's
            return bytearray()
        elif isinstance(data[0], str):
            return bytearray([ord(char) for char in data])
        else:
            return bytearray(data)

    elif isinstance(data, int):
        return bytearray([data])
        
    #This covers:
    # - isinstance(data, tuple):
    # - isinstance(data, bytearray):
    # - isinstance(data, bytes):
    # - and everything else. 
    else:
        return bytearray(data)


def bytes_to_string(result):
    """ Helper function for UEIBytes to convert byte array value to a string

        args:
            result (Result): The Result object from a get_UEIBytes

        returns:
            Result: Returns a result object, whose value is set,
                    or with the requested value when the results error is
                    set to NO_ERROR
    """
    if result.error != Result.NO_ERROR:
        return result

    temp_value = bytes(result.value).decode('utf-8')
    return Result(Result.NO_ERROR, temp_value)


def handle_sign(result, num_bits=0, signed=True):
    """ Helper function for managing the sign of the returned value.
        The CCA Result object is of type int; however, sometimes the
        values returned are unsigned. 

        args:
            result (Result (CCA)): The CCA Result object
            num_bits (uint): The number of bits the value represents
            signed (bool): Indicates if the value is signed or not.

        returns:
            Result: Returns a python result object, whose value is set,
                    or with the requested value when the results error is
                    set to NO_ERROR
    """
    value = result.value # Move value out of c type object.
    if result.error == Result.NO_ERROR:
        value = handle_sign_value(value, num_bits, signed)

    return Result(result.error, value)

def handle_sign_value(value, num_bits=0, signed=True):
    """ Helper function for managing the sign of the returned value.
        The CCA Result object is of type int; however, sometimes the
        values returned are unsigned. 

        args:
            result (Result (CCA)): The CCA Result object
            num_bits (uint): The number of bits the value represents
            signed (bool): Indicates if the value is signed or not.

        returns:
            Result: Returns a python result object, whose value is set,
                    or with the requested value when the results error is
                    set to NO_ERROR
    """
    if num_bits and not signed:
        return value & ((1 << num_bits)-1) if value < 0 else value
    return value

def get_ffi_buffer(size, signed, buffer_length):
    """ Helper function to create a FFI Buffer object

        args:
            size (uint): Number of bits in each element
            signed (bool): The signedness of each element
            buffer_length (uint): Number of items to create in buffer

        returns:
            cdata[]: FFI Buffer Type
    """

    buffer_type = 'unsigned ' if not signed else ''
    if size == 8:
        buffer_type += "char"
    elif size == 16:
        buffer_type += "short"
    elif size == 32:
        buffer_type += "int"
    else:
        raise ValueError("Function Prameters requires size of 8, 16, or 32 bits")
    
    return ffi.new("{}[]".format(buffer_type), buffer_length)