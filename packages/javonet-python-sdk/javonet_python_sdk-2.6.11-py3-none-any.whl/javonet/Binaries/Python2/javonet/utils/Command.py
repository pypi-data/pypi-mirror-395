# -*- coding: utf-8 -*-
"""
The Command class represents a command sent to the Javonet runtime environment.
"""

from javonet.utils.CommandType import CommandType

class Command(object):

    def __init__(self, runtime_name, command_type, payload):
        """
        Initializes a new command.

        :param runtime_name: Runtime environment name
        :param command_type: Command type
        :param payload: Command payload (list, tuple, single value, or None)
                        If not provided, creates empty list.
                        If None is explicitly passed, creates [None].
        """
        self.runtime_name = runtime_name
        self.command_type = command_type
        
        if isinstance(payload, list) and len(payload) == 0:
            # Payload is empty - create empty list
            self.payload = []
        elif payload is None:
            # None explicitly passed - wrap in list
            self.payload = [None]
        elif isinstance(payload, (list, tuple)):
            # Convert to list if tuple, reuse list directly
            # None values in the payload are preserved
            self.payload = list(payload) if isinstance(payload, tuple) else payload
        else:
            # Single item - wrap in list
            self.payload = [payload]

    def get_payload(self):
        """
        Returns the command payload.

        :return: Command payload
        """
        return self.payload

    @staticmethod
    def create_response(response, runtime_name):
        """
        Creates a response command.

        :param response: Response
        :param runtime_name: Runtime environment name
        :return: New response command
        """
        return Command(runtime_name, CommandType.Value, response)

    @staticmethod
    def create_reference(guid, runtime_name):
        """
        Creates a reference command.

        :param guid: GUID identifier
        :param runtime_name: Runtime environment name
        :return: New reference command
        """
        return Command(runtime_name, CommandType.Reference, guid)

    @staticmethod
    def create_array_response(array, runtime_name):
        """
        Creates an array response command.

        :param array: Array
        :param runtime_name: Runtime environment name
        :return: New array response command
        """
        return Command(runtime_name, CommandType.Array, array)

    def drop_first_payload_arg(self):
        """
        Removes the first argument from the payload.

        :return: New command without the first argument
        """
        if len(self.payload) <= 1:
            return Command(self.runtime_name, self.command_type, [])
        
        new_length = len(self.payload) - 1
        new_payload = [None] * new_length
        
        # Copy from index 1 to end
        for i in xrange(new_length):
            new_payload[i] = self.payload[i + 1]
        
        return Command(self.runtime_name, self.command_type, new_payload)

    def add_arg_to_payload(self, arg):
        """
        Adds an argument to the payload.

        :param arg: Argument to add
        :return: New command with the added argument
        """
        old_length = len(self.payload)
        new_payload = [None] * (old_length + 1)
        
        # Copy existing payload
        for i in xrange(old_length):
            new_payload[i] = self.payload[i]
        
        # Add new argument at the end
        new_payload[old_length] = arg
        
        return Command(self.runtime_name, self.command_type, new_payload)

    def prepend_arg_to_payload(self, arg_command):
        """
        Adds an argument to the beginning of the payload.

        :param arg_command: Command to prepend
        :return: New command with the argument added at the beginning
        """
        if arg_command is None:
            return self
        
        old_length = len(self.payload)
        new_payload = [None] * (old_length + 1)
        
        # Put new element at the front
        new_payload[0] = arg_command
        
        # Copy existing payload starting from index 1
        for i in xrange(old_length):
            new_payload[i + 1] = self.payload[i]
        
        return Command(self.runtime_name, self.command_type, new_payload)

    def to_string(self):
        """
        Returns a text representation of the command.

        :return: Text representation of the command
        """
        try:
            sb = []
            sb.append("RuntimeName ")
            sb.append(str(self.runtime_name))
            sb.append(" ")
            sb.append("CommandType ")
            sb.append(str(self.command_type))
            sb.append(" ")
            sb.append("Payload ")
            
            payload = self.payload
            payload_len = len(payload)
            
            for i in xrange(payload_len):
                item = payload[i]
                sb.append(str(item) if item is not None else "null")
                
                if i < payload_len - 1:
                    sb.append(" ")
            
            return ''.join(sb)
        except Exception as ex:
            return "Error while converting command to string:" + str(ex)

    def __eq__(self, other):
        """
        Compare this command with another element.
        
        :param other: Element to compare with
        :return: True if equal, False otherwise
        """
        # Basic comparison
        if not isinstance(other, self.__class__):
            return False
        
        # Compare command_type and runtime_name as numeric values
        if hasattr(self.command_type, 'value') and hasattr(other.command_type, 'value'):
            if self.command_type.value != other.command_type.value:
                return False
        else:
            # If they don't have value attribute, compare directly
            if self.command_type != other.command_type:
                return False
            
        if hasattr(self.runtime_name, 'value') and hasattr(other.runtime_name, 'value'):
            if self.runtime_name.value != other.runtime_name.value:
                return False
        else:
            if self.runtime_name != other.runtime_name:
                return False
        
        # Compare payload length
        if len(self.payload) != len(other.payload):
            return False
        
        # Compare each payload item
        for i in range(len(self.payload)):
            # Handle None values explicitly
            if self.payload[i] is None and other.payload[i] is None:
                continue
            elif self.payload[i] is None or other.payload[i] is None:
                return False
            # For simple types
            elif self.payload[i] != other.payload[i]:
                return False
                
        return True

    def __str__(self):
        """
        String representation of the command.
        
        :return: String representation
        """
        return "Command(type={0}, runtime={1}, payload_len={2})".format(
            self.command_type, self.runtime_name, len(self.payload))
        
    def __repr__(self):
        """
        Detailed representation of the command.
        
        :return: Detailed representation
        """
        return self.__str__()

    def __ne__(self, element):
        """
        Compare this command with another element for inequality.
        
        :param element: Element to compare with
        :return: True if not equal, False otherwise
        """
        return not self.__eq__(element)