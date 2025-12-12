# Copyright (c) 2018 Acroname Inc. - All Rights Reserved
#
# This file is part of the BrainStem (tm) package which is released under MIT.
# See file LICENSE or go to https://acroname.com for full license details.

"""
Provides specific module instances, and entity functionality.

The Module and Entity classes contained in this module provide the core API functionality for all of the Brainstem
modules. For more information about possible entities please see the
`Entity`_ section of the `Acroname BrainStem Reference`_

.. _Entity:
    https://acroname.com/reference/api/entities

.. _Acroname BrainStem Reference:
    https://acroname.com/reference
"""

from . import _BS_C
from .module import Module
from .link import Spec
from .entity import *

from . import defs


class EtherStem(Module):
    """ Concrete Module implementation for 40Pin EtherStem modules

        EtherStem modules contain the following entities:
            * system
            * analog[0-3]
            * app[0-3]
            * clock
            * digital[0-14]
            * i2c[0-1]
            * pointer[0-3]
            * servo[0-7]
            * store[0-2]
            * timer[0-7]

        Useful Constants:
            * BASE_ADDRESS (2)
            * NUMBER_OF_STORES (3)
            * NUMBER_OF_INTERNAL_SLOTS (12)
            * NUMBER_OF_RAM_SLOTS (1)
            * NUMBER_OF_SD_SLOTS (255)
            * NUMBER_OF_ANALOGS (4)
            * DAC_ANALOG_INDEX (3)
            * FIXED_DAC_ANALOG (False)
            * NUMBER_OF_DIGITALS (15)
            * NUMBER_OF_I2C (2)
            * NUMBER_OF_POINTERS (4)
            * NUMBER_OF_TIMERS (8)
            * NUMBER_OF_APPS (4)
            * NUMBER_OF_SERVOS (8)
            * NUMBER_OF_SERVO_OUTPUTS (4)
            * NUMBER_OF_SERVO_INPUTS (4)
            * ANALOG_BULK_CAPTURE_MAX_HZ (200000)
            * ANALOG_BULK_CAPTURE_MIN_HZ (7000)

    """

    BASE_ADDRESS = 2
    NUMBER_OF_STORES = 3
    NUMBER_OF_INTERNAL_SLOTS = 12
    NUMBER_OF_RAM_SLOTS = 1
    NUMBER_OF_SD_SLOTS = 255
    NUMBER_OF_ANALOGS = 4
    DAC_ANALOG_INDEX = 3
    FIXED_DAC_ANALOG = False
    NUMBER_OF_DIGITALS = 15
    NUMBER_OF_I2C = 2
    NUMBER_OF_POINTERS = 4
    NUMBER_OF_TIMERS = 8
    NUMBER_OF_APPS = 4
    NUMBER_OF_SERVOS = 8
    NUMBER_OF_SERVO_OUTPUTS = 4
    NUMBER_OF_SERVO_INPUTS = 4
    ANALOG_BULK_CAPTURE_MAX_HZ = 200000
    ANALOG_BULK_CAPTURE_MIN_HZ = 7000

    def __init__(self, address=BASE_ADDRESS, enable_auto_networking=True, model=defs.MODEL_ETHERSTEM):
        super(EtherStem, self).__init__(address, enable_auto_networking, model)
        self.system = System(self, 0)
        self.analog = [Analog(self, i) for i in range(0, 4)]
        self.app = [App(self, i) for i in range(0, 4)]
        self.clock = Clock(self, 0)
        self.digital = [Digital(self, i) for i in range(0, 15)]
        self.i2c = [I2C(self, i) for i in range(0, 2)]
        self.pointer = [Pointer(self, i) for i in range(0, 4)]
        self.store = [Store(self, i) for i in range(0, 3)]
        self.timer = [Timer(self, i) for i in range(0, 8)]
        self.servo = [RCServo(self, i) for i in range(0, 8)]

    def connect(self, serial_number, **kwargs):
        return super(EtherStem, self).connect(Spec.TCPIP, serial_number)


class MTMDAQ1(Module):
    """ Concrete Module implementation for MTM-DAQ-1 module

        MTM-DAQ-1 modules contain contain the following entities:
            * system
            * app[0-3]
            * digital[0-1]
            * analog[0-19]
            * i2c[0]
            * pointer[0-3]
            * store[0-1]
            * timer[0-7]

        Useful Constants:
            * BASE_ADDRESS (10)
            * NUMBER_OF_STORES (2)
            * NUMBER_OF_INTERNAL_SLOTS (12)
            * NUMBER_OF_RAM_SLOTS (1)
            * NUMBER_OF_DIGITALS (2)
            * NUMBER_OF_ANALOGS (20)
            * NUMBER_OF_I2C (1)
            * NUMBER_OF_POINTERS (4)
            * NUMBER_OF_TIMERS (8)
            * NUMBER_OF_APPS (4)
            * ANALOG_RANGE_P0V064N0V064 (0)
            * ANALOG_RANGE_P0V64N0V64 (1)
            * ANALOG_RANGE_P0V128N0V128 (2)
            * ANALOG_RANGE_P1V28N1V28 (3)
            * ANALOG_RANGE_P1V28N0V0 (4)
            * ANALOG_RANGE_P0V256N0V256 (5)
            * ANALOG_RANGE_P2V56N2V56 (6)
            * ANALOG_RANGE_P2V56N0V0 (7)
            * ANALOG_RANGE_P0V512N0V512 (8)
            * ANALOG_RANGE_P5V12N5V12 (9)
            * ANALOG_RANGE_P5V12N0V0 (10)
            * ANALOG_RANGE_P1V024N1V024 (11)
            * ANALOG_RANGE_P10V24N10V24 (12)
            * ANALOG_RANGE_P10V24N0V0 (13)
            * ANALOG_RANGE_P2V048N0V0 (14)
            * ANALOG_RANGE_P4V096N0V0 (15)
    """

    BASE_ADDRESS = 10
    NUMBER_OF_STORES = 2
    NUMBER_OF_INTERNAL_SLOTS = 12
    NUMBER_OF_RAM_SLOTS = 1
    NUMBER_OF_DIGITALS = 2
    NUMBER_OF_ANALOGS = 20
    NUMBER_OF_I2C = 1
    NUMBER_OF_POINTERS = 4
    NUMBER_OF_TIMERS = 8
    NUMBER_OF_APPS = 4
    ANALOG_RANGE_P0V064N0V064 = 0
    ANALOG_RANGE_P0V64N0V64 = 1
    ANALOG_RANGE_P0V128N0V128 = 2
    ANALOG_RANGE_P1V28N1V28 = 3
    ANALOG_RANGE_P1V28N0V0 = 4
    ANALOG_RANGE_P0V256N0V256 = 5
    ANALOG_RANGE_P2V56N2V56 = 6
    ANALOG_RANGE_P2V56N0V0 = 7
    ANALOG_RANGE_P0V512N0V512 = 8
    ANALOG_RANGE_P5V12N5V12 = 9
    ANALOG_RANGE_P5V12N0V0 = 10
    ANALOG_RANGE_P1V024N1V024 = 11
    ANALOG_RANGE_P10V24N10V24 = 12
    ANALOG_RANGE_P10V24N0V0 = 13
    ANALOG_RANGE_P2V048N0V0 = 14
    ANALOG_RANGE_P4V096N0V0 = 15

    def __init__(self, address=BASE_ADDRESS, enable_auto_networking=True, model=defs.MODEL_MTM_DAQ_1):
        super(MTMDAQ1, self).__init__(address, enable_auto_networking, model)
        self.system = System(self, 0)
        self.app = [App(self, i) for i in range(0, 4)]
        self.digital = [Digital(self, i) for i in range(0, 2)]
        self.analog = [Analog(self, i) for i in range(0, 20)]
        self.i2c = [I2C(self, i) for i in range(0, 1)]
        self.pointer = [Pointer(self, i) for i in range(0, 4)]
        self.store = [Store(self, i) for i in range(0, 2)]
        self.timer = [Timer(self, i) for i in range(0, 8)]

    def connect(self, serial_number, **kwargs):
        return super(MTMDAQ1, self).connect(Spec.USB, serial_number)


