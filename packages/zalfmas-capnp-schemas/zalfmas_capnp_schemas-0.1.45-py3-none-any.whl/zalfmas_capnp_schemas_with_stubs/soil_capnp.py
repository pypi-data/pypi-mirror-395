"""This is an automatically generated stub for `soil.capnp`."""

import os
import capnp
from typing import NamedTuple

capnp.remove_import_hook()
here = os.path.dirname(os.path.abspath(__file__))
module_file = os.path.abspath(os.path.join(here, "../zalfmas_capnp_schemas/soil.capnp"))
import_path = [here, os.path.abspath(os.path.join(here, "../zalfmas_capnp_schemas"))]
SType = capnp.load(module_file, imports=import_path).SType
PropertyName = capnp.load(module_file, imports=import_path).PropertyName
Layer = capnp.load(module_file, imports=import_path).Layer
Query = capnp.load(module_file, imports=import_path).Query
ProfileData = capnp.load(module_file, imports=import_path).ProfileData
Profile = capnp.load(module_file, imports=import_path).Profile
Service = capnp.load(module_file, imports=import_path).Service

Profile.Server.DataResultTuple = NamedTuple(
    "DataResultTuple", [("layers", object), ("percentageOfArea", object)]
)
Profile.Server.GeolocationResultTuple = NamedTuple(
    "GeolocationResultTuple", [("lat", object), ("lon", object)]
)
Service.Server.CheckavailableparametersResultTuple = NamedTuple(
    "CheckavailableparametersResultTuple",
    [("failed", object), ("mandatory", object), ("optional", object)],
)
Service.Server.ClosestprofilesatResultTuple = NamedTuple(
    "ClosestprofilesatResultTuple", [("profiles", object)]
)
Service.Server.GetallavailableparametersResultTuple = NamedTuple(
    "GetallavailableparametersResultTuple",
    [("mandatory", object), ("optional", object)],
)
Service.Server.StreamallprofilesResultTuple = NamedTuple(
    "StreamallprofilesResultTuple", [("allProfiles", object)]
)
Service.Stream.Server.NextprofilesResultTuple = NamedTuple(
    "NextprofilesResultTuple", [("profiles", object)]
)
