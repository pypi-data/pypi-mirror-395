import os
from io import BytesIO
from unittest import TestCase
from zipfile import ZipFile

import h5py
import numpy as np

from scidatacontainer import Container

from . import get_test_container


class FileHdf5Test(TestCase):
    def test_encode_decode(self):
        a = get_test_container()

        data = np.random.randint(0, 256, (100, 100, 3))

        a["data/test.hdf5"] = data

        a.write("test.zdc")

        b = Container(file="test.zdc")
        self.assertTrue(np.allclose(a["data/test.hdf5"], b["data/test.hdf5"]))

    def test_file_content(self):
        a = get_test_container()

        data = np.random.randint(0, 256, (100, 100, 3))

        a["data/test.hdf5"] = data

        a.write("test.zdc")

        with ZipFile("test.zdc") as zfile:
            with BytesIO(zfile.read("data/test.hdf5")) as fp:
                with h5py.File(fp) as h5file:
                    self.assertTrue(np.allclose(a["data/test.hdf5"], h5file["dataset"]))
