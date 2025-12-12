from ._bs_c_cffi import ffi
from . import _BS_C #imported from __init__
from .ffi_utils import data_to_bytearray
from .result import Result


class BS_PD_Packet(object):
    """
    Python representation of BS_PD_Packet_t (C structure)
        - channel (uint8_t): Channel/Index
        - seconds (uint8_t): Seconds in device time since power on.
        - uSeconds (uint32_t): Micro Seconds in device time since power on.
        - direction (enumeration): Direction of packet transmission relative to the device.
            - Invalid   = 0
            - Transmit  = 1
            - Receive   = 2
            - Unknown   = 3
        - sop (enumeration): See bs_pd_packet.h for more details
            - SOP       = 0
            - SOP'      = 1
            - SOP''     = 2
            - Unknown   = 3
        - event (enumeration): See powerdeliveryLogEvent in aProtocolDefs.h
            - pdEventNone                       = 0
            - pdEventPacket                     = 1
            - pdEventConnect                    = 2
            - pdEventDisconnect                 = 3
            - pdEventCableResetReceived         = 4
            - pdEventCableResetSent             = 5
            - pdEventHardResetReceived          = 6
            - pdEventHardResetSent              = 7
            - pdEventMessageTransmitFailed      = 8   // No GoodCRC received
            - pdEventMessageTransmitDiscarded   = 9   // Incoming message detected so tx discarded
            - pdEventPDFunctionDisabled         = 10  // PD Stack is giving up on PD Comms
            - pdEventVBUSEnabled                = 11
            - pdEventVBUSDisabled               = 12
            - pdEventVCONNEnabled               = 13
            - pdEventVCONNDisabled              = 14
            - pdEventRp1A5                      = 15  // Used for Src Atomic Message Sequences
            - pdEventRp3A0                      = 16  // Used for Src Atomic Message Sequences
            - pdEventBistEnter                  = 17
            - pdEventBistExit                   = 18
            - pdEventLast                       = 19 // Should always be last!!
        - payload (list): Raw PD Packet data
    """

    def __init__(self, channel=0, seconds=0, uSeconds=0, direction=0, sop=0, event=0, payload=[], ccChannel=0, crc=0):
        self.channel = channel
        self.seconds = seconds
        self.uSeconds = uSeconds
        self.direction = direction
        self.sop = sop
        self.event = event
        self.payload = payload
        self.ccChannel = ccChannel
        self.crc = crc

    def __eq__(self, other):
        if isinstance(other, BS_PD_Packet):
            return  self.channel == other.channel and \
                    self.seconds == other.seconds and \
                    self.uSeconds == other.uSeconds and \
                    self.direction == other.direction and \
                    self.sop == other.sop and \
                    self.event == other.event and \
                    self.payload == other.payload and \
                    self.ccChannel == other.ccChannel and \
                    self.crc == other.crc
        return False

    def __str__(self):
        ret = "\n"
        ret = ret + "Channel: %d\n" % (self.channel)
        ret = ret + "Event: %d\n" % (self.event)
        ret = ret + "Timestamp: %d:%d (seconds:uSeconds)\n" % (self.seconds, self.uSeconds)
        ret = ret + "Direction: %d\n" % (self.direction)
        ret = ret + "SOP: %d\n" % (self.sop)
        ret = ret + "Payload: %s\n" % (self.payload) 
        ret = ret + "CC Channel: %s\n" % (self.ccChannel) 
        ret = ret + "CRC: %s\n" % (self.crc) 

        return ret

    def __repr__(self):
        return self.__str__()


class PDChannelLogger(object):
    """
    Manages BrainStem Power Delivery logging packets.

    :param module: : Reference to an existing BrainStem Module
    :type module: Module

    :param index: Index/channel logging should be enabled for.
    :type index: unsigned byte

    :param buffer_length: Number of packets the class should queue before dropping.
    :type buffer_length: unsigned short
    """

    def __init__(self, module, index, buffer_length=1024):
        self._index = index
        self._module = module
        self._buffer_length = buffer_length

        result = ffi.new("struct Result*")
        _BS_C.PDChannelLogger_create(self._module._id_pointer, result, self._index, self._buffer_length);
        if result.error != Result.NO_ERROR:
            raise RuntimeError("Failed to create PDChannelLogger: {}".format(result.error))

    def __del__(self):
        result = ffi.new("struct Result*")
        _BS_C.PDChannelLogger_destroy(self._module._id_pointer, result, self._index);


    @property
    def index(self):
        """
        Gets the Index/Channel

        :return: Index/channel of the associated object.
        :rtype: unsigned byte
        """
        return self._index


    @property
    def module(self):
        """ 
        Gets the Module object.

        :return: The associated module object. 
        :rtype: Module
        """
        return self._module


    @property
    def buffer_length(self):
        """ 
        Gets the buffer length

        :return: Buffer length of the associated object. 
        :rtype: unsigned int
        """
        return self._buffer_length


    def setEnabled(self, enabled):
        """ 
        Enables Power Delivery logging.

        :param enable: True enables logging; False disables logging
        :type enable: bool
       
        return: An error result from the list of defined error codes in brainstem.result
        """

        result = ffi.new("struct Result*")
        _BS_C.PDChannelLogger_setEnabled(self._module._id_pointer, result, self._index, enabled)
        return result.error
    
    
    def getPacket(self):
        """ 
        Attempts to takes a packet from the internal buffer.

        :return: Result object containing the requested value when the results error is set to NO_ERROR(0)
        """

        result = ffi.new("struct Result*")
        packetCCA = ffi.new("struct BS_PD_Packet_CCA*")
        _BS_C.PDChannelLogger_getPacket(self._module._id_pointer, result, self._index, packetCCA)
        payload_list = [packetCCA.payload[i] for i in range(packetCCA.payloadSize)]
        sample = BS_PD_Packet(packetCCA.channel, packetCCA.seconds, packetCCA.uSeconds, packetCCA.direction, packetCCA.sop, packetCCA.event, payload_list)

        result2 = ffi.new("struct Result*")
        _BS_C.PDChannelLogger_freePayloadBuffer(self._module._id_pointer, result2, packetCCA)
        return Result(result.error, sample)


    def getPackets(self, buffer_length=100):
        """ 
        Attempts to take a multiple packets (up to a maximum) from the internal buffer.

        :return: Result object containing the requested value when the results error is set to NO_ERROR(0)
        """
        result = ffi.new("struct Result*")
        packetBuffer = ffi.new("struct BS_PD_Packet_CCA[]", buffer_length)
        _BS_C.PDChannelLogger_getPackets(self._module._id_pointer, result, self._index, packetBuffer, buffer_length)
        
        sample_list = []
        for x in range(0, result.value):
            payload_list = [packetBuffer[x].payload[i] for i in range(packetBuffer[x].payloadSize)]
            sample = BS_PD_Packet(packetBuffer[x].channel, packetBuffer[x].seconds, packetBuffer[x].uSeconds, packetBuffer[x].direction, packetBuffer[x].sop, packetBuffer[x].event, payload_list)
            sample_list.append(sample)

            result2 = ffi.new("struct Result*")
            element_ptr = ffi.cast("struct BS_PD_Packet_CCA*", packetBuffer) + x
            _BS_C.PDChannelLogger_freePayloadBuffer(self._module._id_pointer, result2, element_ptr)
            
        return Result(result.error, tuple(sample_list))



