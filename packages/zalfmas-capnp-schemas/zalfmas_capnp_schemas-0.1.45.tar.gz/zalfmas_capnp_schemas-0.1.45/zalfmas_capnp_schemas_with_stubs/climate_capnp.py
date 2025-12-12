"""This is an automatically generated stub for `climate.capnp`."""

import os
import capnp
from typing import NamedTuple

capnp.remove_import_hook()
here = os.path.dirname(os.path.abspath(__file__))
module_file = os.path.abspath(
    os.path.join(here, "../zalfmas_capnp_schemas/climate.capnp")
)
import_path = [here, os.path.abspath(os.path.join(here, "../zalfmas_capnp_schemas"))]
GCM = capnp.load(module_file, imports=import_path).GCM
RCM = capnp.load(module_file, imports=import_path).RCM
SSP = capnp.load(module_file, imports=import_path).SSP
RCP = capnp.load(module_file, imports=import_path).RCP
EnsembleMember = capnp.load(module_file, imports=import_path).EnsembleMember
Metadata = capnp.load(module_file, imports=import_path).Metadata
Dataset = capnp.load(module_file, imports=import_path).Dataset
Location = capnp.load(module_file, imports=import_path).Location
TimeSeries = capnp.load(module_file, imports=import_path).TimeSeries
Element = capnp.load(module_file, imports=import_path).Element
MetaPlusData = capnp.load(module_file, imports=import_path).MetaPlusData
TimeSeriesData = capnp.load(module_file, imports=import_path).TimeSeriesData
Service = capnp.load(module_file, imports=import_path).Service
CSVTimeSeriesFactory = capnp.load(module_file, imports=import_path).CSVTimeSeriesFactory
AlterTimeSeriesWrapper = capnp.load(
    module_file, imports=import_path
).AlterTimeSeriesWrapper
AlterTimeSeriesWrapperFactory = capnp.load(
    module_file, imports=import_path
).AlterTimeSeriesWrapperFactory

AlterTimeSeriesWrapperFactory.Server.WrapResultTuple = NamedTuple(
    "WrapResultTuple", [("wrapper", object)]
)
AlterTimeSeriesWrapper.Server.AlterResultTuple = NamedTuple(
    "AlterResultTuple", [("timeSeries", object)]
)
AlterTimeSeriesWrapper.Server.AlteredelementsResultTuple = NamedTuple(
    "AlteredelementsResultTuple", [("list", object)]
)
AlterTimeSeriesWrapper.Server.WrappedtimeseriesResultTuple = NamedTuple(
    "WrappedtimeseriesResultTuple", [("timeSeries", object)]
)
CSVTimeSeriesFactory.Server.CreateResultTuple = NamedTuple(
    "CreateResultTuple", [("timeseries", object), ("error", object)]
)
Dataset.Server.ClosesttimeseriesatResultTuple = NamedTuple(
    "ClosesttimeseriesatResultTuple", [("timeSeries", object)]
)
Dataset.Server.LocationsResultTuple = NamedTuple(
    "LocationsResultTuple", [("locations", object)]
)
Dataset.Server.MetadataResultTuple = NamedTuple(
    "MetadataResultTuple", [("entries", object), ("info", object)]
)
Dataset.Server.StreamlocationsResultTuple = NamedTuple(
    "StreamlocationsResultTuple", [("locationsCallback", object)]
)
Dataset.Server.TimeseriesatResultTuple = NamedTuple(
    "TimeseriesatResultTuple", [("timeSeries", object)]
)
Dataset.GetLocationsCallback.Server.NextlocationsResultTuple = NamedTuple(
    "NextlocationsResultTuple", [("locations", object)]
)
Metadata.Information.Server.ForallResultTuple = NamedTuple(
    "ForallResultTuple", [("all", object)]
)
Metadata.Information.Server.ForoneResultTuple = NamedTuple(
    "ForoneResultTuple", [("id", object), ("name", object), ("description", object)]
)
Metadata.Supported.Server.CategoriesResultTuple = NamedTuple(
    "CategoriesResultTuple", [("types", object)]
)
Metadata.Supported.Server.SupportedvaluesResultTuple = NamedTuple(
    "SupportedvaluesResultTuple", [("values", object)]
)
Service.Server.GetavailabledatasetsResultTuple = NamedTuple(
    "GetavailabledatasetsResultTuple", [("datasets", object)]
)
Service.Server.GetdatasetsforResultTuple = NamedTuple(
    "GetdatasetsforResultTuple", [("datasets", object)]
)
TimeSeries.Server.DataResultTuple = NamedTuple("DataResultTuple", [("data", object)])
TimeSeries.Server.DatatResultTuple = NamedTuple("DatatResultTuple", [("data", object)])
TimeSeries.Server.HeaderResultTuple = NamedTuple(
    "HeaderResultTuple", [("header", object)]
)
TimeSeries.Server.LocationResultTuple = NamedTuple(
    "LocationResultTuple",
    [
        ("id", object),
        ("heightNN", object),
        ("latlon", object),
        ("timeSeries", object),
        ("customData", object),
    ],
)
TimeSeries.Server.MetadataResultTuple = NamedTuple(
    "MetadataResultTuple", [("entries", object), ("info", object)]
)
TimeSeries.Server.RangeResultTuple = NamedTuple(
    "RangeResultTuple", [("startDate", object), ("endDate", object)]
)
TimeSeries.Server.ResolutionResultTuple = NamedTuple(
    "ResolutionResultTuple", [("resolution", object)]
)
TimeSeries.Server.SubheaderResultTuple = NamedTuple(
    "SubheaderResultTuple", [("timeSeries", object)]
)
TimeSeries.Server.SubrangeResultTuple = NamedTuple(
    "SubrangeResultTuple", [("timeSeries", object)]
)
