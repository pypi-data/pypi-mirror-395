import pytest
from pandas import DataFrame
from lasio import LASFile
from unittest.mock import Mock
from importlib import import_module
from . import TARGET_MODULE_NAME

# Test target module import
record_mapper = import_module(f"{TARGET_MODULE_NAME}.service.record_mapper")
Record = record_mapper.Record
LasToRecordMapper = record_mapper.LasToRecordMapper
WellLogRecord = record_mapper.WellLogRecord
MappingUtilities = record_mapper.MappingUtilities
MapWellLogToLas = record_mapper.MapWellLogToLas

file_loader = import_module(f"{TARGET_MODULE_NAME}.common.file_loader")
LasParser = file_loader.LasParser
LocalFileLoader = file_loader.LocalFileLoader

Configuration = import_module(f"{TARGET_MODULE_NAME}.common.configuration").Configuration


@pytest.fixture
def las():
    loader = LasParser(LocalFileLoader())
    las_file = "./test-las-files/15_9-19_SR_CPI.las"
    return loader.load_las_file(las_file)


@pytest.fixture
def las_with_no_uwi():
    loader = LasParser(LocalFileLoader())
    las_file = "./test-las-files/15_9-19_SR_CPI_no_uwi.las"
    return loader.load_las_file(las_file)


@pytest.fixture
def las_with_no_uwi_field():
    loader = LasParser(LocalFileLoader())
    las_file = "./test-las-files/15_9-19_SR_CPI_no_uwi_field.las"
    return loader.load_las_file(las_file)


@pytest.fixture
def config():
    return Configuration(LocalFileLoader(), "./test-config-files/config_example.json")


@pytest.fixture
def config_incomplete():
    return Configuration(LocalFileLoader(), "./test-config-files/config_example_incomplete.json")


@pytest.fixture
def record_mapper(las):
    return LasToRecordMapper(las, Configuration(LocalFileLoader(), "./test-config-files/config_example.json"))


@pytest.fixture
def record_mapper_las_with_no_uwi(las_with_no_uwi):
    return LasToRecordMapper(
        las_with_no_uwi,
        Configuration(LocalFileLoader(), "./test-config-files/config_example.json"))


@pytest.fixture
def record_mapper_las_with_no_uwi_field(las_with_no_uwi_field):
    return LasToRecordMapper(
        las_with_no_uwi_field,
        Configuration(LocalFileLoader(), "./test-config-files/config_example.json"))


