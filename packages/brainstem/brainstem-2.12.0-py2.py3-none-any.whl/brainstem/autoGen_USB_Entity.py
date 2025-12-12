# This file was auto-generated. Do not modify.

from ._bs_c_cffi import ffi
from . import _BS_C #imported from __init__
from .Entity_Entity import *
from .result import Result
from .ffi_utils import data_to_bytearray, bytes_to_string, handle_sign, handle_sign_value, get_ffi_buffer

class USB(Entity):
    
    ''' 
    The USB class provides methods to interact with a USB hub and USB switches.
    Different USB hub products have varying support; check the datasheet to understand the
    capabilities of each product.
    
    ''' 

    UPSTREAM_MODE_AUTO = 2
    UPSTREAM_MODE_PORT_0 = 0
    UPSTREAM_MODE_PORT_1 = 1
    UPSTREAM_MODE_NONE = 255
    DEFAULT_UPSTREAM_MODE = UPSTREAM_MODE_AUTO
    UPSTREAM_STATE_PORT_0 = 0
    UPSTREAM_STATE_PORT_1 = 1
    BOOST_0_PERCENT = 0
    BOOST_4_PERCENT = 1
    BOOST_8_PERCENT = 2
    BOOST_12_PERCENT = 3
    PORT_MODE_SDP = 0
    PORT_MODE_CDP = 1
    PORT_MODE_CHARGING = 2
    PORT_MODE_PASSIVE = 3
    PORT_MODE_USB2_A_ENABLE = 4
    PORT_MODE_USB2_B_ENABLE = 5
    PORT_MODE_VBUS_ENABLE = 6
    PORT_MODE_SUPER_SPEED_1_ENABLE = 7
    PORT_MODE_SUPER_SPEED_2_ENABLE = 8
    PORT_MODE_USB2_BOOST_ENABLE = 9
    PORT_MODE_USB3_BOOST_ENABLE = 10
    PORT_MODE_AUTO_CONNECTION_ENABLE = 11
    PORT_MODE_CC1_ENABLE = 12
    PORT_MODE_CC2_ENABLE = 13
    PORT_MODE_SBU_ENABLE = 14
    PORT_MODE_CC_FLIP_ENABLE = 15
    PORT_MODE_SS_FLIP_ENABLE = 16
    PORT_MODE_SBU_FLIP_ENABLE = 17
    PORT_MODE_USB2_FLIP_ENABLE = 18
    PORT_MODE_CC1_INJECT_ENABLE = 19
    PORT_MODE_CC2_INJECT_ENABLE = 20
    PORT_SPEED_NA = 0
    PORT_SPEED_HISPEED = 1
    PORT_SPEED_SUPERSPEED = 2

    def __init__(self, module, index):
        super(USB, self).__init__(module, _BS_C.cmdUSB, index)

    def setPortEnable(self, channel):

        '''
        Enable both power and data lines for a port.
        
        Parameters
        ----------
        channel : unsigned char
            The USB sub channel.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_setPortEnable(self._module._id_pointer, result, self._index, channel)
        return result.error


    def setPortDisable(self, channel):

        '''
        Disable both power and data lines for a port.
        
        Parameters
        ----------
        channel : unsigned char
            The USB sub channel.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_setPortDisable(self._module._id_pointer, result, self._index, channel)
        return result.error


    def setDataEnable(self, channel):

        '''
        Enable the only the data lines for a port without changing the state of the power line.
        
        Parameters
        ----------
        channel : unsigned char
            The USB sub channel.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_setDataEnable(self._module._id_pointer, result, self._index, channel)
        return result.error


    def setDataDisable(self, channel):

        '''
        Disable only the data lines for a port without changing the state of the power line.
        
        Parameters
        ----------
        channel : unsigned char
            The USB sub channel.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_setDataDisable(self._module._id_pointer, result, self._index, channel)
        return result.error


    def setHiSpeedDataEnable(self, channel):

        '''
        Enable the only the data lines for a port without changing the state of the power line,
        Hi-Speed (2.0) only.
        
        Parameters
        ----------
        channel : unsigned char
            The USB sub channel.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_setHiSpeedDataEnable(self._module._id_pointer, result, self._index, channel)
        return result.error


    def setHiSpeedDataDisable(self, channel):

        '''
        Disable only the data lines for a port without changing the state of the power line, Hi-
        Speed (2.0) only.
        
        Parameters
        ----------
        channel : unsigned char
            The USB sub channel.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_setHiSpeedDataDisable(self._module._id_pointer, result, self._index, channel)
        return result.error


    def setSuperSpeedDataEnable(self, channel):

        '''
        Enable the only the data lines for a port without changing the state of the power line,
        SuperSpeed (3.0) only.
        
        Parameters
        ----------
        channel : unsigned char
            The USB sub channel.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_setSuperSpeedDataEnable(self._module._id_pointer, result, self._index, channel)
        return result.error


    def setSuperSpeedDataDisable(self, channel):

        '''
        Disable only the data lines for a port without changing the state of the power line,
        SuperSpeed (3.0) only.
        
        Parameters
        ----------
        channel : unsigned char
            The USB sub channel.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_setSuperSpeedDataDisable(self._module._id_pointer, result, self._index, channel)
        return result.error


    def setPowerEnable(self, channel):

        '''
        Enable only the power line for a port without changing the state of the data lines.
        
        Parameters
        ----------
        channel : unsigned char
            The USB sub channel.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_setPowerEnable(self._module._id_pointer, result, self._index, channel)
        return result.error


    def setPowerDisable(self, channel):

        '''
        Disable only the power line for a port without changing the state of the data lines.
        
        Parameters
        ----------
        channel : unsigned char
            The USB sub channel.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_setPowerDisable(self._module._id_pointer, result, self._index, channel)
        return result.error


    def getPortCurrent(self, channel):

        '''
        Get the current through the power line for a port.
        
        Parameters
        ----------
        channel : unsigned char
            The USB sub channel.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : int
                    The USB channel current in micro-amps (1 == 1e-6A).
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_getPortCurrent(self._module._id_pointer, result, self._index, channel)
        return handle_sign(Result(result.error, result.value), 32, True)


    def getPortVoltage(self, channel):

        '''
        Get the voltage on the power line for a port.
        
        Parameters
        ----------
        channel : unsigned char
            The USB sub channel.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : int
                    The USB channel voltage in microvolts (1 == 1e-6V).
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_getPortVoltage(self._module._id_pointer, result, self._index, channel)
        return handle_sign(Result(result.error, result.value), 32, True)


    def getHubMode(self):

        '''
        Get a bit mapped representation of the hubs mode; see the product datasheet for mode
        mapping and meaning.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    The USB hub mode.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_getHubMode(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


    def setHubMode(self, mode):

        '''
        Set a bit mapped hub state; see the product datasheet for state mapping and meaning.
        
        Parameters
        ----------
        mode : unsigned int
            The USB hub mode.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_setHubMode(self._module._id_pointer, result, self._index, mode)
        return result.error


    def clearPortErrorStatus(self, channel):

        '''
        Clear the error status for the given port.
        
        Parameters
        ----------
        channel : unsigned char
            The port to clear error status for.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_clearPortErrorStatus(self._module._id_pointer, result, self._index, channel)
        return result.error


    def getUpstreamMode(self):

        '''
        Get the upstream switch mode for the USB upstream ports. Returns auto, port 0 or port 1.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    The Upstream port mode.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_getUpstreamMode(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setUpstreamMode(self, mode):

        '''
        Set the upstream switch mode for the USB upstream ports. Values are usbUpstreamModeAuto,
        usbUpstreamModePort0, usbUpstreamModePort1, and usbUpstreamModeNone.
        
        Parameters
        ----------
        mode : unsigned char
            The Upstream port mode.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_setUpstreamMode(self._module._id_pointer, result, self._index, mode)
        return result.error


    def getUpstreamState(self):

        '''
        Get the upstream switch state for the USB upstream ports.
        Returns 2 if no ports plugged in, 0 if the mode is set correctly and a cable is plugged
        into port 0, and 1 if the mode is set correctly and a cable is plugged into port 1.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    The Upstream port state.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_getUpstreamState(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setEnumerationDelay(self, ms_delay):

        '''
        Set the inter-port enumeration delay in milliseconds.
        
        Parameters
        ----------
        ms_delay : unsigned int
            Millisecond delay in 100mS increments (100, 200, 300 etc.)
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_setEnumerationDelay(self._module._id_pointer, result, self._index, ms_delay)
        return result.error


    def getEnumerationDelay(self):

        '''
        Get the inter-port enumeration delay in milliseconds.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    Millisecond delay in 100mS increments (100, 200, 300 etc.)
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_getEnumerationDelay(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


    def setPortCurrentLimit(self, channel, microamps):

        '''
        Set the current limit for the port.
        If the set limit is not achievable, devices will round down to the nearest available
        current limit setting.
        This setting can be saved with a stem.system.save() call.
        
        Parameters
        ----------
        channel : unsigned char
            USB downstream channel to limit.
        microamps : unsigned int
            The current limit setting.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_setPortCurrentLimit(self._module._id_pointer, result, self._index, channel, microamps)
        return result.error


    def getPortCurrentLimit(self, channel):

        '''
        Get the current limit for the port.
        
        Parameters
        ----------
        channel : unsigned char
            USB downstream channel to limit.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    The current limit setting.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_getPortCurrentLimit(self._module._id_pointer, result, self._index, channel)
        return handle_sign(Result(result.error, result.value), 32, False)


    def setPortMode(self, channel, mode):

        '''
        Set the mode for the Port.
        The mode is a bitmapped representation of the capabilities of the usb port.
        These capabilities change for each of the BrainStem devices which implement the usb
        entity.
        See your device reference page for a complete list of capabilities.
        Some devices use a common bit mapping for port mode, as sub-definitions of usbPortMode.
        
        Parameters
        ----------
        channel : unsigned char
            USB downstream channel to set the mode on.
        mode : unsigned int
            The port mode setting as packed bit field.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_setPortMode(self._module._id_pointer, result, self._index, channel, mode)
        return result.error


    def getPortMode(self, channel):

        '''
        Get the current mode for the Port.
        The mode is a bitmapped representation of the capabilities of the usb port.
        These capabilities change for each of the BrainStem devices which implement the usb
        entity.
        See your device reference page for a complete list of capabilities.
        Some devices use a common bit mapping for port mode, as sub-definitions of usbPortMode.
        
        Parameters
        ----------
        channel : unsigned char
            USB downstream channel.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    The port mode setting.
                    Mode will be filled with the current setting.
                    Mode bits that are not used will be marked as don't care.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_getPortMode(self._module._id_pointer, result, self._index, channel)
        return handle_sign(Result(result.error, result.value), 32, False)


    def getPortState(self, channel):

        '''
        Get the current State for the Port.
        
        Parameters
        ----------
        channel : unsigned char
            USB downstream channel.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    The port mode setting.
                    Mode will be filled with the current setting.
                    Mode bits that are not used will be marked as don't care.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_getPortState(self._module._id_pointer, result, self._index, channel)
        return handle_sign(Result(result.error, result.value), 32, False)


    def getPortError(self, channel):

        '''
        Get the current error for the Port.
        
        Parameters
        ----------
        channel : unsigned char
            USB downstream channel.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    The port mode setting.
                    Mode will be filled with the current setting.
                    Mode bits that are not used will be marked as don't care.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_getPortError(self._module._id_pointer, result, self._index, channel)
        return handle_sign(Result(result.error, result.value), 32, False)


    def setUpstreamBoostMode(self, setting):

        '''
        Set the upstream boost mode.
        Boost mode increases the drive strength of the USB data signals (power signals are not
        changed).
        Boosting the data signal strength may help to overcome connectivity issues when using long
        cables or connecting through "pogo" pins.
        Possible modes are 0 - no boost, 1 - 4% boost, 2 - 8% boost, 3 - 12% boost.
        This setting is not applied until a stem.system.save() call and power cycle of the hub.
        Setting is then persistent until changed or the hub is reset.
        After reset, default value of 0% boost is restored.
        
        Parameters
        ----------
        setting : unsigned char
            Upstream boost setting 0, 1, 2, or 3.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_setUpstreamBoostMode(self._module._id_pointer, result, self._index, setting)
        return result.error


    def setDownstreamBoostMode(self, setting):

        '''
        Set the downstream boost mode.
        Boost mode increases the drive strength of the USB data signals (power signals are not
        changed).
        Boosting the data signal strength may help to overcome connectivity issues when using long
        cables or connecting through "pogo" pins.
        Possible modes are 0 - no boost, 1 - 4% boost, 2 - 8% boost, 3 - 12% boost.
        This setting is not applied until a stem.system.save() call and power cycle of the hub.
        Setting is then persistent until changed or the hub is reset.
        After reset, default value of 0% boost is restored.
        
        Parameters
        ----------
        setting : unsigned char
            Downstream boost setting 0, 1, 2, or 3.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_setDownstreamBoostMode(self._module._id_pointer, result, self._index, setting)
        return result.error


    def getUpstreamBoostMode(self):

        '''
        Get the upstream boost mode.
        Possible modes are 0 - no boost, 1 - 4% boost, 2 - 8% boost, 3 - 12% boost.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    The current Upstream boost setting 0, 1, 2, or 3.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_getUpstreamBoostMode(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def getDownstreamBoostMode(self):

        '''
        Get the downstream boost mode.
        Possible modes are 0 - no boost, 1 - 4% boost, 2 - 8% boost, 3 - 12% boost.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    The current Downstream boost setting 0, 1, 2, or 3.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_getDownstreamBoostMode(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def getDownstreamDataSpeed(self, channel):

        '''
        Get the current data transfer speed for the downstream port.
        The data speed can be Hi-Speed (2.0) or SuperSpeed (3.0) depending on what the downstream
        device attached is using
        
        Parameters
        ----------
        channel : unsigned char
            USB downstream channel to check.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Filled with the current port data speed
                        - N/A: usbDownstreamDataSpeed_na = 0
                        - Hi Speed: usbDownstreamDataSpeed_hs = 1
                        - SuperSpeed: usbDownstreamDataSpeed_ss = 2
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_getDownstreamDataSpeed(self._module._id_pointer, result, self._index, channel)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setConnectMode(self, channel, mode):

        '''
        Sets the connect mode of the switch.
        
        Parameters
        ----------
        channel : unsigned char
            The USB sub channel.
        mode : unsigned char
            The connect mode
                - usbManualConnect = 0
                - usbAutoConnect = 1
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_setConnectMode(self._module._id_pointer, result, self._index, channel, mode)
        return result.error


    def getConnectMode(self, channel):

        '''
        Gets the connect mode of the switch.
        
        Parameters
        ----------
        channel : unsigned char
            The USB sub channel.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    The current connect mode
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_getConnectMode(self._module._id_pointer, result, self._index, channel)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setCC1Enable(self, channel, enable):

        '''
        Set Enable/Disable on the CC1 line.
        
        Parameters
        ----------
        channel : unsigned char
            USB channel.
        enable : bool
            State to be set
                - Disabled: 0
                - Enabled: 1
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_setCC1Enable(self._module._id_pointer, result, self._index, channel, enable)
        return result.error


    def getCC1Enable(self, channel):

        '''
        Get Enable/Disable on the CC1 line.
        
        Parameters
        ----------
        channel : unsigned char
            USB channel.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : bool
                    State to be filled
                        - Disabled: 0
                        - Enabled: 1
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_getCC1Enable(self._module._id_pointer, result, self._index, channel)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setCC2Enable(self, channel, enable):

        '''
        Set Enable/Disable on the CC2 line.
        
        Parameters
        ----------
        channel : unsigned char
            USB channel.
        enable : bool
            State to be filled
                - Disabled: 0
                - Enabled: 1
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_setCC2Enable(self._module._id_pointer, result, self._index, channel, enable)
        return result.error


    def getCC2Enable(self, channel):

        '''
        Get Enable/Disable on the CC2 line.
        
        Parameters
        ----------
        channel : unsigned char
            USB channel.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : bool
                    State to be filled
                        - Disabled: 0
                        - Enabled: 1
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_getCC2Enable(self._module._id_pointer, result, self._index, channel)
        return handle_sign(Result(result.error, result.value), 8, False)


    def getCC1Current(self, channel):

        '''
        Get the current through the CC1 for a port.
        
        Parameters
        ----------
        channel : unsigned char
            The USB sub channel.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : int
                    The USB channel current in micro-amps (1 == 1e-6A).
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_getCC1Current(self._module._id_pointer, result, self._index, channel)
        return handle_sign(Result(result.error, result.value), 32, True)


    def getCC2Current(self, channel):

        '''
        Get the current through the CC2 for a port.
        
        Parameters
        ----------
        channel : unsigned char
            The USB sub channel.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : int
                    The USB channel current in micro-amps (1 == 1e-6A).
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_getCC2Current(self._module._id_pointer, result, self._index, channel)
        return handle_sign(Result(result.error, result.value), 32, True)


    def getCC1Voltage(self, channel):

        '''
        Get the voltage of CC1 for a port.
        
        Parameters
        ----------
        channel : unsigned char
            The USB sub channel.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : int
                    The USB channel voltage in micro-volts (1 == 1e-6V).
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_getCC1Voltage(self._module._id_pointer, result, self._index, channel)
        return handle_sign(Result(result.error, result.value), 32, True)


    def getCC2Voltage(self, channel):

        '''
        Get the voltage of CC2 for a port.
        
        Parameters
        ----------
        channel : unsigned char
            The USB sub channel.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : int
                    The USB channel voltage in micro-volts (1 == 1e-6V).
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_getCC2Voltage(self._module._id_pointer, result, self._index, channel)
        return handle_sign(Result(result.error, result.value), 32, True)


    def setSBUEnable(self, channel, enable):

        '''
        Enable/Disable only the SBU1/2 based on the configuration of the usbPortMode settings.
        
        Parameters
        ----------
        channel : unsigned char
            The USB sub channel.
        enable : bool
            The state to be set
            - Disabled: 0
            - Enabled: 1
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_setSBUEnable(self._module._id_pointer, result, self._index, channel, enable)
        return result.error


    def getSBUEnable(self, channel):

        '''
        Get the Enable/Disable status of the SBU
        
        Parameters
        ----------
        channel : unsigned char
            The USB sub channel.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : bool
                    The enable/disable status of the SBU
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_getSBUEnable(self._module._id_pointer, result, self._index, channel)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setCableFlip(self, channel, enable):

        '''
        Set Cable flip. This will flip SBU, CC and SS data lines.
        
        Parameters
        ----------
        channel : unsigned char
            The USB sub channel.
        enable : bool
            The state to be set The state to be set
                - Disabled: 0
                - Enabled: 1
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_setCableFlip(self._module._id_pointer, result, self._index, channel, enable)
        return result.error


    def getCableFlip(self, channel):

        '''
        Get Cable flip setting.
        
        Parameters
        ----------
        channel : unsigned char
            The USB sub channel.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : bool
                    The enable/disable status of cable flip.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_getCableFlip(self._module._id_pointer, result, self._index, channel)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setAltModeConfig(self, channel, configuration):

        '''
        Set USB Alt Mode Configuration.
        
        Parameters
        ----------
        channel : unsigned char
            The USB sub channel
        configuration : unsigned int
            The USB configuration to be set for the given channel.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_setAltModeConfig(self._module._id_pointer, result, self._index, channel, configuration)
        return result.error


    def getAltModeConfig(self, channel):

        '''
        Get USB Alt Mode Configuration.
        
        Parameters
        ----------
        channel : unsigned char
            The USB sub channel
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    The USB configuration for the given channel.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_getAltModeConfig(self._module._id_pointer, result, self._index, channel)
        return handle_sign(Result(result.error, result.value), 32, False)


    def getSBU1Voltage(self, channel):

        '''
        Get the voltage of SBU1 for a port.
        
        Parameters
        ----------
        channel : unsigned char
            The USB sub channel.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : int
                    The USB channel voltage in micro-volts (1 == 1e-6V).
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_getSBU1Voltage(self._module._id_pointer, result, self._index, channel)
        return handle_sign(Result(result.error, result.value), 32, True)


    def getSBU2Voltage(self, channel):

        '''
        Get the voltage of SBU2 for a port.
        
        Parameters
        ----------
        channel : unsigned char
            The USB sub channel.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : int
                    The USB channel voltage in micro-volts (1 == 1e-6V).
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.usb_getSBU2Voltage(self._module._id_pointer, result, self._index, channel)
        return handle_sign(Result(result.error, result.value), 32, True)


