import json

from knack.log import get_logger

from ..common.configuration import Configuration
from ..common.file_loader import LocalFileLoader
from ..service.well_service import WellBoreService, WellLogService
from ..wrapper.environment_var_helper import EnvironmentVarHelper
from ..wrapper.osdu_client import OsduClient

logger = get_logger(__name__)


def wellbore_search(wellbore_name: str, token: str = None, config_path: str = None):
    """
    Retrieve and print the ids of wellbores that match the specified name
    :param str wellbore_name: The well bore name to search for
    :param str token: a valid bearer token that is used to authenticate against the OSDU instance
    :param str config_path: Path to the configuration file
    """
    token = EnvironmentVarHelper.get_token(token)
    config_path = EnvironmentVarHelper.get_config_path(config_path)

    config = Configuration(LocalFileLoader(), config_path)
    client = OsduClient(config, token)
    service = WellBoreService(client, WellLogService(client))

    data = service.search_for_wellbore(wellbore_name)

    if data is None or len(data) < 1:
        logger.warning("No records found")
    else:
        print("Matching Wellbore ids:")
        print(json.dumps(data, indent=4, sort_keys=True))
