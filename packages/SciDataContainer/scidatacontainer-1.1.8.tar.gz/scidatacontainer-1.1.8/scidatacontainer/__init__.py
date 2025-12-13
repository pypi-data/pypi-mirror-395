##########################################################################
# Copyright (c) 2023-2024 Reinhard Caspary                               #
# <reinhard.caspary@phoenixd.uni-hannover.de>                            #
# This program is free software under the terms of the MIT license.      #
##########################################################################
#
# This package provides the Scientific Data Container as class Container
# which may be stored as a ZIP package containing items (files). Based
# on their file extension, the following item types are supported:
#
# .json: JSON file
# .txt:  Encoded text file (default encoding: UTF-8)
# .log:  Encoded text file (default encoding: UTF-8)
# .pgm:  Encoded text file (default encoding: UTF-8)
# .bin:  Raw binary data file
# .npy:  NumPy array (requires Python module numpy)
# .png:  PNG image (requires Python modules cv2 and numpy)
#
# Users may register other file extensions to file conversion classes
# using the function register(). See package fileimage as an example for
# such a conversion class.
#
##########################################################################

__all__ = [
    "timestamp",
    "modelVersion",
    "load_config",
    "register",
    "Container",
]

import typing
from importlib import import_module

from .config import load_config
from .container import MODELVERSION as modelVersion
from .container import AbstractContainer, timestamp
from .filebase import AbstractFile

__version__ = "1.1.8"

suffixes = {}
classes = {}
formats = []


def register(
    suffix: str,
    fclass: typing.Type[AbstractFile],
    pclass: typing.Type[object] = None,
):
    """Register a suffix to a conversion class.

    If the parameter class is a string, it is interpreted as known suffix and
    the conversion class of this suffix is registered also for the new one.

    Args:
        suffix: file suffix to identify this file type.
        fclass: Conversion class derived from AbstractFile.
        pclass: Python class that represents this object type.
    """

    if isinstance(fclass, str):
        if pclass is not None:
            raise RuntimeError("Alias %s:%s with default class!" % (suffix, fclass))
        fclass = suffixes[fclass]

    # Simple sanity check for the class interface
    for method in ("encode", "decode", "hash"):
        if not hasattr(fclass, method) or not callable(getattr(fclass, method)):
            raise RuntimeError(
                "No method %s() in class for suffix '%s'!" % (method, suffix)
            )

    # Register suffix
    suffixes[suffix] = fclass

    # Register Python class. Last registration becomes default.
    # Overriding the mapping dict:JsonFile is not allowed.
    if pclass not in classes or pclass is not dict:
        classes[pclass] = fclass

    # Register unknown file format
    if fclass not in formats:
        formats.append(fclass)


# Initialize the conversion class database

for name in ("filebase", "fileimage", "filenumpy", "filehdf5"):
    fullname = __name__ + "." + name
    try:
        module = import_module(fullname)
    except ModuleNotFoundError:
        continue

    for suffix, fclass, pclass in module.register:
        register(suffix, fclass, pclass)


# Inject certain known file formats into the container class
class Container(AbstractContainer):
    """Scientific data container."""

    _suffixes = suffixes
    _classes = classes
    _formats = formats
