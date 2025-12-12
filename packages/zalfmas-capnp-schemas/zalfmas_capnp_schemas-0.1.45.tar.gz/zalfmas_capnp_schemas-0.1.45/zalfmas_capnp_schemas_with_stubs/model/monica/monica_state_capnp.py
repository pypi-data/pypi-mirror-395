"""This is an automatically generated stub for `monica_state.capnp`."""

import os
import capnp

capnp.remove_import_hook()
here = os.path.dirname(os.path.abspath(__file__))
module_file = os.path.abspath(
    os.path.join(here, "../../../zalfmas_capnp_schemas/model/monica/monica_state.capnp")
)
import_path = [
    here,
    os.path.abspath(os.path.join(here, "../../../zalfmas_capnp_schemas")),
    os.path.abspath(os.path.join(here, "../../../zalfmas_capnp_schemas/model/monica")),
]
MaybeBool = capnp.load(module_file, imports=import_path).MaybeBool
RuntimeState = capnp.load(module_file, imports=import_path).RuntimeState
MonicaModelState = capnp.load(module_file, imports=import_path).MonicaModelState
SoilColumnState = capnp.load(module_file, imports=import_path).SoilColumnState
CropModuleState = capnp.load(module_file, imports=import_path).CropModuleState
SoilLayerState = capnp.load(module_file, imports=import_path).SoilLayerState
AOMProperties = capnp.load(module_file, imports=import_path).AOMProperties
SoilTemperatureModuleState = capnp.load(
    module_file, imports=import_path
).SoilTemperatureModuleState
SoilMoistureModuleState = capnp.load(
    module_file, imports=import_path
).SoilMoistureModuleState
FrostModuleState = capnp.load(module_file, imports=import_path).FrostModuleState
SnowModuleState = capnp.load(module_file, imports=import_path).SnowModuleState
SoilOrganicModuleState = capnp.load(
    module_file, imports=import_path
).SoilOrganicModuleState
SoilTransportModuleState = capnp.load(
    module_file, imports=import_path
).SoilTransportModuleState
CropState = capnp.load(module_file, imports=import_path).CropState
ICData = capnp.load(module_file, imports=import_path).ICData
