# This file was auto-generated. Do not modify.

from ._bs_c_cffi import ffi
from . import _BS_C #imported from __init__
from .Entity_Entity import *
from .result import Result
from .ffi_utils import data_to_bytearray, bytes_to_string, handle_sign, handle_sign_value, get_ffi_buffer

class PowerDelivery(Entity):
    
    ''' 
    Power Delivery or PD is a power specification which allows more charging options and
    device behaviors within the USB interface.
    This Entity will allow you to directly access the vast landscape of PD.
    
    ''' 


    def __init__(self, module, index):
        super(PowerDelivery, self).__init__(module, _BS_C.cmdPOWERDELIVERY, index)

    def getConnectionState(self):

        '''
        Gets the current state of the connection in the form of an enumeration.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Pointer to be filled with the current connection state.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_getConnectionState(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def getNumberOfPowerDataObjects(self, partner, power_role):

        '''
        Gets the number of Power Data Objects (PDOs) for a given partner and power role.
        
        Parameters
        ----------
        partner : unsigned char
            Indicates which side of the PD connection is in question.
                - Local = 0 = powerdeliveryPartnerLocal
                - Remote = 1 = powerdeliveryPartnerRemote
        power_role : unsigned char
            Indicates which power role of PD connection is in question.
                - Source = 1 = powerdeliveryPowerRoleSource
                - Sink = 2 = powerdeliveryPowerRoleSink
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Variable to be filled with the number of PDOs.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_getNumberOfPowerDataObjects(self._module._id_pointer, result, self._index, partner, power_role)
        return handle_sign(Result(result.error, result.value), 8, False)


    def getPowerDataObject(self, partner, power_role, rule_index):

        '''
        Gets the Power Data Object (PDO) for the requested partner, powerRole and index.
        
        Parameters
        ----------
        partner : unsigned char
            Indicates which side of the PD connection is in question.
                - Local = 0 = powerdeliveryPartnerLocal
                - Remote = 1 = powerdeliveryPartnerRemote
        power_role : unsigned char
            Indicates which power role of PD connection is in question.
                - Source = 1 = powerdeliveryPowerRoleSource
                - Sink = 2 = powerdeliveryPowerRoleSink
        rule_index : unsigned char
            The index of the PDO in question. Valid index are 1-7.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    Variable to be filled with the requested power rule.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_getPowerDataObject(self._module._id_pointer, result, self._index, partner, power_role, rule_index)
        return handle_sign(Result(result.error, result.value), 32, False)


    def setPowerDataObject(self, power_role, rule_index, pdo):

        '''
        Sets the Power Data Object (PDO) of the local partner for a given power role and index.
        
        Parameters
        ----------
        power_role : unsigned char
            Indicates which power role of PD connection is in question.
                - Source = 1 = powerdeliveryPowerRoleSource
                - Sink = 2 = powerdeliveryPowerRoleSink
        rule_index : unsigned char
            The index of the PDO in question. Valid index are 1-7.
        pdo : unsigned int
            Power Data Object to be set.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_setPowerDataObject(self._module._id_pointer, result, self._index, power_role, rule_index, pdo)
        return result.error


    def resetPowerDataObjectToDefault(self, power_role, rule_index):

        '''
        Resets the Power Data Object (PDO) of the Local partner for a given power role and index.
        
        Parameters
        ----------
        power_role : unsigned char
            Indicates which power role of PD connection is in question.
                - Source = 1 = powerdeliveryPowerRoleSource
                - Sink = 2 = powerdeliveryPowerRoleSink
        rule_index : unsigned char
            The index of the PDO in question. Valid index are 1-7.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_resetPowerDataObjectToDefault(self._module._id_pointer, result, self._index, power_role, rule_index)
        return result.error


    def getPowerDataObjectList(self, buffer_length = 16384):

        '''
        Gets all Power Data Objects (PDOs).
        Equivalent to calling PowerDeliveryClass::getPowerDataObject() on all partners, power
        roles, and index's.
        
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
                    The order of which is:
                        - Rules 1-7 Local Source
                        - Rules 1-7 Local Sink
                        - Rules 1-7 Partner Source
                        - Rules 1-7 Partner Sink.
        
        '''

        ffi_buffer = get_ffi_buffer(32, False, buffer_length)

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_getPowerDataObjectList(self._module._id_pointer, result, self._index, ffi_buffer, buffer_length)
        return_list = [handle_sign_value(ffi_buffer[i], 32, False) for i in range(result.value)]
        return Result(result.error, return_list)


    def getPowerDataObjectEnabled(self, power_role, rule_index):

        '''
        Gets the enabled state of the Local Power Data Object (PDO) for a given power role and
        index.
        Enabled refers to whether the PDO will be advertised when a PD connection is made.
        This does not indicate the currently active rule index. This information can be found in
        Request Data Object (RDO).
        
        Parameters
        ----------
        power_role : unsigned char
            Indicates which power role of PD connection is in question.
                - Source = 1 = powerdeliveryPowerRoleSource
                - Sink = 2 = powerdeliveryPowerRoleSink
        rule_index : unsigned char
            The index of the PDO in question. Valid index are 1-7.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : bool
                    Variable to be filled with enabled state.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_getPowerDataObjectEnabled(self._module._id_pointer, result, self._index, power_role, rule_index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setPowerDataObjectEnabled(self, power_role, rule_index, enabled):

        '''
        Sets the enabled state of the Local Power Data Object (PDO) for a given powerRole and
        index.
        Enabled refers to whether the PDO will be advertised when a PD connection is made.
        This does not indicate the currently active rule index. This information can be found in
        Request Data Object (RDO).
        
        Parameters
        ----------
        power_role : unsigned char
            Indicates which power role of PD connection is in question.
                - Source = 1 = powerdeliveryPowerRoleSource
                - Sink = 2 = powerdeliveryPowerRoleSink
        rule_index : unsigned char
            The index of the PDO in question. Valid index are 1-7.
        enabled : bool
            The state to be set.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_setPowerDataObjectEnabled(self._module._id_pointer, result, self._index, power_role, rule_index, enabled)
        return result.error


    def getPowerDataObjectEnabledList(self, power_role):

        '''
        Gets all Power Data Object enables for a given power role.
        Equivalent of calling PowerDeliveryClass::getPowerDataObjectEnabled() for all indexes.
        
        Parameters
        ----------
        power_role : unsigned char
            Indicates which power role of PD connection is in question.
                - Source = 1 = powerdeliveryPowerRoleSource
                - Sink = 2 = powerdeliveryPowerRoleSink
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Variable to be filled with a mapped representation of the enabled PDOs for a
                    given power role.
                    Values align with a given rule index (bits 1-7, bit 0 is invalid)
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_getPowerDataObjectEnabledList(self._module._id_pointer, result, self._index, power_role)
        return handle_sign(Result(result.error, result.value), 8, False)


    def getRequestDataObject(self, partner):

        '''
        Gets the current Request Data Object (RDO) for a given partner.
        RDOs are provided by the sinking device and exist only after a successful PD negotiation
        (Otherwise zero).
        Only one RDO can exist at a time. i.e. Either the Local or Remote partner RDO
        
        Parameters
        ----------
        partner : unsigned char
            Indicates which side of the PD connection is in question.
                - Local = 0 = powerdeliveryPartnerLocal
                - Remote = 1 = powerdeliveryPartnerRemote
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    Variable to be filled with the current RDO.
                    Zero indicates the RDO is not active.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_getRequestDataObject(self._module._id_pointer, result, self._index, partner)
        return handle_sign(Result(result.error, result.value), 32, False)


    def setRequestDataObject(self, rdo):

        '''
        Sets the current Request Data Object (RDO) for a given partner.
        Only the local partner can be changed.
        RDOs are provided by the sinking device and exist only after a successful PD negotiation
        (Otherwise zero).
        Only one RDO can exist at a time. i.e. Either the Local or Remote partner RDO
        
        Parameters
        ----------
        rdo : unsigned int
            Request Data Object to be set.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_setRequestDataObject(self._module._id_pointer, result, self._index, rdo)
        return result.error


    def getLinkState(self):

        '''
        Gets the current state of the connection in the form of a bitmask.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    Pointer to be filled with the current connection state bits.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_getLinkState(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


    def getAttachTimeElapsed(self, buffer_length = 16384):

        '''
        Gets the length of time that the port has been in the attached state.
        Returned as a list of two unsigned integers, first seconds, then microseconds.
        
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
                    Pointer to list of unsigned integers to fill with attach time elapsed
        
        '''

        ffi_buffer = get_ffi_buffer(32, False, buffer_length)

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_getAttachTimeElapsed(self._module._id_pointer, result, self._index, ffi_buffer, buffer_length)
        return_list = [handle_sign_value(ffi_buffer[i], 32, False) for i in range(result.value)]
        return Result(result.error, return_list)


    def getPowerRoleCapabilities(self):

        '''
        Gets the power roles that may be advertised by the local partner. (CC Strapping).
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Variable to be filed with the power role
                        - None = 0 = pdPowerRoleCapabilities_None
                        - Source = 1 = pdPowerRoleCapabilities_Source
                        - Sink = 2 = pdPowerRoleCapabilities_Sink
                        - Source/Sink = 3 = pdPowerRoleCapabilities_DualRole (Dual Role Port)
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_getPowerRoleCapabilities(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def getPowerRole(self):

        '''
        Gets the power role that is currently being advertised by the local partner. (CC
        Strapping).
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Variable to be filed with the power role
                        - Disabled = 0 = powerdeliveryPowerRoleDisabled
                        - Source = 1= powerdeliveryPowerRoleSource
                        - Sink = 2 = powerdeliveryPowerRoleSink
                        - Source/Sink = 3 = powerdeliveryPowerRoleSourceSink (Dual Role Port)
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_getPowerRole(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setPowerRole(self, power_role):

        '''
        Set the current power role to be advertised by the Local partner. (CC Strapping).
        
        Parameters
        ----------
        power_role : unsigned char
            Value to be applied.
                - Disabled = 0 = powerdeliveryPowerRoleDisabled
                - Source = 1= powerdeliveryPowerRoleSource
                - Sink = 2 = powerdeliveryPowerRoleSink
                - Source/Sink = 3 = powerdeliveryPowerRoleSourceSink (Dual Role Port)
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_setPowerRole(self._module._id_pointer, result, self._index, power_role)
        return result.error


    def getPowerRolePreferred(self):

        '''
        Gets the preferred power role currently being advertised by the Local partner. (CC
        Strapping).
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Value to be applied.
                        - Disabled = 0 = powerdeliveryPowerRoleDisabled
                        - Source = 1= powerdeliveryPowerRoleSource
                        - Sink = 2 = powerdeliveryPowerRoleSink
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_getPowerRolePreferred(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setPowerRolePreferred(self, power_role):

        '''
        Set the preferred power role to be advertised by the Local partner (CC Strapping).
        
        Parameters
        ----------
        power_role : unsigned char
            Value to be applied.
                - Disabled = 0 = powerdeliveryPowerRoleDisabled
                - Source = 1= powerdeliveryPowerRoleSource
                - Sink = 2 = powerdeliveryPowerRoleSink
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_setPowerRolePreferred(self._module._id_pointer, result, self._index, power_role)
        return result.error


    def getDataRoleCapabilities(self):

        '''
        Gets the data roles that may be advertised by the local partner.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Variable to be filed with the data role
                        - None = 0 = pdDataRoleCapabilities_None
                        - DFP = 1 = pdDataRoleCapabilities_DFP
                        - UFP = 2 = pdDataRoleCapabilities_UFP
                        - DFP/UFP = 3 = pdDataRoleCapabilities_DualRole (Dual Role Port)
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_getDataRoleCapabilities(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def getCableVoltageMax(self):

        '''
        Gets the maximum voltage capability reported by the e-mark of the attached cable.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Variable to be filled with an enumerated representation of voltage.
                        - Unknown/Unattached (0)
                        - 20 Volts DC (1)
                        - 30 Volts DC (2)
                        - 40 Volts DC (3)
                        - 50 Volts DC (4)
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_getCableVoltageMax(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def getCableCurrentMax(self):

        '''
        Gets the maximum current capability report by the e-mark of the attached cable.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Variable to be filled with an enumerated representation of current.
                        - Unknown/Unattached (0)
                        - 3 Amps (1)
                        - 5 Amps (2)
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_getCableCurrentMax(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def getCableSpeedMax(self):

        '''
        Gets the maximum data rate capability reported by the e-mark of the attached cable.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Variable to be filled with an enumerated representation of data speed.
                        - Unknown/Unattached (0)
                        - USB 2.0 (1)
                        - USB 3.2 gen 1 (2)
                        - USB 3.2 / USB 4 gen 2 (3)
                        - USB 4 gen 3 (4)
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_getCableSpeedMax(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def getCableType(self):

        '''
        Gets the cable type reported by the e-mark of the attached cable.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Variable to be filled with an enumerated representation of the cable type.
                        - Invalid, no e-mark and not Vconn powered (0)
                        - Passive cable with e-mark (1)
                        - Active cable (2)
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_getCableType(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def getCableOrientation(self):

        '''
        Gets the current orientation being used for PD communication
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Variable filled with an enumeration of the orientation.
                        - Unconnected (0)
                        - CC1 (1)
                        - CC2 (2)
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_getCableOrientation(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def request(self, request):

        '''
        Requests an action of the Remote partner.
        Actions are not guaranteed to occur.
        
        Parameters
        ----------
        request : unsigned char
            Request to be issued to the remote partner
                - pdRequestHardReset (0)
                - pdRequestSoftReset (1)
                - pdRequestDataReset (2)
                - pdRequestPowerRoleSwap (3)
                - pdRequestPowerFastRoleSwap (4)
                - pdRequestDataRoleSwap (5)
                - pdRequestVconnSwap (6)
                - pdRequestSinkGoToMinimum (7)
                - pdRequestRemoteSourcePowerDataObjects (8)
                - pdRequestRemoteSinkPowerDataObjects (9)
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_request(self._module._id_pointer, result, self._index, request)
        return result.error


    def requestStatus(self):

        '''
        Gets the status of the last request command sent.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    Variable to be filled with the status
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_requestStatus(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


    def getOverride(self):

        '''
        Gets the current enabled overrides
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned int
                    Bit mapped representation of the current override configuration.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_getOverride(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 32, False)


    def setOverride(self, overrides):

        '''
        Sets the current enabled overrides
        
        Parameters
        ----------
        overrides : unsigned int
            Overrides to be set in a bit mapped representation.
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_setOverride(self._module._id_pointer, result, self._index, overrides)
        return result.error


    def getFlagMode(self, flag):

        '''
        Gets the current mode of the local partner flag/advertisement.
        These flags are apart of the first Local Power Data Object and must be managed in order to
        accurately represent the system to other PD devices.
        This API allows overriding of that feature. Overriding may lead to unexpected behaviors.
        
        Parameters
        ----------
        flag : unsigned char
            Flag/Advertisement to be modified
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Variable to be filled with the current mode.
                        - Disabled (0)
                        - Enabled (1)
                        - Auto (2) default
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_getFlagMode(self._module._id_pointer, result, self._index, flag)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setFlagMode(self, flag, mode):

        '''
        Sets how the local partner flag/advertisement is managed.
        These flags are apart of the first Local Power Data Object and must be managed in order to
        accurately represent the system to other PD devices.
        This API allows overriding of that feature. Overriding may lead to unexpected behaviors.
        
        Parameters
        ----------
        flag : unsigned char
            Flag/Advertisement to be modified
        mode : unsigned char
            Value to be applied.
                - Disabled (0)
                - Enabled (1)
                - Auto (2) default
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_setFlagMode(self._module._id_pointer, result, self._index, flag, mode)
        return result.error


    def getPeakCurrentConfiguration(self):

        '''
        Gets the Peak Current Configuration for the Local Source.
        The peak current configuration refers to the allowable tolerance/overload capabilities in
        regards to the devices max current.
        This tolerance includes a maximum value and a time unit.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    An enumerated value referring to the current configuration.
                        - Allowable values are 0 - 4
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_getPeakCurrentConfiguration(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setPeakCurrentConfiguration(self, configuration):

        '''
        Sets the Peak Current Configuration for the Local Source.
        The peak current configuration refers to the allowable tolerance/overload capabilities in
        regards to the devices max current.
        This tolerance includes a maximum value and a time unit.
        
        Parameters
        ----------
        configuration : unsigned char
            An enumerated value referring to the configuration to be set
                - Allowable values are 0 - 4
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_setPeakCurrentConfiguration(self._module._id_pointer, result, self._index, configuration)
        return result.error


    def getFastRoleSwapCurrent(self):

        '''
        Gets the Fast Role Swap Current
        The fast role swap current refers to the amount of current required by the Local Sink in
        order to successfully preform the swap.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    An enumerated value referring to current swap value.
                        - 0A (0)
                        - 900mA (1)
                        - 1.5A (2)
                        - 3A (3)
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_getFastRoleSwapCurrent(self._module._id_pointer, result, self._index)
        return handle_sign(Result(result.error, result.value), 8, False)


    def setFastRoleSwapCurrent(self, swap_current):

        '''
        Sets the Fast Role Swap Current
        The fast role swap current refers to the amount of current required by the Local Sink in
        order to successfully preform the swap.
        
        Parameters
        ----------
        swap_current : unsigned char
            An enumerated value referring to value to be set.
                - 0A (0)
                - 900mA (1)
                - 1.5A (2)
                - 3A (3)
        
        Returns
        -------
        unsigned byte
            An error result from the list of defined error codes in brainstem.result.Result
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_setFastRoleSwapCurrent(self._module._id_pointer, result, self._index, swap_current)
        return result.error


    @staticmethod
    def packDataObjectAttributes(partner, power_role, rule_index):

        '''
        Helper function for packing Data Object attributes.
        This value is used as a subindex for all Data Object calls with the BrainStem Protocol.
        
        Parameters
        ----------
        partner : unsigned char
            Indicates which side of the PD connection.
                - Local = 0 = powerdeliveryPartnerLocal
                - Remote = 1 = powerdeliveryPartnerRemote
        power_role : unsigned char
            Indicates which power role of PD connection.
                - Source = 1 = powerdeliveryPowerRoleSource
                - Sink = 2 = powerdeliveryPowerRoleSink
        rule_index : unsigned char
            Data object index.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned value on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                value : unsigned char
                    Variable to be filled with packed values.
        
        '''

        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_packDataObjectAttributes(result, partner, power_role, rule_index)
        return handle_sign(Result(result.error, result.value), 8, False)


    @staticmethod
    def unpackDataObjectAttributes(attributes):

        '''
        Helper function for unpacking Data Object attributes.
        This value is used as a subindex for all Data Object calls with the BrainStem Protocol.
        
        Parameters
        ----------
        attributes : unsigned char
            Variable to be filled with packed values.
        
        Returns
        -------
        brainstem.result.Result
            Object containing error code and returned values on success.
                error : unsigned byte
                    An error result from the list of defined error codes
                partner : unsigned char
                    Indicates which side of the PD connection.
                        - Local = 0 = powerdeliveryPartnerLocal
                        - Remote = 1 = powerdeliveryPartnerRemote
                power_role : unsigned char
                    Indicates which power role of PD connection.
                        - Source = 1 = powerdeliveryPowerRoleSource
                        - Sink = 2 = powerdeliveryPowerRoleSink
                rule_index : unsigned char
                    Data object index.
        
        '''

        _partner = ffi.new("unsigned char*")
        _powerRole = ffi.new("unsigned char*")
        _ruleIndex = ffi.new("unsigned char*")
        result = ffi.new("struct Result*")
        _BS_C.powerdelivery_unpackDataObjectAttributes(result, attributes, _partner, _powerRole, _ruleIndex)
        return Result(result.error, partner=int(_partner), power_role=int(_powerRole), rule_index=int(_ruleIndex))


