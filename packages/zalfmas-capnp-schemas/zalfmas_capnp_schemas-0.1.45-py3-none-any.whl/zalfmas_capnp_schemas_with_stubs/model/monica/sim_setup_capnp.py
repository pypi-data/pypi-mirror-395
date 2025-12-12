"""This is an automatically generated stub for `sim_setup.capnp`."""

import os
import capnp

capnp.remove_import_hook()
here = os.path.dirname(os.path.abspath(__file__))
module_file = os.path.abspath(
    os.path.join(here, "../../../zalfmas_capnp_schemas/model/monica/sim_setup.capnp")
)
import_path = [
    here,
    os.path.abspath(os.path.join(here, "../../../zalfmas_capnp_schemas")),
    os.path.abspath(os.path.join(here, "../../../zalfmas_capnp_schemas/model/monica")),
]
Setup = capnp.load(module_file, imports=import_path).Setup
