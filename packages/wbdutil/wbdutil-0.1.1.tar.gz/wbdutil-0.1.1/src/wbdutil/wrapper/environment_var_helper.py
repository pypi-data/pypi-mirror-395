import os

from knack.log import get_logger

logger = get_logger(__name__)


class MissingArgumentError(Exception):
    """
    Custom error for missing arguments.
    """

    def __init__(self, message="Required arguments not provided. See error logs for details."):
        super().__init__(message)


class EnvironmentVarHelper:
    def get_token(arg_token: str) -> str:
        if arg_token is not None:
            return arg_token
        token = os.environ.get('OSDUTOKEN')
        if token is not None:
            return token

        logger.error("A bearer token was not provided as an environment variable ('OSDUTOKEN') or command argument.")
        raise MissingArgumentError

    def get_config_path(arg_config_path: str) -> str:
        if arg_config_path is not None:
            return arg_config_path
        config_path = os.environ.get('CONFIGPATH')
        if config_path is not None:
            return config_path

        logger.error("A path to a configuration file was not provided as an environment variable ('CONFIGPATH') or command argument.")
        raise MissingArgumentError
