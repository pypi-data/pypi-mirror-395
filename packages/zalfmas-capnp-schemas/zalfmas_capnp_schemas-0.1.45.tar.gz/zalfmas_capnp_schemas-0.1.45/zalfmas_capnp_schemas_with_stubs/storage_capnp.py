"""This is an automatically generated stub for `storage.capnp`."""

import os
import capnp
from typing import NamedTuple

capnp.remove_import_hook()
here = os.path.dirname(os.path.abspath(__file__))
module_file = os.path.abspath(
    os.path.join(here, "../zalfmas_capnp_schemas/storage.capnp")
)
import_path = [here, os.path.abspath(os.path.join(here, "../zalfmas_capnp_schemas"))]
Store = capnp.load(module_file, imports=import_path).Store

Store.Server.ContainerwithidResultTuple = NamedTuple(
    "ContainerwithidResultTuple", [("container", object)]
)
Store.Server.ImportcontainerResultTuple = NamedTuple(
    "ImportcontainerResultTuple", [("container", object)]
)
Store.Server.ListcontainersResultTuple = NamedTuple(
    "ListcontainersResultTuple", [("containers", object)]
)
Store.Server.NewcontainerResultTuple = NamedTuple(
    "NewcontainerResultTuple", [("container", object)]
)
Store.Server.RemovecontainerResultTuple = NamedTuple(
    "RemovecontainerResultTuple", [("success", object)]
)
Store.Container.Server.AddentryResultTuple = NamedTuple(
    "AddentryResultTuple", [("entry", object), ("success", object)]
)
Store.Container.Server.ClearResultTuple = NamedTuple(
    "ClearResultTuple", [("success", object)]
)
Store.Container.Server.DownloadentriesResultTuple = NamedTuple(
    "DownloadentriesResultTuple", [("entries", object)]
)
Store.Container.Server.ExportResultTuple = NamedTuple(
    "ExportResultTuple", [("json", object)]
)
Store.Container.Server.GetentryResultTuple = NamedTuple(
    "GetentryResultTuple", [("entry", object)]
)
Store.Container.Server.ListentriesResultTuple = NamedTuple(
    "ListentriesResultTuple", [("entries", object)]
)
Store.Container.Server.RemoveentryResultTuple = NamedTuple(
    "RemoveentryResultTuple", [("success", object)]
)
Store.Container.Entry.Server.GetkeyResultTuple = NamedTuple(
    "GetkeyResultTuple", [("key", object)]
)
Store.Container.Entry.Server.GetvalueResultTuple = NamedTuple(
    "GetvalueResultTuple", [("value", object), ("isUnset", object)]
)
Store.Container.Entry.Server.SetvalueResultTuple = NamedTuple(
    "SetvalueResultTuple", [("success", object)]
)
