"""
The Interpreter module implements the Javonet command interpreter.
"""

from javonet.core.handler.Handler import Handler
from javonet.core.protocol.CommandDeserializer import CommandDeserializer
from javonet.core.protocol.CommandSerializer import CommandSerializer
from javonet.utils.ConnectionType import ConnectionType
from javonet.utils.RuntimeName import RuntimeName


class Interpreter(object):
    """
    Class responsible for interpreting and executing Javonet commands.
    """

    @staticmethod
    def execute(command, connection_data):
        message_byte_array = CommandSerializer.serialize(command, connection_data)
        if connection_data.connection_type == ConnectionType.WebSocket:
            from javonet.core.webSocketClient.WebSocketClient import WebSocketClient
            response_byte_array = WebSocketClient.send_message(connection_data.hostname, message_byte_array)
        elif (command.runtime_name == RuntimeName.python27) & (
                connection_data.connection_type == ConnectionType.InMemory):
            from javonet.core.receiver.Receiver import Receiver
            response_byte_array = Receiver.SendCommand(message_byte_array)
        else:
            from javonet.core.transmitter.Transmitter import Transmitter
            response_byte_array = Transmitter.send_command(message_byte_array)

        return CommandDeserializer.deserialize(response_byte_array)

    @staticmethod
    def process(message_byte_array):
        received_command = CommandDeserializer.deserialize(message_byte_array)
        return Handler.handle_command(received_command)