from knack.log import get_logger

from ..common.configuration import Configuration
from ..common.file_loader import LocalFileLoader
from ..service.well_service import WellLogService
from ..wrapper.environment_var_helper import EnvironmentVarHelper
from ..wrapper.osdu_client import DataLoaderWebResponseError, OsduClient

logger = get_logger(__name__)


def welllog(welllog_id: str, token: str = None, config_path: str = None, curve_families: bool = True):
    """
    Update an existing well log record.
    :param str welllog_id: ID of the well log to be updated.
    :param str token: A valid bearer token that is used to authenticate the update request.
    :param str config_path: Path to the configuration file.
    :param str curve_families: If true, recognize and update the curve families, otherwise don't.
    """
    # This command currently only contains functionality to update the curve families of a well log.
    # It is set up in such a way that it should be possible to extend to include other update operations in future if needed.
    token = EnvironmentVarHelper.get_token(token)
    config_path = EnvironmentVarHelper.get_config_path(config_path)

    config = Configuration(LocalFileLoader(), config_path)
    client = OsduClient(config, token)
    service = WellLogService(client)

    if curve_families:
        logger.info("Recognizing curve families and updating well log record.")
        try:
            service.update_log_family(welllog_id, config.data_partition_id)
        except DataLoaderWebResponseError as ex:
            logger.error(f"Error - record not updated: {str(ex)}")
            return
        logger.warning(f"Curve families recognized and updated for well log: {welllog_id}")
    else:
        logger.warning("No updates made - set command option 'curve_families' to True to update curve families.")
