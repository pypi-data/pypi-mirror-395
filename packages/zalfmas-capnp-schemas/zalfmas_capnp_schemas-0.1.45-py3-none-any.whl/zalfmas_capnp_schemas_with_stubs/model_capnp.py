"""This is an automatically generated stub for `model.capnp`."""

import os
import capnp
from typing import NamedTuple

capnp.remove_import_hook()
here = os.path.dirname(os.path.abspath(__file__))
module_file = os.path.abspath(
    os.path.join(here, "../zalfmas_capnp_schemas/model.capnp")
)
import_path = [here, os.path.abspath(os.path.join(here, "../zalfmas_capnp_schemas"))]
XYResult = capnp.load(module_file, imports=import_path).XYResult
Stat = capnp.load(module_file, imports=import_path).Stat
XYPlusResult = capnp.load(module_file, imports=import_path).XYPlusResult
ClimateInstance = capnp.load(module_file, imports=import_path).ClimateInstance
Env = capnp.load(module_file, imports=import_path).Env
EnvInstance = capnp.load(module_file, imports=import_path).EnvInstance
EnvInstanceProxy = capnp.load(module_file, imports=import_path).EnvInstanceProxy
InstanceFactory = capnp.load(module_file, imports=import_path).InstanceFactory

ClimateInstance.Server.RunResultTuple = NamedTuple(
    "RunResultTuple", [("result", object)]
)
ClimateInstance.Server.RunsetResultTuple = NamedTuple(
    "RunsetResultTuple", [("result", object)]
)
EnvInstance.Server.RunResultTuple = NamedTuple("RunResultTuple", [("result", object)])
EnvInstanceProxy.Server.RegisterenvinstanceResultTuple = NamedTuple(
    "RegisterenvinstanceResultTuple", [("unregister", object)]
)
EnvInstanceProxy.Unregister.Server.UnregisterResultTuple = NamedTuple(
    "UnregisterResultTuple", [("success", object)]
)
InstanceFactory.Server.ModelinfoResultTuple = NamedTuple(
    "ModelinfoResultTuple", [("id", object), ("name", object), ("description", object)]
)
InstanceFactory.Server.NewinstanceResultTuple = NamedTuple(
    "NewinstanceResultTuple", [("instance", object)]
)
InstanceFactory.Server.NewinstancesResultTuple = NamedTuple(
    "NewinstancesResultTuple", [("instances", object)]
)