class MTMDAQ2(Module):
    """ Concrete Module implementation for MTM-DAQ-2 module

        MTM-DAQ-2 modules contain contain the following entities:
            * system
            * app[0-3]
            * digital[0-1]
            * analog[0-19]
            * i2c[0]
            * pointer[0-3]
            * store[0-1]
            * timer[0-7]

        Useful Constants:
            * BASE_ADDRESS (10)
            * NUMBER_OF_STORES (2)
            * NUMBER_OF_INTERNAL_SLOTS (12)
            * NUMBER_OF_RAM_SLOTS (1)
            * NUMBER_OF_DIGITALS (2)
            * NUMBER_OF_ANALOGS (20)
            * NUMBER_OF_I2C (1)
            * NUMBER_OF_POINTERS (4)
            * NUMBER_OF_TIMERS (8)
            * NUMBER_OF_APPS (4)
            * ANALOG_RANGE_P0V064N0V064 (0)
            * ANALOG_RANGE_P0V64N0V64 (1)
            * ANALOG_RANGE_P0V128N0V128 (2)
            * ANALOG_RANGE_P1V28N1V28 (3)
            * ANALOG_RANGE_P1V28N0V0 (4)
            * ANALOG_RANGE_P0V256N0V256 (5)
            * ANALOG_RANGE_P2V56N2V56 (6)
            * ANALOG_RANGE_P2V56N0V0 (7)
            * ANALOG_RANGE_P0V512N0V512 (8)
            * ANALOG_RANGE_P5V12N5V12 (9)
            * ANALOG_RANGE_P5V12N0V0 (10)
            * ANALOG_RANGE_P1V024N1V024 (11)
            * ANALOG_RANGE_P10V24N10V24 (12)
            * ANALOG_RANGE_P10V24N0V0 (13)
            * ANALOG_RANGE_P2V048N0V0 (14)
            * ANALOG_RANGE_P4V096N0V0 (15)
            * ANALOG_BULK_CAPTURE_MAX_HZ (500000)
            * ANALOG_BULK_CAPTURE_MIN_HZ (1)
    """

    BASE_ADDRESS = 10
    NUMBER_OF_STORES = 2
    NUMBER_OF_INTERNAL_SLOTS = 12
    NUMBER_OF_RAM_SLOTS = 1
    NUMBER_OF_DIGITALS = 2
    NUMBER_OF_ANALOGS = 20
    NUMBER_OF_I2C = 1
    NUMBER_OF_POINTERS = 4
    NUMBER_OF_TIMERS = 8
    NUMBER_OF_APPS = 4
    ANALOG_RANGE_P0V064N0V064 = 0
    ANALOG_RANGE_P0V64N0V64 = 1
    ANALOG_RANGE_P0V128N0V128 = 2
    ANALOG_RANGE_P1V28N1V28 = 3
    ANALOG_RANGE_P1V28N0V0 = 4
    ANALOG_RANGE_P0V256N0V256 = 5
    ANALOG_RANGE_P2V56N2V56 = 6
    ANALOG_RANGE_P2V56N0V0 = 7
    ANALOG_RANGE_P0V512N0V512 = 8
    ANALOG_RANGE_P5V12N5V12 = 9
    ANALOG_RANGE_P5V12N0V0 = 10
    ANALOG_RANGE_P1V024N1V024 = 11
    ANALOG_RANGE_P10V24N10V24 = 12
    ANALOG_RANGE_P10V24N0V0 = 13
    ANALOG_RANGE_P2V048N0V0 = 14
    ANALOG_RANGE_P4V096N0V0 = 15
    ANALOG_BULK_CAPTURE_MAX_HZ = 500000
    ANALOG_BULK_CAPTURE_MIN_HZ = 1

    def __init__(self, address=BASE_ADDRESS, enable_auto_networking=True, model=defs.MODEL_MTM_DAQ_2):
        super(MTMDAQ2, self).__init__(address, enable_auto_networking, model)
        self.system = System(self, 0)
        self.app = [App(self, i) for i in range(0, 4)]
        self.digital = [Digital(self, i) for i in range(0, 2)]
        self.analog = [Analog(self, i) for i in range(0, 20)]
        self.i2c = [I2C(self, i) for i in range(0, 1)]
        self.pointer = [Pointer(self, i) for i in range(0, 4)]
        self.store = [Store(self, i) for i in range(0, 2)]
        self.timer = [Timer(self, i) for i in range(0, 8)]

    def connect(self, serial_number, **kwargs):
        return super(MTMDAQ2, self).connect(Spec.USB, serial_number)


class MTMEtherStem(Module):
    """ Concrete Module implementation for MTM EtherStem modules

        USBStem modules contain the following entities:
            * system
            * analog[0-3]
            * app[0-3]
            * clock
            * digital[0-14]
            * i2c[0-1]
            * pointer[0-3]
            * servo[0-7]
            * store[0-2]
            * timer[0-7]

        Useful Constants:
            * BASE_ADDRESS (4)
            * NUMBER_OF_STORES (3)
            * NUMBER_OF_INTERNAL_SLOTS (12)
            * NUMBER_OF_RAM_SLOTS (1)
            * NUMBER_OF_SD_SLOTS (255)
            * NUMBER_OF_ANALOGS (4)
            * DAC_ANALOG_INDEX (3)
            * FIXED_DAC_ANALOG (False)
            * NUMBER_OF_DIGITALS (15)
            * NUMBER_OF_I2C (2)
            * NUMBER_OF_POINTERS (4)
            * NUMBER_OF_TIMERS (8)
            * NUMBER_OF_APPS (4)
            * NUMBER_OF_SERVOS (8)
            * NUMBER_OF_SERVO_OUTPUTS (4)
            * NUMBER_OF_SERVO_INPUTS (4)
            * ANALOG_BULK_CAPTURE_MAX_HZ (200000)
            * ANALOG_BULK_CAPTURE_MIN_HZ (7000)
    """

    BASE_ADDRESS = 4
    NUMBER_OF_STORES = 3
    NUMBER_OF_INTERNAL_SLOTS = 12
    NUMBER_OF_RAM_SLOTS = 1
    NUMBER_OF_SD_SLOTS = 255
    NUMBER_OF_ANALOGS = 4
    DAC_ANALOG_INDEX = 3
    FIXED_DAC_ANALOG = True
    NUMBER_OF_DIGITALS = 15
    NUMBER_OF_I2C = 2
    NUMBER_OF_POINTERS = 4
    NUMBER_OF_TIMERS = 8
    NUMBER_OF_APPS = 4
    NUMBER_OF_SERVOS = 8
    NUMBER_OF_SERVO_OUTPUTS = 4
    NUMBER_OF_SERVO_INPUTS = 4
    ANALOG_BULK_CAPTURE_MAX_HZ = 200000
    ANALOG_BULK_CAPTURE_MIN_HZ = 7000

    def __init__(self, address=BASE_ADDRESS, enable_auto_networking=True, model=defs.MODEL_MTM_ETHERSTEM):
        super(MTMEtherStem, self).__init__(address, enable_auto_networking, model)
        self.system = System(self, 0)
        self.analog = [Analog(self, i) for i in range(0, 4)]
        self.app = [App(self, i) for i in range(0, 4)]
        self.clock = Clock(self, 0)
        self.digital = [Digital(self, i) for i in range(0, 15)]
        self.i2c = [I2C(self, i) for i in range(0, 2)]
        self.pointer = [Pointer(self, i) for i in range(0, 4)]
        self.store = [Store(self, i) for i in range(0, 3)]
        self.timer = [Timer(self, i) for i in range(0, 8)]
        self.servo = [RCServo(self, i) for i in range(0, 8)]

    def connect(self, serial_number, **kwargs):
        return super(MTMEtherStem, self).connect(Spec.TCPIP, serial_number)


