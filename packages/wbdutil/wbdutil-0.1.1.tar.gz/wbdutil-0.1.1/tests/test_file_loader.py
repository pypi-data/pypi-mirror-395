import lasio
import pytest
from importlib import import_module
from . import TARGET_MODULE_NAME

# Test target module import
file_loader = import_module(f"{TARGET_MODULE_NAME}.common.file_loader")
LasParser = file_loader.LasParser
FileValidationError = file_loader.FileValidationError
LocalFileLoader = file_loader.LocalFileLoader


class TestLasParser:
    def test_file_loader_returns_lasio_LASFile_object(self):
        # Arrange
        las_file = "./test-las-files/15_9-19_SR_CPI.las"
        loader = LasParser(LocalFileLoader())

        # Act
        las = loader.load_las_file(las_file)

        # Assert
        assert type(las) is lasio.LASFile


class TestLasFileValidation:
    def test_LocalFileLoader_throws_when_file_not_exists(self):
        fileReader = LocalFileLoader()

        with pytest.raises(FileNotFoundError):
            fileReader.load("non_existant_file.txt")

    def test_FileValidationError_raised_when_well_name_not_populated_in_input_file(self):
        # Arrange
        invalid_las_file = "./test-las-files/15_9-19_SR_CPI_no_well_name.las"
        loader = LasParser(LocalFileLoader())

        # Act/Assert
        with pytest.raises(FileValidationError):
            loader.load_las_file(invalid_las_file)

    @pytest.mark.parametrize(
        "rec_well_name, rec_curves",
        [
            ("different well name", ["DEPTH", "BWV", "DT", "KLOGH", "KLOGV", "PHIF", "SAND_FLAG", "SW", "VSH"]),
            ("NPD-2105", ["DEPTH", "BWV"])
        ]
    )
    def test_FileValidationError_raised_when_ingest_data_las_does_not_match_welllog_record(self, rec_well_name, rec_curves):
        # Arrange
        loader = LasParser(LocalFileLoader())
        las_data = loader.load_las_file("./test-las-files/15_9-19_SR_CPI.las")

        # Act/Assert
        with pytest.raises(FileValidationError):
            loader.validate_las_file_against_record(las_data, rec_well_name, rec_curves)
