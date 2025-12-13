import copy
import os

from scidatacontainer import Container

from ._abstract_container_test import AbstractContainerTest


class TestStaticContainer(AbstractContainerTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.items["content.json"]["static"] = True
        cls.items_minimal["content.json"]["static"] = True

    def _compare_with_items(self, dc):
        super()._compare_with_items(dc)
        self._check_timestamp(dc["content.json"]["created"])

        self._check_timestamp(dc["content.json"]["storageTime"])

        self.assertTrue(dc["content.json"]["complete"])

        self.assertTrue(dc["content.json"]["static"])

    def _compare_with_minimal_items(self, dc):
        super()._compare_with_minimal_items(dc)
        self._check_timestamp(dc["content.json"]["created"])

        self._check_timestamp(dc["content.json"]["storageTime"])

        self.assertTrue(dc["content.json"]["complete"])

        self.assertTrue(dc["content.json"]["static"])

    def test_container_creation(self):
        items = copy.deepcopy(self.items)
        items["content.json"]["static"] = True
        dc = Container(items=items)

        self._compare_with_items(dc)
        self.assertTrue(dc["content.json"]["static"])
        self.assertIsNotNone(dc["content.json"]["hash"])

        self.dc = dc

    def test_container_creation_minimal(self):
        items = copy.deepcopy(self.items_minimal)
        items["content.json"]["static"] = True
        dc = Container(items=items)

        self._compare_with_minimal_items(dc)
        self.assertTrue(dc["content.json"]["static"])
        self.assertIsNotNone(dc["content.json"]["hash"])

        self.dc = dc

    def test_freeze(self):
        items = copy.deepcopy(self.items)
        items["content.json"]["static"] = False
        dc = Container(items=items)

        super()._compare_with_items(dc)

        self.assertIsNone(dc["content.json"]["hash"])
        self.assertFalse(dc["content.json"]["static"])

        dc.freeze()

        self._compare_with_items(dc)
        self.assertTrue(dc["content.json"]["static"])
        self.assertIsNotNone(dc["content.json"]["hash"])

        self.dc = dc

    def test_freeze_minimal(self):
        items = copy.deepcopy(self.items_minimal)
        items["content.json"]["static"] = False
        dc = Container(items=items)

        super()._compare_with_minimal_items(dc)

        self.assertIsNone(dc["content.json"]["hash"])
        self.assertFalse(dc["content.json"]["static"])

        dc.freeze()

        self._compare_with_minimal_items(dc)
        self.assertTrue(dc["content.json"]["static"])
        self.assertIsNotNone(dc["content.json"]["hash"])

        self.dc = dc

    def test_write(self, clean=True):
        self.test_freeze()
        self.dc.write(self.export_filename)
        if clean:
            os.remove(self.export_filename)

    def test_read(self):
        self.test_write(clean=False)
        dc = Container(file=self.export_filename)

        self._compare_with_items(dc)

        self.assertTrue(dc["content.json"]["static"])

        old_hash = dc["content.json"]["hash"]
        self.assertIsNotNone(dc["content.json"]["hash"])

        dc.hash()
        self.assertIsNotNone(dc["content.json"]["hash"])
        # new hash is equal with the old one
        self.assertEqual(old_hash, dc["content.json"]["hash"])

    def test_read_wrong_hash(self, clean=True):
        self.test_freeze()
        self.dc.content["hash"] += "ab"
        self.dc.write(self.export_filename)

        with self.assertRaises(RuntimeError) as cm:
            Container(file=self.export_filename)

        self.assertEqual(cm.exception.args[0], "Wrong hash!")

        if clean:
            os.remove(self.export_filename)

    def test_print(self):
        self.test_freeze()
        s = self.dc.__str__()

        self.assertIn("Static Container", s)
        ct = self.items["content.json"]["containerType"]
        self.assertIn("type:        " + ct["name"] + " " + ct["version"]
                      + " (" + ct["id"] + ")", s)
        self.assertIn("uuid:        " + self.dc["content.json"]["uuid"], s)
        self.assertIn("replaces:    " + self.dc["content.json"]["replaces"], s)
        self.assertIn("hash:        " + self.dc["content.json"]["hash"], s)
        self.assertIn("created:     " + self.dc["content.json"]["created"], s)
        self.assertIn("storageTime: " + self.dc["content.json"]["storageTime"],
                      s)
        self.assertIn("author:      " + self.dc["meta.json"]["author"], s)

    def test_immutable(self):
        self.test_freeze()
        with self.assertRaisesRegex(RuntimeError, "Immutable container!"):
            self.dc["data/test.txt"] = "Test123"
