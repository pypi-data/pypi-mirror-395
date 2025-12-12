import os
import sys

import zalfmas_capnp_schemas

schemas_dir = os.path.dirname(zalfmas_capnp_schemas.__file__)
sys.path.append(schemas_dir)

from . import (
    a_capnp,
    climate_capnp,
    cluster_admin_service_capnp,
    common_capnp,
    config_capnp,
    crop_capnp,
    date_capnp,
    fbp_capnp,
    frontend_capnp,
    geo_capnp,
    grid_capnp,
    jobs_capnp,
    management_capnp,
    model_capnp,
    persistence_capnp,
    registry_capnp,
    service_capnp,
    soil_capnp,
    storage_capnp,
    x_capnp,
)

__all__ = [
    "a_capnp",
    "climate_capnp",
    "cluster_admin_service_capnp",
    "common_capnp",
    "config_capnp",
    "crop_capnp",
    "date_capnp",
    "fbp_capnp",
    "frontend_capnp",
    "geo_capnp",
    "grid_capnp",
    "jobs_capnp",
    "management_capnp",
    "model_capnp",
    "persistence_capnp",
    "registry_capnp",
    "service_capnp",
    "soil_capnp",
    "storage_capnp",
    "x_capnp",
    "schemas_dir",
]