class MTMIOSerial(Module):
    """ Concrete Module implementation for MTM-IO-Serial module

        MTM-IO-SERIAL modules contain contain the following entities:
            * system
            * app[0-3]
            * digital[0-8]
            * i2c[0]
            * pointer[0-3]
            * servo[0-7]
            * signal[0-4]
            * store[0-1]
            * temperature
            * timer[0-7]
            * uart[0-3]
            * rail[0-2]

        Useful Constants:
            * BASE_ADDRESS (8)
            * NUMBER_OF_STORES (2)
            * NUMBER_OF_INTERNAL_SLOTS (12)
            * NUMBER_OF_RAM_SLOTS (1)
            * NUMBER_OF_DIGITALS (8)
            * NUMBER_OF_I2C (1)
            * NUMBER_OF_POINTERS (4)
            * NUMBER_OF_TIMERS (8)
            * NUMBER_OF_APPS (4)
            * NUMBER_OF_UART (1)
            * NUMBER_OF_RAILS (3)
            * NUMBER_OF_SERVOS (8)
            * NUMBER_OF_SERVO_OUTPUTS (4)
            * NUMBER_OF_SERVO_INPUTS (4)
            * NUMBER_OF_SIGNALS (5)
            * NUMBER_OF_USB (1)
            * NUMBER_OF_USB_PORTS (4)
            * NUMBER_OF_PORTS (5)

            * aMTMIOSERIAL_USB_VBUS_ENABLED (0)
            * aMTMIOSERIAL_USB2_DATA_ENABLED (1)
            * aMTMIOSERIAL_USB_ERROR_FLAG (19)
            * aMTMIOSERIAL_USB2_BOOST_ENABLED (20)

            * aMTMIOSERIAL_ERROR_VBUS_OVERCURRENT (0)

    """

    BASE_ADDRESS = 8
    NUMBER_OF_STORES = 2
    NUMBER_OF_INTERNAL_SLOTS = 12
    NUMBER_OF_RAM_SLOTS = 1
    NUMBER_OF_DIGITALS = 8
    NUMBER_OF_I2C = 1
    NUMBER_OF_POINTERS = 2
    NUMBER_OF_TIMERS = 8
    NUMBER_OF_APPS = 4
    NUMBER_OF_UART = 4
    NUMBER_OF_RAILS = 3
    NUMBER_OF_SERVOS = 8
    NUMBER_OF_SERVO_OUTPUTS = 4
    NUMBER_OF_SERVO_INPUTS = 4
    NUMBER_OF_SIGNALS = 5
    NUMBER_OF_USB = 1
    NUMBER_OF_USB_PORTS = 4
    NUMBER_OF_PORTS = 5

    # Bit defines for port state UInt32
    # use brainstem.BIT(X) from aDefs.h to get bit value.
    # i.e if (state & brainstem.BIT(aMTMIOSERIAL_USB_VBUS_ENABLED))
    aMTMIOSERIAL_USB_VBUS_ENABLED = 0
    aMTMIOSERIAL_USB2_DATA_ENABLED = 1
    aMTMIOSERIAL_USB_ERROR_FLAG = 19
    aMTMIOSERIAL_USB2_BOOST_ENABLED = 20

    # Bit defines for port error UInt32
    # use brainstem.BIT(X) from aDefs.h to get bit value.
    # i.e if (error & brainstem.BIT(aMTMIOSERIAL_ERROR_VBUS_OVERCURRENT))
    aMTMIOSERIAL_ERROR_VBUS_OVERCURRENT = 0

    def __init__(self, address=BASE_ADDRESS, enable_auto_networking=True, model=defs.MODEL_MTM_IOSERIAL):
        super(MTMIOSerial, self).__init__(address, enable_auto_networking, model)
        self.system = System(self, 0)
        self.app = [App(self, i) for i in range(0, 4)]
        self.digital = [Digital(self, i) for i in range(0, 8)]
        self.i2c = [I2C(self, i) for i in range(0, 1)]
        self.pointer = [Pointer(self, i) for i in range(0, 4)]
        self.uart = [UART(self, i) for i in range(0, 4)]
        self.rail = [Rail(self, i) for i in range(0, 3)]
        self.store = [Store(self, i) for i in range(0, 2)]
        self.temperature = Temperature(self, 0)
        self.timer = [Timer(self, i) for i in range(0, 8)]
        self.hub = MTMIOSerial.Hub(self, 0)
        self.usb = USB(self, 0)
        self.servo = [RCServo(self, i) for i in range(0, 8)]
        self.signal = [Signal(self, i) for i in range(0, 5)]

    def connect(self, serial_number, **kwargs):
        return super(MTMIOSerial, self).connect(Spec.USB, serial_number)


    class Hub(USBSystem):
        def __init__(self, module, index):
            super(MTMIOSerial.Hub, self).__init__(module, index)
            self.port = [Port(module, i) for i in range(0, MTMIOSerial.NUMBER_OF_PORTS)]


class MTMLOAD1(Module):
    """ Concrete Module implementation for MTM-LOAD-1 module

        MTM-LOAD-1 modules contain contain the following entities:
            * system
            * app[0-3]
            * digital[0-3]
            * i2c[0]
            * pointer[0-3]
            * store[0-1]
            * timer[0-7]
            * rail[0]
            * temperature

        Useful Constants:
            * BASE_ADDRESS (14)
            * NUMBER_OF_STORES (2)
            * NUMBER_OF_INTERNAL_SLOTS (12)
            * NUMBER_OF_RAM_SLOTS (1)
            * NUMBER_OF_DIGITALS (2)
            * NUMBER_OF_I2C (1)
            * NUMBER_OF_POINTERS (4)
            * NUMBER_OF_TIMERS (8)
            * NUMBER_OF_APPS (4)
            * NUMBER_OF_RAILS (2)
            * NUMBER_OF_TEMPERATURES (1)
    """

    BASE_ADDRESS = 14
    NUMBER_OF_STORES = 2
    NUMBER_OF_INTERNAL_SLOTS = 12
    NUMBER_OF_RAM_SLOTS = 1
    NUMBER_OF_DIGITALS = 4
    NUMBER_OF_I2C = 1
    NUMBER_OF_POINTERS = 4
    NUMBER_OF_TIMERS = 8
    NUMBER_OF_APPS = 4
    NUMBER_OF_RAILS = 1
    NUMBER_OF_TEMPERATURES = 1

    def __init__(self, address=BASE_ADDRESS, enable_auto_networking=True, model=defs.MODEL_MTM_LOAD_1):
        super(MTMLOAD1, self).__init__(address, enable_auto_networking, model)
        self.system = System(self, 0)
        self.app = [App(self, i) for i in range(0, 4)]
        self.digital = [Digital(self, i) for i in range(0, 4)]
        self.i2c = [I2C(self, i) for i in range(0, 1)]
        self.pointer = [Pointer(self, i) for i in range(0, 4)]
        self.rail = [Rail(self, i) for i in range(0, 1)]
        self.store = [Store(self, i) for i in range(0, 2)]
        self.timer = [Timer(self, i) for i in range(0, 8)]
        self.temperature = Temperature(self, 0)

    def connect(self, serial_number, **kwargs):
        return super(MTMLOAD1, self).connect(Spec.USB, serial_number)


class MTMPM1(Module):
    """ Concrete Module implementation for MTM-PM-1 module

        MTM-PM-1 modules contain contain the following entities:
            * system
            * app[0-3]
            * digital[0-1]
            * i2c[0]
            * pointer[0-3]
            * store[0-1]
            * timer[0-7]
            * rail[0-1]
            * temperature

        Useful Constants:
            * BASE_ADDRESS (6)
            * NUMBER_OF_STORES (2)
            * NUMBER_OF_INTERNAL_SLOTS (12)
            * NUMBER_OF_RAM_SLOTS (1)
            * NUMBER_OF_DIGITALS (2)
            * NUMBER_OF_I2C (1)
            * NUMBER_OF_POINTERS (4)
            * NUMBER_OF_TIMERS (8)
            * NUMBER_OF_APPS (4)
            * NUMBER_OF_RAILS (2)
            * NUMBER_OF_TEMPERATURES (1)
    """

    BASE_ADDRESS = 6
    NUMBER_OF_STORES = 2
    NUMBER_OF_INTERNAL_SLOTS = 12
    NUMBER_OF_RAM_SLOTS = 1
    NUMBER_OF_DIGITALS = 2
    NUMBER_OF_I2C = 1
    NUMBER_OF_POINTERS = 4
    NUMBER_OF_TIMERS = 8
    NUMBER_OF_APPS = 4
    NUMBER_OF_RAILS = 2
    NUMBER_OF_TEMPERATURES = 1

    def __init__(self, address=BASE_ADDRESS, enable_auto_networking=True, model=defs.MODEL_MTM_PM_1):
        super(MTMPM1, self).__init__(address, enable_auto_networking, model)
        self.system = System(self, 0)
        self.app = [App(self, i) for i in range(0, 4)]
        self.digital = [Digital(self, i) for i in range(0, 2)]
        self.i2c = [I2C(self, i) for i in range(0, 1)]
        self.pointer = [Pointer(self, i) for i in range(0, 4)]
        self.rail = [Rail(self, i) for i in range(0, 2)]
        self.store = [Store(self, i) for i in range(0, 2)]
        self.timer = [Timer(self, i) for i in range(0, 8)]
        self.temperature = Temperature(self, 0)

    def connect(self, serial_number, **kwargs):
        return super(MTMPM1, self).connect(Spec.USB, serial_number)


class MTMRelay(Module):
    """ Concrete Module implementation for MTM-RELAY module

        MTM-RELAY modules contain contain the following entities:
            * system
            * app[0-3]
            * digital[0-3]
            * i2c[0]
            * pointer[0-3]
            * store[0-1]
            * timer[0-7]
            * relay[0-3]
            * temperature

        Useful Constants:
            * BASE_ADDRESS (12)
            * NUMBER_OF_STORES (2)
            * NUMBER_OF_INTERNAL_SLOTS (12)
            * NUMBER_OF_RAM_SLOTS (1)
            * NUMBER_OF_DIGITALS (4)
            * NUMBER_OF_I2C (1)
            * NUMBER_OF_POINTERS (4)
            * NUMBER_OF_TIMERS (8)
            * NUMBER_OF_APPS (4)
            * NUMBER_OF_RELAYS (4)
    """

    BASE_ADDRESS = 12
    NUMBER_OF_STORES = 2
    NUMBER_OF_INTERNAL_SLOTS = 12
    NUMBER_OF_RAM_SLOTS = 1
    NUMBER_OF_DIGITALS = 4
    NUMBER_OF_I2C = 1
    NUMBER_OF_POINTERS = 4
    NUMBER_OF_TIMERS = 8
    NUMBER_OF_APPS = 4
    NUMBER_OF_RELAYS = 4

    def __init__(self, address=BASE_ADDRESS, enable_auto_networking=True, model=defs.MODEL_MTM_RELAY):
        super(MTMRelay, self).__init__(address, enable_auto_networking, model)
        self.system = System(self, 0)
        self.app = [App(self, i) for i in range(0, 4)]
        self.digital = [Digital(self, i) for i in range(0, 4)]
        self.i2c = [I2C(self, i) for i in range(0, 1)]
        self.pointer = [Pointer(self, i) for i in range(0, 4)]
        self.relay = [Relay(self, i) for i in range(0, 4)]
        self.store = [Store(self, i) for i in range(0, 2)]
        self.timer = [Timer(self, i) for i in range(0, 8)]

    def connect(self, serial_number, **kwargs):
        return super(MTMRelay, self).connect(Spec.USB, serial_number)


