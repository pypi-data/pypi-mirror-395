from typing import List

from knack.log import get_logger

from ..common.configuration import Configuration
from ..common.file_loader import LocalFileLoader
from ..service.well_service import WellLogService
from ..wrapper.environment_var_helper import EnvironmentVarHelper
from ..wrapper.osdu_client import OsduClient

logger = get_logger(__name__)


def download_las(welllog_id: str, outfile: str, token: str = None, config_path: str = None, curves: List[str] = None):
    """
    Retrieve welllog data from an OSDU instance and save to a LAS format file
    :param str welllog_id: The well bore id of the record to retrieve
    :param str outfile: The path of the output file
    :param str token: a valid bearer token that is used to authenticate against the OSDU instance
    :param str config_path: Path to the configuration file
    :param List[str] curves: The curves to retrieve, use None to get all curves
    """
    token = EnvironmentVarHelper.get_token(token)
    config_path = EnvironmentVarHelper.get_config_path(config_path)

    config = Configuration(LocalFileLoader(), config_path)
    client = OsduClient(config, token)

    service = WellLogService(client)

    las_file = service.download_and_construct_las(config, welllog_id, curves)

    logger.warning(f"Writing to file {outfile}")

    with open(outfile, mode="w") as f:
        las_file.write(f, version=2)
