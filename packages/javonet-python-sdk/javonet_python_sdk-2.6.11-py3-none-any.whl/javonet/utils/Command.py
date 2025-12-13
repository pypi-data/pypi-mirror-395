from javonet.utils.CommandType import CommandType


class Command:

    def __init__(self, runtime_name, command_type, payload=None):
        """
        Initialize a Command.
        Matches C# constructor: Command(RuntimeName runtimeName, CommandType commandType, params object[] payload)
        and: Command(RuntimeName runtimeName, CommandType commandType, Array payload)

        Args:
            runtime_name: The runtime name.
            command_type: The command type.
            payload: The payload. Can be None, a list/tuple (array-like), or a single item.
                    If None, defaults to empty list.
        """
        self.runtime_name = runtime_name
        self.command_type = command_type

        if isinstance(payload, list) and len(payload) == 0:
            # Payload is empty - create empty list
            self.payload = []
        if payload is None:
            self.payload = [None]
        elif isinstance(payload, (list, tuple)):
            # If it's a list or tuple, convert to list (matching C# Array handling)
            # For list, reuse directly for efficiency (matching C# object[] case)
            if isinstance(payload, list):
                self.payload = payload
            else:
                # For tuple or other sequence, convert to list
                self.payload = list(payload)
        else:
            # Single item - wrap in list
            self.payload = [payload]

    @property
    def RuntimeName(self):
        """Get the runtime name (property accessor matching C# style)."""
        return self.runtime_name

    @property
    def CommandType(self):
        """Get the command type (property accessor matching C# style)."""
        return self.command_type

    @property
    def Payload(self):
        """Get the payload (property accessor matching C# style)."""
        return self.payload

    def get_payload(self):
        """Get the payload (legacy method for backward compatibility)."""
        return self.payload

    @staticmethod
    def create_response(response, runtime_name):
        return Command(runtime_name, CommandType.Value, response)

    @staticmethod
    def create_reference(guid, runtime_name):
        return Command(runtime_name, CommandType.Reference, guid)

    @staticmethod
    def create_array_response(array, runtime_name):
        return Command(runtime_name, CommandType.Array, array)

    def drop_first_payload_argument(self):
        """Legacy method name for backward compatibility."""
        return self.drop_first_payload_arg()

    def drop_first_payload_arg(self):
        if len(self.payload) <= 1:
            return Command(self.runtime_name, self.command_type, [])
        
        new_length = len(self.payload) - 1
        new_payload = [None] * new_length
        
        # Copy from index 1 to end
        for i in range(new_length):
            new_payload[i] = self.payload[i + 1]
        
        return Command(self.runtime_name, self.command_type, new_payload)

    def add_arg_to_payload(self, arg):
        old_length = len(self.payload)
        new_payload = [None] * (old_length + 1)
        
        if old_length > 0:
            for i in range(old_length):
                new_payload[i] = self.payload[i]
        
        new_payload[old_length] = arg
        
        return Command(self.runtime_name, self.command_type, new_payload)

    def prepend_arg_to_payload(self, arg_command):
        if arg_command is None:
            return self
        
        old_length = len(self.payload)
        new_payload = [None] * (old_length + 1)
        
        # Put new element at the front
        new_payload[0] = arg_command
        
        if old_length > 0:
            for i in range(old_length):
                new_payload[i + 1] = self.payload[i]
        
        return Command(self.runtime_name, self.command_type, new_payload)

    def to_string(self):
        """Legacy method for backward compatibility."""
        return str(self)

    def __eq__(self, element):
        if self is element:
            return True
        if element is None or self.__class__ != element.__class__:
            return False
        if self.command_type != element.command_type or self.runtime_name != element.runtime_name:
            return False
        if len(self.payload) != len(element.payload):
            return False
        
        for i, payload_item in enumerate(self.payload):
            if payload_item != element.payload[i]:
                return False
        
        return True

    def __str__(self):
        try:
            result = "RuntimeName "
            result += str(self.runtime_name)
            result += " "
            result += "CommandType "
            result += str(self.command_type)
            result += " "
            result += "Payload "
            
            payload = self.payload
            length = len(payload)
            
            for i in range(length):
                item = payload[i]
                if item is None:
                    result += "null"
                else:
                    result += str(item)
                
                if i < length - 1:
                    result += " "
            
            return result
        except Exception as ex:
            return f"Error while converting command to string: {str(ex)}"