import json
from typing import List

from knack.log import get_logger

from ..common.configuration import Configuration
from ..common.file_loader import LocalFileLoader
from ..wrapper.environment_var_helper import EnvironmentVarHelper
from ..wrapper.osdu_client import OsduClient

logger = get_logger(__name__)


def wellbore(wellbore_id: str,
             token: str = None,
             config_path: str = None):
    """
    Retrieve and print wellbore record from an OSDU instance
    :param str wellbore_id: The well bore id of the record to retrieve
    :param str token: a valid bearer token that is used to authenticate against the OSDU instance
    :param str config_path: Path to the configuration file
    """
    token = EnvironmentVarHelper.get_token(token)
    config_path = EnvironmentVarHelper.get_config_path(config_path)

    config = Configuration(LocalFileLoader(), config_path)
    client = OsduClient(config, token)
    logger.warning(f"Getting wellbore ID {wellbore_id}")
    wellbore = client.get_wellbore_record(wellbore_id)

    print(json.dumps(wellbore.get_raw_data(), indent=4, sort_keys=True))


def welllog(welllog_id: str,
            token: str = None,
            config_path: str = None,
            curves: bool = False):
    """
    Retrieve and print welllog record from an OSDU instance
    :param str wellbore_id: The well bore id of the record to retrieve
    :param str token: a valid bearer token that is used to authenticate against the OSDU instance
    :param str config_path: Path to the las metadata file
    :param bool curves: Boolean to determine whether to list curves
    """
    token = EnvironmentVarHelper.get_token(token)
    config_path = EnvironmentVarHelper.get_config_path(config_path)

    config = Configuration(LocalFileLoader(), config_path)
    client = OsduClient(config, token)
    logger.warning(f"Getting welllog ID {welllog_id}")

    welllog = client.get_welllog_record(welllog_id)

    if curves:
        print(welllog.get_curveids())
    else:
        print(json.dumps(welllog.get_raw_data(), indent=4, sort_keys=True))


def welllog_data(welllog_id: str,
                 token: str = None,
                 config_path: str = None,
                 curves: List[str] = None):
    """
    Retrieve and print welllog data from an OSDU instance
    :param str welllog_id: The welllog id of the record to retrieve
    :param str token: a valid bearer token that is used to authenticate against the OSDU instance
    :param str config_path: Path to the las metadata file
    :param List[str] curves: The curves to retrieve, use None to get all curves
    """
    token = EnvironmentVarHelper.get_token(token)
    config_path = EnvironmentVarHelper.get_config_path(config_path)

    config = Configuration(LocalFileLoader(), config_path)
    client = OsduClient(config, token)
    logger.warning(f"Getting data for welllog ID {welllog_id}")

    if curves:
        logger.warning(f"Curves {curves}")

    welllog_data = client.get_welllog_data(welllog_id, curves)

    if welllog_data is not None:
        print(welllog_data.to_string())
