"""This is an automatically generated stub for `geo.capnp`."""

import os
import capnp

capnp.remove_import_hook()
here = os.path.dirname(os.path.abspath(__file__))
module_file = os.path.abspath(os.path.join(here, "../zalfmas_capnp_schemas/geo.capnp"))
import_path = [here, os.path.abspath(os.path.join(here, "../zalfmas_capnp_schemas"))]
CoordType = capnp.load(module_file, imports=import_path).CoordType
EPSG = capnp.load(module_file, imports=import_path).EPSG
UTMCoord = capnp.load(module_file, imports=import_path).UTMCoord
LatLonCoord = capnp.load(module_file, imports=import_path).LatLonCoord
GKCoord = capnp.load(module_file, imports=import_path).GKCoord
Point2D = capnp.load(module_file, imports=import_path).Point2D
RowCol = capnp.load(module_file, imports=import_path).RowCol
Coord = capnp.load(module_file, imports=import_path).Coord
RectBounds = capnp.load(module_file, imports=import_path).RectBounds
