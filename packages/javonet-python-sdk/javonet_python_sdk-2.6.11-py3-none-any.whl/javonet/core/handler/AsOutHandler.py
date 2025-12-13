from javonet.core.handler.AbstractCommandHandler import *

class AsOutHandler(AbstractCommandHandler):
    def process(self, command):
        raise NotImplementedError(f"{self.__class__.__name__} is not implemented in Python")

