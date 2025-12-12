from abc import ABC, abstractmethod
from typing import Any, Dict

from knack.log import get_logger

from ..common.configuration import Configuration
from ..common.exceptions import WbdutilAttributeError
from ..common.reflection_utilities import ReflectionHelper

logger = get_logger(__name__)


class IPropertyMappingLoader(ABC):
    @property
    @abstractmethod
    def mapping(self) -> Dict[str, Any]:
        pass

    @property
    @abstractmethod
    def kind(self) -> str:
        pass


class DictionaryMappingLoader(IPropertyMappingLoader):
    def __init__(self, base_mapping: Dict[str, Any]) -> None:
        self._base_mapping = base_mapping

    @property
    def mapping(self) -> Dict[str, Any]:
        """
        Gets the mapping dictionary.
        return:The mapping
        rtype: Dict[str, any]
        """
        return self._base_mapping["mapping"]

    @property
    def kind(self) -> str:
        """
        Gets the kind for the mapping
        return: the kind string
        rtype: str
        """
        return self._base_mapping.get("kind")


class PropertyMapper:
    """
    Class to handle the mapping of one data type to another using a dictionary of mappings
    """

    _mapping_functions: Any
    _config: Configuration
    _kind: str
    _mapping: Dict[str, Any]

    def __init__(self, loader: IPropertyMappingLoader, config: Configuration, mapping_functions: any) -> None:
        """
        Create a new instance of a PropertyMapper
        :param IPropertyMappingLoader loader: A IPropertyMappingLoader loader instance that
                                              contains the mapping between data types.
        :param Configuration config: The application configuration
        :param any mapping_functions: An instance of a class that contains the available mapping functions
        """
        self._mapping = loader.mapping
        self._kind = loader.kind
        self._config = config
        self._mapping_functions = mapping_functions

    def remap_data_with_kind(self, source: any) -> Dict[str, Any]:
        """
        Remap the data in the source object using the mapping dictionary to a new object. Adds the kind field extracted from the config
        :param any source: The source object
        :return: A new data object that contains the remapped data
        :rtype: Dict[str, Any]
        """
        destination = self.remap_data(source, {})
        destination["kind"] = self._kind
        return destination

    def remap_data(self, source: any, destination: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remap the data in the source object using the mapping dictionary to a new object
        :param any source: The source object
        :param Dict[str, Any] destination: The destination object

        :return: The populated destination object
        :rtype: Dict[str, Any]
        """

        return self._remap_data(source, self._mapping, destination)

    def _remap_data(self, source: any, mapping: Dict[str, Any], extensible: Dict[str, Any]) -> Dict[str, Any]:

        # iterate through the mapping dictionary remapping data as we go
        for target_field, source_field in mapping.items():
            source_data = self._get_source_attribute_value(source, source_field)
            ReflectionHelper.setattr_recursive(source_data, extensible, target_field.split('.'))

        return extensible

    def _get_source_attribute_value(self, source, source_field):
        if isinstance(source_field, dict):
            source_data = self._process_complex_mapping(source, source_field)
        elif isinstance(source_field, int):
            source_data = source_field
        else:
            source_field_list = source_field.split('.')
            if source_field_list[0] == "CONFIGURATION":
                # get data from config
                del source_field_list[0]
                source_data = self._config.get_recursive(source_field_list)
            else:
                # Get data from source
                source_data = ReflectionHelper.getattr_recursive(source, source_field_list)

        return source_data

    def _process_complex_mapping(self, source: any, source_field: Dict[str, Any]) -> any:
        mapping_type = source_field.get("type")

        if mapping_type is None:
            raise ValueError("The mapping type must be specified. Supported types are: function, array")

        if mapping_type == "function":
            try:
                function_name = source_field.get("function")
                if function_name is None:
                    raise ValueError("The function name must be given in the configuration file")

                argument_names = source_field.get("args", [])

                if not isinstance(argument_names, list):
                    message = f"The mapping function arguments must be a list but was '{type(argument_names)}'."
                    logger.error(message)
                    raise WbdutilAttributeError(message, None)

                if len(argument_names) > 0 and any(not isinstance(a, str) for a in argument_names):
                    message = "All of the mapping function arguments must be strings."
                    logger.error(message)
                    raise WbdutilAttributeError(message, None)

                arguments = [self._get_source_attribute_value(source, a) for a in argument_names]
                function_to_call = getattr(self._mapping_functions, function_name)

                return function_to_call(*arguments)

            except AttributeError as ex:
                message = f"The function '{function_name}' was not found in the provided mapping functions"
                logger.error(message)

                raise WbdutilAttributeError(message, ex)

        elif mapping_type == "array":
            source_array_name = source_field.get("source")
            source_array = self._get_source_attribute_value(source, source_array_name)
            submapping = source_field.get("mapping", {})

            remapped_array = []
            for item in source_array:
                remapped_array.append(self._remap_data(item, submapping, {}))

            return remapped_array

        raise ValueError("Unknown mapping type: {mapping_type}. Supported types are: function, array")
