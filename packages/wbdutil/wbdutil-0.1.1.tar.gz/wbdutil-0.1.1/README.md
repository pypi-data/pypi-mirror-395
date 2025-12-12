# Data Loader Utility for Wellbore DDMS

## Description

1. This will be the OSDU Data loader utility to support Wellbore DDMS.

2. This is a wrapper behind the Wellbore DDMS [API](https://community.opengroup.org/osdu/platform/domain-data-mgmt-services/wellbore/wellbore-domain-services/-/blob/master/spec/generated/openapi.json)

## Install from Package Registry

### Before installation:

-   Ensure Python 3.13 or newer is installed and that Python has been added to the PATH (in your system's environment variables).
-   Confirm you have `pip` installed by running the following command (it should be installed automatically when you installed Python) - `pip --version`
-   If installing `wbdutil` within a virtual environment, first install `pipenv` using the following command - `pip install pipenv`
    -   Note: There is a bug in `pipenv` version 2021.11.23 which will cause the `wbdutil` installation command to fail. Ensure your version number is different to this (e.g. `pip install pipenv=="2021.11.15"` or alternatively a newer version).

### Installation:

The simplest way to install `wbdutil` is from the community package registry.

**Method 1:** To download and install `wbdutil` on your machine run:

```
pip install wbdutil --extra-index-url https://community.opengroup.org/api/v4/projects/801/packages/pypi/simple
```

**Method 2:** Alternatively, you may install the `wbdutil` package within a virtual environment using `pipenv`. If you have `pipenv` installed, simply run:

```
pipenv install wbdutil --extra-index-url https://community.opengroup.org/api/v4/projects/801/packages/pypi/simple --skip-lock
```

## Usage

The `wbdutil` package has a command line interface of the same name `wbdutil` which has the general syntax:

```
wbdutil <group> <command> options
```

Help for any group or command can be obtained by using the `-h` option.

There are several groups:

-   `download`: Download a welllog and curve data to a las format file.
-   `ingest`: Upload a wellbore, welllog and/or bulk data to an OSDU instance
-   `list`: List the data held in OSDU for a given wellbore or welllog id.
-   `parse`: Dry run of the ingest command, instead of uploading data to the OSDU instance it creates json files for the wellbore and welllog.
-   `search`: Search for a wellbore given a well name.
-   `update`: Update the existing bulk data for a given welllog

The `wbdutil` requires configuration information, read from a [configuration file](#config-file).
The path to this file must either be provided in the environment variable `CONFIGPATH` or as a command line option.

All the commands that connect to an OSDU instance (e.g. commands within the `ingest` group) require a bearer token.
This must be provided either in the environment variable `OSDUTOKEN` or as a command line option.

### Environment variables

| Varaible name | overriding command option | Comment                                                    |
| ------------- | ------------------------- | ---------------------------------------------------------- |
| OSDUTOKEN     | `--token` `-t`            | The JWT required to authenticate against an OSDU instance. |
| CONFIGPATH    | `--config_path` `-c`      | The path to the configuration file.                        |

### Config file

The `wbdutil` requires a configuration file that has the following JSON structure:

```
{
    "base_url": "https://osdu-ship.msft-osdu-test.org",
    "data_partition_id": "opendes",
    "legal":
    {
        "legaltags": ["opendes-public-usa-dataset-7643990"],
        "otherRelevantDataCountries": ["US"],
        "status": "compliant"
    },
    "data": {
        "default": {
            "viewers": [ "data.default.viewers@opendes.contoso.com" ],
            "owners": [ "data.default.owners@opendes.contoso.com" ]
        }
    },
    "wellbore_mapping": {},
    "welllog_mapping": {}
}
```

The `base_url` and `data_partition_id` must be correct for the OSDU instance that you want to connect to.
`wellbore_mapping` and `welllog_mapping` are optional features described in the [custom mappings](#custom-mappings) section.

#### Custom mappings

**Custom mappings are an advanced feature of `wbdutil` that require knowledge of both `lasio.LASFile` and OSDU data object schemas and should be used with care.**
The configuration file can be used to define optional custom mappings between `lasio.LASFile` data objects
and OSDU wellbore and welllog objects of a specified kind.
It is recommended that a new mapping is thoroughly tested using the `parse` command group, before upload to OSDU.

There are 3 mapping definitions `wellbore_mapping`, `welllog_mapping` and `las_file_mapping`.
The first 2 (`wellbore_mapping` and `welllog_mapping`) define mappings from LAS format data to OSDU wellbore and welllog objects.
`las_file_mapping` defines the mapping from OSDU well log, well bore and curve data to LAS format data (a `lasio.LASFile` object).

All the mapping definitions must contain a `mapping` attribute, in addition the LAS to OSDU mapping definitions (`wellbore_mapping` and `welllog_mapping`) must contain a `kind` attribute.
If `wellbore_mapping`, `welllog_mapping` and `las_file_mapping` are not defined in the configuration file `wbdutil` will use the default mappings.
The `mapping` attribute describes how data in the incoming object should be transformed into the outgoing data type.
The `kind` attribute defines the target OSDU data type (kind), for example `osdu:wks:work-product-component--WellLog:1.1.0`.
Here is an example mapping for a welllog that could be added to a configuration file.

```
{
    "welllog_mapping": {
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
}
```

The simple data mappings take the form of a key and string value pair.
The key (string to the left of the semi-colon) is the target field within the OSDU data kind and
the value string defines the source of the data. For example:
`"data.ReferenceCurveID": "curves[0].mnemonic"` will set the `data.ReferenceCurveID` field of the output OSDU object
to the value of the `mnemonic` field of the first element in the `curves` array of the input `lasio.LASFile` object.
The `CONFIGURATION` keyword indicates that data should be taken from the configuration file, for example:
`"acl.viewers": "CONFIGURATION.data.default.viewers"` will set the `acl.viewers` field of the output OSDU object
to the value of the `data.default.viewers` field of the configuration. The simple mapping form supports the direct copying of
all objects including arrays from the incoming LAS data to the output OSDU data kind.

There are often more complex transformations that need to be performed on the incoming data,
`wbdutil` supports two types of complex mapping `array` and `function`.
The `function` complex mapping type makes a call to a hard coded function to perform a transformation on the incoming data.
For example:

```
"CurveUnit": {
    "type": "function",
    "function": "las2osdu_curve_uom_converter",
    "args": [
        "unit",
        "CONFIGURATION.data_partition_id"
    ]
}
```

This will set the value of the `CurveUnit` field to the output of the function `las2osdu_curve_uom_converter` using the input arguments in the args array. The `args` section defines the argument for the function, each `arg` is not the direct input argument to the function. An `arg` is a reference to piece of data in the incoming data or configuration file.
In this case `unit` references data in the input data and `data_partition_id` data in the configuration file.

The second complex mapping is `array` this should be used if the elements of an incoming array need to be changed in some way.
This could be a field name change, a change in the object structure or to call a function on specific data within each element.
Here is an example:

```
{
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
```

This mapping will iterate over the `curves` array of the input `lasio.LASFile` object and apply an
inner mapping to each element in the array.
In this case the inner mapping is defined so that the `mnemonic` field of the `curve` element is
mapped to both the `CurveID` and `Mnemonic` output fields, and the `CurveUnit` output field is set
to the return value of the function `las2osdu_curve_uom_converter`
that takes the `unit` field of array element and the `data_partition_id` (from configuration) as arguments.
The resulting output array is mapped to the `data.Curves` field of the output OSDU kind.

Here is an example `las_file_mapping` section:

```
"las_file_mapping": {
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
```

With OSDU to LAS mappings, data is drawn from 3 types of OSDU data object: wellbore, welllog and curves.
Each of these incoming OSDU data can be referenced by the keywords `WELLBORE`, `WELLLOG` and `CURVES`.
Where `WELLBORE` and `WELLLOG` are wellbore and welllog OSDU kinds and `CURVES` is a Pandas DataFrame that
contains the incoming curves data from OSDU.

An example configuration file that is setup for the preship OSDU instance is given in `src/example_opendes_configuration.json`,
it also contains example custom mappings for the `osdu:wks:master-data--Wellbore:1.0.0` wellbore kind and the `osdu:wks:work-product-component--WellLog:1.1.0` welllog kind.

This table summarises the available keywords.

| Keyword         | Valid Mapping type | Incomming data source     |
| --------------- | ------------------ | ------------------------- |
| `CONFIGURATION` | All                | The configuration file    |
| `WELLBORE`      | `las_file_mapping` | The OSDU wellbore object  |
| `WELLLOG`       | `las_file_mapping` | The OSDU welllog object   |
| `CURVES`        | `las_file_mapping` | The OSDU Curves DataFrame |

There are a limited number of mapping functions available these are listed below:

| Function name                                              | Mapping type       | Purpose                                                                                                  |
| ---------------------------------------------------------- | ------------------ | -------------------------------------------------------------------------------------------------------- |
| `build_wellbore_name_aliases(uwi, data_partition_id)`      | `wellbore_mapping` | Constructs a name alias object from the LAS UWI and the data partition id.                               |
| `get_wellbore_id()`                                        | `welllog_mapping`  | Returns the wellbore id from the wellbore that corresponds to the welllog                                |
| `las2osdu_curve_uom_converter(unit, data_partition_id)`    | `welllog_mapping`  | This function converts a LAS format unit of measure to an OSDU format UoM.                               |
| `extract_uwi_from_name_aliases(NameAliases: list)`         | `las_file_mapping` | Return the first name alias or None if none exist                                                        |
| `build_curves_section(wl_curves: list, curves: DataFrame)` | `las_file_mapping` | Iterates over curves, converting units of measure from OSDU to LAS form. Returns the updated curve data. |

These are hard coded functions, so a change request will need to be raised if additional functions are required. We have avoided user defined functions, because such functions represent a small security risk.

## Development
Refer to [System Maintenance Guide](doc/SMG.md) for instructions on setting up a development environment.
