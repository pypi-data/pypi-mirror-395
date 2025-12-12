import urllib
from typing import Dict, List

import lasio
from knack.log import get_logger
from lasio.las import LASFile
from lasio.las_items import CurveItem, SectionItems
from pandas.core.frame import DataFrame

from ..common.configuration import Configuration
from .property_mapping import DictionaryMappingLoader, PropertyMapper

logger = get_logger(__name__)


class Record:
    _raw_data: Dict[str, any]

    def __init__(self, data: Dict[str, any]) -> None:
        self._raw_data = data

        if "kind" not in self._raw_data:
            self._raw_data["kind"] = None

        if "acl" not in self._raw_data:
            self._raw_data["acl"] = {}

        if "legal" not in self._raw_data:
            self._raw_data["legal"] = {}

        if "data" not in self._raw_data:
            self._raw_data["data"] = {}

    @property
    def data(self) -> Dict[str, any]:
        return self._raw_data.get("data")

    def get_raw_data(self) -> Dict[str, any]:
        """
        Get the wellbore data used to construct this object
        :returns: The wellbore data
        :rtype: Dict[str, any]
        """
        return self._raw_data


class WellLogRecord(Record):
    def get_curveids(self) -> List[str]:
        """
        Get the curve ids
        :returns: The List of curve ids
        :rtype: List[str]
        """
        curves = self.data['Curves'] if self.data and 'Curves' in self.data else []
        return [c['CurveID'] for c in curves if 'CurveID' in c]


class WellboreMappingFunctions:
    def build_wellbore_name_aliases(self, uwi: str, data_partition_id: str) -> List[Dict[str, str]]:
        """
        Map UWI and the data_partition_id to the wellbore name alias data type.

        :param uwi str: The UWI from the LASFile.
        :param data_partition_id str: The data partition id of the OSDU instance.
        :returns: The 'name aliases' component of a wellbore record's data attribute.
        :rtype: List[Dict[str, str]]
        """

        if uwi is not None and uwi.strip():
            if data_partition_id is None:
                raise ValueError("Please ensure a data partition ID has been provided in the config file.")
            return [
                {
                    "AliasName": uwi,
                    "AliasNameTypeID": f"{data_partition_id}:reference-data--AliasNameType:UniqueIdentifier:",
                }
            ]
        else:
            return []


class WellLogMappingFunctions:
    def __init__(self, wellbore_id: str) -> None:
        self._wellbore_id = f"{wellbore_id}:"

    def get_wellbore_id(self):
        return self._wellbore_id

    def las2osdu_curve_uom_converter(self, unit: str, data_partition_id: str) -> str:
        unit_local = urllib.parse.quote(unit, safe="").replace(" ", "-")
        if unit_local == "":
            unit_local = "UNITLESS"

        return f"{data_partition_id}:reference-data--UnitOfMeasure:{unit_local}:"


class LasToRecordMapper:
    """
    Class for mapping LASFile objects to Wellbore and/or Well Log records.

    :param las LASFile: The LASFile object to map to a Wellbore or Well Log record
    :param configuration Configuration: LAS file metadata object"
    """

    _DEFAULT_WELLBORE_MAPPING = {
        "kind": "osdu:wks:master-data--Wellbore:1.0.0",
        "mapping": {
            "acl.viewers": "CONFIGURATION.data.default.viewers",
            "acl.owners": "CONFIGURATION.data.default.owners",
            "legal.legaltags": "CONFIGURATION.legal.legaltags",
            "legal.otherRelevantDataCountries": "CONFIGURATION.legal.otherRelevantDataCountries",
            "legal.status": "CONFIGURATION.legal.status",
            "data.FacilityName": "well.WELL.value",
            "data.NameAliases": {
                "type": "function",
                "function": "build_wellbore_name_aliases",
                "args": ["well.UWI.value", "CONFIGURATION.data_partition_id"]
            }
        }
    }

    _DEFAULT_WELLLOG_MAPPING = {
        "kind": "osdu:wks:work-product-component--WellLog:1.1.0",
        "mapping":
        {
            "acl.viewers": "CONFIGURATION.data.default.viewers",
            "acl.owners": "CONFIGURATION.data.default.owners",
            "legal.legaltags": "CONFIGURATION.legal.legaltags",
            "legal.otherRelevantDataCountries": "CONFIGURATION.legal.otherRelevantDataCountries",
            "legal.status": "CONFIGURATION.legal.status",
            "data.ReferenceCurveID": "curves[0].mnemonic",
            "data.WellboreID": {
                "type": "function",
                "function": "get_wellbore_id",
                "args": []
            },
            "data.Curves": {
                "type": "array",
                "source": "curves",
                "mapping": {
                    "CurveID": "mnemonic",
                    "Mnemonic": "mnemonic",
                    "CurveUnit": {
                        "type": "function",
                        "function": "las2osdu_curve_uom_converter",
                        "args": [
                            "unit",
                            "CONFIGURATION.data_partition_id"
                        ]
                    }
                }
            }
        }
    }

    las: lasio.LASFile
    config: Configuration

    def __init__(self, las: lasio.LASFile, configuration: Configuration) -> None:
        if not isinstance(las, lasio.LASFile):
            raise TypeError("Please provide a LAS data object as input.")

        self.config = configuration
        self.las = las

    def map_to_wellbore_record(self) -> Record:
        """
        Map the LAS data object to a Wellbore record.

        :returns: A Wellbore record object that can be uploaded to OSDU as JSON payload.
        :rtype: Record
        """
        mapper = PropertyMapper(
            DictionaryMappingLoader(self.config.wellbore_mapping or self._DEFAULT_WELLBORE_MAPPING),
            self.config,
            WellboreMappingFunctions())

        return Record(mapper.remap_data_with_kind(self.las))

    def map_to_well_log_record(self, wellbore_id: str) -> Record:
        """
        Map the LAS data object to a Well Log record.

        :param wellbore_id str: The wellbore_id object, often returned by OSDU.
        :returns: A Well Log record object that can be uploaded to OSDU as JSON payload.
        :rtype: Record
        """

        mapper = PropertyMapper(
            DictionaryMappingLoader(self.config.welllog_mapping or self._DEFAULT_WELLLOG_MAPPING),
            self.config,
            WellLogMappingFunctions(wellbore_id))

        return Record(mapper.remap_data_with_kind(self.las))

    def extract_log_data(self) -> DataFrame:
        """
        Extract the log data and return as a dataframe.

        :returns: A dataframe that contains the Well Log curve data
        :rtype: DataFrame
        """

        return self.las.df().reset_index()


