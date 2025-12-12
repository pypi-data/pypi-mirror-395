"""This is an automatically generated stub for `crop.capnp`."""

import os
import capnp
from typing import NamedTuple

capnp.remove_import_hook()
here = os.path.dirname(os.path.abspath(__file__))
module_file = os.path.abspath(os.path.join(here, "../zalfmas_capnp_schemas/crop.capnp"))
import_path = [here, os.path.abspath(os.path.join(here, "../zalfmas_capnp_schemas"))]
Crop = capnp.load(module_file, imports=import_path).Crop
Service = capnp.load(module_file, imports=import_path).Service

Crop.Server.CultivarResultTuple = NamedTuple("CultivarResultTuple", [("info", object)])
Crop.Server.ParametersResultTuple = NamedTuple(
    "ParametersResultTuple", [("params", object)]
)
Crop.Server.SpeciesResultTuple = NamedTuple("SpeciesResultTuple", [("info", object)])
