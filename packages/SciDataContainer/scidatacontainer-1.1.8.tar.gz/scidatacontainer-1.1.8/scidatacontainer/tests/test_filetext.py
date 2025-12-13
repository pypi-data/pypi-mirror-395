from unittest import TestCase

from . import get_test_container
from scidatacontainer import Container


class FileTextTest(TestCase):

    def test_encode_decode(self):
        a = get_test_container()

        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed "
        text += "do eiusmod tempor incididunt ut labore et dolore magna "
        text += "aliqua. Varius duis at consectetur lorem donec massa. Amet "
        text += "consectetur adipiscing elit ut aliquam purus sit amet. Duis "
        text += "ultricies lacus sed turpis tincidunt id aliquet risus "
        text += "feugiat. Dui id ornare arcu odio ut sem nulla pharetra."

        a["data/test.txt"] = text
        self.assertEqual(text, a["data/test.txt"])

        a.write("test.zdc")

        b = Container(file="test.zdc")

        self.assertEqual(a["data/test.txt"], b["data/test.txt"])