class MTMUSBStem(Module):
    """ Concrete Module implementation for MTM USBStem modules

        MTMUSBStem modules contain the following entities:
            * system
            * analog[0-3]
            * app[0-3]
            * clock
            * digital[0-14]
            * i2c[0-1]
            * pointer[0-3]
            * servo[0-7]
            * signal[0-4]
            * store[0-2]
            * timer[0-7]

        Useful Constants:
            * BASE_ADDRESS (4)
            * NUMBER_OF_STORES (3)
            * NUMBER_OF_INTERNAL_SLOTS (12)
            * NUMBER_OF_RAM_SLOTS (1)
            * NUMBER_OF_SD_SLOTS (255)
            * NUMBER_OF_ANALOGS (4)
            * DAC_ANALOG_INDEX (3)
            * FIXED_DAC_ANALOG (True)
            * NUMBER_OF_DIGITALS (15)
            * NUMBER_OF_I2C (2)
            * NUMBER_OF_POINTERS (4)
            * NUMBER_OF_TIMERS (8)
            * NUMBER_OF_APPS (4)
            * NUMBER_OF_SERVOS (8)
            * NUMBER_OF_SERVO_OUTPUTS (4)
            * NUMBER_OF_SERVO_INPUTS (4)
            * NUMBER_OF_SIGNALS (5)
            * ANALOG_BULK_CAPTURE_MAX_HZ (200000)
            * ANALOG_BULK_CAPTURE_MIN_HZ (7000)

    """

    BASE_ADDRESS = 4
    NUMBER_OF_STORES = 3
    NUMBER_OF_INTERNAL_SLOTS = 12
    NUMBER_OF_RAM_SLOTS = 1
    NUMBER_OF_SD_SLOTS = 255
    NUMBER_OF_ANALOGS = 4
    DAC_ANALOG_INDEX = 3
    FIXED_DAC_ANALOG = True
    NUMBER_OF_DIGITALS = 15
    NUMBER_OF_I2C = 2
    NUMBER_OF_POINTERS = 4
    NUMBER_OF_TIMERS = 8
    NUMBER_OF_APPS = 4
    NUMBER_OF_SERVOS = 8
    NUMBER_OF_SERVO_OUTPUTS = 4
    NUMBER_OF_SERVO_INPUTS = 4
    NUMBER_OF_SIGNALS = 5
    ANALOG_BULK_CAPTURE_MAX_HZ = 200000
    ANALOG_BULK_CAPTURE_MIN_HZ = 7000

    def __init__(self, address=BASE_ADDRESS, enable_auto_networking=True, model=defs.MODEL_MTM_USBSTEM):
        super(MTMUSBStem, self).__init__(address, enable_auto_networking, model)
        self.system = System(self, 0)
        self.analog = [Analog(self, i) for i in range(0, 4)]
        self.app = [App(self, i) for i in range(0, 4)]
        self.clock = Clock(self, 0)
        self.digital = [Digital(self, i) for i in range(0, 15)]
        self.i2c = [I2C(self, i) for i in range(0, 2)]
        self.pointer = [Pointer(self, i) for i in range(0, 4)]
        self.store = [Store(self, i) for i in range(0, 3)]
        self.timer = [Timer(self, i) for i in range(0, 8)]
        self.servo = [RCServo(self, i) for i in range(0, 8)]
        self.signal = [Signal(self, i) for i in range(0, 5)]

    def connect(self, serial_number, **kwargs):
        return super(MTMUSBStem, self).connect(Spec.USB, serial_number)



class PD3M(Module):
    """ Concrete Module implementation for the PD3M.

        The module contains the USB entity as well as the following.

        Entities:
            * system
            * pd
            * port

        Useful Constants:
            * BASE_ADDRESS (18)
            * NUMBER_OF_PORTS (3)
            * NUMBER_OF_PD_PORTS (12)
            * NUMBER_OF_PD_RULES_PER_PORT (1)

    """

    BASE_ADDRESS = 18
    NUMBER_OF_PORTS = 1
    NUMBER_OF_PD_PORTS = 1
    NUMBER_OF_PD_RULES_PER_PORT = 7
    
    def __init__(self, address=BASE_ADDRESS, enable_auto_networking=True, model=defs.MODEL_PD3M):
        super(PD3M, self).__init__(address, enable_auto_networking, model)
        self.system = System(self, 0)
        self.pd = PowerDelivery(self, 0)
        self.port = Port(self, 0)


    def connect(self, serial_number, **kwargs):
        return super(PD3M, self).connect(Spec.USB, serial_number)



