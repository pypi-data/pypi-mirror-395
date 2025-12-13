from javonet.core.protocol.TypeDeserializer import TypeDeserializer
from javonet.utils.Command import Command
from javonet.utils.CommandType import CommandType
from javonet.utils.RuntimeName import RuntimeName
from javonet.utils.Type import Type
from javonet.utils.StringEncodingMode import StringEncodingMode


class CommandDeserializer:
    """
    Static class for deserializing commands from byte arrays.
    """

    @staticmethod
    def deserialize(buffer):
        """
        Deserialize a command from a byte array.

        Args:
            buffer: The byte array containing the serialized command.

        Returns:
            Command: The deserialized command.
        """
        buffer_len = len(buffer)
        command = Command(RuntimeName(buffer[0]), CommandType(buffer[10]), [])
        position = 11

        # Use a list to hold position (mutable reference for nested functions)
        pos_ref = [position]

        def is_at_end():
            return pos_ref[0] == buffer_len

        def read_object(type_num):
            type_value = Type(type_num)
            switch = {
                Type.Command: read_command,
                Type.JavonetString: read_string,
                Type.JavonetInteger: read_int,
                Type.JavonetBoolean: read_bool,
                Type.JavonetFloat: read_float,
                Type.JavonetByte: read_byte,
                Type.JavonetChar: read_char,
                Type.JavonetLongLong: read_longlong,
                Type.JavonetDouble: read_double,
                Type.JavonetUnsignedLongLong: read_ullong,
                Type.JavonetUnsignedInteger: read_uint,
                Type.JavonetNoneType: read_none
            }
            func = switch.get(type_value)
            if func is None:
                raise Exception("Type not supported")
            return func()

        def read_command():
            p = pos_ref[0]
            number_of_elements_in_payload = TypeDeserializer.deserialize_int(buffer[p + 1: p + 5])
            runtime = buffer[p + 5]
            command_type = buffer[p + 6]
            pos_ref[0] += 7

            payload = [
                read_object(buffer[pos_ref[0]])
                for _ in range(number_of_elements_in_payload)
            ]
            return Command(RuntimeName(runtime), CommandType(command_type), payload)

        def read_string():
            p = pos_ref[0]
            string_encoding_mode = StringEncodingMode(buffer[p + 1])
            size = TypeDeserializer.deserialize_int(buffer[p + 2:p + 6])
            pos_ref[0] += 6
            p = pos_ref[0]
            pos_ref[0] += size
            return TypeDeserializer.deserialize_string(string_encoding_mode, buffer[p:p + size])

        def read_int():
            size = 4
            pos_ref[0] += 2
            p = pos_ref[0]
            pos_ref[0] += size
            return TypeDeserializer.deserialize_int(buffer[p:p + size])

        def read_bool():
            size = 1
            pos_ref[0] += 2
            p = pos_ref[0]
            pos_ref[0] += size
            return TypeDeserializer.deserialize_bool(buffer[p:p + size])

        def read_float():
            size = 4
            pos_ref[0] += 2
            p = pos_ref[0]
            pos_ref[0] += size
            return TypeDeserializer.deserialize_float(buffer[p:p + size])

        def read_byte():
            size = 1
            pos_ref[0] += 2
            p = pos_ref[0]
            pos_ref[0] += size
            return TypeDeserializer.deserialize_byte(buffer[p:p + size])

        def read_char():
            size = 1
            pos_ref[0] += 2
            p = pos_ref[0]
            pos_ref[0] += size
            return TypeDeserializer.deserialize_char(buffer[p:p + size])

        def read_longlong():
            size = 8
            pos_ref[0] += 2
            p = pos_ref[0]
            pos_ref[0] += size
            return TypeDeserializer.deserialize_longlong(buffer[p:p + size])

        def read_double():
            size = 8
            pos_ref[0] += 2
            p = pos_ref[0]
            pos_ref[0] += size
            return TypeDeserializer.deserialize_double(buffer[p:p + size])

        def read_ullong():
            size = 8
            pos_ref[0] += 2
            p = pos_ref[0]
            pos_ref[0] += size
            return TypeDeserializer.deserialize_ullong(buffer[p:p + size])

        def read_uint():
            size = 4
            pos_ref[0] += 2
            p = pos_ref[0]
            pos_ref[0] += size
            return TypeDeserializer.deserialize_uint(buffer[p:p + size])

        def read_none():
            size = 1
            pos_ref[0] += 2
            p = pos_ref[0]
            pos_ref[0] += size
            return TypeDeserializer.deserialize_none(buffer[p:p + size])

        # Main deserialization loop
        while not is_at_end():
            command = command.add_arg_to_payload(read_object(buffer[pos_ref[0]]))

        return command
