"""This is an automatically generated stub for `geo.capnp`."""

from __future__ import annotations
from capnp.lib.capnp import (
    _DynamicCapabilityClient,
    _DynamicCapabilityServer,
    _DynamicStructBuilder,
    _DynamicStructReader,
    _DynamicListBuilder,
    _DynamicListReader,
    _DynamicObjectBuilder,
    _DynamicObjectReader,
    _StructModule,
)
from contextlib import AbstractContextManager
from collections.abc import Callable
from typing import Literal, overload, override, Any, IO

# Type alias for AnyPointer parameters (accepts all Cap'n Proto pointer types)
type AnyPointer = (
    str
    | bytes
    | _DynamicStructBuilder
    | _DynamicStructReader
    | _DynamicCapabilityClient
    | _DynamicCapabilityServer
    | _DynamicListBuilder
    | _DynamicListReader
    | _DynamicObjectReader
    | _DynamicObjectBuilder
)

class _CoordTypeEnumModule:
    gk: int
    utm: int
    latlon: int

class _EPSGStructModule(_StructModule):
    wgs84: int
    utm21S: int
    utm32N: int
    gk5: int
    gk4: int
    gk3: int
    class Reader(_DynamicStructReader):
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> EPSGBuilder: ...

    class Builder(_DynamicStructBuilder):
        @override
        def as_reader(self) -> EPSGReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        **kwargs: Any,
    ) -> EPSGBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[EPSGReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[EPSGReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[EPSGBuilder]: ...
    @override
    def from_bytes_packed(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> _DynamicStructReader: ...
    @override
    def read(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> EPSGReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> EPSGReader: ...

EPSG: _EPSGStructModule

class _UTMCoordStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def zone(self) -> int: ...
        @property
        def latitudeBand(self) -> str: ...
        @property
        def r(self) -> float: ...
        @property
        def h(self) -> float: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> UTMCoordBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def zone(self) -> int: ...
        @zone.setter
        def zone(self, value: int) -> None: ...
        @property
        def latitudeBand(self) -> str: ...
        @latitudeBand.setter
        def latitudeBand(self, value: str) -> None: ...
        @property
        def r(self) -> float: ...
        @r.setter
        def r(self, value: float) -> None: ...
        @property
        def h(self) -> float: ...
        @h.setter
        def h(self, value: float) -> None: ...
        @override
        def as_reader(self) -> UTMCoordReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        zone: int | None = None,
        latitudeBand: str | None = None,
        r: float | None = None,
        h: float | None = None,
        **kwargs: Any,
    ) -> UTMCoordBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[UTMCoordReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[UTMCoordReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[UTMCoordBuilder]: ...
    @override
    def from_bytes_packed(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> _DynamicStructReader: ...
    @override
    def read(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> UTMCoordReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> UTMCoordReader: ...

UTMCoord: _UTMCoordStructModule

class _LatLonCoordStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def lat(self) -> float: ...
        @property
        def lon(self) -> float: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> LatLonCoordBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def lat(self) -> float: ...
        @lat.setter
        def lat(self, value: float) -> None: ...
        @property
        def lon(self) -> float: ...
        @lon.setter
        def lon(self, value: float) -> None: ...
        @override
        def as_reader(self) -> LatLonCoordReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        lat: float | None = None,
        lon: float | None = None,
        **kwargs: Any,
    ) -> LatLonCoordBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[LatLonCoordReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[LatLonCoordReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[LatLonCoordBuilder]: ...
    @override
    def from_bytes_packed(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> _DynamicStructReader: ...
    @override
    def read(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> LatLonCoordReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> LatLonCoordReader: ...

LatLonCoord: _LatLonCoordStructModule

class _GKCoordStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def meridianNo(self) -> int: ...
        @property
        def r(self) -> float: ...
        @property
        def h(self) -> float: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> GKCoordBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def meridianNo(self) -> int: ...
        @meridianNo.setter
        def meridianNo(self, value: int) -> None: ...
        @property
        def r(self) -> float: ...
        @r.setter
        def r(self, value: float) -> None: ...
        @property
        def h(self) -> float: ...
        @h.setter
        def h(self, value: float) -> None: ...
        @override
        def as_reader(self) -> GKCoordReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        meridianNo: int | None = None,
        r: float | None = None,
        h: float | None = None,
        **kwargs: Any,
    ) -> GKCoordBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[GKCoordReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[GKCoordReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[GKCoordBuilder]: ...
    @override
    def from_bytes_packed(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> _DynamicStructReader: ...
    @override
    def read(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> GKCoordReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> GKCoordReader: ...

GKCoord: _GKCoordStructModule

class _Point2DStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def x(self) -> float: ...
        @property
        def y(self) -> float: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> Point2DBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def x(self) -> float: ...
        @x.setter
        def x(self, value: float) -> None: ...
        @property
        def y(self) -> float: ...
        @y.setter
        def y(self, value: float) -> None: ...
        @override
        def as_reader(self) -> Point2DReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        x: float | None = None,
        y: float | None = None,
        **kwargs: Any,
    ) -> Point2DBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[Point2DReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[Point2DReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[Point2DBuilder]: ...
    @override
    def from_bytes_packed(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> _DynamicStructReader: ...
    @override
    def read(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> Point2DReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> Point2DReader: ...

Point2D: _Point2DStructModule

class _RowColStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def row(self) -> int: ...
        @property
        def col(self) -> int: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> RowColBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def row(self) -> int: ...
        @row.setter
        def row(self, value: int) -> None: ...
        @property
        def col(self) -> int: ...
        @col.setter
        def col(self, value: int) -> None: ...
        @override
        def as_reader(self) -> RowColReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        row: int | None = None,
        col: int | None = None,
        **kwargs: Any,
    ) -> RowColBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[RowColReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[RowColReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[RowColBuilder]: ...
    @override
    def from_bytes_packed(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> _DynamicStructReader: ...
    @override
    def read(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> RowColReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> RowColReader: ...

RowCol: _RowColStructModule

class _CoordStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def gk(self) -> GKCoordReader: ...
        @property
        def latlon(self) -> LatLonCoordReader: ...
        @property
        def utm(self) -> UTMCoordReader: ...
        @property
        def p2D(self) -> Point2DReader: ...
        @property
        def rowcol(self) -> RowColReader: ...
        @override
        def which(self) -> Literal["gk", "latlon", "utm", "p2D", "rowcol"]: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> CoordBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def gk(self) -> GKCoordBuilder: ...
        @gk.setter
        def gk(
            self, value: GKCoordBuilder | GKCoordReader | dict[str, Any]
        ) -> None: ...
        @property
        def latlon(self) -> LatLonCoordBuilder: ...
        @latlon.setter
        def latlon(
            self, value: LatLonCoordBuilder | LatLonCoordReader | dict[str, Any]
        ) -> None: ...
        @property
        def utm(self) -> UTMCoordBuilder: ...
        @utm.setter
        def utm(
            self, value: UTMCoordBuilder | UTMCoordReader | dict[str, Any]
        ) -> None: ...
        @property
        def p2D(self) -> Point2DBuilder: ...
        @p2D.setter
        def p2D(
            self, value: Point2DBuilder | Point2DReader | dict[str, Any]
        ) -> None: ...
        @property
        def rowcol(self) -> RowColBuilder: ...
        @rowcol.setter
        def rowcol(
            self, value: RowColBuilder | RowColReader | dict[str, Any]
        ) -> None: ...
        @override
        def which(self) -> Literal["gk", "latlon", "utm", "p2D", "rowcol"]: ...
        @override
        @overload
        def init(
            self, field: Literal["gk"], size: int | None = None
        ) -> GKCoordBuilder: ...
        @overload
        def init(
            self, field: Literal["latlon"], size: int | None = None
        ) -> LatLonCoordBuilder: ...
        @overload
        def init(
            self, field: Literal["utm"], size: int | None = None
        ) -> UTMCoordBuilder: ...
        @overload
        def init(
            self, field: Literal["p2D"], size: int | None = None
        ) -> Point2DBuilder: ...
        @overload
        def init(
            self, field: Literal["rowcol"], size: int | None = None
        ) -> RowColBuilder: ...
        @overload
        def init(self, field: str, size: int | None = None) -> Any: ...
        @override
        def as_reader(self) -> CoordReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        gk: GKCoordBuilder | dict[str, Any] | None = None,
        latlon: LatLonCoordBuilder | dict[str, Any] | None = None,
        utm: UTMCoordBuilder | dict[str, Any] | None = None,
        p2D: Point2DBuilder | dict[str, Any] | None = None,
        rowcol: RowColBuilder | dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> CoordBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[CoordReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[CoordReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[CoordBuilder]: ...
    @override
    def from_bytes_packed(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> _DynamicStructReader: ...
    @override
    def read(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> CoordReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> CoordReader: ...

Coord: _CoordStructModule

class _RectBoundsStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def tl(self) -> _DynamicObjectReader: ...
        @property
        def br(self) -> _DynamicObjectReader: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> RectBoundsBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def tl(self) -> _DynamicObjectReader: ...
        @tl.setter
        def tl(self, value: AnyPointer) -> None: ...
        @property
        def br(self) -> _DynamicObjectReader: ...
        @br.setter
        def br(self, value: AnyPointer) -> None: ...
        @override
        def as_reader(self) -> RectBoundsReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        tl: AnyPointer | None = None,
        br: AnyPointer | None = None,
        **kwargs: Any,
    ) -> RectBoundsBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[RectBoundsReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[RectBoundsReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[RectBoundsBuilder]: ...
    @override
    def from_bytes_packed(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> _DynamicStructReader: ...
    @override
    def read(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> RectBoundsReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> RectBoundsReader: ...

RectBounds: _RectBoundsStructModule

# Top-level type aliases for use in type annotations
type CoordBuilder = _CoordStructModule.Builder
type CoordReader = _CoordStructModule.Reader
type CoordTypeEnum = int | Literal["gk", "utm", "latlon"]
type EPSGBuilder = _EPSGStructModule.Builder
type EPSGReader = _EPSGStructModule.Reader
type GKCoordBuilder = _GKCoordStructModule.Builder
type GKCoordReader = _GKCoordStructModule.Reader
type LatLonCoordBuilder = _LatLonCoordStructModule.Builder
type LatLonCoordReader = _LatLonCoordStructModule.Reader
type Point2DBuilder = _Point2DStructModule.Builder
type Point2DReader = _Point2DStructModule.Reader
type RectBoundsBuilder = _RectBoundsStructModule.Builder
type RectBoundsReader = _RectBoundsStructModule.Reader
type RowColBuilder = _RowColStructModule.Builder
type RowColReader = _RowColStructModule.Reader
type UTMCoordBuilder = _UTMCoordStructModule.Builder
type UTMCoordReader = _UTMCoordStructModule.Reader
