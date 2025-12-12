# Copyright (c) 2018 Acroname Inc. - All Rights Reserved
#
# This file is part of the BrainStem (tm) package which is released under MIT.
# See file LICENSE or go to https://acroname.com for full license details.

"""
A module that provides a result class for returning results of UEI commands.

Results consist of an error attribute and a value attribute. If the error
attribute is set to NO_ERROR, then the result value is the response to the
UEI command that was sent.

For more information about return values for commands and UEI's
see the `Acroname BrainStem Reference`_

.. _Acroname BrainStem Reference:
    https://acroname.com/reference
"""
from . import _BS_C, ffi
import types

class Result(object):
    """ Result class for returning results of commands

        Instances of Result represent the response to a command. The Result class
        also contains constants for the error codes that Brainstem APIs may return,
        for example Result.aErrNone, result.aErrorMemory, etc.
        Refer to the C API Error Codes for a complete list.
    """

    NO_ERROR               = _BS_C.aErrNone           # 0: No Error occurred.
    MEMORY_ERROR           = _BS_C.aErrMemory         # 1: Memory allocation/de-allocation error.
    PARAMETER_ERROR        = _BS_C.aErrParam          # 2: Invalid parameters given.
    NOT_FOUND              = _BS_C.aErrNotFound       # 3: Entity, module or information not found.
    FILE_NAME_LENGTH_ERROR = _BS_C.aErrFileNameLength # 4: File name is to long.
    BUSY                   = _BS_C.aErrBusy           # 5: Module or resource is currently busy.
    IO_ERROR               = _BS_C.aErrIO             # 6: An Input/Output error occurred.
    MODE_ERROR             = _BS_C.aErrMode           # 7: Invalid Mode or mode not accessible for current state.
    WRITE_ERROR            = _BS_C.aErrWrite          # 8: Write error occurred.
    READ_ERROR             = _BS_C.aErrRead           # 9: Read error occurred.
    EOF_ERROR              = _BS_C.aErrEOF            # 10: Unexpected end of file encountered.
    NOT_READY              = _BS_C.aErrNotReady       # 11: Resource not ready.
    PERMISSION_ERROR       = _BS_C.aErrPermission     # 12: Insufficient permissions.
    RANGE_ERROR            = _BS_C.aErrRange          # 13: Request is outside of valid range.
    SIZE_ERROR             = _BS_C.aErrSize           # 14: Size is incorrect for resource.
    OVERRUN_ERROR          = _BS_C.aErrOverrun        # 15: Buffer was overrun or will be.
    PARSE_ERROR            = _BS_C.aErrParse          # 16: Unable to parse command.
    CONFIGURATION_ERROR    = _BS_C.aErrConfiguration  # 17: Configuration is invalid.
    TIMEOUT                = _BS_C.aErrTimeout        # 18: Timeout occurred.
    INITIALIZATION_ERROR   = _BS_C.aErrInitialization # 19: Could not initialize resource.
    VERSION_ERROR          = _BS_C.aErrVersion        # 20: Version mismatch
    UNIMPLEMENTED_ERROR    = _BS_C.aErrUnimplemented  # 21: Functionality unavailable or unimplemented.
    DUPLICATE              = _BS_C.aErrDuplicate      # 22: Duplicate request received.
    CANCELED               = _BS_C.aErrCancel         # 23: Request was canceled
    PACKET_ERROR           = _BS_C.aErrPacket         # 24: packet was invalid or had invalid contents.
    CONNECTION_ERROR       = _BS_C.aErrConnection     # 25: connection is no longer valid, or was closed.
    INDEX_RANGE_ERROR      = _BS_C.aErrIndexRange     # 26: Requested entity does not exist.
    SHORT_COMMAND_ERROR    = _BS_C.aErrShortCommand   # 27: Command to short, not enough data to parse.
    INVALID_ENTITY_ERROR   = _BS_C.aErrInvalidEntity  # 28: Entity is not available, or does not exist.
    INVALID_OPTION_ERROR   = _BS_C.aErrInvalidOption  # 29: Option for given entity is invalid.
    RESOURCE_ERROR         = _BS_C.aErrResource       # 30: Error allocating or acquiring a resource.
    MEDIA_ERROR            = _BS_C.aErrMedia          # 31: Media not found or not available.
    ASYNC_RETURN_ERROR     = _BS_C.aErrAsyncReturn    # 32: Asynchronous return.
    STREAM_STALE_ERROR     = _BS_C.aErrStreamStale    # 33: Stream value is stale.
    UNKNOWN_ERROR          = _BS_C.aErrUnknown        # 34: Unknown error encountered.

    # another set of error names that's more inline with C library names
    aErrNone               = _BS_C.aErrNone
    aErrMemory             = _BS_C.aErrMemory
    aErrParam              = _BS_C.aErrParam
    aErrNotFound           = _BS_C.aErrNotFound
    aErrFileNameLength     = _BS_C.aErrFileNameLength
    aErrBusy               = _BS_C.aErrBusy
    aErrIO                 = _BS_C.aErrIO
    aErrMode               = _BS_C.aErrMode
    aErrWrite              = _BS_C.aErrWrite
    aErrRead               = _BS_C.aErrRead
    aErrEOF                = _BS_C.aErrEOF
    aErrNotReady           = _BS_C.aErrNotReady
    aErrPermission         = _BS_C.aErrPermission
    aErrRange              = _BS_C.aErrRange
    aErrSize               = _BS_C.aErrSize
    aErrOverrun            = _BS_C.aErrOverrun
    aErrParse              = _BS_C.aErrParse
    aErrConfiguration      = _BS_C.aErrConfiguration
    aErrTimeout            = _BS_C.aErrTimeout
    aErrInitialization     = _BS_C.aErrInitialization
    aErrVersion            = _BS_C.aErrVersion
    aErrUnimplemented      = _BS_C.aErrUnimplemented
    aErrDuplicate          = _BS_C.aErrDuplicate
    aErrCancel             = _BS_C.aErrCancel
    aErrPacket             = _BS_C.aErrPacket
    aErrConnection         = _BS_C.aErrConnection
    aErrIndexRange         = _BS_C.aErrIndexRange
    aErrShortCommand       = _BS_C.aErrShortCommand
    aErrInvalidEntity      = _BS_C.aErrInvalidEntity
    aErrInvalidOption      = _BS_C.aErrInvalidOption
    aErrResource           = _BS_C.aErrResource
    aErrMedia              = _BS_C.aErrMedia
    aErrAsyncReturn        = _BS_C.aErrAsyncReturn
    aErrStreamStale        = _BS_C.aErrStreamStale
    aErrUnknown            = _BS_C.aErrUnknown

    def __init__(self, error, *args, **kwargs):
        """ Initialize a Result object

        :param error: The error value.
        :type error: unsigned byte

        :param value: the result value.
        """
        self._error = error
        if len(args) == 0:
            self._values = {'value': None}
        elif len(args) == 1:
            self._values = {'value': args[0]}
        else:
            raise ValueError('Only one non-named argument is allowed')
        
        if len(kwargs.keys()) > 0:
            if len(args) == 0:
                self._values = kwargs
            else:
                raise ValueError('Named arguments and unnamed arguments may not be combined')

    def __eq__(self, other):
        """ 
        Compare two Result objects for equality.

        :param other: The other Result object to compare to.
        :type other: Result

        :return: True if the two Result objects are equal, False otherwise.
        :rtype: bool
        """
        if not isinstance(other, Result):
            raise TypeError("Cannot compare Result to {}".format(type(other).__name__))
        return self.error == other.error and self.value == other.value

    @property
    def error(self):
        """ Return the error attribute"""
        return self._error

    @property
    def value(self):
        """ Return the value attribute(s)"""
        if len(self._values) > 1:
            return self._values
        return self._values['value']

    def keys(self):
        """ Return a list of the names of each value in the result"""
        return self._values.keys()

    def values(self):
        """ Return a list of the values of each value in the result"""
        return self._values.values()

    def items(self):
        """ Return the key, value mapping for each result value"""
        return self._values.items()
    
    def __getattr__(self, name):
        """ Return a representation of the PackedResult object"""
        if name in self._values:
            return self._values[name]
        else:
            raise AttributeError("'{}' object has no attribute '{}'".format(type(self).__name__, name))

    @staticmethod
    def getErrorText(error):
        """ 
        Get the string representation of an error code.

        :param error: The error to decode.
        :type error: int or Result object
        
        :return: The error code in human readable form.
        :rtype: string 
        """
        return Result.__getErrorText(Result.__getError(error))

    @staticmethod
    def getErrorDescription(error, buffer_length=256):
        """ 
        Get the description of an error code.

        :param error: The error to decode.
        :type error: int or Result object
        
        :return: The error code in human readable form.
        :rtype: string 
        """
        result = ffi.new("struct Result*")
        ffi_buffer = ffi.new("unsigned char[]", buffer_length)
        _BS_C.error_GetErrorDescription(result, Result.__getError(error), ffi_buffer, buffer_length)
        if result.error:
            raise MemoryError("error_GetErrorDescription: {}".format(pResult.error))

        return bytes([ffi_buffer[i] for i in range(result.value)])

    @staticmethod
    def __getErrorText(error):
        # Build list of class "constants"/error code strings using reflection.
        members = [attr for attr in dir(Result) if not callable(getattr(Result, attr)) and not attr.startswith("__") and attr.isupper()]
        for member in members:
            # 'error' is an int; 'member' is a string
            # Using eval we get the value (int) of 'member' 
            if error == eval(__class__.__name__ + "." + member):
                return member
        return ""

        # If we ever align python errors with C errors then we can use this. 
        # return ffi.string(_BS_C.error_GetErrorText(the_error), 100)
    
    @staticmethod
    def __getError(error):
        # Strips off the result object to acquire the raw error code. 
        the_error = Result.UNKNOWN_ERROR;
        if type(error) is Result:
            the_error = error.error
        elif type(error) is int:
            the_error = error
        return the_error

    def __iter__(self):
        yield self.error
        yield self.value
        return

    def __repr__(self):
        """ Return a representation of the Result object"""
        return "<id(%x) %s>" % (id(self), str(self))

    def __str__(self):
        """ Pretty print the Result object"""
        if len(self._values) > 1:
            return "<Result(%s): %s>" % (self.error, ', '.join(["{}={}".format(k, v) for k, v in self.items()]))
        return "<Result(%s): %s>" % (self.error, str(self.value))
