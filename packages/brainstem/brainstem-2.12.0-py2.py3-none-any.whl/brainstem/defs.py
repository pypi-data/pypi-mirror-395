# Copyright (c) 2018 Acroname Inc. - All Rights Reserved
#
# This file is part of the BrainStem (tm) package which is released under MIT.
# See file LICENSE or go to https://acroname.com for full license details.

"""
A module that provides defines and constants useful for working with the python
library.

"""


from . import _BS_C


MODEL_USBSTEM =            _BS_C.aMODULE_TYPE_USBStem_1         #4  USBStem Model number
MODEL_ETHERSTEM =          _BS_C.aMODULE_TYPE_EtherStem_1       #5  EtherStem Model number
MODEL_MTM_IOSERIAL =       _BS_C.aMODULE_TYPE_MTMIOSerial_1     #13 MTM-IO-Serial Model number
MODEL_MTM_PM_1 =           _BS_C.aMODULE_TYPE_MTM_PM_1          #14 MTM-PM-1 Model number
MODEL_MTM_ETHERSTEM =      _BS_C.aMODULE_TYPE_MTM_EtherStem     #15 MTM EtherStem Model number
MODEL_MTM_USBSTEM =        _BS_C.aMODULE_TYPE_MTM_USBStem       #16 MTM USBStem Model number
MODEL_USBHUB_2X4 =         _BS_C.aMODULE_TYPE_USBHub2x4         #17 USBHub 2x4 Model number
MODEL_MTM_RELAY =          _BS_C.aMODULE_TYPE_MTM_Relay         #18 MTM-Relay Model number
MODEL_USBHUB_3P =          _BS_C.aMODULE_TYPE_USBHub3p          #19 USBHub 3+ Model number
MODEL_MTM_DAQ_1 =          _BS_C.aMODULE_TYPE_MTM_DAQ_1         #20 MTM-DAQ-1 Model number
MODEL_USB_C_SWITCH =       _BS_C.aMODULE_TYPE_USBC_Switch       #21 USBC-Switch Model number
MODEL_MTM_DAQ_2 =          _BS_C.aMODULE_TYPE_MTM_DAQ_2         #22 MTM-DAQ-2 Model number
MODEL_MTM_LOAD_1 =         _BS_C.aMODULE_TYPE_MTM_LOAD_1        #23 MTM-LOAD-1 Model Number
MODEL_USBHUB_3C =          _BS_C.aMODULE_TYPE_USBHub3c          #24 USBHub3c Model number
MODEL_USB_C_SWITCH_PRO =   _BS_C.aMODULE_TYPE_USBC_Switch_Pro   #25 USBCSwitchPro Model number
MODEL_PD3M =               _BS_C.aMODULE_TYPE_PD3M              #26 PD3M Model number
MODEL_USBEXT_3C =          _BS_C.aMODULE_TYPE_USBExt3c          #27 USBExt3c Model number



def model_info(model):
    """ 
    Get Model information.

    :param model:  One of the model numbers, i.e from stem.system.getModel().
    :type model: int

    :return: String containing model information.
    """
    if model == MODEL_USBSTEM:
        return "40 Pin USBStem module: Default module address is 2."
    elif model == MODEL_ETHERSTEM:
        return "40 Pin EtherStem module: Default module address is 2."
    elif model == MODEL_MTM_IOSERIAL:
        return "MTM IO Serial module: Default module address is 8."
    elif model == MODEL_MTM_PM_1:
        return "MTM 1 Channel Power module: Default module address is 6."
    elif model == MODEL_MTM_ETHERSTEM:
        return "MTM EtherStem module: Default module address is 4."
    elif model == MODEL_MTM_USBSTEM:
        return "MTM USBStem module: Default module address is 4."
    elif model == MODEL_USBHUB_2X4:
        return "Programmable 4 port USB Hub: Default module address is 6."
    elif model == MODEL_MTM_RELAY:
        return "MTM Relay module: Default module address is 12."
    elif model == MODEL_USBHUB_3P:
        return "Programmable 8+1 port USB 3.0 Hub: Default module address is 6."
    elif model == MODEL_MTM_DAQ_1:
        return "MTM DAQ module: Default module address is 10."
    elif model == MODEL_USB_C_SWITCH:
        return "Programmable USB Type-C Switch module: Default module address is 6."
    elif model == MODEL_USB_C_SWITCH_PRO:
        return "Programmable USB Type-C Switch Pro module: Default module address is 16."
    elif model == MODEL_MTM_DAQ_2:
        return "MTM DAQ 2 module: Default module address is 14."
    elif model == MODEL_USBHUB_3C:
        return "USBHub3c module: Default module address is 6."
    elif model == MODEL_MTM_LOAD_1:
        return "MTM Load 1 module: Default module address is 14."
    elif model == MODEL_PD3M:
        return "PD3M module: Default module address is 18."
    elif model == MODEL_USBEXT_3C:
        return "USBExt3c module: Default module address is 20."
    else:
        return "Could not find model matching the value %d" % model


def model_name(model):
    """ 
    Get Model Name.

    :param model: One of the model numbers, i.e from stem.system.getModel().
    :type model: int

    :return: A string containing model name.
    """
    if model == MODEL_USBSTEM:
        return "USBStem"
    elif model == MODEL_ETHERSTEM:
        return "EtherStem"
    elif model == MODEL_MTM_IOSERIAL:
        return "MTMIOSerial"
    elif model == MODEL_MTM_PM_1:
        return "MTMPM1"
    elif model == MODEL_MTM_ETHERSTEM:
        return "MTMEtherStem"
    elif model == MODEL_MTM_USBSTEM:
        return "MTMUSBStem"
    elif model == MODEL_USBHUB_2X4:
        return "USBHub2x4"
    elif model == MODEL_MTM_RELAY:
        return "MTMRelay"
    elif model == MODEL_USBHUB_3P:
        return "USBHub3p"
    elif model == MODEL_MTM_DAQ_1:
        return "MTMDAQ1"
    elif model == MODEL_USB_C_SWITCH:
        return "USBCSwitch"
    elif model == MODEL_USB_C_SWITCH_PRO:
        return "USBCSwitchPro"
    elif model == MODEL_MTM_DAQ_2:
        return "MTMDAQ2"
    elif model == MODEL_USBHUB_3C:
        return "USBHub3c"
    elif model == MODEL_MTM_LOAD_1:
        return "MTMLoad1"
    elif model == MODEL_PD3M:
        return "PD3M"
    elif model == MODEL_USBEXT_3C:
        return "USBExt3c"
    else:
        return "Unknown"
