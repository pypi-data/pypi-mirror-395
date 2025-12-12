"""This is an automatically generated stub for `field_exp_data.capnp`."""

import os
import capnp

capnp.remove_import_hook()
here = os.path.dirname(os.path.abspath(__file__))
module_file = os.path.abspath(
    os.path.join(here, "../zalfmas_capnp_schemas/field_exp_data.capnp")
)
import_path = [here, os.path.abspath(os.path.join(here, "../zalfmas_capnp_schemas"))]
WeatherStation = capnp.load(module_file, imports=import_path).WeatherStation
SoilMetadata = capnp.load(module_file, imports=import_path).SoilMetadata
Field = capnp.load(module_file, imports=import_path).Field
ExperimentDescription = capnp.load(
    module_file, imports=import_path
).ExperimentDescription
Treatment = capnp.load(module_file, imports=import_path).Treatment
Plot = capnp.load(module_file, imports=import_path).Plot
Cultivar = capnp.load(module_file, imports=import_path).Cultivar
Residue = capnp.load(module_file, imports=import_path).Residue
InitialConditionsLayer = capnp.load(
    module_file, imports=import_path
).InitialConditionsLayer
PlantingEvent = capnp.load(module_file, imports=import_path).PlantingEvent
HarvestEvent = capnp.load(module_file, imports=import_path).HarvestEvent
IrrigationEvent = capnp.load(module_file, imports=import_path).IrrigationEvent
FertilizerEvent = capnp.load(module_file, imports=import_path).FertilizerEvent
EnvironmentModification = capnp.load(
    module_file, imports=import_path
).EnvironmentModification
