import re
import unittest
from openframe_criteria_set_protocol.v1 import schemas as v1_schemas


class TestSchemas(unittest.TestCase):
    def test_criteria_set_id_schema(self):
        regex = re.compile(v1_schemas.criteria_set_id)

        self.assertFalse(regex.match('a b c'))
        self.assertFalse(regex.match('ææø'))
        self.assertFalse(regex.match('$a$b$c'))

        self.assertTrue(regex.match('a-b-c'))
        self.assertTrue(regex.match('a-b-c-1'))
        self.assertTrue(regex.match('a-b-c-1.2'))

    def test_version_schema(self):
        regex = re.compile(v1_schemas.version)

        self.assertFalse(regex.match('1'))
        self.assertFalse(regex.match('2.2'))
        self.assertFalse(regex.match('3.3.a'))

        self.assertTrue(regex.match('1.0.0'))
