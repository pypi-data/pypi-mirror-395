# Copyright (c) 2018 Acroname Inc. - All Rights Reserved
#
# This file is part of the BrainStem (tm) package which is released under MIT.
# See file LICENSE or go to https://acroname.com for full license details.

""" Provides version access utilities. """

from . import _BS_C, ffi
from .ffi_utils import bytes_to_string
from .result import Result


def get_version_string(packed_version=None, buffer_length=256):
    """ 
    Gets the version string from a packed version.

    :param packed_version: If version is provided, it is unpacked and presented as the version string. Most useful for printing the firmware version currently installed on a module.
    :type packed_version: unsigned int

    :param buffer_length: The amount of C memory to allocate
    :type buffer_length: unsigned short

    :return: The library version as a string
    :rtype: str
    """

    result = ffi.new("struct Result*")
    
    if not packed_version:
        ffi_buffer = ffi.new("unsigned char[]", buffer_length)
        _BS_C.version_GetString(result, ffi_buffer, buffer_length)
        pResult = bytes_to_string(Result(result.error, [ffi_buffer[i] for i in range(result.value)]))
        if pResult.error:
            raise MemoryError("version_GetString: ".format(pResult.error))
        return 'Brainstem library version: ' + pResult.value

    else:
        return 'Brainstem version: %d.%d.%d' % unpack_version(packed_version)


def unpack_version(packed_version):
    """ 
    Unpacks a packed version. 

    :param packed_version: The packed version number.
    :type packed_version: unsigned int

    :return: Returns the library version as a 3-tuple (major, minor, patch)
    :rtype: str 
    """
    result_major = ffi.new("struct Result*")
    result_minor = ffi.new("struct Result*")
    result_patch = ffi.new("struct Result*")

    _BS_C.version_ParseMajor(result_major, packed_version)
    _BS_C.version_ParseMinor(result_minor, packed_version)
    _BS_C.version_ParsePatch(result_patch, packed_version)

    #Shouldn't be able to hit this. These functions don't return errors. 
    if result_major.error or result_minor.error or result_patch.error:
        raise RuntimeError("Error getting version: major: %d, minor: %d, patch: %d" % (result_major.error, result_minor.error, result_patch.error))

    return result_major.value, result_minor.value, result_patch.value


def parseMajor(packed_version):
    """ 
    Parses the major revision level from the given build number.

    :param packed_version: The packed version number returned from version.pack() or system.getVersion()
    :type packed_version: const unsigned int

    :return: Result object containing the requested value when the results error is set to NO_ERROR(0)
    :rtype: Result
    """

    result = ffi.new("struct Result*")
    _BS_C.version_ParseMajor(result, packed_version)
    return Result(result.error, result.value)


def parseMinor(packed_version):
    """ 
    Parses the minor revision level from the given build number.

    :param packed_version: The packed version number returned from version.pack() or system.getVersion()
    :type packed_version: const unsigned int

    :return: Result object containing the requested value when the results error is set to NO_ERROR(0)
    :rtype: Result
    """

    result = ffi.new("struct Result*")
    _BS_C.version_ParseMinor(result, packed_version)
    return Result(result.error, result.value)


def parsePatch(packed_version):
    """ 
    Parses the revision patch level from the given build number.

    :param packed_version: The packed version number returned from version.pack() or system.getVersion()
    :type packed_version: const unsigned int

    :return: Result object containing the requested value when the results error is set to NO_ERROR(0)
    :rtype: Result
    """

    result = ffi.new("struct Result*")
    _BS_C.version_ParsePatch(result, packed_version)
    return Result(result.error, result.value)


def isLegacyFormat(packed_version):
    """ 
    Check if the given build version is of the legacy packing format

    :param packed_version: The packed version number returned from version.pack() or system.getVersion()
    :type packed_version: const unsigned int

    :return: Result object containing the requested value when the results error is set to NO_ERROR(0)
    :rtype: Result
    """

    result = ffi.new("struct Result*")
    _BS_C.version_IsLegacyFormat(result, packed_version)
    return Result(result.error, result.value)


def getMajor():
    """ 
    Gets the major revision number for the software package.

    :return: Result object containing the requested value when the results error is set to NO_ERROR(0)
    :rtype: Result
    """

    result = ffi.new("struct Result*")
    _BS_C.version_GetMajor(result)
    return Result(result.error, result.value)


def getMinor():
    """ 
    Gets the minor revision number for the software package.

    :return: Result object containing the requested value when the results error is set to NO_ERROR(0)
    :rtype: Result
    """

    result = ffi.new("struct Result*")
    _BS_C.version_GetMinor(result)
    return Result(result.error, result.value)


def getPatch():
    """ 
    Gets the patch revision number for the software package.
    
    :return: Result object containing the requested value when the results error is set to NO_ERROR(0)
    :rtype: Result
    """
    result = ffi.new("struct Result*")
    _BS_C.version_GetPatch(result)
    return Result(result.error, result.value)


def isAtLeast(major, minor, patch):
    """ 
    Check that the current software version is at least major.minor.patch

    :param major: The major revision level.
    :type major: const unsigned byte

    :param minor: The minor revision level.
    :type minor: const unsigned byte

    :param patch: The patch revision level.
    :type patch: const unsigned byte

    :return: Result object containing the requested value when the results error is set to NO_ERROR(0)
    :rtype: Result
    """

    result = ffi.new("struct Result*")
    _BS_C.version_IsAtLeast(result, major, minor, patch)
    return Result(result.error, result.value)


def isAtleastCompare(major_lhs, minor_lhs, patch_lhs, major_rhs, minor_rhs, patch_rhs):
    """
    Check that the supplied left hand side (lhs) version is at least (>=) the right hand side (rhs).

    :param major_lhs: The lhs major revision level.
    :type major_lhs: const unsigned byte

    :param minor_lhs: The lhs minor revision level.
    :type minor_lhs: const unsigned byte

    :param patch_lhs: The lhs patch revision level.
    :type patch_lhs: const unsigned byte

    :param major_rhs: The rhs major revision level.
    :type major_rhs: const unsigned byte

    :param minor_rhs: The rhs minor revision level.
    :type minor_rhs: const unsigned byte

    :param patch_rhs: The rhs patch revision level.
    :type patch_rhs: const unsigned byte

    :return: Result object containing the requested value when the results error is set to NO_ERROR(0)
    :rtype: Result
    """

    result = ffi.new("struct Result*")
    _BS_C.version_IsAtLeastCompare(result, major_lhs, minor_lhs, patch_lhs, major_rhs, minor_rhs, patch_rhs)
    return Result(result.error, result.value)


def pack(major, minor, patch):
    """
    Packs the given version into a single integer

    :param major: The major revision level.
    :type major: const unsigned byte

    :param minor: The minor revision level.
    :type minor: const unsigned byte

    :param patch: The patch revision level.
    :type patch: const unsigned byte

    :return: Result object containing the requested value when the results error is set to NO_ERROR(0)
    :rtype: Result
    """
    
    result = ffi.new("struct Result*")
    _BS_C.version_Pack(result, major, minor, patch)
    return Result(result.error, result.value)

