##########################################################################
# Copyright (c) 2023-2024 Reinhard Caspary                               #
# <reinhard.caspary@phoenixd.uni-hannover.de>                            #
# This program is free software under the terms of the MIT license.      #
##########################################################################
#
# This module provides the Scientific Data Container as class
# DataContainer which may be stored or uploaded as a ZIP package
# containing items (files). Do not use this class directly! Use the
# class Container provided by the package scidatacontainer instead.
#
##########################################################################

import copy
import hashlib
import io
import json
import typing
import uuid
from abc import ABC
from datetime import datetime, timezone
from types import SimpleNamespace
from zipfile import ZIP_DEFLATED, ZipFile

import requests

from .config import load_config
from .filebase import BinaryFile, JsonFile, TextFile

# Version of the implemented data model
MODELVERSION = "1.0.0"


##########################################################################
# Timestamp function


def timestamp() -> str:
    """Return the current ISO 8601 compatible timestamp as string.

    Returns:
        str: timestamp as string
    """
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


##########################################################################
# Data container class


class AbstractContainer(ABC):
    """Scientific data container with minimal file support.

    The following file types are supported:
        - .json <-> dict
        - .txt <-> str
        - .bin <-> bytes
    """

    _config = None
    _suffixes = {"json": JsonFile, "txt": TextFile, "bin": BinaryFile}
    _classes = {dict: JsonFile, str: TextFile, bytes: BinaryFile}
    _formats = [TextFile]

    def __init__(
        self,
        items: dict = None,
        file: str = None,
        uuid: str = None,
        config: dict = None,
        compression: int = ZIP_DEFLATED,
        compresslevel: int = -1,
        **kwargs,
    ):
        """Construct a DataContainer object.

        It will try the following in the specified order:
            - Create a new DataContainer if items is passed as argument.
            - Load local DataContainer from hard drive if file is passed.
            - Download a DataContainer from a server if uuid is passed.

        Args:
            items: Dictionary of items to build a new DataContainer.
            file: Filename to read a DataContainer from local hard drive.
            uuid: UUID of a Container to download from a server instance.
            author: Author name for meta.json
            email: Author email for meta.json
            server: URL of the server instance providing the Container.
            key: API-Key from the server to identify yourself.
            compression: Numeric constant for the compression method
            compresslevel: Level of compression, 0-fastest, 9-best compression
        """
        self.kwargs = {
            "items": items,
            "file": file,
            "uuid": uuid,
            "config": config,
            "compression": compression,
            "compresslevel": compresslevel,
        }
        self.kwargs.update(kwargs)

        self.__pre_init__()

        # Load variables from kwargs in namespace
        n = SimpleNamespace(**self.kwargs)

        # Container must be mutable initially
        self.mutable = True

        # Load configuration
        if n.config is not None:
            self._config = dict(n.config)
        else:
            self._config = load_config()

        # Store all items in the container
        if n.items is not None:
            self._store(n.items, True, False)
            self.mutable = not self["content.json"]["static"]

        # Load local container file
        elif n.file is not None:
            self._read(fn=n.file)

        # Download container from server
        elif n.uuid is not None:
            server = self._config["server"]
            key = self._config["key"]
            self._download(uuid=n.uuid, server=server, key=key)

        # No data source
        else:
            raise RuntimeError("No data!")

        self.compression = n.compression
        self.compresslevel = n.compresslevel

        # Check validity of author ORCID
        self._norm_orcid()

        self.__post_init__()

    def __pre_init__(self):
        """Manipulate the container before initialization.

        This method can be overwritten by inheriting classes to manipulate the
        container object or the arguments passed to __init__ before the
        arguments are processed in __init__. To do so, manipulate the
        dictionary self.kwargs inside this function.
        """

    def __post_init__(self):
        """Manipulate the container after initialization.

        This method can be overwritten by inheriting classes to manipulate the
        container object after __init__ is executed. This might be useful to
        implement custom checks after creation of a container.
        """

    def _store(self, items, validate=True, strict=True):
        """Store all items in the container."""
        # Add all items in the container
        self._items = {}
        mutable = self.mutable
        self.mutable = True
        for path, data in items.items():
            self[path] = data

        # Make sure that the items content.json and meta.json exist and
        # contain all required attributes
        if "content.json" not in self:
            raise RuntimeError("Item 'content.json' is missing!")
        if "meta.json" not in self:
            raise RuntimeError("Item 'meta.json' is missing!")
        if validate:
            self.validate_content()
            self.validate_meta()

        if self["content.json"]["static"] and not self["content.json"]["hash"]:
            self.hash()

        # Check validity of hash
        if strict and self["content.json"]["hash"]:
            oldhash = self["content.json"]["hash"]
            self.hash()
            if self["content.json"]["hash"] != oldhash:
                raise RuntimeError("Wrong hash!")

        # Restore mutable flag
        self.mutable = mutable

    @property
    def content(self) -> dict:
        return self["content.json"]

    @content.setter
    def content(self, value: dict):
        self["content.json"] = value

    @property
    def meta(self) -> dict:
        return self["meta.json"]

    @meta.setter
    def meta(self, value: dict):
        self["meta.json"] = value

    @property
    def uuid(self) -> str:
        return self["content.json"]["uuid"]

    def __contains__(self, path):
        """Return true, if the given path matches an item in this container."""
        return path in self._items

    def __setitem__(self, path, data):
        """Store data as a container item."""
        # Immutable container must not be modified
        if not self.mutable:
            raise RuntimeError("Immutable container!")

        # Get file extension
        ext = path.rsplit(".", 1)[1]

        # Unregistered file extension
        if ext not in self._suffixes:
            # Try to convert bytes. Default is BinaryFile.
            if isinstance(data, bytes):
                for cls in self._formats:
                    try:
                        item = cls(data)
                        break
                    except Exception:
                        pass
                else:
                    item = BinaryFile(data)

            # Other Python object must be registered
            else:
                if type(data) in self._classes:
                    cls = self._classes[type(data)]
                    item = cls(data)
                else:
                    raise RuntimeError(
                        "No matching file format found for "
                        + "item '%s'!" % path
                    )

        # Registered file extension
        else:
            cls = self._suffixes[ext]
            item = cls(data)

        # Store conversion object containing data
        self._items[path] = item

    def __getitem__(self, path):
        """Get the data content of a container item."""
        if path in self:
            return self._items[path].data
        raise KeyError("Unknown item '%s'!" % path)

    def validate_content(self):
        """Make sure that the item "content.json" exists and contains
        all required attributes.
        """
        # Get a copy of the item "content.json"
        content = copy.deepcopy(self["content.json"])

        # Keep UUID of a multi-step container and create a new one otherwise
        if "uuid" not in content or not content["uuid"]:
            content["uuid"] = str(uuid.uuid4())

        # The optional attribute 'replace' contains the UUID of the
        # predecessor of this container. It replaces the former one,
        # which must have the same containerType and owner and a smaller
        # or equal creation time. The replacement feature should only be
        # used for minor data modifications (e.g. additional keywords or
        # comment in meta.json). The server returns always the latest
        # version.
        if "replaces" not in content:
            content["replaces"] = None

        # The attribute 'containerType' is a dictionary which must at
        # least contain the type of the container as short string
        # without spaces. If the container type is standardized, it must
        # also contain a type id and a version string.
        if "containerType" not in content:
            raise RuntimeError("Attribute 'containerType' is missing!")
        ptype = content["containerType"]
        if not isinstance(ptype, dict):
            raise RuntimeError("Attribute containerType is no dictionary!")
        if "name" not in ptype:
            raise RuntimeError("Name of containerType is missing!")
        if "id" in ptype and "version" not in ptype:
            raise RuntimeError("Version of containerType is missing!")

        # The boolean attribute 'static' is required. Default is False.
        if "static" in content:
            content["static"] = bool(content["static"])
        else:
            content["static"] = False

        # The boolean attribute 'complete' is required. Default is True.
        if not content["static"] and "complete" in content:
            content["complete"] = bool(content["complete"])
        else:
            content["complete"] = True

        # Current time
        ts = timestamp()

        # The attribute 'created' is required. It is created
        # automatically for a new dataset.
        if "created" not in content or not content["created"]:
            content["created"] = ts

        # The attribute 'storageTime' is updated automatically when the
        # container is stored
        if "storageTime" not in content or not content["complete"]:
            content["storageTime"] = ts

        # The attribute 'hash' is optional
        if "hash" not in content or not content["hash"]:
            content["hash"] = None

        # The attribute 'usedSoftware' is a list of dictionaries, which
        # may be empty. Each dictionary must contain atleast the items
        # "name" and "version" specifying name and version of a
        # software. It may also contain the items "id" and "idType"
        # specifying a reference id (e.g. GitHub-URL) and its type.
        if "usedSoftware" not in content or not content["usedSoftware"]:
            content["usedSoftware"] = []
        for sw in content["usedSoftware"]:
            if "name" not in sw:
                raise RuntimeError("Software name is missing!")
            if "version" not in sw:
                raise RuntimeError("Software version is missing!")
            if "id" in sw and "idType" not in sw:
                raise RuntimeError("Type of software reference id is missing!")

        # Version of the data model provided by this package
        content["modelVersion"] = MODELVERSION

        # Store the item "content.json"
        self["content.json"] = content

    def validate_meta(self):
        """Make sure that the item "meta.json" exists and contains all
        required attributes."""
        # Get a copy of the item "meta.json"
        meta = copy.deepcopy(self["meta.json"])

        # Author name is required
        if "author" not in meta:
            meta["author"] = self._config["author"]
        if not meta["author"]:
            raise RuntimeError("Author name is missing!")

        # Author email address is required
        if "email" not in meta:
            meta["email"] = self._config["email"]

        # Author ORCiD is optional
        if "orcid" not in meta:
            meta["orcid"] = self._config["orcid"]

        # Author affiliation is optional
        if "organization" not in meta:
            meta["organization"] = self._config["organization"]

        # Comment on dataset is optional
        if "comment" not in meta:
            meta["comment"] = ""

        # Title of dataset is required
        if "title" not in meta:
            meta["title"] = ""
        if not meta["title"]:
            raise RuntimeError("Data title is missing!")

        # List of keywords is optional
        if "keywords" not in meta:
            meta["keywords"] = []

        # Description of dataset is optional
        if "description" not in meta:
            meta["description"] = ""

        # Data creation time is optional
        if "timestamp" not in meta:
            meta["timestamp"] = ""

        # Data DOI is optional
        if "doi" not in meta:
            meta["doi"] = ""

        # Data license name is optional
        if "license" not in meta:
            meta["license"] = ""

        # Store the item "meta.json"
        self["meta.json"] = meta

    def __delitem__(self, path):
        """Delete the given item."""
        # Immutable container must not be modified
        if not self.mutable:
            raise RuntimeError("Immutable container!")

        # Delete item
        if path in self:
            del self._items[path]

    def keys(self) -> typing.List[str]:
        """Return a sorted list of the full paths of all items.

        Returns:
            typing.List[str]: List of paths of Container items.
        """
        return sorted(self._items.keys())

    def values(self) -> typing.List:
        """Return a list of all item objects.

        Returns:
            typing.List: List of item objects of the Container.
        """
        return [self[k] for k in self.keys()]

    def items(self):
        """Return this container as a dictionary of item objects (key, value)
        tuples.
        """
        return {k: self[k] for k in self.keys()}

    def hash(self):
        """Calculate and save the hash value of this container."""
        # Some attributes of content.json are excluded from the hash
        # calculation
        save = ("uuid", "created", "storageTime")
        save = {k: self["content.json"][k] for k in save}
        for key in save:
            self["content.json"][key] = None
        self["content.json"]["hash"] = None

        # Calculate and store hash of this container
        hashes = [self._items[p].hash() for p in sorted(self.items())]
        myhash = hashlib.sha256(" ".join(hashes).encode("ascii")).hexdigest()
        self["content.json"]["hash"] = myhash

        # Restore excluded attributes
        for key, value in save.items():
            self["content.json"][key] = value

        # Make container immutable
        self.mutable = False
        self["content.json"]["storageTime"] = timestamp()

    def freeze(self):
        """Calculate the hash value of this container and make it
        static. The container cannot be modified any more when this
        method was called once."""
        self["content.json"]["static"] = True
        self["content.json"]["complete"] = True
        self.hash()

    def release(self):
        """Make this container mutable. If it was immutable, this method
        will create a new UUID and initialize the attributes replaces,
        createdstorageTime and modelVersion in the item "content.json".
        It will also delete an existing hash and make it a new
        container."""
        # Do nothing if the container is already mutable
        if self.mutable:
            return
        self.mutable = True

        # Remove and initialize certain container attributes
        content = self["content.json"]
        content["static"] = False
        content["complete"] = True
        for key in ("uuid", "replaces", "created", "storageTime", "hash"):
            content.pop(key, None)
        self.validate_content()

    def encode(self):
        """Encode container as ZIP package. Return package as binary
        string.
        """

        # Check/format of author ORCID
        self._norm_orcid()

        items = {p: self._items[p].encode() for p in self.items()}
        with io.BytesIO() as f:
            with ZipFile(
                f,
                "w",
                compression=self.compression,
                compresslevel=self.compresslevel,
            ) as fp:
                for path in sorted(items.keys()):
                    fp.writestr(path, items[path])
            f.seek(0)
            data = f.read()
        return data

    def decode(self, data: bytes, validate: bool = True, strict: bool = True):
        """Take ZIP package as binary string. Read items from the
        package and store them in this object.

        Arguments:
            data: Bytestring containing the ZIP DataContainer.
            validate: If true, validate the content.
            strict: If true, validate the hash, too.
        """
        with io.BytesIO() as f:
            f.write(data)
            f.seek(0)
            with ZipFile(f, "r") as fp:
                items = {p: fp.read(p) for p in fp.namelist()}
        self._store(items, validate, strict)

    def write(self, fn: str, data: bytes = None):
        """Write the container to a ZIP package file.

        If data is passed to the function, data will be written to the file.
        Otherwise the byte representation of the class instance will be written
        to the file, which is what you typically want.

        Args:
            fn: Filename of export file.
            data: If given, data to write to the file.
        """
        if self.mutable:
            self["content.json"]["storageTime"] = timestamp()
        if data is None:
            data = self.encode()
        with open(fn, "wb") as fp:
            fp.write(data)
        self.mutable = not (
            self["content.json"]["static"] or self["content.json"]["complete"]
        )

    def _read(self, fn, strict=True):
        """Read a ZIP package file and store it as container in this
        object.
        """
        with open(fn, "rb") as fp:
            data = fp.read()
        self.decode(data, False, strict)
        self.mutable = not (
            self["content.json"]["static"] or self["content.json"]["complete"]
        )

    def upload(self, data: bytes = None, server: str = None, key: str = None):
        """Create a ZIP archive of the DataContainer and upload it to a server.

        If data is passed to the function, data will be written to the file.
        Otherwise the byte representation of the class instance will be written
        to the file, which is what you typically want.

        Args:
            data: If given, data to write to the file.
            server: URL of the server.
            key: API Key from the server to identify yourself.
        """
        # Server name is required and must be provided either via config
        # file, environment variable or method parameter
        if server is None:
            server = self._config["server"]
        if not server:
            raise RuntimeError("Server URL is missing!")

        # API key is required and must be provided either via config
        # file, environment variable or method parameter
        if key is None:
            key = self._config["key"]
        if not key:
            raise RuntimeError("Server API key is missing!")

        # Upload container as byte string
        if self.mutable:
            self["content.json"]["storageTime"] = timestamp()
        if data is None:
            data = self.encode()
        try:
            response = requests.post(
                server + "/api/datasets/",
                files={"uploadfile": data},
                headers={"Authorization": "Token " + key},
            )
        except Exception:
            response = None
        if response is None:
            raise ConnectionError("Connection to server %s failed!" % server)

        # HTTP status code 409 is returned when a dataset is already
        # available on the server. Static datasets require a special
        # treatment: The current dataset is replaced by the one from the
        # server.
        if response.status_code == 400:
            if self["content.json"]["static"]:
                data = json.loads(response.content.decode("UTF-8"))
                if isinstance(data, dict) and data["static"]:
                    self._download(uuid=data["id"], server=server, key=key)
                    return
            raise requests.HTTPError(
                "400 Bad Request: Invalid container " + "content"
            )

        # Unauthorized access
        elif response.status_code == 403:
            raise requests.HTTPError("403 Forbidden: Unauthorized access")

        # Duplicate UUID
        elif response.status_code == 409:
            raise requests.HTTPError("409 Conflict: UUID is already existing")

        # Invalid container format
        elif response.status_code == 415:
            raise requests.HTTPError(
                "415 Unsupported: Invalid container" + "format"
            )

        # Standard exception handler for other HTTP status codes
        else:
            response.raise_for_status()

        # Make container immutable
        self.mutable = not (
            self["content.json"]["static"] or self["content.json"]["complete"]
        )

    def _download(self, uuid, strict=True, server=None, key=None):
        # Server name is required and must be provided either via config
        # file, environment variable or method parameter
        if server is None:
            server = self._config["server"]
        if not server:
            raise RuntimeError("Server URL is missing!")

        # API key is required and must be provided either via config
        # file, environment variable or method parameter
        if key is None:
            key = self._config["key"]
        if not key:
            raise RuntimeError("Server API key is missing!")

        # Download container as byte stream from the server
        try:
            url = server + "/api/datasets/" + uuid + "/download/"
            response = requests.get(
                url, headers={"Authorization": "Token " + key}
            )
        except Exception:
            response = None
        if response is None:
            raise ConnectionError("Connection to server %s failed!" % server)
        data = response.content

        # Valid dataset: Store in this container
        if response.status_code == 200:
            self.decode(data, False, strict)

        # Deleted dataset: Raise exception
        elif response.status_code == 204:
            raise requests.HTTPError("204 No Content: Deleted dataset")

        # Replaced dataset: Store in this container
        elif response.status_code == 301:
            self.decode(data, strict)

        # Unauthorized access
        elif response.status_code == 403:
            raise requests.HTTPError("403 Forbidden: Unauthorized access")

        # Unknown dataset: Raise exception
        elif response.status_code == 404:
            raise requests.HTTPError("404 Not Found: Unknown dataset")

        # Standard exception handler for other HTTP status codes
        else:
            response.raise_for_status()

        # Make container immutable
        self.mutable = not (
            self["content.json"]["static"] or self["content.json"]["complete"]
        )

    def __str__(self):
        content = self["content.json"]
        meta = self["meta.json"]

        if content["static"]:
            ctype = "Static Container"
        elif content["complete"]:
            ctype = "Complete Container"
        else:
            ctype = "Incomplete Container"

        s = [ctype]
        ptype = content["containerType"]
        name = ptype["name"]
        if "id" in ptype:
            name = "%s %s (%s)" % (name, ptype["version"], ptype["id"])
        s.append("  type:        " + name)
        s.append("  uuid:        " + content["uuid"])
        if content["replaces"]:
            s.append("  replaces:    " + content["replaces"])
        if content["hash"]:
            s.append("  hash:        " + content["hash"])
        s.append("  created:     " + content["created"])
        s.append("  storageTime: " + content["storageTime"])
        s.append("  author:      " + meta["author"])

        return "\n".join(s)

    def _norm_orcid(self, orcid: typing.Optional[str] = None) -> None:
        """Set ORCID to normalized string if the given string is a valid ORCiD
        or to an empty string otherwise."""

        if orcid is None:
            orcid = self["meta.json"]["orcid"]

        assert isinstance(orcid, str)

        # Pick all digits and normalize
        orcid = orcid.replace("-", "").replace(" ", "").upper()
        if len(orcid) != 16:
            self["meta.json"]["orcid"] = ""
            return

        # Check if ORCID is in the correct number space.
        try:
            orcid_number = int(orcid[:-1])
        except ValueError:
            self["meta.json"]["orcid"] = ""
            return

        if not (
            (15000000 <= int(orcid_number) <= 35000000)
            or (900000000000 <= int(orcid_number) <= 900100000000)
        ):
            self["meta.json"]["orcid"] = ""
            return

        # Calculate checksum product
        r = 2
        m = 11
        try:
            product = 0
            for digit in orcid[:-1]:
                product = ((int(digit) + product) * r) % m
        except ValueError:
            self["meta.json"]["orcid"] = ""
            return

        # Calculate checksum digit
        checksum = (m + 1 - product) % m
        check = "0123456789X"[checksum]
        if orcid[-1] != check:
            self["meta.json"]["orcid"] = ""
            return

        # Valid ORCID. Set orcid variable to formatted string
        self["meta.json"]["orcid"] = (
            orcid[:4] + "-" + orcid[4:8] + "-" + orcid[8:12] + "-" + orcid[12:]
        )
