# -*- coding: utf-8 -*-
"""
The CommandDeserializer module implements command deserialization.
"""

from javonet.core.protocol.TypeDeserializer import TypeDeserializer
from javonet.utils.Command import Command
from javonet.utils.CommandType import CommandType
from javonet.utils.RuntimeName import RuntimeName
from javonet.utils.StringEncodingMode import StringEncodingMode
from javonet.utils.Type import Type


class _DeserializerState(object):
    """Internal state holder for deserialization."""
    def __init__(self, buffer):
        self.buffer = buffer
        self.buffer_len = len(buffer)
        self.position = 0


class CommandDeserializer(object):
    """
    Class responsible for command deserialization.
    """

    @staticmethod
    def deserialize(buffer):
        """
        Deserializes a command from a buffer.

        :param buffer: Buffer with data to deserialize
        :return: Deserialized command
        """
        if len(buffer) < 11:
            raise ValueError("Buffer too small to contain a command header.")
        
        state = _DeserializerState(buffer)
        command = Command(RuntimeName(buffer[0]), CommandType(buffer[10]), [])
        state.position = 11
        
        while not CommandDeserializer._is_at_end(state):
            command = command.add_arg_to_payload(CommandDeserializer._read_object(state))
        
        return command

    @staticmethod
    def _is_at_end(state):
        """
        Checks if the end of buffer has been reached.

        :param state: Deserializer state
        :return: True if end of buffer is reached, False otherwise
        """
        return state.position >= state.buffer_len

    @staticmethod
    def _check_buffer(state, required_size):
        """Checks if there are enough bytes left in the buffer."""
        if state.position + required_size > state.buffer_len:
            raise IndexError("Not enough data in buffer to read next value.")

    @staticmethod
    def _read_object(state):
        """
        Reads an object from the buffer based on its type.

        :param state: Deserializer state
        :return: Read object
        """
        type_num = state.buffer[state.position]
        type_value = Type(type_num)
        switch = {
            Type.Command: CommandDeserializer._read_command,
            Type.JavonetString: CommandDeserializer._read_string,
            Type.JavonetInteger: CommandDeserializer._read_int,
            Type.JavonetBoolean: CommandDeserializer._read_bool,
            Type.JavonetFloat: CommandDeserializer._read_float,
            Type.JavonetByte: CommandDeserializer._read_byte,
            Type.JavonetChar: CommandDeserializer._read_char,
            Type.JavonetLongLong: CommandDeserializer._read_longlong,
            Type.JavonetDouble: CommandDeserializer._read_double,
            Type.JavonetUnsignedLongLong: CommandDeserializer._read_ullong,
            Type.JavonetUnsignedInteger: CommandDeserializer._read_uint,
            Type.JavonetNoneType: CommandDeserializer._read_none
        }
        func = switch.get(type_value)
        if func is None:
            raise ValueError("Type not supported: " + str(type_num))
        return func(state)

    @staticmethod
    def _read_command(state):
        """
        Reads a command from the buffer.

        :param state: Deserializer state
        :return: Read command
        """
        CommandDeserializer._check_buffer(state, 7)
        p = state.position
        number_of_elements_in_payload = TypeDeserializer.deserialize_int(state.buffer[p + 1: p + 5])
        runtime = state.buffer[p + 5]
        command_type = state.buffer[p + 6]
        state.position += 7

        payload = []
        for _ in xrange(number_of_elements_in_payload):
            payload.append(CommandDeserializer._read_object(state))

        return Command(RuntimeName(runtime), CommandType(command_type), payload)

    @staticmethod
    def _read_string(state):
        """
        Reads a string from the buffer.

        :param state: Deserializer state
        :return: Read string
        """
        CommandDeserializer._check_buffer(state, 6)
        p = state.position
        string_encoding_mode = StringEncodingMode(state.buffer[p + 1])
        size = TypeDeserializer.deserialize_int(state.buffer[p + 2:p + 6])
        state.position += 6
        CommandDeserializer._check_buffer(state, size)
        p = state.position
        state.position += size
        return TypeDeserializer.deserialize_string(string_encoding_mode, state.buffer[p:p + size])

    @staticmethod
    def _read_int(state):
        size = 4
        CommandDeserializer._check_buffer(state, size + 2)
        state.position += 2
        p = state.position
        state.position += size
        return TypeDeserializer.deserialize_int(state.buffer[p:p + size])

    @staticmethod
    def _read_bool(state):
        size = 1
        CommandDeserializer._check_buffer(state, size + 2)
        state.position += 2
        p = state.position
        state.position += size
        return TypeDeserializer.deserialize_bool(state.buffer[p:p + size])

    @staticmethod
    def _read_float(state):
        size = 4
        CommandDeserializer._check_buffer(state, size + 2)
        state.position += 2
        p = state.position
        state.position += size
        return TypeDeserializer.deserialize_float(state.buffer[p:p + size])

    @staticmethod
    def _read_byte(state):
        size = 1
        CommandDeserializer._check_buffer(state, size + 2)
        state.position += 2
        p = state.position
        state.position += size
        return TypeDeserializer.deserialize_byte(state.buffer[p:p + size])

    @staticmethod
    def _read_char(state):
        size = 1
        CommandDeserializer._check_buffer(state, size + 2)
        state.position += 2
        p = state.position
        state.position += size
        return TypeDeserializer.deserialize_char(state.buffer[p:p + size])

    @staticmethod
    def _read_longlong(state):
        size = 8
        CommandDeserializer._check_buffer(state, size + 2)
        state.position += 2
        p = state.position
        state.position += size
        return TypeDeserializer.deserialize_longlong(state.buffer[p:p + size])

    @staticmethod
    def _read_double(state):
        size = 8
        CommandDeserializer._check_buffer(state, size + 2)
        state.position += 2
        p = state.position
        state.position += size
        return TypeDeserializer.deserialize_double(state.buffer[p:p + size])

    @staticmethod
    def _read_ullong(state):
        size = 8
        CommandDeserializer._check_buffer(state, size + 2)
        state.position += 2
        p = state.position
        state.position += size
        return TypeDeserializer.deserialize_ullong(state.buffer[p:p + size])

    @staticmethod
    def _read_uint(state):
        size = 4
        CommandDeserializer._check_buffer(state, size + 2)
        state.position += 2
        p = state.position
        state.position += size
        return TypeDeserializer.deserialize_uint(state.buffer[p:p + size])

    @staticmethod
    def _read_none(state):
        size = 1
        CommandDeserializer._check_buffer(state, size + 2)
        state.position += 2
        p = state.position
        state.position += size
        return TypeDeserializer.deserialize_none(state.buffer[p:p + size])
