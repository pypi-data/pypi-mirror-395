import unittest
import json
import os.path
import pytest
from importlib import import_module
from . import TARGET_MODULE_NAME

# Test target module import
JsonToFile = import_module(f"{TARGET_MODULE_NAME}.wrapper.json_writer").JsonToFile


class TestJsonToFile(unittest.TestCase):
    TESTFILENAME = "testfile.json"

    def tearDown(self):
        if os.path.isfile(self.TESTFILENAME):
            os.remove(self.TESTFILENAME)

    def test_basic_write(self):
        data = {
            "string": "a string",
            "number": 1,
            "array": [1, 2, 3, 4],
            "object": {
                "substring": "another string"
            }
        }

        subject = JsonToFile()

        # Act
        subject.write(data, self.TESTFILENAME)

        # Assert
        with open(self.TESTFILENAME) as json_file:
            result = json.load(json_file)

        self.assertDictEqual(data, result)

    def test_write_to_invalid_path_fails(self):
        invalid_path = "/nonsense/path/that/does/not/exist/file.json"

        data = {
            "string": "a string"
        }

        subject = JsonToFile()

        # Act/Assert
        with pytest.raises(FileNotFoundError):
            subject.write(data, invalid_path)
