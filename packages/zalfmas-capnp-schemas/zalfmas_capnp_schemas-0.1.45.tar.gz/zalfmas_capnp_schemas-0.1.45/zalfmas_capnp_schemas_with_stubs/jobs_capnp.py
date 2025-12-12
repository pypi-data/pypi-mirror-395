"""This is an automatically generated stub for `jobs.capnp`."""

import os
import capnp
from typing import NamedTuple

capnp.remove_import_hook()
here = os.path.dirname(os.path.abspath(__file__))
module_file = os.path.abspath(os.path.join(here, "../zalfmas_capnp_schemas/jobs.capnp"))
import_path = [here, os.path.abspath(os.path.join(here, "../zalfmas_capnp_schemas"))]
Job = capnp.load(module_file, imports=import_path).Job
Service = capnp.load(module_file, imports=import_path).Service

Service.Server.NextjobResultTuple = NamedTuple("NextjobResultTuple", [("job", object)])
