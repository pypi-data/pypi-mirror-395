# This file was auto-generated. Do not modify.

from ._bs_c_cffi import ffi
from . import _BS_C #imported from __init__
from .Entity_Entity import *
from .result import Result
from .ffi_utils import data_to_bytearray, bytes_to_string, handle_sign, handle_sign_value, get_ffi_buffer

class PoE(Entity):
    
    ''' 
    This entity is only available on certain modules, and provides a Power over Ethernet
    control ability.
    
    ''' 


    def __init__(self, module, index):
        super(PoE, self).__init__(module, _BS_C.cmdPOE, index)

    def getPairEnabled(self, pair):

        '''
        Gets the current enable value of the indicated POE pair.
        
        Parameters
        ----------
        pair : unsigned char
            Selects PoE pair to access
                - 0 = Pair 1/2
                - 1 = Pair 3/4
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : bool
                    1 = Enabled; 0 = Disabled;
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.poe_getPairEnabled(self._module._id_pointer, result, self._index, pair)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setPairEnabled(self, pair, enable):

        '''
        Enables or disables the indicated POE pair.
        
        Parameters
        ----------
        pair : unsigned char
            Selects PoE pair to access
                - 0 = Pair 1/2
                - 1 = Pair 3/4
        enable : bool
            1 = Enable port; 0 = Disable port.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.poe_setPairEnabled(self._module._id_pointer, result, self._index, pair, enable)
        return result.error


    def getPowerMode(self):

        '''
        Gets the power mode of the device
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    The power mode (PD, PSE, Auto, Off).
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.poe_getPowerMode(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setPowerMode(self, value):

        '''
        Sets the power mode of the device
        
        Parameters
        ----------
        value : unsigned char
            The power mode (PD, PSE, Auto, Off).
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.poe_setPowerMode(self._module._id_pointer, result, self._index, value)
        return result.error


    def getPowerState(self):

        '''
        Gets the power state of the device
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    The power state (PD, PSE, Off).
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.poe_getPowerState(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def getPairSourcingClass(self, pair):

        '''
        Gets the sourcing class for a given pair.
        
        Parameters
        ----------
        pair : unsigned char
            Selects PoE pair to access
                - 0 = Pair 1/2
                - 1 = Pair 3/4
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    The POE class being offered by the device (PSE).
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.poe_getPairSourcingClass(self._module._id_pointer, result, self._index, pair)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setPairSourcingClass(self, pair, value):

        '''
        Sets the sourcing class for a given pair.
        
        Parameters
        ----------
        pair : unsigned char
            Selects PoE pair to access
                - 0 = Pair 1/2
                - 1 = Pair 3/4
        value : unsigned char
            The POE class being offered by the device (PSE).
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.poe_setPairSourcingClass(self._module._id_pointer, result, self._index, pair, value)
        return result.error


    def getPairRequestedClass(self, pair):

        '''
        Gets the requested class for a given pair.
        
        Parameters
        ----------
        pair : unsigned char
            Selects PoE pair to access
                - 0 = Pair 1/2
                - 1 = Pair 3/4
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    The requested POE class by the device (PD).
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.poe_getPairRequestedClass(self._module._id_pointer, result, self._index, pair)
        return handle_sign(Result(result.error, result.value), 8, False)


    def getPairDiscoveredClass(self, pair):

        '''
        Gets the discovered class for a given pair.
        
        Parameters
        ----------
        pair : unsigned char
            Selects PoE pair to access
                - 0 = Pair 1/2
                - 1 = Pair 3/4
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    The negotiated POE class by the device (PSE/PD).
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.poe_getPairDiscoveredClass(self._module._id_pointer, result, self._index, pair)
        return handle_sign(Result(result.error, result.value), 8, False)


    def getPairDetectionStatus(self, pair):

        '''
        Gets detected status of the POE connection for a given pair.
        
        Parameters
        ----------
        pair : unsigned char
            Selects PoE pair to access
                - 0 = Pair 1/2
                - 1 = Pair 3/4
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    The current detected status of the pairs.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.poe_getPairDetectionStatus(self._module._id_pointer, result, self._index, pair)
        return handle_sign(Result(result.error, result.value), 8, False)


    def getPairVoltage(self, pair):

        '''
        Gets the Voltage for a given pair.
        
        Parameters
        ----------
        pair : unsigned char
            Selects PoE pair to access
                - 0 = Pair 1/2
                - 1 = Pair 3/4
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : int
                    The voltage in microvolts (1 == 1e-6V).
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.poe_getPairVoltage(self._module._id_pointer, result, self._index, pair)
        return handle_sign(Result(result.error, result.value), 32, True)


    def getPairCurrent(self, pair):

        '''
        Gets the Current for a given pair.
        
        Parameters
        ----------
        pair : unsigned char
            Selects PoE pair to access
                - 0 = Pair 1/2
                - 1 = Pair 3/4
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : int
                    The current in microamps (1 == 1e-6V).
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.poe_getPairCurrent(self._module._id_pointer, result, self._index, pair)
        return handle_sign(Result(result.error, result.value), 32, True)


    def getPairResistance(self, pair):

        '''
        Gets the Resistance for a given pair.
        
        Parameters
        ----------
        pair : unsigned char
            Selects PoE pair to access
                - 0 = Pair 1/2
                - 1 = Pair 3/4
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : int
                    The resistance in milliohms (1 == 1e-3Z).
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.poe_getPairResistance(self._module._id_pointer, result, self._index, pair)
        return handle_sign(Result(result.error, result.value), 32, True)


    def getPairCapacitance(self, pair):

        '''
        Gets the Capacitance for a given pair
        
        Parameters
        ----------
        pair : unsigned char
            Selects PoE pair to access
                - 0 = Pair 1/2
                - 1 = Pair 3/4
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : int
                    The capacitance in nanofarads (1 == 1e-9F).
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.poe_getPairCapacitance(self._module._id_pointer, result, self._index, pair)
        return handle_sign(Result(result.error, result.value), 32, True)


    def getPairPower(self, pair):

        '''
        Get the instantaneous power consumption for a given pair
        The equivalent of Voltage x Current
        
        Parameters
        ----------
        pair : unsigned char
            Selects PoE pair to access
                - 0 = Pair 1/2
                - 1 = Pair 3/4
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : int
                    Variable to be filled with the pairs power in milli-watts (mW).
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.poe_getPairPower(self._module._id_pointer, result, self._index, pair)
        return handle_sign(Result(result.error, result.value), 32, True)


    def getTotalPower(self):

        '''
        Gets the total instantaneous power consumption
        The equivalent of Pair1(Voltage x Current) + Pair2(Voltage x Current)
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : int
                    Variable to be filled with the total POE power in milli-watts (mW).
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.poe_getTotalPower(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, True)


    def getPairAccumulatedPower(self, pair):

        '''
        Gets the accumulated power for a given pair.
        
        Parameters
        ----------
        pair : unsigned char
            Selects PoE pair to access
                - 0 = Pair 1/2
                - 1 = Pair 3/4
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : int
                    Variable to be filled with the total accumulated POE power in milli-watts
                    (mW).
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.poe_getPairAccumulatedPower(self._module._id_pointer, result, self._index, pair)
        return handle_sign(Result(result.error, result.value), 32, True)


    def setPairAccumulatedPower(self, pair, power):

        '''
        Sets the accumulated power for a given pair.
        
        Parameters
        ----------
        pair : unsigned char
            Selects PoE pair to access
                - 0 = Pair 1/2
                - 1 = Pair 3/4
        power : int
            The power accumulator value to be set in milli-watts (mW).
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.poe_setPairAccumulatedPower(self._module._id_pointer, result, self._index, pair, power)
        return result.error


    def getTotalAccumulatedPower(self):

        '''
        Gets the total Accumulated Power
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : int
                    Variable to be filled with the total accumulated POE power in milli-watts
                    (mW).
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.poe_getTotalAccumulatedPower(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, True)


    def setTotalAccumulatedPower(self, power):

        '''
        Sets the total accumulated power
        
        Parameters
        ----------
        power : int
            The power accumulator value to be set in milli-watts (mW).
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.poe_setTotalAccumulatedPower(self._module._id_pointer, result, self._index, power)
        return result.error


