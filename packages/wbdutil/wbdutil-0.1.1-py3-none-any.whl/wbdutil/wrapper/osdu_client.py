import io
from typing import Dict, List, Union

import httpx
from knack.log import get_logger
from pandas import DataFrame, read_parquet

from ..common.configuration import Configuration
from ..service.record_mapper import Record, WellLogRecord

logger = get_logger(__name__)


class DataLoaderWebResponseError(Exception):
    """
    Common class for web response errors
    """

    def __init__(self, http_code: str, url: str, message: str = ""):
        """
        Create a new instance of a DataLoaderWebResponseError

        :param str http_code: The HTTP response code.
        :param str url: The URL that was called.
        :param str message: An optional message.
        """
        super().__init__(f"HTTP error: {http_code}. Calling: '{url}'. {message}")


class OsduClient:
    def __init__(self, config: Configuration, access_token: str) -> None:
        """
        Create a new instance of a OsduClient

        :param str config: The configuration object having all properties.
        :param str access_token: The access token required to access the OSDU instance.

        """
        self._access_token = access_token
        self._base_url = config.base_url
        self._data_partition_id = config.data_partition_id
        self._wellbore_service_path_prefix = config.wellbore_service_path_prefix
        self._search_service_path_prefix = config.search_service_path_prefix
        self._wellbore_service = "wellbore"
        self._search_service = "search"

    def _create_headers(self) -> Dict[str, str]:
        """
        Create a new set of auth headers for OSDU

        :return: the header for a standard request
        :rtype: str
        """
        return {
            "Authorization": f"Bearer {self._access_token}",
            "data-partition-id": self._data_partition_id,
        }

    def create_wellbore(self, record: Record) -> List[any]:
        """
        Make a post request to OSDU to create a new wellbore record.

        :param Record record: The wellbore record to be uploaded
        :return: the id of the new well bore
        :rtype: str
        """
        url = f'{self.get_base_url(self._wellbore_service)}/api/os-wellbore-ddms/ddms/v3/wellbores'
        return self._post_data_with_id_response(url, record)

    def post_welllog(self, record: Union[Record, WellLogRecord]) -> List[any]:
        """
        Make a post request to OSDU to create a new or update an existing well log record.
        If the `welllog_record` contains an `id` attribute, the well log with that ID shall be updated.
        If the `welllog_record` does not contain an `id` attribute, a new record will be created.

        :param Union[Record, WellLogRecord] welllog_record: The well log record to be uploaded.
        :return: The ID of the created/updated well log
        :rtype: List[any]
        """
        url = f'{self.get_base_url(self._wellbore_service)}/api/os-wellbore-ddms/ddms/v3/welllogs'
        return self._post_data_with_id_response(url, record)

    def get_wellbore_record(self, wellbore_id: str) -> Record:
        """
        Make a get request to OSDU to retreive an existing wellbore record.

        :param str wellbore_id: The wellbore id to be uploaded
        :return: the wellbore record
        :rtype: Record
        """

        get_record_url = f'{self.get_base_url(self._wellbore_service)}/api/os-wellbore-ddms/ddms/v3/wellbores/{wellbore_id}'

        return Record(self._send_request_json_response("GET", get_record_url, None, None))

    def get_welllog_record(self, welllog_id: str) -> WellLogRecord:
        """
        Make a get request to OSDU to retreive an existing welllog record.

        :param str welllog_id: The welllog id to be uploaded
        :return: the welllog record
        :rtype: WellLogRecord
        """
        get_record_url = f'{self.get_base_url(self._wellbore_service)}/api/os-wellbore-ddms/ddms/v3/welllogs/{welllog_id}'
        return WellLogRecord(self._send_request_json_response("GET", get_record_url, None, None))

    def add_welllog_data(self, data: DataFrame, welllog_id: str) -> None:
        """
        Make a post request to OSDU to add a new data to an existing well log.

        :param DataFrame data: The welllog data to add
        :param str welllog_id: The id of the new well log
        """

        url = f'{self.get_base_url(self._wellbore_service)}/api/os-wellbore-ddms/ddms/v3/welllogs/{welllog_id}/data'

        # Adding content-type to standard headers
        headers = self._create_headers()
        headers.update({"content-type": "application/x-parquet"})

        payload = data.to_parquet()
        self._send_request_json_response("POST", url, payload, None, headers=headers)

    def get_welllog_data(self, welllog_id: str, curves: List[str] = None) -> DataFrame:
        """
        Get welllog data for all or a specified set of curves.
        :param str welllog_id: The id of the well log
        :param List[str] curves: The welllog curves, None or empty returns all curves
        :return: The welllog data
        :rtype: DataFrame
        """
        curves_query = ""
        if curves is not None and len(curves) > 0:
            curves_query = f"&curves={','.join(curves)}"

        url = self.get_base_url(self._wellbore_service)

        get_welllog_data_url = f'{url}/api/os-wellbore-ddms/ddms/v3/welllogs/{welllog_id}/data?describe=false{curves_query}'

        try:
            res = self._send_request("GET", get_welllog_data_url, None, None)
        except DataLoaderWebResponseError as ex:
            logger.warning(f"No curve data found. Error: {str(ex)}")
            return None
        return read_parquet(io.BytesIO(res.content))

    def post_log_recognition(self, mnemonic: str, unit: str) -> any:
        """
        Make a request to OSDU to recognize a particular combination of mnemonic and unit.
        :param str mnemonic: The mnemonic
        :param str unit: The unit
        :return: A dictionary that contains the curve family
        :rtype: any
        """
        recognize_family_url = f'{self.get_base_url(self._wellbore_service)}/api/os-wellbore-ddms/log-recognition/family'
        payload = {"label": mnemonic, "log_unit": unit}
        return self._send_request_json_response("POST", recognize_family_url, None, payload)

    def search_for_wellbore(self, wellbore_name: str) -> List[str]:
        """
        Search an OSDU instance to find all wellbores with the specified name and return their ids.
        :param str wellbore_name: The well name
        :return: A List that contains the matching wellbore ids
        :rtype: List[str]
        """
        url = f'{self.get_base_url(self._search_service)}/api/search/v2/query'

        payload = {
            "kind": "*:*:master-data--Wellbore:*",
            "query": f'data.FacilityName:"{wellbore_name}"',
            "returnedFields": ["id"],
            "limit": 1000
        }

        result = self._send_request_json_response("POST", url, None, payload)
        if result is None or result.get("totalCount") is None or result.get("totalCount") < 1:
            return []
        else:
            return [r["id"] for r in result.get("results")]

    def _post_data_with_id_response(self, path: str, record: Record) -> List[any]:
        payload = [record.get_raw_data()]
        url = f"{path}"

        parsed_result = self._send_request_json_response("POST", url, None, payload)

        if "recordIds" in parsed_result:
            return parsed_result["recordIds"]
        else:
            return []

    def _send_request_json_response(self, method: str, url: str, content: any, json: Dict[str, any], headers=None) -> any:
        res = self._send_request(method, url, content, json, headers)
        return res.json()

    def _send_request(self, method: str, url: str, content: any, json: Dict[str, any], headers=None) -> any:
        logger.debug(f"{method}: {url}")

        headers = self._create_headers() if headers is None else headers

        with httpx.Client() as client:
            res = client.request(method, url, json=json, content=content, headers=headers)

            if res.status_code >= 300:
                raise DataLoaderWebResponseError(res.status_code, url, res.text)

            return res

    def get_base_url(self, service_name: str) -> str:
        wellbore_path_prefix = self._wellbore_service_path_prefix
        search_path_prefix = self._search_service_path_prefix

        if service_name == self._wellbore_service and wellbore_path_prefix is not None and len(wellbore_path_prefix) > 0:
            return f"{self._base_url}/{wellbore_path_prefix}"
        elif service_name == self._search_service and search_path_prefix is not None and len(search_path_prefix) > 0:
            return f"{self._base_url}/{search_path_prefix}"
        else:
            return self._base_url
