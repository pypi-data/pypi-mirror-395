"""This is an automatically generated stub for `persistent.capnp`."""

import os
import capnp
from typing import NamedTuple

capnp.remove_import_hook()
here = os.path.dirname(os.path.abspath(__file__))
module_file = os.path.abspath(
    os.path.join(here, "../../zalfmas_capnp_schemas/capnp/persistent.capnp")
)
import_path = [
    here,
    os.path.abspath(os.path.join(here, "../../zalfmas_capnp_schemas")),
    os.path.abspath(os.path.join(here, "../../zalfmas_capnp_schemas/capnp")),
]
Persistent = capnp.load(module_file, imports=import_path).Persistent

Persistent.Server.SaveResultTuple = NamedTuple(
    "SaveResultTuple", [("sturdyRef", object)]
)