class USBCSwitch(Module):
    """ Concrete Module implementation for the USBC-Switch.

        The module contains the USB entity as well as the following.

        Entities:
            * system
            * app[0-3]
            * pointer[0-3]
            * usb
            * mux
            * store[0-1]
            * timer[0-7]
            * equalizer[0-1]

        Useful Constants:
            * BASE_ADDRESS (6)
            * NUMBER_OF_STORES (3)
            * NUMBER_OF_INTERNAL_SLOTS (12)
            * NUMBER_OF_RAM_SLOTS (1)
            * NUMBER_OF_TIMERS (8)
            * NUMBER_OF_APPS (4)
            * NUMBER_OF_POINTERS (4)
            * NUMBER_OF_USB (1)
            * NUMBER_OF_MUXS  (1)
            * NUMBER_OF_EQUALIZERS (2)

            Bit defines for port state UInt32
            use brainstem.BIT(X) from aDefs.h to get bit value.
            i.e if (state & brainstem.BIT(usbPortStateVBUS))

            * usbPortStateVBUS (0)
            * usbPortStateHiSpeed (1)
            * usbPortStateSBU (2)
            * usbPortStateSS1 (3)
            * usbPortStateSS2 (4)
            * usbPortStateCC1 5)
            * usbPortStateCC2 (6)
            * usbPortStateCCFlip (13)
            * usbPortStateSSFlip (14)
            * usbPortStateSBUFlip (15)
            * usbPortStateErrorFlag (19)
            * usbPortStateUSB2Boost (20)
            * usbPortStateUSB3Boost (21)
            * usbPortStateConnectionEstablished (22)
            * usbPortStateCC1Inject (26)
            * usbPortStateCC2Inject (27)
            * usbPortStateCC1Detect (28)
            * usbPortStateCC2Detect (29)
            * usbPortStateCC1LogicState (30)
            * usbPortStateCC2LogicState 31)

            * usbPortStateOff (0)
            * usbPortStateSideA (1)
            * usbPortStateSideB (2)
            * usbPortStateSideUndefined (3)

            * TRANSMITTER_2P0_40mV (0)
            * TRANSMITTER_2P0_60mV (1)
            * TRANSMITTER_2P0_80mV (2)
            * TRANSMITTER_2P0_0mV (3)

            * MUX_1db_COM_0db_900mV (0)
            * MUX_0db_COM_1db_900mV (1)
            * MUX_1db_COM_1db_900mV (2)
            * MUX_0db_COM_0db_900mV (3)
            * MUX_0db_COM_0db_1100mV (4)
            * MUX_1db_COM_0db_1100mV (5)
            * MUX_0db_COM_1db_1100mV (6)
            * MUX_2db_COM_2db_1100mV (7)
            * MUX_0db_COM_0db_1300mV (8)

            * LEVEL_1_2P0 (0)
            * LEVEL_2_2P0 (1)

            * LEVEL_1_3P0 (0)
            * LEVEL_2_3P0 (1)
            * LEVEL_3_3P0 (2)
            * LEVEL_4_3P0 (3)
            * LEVEL_5_3P0 (4)
            * LEVEL_6_3P0 (5)
            * LEVEL_7_3P0 (6)
            * LEVEL_8_3P0 (7)
            * LEVEL_9_3P0 (8)
            * LEVEL_10_3P0 (9)
            * LEVEL_11_3P0 (10)
            * LEVEL_12_3P0 (11)
            * LEVEL_13_3P0 (12)
            * LEVEL_14_3P0 (13)
            * LEVEL_15_3P0 (14)
            * LEVEL_16_3P0 (15)

            * EQUALIZER_CHANNEL_BOTH (0)
            * EQUALIZER_CHANNEL_MUX (1)
            * EQUALIZER_CHANNEL_COMMON (2)

            * NO_DAUGHTERCARD (0)
            * PASSIVE_DAUGHTERCARD (1)
            * REDRIVER_DAUGHTERCARD (2)
            * UNKNOWN_DAUGHTERCARD (3)
    """

    BASE_ADDRESS = 6
    NUMBER_OF_STORES = 2
    NUMBER_OF_INTERNAL_SLOTS = 12
    NUMBER_OF_RAM_SLOTS = 1
    NUMBER_OF_TIMERS = 8
    NUMBER_OF_APPS = 4
    NUMBER_OF_POINTERS = 4
    NUMBER_OF_USB = 1
    NUMBER_OF_MUXS = 1
    NUMBER_OF_EQUALIZERS = 2

    # Bit defines for port state UInt32
    # use brainstem.BIT(X) from aDefs.h to get bit value.
    # i.e if (state & brainstem.BIT(usbPortStateVBUS))
    usbPortStateVBUS = 0
    usbPortStateHiSpeed = 1
    usbPortStateSBU = 2
    usbPortStateSS1 = 3
    usbPortStateSS2 = 4
    usbPortStateCC1 = 5
    usbPortStateCC2 = 6
    usbPortStateCCFlip = 13
    usbPortStateSSFlip = 14
    usbPortStateSBUFlip = 15
    usbPortStateErrorFlag = 19
    usbPortStateUSB2Boost = 20
    usbPortStateUSB3Boost = 21
    usbPortStateConnectionEstablished = 22
    usbPortStateCC1Inject = 26
    usbPortStateCC2Inject = 27
    usbPortStateCC1Detect = 28
    usbPortStateCC2Detect = 29
    usbPortStateCC1LogicState = 30
    usbPortStateCC2LogicState = 31

    # State defines for 2 bit orientation state elements.
    usbPortStateOff = 0
    usbPortStateSideA = 1
    usbPortStateSideB = 2
    usbPortStateSideUndefined = 3

    #2.0 Equalizer Transmitter defines
    TRANSMITTER_2P0_40mV = 0
    TRANSMITTER_2P0_60mV = 1
    TRANSMITTER_2P0_80mV = 2
    TRANSMITTER_2P0_0mV = 3

    #3.0 Equalizer Transmitter defines.
    MUX_1db_COM_0db_900mV = 0
    MUX_0db_COM_1db_900mV = 1
    MUX_1db_COM_1db_900mV = 2
    MUX_0db_COM_0db_900mV = 3
    MUX_0db_COM_0db_1100mV = 4
    MUX_1db_COM_0db_1100mV = 5
    MUX_0db_COM_1db_1100mV = 6
    MUX_2db_COM_2db_1100mV = 7
    MUX_0db_COM_0db_1300mV = 8

    #2.0 Equalizer Receiver defines.
    LEVEL_1_2P0 = 0
    LEVEL_2_2P0 = 1

    # 3.0 Equalizer Receiver defines.
    LEVEL_1_3P0 = 0
    LEVEL_2_3P0 = 1
    LEVEL_3_3P0 = 2
    LEVEL_4_3P0 = 3
    LEVEL_5_3P0 = 4
    LEVEL_6_3P0 = 5
    LEVEL_7_3P0 = 6
    LEVEL_8_3P0 = 7
    LEVEL_9_3P0 = 8
    LEVEL_10_3P0 = 9
    LEVEL_11_3P0 = 10
    LEVEL_12_3P0 = 11
    LEVEL_13_3P0 = 12
    LEVEL_14_3P0 = 13
    LEVEL_15_3P0 = 14
    LEVEL_16_3P0 = 15

    #Equalizer Channels
    EQUALIZER_CHANNEL_BOTH = 0
    EQUALIZER_CHANNEL_MUX = 1
    EQUALIZER_CHANNEL_COMMON = 2

    #Daughter Card Types:
    NO_DAUGHTERCARD = 0
    PASSIVE_DAUGHTERCARD = 1
    REDRIVER_DAUGHTERCARD = 2
    UNKNOWN_DAUGHTERCARD = 3

    def __init__(self, address=BASE_ADDRESS, enable_auto_networking=True, model=defs.MODEL_USB_C_SWITCH):
        super(USBCSwitch, self).__init__(address, enable_auto_networking, model)
        self.system = System(self, 0)
        self.app = [App(self, i) for i in range(0, 4)]
        self.pointer = [Pointer(self, i) for i in range(0, 4)]
        self.usb = USB(self, 0)
        self.store = [Store(self, i) for i in range(0, 2)]
        self.timer = [Timer(self, i) for i in range(0, 8)]
        self.mux = Mux(self, 0)
        self.equalizer = [Equalizer(self, i) for i in range(0, 2)]

    def connect(self, serial_number, **kwargs):
        return super(USBCSwitch, self).connect(Spec.USB, serial_number)

    @staticmethod
    def set_usbPortStateCOM_ORIENT_STATUS(var, state):
        return (var & ~(3 << 7)) | (state << 7)

    @staticmethod
    def get_usbPortStateCOM_ORIENT_STATUS(var):
        return (var & (3 << 7)) >> 7

    @staticmethod
    def set_usbPortStateMUX_ORIENT_STATUS(var, state):
        return (var & ~(3 << 9)) | (state << 9)

    @staticmethod
    def get_usbPortStateMUX_ORIENT_STATUS(var):
        return (var & (3 << 9)) >> 9

    @staticmethod
    def set_usbPortStateSPEED_STATUS(var, state):
        return (var & ~(3 << 11)) | (state << 11)

    @staticmethod
    def get_usbPortStateSPEED_STATUS(var):
        return (var & (3 << 11)) >> 11

    @staticmethod
    def get_usbPortStateDaughterCard(var):
        return (var & (3 << 18)) >> 18


