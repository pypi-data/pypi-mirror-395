##########################################################################
# Copyright (c) 2023 Reinhard Caspary                                    #
# <reinhard.caspary@phoenixd.uni-hannover.de>                            #
# This program is free software under the terms of the MIT license.      #
##########################################################################
#
# This module provides data conversion classes for image files. All
# data conversion classes should inherit from filebase.AbstractFile and must
# provide three methods:
#
# encode(): Return data encoded as bytes string.
# decode(data): Decode and store given bytes string data.
# hash(): Return SHA256 hash from data as hex string.
#
# The hash implementation shoud make sure that semantically equivalent
# data results in the same hash.
#
##########################################################################

import io

import numpy as np

from .filebase import AbstractFile


class NpyFile(AbstractFile):
    """Data conversion class for NumPy arrays (ndarray)."""

    allow_pickle = False

    def encode(self):
        """Convert NumPy array to bytes string."""

        with io.BytesIO() as fp:
            np.save(fp, self.data, allow_pickle=self.allow_pickle)
            fp.seek(0)
            data = fp.read()
        return data

    def decode(self, data):
        """Decode NumPy array from bytes string."""

        with io.BytesIO() as fp:
            fp.write(data)
            fp.seek(0)
            self.data = np.load(fp, allow_pickle=self.allow_pickle)


register = [
    ("npy", NpyFile, np.ndarray),
]
