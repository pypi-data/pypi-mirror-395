from typing import List
from pandas.core.frame import DataFrame
import pytest
from unittest.mock import Mock, ANY
from importlib import import_module
from . import TARGET_MODULE_NAME

# Test target module import
well_service = import_module(f"{TARGET_MODULE_NAME}.service.well_service")
WellBoreService = well_service.WellBoreService
WellLogService = well_service.WellLogService
DataLoaderConflictError = well_service.DataLoaderConflictError

osdu_client = import_module(f"{TARGET_MODULE_NAME}.wrapper.osdu_client")
DataLoaderWebResponseError = osdu_client.DataLoaderWebResponseError
OsduClient = osdu_client.OsduClient

record_mapper = import_module(f"{TARGET_MODULE_NAME}.service.record_mapper")
LasToRecordMapper = record_mapper.LasToRecordMapper
Record = record_mapper.Record
WellLogRecord = record_mapper.WellLogRecord

Configuration = import_module(f"{TARGET_MODULE_NAME}.common.configuration").Configuration


class TestWellLogService:

    def test_recognize_log_family(self):
        # Assemble
        client = Mock(spec=OsduClient)
        client.post_log_recognition.return_value = {"family": "family_id"}

        subject = WellLogService(client)

        record = Record({"data": {"Curves": [{"Mnemonic": "Mnemonic1", "NumberOfColumns": 1, "CurveUnit": "::cvunit1:"}]}})

        # Act
        result = subject.recognize_log_family(record, "dp_id")

        # Assert
        client.post_log_recognition.assert_called_with("Mnemonic1", "cvunit1")

        assert result.data["Curves"] == [{'CurveUnit': '::cvunit1:',
                                          'LogCurveFamilyID': 'dp_id:reference-data--LogCurveFamily:family_id:',
                                          "NumberOfColumns": 1,
                                          'Mnemonic': 'Mnemonic1'}]

    recognize_parameters = [
        ([], []),
        ([{"Mnemonic": "Mnemonic1",  "NumberOfColumns": 1, "CurveUnit": "::cvunit1:"}],
         [{'CurveUnit': '::cvunit1:', 'LogCurveFamilyID': 'dp_id:reference-data--LogCurveFamily:family_id:',
           "NumberOfColumns": 1, 'Mnemonic': 'Mnemonic1'}]),
        ([{"Mnemonic": "Mnemonic1", "NumberOfColumns": 1, "CurveUnit": "::cvunit1:"},
          {"Mnemonic": "Mnemonic2", "NumberOfColumns": 1, "CurveUnit": "::cvunit2:"}],
         [{'CurveUnit': '::cvunit1:', "NumberOfColumns": 1,
           'LogCurveFamilyID': 'dp_id:reference-data--LogCurveFamily:family_id:', 'Mnemonic': 'Mnemonic1'},
          {'CurveUnit': '::cvunit2:', "NumberOfColumns": 1,
           'LogCurveFamilyID': 'dp_id:reference-data--LogCurveFamily:family_id:', 'Mnemonic': 'Mnemonic2'}])
    ]

    @pytest.mark.parametrize("curves,expected", recognize_parameters)
    def test_recognize_curves_family(self, curves, expected):
        # Assemble
        client = Mock(spec=OsduClient)
        client.post_log_recognition.return_value = {"family": "family_id"}

        subject = WellLogService(client)

        # Act
        result = subject.recognize_curves_family(curves, "dp_id")

        # Assert
        if len(curves) > 0:
            client.post_log_recognition.assert_called_with(ANY, ANY)

        assert result == expected

    def test_recognize_curve_family_osdu_raises(self):
        # Assemble
        client = Mock(spec=OsduClient)

        client.post_log_recognition.side_effect = DataLoaderWebResponseError('POST', "URL", "BOOM!")
        subject = WellLogService(client)

        # Act
        result = subject.recognize_curve_family("mnemonic", "unit", "dp_id")

        # Assert
        client.post_log_recognition.assert_called_once_with("mnemonic", "unit")
        assert result is None

    recognize_parameters = [("mne", "unit1", "anid", {"family": "family_id"}, "anid:reference-data--LogCurveFamily:family_id:"),
                            ("mne", "unit1", "anid", {"family": "family id"}, "anid:reference-data--LogCurveFamily:family-id:"),
                            ("mne", "unit1", "anid", {"family": "family,id"}, "anid:reference-data--LogCurveFamily:family%2Cid:"),
                            ("mne", "unit1", "anid", {"notFamily": "family,id"}, None),
                            ("mne", "unit1", "anid", None, None),
                            ("mne", "unit1", "anid", {"family": None}, None)]

    @pytest.mark.parametrize("mnemonic, unit, dp_id, osdu_response, expected", recognize_parameters)
    def test_recognize_curve_family(self, mnemonic, unit, dp_id, osdu_response, expected):
        # Assemble
        client = Mock(spec=OsduClient)

        client.post_log_recognition.return_value = osdu_response
        subject = WellLogService(client)

        # Act
        result = subject.recognize_curve_family(mnemonic, unit, dp_id)

        # Assert
        client.post_log_recognition.assert_called_once_with(mnemonic, unit)
        assert result == expected

    def test_update_log_family(self):
        # Arrange
        welllog_id = "WL-ID-123"
        data_partition_id = "dp-123"

        curves = [
            {"Mnemonic": "DEPT", "CurveUnit": "::Unit1"},
            {"Mnemonic": "BWV", "CurveUnit": "::Unit2"},
            {"Mnemonic": "DT", "CurveUnit": "::Unit3"}
        ]
        welllog_record = WellLogRecord({
            "kind": "a kind",
            "data": {
                "ReferenceCurveID": "DEPT",
                "Curves": curves,
                "WellboreID": "WB-ID-123",
            },
            "id": welllog_id
        })

        family_id_prefix = "dp-123:reference-data--LogCurveFamily"
        enriched_curves = [
            {"Mnemonic": "DEPT", "CurveUnit": "::Unit1", "LogCurveFamilyID": f"{family_id_prefix}:Fam-ID-1:", "NumberOfColumns": 1},
            {"Mnemonic": "BWV", "CurveUnit": "::Unit2", "LogCurveFamilyID": f"{family_id_prefix}:Fam-ID-1:", "NumberOfColumns": 1},
            {"Mnemonic": "DT", "CurveUnit": "::Unit3", "LogCurveFamilyID": f"{family_id_prefix}:Fam-ID-1:", "NumberOfColumns": 1}
        ]
        enriched_welllog_record = WellLogRecord({
            "kind": "a kind",
            "data": {
                "ReferenceCurveID": "DEPT",
                "Curves": enriched_curves,
                "WellboreID": "WB-ID-123",
            },
            "id": welllog_id
        })

        client = Mock(spec=OsduClient)
        client.get_welllog_record.return_value = welllog_record
        client.post_log_recognition.return_value = {"family": "Fam ID 1"}
        client.post_welllog.return_value = [welllog_id]

        subject = WellLogService(client)

        # Act
        subject.update_log_family(welllog_id, data_partition_id)

        # Assert
        assert client.get_welllog_record.call_count == 2
        client.get_welllog_record.assert_called_with(welllog_id)
        assert client.post_log_recognition.call_count == 3
        client.post_log_recognition.assert_called_with("DT", "Unit3")

        calls = client.post_welllog.call_args_list
        assert len(calls) == 1
        assert calls[0][0][0].get_raw_data() == enriched_welllog_record.get_raw_data()

    def test_get_data_ingest_validation_variables(self):
        # Assemble
        client = Mock(spec=OsduClient)
        subject = WellLogService(client)

        welllog_record = WellLogRecord({
            "kind": "a kind",
            "data": {
                "ReferenceCurveID": "DEPT",
                "Curves": [{"CurveID": "DEPT"}, {"CurveID": "BWV"}, {"CurveID": "DT"}],
                "WellboreID": "WB-ID123",
            }
        })

        wellbore_record = Record({
            "kind": "some kind",
            "data": {
                "FacilityName": "Well-ABC",
                "NameAliases": []
            }
        })

        client.get_welllog_record.return_value = welllog_record
        client.get_wellbore_record.return_value = wellbore_record

        # Act
        welllog_well_name, welllog_curve_ids = subject._get_data_ingest_validation_variables(welllog_id="WL-ID123")
        assert welllog_well_name == "Well-ABC"
        assert welllog_curve_ids == ["DEPT", "BWV", "DT"]

    def test_download_and_construct_las(self):
        logdata = {
            "WellboreID": "well bore Id",
            "Curves": [
                {"CurveID": "ABC", "CurveUnit": "opendes:reference-data--UnitOfMeasure:M:"},
                {"CurveID": "LMN", "CurveUnit": "opendes:reference-data--UnitOfMeasure:Ft:"},
                {"CurveID": "XYZ", "CurveUnit": "opendes:reference-data--UnitOfMeasure:GAPI:"}]
        }

        welllog = Record({"kind": "LogKind", "data": logdata})
        wellbore = Record({"data": {"FacilityName": "Well name", "NameAliases": [{"AliasName": "Some Name"}]}})
        data = DataFrame({"ABC": [1, 2, 3], "XYZ": [9, 8, 7], "IJK": [-1, -2, -3]})

        client = Mock(spec=OsduClient)

        client.get_welllog_record.return_value = welllog
        client.get_wellbore_record.return_value = wellbore
        client.get_welllog_data.return_value = data
        subject = WellLogService(client)

        arg_welllog_id = "wellog_id argument"
        arg_curves = ["ABC", "XYZ"]

        mockConfig = Mock(spec=Configuration)
        mockConfig.las_file_mapping = None

        # Act
        result = subject.download_and_construct_las(mockConfig, arg_welllog_id, arg_curves)

        # Assert
        client.get_welllog_record.assert_called_once_with(arg_welllog_id)
        client.get_wellbore_record.assert_called_once_with("well bore Id")
        client.get_welllog_data.assert_called_once_with(arg_welllog_id, arg_curves)

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

    def test_download_and_construct_las_no_wellbore(self):
        logdata = {
            "WellboreID": None,
            "Curves": [
                {"CurveID": "ABC", "CurveUnit": "opendes:reference-data--UnitOfMeasure:M:"},
                {"CurveID": "LMN", "CurveUnit": "opendes:reference-data--UnitOfMeasure:Ft:"},
                {"CurveID": "XYZ", "CurveUnit": "opendes:reference-data--UnitOfMeasure:GAPI:"}]
        }

        welllog = Record({"kind": "LogKind", "acl": {}, "legal": {}, "data": logdata})
        data = DataFrame({"ABC": [1, 2, 3], "XYZ": [9, 8, 7], "IJK": [-1, -2, -3]})

        client = Mock(spec=OsduClient)

        client.get_welllog_record.return_value = welllog
        client.get_welllog_data.return_value = data
        subject = WellLogService(client)

        arg_welllog_id = "wellog_id argument"
        arg_curves = ["ABC", "XYZ"]

        mockConfig = Mock(spec=Configuration)
        mockConfig.las_file_mapping = None

        # Act
        result = subject.download_and_construct_las(mockConfig, arg_welllog_id, arg_curves)

        # Assert
        client.get_welllog_record.assert_called_once_with(arg_welllog_id)
        client.get_wellbore_record.assert_not_called()
        client.get_welllog_data.assert_called_once_with(arg_welllog_id, arg_curves)

        assert result.well.UWI.value is None
        assert result.well.WELL.value is None

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


