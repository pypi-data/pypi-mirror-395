"""This is an automatically generated stub for `date.capnp`."""

import os
import capnp

capnp.remove_import_hook()
here = os.path.dirname(os.path.abspath(__file__))
module_file = os.path.abspath(os.path.join(here, "../zalfmas_capnp_schemas/date.capnp"))
import_path = [here, os.path.abspath(os.path.join(here, "../zalfmas_capnp_schemas"))]
Date = capnp.load(module_file, imports=import_path).Date
