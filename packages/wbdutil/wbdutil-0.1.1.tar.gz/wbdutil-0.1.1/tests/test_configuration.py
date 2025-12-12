
import json
import importlib
from unittest.mock import Mock
from . import TARGET_MODULE_NAME

# Test target module import
Configuration = importlib.import_module(f"{TARGET_MODULE_NAME}.common.configuration").Configuration
IFileLoader = importlib.import_module(f"{TARGET_MODULE_NAME}.common.file_loader").IFileLoader


class TestConfiguration:

    _config = {
        "base_url": "https://osdu-ship.msft-osdu-test.org",
        "data_partition_id": "opendes",
        "legal":
        {
            "legaltags": ["opendes-public-usa-dataset-7643990"],
            "otherRelevantDataCountries": ["US"],
            "status": "compliant"
        },
        "data": {
            "default": {
                "viewers": ["data.default.viewers@opendes.contoso.com"],
                "owners": ["data.default.owners@opendes.contoso.com"]
            }
        },
        "wellbore_mapping": {"kind": "osdu:wks:master-data--Wellbore:1.0.0"},
        "welllog_mapping": {"kind": "osdu:wks:work-product-component--WellLog:1.1.0"}
    }

    def test_parses_json_as_expected(self):
        # Assemble
        mock_reader = Mock(spec=IFileLoader)
        mock_reader.load.return_value = json.dumps(self._config)

        # Act
        conf = Configuration(mock_reader, "some_filename.json")

        # Assert
        assert conf.base_url == self._config["base_url"]
        assert conf.data_partition_id == self._config["data_partition_id"]

        assert conf.wellbore_mapping == self._config["wellbore_mapping"]
        assert conf.welllog_mapping == self._config["welllog_mapping"]

    def test_get_recursive_returns_expected_result(self):
        # Assemble
        mock_reader = Mock(spec=IFileLoader)
        mock_reader.load.return_value = json.dumps(self._config)

        # Act
        conf = Configuration(mock_reader, "some_filename.json")

        # Assert
        assert conf.get_recursive(["legal", "legaltags"]) == self._config["legal"]["legaltags"]
        assert conf.get_recursive(["data", "default", "owners"]) == self._config["data"]["default"]["owners"]