class TestWellBoreService:
    @pytest.mark.parametrize("no_recognize,existing_wellbore_ids", [(True, None), (False, None), (True, ["well_bore_id"])])
    def test_file_ingest(self, no_recognize: bool, existing_wellbore_ids: List[str]):
        # Assemble
        mock_client = Mock(spec=OsduClient)
        mock_well_log_service = Mock(spec=WellLogService)
        mock_mapper = Mock(spec=LasToRecordMapper)

        well_bore_record = Record({"Kind": "well_bore_kind", "acl": {}, "legal": {}, "data": {"FacilityName": "WellBoreName"}})
        well_log_record = Record({"kind": "well_log_kind", "acl": {}, "legal": {}, "data": {}})
        well_log_record_recognized = Record({"kind": "well_log_rec_kind", "acl": {"blah": "blah"}, "legal": {}, "data": {}})
        well_log_record_returned = WellLogRecord({"kind": "returned_welllog_record"})
        well_log_data = DataFrame({"SomeData": ["some data value", "some data value 2"]})
        data_partition_id = "dp_id"

        well_bore_ids = ["well_bore_id"]
        well_log_ids = ["well_log_id"]

        mock_mapper.map_to_wellbore_record.return_value = well_bore_record
        mock_mapper.map_to_well_log_record.return_value = well_log_record
        mock_mapper.extract_log_data.return_value = well_log_data

        mock_client.search_for_wellbore.return_value = existing_wellbore_ids
        mock_client.create_wellbore.return_value = well_bore_ids
        mock_client.get_wellbore_record.return_value = well_bore_record
        mock_client.post_welllog.return_value = well_log_ids
        mock_client.get_welllog_record.return_value = well_log_record_returned

        mock_well_log_service.recognize_log_family.return_value = well_log_record_recognized

        subject = WellBoreService(mock_client, mock_well_log_service)

        # Act
        subject.file_ingest(mock_mapper, data_partition_id, no_recognize)

        # Assert

        mock_client.search_for_wellbore.assert_called_once_with("WellBoreName")
        mock_mapper.map_to_wellbore_record.assert_called_once()

        if existing_wellbore_ids is None:
            mock_client.create_wellbore.assert_called_once_with(well_bore_record)
        else:
            mock_client.create_wellbore.assert_not_called()

        mock_client.get_wellbore_record.assert_called_once_with(well_bore_ids[0])
        mock_mapper.map_to_well_log_record.assert_called_once_with(well_bore_ids[0])

        if no_recognize:
            mock_well_log_service.recognize_log_family.assert_not_called()

            assert not mock_well_log_service.recognize_log_family.called
            mock_client.post_welllog.assert_called_once_with(well_log_record)
        else:
            mock_well_log_service.recognize_log_family.assert_called_once_with(well_log_record, data_partition_id)
            mock_client.post_welllog.assert_called_once_with(well_log_record_recognized)

        mock_client.get_welllog_record.assert_called_once_with(well_log_ids[0])
        mock_mapper.extract_log_data.assert_called_once()
        mock_client.add_welllog_data.assert_called_once_with(well_log_data, well_log_ids[0])

    def test_file_ingest_raises_on_well_bore_conflict(self):
        # Assemble
        mock_client = Mock(spec=OsduClient)
        mock_well_log_service = Mock(spec=WellLogService)
        mock_mapper = Mock(spec=LasToRecordMapper)

        well_bore_record = Record({"Kind": "well_bore_kind", "acl": {}, "legal": {}, "data": {"FacilityName": "WellBoreName"}})
        data_partition_id = "dp_id"

        mock_mapper.map_to_wellbore_record.return_value = well_bore_record
        mock_client.search_for_wellbore.return_value = ["id1", "id2"]
        subject = WellBoreService(mock_client, mock_well_log_service)

        # Act
        with pytest.raises(DataLoaderConflictError):
            subject.file_ingest(mock_mapper, data_partition_id, False)

        # Assert
        mock_client.search_for_wellbore.assert_called_once_with("WellBoreName")
        mock_mapper.map_to_wellbore_record.assert_called_once()

        mock_client.create_wellbore.assert_not_called()
        mock_client.post_welllog.assert_not_called()
        mock_client.add_welllog_data.assert_not_called()

    def test_get_wellbore_by_name_raises_on_conflict(self):
        # Assemble
        mock_client = Mock(spec=OsduClient)
        mock_well_log_service = Mock(spec=WellLogService)

        mock_client.search_for_wellbore.return_value = ["id1", "id2"]
        subject = WellBoreService(mock_client, mock_well_log_service)

        # Act
        with pytest.raises(DataLoaderConflictError):
            subject._get_wellbore_by_name("WellBoreName")

        # Assert
        mock_client.search_for_wellbore.assert_called_once_with("WellBoreName")

    @pytest.mark.parametrize("existing_wellbore_ids,wellbore_name",
                             [(None, "WellBoreName"), (["well_bore_id"], "WellBoreName"), (None, None)])
    def test_get_wellbore_by_name(self, existing_wellbore_ids, wellbore_name):
        # Assemble
        mock_client = Mock(spec=OsduClient)
        mock_well_log_service = Mock(spec=WellLogService)

        mock_client.search_for_wellbore.return_value = existing_wellbore_ids
        subject = WellBoreService(mock_client, mock_well_log_service)

        # Act
        result = subject._get_wellbore_by_name(wellbore_name)

        # Assert
        if wellbore_name is None:
            mock_client.search_for_wellbore.assert_not_called()
        else:
            mock_client.search_for_wellbore.assert_called_once_with(wellbore_name)

        if existing_wellbore_ids is None or wellbore_name is None:
            assert result is None
        else:
            assert result == existing_wellbore_ids[0]