class MapWellLogToLas:
    _DEFAULT_LAS_MAPPING = {
        "mapping": {
            "Well.WELL": "WELLBORE.data.FacilityName",
            "Well.UWI": {
                "type": "function",
                "function": "extract_uwi_from_name_aliases",
                "args": ["WELLBORE.data.NameAliases"]
            },
            "Curves": {
                "type": "function",
                "function": "build_curves_section",
                "args": ["WELLLOG.data.Curves", "CURVES"]
            }
        }
    }

    def __init__(self, configuration: Configuration, wellbore: Record, welllog: Record, data: DataFrame) -> None:
        """
        Construct a new instance of MapWellLogToLas
        :param configuration Configuration: The application configuration
        :param wellbore Record: The wellbore record
        :param welllog Record: The well log record
        :param data DataFrame: The well log curve data
        """
        self._config = configuration
        self._data = {
            "CURVES": data,
            "WELLLOG": welllog,
            "WELLBORE": wellbore
        }

    def build_las_file(self) -> LASFile:
        """
        Build a new instance of LASFile and populate it with data from the welllog
        :returns: A new instance of LASFile.
        :rtype: LASFile
        """

        mapper = PropertyMapper(
            DictionaryMappingLoader(self._config.las_file_mapping or self._DEFAULT_LAS_MAPPING),
            None,
            LasFileMappingFunctions())

        las = lasio.LASFile()
        las.sections = mapper.remap_data(self._data, las.sections)
        return las


class LasFileMappingFunctions:
    def extract_uwi_from_name_aliases(self, name_aliases: list):
        return name_aliases[0].get("AliasName") if name_aliases is not None and len(name_aliases) > 0 else None

    def build_curves_section(self, wl_curves: list, data: DataFrame) -> SectionItems:
        curve_items = []

        for curve in data:
            # Try to get the curve units from the welllog
            if wl_curves is not None:
                wl_curve_matches = [c for c in wl_curves if c.get("CurveID") == curve]
                wl_curve = wl_curve_matches[0] if wl_curve_matches is not None and len(wl_curve_matches) > 0 else {}
                wl_unit = wl_curve.get("CurveUnit")
                las_units = MappingUtilities.convert_osdu_unit_to_raw_unit(wl_unit)
            else:
                las_units = None

            curve_items.append(CurveItem(curve, las_units, "", "", data[curve]))

        return SectionItems(curve_items)


class MappingUtilities:
    @staticmethod
    def convert_osdu_unit_to_raw_unit(osdu_unit: str) -> str:
        """
        Extract and return the unit section from a OSDU qualified unit.
        :param str osdu_unit: The osdu qualified unit
        :return: The unit part or None if the unit cannot be extracted.
        :rtype: str
        """
        if osdu_unit is None:
            return None

        split_units = osdu_unit.split(':')
        if (split_units is None or len(split_units) < 3):
            logger.warning(f"Could not extract units from {osdu_unit}")
            return None

        return urllib.parse.unquote(split_units[2])
