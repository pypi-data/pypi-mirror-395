import json
from ntpath import basename
from pathlib import Path

from knack.log import get_logger

from ..common.configuration import Configuration
from ..common.file_loader import FileUtilities, LasParser, LocalFileLoader
from ..service.record_mapper import LasToRecordMapper
from ..service.well_service import (DataLoaderConflictError, WellBoreService,
                                    WellLogService)
from ..wrapper.environment_var_helper import EnvironmentVarHelper
from ..wrapper.osdu_client import OsduClient

logger = get_logger(__name__)


def wellbore(input_path: str, token: str = None, config_path: str = None, no_recognize: bool = False):
    """
    Ingest a LAS file (single) or directory of LAS files (bulk) into OSDU
    :param str input_path: Path and filename of a LAS file OR path to directory containing LAS and config files.
    :param str token: A valid bearer token that is used to authenticate the ingest request.
    :param str config_path: Path to the LAS metadata file.
    :param bool no_recognize: If true don't attempt to recognize the curves, otherwise recognize the curves
    """
    token = EnvironmentVarHelper.get_token(token)
    config_path = EnvironmentVarHelper.get_config_path(config_path)

    config = Configuration(LocalFileLoader(), config_path)
    las_parser = LasParser(LocalFileLoader())
    client = OsduClient(config, token)
    service = WellBoreService(client, WellLogService(client))

    failed_ingests = []

    for file_path in FileUtilities.get_filenames(Path(input_path), ".las"):
        logger.warning(f"Beginning ingest of LAS file: {file_path}")

        try:
            las_data = las_parser.load_las_file(file_path)
            las_mapper = LasToRecordMapper(las_data, config)
            service.file_ingest(las_mapper, config.data_partition_id, no_recognize)
            logger.warning(f"Ingest complete: {basename(file_path)}")
        except DataLoaderConflictError as e:
            logger.error(f"Ingest failed: {basename(file_path)} (see summary for details)")
            ids = json.dumps(e.ids, indent=4, sort_keys=True)
            logger.debug(f"{basename(file_path)} ({str(e)} Matching wellbore ids {ids})")
            failed_ingests.append(
                f"{basename(file_path)} ({str(e)} Perform a search to list the conflicted wellbore ids.)"
            )
        except Exception as e:
            failed_ingests.append(f"{basename(file_path)} ({str(e)})")
            logger.error(f"Ingest failed: {basename(file_path)} (see summary for details)")

    if failed_ingests != []:
        logger.error("SUMMARY - files not ingested: ")
        for message in failed_ingests:
            logger.error(f"     {message}")


def welllog_data(welllog_id: str, input_path: str, token: str = None, config_path: str = None):
    """
    Write data from a LAS file to an existing Well Log.
    :param str welllog_id: ID of well log to be updated.
    :param str input_path: Path and filename of a LAS file containing data to be written to existing well log.
    :param str token: A valid bearer token that is used to authenticate the update request.
    :param str config_path: Path to the configuration file.
    """
    token = EnvironmentVarHelper.get_token(token)
    config_path = EnvironmentVarHelper.get_config_path(config_path)

    config = Configuration(LocalFileLoader(), config_path)
    client = OsduClient(config, token)
    service = WellLogService(client)

    failed_ingests = []
    for file_path in FileUtilities.get_filenames(Path(input_path), ".las"):
        logger.warning(f"Beginning ingest of LAS file: {file_path}")
        try:
            service.ingest_welllog_data(input_path, welllog_id)
            logger.warning(f"Ingest complete: Data written from {basename(input_path)} to Well Log ({welllog_id}).")
        except Exception as e:
            failed_ingests.append(f"{basename(file_path)} ({str(e)})")
            logger.error(f"Ingest failed: {basename(file_path)} (see summary for details)")