class USBCSwitchPro(Module):
    """ Concrete Module implementation for the USBCSwitchPro.

        The module contains the USB entity as well as the following.

        Entities:
            * system
            * app[0-3]
            * pointer[0-3]
            * pd[0-5]
            * rail[0]
            * store[0-2]
            * temperature[0-4]
            * timer[0-7]
            * i2c[0]
            * usb
            * uart[0-1]
            * port[0-5]
            * mux
            * equalizer[0-1]

        Useful Constants:
            * BASE_ADDRESS (16)
            * NUMBER_OF_STORES (3)
            * NUMBER_OF_INTERNAL_SLOTS (12)
            * NUMBER_OF_RAM_SLOTS (1)
            * NUMBER_OF_TEMPERATURES (5)
            * NUMBER_OF_TIMERS (8)
            * NUMBER_OF_APPS (4)
            * NUMBER_OF_POINTERS (4)
            * NUMBER_OF_USB (1)
            * NUMBER_OF_UARTS (2)
            * NUMBER_OF_MUXS  (1)
            * NUMBER_OF_EQUALIZERS (2)

            Bit defines for port state UInt32
            use brainstem.BIT(X) from aDefs.h to get bit value.
            i.e if (state & brainstem.BIT(usbPortStateVBUS))

            * usbPortStateVBUS (0)
            * usbPortStateHiSpeed (1)
            * usbPortStateSBU (2)
            * usbPortStateSS1 (3)
            * usbPortStateSS2 (4)
            * usbPortStateCC1 5)
            * usbPortStateCC2 (6)
            * usbPortStateCCFlip (13)
            * usbPortStateSSFlip (14)
            * usbPortStateSBUFlip (15)
            * usbPortStateErrorFlag (19)
            * usbPortStateUSB2Boost (20)
            * usbPortStateUSB3Boost (21)
            * usbPortStateConnectionEstablished (22)
            * usbPortStateCC1Inject (26)
            * usbPortStateCC2Inject (27)
            * usbPortStateCC1Detect (28)
            * usbPortStateCC2Detect (29)
            * usbPortStateCC1LogicState (30)
            * usbPortStateCC2LogicState 31)

            * usbPortStateOff (0)
            * usbPortStateSideA (1)
            * usbPortStateSideB (2)
            * usbPortStateSideUndefined (3)

            * TRANSMITTER_2P0_40mV (0)
            * TRANSMITTER_2P0_60mV (1)
            * TRANSMITTER_2P0_80mV (2)
            * TRANSMITTER_2P0_0mV (3)

            * MUX_1db_COM_0db_900mV (0)
            * MUX_0db_COM_1db_900mV (1)
            * MUX_1db_COM_1db_900mV (2)
            * MUX_0db_COM_0db_900mV (3)
            * MUX_0db_COM_0db_1100mV (4)
            * MUX_1db_COM_0db_1100mV (5)
            * MUX_0db_COM_1db_1100mV (6)
            * MUX_2db_COM_2db_1100mV (7)
            * MUX_0db_COM_0db_1300mV (8)

            * LEVEL_1_2P0 (0)
            * LEVEL_2_2P0 (1)

            * LEVEL_1_3P0 (0)
            * LEVEL_2_3P0 (1)
            * LEVEL_3_3P0 (2)
            * LEVEL_4_3P0 (3)
            * LEVEL_5_3P0 (4)
            * LEVEL_6_3P0 (5)
            * LEVEL_7_3P0 (6)
            * LEVEL_8_3P0 (7)
            * LEVEL_9_3P0 (8)
            * LEVEL_10_3P0 (9)
            * LEVEL_11_3P0 (10)
            * LEVEL_12_3P0 (11)
            * LEVEL_13_3P0 (12)
            * LEVEL_14_3P0 (13)
            * LEVEL_15_3P0 (14)
            * LEVEL_16_3P0 (15)

            * EQUALIZER_CHANNEL_BOTH (0)
            * EQUALIZER_CHANNEL_MUX (1)
            * EQUALIZER_CHANNEL_COMMON (2)

            * NO_DAUGHTERCARD (0)
            * PASSIVE_DAUGHTERCARD (1)
            * REDRIVER_DAUGHTERCARD (2)
            * UNKNOWN_DAUGHTERCARD (3)
    """

    BASE_ADDRESS = 16
    NUMBER_OF_APPS = 4
    NUMBER_OF_POINTERS = 4
    NUMBER_OF_STORES = 3
    # TODO: Are these right?
    NUMBER_OF_INTERNAL_SLOTS = 12
    NUMBER_OF_RAM_SLOTS = 1
    NUMBER_OF_EEPROM_SLOTS = 8
    NUMBER_OF_TEMPERATURES = 5
    NUMBER_OF_TIMERS = 8
    NUMBER_OF_USB = 1
    NUMBER_OF_USB_PORTS = 6
    NUMBER_OF_PORTS = 6
    NUMBER_OF_POWER_DELIVERY_PORTS = 7
    NUMBER_OF_RAILS = 1
    NUMBER_OF_I2CS = 1
    NUMBER_OF_UARTS = 2
    NUMBER_OF_MUXS = 1
    NUMBER_OF_EQUALIZERS = 2

    # Bit defines for port state UInt32
    # use brainstem.BIT(X) from aDefs.h to get bit value.
    # i.e if (state & brainstem.BIT(usbPortStateVBUS))
    usbPortStateVBUS = 0
    usbPortStateHiSpeed = 1
    usbPortStateSBU = 2
    usbPortStateSS1 = 3
    usbPortStateSS2 = 4
    usbPortStateCC1 = 5
    usbPortStateCC2 = 6
    usbPortStateCCFlip = 13
    usbPortStateSSFlip = 14
    usbPortStateSBUFlip = 15
    usbPortStateErrorFlag = 19
    usbPortStateUSB2Boost = 20
    usbPortStateUSB3Boost = 21
    usbPortStateConnectionEstablished = 22
    usbPortStateCC1Inject = 26
    usbPortStateCC2Inject = 27
    usbPortStateCC1Detect = 28
    usbPortStateCC2Detect = 29
    usbPortStateCC1LogicState = 30
    usbPortStateCC2LogicState = 31

    # State defines for 2 bit orientation state elements.
    usbPortStateOff = 0
    usbPortStateSideA = 1
    usbPortStateSideB = 2
    usbPortStateSideUndefined = 3

    #2.0 Equalizer Transmitter defines
    TRANSMITTER_2P0_40mV = 0
    TRANSMITTER_2P0_60mV = 1
    TRANSMITTER_2P0_80mV = 2
    TRANSMITTER_2P0_0mV = 3

    #3.0 Equalizer Transmitter defines.
    MUX_1db_COM_0db_900mV = 0
    MUX_0db_COM_1db_900mV = 1
    MUX_1db_COM_1db_900mV = 2
    MUX_0db_COM_0db_900mV = 3
    MUX_0db_COM_0db_1100mV = 4
    MUX_1db_COM_0db_1100mV = 5
    MUX_0db_COM_1db_1100mV = 6
    MUX_2db_COM_2db_1100mV = 7
    MUX_0db_COM_0db_1300mV = 8

    #2.0 Equalizer Receiver defines.
    LEVEL_1_2P0 = 0
    LEVEL_2_2P0 = 1

    # 3.0 Equalizer Receiver defines.
    LEVEL_1_3P0 = 0
    LEVEL_2_3P0 = 1
    LEVEL_3_3P0 = 2
    LEVEL_4_3P0 = 3
    LEVEL_5_3P0 = 4
    LEVEL_6_3P0 = 5
    LEVEL_7_3P0 = 6
    LEVEL_8_3P0 = 7
    LEVEL_9_3P0 = 8
    LEVEL_10_3P0 = 9
    LEVEL_11_3P0 = 10
    LEVEL_12_3P0 = 11
    LEVEL_13_3P0 = 12
    LEVEL_14_3P0 = 13
    LEVEL_15_3P0 = 14
    LEVEL_16_3P0 = 15

    #Equalizer Channels
    EQUALIZER_CHANNEL_BOTH = 0
    EQUALIZER_CHANNEL_MUX = 1
    EQUALIZER_CHANNEL_COMMON = 2

    #Daughter Card Types:
    NO_DAUGHTERCARD = 0
    PASSIVE_DAUGHTERCARD = 1
    REDRIVER_DAUGHTERCARD = 2
    UNKNOWN_DAUGHTERCARD = 3

    def __init__(self, address=BASE_ADDRESS, enable_auto_networking=True, model=defs.MODEL_USB_C_SWITCH_PRO):
        super(USBCSwitchPro, self).__init__(address, enable_auto_networking, model)
        self.system = System(self, 0)
        self.app = [App(self, i) for i in range(0, USBCSwitchPro.NUMBER_OF_APPS)]
        self.pointer = [Pointer(self, i) for i in range(0, USBCSwitchPro.NUMBER_OF_POINTERS)]
        self.store = [Store(self, Store.INTERNAL_STORE),
                      Store(self, Store.RAM_STORE),
                      Store(self, Store.EEPROM_STORE)]
        self.temperature = [Temperature(self, i) for i in range(0, USBCSwitchPro.NUMBER_OF_TEMPERATURES)]
        self.timer = [Timer(self, i) for i in range(0, USBCSwitchPro.NUMBER_OF_TIMERS)]
        self.rail = [Rail(self, i) for i in range(0, USBCSwitchPro.NUMBER_OF_RAILS)]
        #self.pd = [PowerDelivery(self, i) for i in range(0, USBCSwitchPro.NUMBER_OF_POWER_DELIVERY_PORTS)]
        self.i2c = [I2C(self, i) for i in range(0, USBCSwitchPro.NUMBER_OF_I2CS)]
        self.usb = USB(self, 0)
        self.uart = [UART(self, i) for i in range(0, USBCSwitchPro.NUMBER_OF_UARTS)]
        self.mux = Mux(self, 0)
        self.equalizer = [Equalizer(self, i) for i in range(0, USBCSwitchPro.NUMBER_OF_EQUALIZERS)]
        self.port = [Port(self, i) for i in range(0, USBCSwitchPro.NUMBER_OF_PORTS)]
        self.ethernet = Ethernet(self, 0)

    def connect(self, serial_number, **kwargs):
        return super(USBCSwitchPro, self).connect(Spec.USB, serial_number)

class USBHub2x4(Module):
    """ Concrete Module implementation for the USBHub2x4.

        The module contains the USB entity as well as the following.

        Entities:
            * system
            * app[0-3]
            * pointer[0-3]
            * usb
            * mux
            * store[0-1]
            * temperature
            * timer[0-7]

        Useful Constants:
            * BASE_ADDRESS (6)
            * NUMBER_OF_STORES (3)
            * NUMBER_OF_INTERNAL_SLOTS (12)
            * NUMBER_OF_RAM_SLOTS (1)
            * NUMBER_OF_TIMERS (8)
            * NUMBER_OF_APPS (4)
            * NUMBER_OF_POINTERS (4)
            * NUMBER_OF_DOWNSTREAM_USB (4)
            * NUMBER_OF_UPSTREAM_USB (2)
            * NUMBER_OF_PORTS (6)

            Bit defines for port error UInt32
            use brainstem.BIT(X) from aDefs.h to get bit value.
            i.e if (error & brainstem.BIT(aUSBHUB2X4_USB_VBUS_ENABLED))

            * aUSBHUB2X4_USB_VBUS_ENABLED (0)
            * aUSBHUB2X4_USB2_DATA_ENABLED (1)
            * aUSBHUB2X4_USB_ERROR_FLAG (19)
            * aUSBHUB2X4_USB2_BOOST_ENABLED (20)
            * aUSBHUB2X4_DEVICE_ATTACHED (23)
            * aUSBHUB2X4_CONSTANT_CURRENT (24)

            Bit defines for port error UInt32
            use brainstem.BIT(X) from aDefs.h to get bit value.
            i.e if (error & brainstem.BIT(aUSBHUB3P_ERROR_VBUS_OVERCURRENT))

            * aUSBHUB2X4_ERROR_VBUS_OVERCURRENT (0)
            * aUSBHUB2X4_ERROR_OVER_TEMPERATURE (3)
            * aUSBHub2X4_ERROR_DISCHARGE (4)
    """

    BASE_ADDRESS = 6
    NUMBER_OF_STORES = 2
    NUMBER_OF_INTERNAL_SLOTS = 12
    NUMBER_OF_RAM_SLOTS = 1
    NUMBER_OF_TIMERS = 8
    NUMBER_OF_APPS = 4
    NUMBER_OF_POINTERS = 4
    NUMBER_OF_DOWNSTREAM_USB = 4
    NUMBER_OF_UPSTREAM_USB = 2
    NUMBER_OF_PORTS = 6

    # Bit defines for port state UInt32
    # use brainstem.BIT(X) from aDefs.h to get bit value.
    # i.e if (state & brainstem.BIT(aUSBHUB2X4_USB_VBUS_ENABLED))
    aUSBHUB2X4_USB_VBUS_ENABLED = 0
    aUSBHUB2X4_USB2_DATA_ENABLED = 1
    aUSBHUB2X4_USB_ERROR_FLAG = 19
    aUSBHUB2X4_USB2_BOOST_ENABLED = 20
    aUSBHUB2X4_DEVICE_ATTACHED = 23
    aUSBHUB2X4_CONSTANT_CURRENT = 24

    # Bit defines for port error UInt32
    # use brainstem.BIT(X) from aDefs.h to get bit value.
    # i.e if (error & brainstem.BIT(aUSBHUB2X4_ERROR_VBUS_OVERCURRENT))
    aUSBHUB2X4_ERROR_VBUS_OVERCURRENT = 0
    aUSBHUB2X4_ERROR_OVER_TEMPERATURE = 3
    aUSBHub2X4_ERROR_DISCHARGE = 4

    def __init__(self, address=BASE_ADDRESS, enable_auto_networking=True, model=defs.MODEL_USBHUB_2X4):
        super(USBHub2x4, self).__init__(address, enable_auto_networking, model)
        self.system = System(self, 0)
        self.app = [App(self, i) for i in range(0, 4)]
        self.pointer = [Pointer(self, i) for i in range(0, 4)]
        self.hub = USBHub2x4.Hub(self, 0)
        self.usb = USB(self, 0)
        self.store = [Store(self, i) for i in range(0, 2)]
        self.temperature = Temperature(self, 0)
        self.timer = [Timer(self, i) for i in range(0, 8)]

    def connect(self, serial_number, **kwargs):
        return super(USBHub2x4, self).connect(Spec.USB, serial_number)


    class Hub(USBSystem):
        def __init__(self, module, index):
            super(USBHub2x4.Hub, self).__init__(module, index)
            self.port = [Port(module, i) for i in range(0, USBHub2x4.NUMBER_OF_PORTS)]


