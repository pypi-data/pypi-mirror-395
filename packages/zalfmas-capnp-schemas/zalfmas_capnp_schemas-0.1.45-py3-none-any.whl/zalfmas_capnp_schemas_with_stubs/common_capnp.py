"""This is an automatically generated stub for `common.capnp`."""

import os
import capnp
from typing import NamedTuple

capnp.remove_import_hook()
here = os.path.dirname(os.path.abspath(__file__))
module_file = os.path.abspath(
    os.path.join(here, "../zalfmas_capnp_schemas/common.capnp")
)
import_path = [here, os.path.abspath(os.path.join(here, "../zalfmas_capnp_schemas"))]
IdInformation = capnp.load(module_file, imports=import_path).IdInformation
Identifiable = capnp.load(module_file, imports=import_path).Identifiable
StructuredText = capnp.load(module_file, imports=import_path).StructuredText
Value = capnp.load(module_file, imports=import_path).Value
Pair = capnp.load(module_file, imports=import_path).Pair
Holder = capnp.load(module_file, imports=import_path).Holder
IdentifiableHolder = capnp.load(module_file, imports=import_path).IdentifiableHolder

Holder.Server.ValueResultTuple = NamedTuple("ValueResultTuple", [("value", object)])
Identifiable.Server.InfoResultTuple = NamedTuple(
    "InfoResultTuple", [("id", object), ("name", object), ("description", object)]
)