class TestLasToRecordMapper:
    @pytest.mark.parametrize("invalid_las_input", ["not a las object", True, 5, 0.123, ["str", 20]])
    def test_record_mapper_raises_TypeError_when_input_not_las_object(self, invalid_las_input, config):

        with pytest.raises(TypeError):
            LasToRecordMapper(invalid_las_input, Configuration(
                LocalFileLoader(), "./test-config-files/config_example.json"))

    def test_record_mapper_raises_FileNotFoundError_when_config_file_not_found(self, las):
        with pytest.raises(FileNotFoundError):
            LasToRecordMapper(las, Configuration(LocalFileLoader(), "a/non/existent/file/path/config.json"))

    def test_wellbore_mapping_returns_Record_object_containing_formatted_config_variables(self, record_mapper):
        # Arrange
        expected_wellbore_record = Record({
            "kind": "osdu:wks:master-data--Wellbore:1.0.0",
            "acl": {'viewers': ['data.default.viewers@opendes.contoso.com'], 'owners': ['data.default.owners@opendes.contoso.com']},
            "legal": {'legaltags': ['opendes-public-usa-dataset-7643990'], 'otherRelevantDataCountries': ['US'], 'status': 'compliant'},
            "data": {
                'FacilityName': 'NPD-2105',
                'NameAliases': [
                    {'AliasName': 'UWI12345', 'AliasNameTypeID': 'opendes:reference-data--AliasNameType:UniqueIdentifier:'}
                ]
            }
        })

        # Act
        wellbore_record = record_mapper.map_to_wellbore_record()

        # Assert
        assert isinstance(wellbore_record, Record)
        assert wellbore_record.get_raw_data() == expected_wellbore_record.get_raw_data()

    def test_wellbore_mapping_returns_Record_object_containing_formatted_config_variables_record_mapper_las_with_no_uwi(
        self,
        record_mapper_las_with_no_uwi
    ):
        # Arrange
        expected_wellbore_record = Record({
            "kind": "osdu:wks:master-data--Wellbore:1.0.0",
            "acl": {'viewers': ['data.default.viewers@opendes.contoso.com'], 'owners': ['data.default.owners@opendes.contoso.com']},
            "legal": {'legaltags': ['opendes-public-usa-dataset-7643990'], 'otherRelevantDataCountries': ['US'], 'status': 'compliant'},
            "data": {'FacilityName': 'NPD-2105', 'NameAliases': []}
        })

        # Act
        wellbore_record = record_mapper_las_with_no_uwi.map_to_wellbore_record()

        # Assert
        assert isinstance(wellbore_record, Record)
        assert wellbore_record.get_raw_data() == expected_wellbore_record.get_raw_data()

    def test_wellbore_mapping_returns_Record_object_containing_formatted_config_variables_las_with_no_uwi_field(
        self,
        record_mapper_las_with_no_uwi_field
    ):
        # Arrange
        expected_wellbore_record = Record({
            "kind": "osdu:wks:master-data--Wellbore:1.0.0",
            "acl": {
                'viewers': ['data.default.viewers@opendes.contoso.com'],
                'owners': ['data.default.owners@opendes.contoso.com']
            },
            "legal": {
                'legaltags': ['opendes-public-usa-dataset-7643990'],
                'otherRelevantDataCountries': ['US'],
                'status': 'compliant'
            },
            "data": {
                'FacilityName': 'NPD-2105',
                'NameAliases': []
            }
        })

        # Act
        wellbore_record = record_mapper_las_with_no_uwi_field.map_to_wellbore_record()

        # Assert
        assert isinstance(wellbore_record, Record)
        assert wellbore_record.get_raw_data() == expected_wellbore_record.get_raw_data()

    def test_well_log_mapping_returns_Record_object_containing_formatted_config_variables(
            self, record_mapper):
        # Arrange
        expected_well_log_record = Record({
            "kind": "osdu:wks:work-product-component--WellLog:1.1.0",
            "acl": {'viewers': ['data.default.viewers@opendes.contoso.com'], 'owners': ['data.default.owners@opendes.contoso.com']},
            "legal": {'legaltags': ['opendes-public-usa-dataset-7643990'], 'otherRelevantDataCountries': ['US'], 'status': 'compliant'},
            "data": {
                'ReferenceCurveID': 'DEPTH',
                'Curves': [
                    {'CurveID': 'DEPTH', 'CurveUnit': 'opendes:reference-data--UnitOfMeasure:M:', 'Mnemonic': 'DEPTH'},
                    {'CurveID': 'BWV', 'CurveUnit': 'opendes:reference-data--UnitOfMeasure:UNITLESS:', 'Mnemonic': 'BWV'},
                    {'CurveID': 'DT', 'CurveUnit': 'opendes:reference-data--UnitOfMeasure:UNITLESS:', 'Mnemonic': 'DT'},
                    {'CurveID': 'KLOGH', 'CurveUnit': 'opendes:reference-data--UnitOfMeasure:MD:', 'Mnemonic': 'KLOGH'},
                    {'CurveID': 'KLOGV', 'CurveUnit': 'opendes:reference-data--UnitOfMeasure:MD:', 'Mnemonic': 'KLOGV'},
                    {'CurveID': 'PHIF', 'CurveUnit': 'opendes:reference-data--UnitOfMeasure:V%2FV:', 'Mnemonic': 'PHIF'},
                    {'CurveID': 'SAND_FLAG', 'CurveUnit': 'opendes:reference-data--UnitOfMeasure:UNITLESS:', 'Mnemonic': 'SAND_FLAG'},
                    {'CurveID': 'SW', 'CurveUnit': 'opendes:reference-data--UnitOfMeasure:V%2FV:', 'Mnemonic': 'SW'},
                    {'CurveID': 'VSH', 'CurveUnit': 'opendes:reference-data--UnitOfMeasure:V%2FV:', 'Mnemonic': 'VSH'}
                ],
                'WellboreID': 'WB12348:'
            }
        })

        # Act
        well_log_record = record_mapper.map_to_well_log_record("WB12348")

        # Assert
        assert isinstance(well_log_record, Record)
        assert well_log_record.get_raw_data() == expected_well_log_record.get_raw_data()

    def test_extract_log_data(self):
        # Arrange
        rawdata = {'one': [4., 5., 6., 7.], 'two': [7., 6., 5., 4.]}

        expected_result = DataFrame(rawdata)
        mockLas = Mock(spec=LASFile)
        mockLas.df.return_value = expected_result

        subject = LasToRecordMapper(mockLas, Mock(spec=Configuration))

        # Act
        result = subject.extract_log_data()

        # Assert
        assert isinstance(result, DataFrame)
        assert expected_result.reset_index().equals(result)


