from unittest import TestCase

from jsonschema.exceptions import ValidationError

from scidatacontainer.jsonschema import content, meta, validate,\
                                        VERSIONS_AVAILABLE


from scidatacontainer.tests import get_test_container


class JSONSchemaTest(TestCase):
    def test_content(self):
        self.assertIsInstance(content, dict)

        self.assertEqual(len(VERSIONS_AVAILABLE), len(content))

        for v in VERSIONS_AVAILABLE:
            self.assertIn(v, content.keys())

    def test_meta(self):
        self.assertIsInstance(meta, dict)

        self.assertEqual(len(VERSIONS_AVAILABLE), len(meta))

        for v in VERSIONS_AVAILABLE:
            self.assertIn(v, meta.keys())

    def test_validate_content(self):
        a = get_test_container()
        validate(a["content.json"],
                 schema=content[VERSIONS_AVAILABLE[-1]],
                 schema_name="content")

    def test_validate_meta(self):
        a = get_test_container()
        validate(a["meta.json"],
                 schema=meta[VERSIONS_AVAILABLE[-1]],
                 schema_name="meta")

    def test_validate_missing_attribute(self):
        a = get_test_container()
        del a["content.json"]["complete"]
        with self.assertRaises(ValidationError) as cm:
            validate(a["content.json"],
                     schema=content[VERSIONS_AVAILABLE[-1]],
                     schema_name="content")

        self.assertEqual(cm.exception.message,
                         "'complete' is a required property in content.json.")

        with self.assertRaises(ValidationError) as cm:
            validate(a["content.json"],
                     schema=content[VERSIONS_AVAILABLE[-1]],
                     schema_name="content",
                     translate=False)

        self.assertEqual(cm.exception.message,
                         "'complete' is a required property")

        a = get_test_container()
        del a["meta.json"]["author"]
        with self.assertRaises(ValidationError) as cm:
            validate(a["meta.json"],
                     schema=meta[VERSIONS_AVAILABLE[-1]],
                     schema_name="meta")

        self.assertEqual(cm.exception.message,
                         "'author' is a required property in meta.json.")

    def test_validate_wrong_type(self):
        a = get_test_container()
        a["content.json"]["complete"] = "True"
        with self.assertRaises(ValidationError) as cm:
            validate(a["content.json"],
                     schema=content[VERSIONS_AVAILABLE[-1]],
                     schema_name="content")

        self.assertEqual(cm.exception.message,
                         "Value of 'complete' in content.json has the wrong " +
                         "type: 'True' is not of type 'boolean'.")

        a = get_test_container()
        a["content.json"]["created"] = 42
        with self.assertRaises(ValidationError) as cm:
            validate(a["content.json"],
                     schema=content[VERSIONS_AVAILABLE[-1]],
                     schema_name="content")

        self.assertEqual(cm.exception.message,
                         "Value of 'created' in content.json has the wrong " +
                         "type: 42 is not of type 'string'.")

    def test_validate_wrong_format(self):
        a = get_test_container()
        a["content.json"]["uuid"] = "test123"
        with self.assertRaises(ValidationError) as cm:
            validate(a["content.json"],
                     schema=content[VERSIONS_AVAILABLE[-1]],
                     schema_name="content")

        self.assertEqual(cm.exception.message,
                         "Value of 'uuid' in content.json has the wrong " +
                         "format: 'test123' is not a 'uuid'.")

        a = get_test_container()
        a["content.json"]["created"] = "test123"
        with self.assertRaises(ValidationError) as cm:
            validate(a["content.json"],
                     schema=content[VERSIONS_AVAILABLE[-1]],
                     schema_name="content")

        self.assertEqual(cm.exception.message,
                         "Value of 'created' in content.json has the wrong " +
                         "format: 'test123' is not a 'date-time'.")

        validate(a["content.json"],
                 schema=content[VERSIONS_AVAILABLE[-1]],
                 schema_name="content",
                 check_format=False)

        a = get_test_container()
        a["meta.json"]["email"] = "test123"
        with self.assertRaises(ValidationError) as cm:
            validate(a["meta.json"],
                     schema=meta[VERSIONS_AVAILABLE[-1]],
                     schema_name="meta")

        self.assertEqual(cm.exception.message,
                         "Value of 'email' in meta.json has the wrong " +
                         "format: 'test123' is not a 'email'.")

        a = get_test_container()
        a["content.json"]["hash"] = "test"
        with self.assertRaises(ValidationError) as cm:
            validate(a["content.json"],
                     schema=content[VERSIONS_AVAILABLE[-1]],
                     schema_name="content")

        self.assertEqual(cm.exception.message,
                         "Value of 'hash' in content.json has the wrong " +
                         "format: A hash can only contain hex digits (0-9, " +
                         "a-f and A-F).")

        a = get_test_container()
        a["content.json"]["modelVersion"] = "1.bcd.2.3"
        with self.assertRaises(ValidationError) as cm:
            validate(a["content.json"],
                     schema=content[VERSIONS_AVAILABLE[-1]],
                     schema_name="content")

        self.assertEqual(cm.exception.message,
                         "Value of 'modelVersion' in content.json has the " +
                         "wrong format: A model version only contains digits" +
                         " and dots.")

    def test_guess_schema(self):
        a = get_test_container()
        a["content.json"]["uuid"] = "test123"
        with self.assertRaises(ValidationError) as cm:
            validate(a["content.json"])

        self.assertEqual(cm.exception.message,
                         "Value of 'uuid' in content.json has the wrong " +
                         "format: 'test123' is not a 'uuid'.")

        a["meta.json"]["timestamp"] = "test123"
        with self.assertRaises(ValidationError) as cm:
            validate(a["meta.json"])

        self.assertEqual(cm.exception.message,
                         "Value of 'timestamp' in meta.json has the wrong " +
                         "format: 'test123' is not a 'date-time'.")

    def test_static_requires_hash(self):
        a = get_test_container()
        a.freeze()
        validate(a["content.json"],
                 schema=content[VERSIONS_AVAILABLE[-1]],
                 schema_name="content")

        del a["content.json"]["hash"]

        with self.assertRaises(ValidationError) as cm:
            validate(a["content.json"],
                     schema=content[VERSIONS_AVAILABLE[-1]],
                     schema_name="content")

        self.assertEqual(cm.exception.message,
                         "A static container requires a hash.")

        a["content.json"]["hash"] = None

        with self.assertRaises(ValidationError) as cm:
            validate(a["content.json"],
                     schema=content[VERSIONS_AVAILABLE[-1]],
                     schema_name="content")

        self.assertEqual(cm.exception.message,
                         "A static container requires a hash.")
