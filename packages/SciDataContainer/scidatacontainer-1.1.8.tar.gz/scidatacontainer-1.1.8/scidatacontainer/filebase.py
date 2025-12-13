##########################################################################
# Copyright (c) 2023 Reinhard Caspary                                    #
# <reinhard.caspary@phoenixd.uni-hannover.de>                            #
# This program is free software under the terms of the MIT license.      #
##########################################################################
#
# This module provides the base data conversion class AbstractFile and
# standard text conversion classes. All data conversion classes should
# inherit from AbstractFile and must provide three methods:
#
# encode(): Return data encoded as bytes string.
# decode(data): Decode and store given bytes string data.
# hash(): Return SHA256 hash from data as hex string.
#
# The hash implementation shoud make sure that semantically equivalent
# data results in the same hash.
#
##########################################################################

from abc import ABC, abstractmethod
import hashlib
import json
import typing


##########################################################################
# Data conversion classes


class AbstractFile(ABC):
    """Base class for converting datatypes to their file representation."""

    def __init__(self, data):
        """Constructor to create an instance of the converter class."""
        if isinstance(data, bytes):
            self.decode(data)
        else:
            self.data = data

    def hash(self) -> str:
        """Return hex digest of SHA256 hash.

        Returns:
            str: Hex digest of this object as string.
        """
        return hashlib.sha256(self.encode()).hexdigest()

    @abstractmethod
    def encode(self) -> bytes:
        """Encode the Container content to bytes. This is an abstract method
        and it needs to be overwritten by inheriting class.

        Returns:
            bytes: Byte string representation of the object.
        """
        pass  # pragma: no cover

    @abstractmethod
    def decode(self, data: bytes):
        """Decode the Container content from bytes. This is an abstract method
        and it neets to be overwritten by inheriting class.
        """
        pass  # pragma: no cover


class BinaryFile(AbstractFile):
    """Data conversion class for a binary file."""

    def encode(self) -> bytes:
        """Return byte string stored in this class.

        Returns:
            bytes: Byte string representation of the object.
        """
        return self.data

    def decode(self, data: bytes):
        """Store bytes in this class."""
        self.data = data


class TextFile(AbstractFile):
    """Data conversion class for a text file."""

    charset = "utf8"
    """charset (str): Character encoding used for translation from text to\
                      bytes."""

    def encode(self) -> bytes:
        """Encode text to bytes string.

        Returns:
            bytes: Byte string representation of the object.
        """

        return bytes(self.data, self.charset)

    def decode(self, data: bytes):
        """Decode text from given bytes string."""

        self.data = data.decode(self.charset)


class JsonFile(AbstractFile):

    """Data conversion class for a JSON file represented as Python
    dictionary."""

    indent = 4
    """indent (int): Indentation of exported JSON files."""
    charset = "utf8"
    """charset (str): Character encoding used for translation from text to\
                      bytes."""

    def sortit(self, data: typing.Union[dict, list, tuple]) -> str:
        """Return compact string representation with keys of all
        sub-dictionaries sorted.

        Args:
            data: Dictionary, list or tuple to convert to string"

        Returns:
            str: String representation of `data`
        """

        if isinstance(data, dict):
            keys = sorted(data.keys())
            data = [k + ": " + self.sortit(data[k]) for k in keys]
            data = ", ".join(data)
            data = "{" + data + "}"
            return data
        elif isinstance(data, (list, tuple)):
            data = [self.sortit(v) for v in data]
            data = ", ".join(data)
            data = "[" + data + "]"
            return data
        return repr(data)

    def hash(self) -> str:
        """Return hex digest of the SHA256 hash calculated from the
        sorted compact representation. This should result in the same
        hash for semantically equal data dictionaries.

        Returns:
            str: Hex digest of this object as string.
        """

        data = bytes(self.sortit(self.data), self.charset)
        return hashlib.sha256(data).hexdigest()

    def encode(self) -> bytes:
        """Convert dictionary to pretty string representation with
        indentation and return it as bytes string.

        Returns:
            bytes: Byte string representation of the object.
        """

        data = json.dumps(
            self.data, sort_keys=True, indent=self.indent, ensure_ascii=False
        )
        return bytes(data, self.charset)

    def decode(self, data: bytes):
        """Decode dictionary from given bytes string."""

        self.data = json.loads(data.decode(self.charset))


class TabSeparatedValuesFile(AbstractFile):
    """Data conversion class for a tab-separated value file."""

    charset = "utf8"
    """charset (str): Character encoding used for translation from a list of\
                      lists to bytes."""

    def encode(self) -> bytes:
        """Encode 2D array (list of lists) to bytes string.

        Returns:
            bytes: Byte string representation of the object.
        """
        s = "\n".join(["\t".join([str(v) for v in a]) for a in self.data])

        return bytes(s, self.charset)

    def decode(self, data: bytes):
        """Decode 2D array (list of lists) from given bytes string."""

        s = data.decode(self.charset)
        self.data = [[float(x) for x in a.split("\t")] for a in s.split("\n")]


register = [
    ("bin", BinaryFile, bytes),
    ("json", JsonFile, dict),
    ("txt", TextFile, str),
    ("log", TextFile, None),
    ("pgm", "txt", None),
    ("tsv", TabSeparatedValuesFile, None),
]
