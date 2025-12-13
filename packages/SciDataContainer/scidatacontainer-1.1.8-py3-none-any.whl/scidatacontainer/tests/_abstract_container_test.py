from abc import ABC
from datetime import datetime, timedelta
from unittest import TestCase
import uuid

import requests

import scidatacontainer


class AbstractContainerTest(ABC, TestCase):
    @classmethod
    def setUpClass(cls):
        # Dummy parameters: a dict
        cls.parameter = {
                          "acquisition": {
                                          "acquisitionMode": "SingleFrame",
                                          "exposureAuto": "Off",
                                          "exposureMode": "Timed",
                                          "exposureTime": 19605.0,
                                          "gain": 0.0,
                                          "gainAuto": "Off",
                                          "gainMode": "Default",
                                          "gainSelector": "AnalogAll"
                                          },
                          "device": {
                                     "family": "mvBlueFOX3",
                                     "id": 0,
                                     "product": "mvBlueFOX3-2032aG",
                                     "serial": "FF008343"
                                     },
                          "format": {
                                     "height": 1544,
                                     "offsetX": 0,
                                     "offsetY": 0,
                                     "width": 2064
                                     }
                          }

        cls.data = [[float(i) for i in range(256)] for j in range(128)]
        cls.name = "John Doe"
        cls.email = "john@example.com"
        cls.org = "Example ORG"

        cls.timestamp = scidatacontainer.timestamp()
        cls.items = {
                     "content.json": {
                         "uuid": str(uuid.uuid4()),
                         "replaces": str(uuid.uuid4()),
                         "containerType": {"name": "TestType",
                                           "id": "TestID",
                                           "version": "0.1"
                                           },
                         "usedSoftware": [
                                          {"name": "testSoftware1",
                                           "version": "0.2",
                                           },
                                          {"name": "testSoftware2",
                                           "version": "0.3",
                                           "id": "TestID2",
                                           "idType": "URL",
                                           },
                                          ],
                         "complete": True,
                         "static": False,
                         "created": cls.timestamp,
                         "storageTime": cls.timestamp,
                         },
                     "meta.json": {
                         "author": cls.name,
                         "email": cls.email,
                         "organization": cls.org,
                         "comment": "Example comment",
                         "title": "This is a sample image dataset",
                         "keywords": ["keyword1", "keyword2", "keyword3"],
                         "description": "Example description",
                         "doi": "https://example.com/" + str(uuid.uuid4()),
                         "license": "MIT",
                         "timestamp": cls.timestamp,
                         },
                     "meas/image.tsv": cls.data,
                     "data/parameter.json": cls.parameter,
                     }

        cls.items_minimal = {
                      "content.json": {
                          "containerType": {"name": "TestType"},
                          "usedSoftware": [],
                          },
                      "meta.json": {
                          "author": cls.name,
                          "email": cls.email,
                          "title": "This is a sample image dataset",
                          },
                      "meas/image.tsv": cls.data,
                      "data/parameter.json": cls.parameter,
                      }
        cls.export_filename = "test.zdc"

    def _compare_with_items(self, dc):
        items = self.items
        self.assertEqual(dc["content.json"]["uuid"],
                         items["content.json"]["uuid"])

        self.assertEqual(dc["content.json"]["uuid"],
                         items["content.json"]["uuid"])

        self.assertEqual(items["content.json"]["containerType"],
                         dc["content.json"]["containerType"])

        self.assertEqual(items["content.json"]["usedSoftware"],
                         dc["content.json"]["usedSoftware"])

        self.assertEqual(dc["content.json"]["modelVersion"],
                         scidatacontainer.modelVersion)

        self.assertEqual(items["meta.json"]["author"],
                         dc["meta.json"]["author"])

        self.assertEqual(items["meta.json"]["email"],
                         dc["meta.json"]["email"])

        self.assertEqual(items["meta.json"]["organization"],
                         dc["meta.json"]["organization"])

        self.assertEqual(items["meta.json"]["comment"],
                         dc["meta.json"]["comment"])

        self.assertEqual(items["meta.json"]["title"],
                         dc["meta.json"]["title"])

        self.assertEqual(items["meta.json"]["keywords"],
                         dc["meta.json"]["keywords"])

        self.assertEqual(items["meta.json"]["description"],
                         dc["meta.json"]["description"])

        self.assertEqual(self.timestamp,
                         dc["meta.json"]["timestamp"])

        self.assertEqual(items["meta.json"]["doi"],
                         dc["meta.json"]["doi"])

        self.assertEqual(items["meta.json"]["license"],
                         dc["meta.json"]["license"])

        self.assertEqual(dc["meas/image.tsv"],
                         self.data)

        self.assertEqual(dc["data/parameter.json"],
                         self.parameter)

    def _compare_with_minimal_items(self, dc):
        items = self.items_minimal
        # check if uuid is a valid uuid
        self.assertTrue(isinstance(dc["content.json"]["uuid"], str))
        self.assertEqual(dc["content.json"]["uuid"],
                         str(uuid.UUID(dc["content.json"]["uuid"])))

        self.assertIsNone(dc["content.json"]["replaces"])

        self.assertEqual(items["content.json"]["containerType"],
                         dc["content.json"]["containerType"])

        self.assertEqual(items["content.json"]["usedSoftware"],
                         dc["content.json"]["usedSoftware"])

        self.assertEqual(dc["content.json"]["modelVersion"],
                         scidatacontainer.modelVersion)

        self.assertEqual(items["meta.json"]["author"],
                         dc["meta.json"]["author"])

        self.assertEqual(items["meta.json"]["email"],
                         dc["meta.json"]["email"])

        self.assertEqual("",
                         dc["meta.json"]["organization"])

        self.assertEqual("",
                         dc["meta.json"]["comment"])

        self.assertEqual(items["meta.json"]["title"],
                         dc["meta.json"]["title"])

        self.assertEqual([],
                         dc["meta.json"]["keywords"])

        self.assertEqual("",
                         dc["meta.json"]["description"])

        self.assertEqual("",
                         dc["meta.json"]["timestamp"])

        self.assertEqual("",
                         dc["meta.json"]["doi"])

        self.assertEqual("",
                         dc["meta.json"]["license"])

        self.assertEqual(dc["meas/image.tsv"],
                         self.data)

        self.assertEqual(dc["data/parameter.json"],
                         self.parameter)

    def _check_timestamp(self, timestamp):
        t1 = datetime.fromisoformat(timestamp)
        t2 = datetime.fromisoformat(self.timestamp)
        self.assertTrue(abs(t1 - t2) < timedelta(seconds=2))


def _check_server_connection():
    cfg = scidatacontainer.config.load_config()
    if (cfg["server"] == "") or (cfg["key"] == ""):
        return False

    try:
        response = requests.get(cfg["server"] + "/api/datasets/",
                                headers={"Authorization": "Token " +
                                                          cfg["key"]})
    except requests.exceptions.ConnectionError:
        return False
    return response.status_code == 200


has_connection = _check_server_connection()
