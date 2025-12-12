import json
from abc import ABC, abstractmethod
from typing import Dict


class IJsonWriter(ABC):

    @abstractmethod
    def write(self, data: Dict, filepath: str):
        """
        Write a Dict containing data to a destination.

        :param data: Dict, a dictionary of data, typically json like data.
        :param filepath: The path and filename of the file that will be created.
        """
        pass


class JsonToFile(IJsonWriter):
    def write(self, data: Dict, path: str):
        """
        Write a Dict containing data to a local json file.

        :param data: Dict, a dictionary of json like data.
        :param filepath: The path and filename of the file that will be created.
        """

        with open(path, "w") as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True)
