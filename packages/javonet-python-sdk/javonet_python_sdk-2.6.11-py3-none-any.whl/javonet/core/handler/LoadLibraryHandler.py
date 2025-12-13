import os
import sys
import py_compile
from argparse import ArgumentError

from javonet.core.handler.AbstractCommandHandler import *
from javonet.utils.LazyModuleLoader import LazyModuleLoader


class LoadLibraryHandler(AbstractCommandHandler):
    # Track loaded directories/files by absolute path
    loaded_dir_and_files = set()

    def __init__(self):
        self._required_parameters_count = 1

    def process(self, command):
        try:
            if len(command.payload) != self._required_parameters_count:
                raise Exception("LoadLibrary payload parameters mismatch")

            dir_or_file_to_load = command.payload[0]

            if not isinstance(dir_or_file_to_load, str) or not dir_or_file_to_load:
                raise Exception("Library path is required and must be a non-empty string")

            # ------------------------------------------------------------------
            # Normalize file extension:
            # - If no extension is provided and "<path>.py" exists, use that.
            # ------------------------------------------------------------------
            normalized_path = dir_or_file_to_load
            root, ext = os.path.splitext(normalized_path)
            if ext == "":
                candidate = normalized_path + ".py"
                if os.path.isfile(candidate):
                    normalized_path = candidate

            # Use absolute path for de-duplication
            absolute_path = os.path.abspath(normalized_path)

            # Ensure path exists
            if not os.path.exists(absolute_path):
                raise Exception(f"{dir_or_file_to_load} does not exist")

            # ------------------------------------------------------------------
            # Load only once (by absolute path)
            # ------------------------------------------------------------------
            if absolute_path in LoadLibraryHandler.loaded_dir_and_files:
                return 0

            if os.path.isdir(absolute_path):
                # Add directory to sys.path only if not already present
                if absolute_path not in sys.path:
                    sys.path.append(absolute_path)

            elif os.path.isfile(absolute_path) and absolute_path.endswith(".py"):
                # ------------------------------------------------------------------
                # Validate Python syntax before registering module
                # ------------------------------------------------------------------
                py_compile.compile(absolute_path, doraise=True)

                module_name = os.path.splitext(os.path.basename(absolute_path))[0]
                LazyModuleLoader.register_module_path(module_name, absolute_path)
            else:
                raise Exception(f"{dir_or_file_to_load} is not a valid directory or .py file")

            # Mark as loaded
            LoadLibraryHandler.loaded_dir_and_files.add(absolute_path)

            return 0

        except Exception as e:
            new_exc = ArgumentError(None, str(e)).with_traceback(e.__traceback__)
            raise new_exc from None

    @staticmethod
    def get_loaded_directories():
        # Return a list for external callers
        return list(LoadLibraryHandler.loaded_dir_and_files)
