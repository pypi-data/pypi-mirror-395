"""This is an automatically generated stub for `persistence.capnp`."""

import os
import capnp
from typing import NamedTuple

capnp.remove_import_hook()
here = os.path.dirname(os.path.abspath(__file__))
module_file = os.path.abspath(
    os.path.join(here, "../zalfmas_capnp_schemas/persistence.capnp")
)
import_path = [here, os.path.abspath(os.path.join(here, "../zalfmas_capnp_schemas"))]
VatId = capnp.load(module_file, imports=import_path).VatId
Address = capnp.load(module_file, imports=import_path).Address
VatPath = capnp.load(module_file, imports=import_path).VatPath
SturdyRef = capnp.load(module_file, imports=import_path).SturdyRef
Heartbeat = capnp.load(module_file, imports=import_path).Heartbeat
Persistent = capnp.load(module_file, imports=import_path).Persistent
Restorer = capnp.load(module_file, imports=import_path).Restorer
HostPortResolver = capnp.load(module_file, imports=import_path).HostPortResolver
Gateway = capnp.load(module_file, imports=import_path).Gateway

Gateway.Server.RegisterResultTuple = NamedTuple(
    "RegisterResultTuple",
    [("sturdyRef", object), ("heartbeat", object), ("secsHeartbeatInterval", object)],
)
HostPortResolver.Server.ResolveResultTuple = NamedTuple(
    "ResolveResultTuple", [("host", object), ("port", object)]
)
HostPortResolver.Registrar.Server.RegisterResultTuple = NamedTuple(
    "RegisterResultTuple", [("heartbeat", object), ("secsHeartbeatInterval", object)]
)
Persistent.Server.SaveResultTuple = NamedTuple(
    "SaveResultTuple", [("sturdyRef", object), ("unsaveSR", object)]
)
Persistent.ReleaseSturdyRef.Server.ReleaseResultTuple = NamedTuple(
    "ReleaseResultTuple", [("success", object)]
)
Restorer.Server.RestoreResultTuple = NamedTuple("RestoreResultTuple", [("cap", object)])
