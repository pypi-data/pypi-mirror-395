# This file was auto-generated. Do not modify.

from ._bs_c_cffi import ffi
from . import _BS_C #imported from __init__
from .Entity_Entity import *
from .result import Result
from .ffi_utils import data_to_bytearray, bytes_to_string, handle_sign, handle_sign_value, get_ffi_buffer

class System(Entity):
    
    ''' 
    The System class provides access to the core settings, configuration and system
    information of the BrainStem module.
    The class provides access to the model type, serial number and other static information as
    well as the ability to set boot reflexes, toggle the user LED, as well as affect module
    and router addresses etc.
    
    ''' 

    BOOT_SLOT_DISABLE = 255

    def __init__(self, module, index):
        super(System, self).__init__(module, _BS_C.cmdSYSTEM, index)

    def getModule(self):

        '''
        Get the current address the module uses on the BrainStem network.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    The address the module is using on the BrainStem network.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_getModule(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def getModuleBaseAddress(self):

        '''
        Get the base address of the module.
        Software offsets and hardware offsets are added to this base address to produce the
        effective module address.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    The address the module is using on the BrainStem network.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_getModuleBaseAddress(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setRouter(self, address):

        '''
        Set the router address the module uses to communicate with the host and heartbeat to in
        order to establish the BrainStem network.
        This setting must be saved and the board reset before the setting becomes active.
        Warning: changing the router address may cause the module to "drop off" the BrainStem
        network if the new router address is not in use by a BrainStem module.
        Please review the BrainStem network fundamentals before modifying the router address.
        
        Parameters
        ----------
        address : unsigned char
            The router address to be used.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_setRouter(self._module._id_pointer, result, self._index, address)
        return result.error


    def getRouter(self):

        '''
        Get the router address the module uses to communicate with the host and heartbeat to in
        order to establish the BrainStem network.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    The address.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_getRouter(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setHBInterval(self, interval):

        '''
        Set the delay between heartbeat packets which are sent from the module.
        For link modules, these these heartbeat are sent to the host.
        For non-link modules, these heartbeats are sent to the router address.
        Interval values are in 25.6 millisecond increments
        Valid values are 1-255; default is 10 (256 milliseconds).
        
        Parameters
        ----------
        interval : unsigned char
            The desired heartbeat delay.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_setHBInterval(self._module._id_pointer, result, self._index, interval)
        return result.error


    def getHBInterval(self):

        '''
        Get the delay between heartbeat packets which are sent from the module.
        For link modules, these these heartbeat are sent to the host.
        For non-link modules, these heartbeats are sent to the router address.
        Interval values are in 25.6 millisecond increments.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    The current heartbeat delay.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_getHBInterval(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setLED(self, led_on):

        '''
        Set the system LED state. Most modules have a blue system LED.
        Refer to the module datasheet for details on the system LED location and color.
        
        Parameters
        ----------
        led_on : bool
            true: turn the LED on, false: turn LED off.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_setLED(self._module._id_pointer, result, self._index, led_on)
        return result.error


    def getLED(self):

        '''
        Get the system LED state. Most modules have a blue system LED.
        Refer to the module datasheet for details on the system LED location and color.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : bool
                    true: LED on, false: LED off.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_getLED(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setLEDMaxBrightness(self, brightness):

        '''
        Sets the scaling factor for the brightness of all LEDs on the system.
        The brightness is set to the ratio of this value compared to 255 (maximum).
        The colors of each LED may be inconsistent at low brightness levels.
        Note that if the brightness is set to zero and the settings are saved, then the LEDs will
        no longer indicate whether the system is powered on.
        When troubleshooting, the user configuration may need to be manually reset in order to
        view the LEDs again.
        
        Parameters
        ----------
        brightness : unsigned char
            Brightness value relative to 255
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_setLEDMaxBrightness(self._module._id_pointer, result, self._index, brightness)
        return result.error


    def getLEDMaxBrightness(self):

        '''
        Gets the scaling factor for the brightness of all LEDs on the system.
        The brightness is set to the ratio of this value compared to 255 (maximum).
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Brightness value relative to 255
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_getLEDMaxBrightness(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setBootSlot(self, slot):

        '''
        Set a store slot to be mapped when the module boots.
        The boot slot will be mapped after the module boots from powers up, receives a reset
        signal on its reset input, or is issued a software reset command.
        Set the slot to 255 to disable mapping on boot.
        
        Parameters
        ----------
        slot : unsigned char
            The slot number in aSTORE_INTERNAL to be marked as a boot slot.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_setBootSlot(self._module._id_pointer, result, self._index, slot)
        return result.error


    def getBootSlot(self):

        '''
        Get the store slot which is mapped when the module boots.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    The slot number in aSTORE_INTERNAL that is mapped after the module
                    boots.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_getBootSlot(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def getVersion(self):

        '''
        Get the modules firmware version number.
        The version number is packed into the return value.
        Utility functions in the aVersion module can unpack the major, minor and patch numbers
        from the version number which looks like M.m.p.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    The build version date code.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_getVersion(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


    def getBuild(self):

        '''
        Get the modules firmware build number
        The build number is a unique hash assigned to a specific firmware.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    Variable to be filled with build.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_getBuild(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


    def getModel(self):

        '''
        Get the module's model enumeration.
        A subset of the possible model enumerations is defined in BrainStem.h under "BrainStem
        model codes".
        Other codes are be used by Acroname for proprietary module types.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    The module's model enumeration.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_getModel(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def getHardwareVersion(self):

        '''
        Get the module's hardware revision information.
        The content of the hardware version is specific to each Acroname product and used to
        indicate behavioral differences between product revisions.
        The codes are not well defined and may change at any time.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    The module's hardware version information.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_getHardwareVersion(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


    def getSerialNumber(self):

        '''
        Get the module's serial number.
        The serial number is a unique 32 bit integer which is usually communicated in hexadecimal
        format.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    The module's serial number.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_getSerialNumber(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


    def save(self):

        '''
        Save the system operating parameters to the persistent module flash memory.
        Operating parameters stored in the system flash will be loaded after the module reboots.
        Operating parameters include: heartbeat interval, module address, module router address.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_save(self._module._id_pointer, result, self._index)
        return result.error



    def reset(self):

        '''
        Reset the system.
        A return value of aErrTimeout indicates a successful reset, as the system resets
        immediately, which tears down the USB-link immediately, thus preventing an affirmative
        response.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_reset(self._module._id_pointer, result, self._index)
        return result.error



    def logEvents(self):

        '''
        Saves system log events to a slot defined by the module (usually ram slot 0).
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_logEvents(self._module._id_pointer, result, self._index)
        return result.error



    def getUptime(self):

        '''
        Get the module's accumulated uptime in minutes
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    The module's accumulated uptime in minutes.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_getUptime(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


    def getTemperature(self):

        '''
        Get the module's current temperature in micro-C
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : int
                    The module's system temperature in micro-C
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_getTemperature(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, True)


    def getMinimumTemperature(self):

        '''
        Get the module's minimum temperature ever recorded in micro-C (uC).
        This value will persists through a power cycle.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : int
                    The module's minimum system temperature in micro-C
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_getMinimumTemperature(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, True)


    def getMaximumTemperature(self):

        '''
        Get the module's maximum temperature ever recorded in micro-C (uC).
        This value will persists through a power cycle.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : int
                    The module's maximum system temperature in micro-C
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_getMaximumTemperature(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, True)


    def getInputVoltage(self):

        '''
        Get the module's input voltage.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    The module's input voltage reported in microvolts.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_getInputVoltage(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


    def getInputCurrent(self):

        '''
        Get the module's input current.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    The module's input current reported in microamps.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_getInputCurrent(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


    def getModuleHardwareOffset(self):

        '''
        Get the module hardware address offset. This is added to the base address to allow the
        module address to be configured in hardware.
        Not all modules support the hardware module address offset. Refer to the module datasheet.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    The module address offset.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_getModuleHardwareOffset(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setModuleSoftwareOffset(self, address):

        '''
        Set the software address offset.
        This software offset is added to the module base address, and potentially a module
        hardware address to produce the final module address.
        You must save the system settings and restart for this to take effect.
        Please review the BrainStem network fundamentals before modifying the module address.
        
        Parameters
        ----------
        address : unsigned char
            The address for the module. Value must be even from 0-254.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_setModuleSoftwareOffset(self._module._id_pointer, result, self._index, address)
        return result.error


    def getModuleSoftwareOffset(self):

        '''
        Get the software address offset.
        This software offset is added to the module base address, and potentially a module
        hardware address to produce the final module address.
        You must save the system settings and restart for this to take effect.
        Please review the BrainStem network fundamentals before modifying the module address.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    The address for the module. Value must be even from 0-254.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_getModuleSoftwareOffset(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def getRouterAddressSetting(self):

        '''
        Get the router address system setting.
        This setting may not be the same as the current router address if the router setting was
        set and saved but no reset has occurred.
        Please review the BrainStem network fundamentals before modifying the module address.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    The address for the module. Value must be even from 0-254.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_getRouterAddressSetting(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def routeToMe(self, enable):

        '''
        Enables/Disables the route to me function.
        This function allows for easy networking of BrainStem modules.
        Enabling (1) this function will send an I2C General Call to all devices on the network and
        request that they change their router address to the of the calling device.
        Disabling (0) will cause all devices on the BrainStem network to revert to their default
        address.
        
        Parameters
        ----------
        enable : bool
            Enable or disable of the route to me function 1 = enable.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_routeToMe(self._module._id_pointer, result, self._index, enable)
        return result.error


    def getPowerLimit(self):

        '''
        Reports the amount of power the system has access to and thus how much power can be
        budgeted to sinking devices.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    The available power in milli-Watts (mW, 1 t)
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_getPowerLimit(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


    def getPowerLimitMax(self):

        '''
        Gets the user defined maximum power limit for the system.
        Provides mechanism for defining an unregulated power supplies capability.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    Variable to be filled with the power limit in milli-Watts (mW)
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_getPowerLimitMax(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


    def setPowerLimitMax(self, power):

        '''
        Sets a user defined maximum power limit for the system.
        Provides mechanism for defining an unregulated power supplies capability.
        
        Parameters
        ----------
        power : unsigned int
            Limit in milli-Watts (mW) to be set.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_setPowerLimitMax(self._module._id_pointer, result, self._index, power)
        return result.error


    def getPowerLimitState(self):

        '''
        Gets a bit mapped representation of the factors contributing to the power limit.
        Active limit can be found through PowerDeliverClass::getPowerLimit().
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    Variable to be filled with the state.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_getPowerLimitState(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


    def getUnregulatedVoltage(self):

        '''
        Gets the voltage present at the unregulated port.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : int
                    Variable to be filled with the voltage in micro-Volts (uV).
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_getUnregulatedVoltage(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, True)


    def getUnregulatedCurrent(self):

        '''
        Gets the current passing through the unregulated port.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : int
                    Variable to be filled with the current in micro-Amps (uA).
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_getUnregulatedCurrent(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, True)


    def getInputPowerSource(self):

        '''
        Provides the source of the current power source in use.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Variable to be filled with enumerated representation of the source.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_getInputPowerSource(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def getInputPowerBehavior(self):

        '''
        Gets the systems input power behavior.
        This behavior refers to where the device sources its power from and what happens if that
        power source goes away.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Variable to be filled with an enumerated value representing behavior.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_getInputPowerBehavior(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setInputPowerBehavior(self, behavior):

        '''
        Sets the systems input power behavior.
        This behavior refers to where the device sources its power from and what happens if that
        power source goes away.
        
        Parameters
        ----------
        behavior : unsigned char
            An enumerated representation of behavior to be set.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_setInputPowerBehavior(self._module._id_pointer, result, self._index, behavior)
        return result.error


    def getInputPowerBehaviorConfig(self, buffer_length = 16384):

        '''
        Gets the input power behavior configuration
        Certain behaviors use a list of ports to determine priority when budgeting power.
        
        Parameters
        ----------
        buffer_length : unsigned int
            Length of the buffer to be filed
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : list(unsigned int)
                    pointer to the start of a c style buffer to be filled
        
        '''

        ffi_buffer = get_ffi_buffer(32, False, buffer_length)

        result = ffi.new("struct Result*")
        _BS_C.system_getInputPowerBehaviorConfig(self._module._id_pointer, result, self._index, ffi_buffer, buffer_length)
        return_list = [handle_sign_value(ffi_buffer[i], 32, False) for i in range(result.value)]
        return Result(result.error, return_list)


    def setInputPowerBehaviorConfig(self, buffer):

        '''
        Sets the input power behavior configuration
        Certain behaviors use a list of ports to determine priority when budgeting power.
        
        Parameters
        ----------
        buffer : list(unsigned int)
            Pointer to the start of a c style buffer to be transferred.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        buffer_length = len(buffer)
        ffi_buffer = get_ffi_buffer(32, False, buffer_length)
        for x in range(buffer_length):
            ffi_buffer[x] = buffer[x]

        result = ffi.new("struct Result*")
        _BS_C.system_setInputPowerBehaviorConfig(self._module._id_pointer, result, self._index, ffi_buffer, buffer_length)
        return result.error


    def getName(self, buffer_length = 65536):

        '''
        Gets a user defined name of the device.
        Helpful for identifying ports/devices in a static environment.
        
        Parameters
        ----------
        buffer_length : unsigned int
            Length of the buffer to be filed
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : string
                    pointer to the start of a c style buffer to be filled
        
        '''

        ffi_buffer = get_ffi_buffer(8, False, buffer_length)

        result = ffi.new("struct Result*")
        _BS_C.system_getName(self._module._id_pointer, result, self._index, ffi_buffer, buffer_length)
        return_list = [handle_sign_value(ffi_buffer[i], 8, False) for i in range(result.value)]
        return Result(result.error, bytes(return_list).decode('utf-8'))


    def setName(self, buffer):

        '''
        Sets a user defined name for the device.
        Helpful for identification when multiple devices of the same type are present in a system.
        
        Parameters
        ----------
        buffer : string
            Pointer to the start of a c style buffer to be transferred.
        
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
        _BS_C.system_setName(self._module._id_pointer, result, self._index, ffi_buffer, buffer_length)
        return result.error



    def resetDeviceToFactoryDefaults(self):

        '''
        Resets the device to it factory default configuration.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_resetDeviceToFactoryDefaults(self._module._id_pointer, result, self._index)
        return result.error



    def getLinkInterface(self):

        '''
        Gets the link interface configuration.
        This refers to which interface is being used for control by the device.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Variable to be filled with an enumerated value representing interface.
                        - 0 = Auto= systemLinkAuto
                        - 1 = Control Port = systemLinkUSBControl
                        - 2 = Hub Upstream Port = systemLinkUSBHub
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_getLinkInterface(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setLinkInterface(self, link_interface):

        '''
        Sets the link interface configuration.
        This refers to which interface is being used for control by the device.
        
        Parameters
        ----------
        link_interface : unsigned char
            An enumerated representation of interface to be set.
                - 0 = Auto= systemLinkAuto
                - 1 = Control Port = systemLinkUSBControl
                - 2 = Hub Upstream Port = systemLinkUSBHub
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_setLinkInterface(self._module._id_pointer, result, self._index, link_interface)
        return result.error


    def getErrors(self):

        '''
        Gets any system level errors.
        Calling this function will clear the current errors. If the error persists it will be set
        again.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    Bit mapped field representing the devices errors
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_getErrors(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


    def getProtocolFeatures(self):

        '''
        Gets the firmware protocol features
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    Value representing the firmware protocol features
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.system_getProtocolFeatures(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


