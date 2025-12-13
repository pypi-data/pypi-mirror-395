# -*- coding: utf-8 -*-
"""
The CommandSerializer module implements command serialization.
"""

from javonet.core.protocol.TypeSerializer import TypeSerializer
from javonet.utils.Command import Command
from javonet.utils.CommandType import CommandType
from javonet.utils.RuntimeName import RuntimeName
from javonet.utils.connectionData.IConnectionData import IConnectionData
from javonet.utils.TypesHandler import TypesHandler
from javonet.core.referenceCache.ReferencesCache import ReferencesCache

class CommandSerializer(object):
    """
    Class responsible for command serialization.
    """

    @staticmethod
    def serialize(root_command, connection_data, runtime_version=0):
        """
        Serializes a command.

        :param root_command: Command to serialize
        :param connection_data: Connection data
        :param runtime_version: Runtime version
        :return: Serialized command
        """
        buffer = []  # Reset buffer for each serialization
        CommandSerializer._insert_into_buffer(buffer, [root_command.runtime_name.value, runtime_version])
        CommandSerializer._insert_into_buffer(buffer, connection_data.serialize_connection_data())
        CommandSerializer._insert_into_buffer(buffer, [RuntimeName.python27.value, root_command.command_type.value])
        CommandSerializer._serialize_recursively(buffer, root_command)
        return buffer

    @staticmethod
    def _serialize_recursively(buffer, command):
        """
        Serializes a command recursively.

        :param buffer: Buffer to serialize into
        :param command: Command to serialize
        """
        for item in command.payload:
            if isinstance(item, Command):
                CommandSerializer._insert_into_buffer(buffer, TypeSerializer.serialize_command(item))
                CommandSerializer._serialize_recursively(buffer, item)
            elif TypesHandler.is_primitive_or_none(item):
                CommandSerializer._insert_into_buffer(buffer, TypeSerializer.serialize_primitive(item))
            else:
                cached_reference = ReferencesCache().cache_reference(item)
                ref_command = Command(RuntimeName.python, CommandType.Reference, cached_reference)
                CommandSerializer._serialize_recursively(buffer, ref_command)

        return

    @staticmethod
    def _insert_into_buffer(buffer, arguments):
        """
        Inserts arguments into the buffer.

        :param buffer: Buffer to insert into
        :type arguments: list
        """
        buffer.extend(arguments) 