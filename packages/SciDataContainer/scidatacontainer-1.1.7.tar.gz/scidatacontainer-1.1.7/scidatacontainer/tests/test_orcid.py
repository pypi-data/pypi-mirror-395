import copy
import os

from scidatacontainer import Container

from ._abstract_container_test import AbstractContainerTest


class TestORCID(AbstractContainerTest):
    def test_valid_orcid(self):
        orcid = "0000-0002-9079-593X"
        items = copy.deepcopy(self.items)
        dc = Container(items=items, config={"orcid": orcid})

        self._compare_with_items(dc)
        self.assertEqual(dc.meta["orcid"], orcid)

    def test_format_orcid(self):
        orcid = "0000-0002-9079-593X"
        items = copy.deepcopy(self.items)
        dc = Container(
            items=items, config={"orcid": orcid.replace("-", "").lower()}
        )

        self._compare_with_items(dc)
        self.assertEqual(dc.meta["orcid"], orcid)

    def test_length_orcid(self):
        orcid = "00-0002-9079-593X"
        items = copy.deepcopy(self.items)
        dc = Container(
            items=items, config={"orcid": orcid.replace("-", "").lower()}
        )

        self._compare_with_items(dc)
        self.assertEqual(dc.meta["orcid"], "")

    def test_num_space_orcid(self):
        for orcid in [
            "0000-0001-5000-0007",
            "0000-0003-5000-0001",
            "0009-0000-0000-0009",
            "0009-0010-0000-0003",
        ]:
            items = copy.deepcopy(self.items)
            dc = Container(items=items, config={"orcid": orcid})
            self._compare_with_items(dc)
            self.assertEqual(dc.meta["orcid"], orcid)

        # Check first ORCID outside the range of valid numbers
        for orcid in [
            "0000-0001-4999-9992",
            "0000-0003-5000-001X",
            "0008-9999-9999-9996",
            "0009-0010-0000-0011",
        ]:
            items = copy.deepcopy(self.items)
            dc = Container(items=items, config={"orcid": orcid})
            self._compare_with_items(dc)
            self.assertEqual(dc.meta["orcid"], "")

    def test_invalid_orcid(self):
        orcid = "0000-0001-5000-0X07"
        items = copy.deepcopy(self.items)
        dc = Container(items=items, config={"orcid": orcid})
        self._compare_with_items(dc)
        self.assertEqual(dc.meta["orcid"], "")

    def test_invalid_checksum(self):
        orcid = "0000-0002-9079-5930"
        items = copy.deepcopy(self.items)
        dc = Container(items=items, config={"orcid": orcid})
        self._compare_with_items(dc)
        self.assertEqual(dc.meta["orcid"], "")

    def test_write_read(self, clean=True):
        orcid = "0000-0002-9079-593X"
        items = copy.deepcopy(self.items)
        dc = Container(items=items, config={"orcid": orcid})
        self._compare_with_items(dc)
        self.assertEqual(dc.meta["orcid"], orcid)
        dc.write(self.export_filename)

        dc2 = Container(file=self.export_filename)
        self._compare_with_items(dc2)
        self.assertEqual(dc2.meta["orcid"], orcid)

        if clean:
            os.remove(self.export_filename)
