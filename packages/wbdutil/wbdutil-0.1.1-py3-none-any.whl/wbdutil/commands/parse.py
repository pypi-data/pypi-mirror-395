from pathlib import Path

from knack.log import get_logger

from ..common.configuration import Configuration
from ..common.file_loader import FileUtilities, LasParser, LocalFileLoader
from ..service.record_mapper import LasToRecordMapper
from ..wrapper.environment_var_helper import EnvironmentVarHelper
from ..wrapper.json_writer import JsonToFile

logger = get_logger(__name__)


def printlas(input_path):
    """
    Print a LAS file header
    :param str input_path: Path and filename of a LAS file or folder containing LAS files
    """

    las_parser = LasParser(LocalFileLoader())
    logger.info(f"LAS path: {input_path}")
    for file_path in FileUtilities.get_filenames(Path(input_path), '.las'):
        logger.warning(f"LAS file: {file_path}")
        las_data = las_parser.load_las_file(file_path)
        print(las_data.header)


def convert(input_path: str, wellbore_id: str, config_path: str = None):
    """
    Convert a LAS file to Wellbore and Well Log and write to JSON files.
    :param str input_path: Path and filename of a LAS file or folder containing LAS files
    :param str wellbore_id: The wellbore id
    :param str config_path: Path to the configuration file
    """
    config_path = EnvironmentVarHelper.get_config_path(config_path)

    las_parser = LasParser(LocalFileLoader())
    config = Configuration(LocalFileLoader(), config_path)

    logger.info(f"LAS path: {input_path}")
    for file_path in FileUtilities.get_filenames(Path(input_path), '.las'):
        logger.warning(f"LAS file: {file_path}")
        las_data = las_parser.load_las_file(file_path)

        mapper = LasToRecordMapper(las_data, config)
        wellbore_record = mapper.map_to_wellbore_record()
        welllog_record = mapper.map_to_well_log_record(wellbore_id)

        path = Path(file_path)
        writer = JsonToFile()

        writer.write(wellbore_record.get_raw_data(), path.with_suffix('.wellbore.json'))
        logger.warning(f"Wellbore record file created: {path.with_suffix('.wellbore.json')}")
        writer.write(welllog_record.get_raw_data(), path.with_suffix('.welllog.json'))
        logger.warning(f"Well log record file created: {path.with_suffix('.welllog.json')}")
