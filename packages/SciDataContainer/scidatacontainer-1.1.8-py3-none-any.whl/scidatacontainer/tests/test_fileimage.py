from unittest import TestCase

import numpy as np

from . import get_test_container
from scidatacontainer import Container, register
from scidatacontainer.fileimage import PngFile


class FileImageTest(TestCase):

    def test_encode_decode(self):
        a = get_test_container()
        register("png", PngFile)
        data = np.random.randint(0, 256, (100, 100, 3))

        a["data/test.png"] = data

        a.write("test.zdc")

        b = Container(file="test.zdc")

        self.assertTrue(np.allclose(a["data/test.png"], b["data/test.png"]))
