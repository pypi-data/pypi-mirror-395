import json
import urllib
from typing import Dict, List, Tuple

from knack.log import get_logger
from lasio.las import LASFile

from ..common.configuration import Configuration
from ..common.file_loader import (FileValidationError, LasParser,
                                  LocalFileLoader)
from ..wrapper.osdu_client import DataLoaderWebResponseError, OsduClient
from .record_mapper import (LasToRecordMapper, MappingUtilities,
                            MapWellLogToLas, Record)

logger = get_logger(__name__)


class DataLoaderConflictError(Exception):
    """
    Exception class for data conflict errors that occur in the service layer
    """

    def __init__(self, message: str, ids: List[str]):
        """
        Create a new instance of a DataLoaderConflictError

        :param str message: An error message.
        :param List[str] ids: List of ids
        """
        self._ids = ids
        super().__init__(message)

    @property
    def ids(self):
        """
        Get the ids of the conflicted objects
        """
        return self._ids


class WellLogService:
    def __init__(self, client: OsduClient):
        """
        Construct a new instance of WellLogService
        :param OsduClient client: An OSDU client wrapper
        """
        self._client = client

    def recognize_log_family(self, welllog_record: Record, data_partition_id: str) -> Record:
        """
        For all the curves in the welllog record call OSDU to get the curve family and
        return an enriched welllog record. This makes no changes to data in OSDU.
        :param Record welllog_record: The welllog record to be enriched
        :param str data_partition_id: The data partition Id.
        :return: the updated welllog record
        :rtype: Record
        """
        welllog_record.data["Curves"] = self.recognize_curves_family(
            welllog_record.data.get("Curves"), data_partition_id
        )
        return welllog_record

    def recognize_curves_family(self, curves: List[Dict[str, any]], data_partition_id: str) -> Dict[str, any]:
        """
        For a set of curves call OSDU to get the curve family and
        return an enriched set of curves. This makes no changes to data in OSDU.
        :param List[Dict[str, any]] curves: The curves to be enriched
        :param str data_partition_id: The data partition Id.
        :return: the updated curves
        :rtype: Dict[str, any]
        """
        if curves is None:
            logger.warning("No curve data to recognize")
            return None

        for curve in curves:
            mnemonic = curve["Mnemonic"]
            osdu_unit = curve["CurveUnit"]
            unit = MappingUtilities.convert_osdu_unit_to_raw_unit(osdu_unit)

            curve["LogCurveFamilyID"] = (
                self.recognize_curve_family(mnemonic, unit, data_partition_id) if unit is not None else None
            )
            curve[
                "NumberOfColumns"
            ] = 1  # las files this should be set to 1 for this utility | may update later if new types are implemented.
        return curves

    def recognize_curve_family(self, mnemonic: str, unit: str, data_partition_id: str) -> str:
        """
        For a mnemonic and unit call OSDU to get the curve family and return the family id.
        :param str mnemonic: The mnemonic
        :param str unit: The unit
        :param str data_partition_id: The data partition Id.
        :return: The curve family id
        :rtype: str
        """
        logger.info("Recognizing log family curve: " + mnemonic)

        try:
            res = self._client.post_log_recognition(mnemonic, unit)
        except DataLoaderWebResponseError as ex:
            logger.warning(f"Could not identify log family curve: {mnemonic}. Error: {str(ex)}")
            return None

        if res is None or res.get("family") is None:
            logger.warning(f"Family not given in response from OSDU. log family curve: {mnemonic}.")
            return None

        family_id = urllib.parse.quote(res.get("family").replace(" ", "-"), safe="")

        return f"{data_partition_id}:reference-data--LogCurveFamily:{family_id}:"

    def update_log_family(self, welllog_id: str, data_partition_id: str) -> None:
        """
        Update the recognized curve families for an existing well log record.
        :param str welllog_id: ID of the well log record to be updated.
        :param str data_partition_id: The data partition ID.
        """
        logger.info("Retrieving existing well log record.")
        welllog_record = self._client.get_welllog_record(welllog_id)

        logger.info("Beginning recognition of curve families.")
        enriched_welllog_record = self.recognize_log_family(welllog_record, data_partition_id)

        logger.info("Updating existing well log record with recognized curve families.")
        welllog_ids = self._client.post_welllog(enriched_welllog_record)

        # Print out updated record in logging for user to see.
        wellbore_service = WellBoreService(self._client, self)
        welllog_id = wellbore_service._safe_get_first_record(welllog_ids)
        welllog_record = self._client.get_welllog_record(welllog_id)
        logger.info(json.dumps(welllog_record.get_raw_data(), indent=4, sort_keys=True))

    def ingest_welllog_data(self, input_path: str, welllog_id: str) -> None:
        """
        Write data from a LAS file to an existing well log. First the LAS file is validated against the
        existing well log record, then the data is extracted and written to the existing well log record.

        :param str input_path: Path and filename of a LAS file containing data to be written to existing well log.
        :param str welllog_id: ID of well log to be updated.
        """
        las_parser = LasParser(LocalFileLoader())
        las_data = las_parser.load_las_file(input_path)

        logger.info("Beginning LAS file validation.")
        try:
            self._validate_welllog_data_ingest_file(las_data, welllog_id)
            logger.info("LAS file validation completed.")
            logger.info("Extracting data from LAS file and writing to existing Well Log.")
            data = las_data.df().reset_index()
            self._client.add_welllog_data(data, welllog_id)
        except FileValidationError as e:
            logger.error(f"Data not ingested - LAS file validation failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Data not ingested: {str(e)}")
            raise

    def download_and_construct_las(self, config: Configuration, welllog_id: str, curves: List[str] = None) -> LASFile:
        """
        Download wellbore and log data and convert to a LAS file.
        :param Configuration config: The application configuration
        :param str welllog_id: The welllog_id
        :param List[str] curves: The Curves to get, or None for all curves
        :return: A new instance of the LAS file object
        :rtype: LASFile
        """

        logger.warning(f"Getting welllog ID {welllog_id}")
        welllog = self._client.get_welllog_record(welllog_id)
        wellbore_id = welllog.data.get("WellboreID")

        if wellbore_id is None:
            logger.error("The welllog records contained no wellbore Id, cannot get wellbore")
            wellbore = Record({})
        else:
            logger.warning(f"Getting wellbore ID {wellbore_id}")
            wellbore = self._client.get_wellbore_record(wellbore_id)

        logger.warning(f"Getting curve data for welllog ID {welllog_id}")

        if curves:
            logger.warning(f"Curves: {curves}")

        welllog_data = self._client.get_welllog_data(welllog_id, curves)

        mapper = MapWellLogToLas(config, wellbore, welllog, welllog_data)

        return mapper.build_las_file()

    def _validate_welllog_data_ingest_file(self, las_data: LASFile, welllog_id: str) -> None:
        """
        Validate a LAS File against an existing well log record.
        This should be done before attempting to write data from a LAS file to an existing record.

        :param LASFile las_data: LASFile object to be validated.
        :param str welllog_id: ID of the well log record to write data to.
        """
        logger.warning("Retrieving well log record and associated information.")
        welllog_well_name, welllog_curve_ids = self._get_data_ingest_validation_variables(welllog_id)
        logger.warning("Validating LAS file well name and curves against existing well log record.")
        las_parser = LasParser(LocalFileLoader())
        las_parser.validate_las_file_against_record(las_data, welllog_well_name, welllog_curve_ids)

    def _get_data_ingest_validation_variables(self, welllog_id: str) -> Tuple[str, List[str]]:
        """
        Get the associated well name and curve IDs of the existing well log for validating against LAS file.
        :param str welllog_id: ID of the well log record to validate a LAS file against.
        :returns: Well name associated with well log AND curve IDs of the well log.
        :rtype: Tuple[str, List[str]]
        """
        welllog_record = self._client.get_welllog_record(welllog_id)
        wellbore_record = self._client.get_wellbore_record(welllog_record.data["WellboreID"])
        welllog_well_name = wellbore_record.data["FacilityName"]
        welllog_curve_ids = welllog_record.get_curveids()
        if welllog_curve_ids == []:
            raise FileValidationError(f"CurveID not found in the well log record: {welllog_id}")
        return welllog_well_name, welllog_curve_ids