class TestRecord:
    def test_construct_with_empty_dict(self):
        record = Record({})

        assert record.data == {}
        assert record.get_raw_data()["acl"] == {}
        assert record.get_raw_data()["kind"] is None
        assert record.get_raw_data()["legal"] == {}
        assert "id" not in record.get_raw_data()
        assert record.get_raw_data() == {"kind": None, "acl": {}, "legal": {}, "data": {}}

    def test_construct_with_populated_dict(self):
        wellbore = {
            'data':
            {
                'FacilityName': 'a well name',
                'NameAliases': [{'AliasName': 'name', 'AliasNameTypeID': 'typeID'}]
            },
            'acl': {'some': 'acl'},
            'kind': 'A Kind',
            'legal': {'some': 'legal'},
            'id': 'WBID-123'
        }

        record = WellLogRecord(wellbore)

        assert record.data == wellbore['data']
        assert record.get_raw_data()["acl"] == wellbore['acl']
        assert record.get_raw_data()["kind"] == wellbore['kind']
        assert record.get_raw_data()["legal"] == wellbore['legal']
        assert record.get_raw_data()["id"] == wellbore['id']
        assert record.get_raw_data() == wellbore


class TestWellLogRecord:
    def test_construct_with_empty_dict(self):
        record = WellLogRecord({})

        assert record.data == {}
        assert record.get_raw_data()["acl"] == {}
        assert record.get_raw_data()["kind"] is None
        assert record.get_raw_data()["legal"] == {}
        assert "id" not in record.get_raw_data()
        assert record.get_raw_data() == {"kind": None, "acl": {}, "legal": {}, "data": {}}
        assert record.get_curveids() == []

    def test_construct_with_populated_dict(self):
        welllog = {
            'data':
            {
                'some': 'data',
                'Curves': [{'CurveID': 'abc'}, {'CurveID': 'xyz'}]
            },
            'acl': {'some': 'acl'},
            'kind': 'A Kind',
            'legal': {'some': 'legal'},
            'id': 'WLID-123'
        }

        record = WellLogRecord(welllog)

        assert record.data == welllog['data']
        assert record.get_raw_data()["acl"] == welllog['acl']
        assert record.get_raw_data()["kind"] == welllog['kind']
        assert record.get_raw_data()["legal"] == welllog['legal']
        assert record.get_raw_data()["id"] == welllog['id']
        assert record.get_raw_data() == welllog
        assert record.get_curveids() == ['abc', 'xyz']


class TestMappingUtilities:
    @pytest.mark.parametrize("osdu_unit,expected",
                             [("opendes:reference-data--UnitOfMeasure:M:", "M"), ("opendes:reference-data--UnitOfMeasure:GAPI:", "GAPI"),
                              ("opendes:reference-data--UnitOfMeasure:US%2FF:", "US/F"),
                              ("opendes:reference-data--UnitOfMeasure:G%2FC3:", "G/C3")])
    def test_convert_osdu_unit_to_raw_unit(self, osdu_unit, expected):
        # Assemble
        # Act
        result = MappingUtilities.convert_osdu_unit_to_raw_unit(osdu_unit)

        # Assert
        assert result == expected

    @pytest.mark.parametrize("osdu_unit", ["", None, "opendes:reference-data--UnitOfMeasure"])
    def test_convert_osdu_unit_to_raw_unit_bad_data(self, osdu_unit):
        # Assemble
        # Act
        result = MappingUtilities.convert_osdu_unit_to_raw_unit(osdu_unit)

        # Assert
        assert result is None


