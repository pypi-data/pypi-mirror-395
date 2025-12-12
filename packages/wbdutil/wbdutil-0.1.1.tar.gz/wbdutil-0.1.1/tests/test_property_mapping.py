import pytest
from importlib import import_module
from unittest.mock import Mock, call
from . import TARGET_MODULE_NAME


# Test target module import
property_mapping = import_module(f"{TARGET_MODULE_NAME}.service.property_mapping")

PropertyMapper = property_mapping.PropertyMapper
IPropertyMappingLoader = property_mapping.IPropertyMappingLoader

IDictionaryLoader = import_module(f"{TARGET_MODULE_NAME}.common.file_loader").IDictionaryLoader
WdutilValidationException = import_module(f"{TARGET_MODULE_NAME}.common.exceptions").WbdutilValidationException
WbdutilAttributeError = import_module(f"{TARGET_MODULE_NAME}.common.exceptions").WbdutilAttributeError
Configuration = import_module(f"{TARGET_MODULE_NAME}.common.configuration").Configuration
IFileLoader = import_module(f"{TARGET_MODULE_NAME}.common.file_loader").IFileLoader


class TestPropertyMapper:
    def test_GIVEN_flat_mapping_WHEN_remap_data_THEN_returns_expected_object(self):
        # Arrange
        mapping = {
            "xyz": "abc",
            "uvw": "ef"
        }

        target = self._construct_property_mapper(mapping)

        source = {
            "abc": "some data",
            "ef": ["An", "Array"]
        }

        # Act
        result = target.remap_data(source, {})

        # Assert
        assert result["xyz"] is source["abc"]
        assert result["uvw"] is source["ef"]

    def test_GIVEN_nested_source_mapping_WHEN_remap_data_THEN_returns_expected_object(self):
        # Arrange
        mapping = {
            "dest1": "level1a.level2.level3",
            "dest2": "level1b.level2",
            "dest3": "level1a"
        }

        target = self._construct_property_mapper(mapping)

        source = {
            "level1a": {
                "level2": {
                    "level3": "a string"
                }
            },
            "level1b": {
                "level2": ["An", "Array"]
            }
        }

        # Act
        result = target.remap_data(source, {})

        # Assert
        assert result["dest1"] is source["level1a"]["level2"]["level3"]
        assert result["dest2"] is source["level1b"]["level2"]
        assert result["dest3"] is source["level1a"]

    def test_GIVEN_source_mapping_wrong_WHEN_remap_data_THEN_missing_field_is_populated_with_None(self):
        # Arrange
        mapping = {
            "dest1": "level1a.level2.level4",
            "dest2": "level1b.level2",
            "dest3": "level1a"
        }

        target = self._construct_property_mapper(mapping)

        source = {
            "level1a": {
                "level2": {
                    "level3": "a string"
                }
            },
            "level1b": {
                "level2": ["An", "Array"]
            }
        }

        # Act
        result = target.remap_data(source, {})

        # Assert
        assert result["dest1"] is None
        assert result["dest2"] is source["level1b"]["level2"]
        assert result["dest3"] is source["level1a"]

    def test_GIVEN_nested_destination_mapping_WHEN_remap_data_THEN_returns_expected_object(self):
        # Arrange
        mapping = {
            "level1.level2.a": "a",
            "level1.b": "b"
        }

        target = self._construct_property_mapper(mapping)

        source = {
            "a": "some data",
            "b": ["An", "Array"]
        }

        # Act
        result = target.remap_data(source, {})

        # Assert
        assert result["level1"]["level2"]["a"] is source["a"]
        assert result["level1"]["b"] is source["b"]

    def test_GIVEN_mapping_from_array_WHEN_remap_data_THEN_returns_expected_object(self):
        # Arrange
        mapping = {
            "dest": "src[1]",
        }

        target = self._construct_property_mapper(mapping)

        source = {
            "src": ["element0", "element1"]
        }

        # Act
        result = target.remap_data(source, {})

        # Assert
        assert result["dest"] is source["src"][1]

    def test_GIVEN_mapping_from_2d_array_WHEN_remap_data_THEN_returns_expected_object(self):
        # Arrange
        mapping = {
            "dest": "src[0][1]",
        }

        target = self._construct_property_mapper(mapping)

        source = {
            "src": [['element0.0', 'element0.1'], 'element1']
        }

        # Act
        result = target.remap_data(source, {})

        # Assert
        assert result["dest"] is source["src"][0][1]

    def test_GIVEN_mapping_from_nested_array_WHEN_remap_data_THEN_returns_expected_object(self):
        # Arrange
        mapping = {
            "dest": "src[0][1].nest[1].value",
        }

        target = self._construct_property_mapper(mapping)

        source = {
            "src": [["element0.0", {"nest": ["", {"value": 123}]}], "element1"]
        }

        # Act
        result = target.remap_data(source, {})

        # Assert
        assert result["dest"] == 123

    def test_GIVEN_array_index_is_string_WHEN_remap_data_THEN_raise(self):
        # Arrange
        mapping = {
            "dest": "src[a]",
        }

        target = self._construct_property_mapper(mapping)

        source = {
            "src": ["element0", "element1"]
        }

        # Act
        with pytest.raises(WbdutilAttributeError) as ex:
            target.remap_data(source, {})

        assert "src[a]" in ex.value.message

    def test_GIVEN_array_has_no_field_name_WHEN_remap_data_THEN_raise(self):
        # Arrange
        mapping = {
            "dest": "[1]",
        }

        target = self._construct_property_mapper(mapping)

        source = {
            "src": ["element0", "element1"]
        }

        # Act
        with pytest.raises(WbdutilAttributeError) as ex:
            target.remap_data(source, {})

        assert "[1]" in ex.value.message

    def test_GIVEN_config_source_WHEN_remap_data_THEN_returns_expected(self):
        # Arrange
        mapping = {
            "dest.dest2": "CONFIGURATION.data.default.viewers",
        }

        mock_config = Mock(spec=Configuration)
        mock_config.get_recursive.return_value = "A value"

        target = self._construct_property_mapper(mapping, mock_config)

        source = {
            "src": ["element0", "element1"]
        }

        # Act
        result = target.remap_data(source, {})

        # Assert
        assert result["dest"]["dest2"] == "A value"
        mock_config.get_recursive.assert_called_once_with(["data", "default", "viewers"])

    def test_GIVEN_mapping_from_function_with_no_args_WHEN_remap_data_THEN_returns_expected(self):
        # Arrange
        mapping = {
            "data.WellboreID": {
                "type": "function",
                "function": "get_wellbore_id",
                "args": []
            }
        }

        mock_functions = Mock()
        mock_functions.get_wellbore_id.return_value = "12345"

        target = self._construct_property_mapper(mapping, None, mock_functions)

        source = {}

        # Act
        result = target.remap_data(source, {})

        # Assert
        assert result["data"]["WellboreID"] == "12345"
        mock_functions.get_wellbore_id.assert_called_once_with()

    def test_GIVEN_mapping_from_function_with_2_args_WHEN_remap_data_THEN_returns_expected(self):
        # Arrange
        mapping = {
            "data.function_result": {
                "type": "function",
                "function": "some_function",
                "args": ["src.arg1", "arg2"]
            }
        }

        mock_functions = Mock()
        mock_functions.some_function.return_value = "12345"

        target = self._construct_property_mapper(mapping, None, mock_functions)

        source = {
            "src": {
                "arg1": "abc"
            },
            "arg2": 123
        }

        # Act
        result = target.remap_data(source, {})

        # Assert
        assert result["data"]["function_result"] == "12345"
        mock_functions.some_function.assert_called_once_with("abc", 123)

    def test_GIVEN_mapping_from_function_that_does_not_exist_WHEN_remap_data_THEN_raises(self):
        # Arrange
        mapping = {
            "data.function_result": {
                "type": "function",
                "function": "some_function_that_does_not_exist",
                "args": ["arg1"]
            }
        }

        target = self._construct_property_mapper(mapping, None, object())

        source = {
            "arg1": 123
        }

        # Act
        # Assert
        with pytest.raises(WbdutilAttributeError) as execinfo:
            target.remap_data(source, {})

        assert execinfo.value.message == "The function 'some_function_that_does_not_exist' was not found in the provided mapping functions"

    def test_GIVEN_mapping_function_arg_is_invalid_WHEN_remap_data_THEN_raises(self):
        # Arrange
        mapping = {
            "data.function_result": {
                "type": "function",
                "function": "some_function",
                "args": [123]
            }
        }

        mock_functions = Mock()
        mock_functions.some_function.return_value = "12345"

        target = self._construct_property_mapper(mapping, None, mock_functions)

        # Act
        # Assert
        with pytest.raises(WbdutilAttributeError) as execinfo:
            target.remap_data({}, {})

        assert execinfo.value.message == "All of the mapping function arguments must be strings."

    def test_GIVEN_mapping_from_array_WHEN_remap_data_THEN_returns_expected(self):
        # Arrange
        mapping = {
            "data.array_remap_result": {
                "type": "array",
                "source": "curves",
                "mapping": {
                    "dest1": "src1",
                    "dest2.lev2": "src2"
                }
            }
        }

        target = self._construct_property_mapper(mapping)

        source = {
            "curves": [{"src1": 1, "src2": "a"}, {"src1": 2, "src2": "b"}, {"src1": 3, "src2": "c"}]
        }

        # Act
        result = target.remap_data(source, {})

        # Assert
        result_array = result["data"]["array_remap_result"]
        assert len(result_array) == 3

        assert result_array[0]["dest1"] == 1
        assert result_array[0]["dest2"]["lev2"] == "a"

        assert result_array[1]["dest1"] == 2
        assert result_array[1]["dest2"]["lev2"] == "b"

        assert result_array[2]["dest1"] == 3
        assert result_array[2]["dest2"]["lev2"] == "c"

    def test_GIVEN_wellbore_mapping_WHEN_remap_data_with_kind_THEN_returns_expected(self):
        # Arrange
        mapping = {
            "kind": "osdu:wks:master-data--Wellbore:1.0.0",
            "mapping": {
                "acl.viewers": "CONFIGURATION.data.default.viewers",
                "acl.owners": "CONFIGURATION.data.default.owners",
                "legal.legaltags": "CONFIGURATION.legal.legaltags",
                "legal.otherRelevantDataCountries": "CONFIGURATION.legal.otherRelevantDataCountries",
                "legal.status": "CONFIGURATION.legal.status",
                "data.FacilityName": "well.WELL.value",
                "data.NameAliases": {
                    "type": "function",
                    "function": "build_wellbore_name_aliases",
                    "args": ["well.UWI.value", "CONFIGURATION.data_partition_id"]
                }
            }
        }

        config_str = '''{
           "base_url": "https://osdu-ship.msft-osdu-test.org",
           "data_partition_id": "opendes",
           "legal": {
               "legaltags": ["opendes-public-usa-dataset-7643990"],
               "otherRelevantDataCountries": ["US"],
               "status": "compliant"
            },
            "data": {
                "default": {
                    "viewers": ["data.default.viewers@opendes.contoso.com"],
                    "owners": ["data.default.owners@opendes.contoso.com"]
                }
            }
        }'''

        mock_loader = Mock(spec=IFileLoader)
        mock_loader.load.return_value = config_str

        config = Configuration(mock_loader, None)

        mock_functions = Mock()
        mock_functions.build_wellbore_name_aliases.return_value = "NameAliasFromFunction"

        mock_reader = Mock(spec=IPropertyMappingLoader)
        mock_reader.mapping = mapping["mapping"]
        mock_reader.kind = mapping["kind"]
        target = PropertyMapper(mock_reader, config, mock_functions)

        source = {
            "well": {
                "WELL": {"value": "SomeWell"},
                "UWI": {"value": "SomeUWI"}
            }
        }

        expected = {
            'kind': 'osdu:wks:master-data--Wellbore:1.0.0',
            'acl': {
                'viewers': ['data.default.viewers@opendes.contoso.com'],
                'owners': ['data.default.owners@opendes.contoso.com']
            },
            'legal': {
                'legaltags': ['opendes-public-usa-dataset-7643990'],
                'otherRelevantDataCountries': ['US'],
                'status': 'compliant'
            },
            'data': {'FacilityName': 'SomeWell', 'NameAliases': 'NameAliasFromFunction'}
        }

        # Act
        result = target.remap_data_with_kind(source)

        # Assert
        assert result == expected
        mock_functions.build_wellbore_name_aliases.assert_called_once_with("SomeUWI", "opendes")

    def test_GIVEN_welllog_mapping_WHEN_remap_data_with_kind_THEN_returns_expected(self):
        # Arrange
        mapping = {
            "kind": "osdu:wks:work-product-component--WellLog:1.1.0",
            "mapping":
            {
                "acl.viewers": "CONFIGURATION.data.default.viewers",
                "acl.owners": "CONFIGURATION.data.default.owners",
                "legal.legaltags": "CONFIGURATION.legal.legaltags",
                "legal.otherRelevantDataCountries": "CONFIGURATION.legal.otherRelevantDataCountries",
                "legal.status": "CONFIGURATION.legal.status",
                "data.ReferenceCurveID": "curves[0].mnemonic",
                "data.WellboreID": {
                    "type": "function",
                    "function": "get_wellbore_id",
                    "args": []
                },
                "data.Curves": {
                    "type": "array",
                    "source": "curves",
                    "mapping": {
                        "CurveID": "mnemonic",
                        "Mnemonic": "mnemonic",
                        "CurveUnit": {
                            "type": "function",
                            "function": "las2osdu_curve_uom_converter",
                            "args": [
                                "CONFIGURATION.data_partition_id",
                                "mnemonic"
                            ]
                        }
                    }
                }
            }
        }

        config_str = '''{
           "base_url": "https://osdu-ship.msft-osdu-test.org",
           "data_partition_id": "opendes",
           "acl_domain": "contoso.com",
           "legal": {
               "legaltags": ["opendes-public-usa-dataset-7643990"],
               "otherRelevantDataCountries": ["US"],
               "status": "compliant"
            },
            "data": {
                "default": {
                    "viewers": ["data.default.viewers@opendes.contoso.com"],
                    "owners": ["data.default.owners@opendes.contoso.com"]
                }
            }
        }'''

        mock_loader = Mock(spec=IFileLoader)
        mock_loader.load.return_value = config_str

        config = Configuration(mock_loader, None)

        mock_functions = Mock()
        mock_functions.get_wellbore_id.return_value = "WellboreIdFromFunction"
        mock_functions.las2osdu_curve_uom_converter.return_value = "UomConverterFunction"

        mock_reader = Mock(spec=IPropertyMappingLoader)
        mock_reader.mapping = mapping["mapping"]
        mock_reader.kind = mapping["kind"]
        target = PropertyMapper(mock_reader, config, mock_functions)

        source = {
            "curves": [
                {"mnemonic": "mnemonic_0"},
                {"mnemonic": "mnemonic_1"},
                {"mnemonic": "mnemonic_2"}
            ]
        }

        expected = {
            'acl': {
                'viewers': ['data.default.viewers@opendes.contoso.com'],
                'owners': ['data.default.owners@opendes.contoso.com']
            },
            'legal': {
                'legaltags': ['opendes-public-usa-dataset-7643990'],
                'otherRelevantDataCountries': ['US'],
                'status': 'compliant'
            },
            'data': {
                'ReferenceCurveID': 'mnemonic_0',
                'WellboreID': 'WellboreIdFromFunction',
                'Curves': [
                    {'CurveID': 'mnemonic_0', 'Mnemonic': 'mnemonic_0', 'CurveUnit': 'UomConverterFunction'},
                    {'CurveID': 'mnemonic_1', 'Mnemonic': 'mnemonic_1', 'CurveUnit': 'UomConverterFunction'},
                    {'CurveID': 'mnemonic_2', 'Mnemonic': 'mnemonic_2', 'CurveUnit': 'UomConverterFunction'}
                ]
            },
            'kind': 'osdu:wks:work-product-component--WellLog:1.1.0'
        }

        # Act
        result = target.remap_data_with_kind(source)

        # Assert
        assert result == expected
        mock_functions.get_wellbore_id.assert_called_once_with()

        calls = [call('opendes', 'mnemonic_0'), call('opendes', 'mnemonic_1'), call('opendes', 'mnemonic_2')]
        mock_functions.las2osdu_curve_uom_converter.assert_has_calls(calls)

    def _construct_property_mapper(self, mapping, mock_config=None, mock_functions=None):
        mock_reader = Mock(spec=IPropertyMappingLoader)
        mock_reader.mapping = mapping
        return PropertyMapper(mock_reader, mock_config, mock_functions)
