import os
from unittest import TestCase

from scidatacontainer.config import load_config


class ConfigTest(TestCase):
    def check_cfg_empty(self):
        cfg = load_config("./thisfiledoesntexist.cfg")

        self.assertEqual(cfg["author"], "")
        self.assertEqual(cfg["email"], "")
        self.assertEqual(cfg["server"], "")
        self.assertEqual(cfg["key"], "")

    def test_envvars(self):
        self.check_cfg_empty()

        os.environ["DC_AUTHOR"] = "Maxi Mustermann"
        os.environ["DC_EMAIL"] = "maxi@example.com"
        os.environ["DC_SERVER"] = "http://example.com"
        os.environ["DC_KEY"] = "SECRETKEY"

        cfg = load_config("./thisfiledoesntexist.cfg")

        self.assertEqual(cfg["author"], "Maxi Mustermann")
        self.assertEqual(cfg["email"], "maxi@example.com")
        self.assertEqual(cfg["server"], "http://example.com")
        self.assertEqual(cfg["key"], "SECRETKEY")

    def test_cfg_file(self):
        self.check_cfg_empty()
        tmp_cfg = "./tmp_cfg"

        with open(tmp_cfg, 'w') as f:
            f.write("# Test comment = should be skipped\n")
            f.write("author=Maxi Mustermann\n")
            f.write("email=maxi@example.com\n")
            f.write("server=http://example.com\n")
            f.write("key=\n")
            f.write("key=SECRETKEY\n")
            f.write("key invalid line and should be ignored\n")

        cfg = load_config(tmp_cfg)

        self.assertEqual(cfg["author"], "Maxi Mustermann")
        self.assertEqual(cfg["email"], "maxi@example.com")
        self.assertEqual(cfg["server"], "http://example.com")
        self.assertEqual(cfg["key"], "SECRETKEY")

        os.remove(tmp_cfg)
