"""
The Receiver module implements the message receiver.
"""

from javonet.core.interpreter.Interpreter import Interpreter
from javonet.core.protocol.CommandSerializer import CommandSerializer
from javonet.utils.RuntimeLogger import RuntimeLogger
from javonet.utils.connectionData.InMemoryConnectionData import InMemoryConnectionData
from javonet.utils.Command import Command
from javonet.utils.CommandType import CommandType
from javonet.utils.RuntimeName import RuntimeName
from javonet.utils.exception.ExceptionSerializer import ExceptionSerializer


class Receiver(object):
    """
    Class implementing the message receiver.
    """

    @staticmethod
    def SendCommand(message_byte_array_as_string):
        try:
            connection_data = InMemoryConnectionData()
            message_byte_array = bytearray(message_byte_array_as_string)
            response_command = Interpreter.process(message_byte_array)
            serialized_response = CommandSerializer.serialize(response_command, connection_data)
            return bytearray(serialized_response)
        except Exception as ex:
            connection_data = InMemoryConnectionData()
            exception_command = ExceptionSerializer.serialize_exception(
                ex,
                Command(RuntimeName.python27, CommandType.Exception, [])
            )
            serialized_exception = CommandSerializer.serialize(exception_command, connection_data)
            return bytearray(serialized_exception)

    @staticmethod
    def HeartBeat(message_byte_array_as_string):
        message_byte_array = bytearray(message_byte_array_as_string)
        response_byte_array = bytearray(2)
        response_byte_array[0] = message_byte_array[11]
        response_byte_array[1] = message_byte_array[12] - 2
        return response_byte_array

    @staticmethod
    def GetRuntimeInfo():
        return RuntimeLogger().get_runtime_info()