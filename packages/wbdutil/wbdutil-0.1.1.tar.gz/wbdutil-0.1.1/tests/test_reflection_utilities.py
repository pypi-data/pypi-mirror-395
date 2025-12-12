import pytest
from importlib import import_module
from . import TARGET_MODULE_NAME


ReflectionHelper = import_module(f"{TARGET_MODULE_NAME}.common.reflection_utilities").ReflectionHelper
WbdutilAttributeError = import_module(f"{TARGET_MODULE_NAME}.common.exceptions").WbdutilAttributeError
WbdutilValueError = import_module(f"{TARGET_MODULE_NAME}.common.exceptions").WbdutilValueError


class TestReflectionHelper:
    def test_GIVEN_valid_source_data_WHEN_getattr_recursive_first_level_item_THEN_returns_expected_object(self):

        data = {
            "abc": 123,
            "xyz": {
                "123": 456
            }
        }

        result = ReflectionHelper.getattr_recursive(data, ["abc"])

        assert result == 123

    def test_GIVEN_valid_source_data_WHEN_getattr_recursive_second_level_item_THEN_returns_expected_object(self):

        data = {
            "abc": 123,
            "xyz": {
                "123": [4, 5, 6]
            }
        }

        result = ReflectionHelper.getattr_recursive(data, ["xyz", "123"])

        assert result == [4, 5, 6]

    def test_GIVEN_valid_source_data_WHEN_getattr_recursive_second_level_array_item_THEN_returns_expected_object(self):

        data = {
            "abc": 123,
            "xyz": {
                "123": [4, 5, 6]
            }
        }

        result = ReflectionHelper.getattr_recursive(data, ["xyz", "123[1]"])

        assert result == 5

    def test_GIVEN_valid_source_data_WHEN_getattr_recursive_second_level_2d_array_item_THEN_returns_expected_object(self):

        data = {
            "abc": 123,
            "xyz": {
                "123": [4, [1, 5], 6]
            }
        }

        result = ReflectionHelper.getattr_recursive(data, ["xyz", "123[1][1]"])

        assert result == 5

    def test_GIVEN_empty_source_data_WHEN_getattr_recursive_THEN_result_is_none(self):
        data = {}
        result = ReflectionHelper.getattr_recursive(data, ["xyz", "123"])
        assert result is None

    def test_GIVEN_none_source_data_WHEN_getattr_recursive_THEN_result_is_none(self):
        data = None
        result = ReflectionHelper.getattr_recursive(data, ["xyz", "123"])
        assert result is None

    def test_GIVEN_valid_source_data_WHEN_getattr_recursive_invalid_array_THEN_returns_expected_object(self):

        data = {
            "abc": 123,
            "xyz": {
                "123": [4, [1, 5], 6]
            }
        }

        with pytest.raises(WbdutilAttributeError):
            ReflectionHelper.getattr_recursive(data, ["xyz", "123[[1][1]"])

        result = ReflectionHelper.getattr_recursive(data, ["xyz", "123[1][1"])
        assert result is None

    def test_GIVEN_empty_destination_dict_WHEN_setattr_recursive_THEN_populates_destination_dict(self):
        expected = {
            "xyz": {
                "123": 123
            }
        }

        data = {}

        ReflectionHelper.setattr_recursive(123, data, ["xyz", "123"])
        assert data == expected

    def test_GIVEN_None_destination_dict_WHEN_setattr_recursive_THEN_populates_destination_dict(self):
        data = None

        with pytest.raises(WbdutilValueError):
            ReflectionHelper.setattr_recursive(123, data, ["xyz", "123"])

    def test_GIVEN_populated_destination_dict_WHEN_setattr_recursive_THEN_populates_destination_dict(self):
        expected = {
            "abc": "a string",
            "xyz": {
                "123": 123,
                "abc": "a string"
            }
        }

        data = {
            "abc": "a string",
            "xyz": {
                "abc": "a string"
            }
        }

        ReflectionHelper.setattr_recursive(123, data, ["xyz", "123"])
        assert data == expected

    def test_GIVEN_populated_destination_dict_and_array_to_add_WHEN_setattr_recursive_THEN_populates_destination_dict(self):
        expected = {
            "abc": "a string",
            "xyz": {
                "123": [1, 2, 3],
                "abc": "a string"
            }
        }

        data = {
            "abc": "a string",
            "xyz": {
                "abc": "a string"
            }
        }

        ReflectionHelper.setattr_recursive([1, 2, 3], data, ["xyz", "123"])
        assert data == expected

    def test_GIVEN_populated_destination_dict_and_array_to_add_WHEN_setattr_recursive_THEN_populates_destination_dict_with_overwrite(self):
        expected = {
            "abc": "a string",
            "xyz": {
                "abc": [1, 2, 3]
            }
        }

        data = {
            "abc": "a string",
            "xyz": {
                "abc": "a string"
            }
        }

        ReflectionHelper.setattr_recursive([1, 2, 3], data, ["xyz", "abc"])
        assert data == expected
