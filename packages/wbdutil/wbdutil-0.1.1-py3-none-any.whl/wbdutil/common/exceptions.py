from typing import List


class WbdutilException(Exception):
    """
    Base class for exceptions raised within Wdutil
    """

    def __init__(self, *args):
        """
        Create a new instance of a WdutilException

        :param *args object: The Exception arguments
        """
        super().__init__(args)


class WbdutilValidationException(Exception):
    """
    General validation exception raised within Wdutil
    """

    def __init__(self, error_messages: List[str], *args):
        """
        Create a new instance of a WdutilValidationException

        :param error_messages List[str]: The validation errors
        :param *args object: The Exception arguments
        """
        self._error_messages = error_messages
        super().__init__(args)

    @property
    def error_messages(self) -> List[str]:
        """
        Gets the list of validation errors
        return: the validation errors
        rtype: List[str]
        """
        return self._error_messages


class WbdutilAttributeError(WbdutilException):
    """
    Common exception class for attribute errors raised in the Wbdutil
    """

    def __init__(self, message: str, inner_exception: Exception, *args):
        """
        Create a new instance of a ExtendedPropertiesAttributeError
        :param str message: The exception message
        :param inner_exception Exception: The inner exception
        :param args object: The Exception arguments
        """
        self.message = message
        self.inner_exception = inner_exception
        super().__init__(args)


class WbdutilValueError(Exception):
    def __init__(self, *args):
        """
        Create a new instance of a WbdutilValueError

        :param *args object: The Exception arguments
        """
        super().__init__(args)
