"""This is an automatically generated stub for `service.capnp`."""

import os
import capnp
from typing import NamedTuple

capnp.remove_import_hook()
here = os.path.dirname(os.path.abspath(__file__))
module_file = os.path.abspath(
    os.path.join(here, "../zalfmas_capnp_schemas/service.capnp")
)
import_path = [here, os.path.abspath(os.path.join(here, "../zalfmas_capnp_schemas"))]
Admin = capnp.load(module_file, imports=import_path).Admin
SimpleFactory = capnp.load(module_file, imports=import_path).SimpleFactory
Factory = capnp.load(module_file, imports=import_path).Factory
Stoppable = capnp.load(module_file, imports=import_path).Stoppable

Admin.Server.IdentitiesResultTuple = NamedTuple(
    "IdentitiesResultTuple", [("infos", object)]
)
Factory.Server.CreateResultTuple = NamedTuple(
    "CreateResultTuple",
    [("adminCap", object), ("serviceCaps", object), ("error", object)],
)
Factory.Server.ServiceinterfacenamesResultTuple = NamedTuple(
    "ServiceinterfacenamesResultTuple", [("names", object)]
)
SimpleFactory.Server.CreateResultTuple = NamedTuple(
    "CreateResultTuple", [("caps", object)]
)
Stoppable.Server.StopResultTuple = NamedTuple("StopResultTuple", [("success", object)])
