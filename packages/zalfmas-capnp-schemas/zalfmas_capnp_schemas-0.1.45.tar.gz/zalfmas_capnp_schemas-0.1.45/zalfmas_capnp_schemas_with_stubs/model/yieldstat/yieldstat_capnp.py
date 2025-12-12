"""This is an automatically generated stub for `yieldstat.capnp`."""

import os
import capnp

capnp.remove_import_hook()
here = os.path.dirname(os.path.abspath(__file__))
module_file = os.path.abspath(
    os.path.join(here, "../../../zalfmas_capnp_schemas/model/yieldstat/yieldstat.capnp")
)
import_path = [
    here,
    os.path.abspath(os.path.join(here, "../../../zalfmas_capnp_schemas")),
    os.path.abspath(
        os.path.join(here, "../../../zalfmas_capnp_schemas/model/yieldstat")
    ),
]
ResultId = capnp.load(module_file, imports=import_path).ResultId
RestInput = capnp.load(module_file, imports=import_path).RestInput
Result = capnp.load(module_file, imports=import_path).Result
Output = capnp.load(module_file, imports=import_path).Output
