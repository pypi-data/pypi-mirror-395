"""This is an automatically generated stub for `grid.capnp`."""

import os
import capnp
from typing import NamedTuple

capnp.remove_import_hook()
here = os.path.dirname(os.path.abspath(__file__))
module_file = os.path.abspath(os.path.join(here, "../zalfmas_capnp_schemas/grid.capnp"))
import_path = [here, os.path.abspath(os.path.join(here, "../zalfmas_capnp_schemas"))]
Aggregation = capnp.load(module_file, imports=import_path).Aggregation
Grid = capnp.load(module_file, imports=import_path).Grid

Grid.Server.ClosestvalueatResultTuple = NamedTuple(
    "ClosestvalueatResultTuple",
    [("val", object), ("tl", object), ("br", object), ("aggParts", object)],
)
Grid.Server.DimensionResultTuple = NamedTuple(
    "DimensionResultTuple", [("rows", object), ("cols", object)]
)
Grid.Server.LatlonboundsResultTuple = NamedTuple(
    "LatlonboundsResultTuple",
    [("tl", object), ("tr", object), ("br", object), ("bl", object)],
)
Grid.Server.NodatavalueResultTuple = NamedTuple(
    "NodatavalueResultTuple", [("nodata", object)]
)
Grid.Server.ResolutionResultTuple = NamedTuple(
    "ResolutionResultTuple", [("res", object)]
)
Grid.Server.StreamcellsResultTuple = NamedTuple(
    "StreamcellsResultTuple", [("callback", object)]
)
Grid.Server.UnitResultTuple = NamedTuple("UnitResultTuple", [("unit", object)])
Grid.Server.ValueatResultTuple = NamedTuple(
    "ValueatResultTuple", [("val", object), ("aggParts", object)]
)
Grid.Callback.Server.SendcellsResultTuple = NamedTuple(
    "SendcellsResultTuple", [("locations", object)]
)
