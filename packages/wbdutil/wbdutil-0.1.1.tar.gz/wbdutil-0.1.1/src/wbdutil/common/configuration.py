from typing import Any, Dict, List, Union

from .file_loader import IFileLoader, JsonLoader
from .reflection_utilities import ReflectionHelper


class Configuration:
    """
    Class to hold metadata for LAS ingestion
    """

    def __init__(self, file_loader: IFileLoader, path: str) -> None:
        """
        Load JSON configuration using the file loader and create a new instance of a Configuration

        :param IFileLoader file_loader: The file loader instance to user
        :param str path: The full path and filename of the configuration file.
        """
        json_parser = JsonLoader(file_loader)
        self._config = json_parser.load(path)

    def get_recursive(self, qualified_attribute_name: List[str]) -> str:
        """
        Gets an item specified by its qualified attribute name - eg ["legal", "legaltags"] will get config[legal][legaltags].
        :param str qualified_attribute_name: The exception message
        return: the base url for API calls
        rtype: str
        """
        return ReflectionHelper.getattr_recursive(self._config, qualified_attribute_name)

    @property
    def base_url(self) -> str:
        """
        Gets the base url.
        return: the base url for API calls
        rtype: str
        """
        return self._config.get("base_url")

    @property
    def data_partition_id(self) -> str:
        """
        Gets the data partition Id.
        return: the data partition id
        rtype: str
        """
        return self._config.get("data_partition_id")

    @property
    def wellbore_mapping(self) -> Union[Dict[str, Any], None]:
        """
        Gets the wellbore_mapping.
        return: the wellbore_mapping
        rtype:  Dict[str, Any]
        """
        return self._config.get("wellbore_mapping")

    @property
    def welllog_mapping(self) -> Union[Dict[str, Any], None]:
        """
        Gets the welllog_mapping.
        return: the welllog_mapping
        rtype:  Dict[str, Any]
        """
        return self._config.get("welllog_mapping")

    @property
    def las_file_mapping(self) -> Union[Dict[str, Any], None]:
        """
        Gets the las_file_mapping.
        return: the las_file_mapping
        rtype:  Dict[str, Any]
        """
        return self._config.get("las_file_mapping")

    @property
    def wellbore_service_path_prefix(self) -> str:
        """
        Gets the wellbore_service_path_prefix.
        return: the prefix for wellbore service
        rtype: str
        """
        return self._config.get("wellbore_service_path_prefix")

    @property
    def search_service_path_prefix(self) -> str:
        """
        Gets the search_service_path_prefix.
        return: the prefix for search service
        rtype: str
        """
        return self._config.get("search_service_path_prefix")
