"""This is an automatically generated stub for `cluster_admin_service.capnp`."""

import os
import capnp
from typing import NamedTuple

capnp.remove_import_hook()
here = os.path.dirname(os.path.abspath(__file__))
module_file = os.path.abspath(
    os.path.join(here, "../zalfmas_capnp_schemas/cluster_admin_service.capnp")
)
import_path = [here, os.path.abspath(os.path.join(here, "../zalfmas_capnp_schemas"))]
Cluster = capnp.load(module_file, imports=import_path).Cluster

Cluster.AdminMaster.Server.AvailablemodelsResultTuple = NamedTuple(
    "AvailablemodelsResultTuple", [("factories", object)]
)
Cluster.AdminMaster.Server.RegistermodelinstancefactoryResultTuple = NamedTuple(
    "RegistermodelinstancefactoryResultTuple", [("unregister", object)]
)
Cluster.ModelInstanceFactory.Server.ModelidResultTuple = NamedTuple(
    "ModelidResultTuple", [("id", object)]
)
Cluster.ModelInstanceFactory.Server.NewcloudviaproxyResultTuple = NamedTuple(
    "NewcloudviaproxyResultTuple", [("proxy", object)]
)
Cluster.ModelInstanceFactory.Server.NewcloudviazmqpipelineproxiesResultTuple = (
    NamedTuple("NewcloudviazmqpipelineproxiesResultTuple", [("proxyAddresses", object)])
)
Cluster.ModelInstanceFactory.Server.NewinstanceResultTuple = NamedTuple(
    "NewinstanceResultTuple", [("instance", object)]
)
Cluster.ModelInstanceFactory.Server.NewinstancesResultTuple = NamedTuple(
    "NewinstancesResultTuple", [("instances", object)]
)
Cluster.ModelInstanceFactory.Server.RegistermodelinstanceResultTuple = NamedTuple(
    "RegistermodelinstanceResultTuple", [("unregister", object)]
)
Cluster.ModelInstanceFactory.Server.RestoresturdyrefResultTuple = NamedTuple(
    "RestoresturdyrefResultTuple", [("cap", object)]
)
Cluster.Runtime.Server.AvailablemodelsResultTuple = NamedTuple(
    "AvailablemodelsResultTuple", [("factories", object)]
)
Cluster.Runtime.Server.FreenumberofcoresResultTuple = NamedTuple(
    "FreenumberofcoresResultTuple", [("cores", object)]
)
Cluster.Runtime.Server.NumberofcoresResultTuple = NamedTuple(
    "NumberofcoresResultTuple", [("cores", object)]
)
Cluster.Runtime.Server.RegistermodelinstancefactoryResultTuple = NamedTuple(
    "RegistermodelinstancefactoryResultTuple", [("unregister", object)]
)
Cluster.Runtime.Server.ReservenumberofcoresResultTuple = NamedTuple(
    "ReservenumberofcoresResultTuple", [("reservedCores", object)]
)
Cluster.Unregister.Server.UnregisterResultTuple = NamedTuple(
    "UnregisterResultTuple", [("success", object)]
)
Cluster.UserMaster.Server.AvailablemodelsResultTuple = NamedTuple(
    "AvailablemodelsResultTuple", [("factories", object)]
)
Cluster.ValueHolder.Server.ValueResultTuple = NamedTuple(
    "ValueResultTuple", [("val", object)]
)
