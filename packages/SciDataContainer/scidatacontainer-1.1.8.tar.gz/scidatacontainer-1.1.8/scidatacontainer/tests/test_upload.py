import unittest

from requests import HTTPError

from ._abstract_container_test import has_connection
from .test_single_step_container import AbstractSingleStepContainerTest


class _TestUpload(AbstractSingleStepContainerTest):
    live_server_url = None
    api_key = None
    __test__ = False

    def run(self, result=None):
        if self.__test__:
            return super().run(result)

    def test_upload(self):
        self.test_container_creation()
        uuid = "00000000-0000-0000-0000-000000000000"
        self.dc["content.json"]["uuid"] = uuid
        self.dc.upload(server=self.live_server_url, key=self.api_key)

    def test_no_url(self):
        self.test_container_creation()
        with self.assertRaisesRegex(RuntimeError, "Server URL is missing!"):
            self.dc.upload(server=False, key=self.api_key)

    def test_wrong_url(self):
        self.test_container_creation()
        with self.assertRaisesRegex(ConnectionError, "Connection to server " +
                                    "http://localhost:54321 failed!"):
            self.dc.upload(server="http://localhost:54321", key=self.api_key)

    def test_no_key(self):
        self.test_container_creation()
        with self.assertRaisesRegex(RuntimeError,
                                    "Server API key is missing!"):
            self.dc.upload(key=False)

    def test_wrong_key(self):
        self.test_container_creation()
        with self.assertRaisesRegex(HTTPError,
                                    "401 Client Error: Unauthorized for url:"):
            self.dc.upload(server=self.live_server_url, key="abcd")

    def test_invalid_container(self):
        self.test_container_creation()
        del self.dc["content.json"]["uuid"]
        with self.assertRaisesRegex(HTTPError,
                                    "400 Bad Request: Invalid container " +
                                    "content"):
            self.dc.upload(server=self.live_server_url, key=self.api_key)

    def test_no_write_permissions(self):
        self.test_container_creation()
        uuid = "00000000-0000-0000-0000-000000000403"
        self.dc["content.json"]["uuid"] = uuid
        with self.assertRaisesRegex(HTTPError,
                                    "403 Forbidden: Unauthorized access"):
            self.dc.upload(server=self.live_server_url, key=self.api_key)

    def test_conflicting_uuid(self):
        self.test_container_creation()
        uuid = "00000000-0000-0000-0000-000000000409"
        self.dc["content.json"]["uuid"] = uuid
        with self.assertRaisesRegex(HTTPError,
                                    "409 Conflict: UUID is already existing"):
            self.dc.upload(server=self.live_server_url, key=self.api_key)

    @unittest.expectedFailure
    def test_static_already_exist(self, server=None):
        self.test_container_creation()
        uuid = "00000000-0000-0000-0000-000000000301"
        self.dc["content.json"]["uuid"] = uuid
        self.dc.upload(server=self.live_server_url, key=self.api_key)
        self.assertEqual(self.dc["content.json"]["uuid"], uuid[:-3] + "000")


@unittest.skipUnless(has_connection, "No server conntection available!")
class TestUpload(_TestUpload):
    __test__ = True
