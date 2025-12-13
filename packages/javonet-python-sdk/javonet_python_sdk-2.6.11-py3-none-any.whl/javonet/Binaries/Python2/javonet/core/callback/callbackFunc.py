# -*- coding: utf-8 -*-
"""
The callbackFunc module implements the callback function.
"""


def callbackFunc(message_byte_array, message_byte_array_len):
    """
    Callback function handling messages.

    :param message_byte_array: Message byte array
    :param message_byte_array_len: Length of the byte array
    :return: Response as byte array
    """
    from javonet.core.receiver.Receiver import Receiver
    if message_byte_array[10] == 11:
        return Receiver.HeartBeat(message_byte_array)
    else:
        return Receiver.SendCommand(message_byte_array)