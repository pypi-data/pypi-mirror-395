import threading
from uuid import UUID
from javonet.core.handler.AbstractCommandHandler import *

class _ThreadContexts(threading.local):
    def __init__(self):
        # guid (UUID or empty GUID) -> object
        self.map = {}

class RegisterForUpdateHandler(AbstractCommandHandler):
    # Shared per process, separate dicts per thread
    _invocation_contexts = _ThreadContexts()
    _required_parameters_count = 2

    @classmethod
    def _get_or_create_context_dict(cls):
        if getattr(cls._invocation_contexts, "map", None) is None:
            cls._invocation_contexts.map = {}
        return cls._invocation_contexts.map

    def process(self, command):
        # Validate minimal number of parameters
        if command.payload is None or len(command.payload) < self._required_parameters_count:
            raise ValueError(f"{self.__class__.__name__} requires at least {self._required_parameters_count} parameter(s).")

        obj_to_register = command.payload[0]
        guid_to_register = None
        if len(command.payload) > 1 and command.payload[1]:
            try:
                guid_to_register = UUID(str(command.payload[1]))
            except Exception:
                # If invalid GUID, treat as no GUID
                guid_to_register = None

        ctx = self._get_or_create_context_dict()
        # Use None as key when GUID is missing (analogous to Guid.Empty)
        ctx[guid_to_register] = obj_to_register
        return obj_to_register
