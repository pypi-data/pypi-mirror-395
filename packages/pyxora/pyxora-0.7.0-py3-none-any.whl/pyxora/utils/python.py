import os
import sys
from os.path import basename, splitext
from importlib.util import spec_from_file_location, module_from_spec
from importlib import reload
from types import ModuleType
from sys import path as sys_path, modules
from os import getcwd

__all__ = ["get_filename","get_filetype","load_module","load_class"]

def get_filename(file_path: str) -> str:
    """
    Get the filename (without extension) from a full path.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: Filename without extension.
    """
    return splitext(basename(file_path))[0]

def get_filetype(file_path: str) -> str:
    """
    Get the filetype (without extension) from a full path.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: Filename without extension.
    """
    return splitext(basename(file_path))[1]


def load_module(file_path: str) -> ModuleType:
    """
    Dynamically load a Python module from a given file path.

    Args:
        file_path (str): Relative or absolute path to the `.py` file.

    Returns:
        module: The loaded module object.

    Raises:
        FileNotFoundError: If the file does not exist.
        ImportError: If the module fails to load.
    """
    full_path = os.path.normpath(os.path.join(os.getcwd(), file_path))

    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Module file not found: {full_path}")

    main_dir = os.path.dirname(full_path)
    if main_dir not in sys_path:
        sys_path.append(main_dir)

    module_name = get_filename(full_path)
    spec = spec_from_file_location(module_name, full_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Couldn't create spec for module '{module_name}'.")

    module = module_from_spec(spec)
    modules[module_name] = module
    spec.loader.exec_module(module)

    return module

def load_class(file_path: str,name:str) -> type:
    """
    Load a class from a path

    Args:
        file_path (str): The class path.
        name (str): The name of the class to retrieve.

    Returns:
        type: The loaded class object.
    """
    module = load_module(file_path)
    the_class = getattr(module, name, None)
    return the_class
