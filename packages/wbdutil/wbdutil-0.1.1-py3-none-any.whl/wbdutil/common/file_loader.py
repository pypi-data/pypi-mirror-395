import json
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List

import lasio
from knack.log import get_logger
from lasio.las import LASFile

logger = get_logger(__name__)


class IFileLoader(ABC):
    @abstractmethod
    def load(self, filepath: str) -> str:
        """
        Open and load a file

        :param path: str The path and filename of the data.
        :return: the contents of the file
        :rtype: str
        :raises FileNotFoundError: If the file does not exist.
        """
        pass


class IDictionaryLoader(ABC):
    @abstractmethod
    def load(self, path: str) -> Dict[str, any]:
        """
        Load and parse a json file
        :param path str : The path and filename of the file to load.
        """
        pass


class LocalFileLoader(IFileLoader):
    def load(self, path: str) -> str:
        """
        Open and load a file from the local file system,

        :param str path: The path and filename of the data.
        :return: the contents of the file
        :rtype: str
        :raises FileNotFoundError: If the file does not exist.
        """

        if not os.path.isfile(path):
            raise FileNotFoundError(f'The file "{path}" does not exist')

        with open(path, "r") as file:
            return file.read()


class FileValidationError(Exception):
    """
    Custom error for file validation.
    """

    def __init__(self, message="File must have a valid Well Name populated."):
        super().__init__(message)


class JsonLoader(IDictionaryLoader):
    def __init__(self, file_loader: IFileLoader):
        """
        Construct a new instance of JsonLoader.
        :param file_loader IFileLoader : an instance of a file loader.
        """
        self._file_loader = file_loader

    def load(self, path: str) -> Dict[str, any]:
        """
        Load and parse a json file
        :param path str : The path and filename of the file to load.
        """
        return json.loads(self._file_loader.load(path))


class LasParser:
    def __init__(self, file_loader: IFileLoader):
        """
        Construct a new instance of LasParser.
        :param file  Union[IO, str]: Either a filename (inc. path), an open file object, or a string containing the contents of a file.
        """
        self._file_loader = file_loader

    def validate_las_file(self, las: LASFile):
        """
        Validate that the Well Name attribute of the inputted LAS file has been populated.

        :param las LASFile: The LASFile object to be validated.
        """
        well_name = las.well.WELL.value
        if not well_name or well_name == " ":
            raise FileValidationError

    def validate_las_file_against_record(self, las: LASFile, record_well_name: str, rec_curve_mnemonics: List[str]):
        """
        More extensive validation of a LAS file if it is to be used to write data to an existing record (as
        opposed to creating new wellbore and well log records).
        In addition to confirming the Well Name attribute of the LAS file has been populated, the well
        name and curves are validated against the existing Wellbore and Well Log records respectively.

        :param las LASFile: The LASFile object to be validated.
        :param record_well_name str: Well name associated with the well log record that is to have data written to it.
        :param rec_curve_mnemonics List[str]: List of available curves in well log record.
        """
        self.validate_las_file(las)

        las_well_name = str(las.well.WELL.value)
        logger.warning(f"LAS well name: {las_well_name}")
        logger.warning(f"Well log record well name: {record_well_name}")
        if not las_well_name == record_well_name:
            raise FileValidationError("Well name associated with well log record does not match well name in LAS file.")

        las_curve_mnemonics = [curve.mnemonic for curve in las.curves] if las.curves else []
        logger.warning(f"LAS curves: {las_curve_mnemonics}")
        logger.warning(f"Well log record curves: {rec_curve_mnemonics}")
        if not all(curve in rec_curve_mnemonics for curve in las_curve_mnemonics):
            raise FileValidationError("Curves available in well log record do not match those in LAS file.")

    def load_las_file(self, path: str) -> LASFile:
        """
        Parse a LAS format data into a LASFile object.

        :param file str: A path and filename of a las file.
        :return: A LASFile object.
        """

        las = lasio.read(self._file_loader.load(path))

        try:
            self.validate_las_file(las)
        except FileValidationError as e:
            print(f"LAS file validation failed: {str(e)}")
            raise e
        except Exception as e:
            print(f"Unexpected error validating file: {str(e)}")
            raise e

        return las


class FileUtilities:
    @staticmethod
    def get_filenames(path: Path, suffix: str = "") -> List[Path]:
        """
        Get the paths of the files in a path and with a suffix.
        If Path itself is a file returns a single item List that contains Path.
        If Path is a directory return a List of all the paths of all the files in the directory with suffix.
        :param Path path: A director or file path
        :return: A List of paths.
        :rtype: List[Path]
        """
        if path.is_file():
            return [path]
        elif path.is_dir():
            return list(path.glob(f"**/*{suffix}"))
        else:
            logger.error("Invalid input paths. Please confirm you have provided the required inputs correctly.")