class TestMapWellLogToLas:
    def test_build_las_file_happy(self):
        # Assemble
        logdata = {
            "Curves": [
                {"CurveID": "ABC", "CurveUnit": "opendes:reference-data--UnitOfMeasure:M:"},
                {"CurveID": "LMN", "CurveUnit": "opendes:reference-data--UnitOfMeasure:Ft:"},
                {"CurveID": "XYZ", "CurveUnit": "opendes:reference-data--UnitOfMeasure:GAPI:"}]
        }

        welllog = Record({"kind": "LogKind", "acl": {}, "legal": {}, "data": logdata})
        wellbore = Record({
            "kind": "BoreKind",
            "acl": {},
            "legal": {},
            "data": {"FacilityName": "Well name", "NameAliases": [{"AliasName": "Some Name"}]}
        })
        data = DataFrame({"ABC": [1, 2, 3], "XYZ": [9, 8, 7], "IJK": [-1, -2, -3]})

        mockConfig = Mock(spec=Configuration)
        mockConfig.las_file_mapping = None
        subject = MapWellLogToLas(mockConfig, wellbore, welllog, data)

        # ACT
        result = subject.build_las_file()

        # Assert
        assert result.well.UWI.value == "Some Name"
        assert result.well.WELL.value == "Well name"

        assert len(result.curves) == 3
        assert result.curves[0].mnemonic == "ABC"
        assert result.curves[0].unit == "M"
        assert (result.curves[0].data == [1, 2, 3]).all()

        assert result.curves[1].mnemonic == "XYZ"
        assert result.curves[1].unit == "GAPI"
        assert (result.curves[1].data == [9, 8, 7]).all()

        assert result.curves[2].mnemonic == "IJK"
        assert result.curves[2].unit is None
        assert (result.curves[2].data == [-1, -2, -3]).all()

    def test_build_las_file_no_curve_data(self):
        # Assemble
        logdata = {
            "Curves": [
                {"CurveID": "ABC", "CurveUnit": "opendes:reference-data--UnitOfMeasure:M:"},
                {"CurveID": "LMN", "CurveUnit": "opendes:reference-data--UnitOfMeasure:Ft:"},
                {"CurveID": "XYZ", "CurveUnit": "opendes:reference-data--UnitOfMeasure:GAPI:"}]
        }

        welllog = Record({"kind": "LogKind", "acl": {}, "legal": {}, "data": logdata})
        wellbore = Record({
            "kind": "BoreKind",
            "acl": {},
            "legal": {},
            "data": {"FacilityName": "Well name", "NameAliases": [{"AliasName": "Some Name"}]}
        })

        data = DataFrame({})

        mockConfig = Mock(spec=Configuration)
        mockConfig.las_file_mapping = None
        subject = MapWellLogToLas(mockConfig, wellbore, welllog, data)

        # ACT
        result = subject.build_las_file()

        # Assert
        assert result.well.UWI.value == "Some Name"
        assert result.well.WELL.value == "Well name"

        assert len(result.curves) == 0

    def test_build_las_file_empty_log_and_bore(self):
        # Assemble

        welllog = Record({"kind": "LogKind", "acl": {}, "legal": {}, "data": {}})
        wellbore = Record({"kind": "BoreKind", "acl": {}, "legal": {}, "data": {}})
        data = DataFrame({"ABC": [1, 2, 3], "XYZ": [9, 8, 7], "IJK": [-1, -2, -3]})

        mockConfig = Mock(spec=Configuration)
        mockConfig.las_file_mapping = None

        subject = MapWellLogToLas(mockConfig, wellbore, welllog, data)

        # ACT
        result = subject.build_las_file()

        # Assert
        assert result.well.UWI.value is None
        assert result.well.WELL.value is None

        assert len(result.curves) == 3
        assert result.curves[0].mnemonic == "ABC"
        assert result.curves[0].unit is None
        assert (result.curves[0].data == [1, 2, 3]).all()

        assert result.curves[1].mnemonic == "XYZ"
        assert result.curves[1].unit is None
        assert (result.curves[1].data == [9, 8, 7]).all()

        assert result.curves[2].mnemonic == "IJK"
        assert result.curves[2].unit is None
        assert (result.curves[2].data == [-1, -2, -3]).all()
