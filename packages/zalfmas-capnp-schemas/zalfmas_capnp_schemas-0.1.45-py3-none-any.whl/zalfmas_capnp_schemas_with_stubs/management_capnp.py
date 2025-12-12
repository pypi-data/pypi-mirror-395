"""This is an automatically generated stub for `management.capnp`."""

import os
import capnp
from typing import NamedTuple

capnp.remove_import_hook()
here = os.path.dirname(os.path.abspath(__file__))
module_file = os.path.abspath(
    os.path.join(here, "../zalfmas_capnp_schemas/management.capnp")
)
import_path = [here, os.path.abspath(os.path.join(here, "../zalfmas_capnp_schemas"))]
EventType = capnp.load(module_file, imports=import_path).EventType
PlantOrgan = capnp.load(module_file, imports=import_path).PlantOrgan
Event = capnp.load(module_file, imports=import_path).Event
Params = capnp.load(module_file, imports=import_path).Params
Fertilizer = capnp.load(module_file, imports=import_path).Fertilizer
Nutrient = capnp.load(module_file, imports=import_path).Nutrient
FertilizerService = capnp.load(module_file, imports=import_path).FertilizerService
Service = capnp.load(module_file, imports=import_path).Service

Fertilizer.Server.NutrientsResultTuple = NamedTuple(
    "NutrientsResultTuple", [("nutrients", object)]
)
Fertilizer.Server.ParametersResultTuple = NamedTuple(
    "ParametersResultTuple", [("params", object)]
)
Service.Server.ManagementatResultTuple = NamedTuple(
    "ManagementatResultTuple", [("mgmt", object)]
)