class USBHub3c(Module):
    """ Concrete Module implementation for the USBHub3c.

        The module contains the USB entity as well as the following.

        Entities:
            * system
            * app[0-3]
            * pointers[0-3]
            * store[0-2]
            * temperature[0-2]
            * timer[0-7]
            * hub
            * hub.port[0-7]
            * rail[0-6]
            * pd[0-7]
            * usb
            * uart[0-1]

        Useful Constants:
            * BASE_ADDRESS (6)
            * NUMBER_OF_STORES (2)
            * NUMBER_OF_INTERNAL_SLOTS (12)
            * NUMBER_OF_RAM_SLOTS (1)
            * NUMBER_OF_TIMERS (8)
            * NUMBER_OF_APPS (4)
            * NUMBER_OF_POINTERS (4)
            * NUMBER_OF_USB_PORTS (8)
            * NUMBER_OF_UARTS (2)
            * NUMBER_OF_RAILS (7)
            * STORE_INTERNAL_INDEX (0)
            * STORE_RAM_INDEX (1)
            * STORE_EEPROM_INDEX (2)
            * PORT_ID_CONTROL_INDEX (6)
            * PORT_ID_POWER_C_INDEX (7)
            * NUMBER_OF_PORTS (8)


    """

    BASE_ADDRESS = 6
    NUMBER_OF_STORES = 3
    NUMBER_OF_INTERNAL_SLOTS = 12
    NUMBER_OF_RAM_SLOTS = 1
    NUMBER_OF_TEMPERATURES = 3
    NUMBER_OF_TIMERS = 8
    NUMBER_OF_APPS = 4
    NUMBER_OF_POINTERS = 4
    NUMBER_OF_USB_PORTS = 8
    NUMBER_OF_UARTS = 2
    NUMBER_OF_RAILS = 7
    NUMBER_OF_POWER_DELIVERY_PORTS = 8
    NUMBER_OF_I2C = 1
    STORE_INTERNAL_INDEX = 0
    STORE_RAM_INDEX = 1
    STORE_EEPROM_INDEX = 2
    PORT_ID_CONTROL_INDEX = 6
    PORT_ID_POWER_C_INDEX = 7
    NUMBER_OF_PORTS = 8


    def __init__(self, address=BASE_ADDRESS, enable_auto_networking=True, model=defs.MODEL_USBHUB_3C):
        super(USBHub3c, self).__init__(address, enable_auto_networking, model)
        self.system = System(self, 0)
        self.app = [App(self, i) for i in range(0, USBHub3c.NUMBER_OF_APPS)]
        self.pointer = [Pointer(self, i) for i in range(0, USBHub3c.NUMBER_OF_POINTERS)]
        self.store = [Store(self, _BS_C.storeInternalStore),
                      Store(self, _BS_C.storeRAMStore),
                      Store(self, _BS_C.storeEEPROMStore)]
        self.temperature = [Temperature(self, i) for i in range(0, USBHub3c.NUMBER_OF_TEMPERATURES)]
        self.timer = [Timer(self, i) for i in range(0, USBHub3c.NUMBER_OF_TIMERS)]
        self.hub = USBHub3c.Hub(self, 0)
        self.rail = [Rail(self, i) for i in range(0, USBHub3c.NUMBER_OF_RAILS)]
        self.pd = [PowerDelivery(self, i) for i in range(0, USBHub3c.NUMBER_OF_POWER_DELIVERY_PORTS)]
        self.i2c = [I2C(self, i) for i in range(0, USBHub3c.NUMBER_OF_I2C)]
        """ usb entity adds minimal legacy support """
        self.usb = USB(self, 0)
        self.uart = [UART(self, i) for i in range(0, USBHub3c.NUMBER_OF_UARTS)]

    def connect(self, serial_number, **kwargs):
        return super(USBHub3c, self).connect(Spec.USB, serial_number)


    class Hub(USBSystem):
        def __init__(self, module, index):
            super(USBHub3c.Hub, self).__init__(module, index)
            self.port = [Port(module, i) for i in range(0, USBHub3c.NUMBER_OF_USB_PORTS)]


class USBHub3p(Module):
    """ Concrete Module implementation for the USBHub3p.

        The module contains the USB entity as well as the following.

        Entities:
            * system
            * app[0-3]
            * pointers[0-3]
            * usb
            * store[0-1]
            * temperature
            * timer[0-7]

        Useful Constants:
            * BASE_ADDRESS (6)
            * NUMBER_OF_STORES (2)
            * NUMBER_OF_INTERNAL_SLOTS (12)
            * NUMBER_OF_RAM_SLOTS (1)
            * NUMBER_OF_TIMERS (8)
            * NUMBER_OF_APPS (4)
            * NUMBER_OF_POINTERS (4)
            * NUMBER_OF_DOWNSTREAM_USB (8)
            * NUMBER_OF_UPSTREAM_USB (2)
            * NUMBER_OF_PORTS (12)

            Bit defines for port state UInt32
            use brainstem.BIT(X) from aDefs.h to get bit value.
            i.e if (state & brainstem.BIT(aUSBHUB3P_USB_VBUS_ENABLED))

            * aUSBHUB3P_USB_VBUS_ENABLED (0)
            * aUSBHUB3P_USB2_DATA_ENABLED (1)
            * aUSBHUB3P_USB3_DATA_ENABLED (3)
            * aUSBHUB3P_USB_SPEED_USB2 (11)
            * aUSBHUB3P_USB_SPEED_USB3 (12)
            * aUSBHUB3P_USB_ERROR_FLAG (19)
            * aUSBHUB3P_USB2_BOOST_ENABLED (20)
            * aUSBHUB3P_DEVICE_ATTACHED (23)

            Bit defines for port error UInt32
            use brainstem.BIT(X) from aDefs.h to get bit value.
            i.e if (error & brainstem.BIT(aUSBHUB3P_ERROR_VBUS_OVERCURRENT))

            * aUSBHUB3P_ERROR_VBUS_OVERCURRENT (0)
            * aUSBHUB3P_ERROR_VBUS_BACKDRIVE (1)
            * aUSBHUB3P_ERROR_HUB_POWER (2)
            * aUSBHUB3P_ERROR_OVER_TEMPERATURE (3)

    """

    BASE_ADDRESS = 6
    NUMBER_OF_STORES = 2
    NUMBER_OF_INTERNAL_SLOTS = 12
    NUMBER_OF_RAM_SLOTS = 1
    NUMBER_OF_TIMERS = 8
    NUMBER_OF_APPS = 4
    NUMBER_OF_POINTERS = 4
    NUMBER_OF_DOWNSTREAM_USB = 8
    NUMBER_OF_UPSTREAM_USB = 2
    NUMBER_OF_USB_PORTS = 8
    NUMBER_OF_PORTS = 12

    # Bit defines for port state UInt32
    # use brainstem.BIT(X) from aDefs.h to get bit value.
    # i.e if (state & brainstem.BIT(aUSBHUB3P_USB_VBUS_ENABLED))
    aUSBHUB3P_USB_VBUS_ENABLED = 0
    aUSBHUB3P_USB2_DATA_ENABLED = 1
    aUSBHUB3P_USB3_DATA_ENABLED = 3
    aUSBHUB3P_USB_SPEED_USB2 = 11
    aUSBHUB3P_USB_SPEED_USB3 = 12
    aUSBHUB3P_USB_ERROR_FLAG = 19
    aUSBHUB3P_USB2_BOOST_ENABLED = 20
    aUSBHUB3P_DEVICE_ATTACHED = 23

    # Bit defines for port error UInt32
    # use brainstem.BIT(X) from aDefs.h to get bit value.
    # i.e if (error & brainstem.BIT(aUSBHUB3P_ERROR_VBUS_OVERCURRENT))
    aUSBHUB3P_ERROR_VBUS_OVERCURRENT = 0
    aUSBHUB3P_ERROR_VBUS_BACKDRIVE = 1
    aUSBHUB3P_ERROR_HUB_POWER = 2
    aUSBHUB3P_ERROR_OVER_TEMPERATURE = 3

    def __init__(self, address=BASE_ADDRESS, enable_auto_networking=True, model=defs.MODEL_USBHUB_3P):
        super(USBHub3p, self).__init__(address, enable_auto_networking, model)
        self.system = System(self, 0)
        self.app = [App(self, i) for i in range(0, 4)]
        self.pointer = [Pointer(self, i) for i in range(0, 4)]
        self.hub = USBHub3p.Hub(self, 0)
        self.usb = USB(self, 0)
        self.store = [Store(self, i) for i in range(0, 2)]
        self.temperature = Temperature(self, 0)
        self.timer = [Timer(self, i) for i in range(0, 8)]

    def connect(self, serial_number, **kwargs):
        return super(USBHub3p, self).connect(Spec.USB, serial_number)


    class Hub(USBSystem):
        def __init__(self, module, index):
            super(USBHub3p.Hub, self).__init__(module, index)
            self.port = [Port(module, i) for i in range(0, USBHub3p.NUMBER_OF_PORTS)]

