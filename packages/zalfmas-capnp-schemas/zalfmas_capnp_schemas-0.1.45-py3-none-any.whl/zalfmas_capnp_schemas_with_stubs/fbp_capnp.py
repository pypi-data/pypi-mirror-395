"""This is an automatically generated stub for `fbp.capnp`."""

import os
import capnp
from typing import NamedTuple

capnp.remove_import_hook()
here = os.path.dirname(os.path.abspath(__file__))
module_file = os.path.abspath(os.path.join(here, "../zalfmas_capnp_schemas/fbp.capnp"))
import_path = [here, os.path.abspath(os.path.join(here, "../zalfmas_capnp_schemas"))]
IP = capnp.load(module_file, imports=import_path).IP
IIP = capnp.load(module_file, imports=import_path).IIP
Channel = capnp.load(module_file, imports=import_path).Channel
StartChannelsService = capnp.load(module_file, imports=import_path).StartChannelsService
PortInfos = capnp.load(module_file, imports=import_path).PortInfos
Component = capnp.load(module_file, imports=import_path).Component

Channel.Server.EndpointsResultTuple = NamedTuple(
    "EndpointsResultTuple", [("r", object), ("w", object)]
)
Channel.Server.ReaderResultTuple = NamedTuple("ReaderResultTuple", [("r", object)])
Channel.Server.WriterResultTuple = NamedTuple("WriterResultTuple", [("w", object)])
Channel.Reader.Server.ReadResultTuple = NamedTuple(
    "ReadResultTuple", [("value", object), ("done", object), ("noMsg", object)]
)
Channel.Reader.Server.ReadifmsgResultTuple = NamedTuple(
    "ReadifmsgResultTuple", [("value", object), ("done", object), ("noMsg", object)]
)
Channel.Writer.Server.WriteifspaceResultTuple = NamedTuple(
    "WriteifspaceResultTuple", [("success", object)]
)
Component.RunnableFactory.Server.CreateResultTuple = NamedTuple(
    "CreateResultTuple", [("r", object)]
)
Component.Runnable.Server.StartResultTuple = NamedTuple(
    "StartResultTuple", [("success", object)]
)
Component.Runnable.Server.StopResultTuple = NamedTuple(
    "StopResultTuple", [("success", object)]
)
StartChannelsService.Server.StartResultTuple = NamedTuple(
    "StartResultTuple", [("startupInfos", object), ("stop", object)]
)
