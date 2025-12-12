import pytest
import httpx
from pandas import DataFrame
from importlib import import_module
from . import TARGET_MODULE_NAME
from unittest.mock import Mock

# Test target module import
Record = import_module(f"{TARGET_MODULE_NAME}.service.record_mapper").Record
osdu_client = import_module(f"{TARGET_MODULE_NAME}.wrapper.osdu_client")
DataLoaderWebResponseError = osdu_client.DataLoaderWebResponseError
OsduClient = osdu_client.OsduClient
Configuration = import_module(f"{TARGET_MODULE_NAME}.common.configuration").Configuration


class TestOsduClient:
    _expected_ids = [123, 234, 345]
    _expected_ids_str = [{"id": "321"}, {"id": "432"}, {"id": "543"}]
    _access_token = "token"
    _data_partition_id = "AnId"
    _serviceName = "wellbore"
    mockConfig = Mock(spec=Configuration)
    mockConfig.data_partition_id = "AnId"
    mockConfig.wellbore_service_path_prefix = None
    mockConfig.search_service_path_prefix = None
    mockConfig.base_url = "http://test.bp.com"

    def match_and_mock_post(self, request: any):
        if request.method != "POST":
            return httpx.Response(500, text="Not a post request")

        if "Authorization" not in request.headers or self._access_token not in request.headers["Authorization"]:
            return httpx.Response(500, text="No Authorization header")

        if "data-partition-id" not in request.headers or self._data_partition_id != request.headers["data-partition-id"]:
            return httpx.Response(500, text="No data-partition-id header")

        return httpx.Response(200, json={"recordIds": self._expected_ids, "totalCount": 3, "results": self._expected_ids_str})

    def match_and_mock_get(self, request: any):
        if request.method != "GET":
            return httpx.Response(500, text="Not a get request")

        if "Authorization" not in request.headers or self._access_token not in request.headers["Authorization"]:
            return httpx.Response(500, text="No Authorization header")

        if "data-partition-id" not in request.headers or self._data_partition_id != request.headers["data-partition-id"]:
            return httpx.Response(500, text="No data-partition-id header")

        return httpx.Response(200, json={"recordIds": self._expected_ids})

    def match_and_mock_post_with_content_header(self, request: any):
        if "content-type" not in request.headers or "application/x-parquet" != request.headers["content-type"]:
            return httpx.Response(500, text="No content-type header")

        return self.match_and_mock_post(request)

    def match_and_mock_get_return_bytes(self, request: any):
        """
        Return `None` to not match the request.
        """

        rawdata = {'one': [4., 5., 6., 7.], 'two': [7., 6., 5., 4.]}
        dataframe = DataFrame(rawdata)

        if request.method != "GET":
            return httpx.Response(500, text="Not a get request")

        if "Authorization" not in request.headers or self._access_token not in request.headers["Authorization"]:
            return httpx.Response(500, text="No Authorization header")

        if "data-partition-id" not in request.headers or self._data_partition_id != request.headers["data-partition-id"]:
            return httpx.Response(500, text="No data-partition-id header")

        return httpx.Response(200, content=dataframe.to_parquet())

    def test_create_wellbore_calls_correct_url_and_returns_ids(self, respx_mock):
        # Assemble
        base_url = "http://test.bp.com"

        record = Record({"kind": "kind", "acl": {}, "legal": "legal", "data": {}})
        respx_mock.post(f"{base_url}/api/os-wellbore-ddms/ddms/v3/wellbores").mock(side_effect=self.match_and_mock_post)

        client = OsduClient(self.mockConfig, self._access_token)

        # Act
        response = client.create_wellbore(record)

        # Assert
        assert response == self._expected_ids

    def test_create_wellbore_raises_on_error_response(self, respx_mock):
        # Assemble
        base_url = "http://test.bp.com"

        record = Record({"kind": "kind", "acl": {}, "legal": "legal", "data": {}})

        mock_response = httpx.Response(400)
        respx_mock.post(f"{base_url}/api/os-wellbore-ddms/ddms/v3/wellbores").mock(return_value=mock_response)

        client = OsduClient(self.mockConfig, self._access_token)

        # Act
        with pytest.raises(DataLoaderWebResponseError) as ex:
            client.create_wellbore(record)

        # Assert
        assert "400" in str(ex.value)
        assert f"{base_url}/api/os-wellbore-ddms/ddms/v3/wellbores" in str(ex.value)

    def test_create_welllog_calls_correct_url_and_returns_ids(self, respx_mock):
        # Assemble
        base_url = "http://test.bp.com"

        record = Record({"kind": "kind", "acl": {}, "legal": "legal", "data": {}})

        respx_mock.post(f"{base_url}/api/os-wellbore-ddms/ddms/v3/welllogs").mock(side_effect=self.match_and_mock_post)

        client = OsduClient(self.mockConfig, self._access_token)
        # Act
        response = client.post_welllog(record)

        # Assert
        assert response == self._expected_ids

    def test_create_welllog_raises_on_error_response(self, respx_mock):
        # Assemble
        base_url = "http://test.bp.com"

        record = Record({"kind": "kind", "acl": {}, "legal": "legal", "data": {}})

        mock_response = httpx.Response(500)
        respx_mock.post(f"{base_url}/api/os-wellbore-ddms/ddms/v3/welllogs").mock(return_value=mock_response)

        client = OsduClient(self.mockConfig, self._access_token)
        # Act
        with pytest.raises(DataLoaderWebResponseError) as ex:
            client.post_welllog(record)

        # Assert
        assert "500" in str(ex.value)
        assert f"{base_url}/api/os-wellbore-ddms/ddms/v3/welllogs" in str(ex.value)

    def test_add_welllog_data_raises_on_error(self, respx_mock):
        # Assemble
        rawdata = {'one': [4., 5., 6., 7.], 'two': [7., 6., 5., 4.]}
        dataframe = DataFrame(rawdata)
        welllog_id = "WL-ID123"

        base_url = "http://test.bp.com"
        url = f"{base_url}/api/os-wellbore-ddms/ddms/v3/welllogs/{welllog_id}/data"

        mock_response = httpx.Response(500)
        respx_mock.post(url).mock(return_value=mock_response)

        client = OsduClient(self.mockConfig, self._access_token)
        # Act
        with pytest.raises(DataLoaderWebResponseError) as ex:
            client.add_welllog_data(dataframe, welllog_id)

        # Assert
        assert "500" in str(ex.value)
        assert url in str(ex.value)

    def test_add_welllog_data(self, respx_mock):
        # Assemble
        rawdata = {'one': [4., 5., 6., 7.], 'two': [7., 6., 5., 4.]}
        dataframe = DataFrame(rawdata)
        welllog_id = "WL-ID123"

        base_url = "http://test.bp.com"
        url = f"{base_url}/api/os-wellbore-ddms/ddms/v3/welllogs/{welllog_id}/data"

        respx_mock.post(url).mock(side_effect=self.match_and_mock_post_with_content_header)

        client = OsduClient(self.mockConfig, self._access_token)

        # Act
        result = client.add_welllog_data(dataframe, welllog_id)

        # Assert
        assert result is None

    def test_get_wellbore_record(self, respx_mock):
        # Assemble
        wellbore_id = "WB-ID123"

        base_url = "http://test.bp.com"
        url = f"{base_url}/api/os-wellbore-ddms/ddms/v3/wellbores/{wellbore_id}"

        respx_mock.get(url).mock(side_effect=self.match_and_mock_get)

        client = OsduClient(self.mockConfig, self._access_token)

        # Act
        client.get_wellbore_record(wellbore_id)

    def test_get_wellbore_record_raises_on_error(self, respx_mock):
        # Assemble
        wellbore_id = "WB-ID123"

        base_url = "http://test.bp.com"
        url = f"{base_url}/api/os-wellbore-ddms/ddms/v3/wellbores/{wellbore_id}"

        mock_response = httpx.Response(500)
        respx_mock.get(url).mock(return_value=mock_response)

        client = OsduClient(self.mockConfig, self._access_token)

        # Act
        with pytest.raises(DataLoaderWebResponseError) as ex:
            client.get_wellbore_record(wellbore_id)

        # Assert
        assert "500" in str(ex.value)
        assert url in str(ex.value)

    def test_get_welllogs_record(self, respx_mock):
        # Assemble
        welllogs_id = "WL-ID123"

        base_url = "http://test.bp.com"
        url = f"{base_url}/api/os-wellbore-ddms/ddms/v3/welllogs/{welllogs_id}"

        respx_mock.get(url).mock(side_effect=self.match_and_mock_get)

        client = OsduClient(self.mockConfig, self._access_token)

        # Act
        client.get_welllog_record(welllogs_id)

    def test_get_welllog_record_raises_on_error(self, respx_mock):
        # Assemble
        welllog_id = "WL-ID123"

        base_url = "http://test.bp.com"
        url = f"{base_url}/api/os-wellbore-ddms/ddms/v3/welllogs/{welllog_id}"

        mock_response = httpx.Response(500)
        respx_mock.get(url).mock(return_value=mock_response)

        client = OsduClient(self.mockConfig, self._access_token)

        # Act
        with pytest.raises(DataLoaderWebResponseError) as ex:
            client.get_welllog_record(welllog_id)

        # Assert
        assert "500" in str(ex.value)
        assert url in str(ex.value)

    def test_get_welllog_data_record(self, respx_mock):
        # Assemble
        welllog_id = "WL-ID123"
        rawdata = {'one': [4., 5., 6., 7.], 'two': [7., 6., 5., 4.]}
        expected_dataframe = DataFrame(rawdata)

        base_url = "http://test.bp.com"

        url = f"{base_url}/api/os-wellbore-ddms/ddms/v3/welllogs/{welllog_id}/data?describe=false"

        respx_mock.get(url).mock(side_effect=self.match_and_mock_get_return_bytes)

        client = OsduClient(self.mockConfig, self._access_token)

        # Act
        result = client.get_welllog_data(welllog_id)

        assert result.equals(expected_dataframe)

    def test_get_welllog_data_record_for_specific_curves(self, respx_mock):
        # Assemble
        welllog_id = "WL-ID123"
        rawdata = {'one': [4., 5., 6., 7.], 'two': [7., 6., 5., 4.]}
        expected_dataframe = DataFrame(rawdata)

        base_url = "http://test.bp.com"

        url = f"{base_url}/api/os-wellbore-ddms/ddms/v3/welllogs/{welllog_id}/data?describe=false&curves=curve1,curve2"

        respx_mock.get(url).mock(side_effect=self.match_and_mock_get_return_bytes)

        client = OsduClient(self.mockConfig, self._access_token)

        # Act
        result = client.get_welllog_data(welllog_id, ["curve1", "curve2"])

        assert result.equals(expected_dataframe)

    def test_post_log_recognition(self, respx_mock):
        # Assemble
        base_url = "http://test.bp.com"

        url = f"{base_url}/api/os-wellbore-ddms/log-recognition/family"

        respx_mock.post(url).mock(side_effect=self.match_and_mock_post)

        client = OsduClient(self.mockConfig, self._access_token)

        # Act
        result = client.post_log_recognition("mnemonic", "unit")

        assert result is not None

    def test_search_for_wellbore(self, respx_mock):
        # Assemble
        base_url = "http://test.bp.com"

        url = f"{base_url}/api/search/v2/query"

        respx_mock.post(url).mock(side_effect=self.match_and_mock_post)

        client = OsduClient(self.mockConfig, self._access_token)

        # Act
        result = client.search_for_wellbore("Wellbore Name")

        assert result == ["321", "432", "543"]

    def test_get_base_url(self):
        # Assemble
        base_url = "http://test.bp.com"
        client = OsduClient(self.mockConfig, self._access_token)

        # Act
        result = client.get_base_url(self._serviceName)

        assert result == base_url