class WellBoreService:
    def __init__(self, client: OsduClient, well_log_service: WellLogService):
        """
        Construct a new instance of WellBoreService
        :param OsduClient client: An OSDU client wrapper
        :param WellLogService well_log_service: An instance of WellLogService
        """
        self._client = client
        self._well_log_service = well_log_service

    def file_ingest(self, mapper: LasToRecordMapper, data_partition_id: str, no_recognize: bool):
        """
        Ingest a single las file into new wellbore and welllog records.
        :param LasToRecordMapper mapper: The Las data mapper
        :param str data_partition_id: The data partition Id.
        :param bool no_recognize: If true don't attempt to recognize the curves, otherwise recognize the curves
        """

        wellbore_record = mapper.map_to_wellbore_record()

        wellbore_id = self._get_wellbore_by_name(wellbore_record.data.get("FacilityName"))

        if wellbore_id is None:
            ids = self._client.create_wellbore(wellbore_record)
            logger.warning(f"New wellbore IDs: {ids}")
            wellbore_id = self._safe_get_first_record(ids)
        else:
            logger.warning(f"Existing Wellbore ID found: {wellbore_id} . Adding welllog data to the record")

        logger.info(json.dumps(self._client.get_wellbore_record(wellbore_id).get_raw_data(), indent=4, sort_keys=True))

        welllog_record = mapper.map_to_well_log_record(wellbore_id)

        # enrich welllog
        if no_recognize:
            enriched_welllog_record = welllog_record
        else:
            logger.warning("Recognizing the curve families")
            enriched_welllog_record = self._well_log_service.recognize_log_family(welllog_record, data_partition_id)

        welllog_ids = self._client.post_welllog(enriched_welllog_record)
        logger.warning(f"New welllog IDs: {welllog_ids}")

        welllog_id = self._safe_get_first_record(welllog_ids)
        welllog_record = self._client.get_welllog_record(welllog_id)
        logger.info(json.dumps(welllog_record.get_raw_data(), indent=4, sort_keys=True))

        welllog_data = mapper.extract_log_data()
        self._client.add_welllog_data(welllog_data, welllog_id)

    def _get_wellbore_by_name(self, wellbore_name: str) -> str:
        """
        Search for existing wellbores by name and return appropriate value for
        the three cases - 1 result, >1 result, 0 results.
        :param str wellbore_name: The wellbore name to search for
        :return: The id of the matching wellbore
        :rtype: str
        """
        if wellbore_name is None:
            return None

        wellbore_ids = self.search_for_wellbore(wellbore_name)

        if wellbore_ids is None or len(wellbore_ids) < 1:
            return None
        elif len(wellbore_ids) > 1:
            message = f"More than one matching wellbore found for '{wellbore_name}'."
            raise DataLoaderConflictError(message, wellbore_ids)
        else:
            return self._safe_get_first_record(wellbore_ids)

    def _safe_get_first_record(self, array: List[any]) -> any:
        """
        Get the first element from a list or return None if the list is None or empty
        :param List array: An OSDU client wrapper
        :return: The first element of the List or None
        :rtype: any
        """
        return array[0] if array is not None and len(array) > 0 else None

    def search_for_wellbore(self, wellbore_name: str) -> List[str]:
        """
        Search for existing wellbores with the provided `wellbore_name`
        :param str wellbore_name: The wellbore name to search for
        :return: List of wellbore IDs that have the provided wellbore name
        :rtype: List[str]
        """
        return self._client.search_for_wellbore(wellbore_name)