class USBStem(Module):
    """ Concrete Module implementation for 40Pin USBStem modules

        USBStem modules contain contain the following entities:
            * system
            * analog[0-3]
            * app[0-3]
            * clock
            * digital[0-14]
            * i2c[0-1]
            * pointer[0-3]
            * servo[0-7]
            * store[0-2]
            * timer[0-7]

    Useful Constants:
        * BASE_ADDRESS (2)
        * NUMBER_OF_STORES (3)
        * NUMBER_OF_INTERNAL_SLOTS (12)
        * NUMBER_OF_RAM_SLOTS (1)
        * NUMBER_OF_SD_SLOTS (255)
        * NUMBER_OF_ANALOGS (4)
        * DAC_ANALOG_INDEX (3)
        * FIXED_DAC_ANALOG (False)
        * NUMBER_OF_DIGITALS (15)
        * NUMBER_OF_I2C (2)
        * NUMBER_OF_POINTERS (4)
        * NUMBER_OF_TIMERS (8)
        * NUMBER_OF_APPS (4)
        * NUMBER_OF_SERVOS (8)
        * NUMBER_OF_SERVO_OUTPUTS (4)
        * NUMBER_OF_SERVO_INPUTS (4)
        * ANALOG_BULK_CAPTURE_MAX_HZ (200000)
        * ANALOG_BULK_CAPTURE_MIN_HZ (7000)
    """

    BASE_ADDRESS = 2
    NUMBER_OF_STORES = 3
    NUMBER_OF_INTERNAL_SLOTS = 12
    NUMBER_OF_RAM_SLOTS = 1
    NUMBER_OF_SD_SLOTS = 255
    NUMBER_OF_ANALOGS = 4
    DAC_ANALOG_INDEX = 3
    FIXED_DAC_ANALOG = False
    NUMBER_OF_DIGITALS = 15
    NUMBER_OF_I2C = 2
    NUMBER_OF_POINTERS = 4
    NUMBER_OF_TIMERS = 8
    NUMBER_OF_APPS = 4
    NUMBER_OF_SERVOS = 8
    NUMBER_OF_SERVO_OUTPUTS = 4
    NUMBER_OF_SERVO_INPUTS = 4
    ANALOG_BULK_CAPTURE_MAX_HZ = 200000
    ANALOG_BULK_CAPTURE_MIN_HZ = 7000

    def __init__(self, address=BASE_ADDRESS, enable_auto_networking=True, model=defs.MODEL_USBSTEM):
        super(USBStem, self).__init__(address, enable_auto_networking, model)
        self.system = System(self, 0)
        self.analog = [Analog(self, i) for i in range(0, 4)]
        self.app = [App(self, i) for i in range(0, 4)]
        self.clock = Clock(self, 0)
        self.digital = [Digital(self, i) for i in range(0, 15)]
        self.i2c = [I2C(self, i) for i in range(0, 2)]
        self.pointer = [Pointer(self, i) for i in range(0, 4)]
        self.store = [Store(self, i) for i in range(0, 3)]
        self.timer = [Timer(self, i) for i in range(0, 8)]
        self.servo = [RCServo(self, i) for i in range(0, 8)]

    def connect(self, serial_number, **kwargs):
        return super(USBStem, self).connect(Spec.USB, serial_number)


class USBExt3c(Module):
    """ Concrete Module implementation for the USBExt3c.

        The module contains the USB entity as well as the following.

        Entities:
            * system
            * app[0-3]
            * pointers[0-3]
            * store[0-2]
            * timer[0-7]
            * hub
            * hub.port[0-2]
            * pd[0-2]
            * usb
            * poe
            * hdbt
            * temperature
            * uart[0-6]

        Useful Constants:
            * BASE_ADDRESS (20)
            * NUMBER_OF_STORES (3)
            * NUMBER_OF_INTERNAL_SLOTS (12)
            * NUMBER_OF_RAM_SLOTS (1)
            * NUMBER_OF_TIMERS (8)
            * NUMBER_OF_APPS (4)
            * NUMBER_OF_POINTERS (4)
            * NUMBER_OF_USB_PORTS (3)
            * NUMBER_OF_UARTS (7)
            * NUMBER_OF_ETHERNET (1)
            * NUMBER_OF_POE (1)
            * STORE_INTERNAL_INDEX (0)
            * STORE_RAM_INDEX (1)
            * STORE_EEPROM_INDEX (2)
            * NUMBER_OF_PORTS (3)
            * NUMBER_OF_TEMPERATURES(7)


    """

    BASE_ADDRESS = 20
    NUMBER_OF_STORES = 3
    NUMBER_OF_INTERNAL_SLOTS = 12
    NUMBER_OF_RAM_SLOTS = 1
    NUMBER_OF_TIMERS = 8
    NUMBER_OF_APPS = 4
    NUMBER_OF_POINTERS = 4
    NUMBER_OF_UARTS = 7
    NUMBER_OF_PORTS = 4 # 3x USB, 1x HDBaseT
    NUMBER_OF_USB_PORTS = 3
    NUMBER_OF_POWER_DELIVERY_PORTS = 3
    NUMBER_OF_ETHERNET = 1
    NUMBER_OF_POE = 1
    NUMBER_OF_HDBASET = 2
    STORE_INTERNAL_INDEX = 0
    STORE_RAM_INDEX = 1
    STORE_EEPROM_INDEX = 2
    NUMBER_OF_TEMPERATURES = 7


    def __init__(self, address=BASE_ADDRESS, enable_auto_networking=True, model=defs.MODEL_USBEXT_3C):
        super(USBExt3c, self).__init__(address, enable_auto_networking, model)
        self.system = System(self, 0)
        self.app = [App(self, i) for i in range(0, USBExt3c.NUMBER_OF_APPS)]
        self.pointer = [Pointer(self, i) for i in range(0, USBExt3c.NUMBER_OF_POINTERS)]
        self.store = [Store(self, _BS_C.storeInternalStore),
                      Store(self, _BS_C.storeRAMStore),
                      Store(self, _BS_C.storeEEPROMStore)]
        self.timer = [Timer(self, i) for i in range(0, USBExt3c.NUMBER_OF_TIMERS)]
        self.hub = USBExt3c.Hub(self, 0)
        self.pd = [PowerDelivery(self, i) for i in range(0, USBExt3c.NUMBER_OF_POWER_DELIVERY_PORTS)]
        self.usb = USB(self, 0) # usb entity adds minimal legacy support
        self.uart = [UART(self, i) for i in range(0, USBExt3c.NUMBER_OF_UARTS)]
        self.ethernet = Ethernet(self, 0)
        self.poe = PoE(self, 0)
        self.hdbt = [HDBaseT(self, i) for i in range(0, USBExt3c.NUMBER_OF_HDBASET)]
        self.temperature = [Temperature(self, i) for i in range(0, USBExt3c.NUMBER_OF_TEMPERATURES)]

    def connect(self, serial_number, **kwargs):
        return super(USBExt3c, self).connect(Spec.USB, serial_number)


    class Hub(USBSystem):
        def __init__(self, module, index):
            super(USBExt3c.Hub, self).__init__(module, index)
            self.port = [Port(module, i) for i in range(0, USBExt3c.NUMBER_OF_PORTS)]