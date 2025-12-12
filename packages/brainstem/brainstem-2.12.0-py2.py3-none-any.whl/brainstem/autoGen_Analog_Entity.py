# This file was auto-generated. Do not modify.

from ._bs_c_cffi import ffi
from . import _BS_C #imported from __init__
from .Entity_Entity import *
from .result import Result
from .ffi_utils import data_to_bytearray, bytes_to_string, handle_sign, handle_sign_value, get_ffi_buffer

class Analog(Entity):
    
    ''' 
    Interface to analog entities on BrainStem modules.
    Analog entities may be configured as a input or output depending on hardware capabilities.
    Some modules are capable of providing actual voltage readings, while other simply return
    the raw analog-to-digital converter (ADC) output value.
    The resolution of the voltage or number of useful bits is also hardware dependent.
    
    ''' 

    CONFIGURATION_INPUT = 0
    CONFIGURATION_OUTPUT = 1
    HERTZ_MINIMUM = 7000
    HERTZ_MAXIMUM = 200000
    BULK_CAPTURE_IDLE = 0
    BULK_CAPTURE_PENDING = 1
    BULK_CAPTURE_FINISHED = 2
    BULK_CAPTURE_ERROR = 3

    def __init__(self, module, index):
        super(Analog, self).__init__(module, _BS_C.cmdANALOG, index)

    def getValue(self):

        '''
        Get the raw ADC output value in bits.
        
        Note
        ----
            Not all modules are provide 16 useful bits; this value's least significant bits are
            zero-padded to 16 bits.
            Refer to the module's datasheet to determine analog bit depth and reference voltage.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned short
                    16 bit analog reading with 0 corresponding to the negative analog voltage
                    reference and 0xFFFF corresponding to the positive analog voltage reference.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.analog_getValue(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 16, False)


    def getVoltage(self):

        '''
        Get the scaled micro volt value with reference to ground.
        
        Note
        ----
            Not all modules provide 32 bits of accuracy.
            Refer to the module's datasheet to determine the analog bit depth and reference
            voltage.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : int
                    32 bit signed integer (in microvolts) based on the board's ground and
                    reference voltages.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.analog_getVoltage(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, True)


    def getRange(self):

        '''
        Get the analog input range.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    8 bit value corresponding to a discrete range option
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.analog_getRange(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def getEnable(self):

        '''
        Get the analog output enable status.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : bool
                    0 if disabled 1 if enabled.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.analog_getEnable(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setValue(self, value):

        '''
        Set the value of an analog output (DAC) in bits.
        
        Parameters
        ----------
        value : unsigned short
            16 bit analog set point with 0 corresponding to the negative analog voltage reference
            and 0xFFFF corresponding to the positive analog voltage reference.
        
        Note
        ----
            Not all modules are provide 16 useful bits; the least significant bits are discarded.
            E.g. for a 10 bit DAC, 0xFFC0 to 0x0040 is the useful range.
            Refer to the module's datasheet to determine analog bit depth and reference voltage.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.analog_setValue(self._module._id_pointer, result, self._index, value)
        return result.error


    def setVoltage(self, microvolts):

        '''
        Set the voltage level of an analog output (DAC) in microvolts.
        
        Parameters
        ----------
        microvolts : int
            32 bit signed integer (in microvolts) based on the board's ground and reference
            voltages.
        
        Note
        ----
            Voltage range is dependent on the specific DAC channel range.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.analog_setVoltage(self._module._id_pointer, result, self._index, microvolts)
        return result.error


    def setRange(self, range):

        '''
        Set the analog input range.
        
        Parameters
        ----------
        range : unsigned char
            8 bit value corresponding to a discrete range option
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.analog_setRange(self._module._id_pointer, result, self._index, range)
        return result.error


    def setEnable(self, enable):

        '''
        Set the analog output enable state.
        
        Parameters
        ----------
        enable : bool
            set 1 to enable or 0 to disable.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.analog_setEnable(self._module._id_pointer, result, self._index, enable)
        return result.error


    def setConfiguration(self, configuration):

        '''
        Set the analog configuration.
        
        Parameters
        ----------
        configuration : unsigned char
            bitAnalogConfigurationOutput configures the analog entity as an output.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.analog_setConfiguration(self._module._id_pointer, result, self._index, configuration)
        return result.error


    def getConfiguration(self):

        '''
        Get the analog configuration.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Current configuration of the analog entity.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.analog_getConfiguration(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setBulkCaptureSampleRate(self, value):

        '''
        Set the sample rate for this analog when bulk capturing.
        
        Parameters
        ----------
        value : unsigned int
            sample rate in samples per second (Hertz).
            - Minimum rate: 7,000 Hz
            - Maximum rate: 200,000 Hz
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.analog_setBulkCaptureSampleRate(self._module._id_pointer, result, self._index, value)
        return result.error


    def getBulkCaptureSampleRate(self):

        '''
        Get the current sample rate setting for this analog when bulk capturing.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    upon success filled with current sample rate in samples per second (Hertz).
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.analog_getBulkCaptureSampleRate(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


    def setBulkCaptureNumberOfSamples(self, value):

        '''
        Set the number of samples to capture for this analog when bulk capturing.
        
        Parameters
        ----------
        value : unsigned int
            number of samples.
            - Minimum # of Samples: 0
            - Maximum # of Samples: (BRAINSTEM_RAM_SLOT_SIZE / 2) = (3FFF / 2) = 1FFF = 8191
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.analog_setBulkCaptureNumberOfSamples(self._module._id_pointer, result, self._index, value)
        return result.error


    def getBulkCaptureNumberOfSamples(self):

        '''
        Get the current number of samples setting for this analog when bulk capturing.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    number of samples.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.analog_getBulkCaptureNumberOfSamples(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


    def initiateBulkCapture(self):

        '''
        Initiate a BulkCapture on this analog.
        Captured measurements are stored in the module's RAM store (RAM_STORE) slot 0.
        Data is stored in a contiguous byte array with each sample stored in two consecutive
        bytes, LSB first.
        
        Note
        ----
            When the bulk capture is complete getBulkCaptureState() will return either
            bulkCaptureFinished or bulkCaptureError.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.analog_initiateBulkCapture(self._module._id_pointer, result, self._index)
        return result.error



    def getBulkCaptureState(self):

        '''
        Get the current bulk capture state for this analog.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    the state of bulk capture.
                    - Idle: bulkCaptureIdle = 0
                    - Pending: bulkCapturePending = 1
                    - Finished: bulkCaptureFinished = 2
                    - Error: bulkCaptureError = 3
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.analog_getBulkCaptureState(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


