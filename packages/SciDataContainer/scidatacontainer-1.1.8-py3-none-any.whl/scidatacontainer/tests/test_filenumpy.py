from unittest import TestCase

import numpy as np

from . import get_test_container
from scidatacontainer import Container, register
from scidatacontainer.filenumpy import NpyFile


class FileNumpyTest(TestCase):

    def test_encode_decode(self):
        a = get_test_container()
        register("npx", NpyFile)

        data = np.random.randint(0, 256, (100, 100, 3))

        a["data/test.npx"] = data

        a.write("test.zdc")

        b = Container(file="test.zdc")

        self.assertTrue(np.allclose(a["data/test.npx"], b["data/test.npx"]))
