import copy
from datetime import datetime, timedelta
import os

from scidatacontainer import Container

from ._abstract_container_test import AbstractContainerTest


class TestMultiStepContainer(AbstractContainerTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.items["content.json"]["static"] = False
        cls.items["content.json"]["complete"] = False
        cls.items_minimal["content.json"]["complete"] = False
        created = datetime.fromisoformat(cls.items["content.json"]["created"])
        created -= timedelta(seconds=1)
        cls.created = created.isoformat(timespec="seconds")
        cls.items["content.json"]["created"] = cls.created
        cls.items_minimal["content.json"]["created"] = cls.created

    def _compare_with_items(self, dc):
        super()._compare_with_items(dc)
        self._check_timestamp(dc["content.json"]["created"])

        self._check_timestamp(dc["content.json"]["storageTime"])

        self.assertFalse(dc["content.json"]["complete"])

        self.assertFalse(dc["content.json"]["static"])

    def _compare_with_minimal_items(self, dc):
        super()._compare_with_minimal_items(dc)
        self._check_timestamp(dc["content.json"]["created"])

        self._check_timestamp(dc["content.json"]["storageTime"])

        self.assertFalse(dc["content.json"]["complete"])

        self.assertFalse(dc["content.json"]["static"])

    def test_container_creation(self):
        items = copy.deepcopy(self.items)
        dc = Container(items=items)

        self._compare_with_items(dc)

        self.dc = dc

    def test_container_creation_minimal(self):
        items = copy.deepcopy(self.items_minimal)
        dc = Container(items=items)

        self._compare_with_minimal_items(dc)

        self.dc = dc

    def test_write(self, clean=True):
        self.test_container_creation()
        self.dc.write(self.export_filename)
        if clean:
            os.remove(self.export_filename)

    def test_read(self):
        self.test_write(clean=False)
        dc = Container(file=self.export_filename)

        self._compare_with_items(dc)

    def test_print(self):
        self.test_container_creation()
        s = self.dc.__str__()

        self.assertIn("Incomplete Container", s)
        ct = self.items["content.json"]["containerType"]
        self.assertIn("type:        " + ct["name"] + " " + ct["version"]
                      + " (" + ct["id"] + ")", s)
        self.assertIn("uuid:        " + self.dc["content.json"]["uuid"], s)
        self.assertIn("replaces:    " + self.dc["content.json"]["replaces"], s)
        self.assertIn("created:     " + self.dc["content.json"]["created"], s)
        self.assertIn("storageTime: " + self.dc["content.json"]["storageTime"],
                      s)
        self.assertIn("author:      " + self.dc["meta.json"]["author"], s)

        self.dc["content.json"]["complete"] = True

        s = self.dc.__str__()

        self.assertIn("Complete Container", s)
        ct = self.items["content.json"]["containerType"]
        self.assertIn("type:        " + ct["name"] + " " + ct["version"]
                      + " (" + ct["id"] + ")", s)
        self.assertIn("uuid:        " + self.dc["content.json"]["uuid"], s)
        self.assertIn("replaces:    " + self.dc["content.json"]["replaces"], s)
        self.assertIn("created:     " + self.dc["content.json"]["created"], s)
        self.assertIn("storageTime: " + self.dc["content.json"]["storageTime"],
                      s)
        self.assertIn("author:      " + self.dc["meta.json"]["author"], s)
