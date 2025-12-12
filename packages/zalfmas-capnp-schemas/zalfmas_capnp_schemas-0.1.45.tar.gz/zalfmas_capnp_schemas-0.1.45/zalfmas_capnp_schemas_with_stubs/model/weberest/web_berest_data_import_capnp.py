"""This is an automatically generated stub for `web-berest-data-import.capnp`."""

import os
import capnp
from typing import NamedTuple

capnp.remove_import_hook()
here = os.path.dirname(os.path.abspath(__file__))
module_file = os.path.abspath(
    os.path.join(
        here,
        "../../../zalfmas_capnp_schemas/model/weberest/web-berest-data-import.capnp",
    )
)
import_path = [
    here,
    os.path.abspath(os.path.join(here, "../../../zalfmas_capnp_schemas")),
    os.path.abspath(
        os.path.join(here, "../../../zalfmas_capnp_schemas/model/weberest")
    ),
]
DWLABImport = capnp.load(module_file, imports=import_path).DWLABImport

DWLABImport.Server.ImportdataResultTuple = NamedTuple(
    "ImportdataResultTuple",
    [("id", object), ("successA", object), ("successB", object)],
)
