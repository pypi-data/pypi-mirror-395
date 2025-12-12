"""This is an automatically generated stub for `monica_management.capnp`."""

import os
import capnp
from typing import NamedTuple

capnp.remove_import_hook()
here = os.path.dirname(os.path.abspath(__file__))
module_file = os.path.abspath(
    os.path.join(
        here, "../../../zalfmas_capnp_schemas/model/monica/monica_management.capnp"
    )
)
import_path = [
    here,
    os.path.abspath(os.path.join(here, "../../../zalfmas_capnp_schemas")),
    os.path.abspath(os.path.join(here, "../../../zalfmas_capnp_schemas/model/monica")),
]
ILRDates = capnp.load(module_file, imports=import_path).ILRDates
EventType = capnp.load(module_file, imports=import_path).EventType
PlantOrgan = capnp.load(module_file, imports=import_path).PlantOrgan
Event = capnp.load(module_file, imports=import_path).Event
Params = capnp.load(module_file, imports=import_path).Params
Service = capnp.load(module_file, imports=import_path).Service

Service.Server.ManagementatResultTuple = NamedTuple(
    "ManagementatResultTuple", [("mgmt", object)]
)
