"""This is an automatically generated stub for `monica_params.capnp`."""

import os
import capnp

capnp.remove_import_hook()
here = os.path.dirname(os.path.abspath(__file__))
module_file = os.path.abspath(
    os.path.join(
        here, "../../../zalfmas_capnp_schemas/model/monica/monica_params.capnp"
    )
)
import_path = [
    here,
    os.path.abspath(os.path.join(here, "../../../zalfmas_capnp_schemas")),
    os.path.abspath(os.path.join(here, "../../../zalfmas_capnp_schemas/model/monica")),
]
CropSpec = capnp.load(module_file, imports=import_path).CropSpec
CropParameters = capnp.load(module_file, imports=import_path).CropParameters
SpeciesParameters = capnp.load(module_file, imports=import_path).SpeciesParameters
CultivarParameters = capnp.load(module_file, imports=import_path).CultivarParameters
YieldComponent = capnp.load(module_file, imports=import_path).YieldComponent
CropResidueParameters = capnp.load(
    module_file, imports=import_path
).CropResidueParameters
AutomaticHarvestParameters = capnp.load(
    module_file, imports=import_path
).AutomaticHarvestParameters
NMinCropParameters = capnp.load(module_file, imports=import_path).NMinCropParameters
NMinApplicationParameters = capnp.load(
    module_file, imports=import_path
).NMinApplicationParameters
SoilParameters = capnp.load(module_file, imports=import_path).SoilParameters
AutomaticIrrigationParameters = capnp.load(
    module_file, imports=import_path
).AutomaticIrrigationParameters
SiteParameters = capnp.load(module_file, imports=import_path).SiteParameters
EnvironmentParameters = capnp.load(
    module_file, imports=import_path
).EnvironmentParameters
MeasuredGroundwaterTableInformation = capnp.load(
    module_file, imports=import_path
).MeasuredGroundwaterTableInformation
SimulationParameters = capnp.load(module_file, imports=import_path).SimulationParameters
CropModuleParameters = capnp.load(module_file, imports=import_path).CropModuleParameters
SoilMoistureModuleParameters = capnp.load(
    module_file, imports=import_path
).SoilMoistureModuleParameters
SoilOrganicModuleParameters = capnp.load(
    module_file, imports=import_path
).SoilOrganicModuleParameters
SticsParameters = capnp.load(module_file, imports=import_path).SticsParameters
SoilTemperatureModuleParameters = capnp.load(
    module_file, imports=import_path
).SoilTemperatureModuleParameters
SoilTransportModuleParameters = capnp.load(
    module_file, imports=import_path
).SoilTransportModuleParameters
Voc = capnp.load(module_file, imports=import_path).Voc
