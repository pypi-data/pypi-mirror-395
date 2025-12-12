from typing import Any, Dict, List

from knack.log import get_logger

from .exceptions import WbdutilAttributeError, WbdutilValueError

logger = get_logger(__name__)


class ReflectionHelper:
    def getattr_recursive(source: any, source_field_heirachy: List[str]) -> any:
        """
        Get the specified field from the source object in a recursive manner.
        :param any destination: The source object
        :param List[str] source_field_heirachy: List of fields, from lowest to the deepest in the heirachy.
        :return: The data value.
        :rtype: any
        """
        field_name = source_field_heirachy.pop(0)

        try:
            if isinstance(source, dict):
                subfield = source[field_name]
            elif isinstance(source, int):
                subfield = source
            else:
                subfield = getattr(source, field_name)

        except (KeyError, AttributeError):
            if field_name.endswith(']') and '[' in field_name:
                # probably a reference to a list item
                logger.debug(f"Attempting to parse the mapping field {field_name} as an array")
                subfield = ReflectionHelper._getattr_list(source, field_name)
            else:
                message = f"The attribute '{field_name}' was not found in the source data. An empty value for this field will be returned."
                logger.error(message)
                return None

        if len(source_field_heirachy) == 0:
            return subfield
        else:
            return ReflectionHelper.getattr_recursive(subfield, source_field_heirachy)

    def _getattr_list(source: any, source_field_name: str) -> any:

        try:
            segments = source_field_name.split('[')

            if isinstance(source, dict):
                subfield = source[segments.pop(0)]
            else:
                subfield = getattr(source, segments.pop(0))

            for ind in segments:
                subfield = subfield[int(ind.rstrip(']'))]

            return subfield

        except (KeyError, AttributeError, ValueError) as ex:
            message = f"The attribute '{source_field_name}' could not be parsed as an array"
            logger.error(message)
            raise WbdutilAttributeError(message, ex)

    def setattr_recursive(value: any, destination: Dict[str, Any], destination_field_heirachy: List[str]) -> None:
        """
        Set the specified field to the given value, recursively create member objects where needed. Update in place.
        :param any value: The data value
        :param any destination: The destination object
        :param List[str] destination_field_heirachy: List of fields in the hierarchy, ordered from top to bottom.
        """
        if destination is None:
            message = "The destination dictionary must not be null"
            logger.critical(message)
            raise WbdutilValueError(message)

        field_name = destination_field_heirachy.pop(0)

        if len(destination_field_heirachy) == 0:
            destination[field_name] = value
            return destination

        if field_name not in destination:
            destination[field_name] = {}

        ReflectionHelper.setattr_recursive(value, destination[field_name], destination_field_heirachy)
