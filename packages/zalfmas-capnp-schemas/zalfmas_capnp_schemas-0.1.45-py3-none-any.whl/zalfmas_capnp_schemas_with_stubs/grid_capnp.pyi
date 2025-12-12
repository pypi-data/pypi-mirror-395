"""This is an automatically generated stub for `grid.capnp`."""

from __future__ import annotations
from capnp.lib.capnp import (
    _DynamicCapabilityClient,
    _DynamicCapabilityServer,
    _DynamicStructBuilder,
    _DynamicStructReader,
    _DynamicListBuilder,
    _DynamicListReader,
    _InterfaceModule,
    _StructModule,
)
from .common_capnp import _IdentifiableInterfaceModule
from .persistence_capnp import _PersistentInterfaceModule
from contextlib import AbstractContextManager
from .geo_capnp import LatLonCoordReader, LatLonCoordBuilder
from collections.abc import Iterator, Sequence, Awaitable, Callable
from typing import Literal, overload, override, Protocol, Any, IO, NamedTuple

class _AggregationEnumModule:
    none: int
    wAvg: int
    wMedian: int
    min: int
    max: int
    sum: int
    iAvg: int
    iMedian: int
    avg: int
    median: int
    wSum: int
    iSum: int
    wMin: int
    iMin: int
    wMax: int
    iMax: int

class _GridInterfaceModule(_IdentifiableInterfaceModule, _PersistentInterfaceModule):
    class _ValueStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def f(self) -> float: ...
            @property
            def i(self) -> int: ...
            @property
            def ui(self) -> int: ...
            @property
            def no(self) -> bool: ...
            @override
            def which(self) -> Literal["f", "i", "ui", "no"]: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> ValueBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def f(self) -> float: ...
            @f.setter
            def f(self, value: float) -> None: ...
            @property
            def i(self) -> int: ...
            @i.setter
            def i(self, value: int) -> None: ...
            @property
            def ui(self) -> int: ...
            @ui.setter
            def ui(self, value: int) -> None: ...
            @property
            def no(self) -> bool: ...
            @no.setter
            def no(self, value: bool) -> None: ...
            @override
            def which(self) -> Literal["f", "i", "ui", "no"]: ...
            @override
            def as_reader(self) -> ValueReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            f: float | None = None,
            i: int | None = None,
            ui: int | None = None,
            no: bool | None = None,
            **kwargs: Any,
        ) -> ValueBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[ValueReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[ValueReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[ValueBuilder]: ...
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
        ) -> ValueReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> ValueReader: ...

    type ValueReader = _ValueStructModule.Reader
    type ValueBuilder = _ValueStructModule.Builder
    Value: _ValueStructModule
    class _ResolutionStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def meter(self) -> int: ...
            @property
            def degree(self) -> float: ...
            @override
            def which(self) -> Literal["meter", "degree"]: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> ResolutionBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def meter(self) -> int: ...
            @meter.setter
            def meter(self, value: int) -> None: ...
            @property
            def degree(self) -> float: ...
            @degree.setter
            def degree(self, value: float) -> None: ...
            @override
            def which(self) -> Literal["meter", "degree"]: ...
            @override
            def as_reader(self) -> ResolutionReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            meter: int | None = None,
            degree: float | None = None,
            **kwargs: Any,
        ) -> ResolutionBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[ResolutionReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[ResolutionReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[ResolutionBuilder]: ...
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
        ) -> ResolutionReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> ResolutionReader: ...

    type ResolutionReader = _ResolutionStructModule.Reader
    type ResolutionBuilder = _ResolutionStructModule.Builder
    Resolution: _ResolutionStructModule
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

    type RowColReader = _RowColStructModule.Reader
    type RowColBuilder = _RowColStructModule.Builder
    RowCol: _RowColStructModule
    class _AggregationPartStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def value(self) -> ValueReader: ...
            @property
            def rowCol(self) -> RowColReader: ...
            @property
            def areaFrac(self) -> float: ...
            @property
            def iValue(self) -> float: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> AggregationPartBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def value(self) -> ValueBuilder: ...
            @value.setter
            def value(
                self, value: ValueBuilder | ValueReader | dict[str, Any]
            ) -> None: ...
            @property
            def rowCol(self) -> RowColBuilder: ...
            @rowCol.setter
            def rowCol(
                self, value: RowColBuilder | RowColReader | dict[str, Any]
            ) -> None: ...
            @property
            def areaFrac(self) -> float: ...
            @areaFrac.setter
            def areaFrac(self, value: float) -> None: ...
            @property
            def iValue(self) -> float: ...
            @iValue.setter
            def iValue(self, value: float) -> None: ...
            @override
            @overload
            def init(
                self, field: Literal["value"], size: int | None = None
            ) -> ValueBuilder: ...
            @overload
            def init(
                self, field: Literal["rowCol"], size: int | None = None
            ) -> RowColBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...
            @override
            def as_reader(self) -> AggregationPartReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            value: ValueBuilder | dict[str, Any] | None = None,
            rowCol: RowColBuilder | dict[str, Any] | None = None,
            areaFrac: float | None = None,
            iValue: float | None = None,
            **kwargs: Any,
        ) -> AggregationPartBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[AggregationPartReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[AggregationPartReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[AggregationPartBuilder]: ...
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
        ) -> AggregationPartReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AggregationPartReader: ...

    type AggregationPartReader = _AggregationPartStructModule.Reader
    type AggregationPartBuilder = _AggregationPartStructModule.Builder
    AggregationPart: _AggregationPartStructModule
    class _LocationStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def latLonCoord(self) -> LatLonCoordReader: ...
            @property
            def rowCol(self) -> RowColReader: ...
            @property
            def value(self) -> ValueReader: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> LocationBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def latLonCoord(self) -> LatLonCoordBuilder: ...
            @latLonCoord.setter
            def latLonCoord(
                self, value: LatLonCoordBuilder | LatLonCoordReader | dict[str, Any]
            ) -> None: ...
            @property
            def rowCol(self) -> RowColBuilder: ...
            @rowCol.setter
            def rowCol(
                self, value: RowColBuilder | RowColReader | dict[str, Any]
            ) -> None: ...
            @property
            def value(self) -> ValueBuilder: ...
            @value.setter
            def value(
                self, value: ValueBuilder | ValueReader | dict[str, Any]
            ) -> None: ...
            @override
            @overload
            def init(
                self, field: Literal["latLonCoord"], size: int | None = None
            ) -> LatLonCoordBuilder: ...
            @overload
            def init(
                self, field: Literal["rowCol"], size: int | None = None
            ) -> RowColBuilder: ...
            @overload
            def init(
                self, field: Literal["value"], size: int | None = None
            ) -> ValueBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...
            @override
            def as_reader(self) -> LocationReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            latLonCoord: LatLonCoordBuilder | dict[str, Any] | None = None,
            rowCol: RowColBuilder | dict[str, Any] | None = None,
            value: ValueBuilder | dict[str, Any] | None = None,
            **kwargs: Any,
        ) -> LocationBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[LocationReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[LocationReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[LocationBuilder]: ...
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
        ) -> LocationReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> LocationReader: ...

    type LocationReader = _LocationStructModule.Reader
    type LocationBuilder = _LocationStructModule.Builder
    Location: _LocationStructModule
    class _CallbackInterfaceModule(_InterfaceModule):
        class SendcellsRequest(Protocol):
            maxCount: int
            def send(
                self,
            ) -> _GridInterfaceModule._CallbackInterfaceModule.CallbackClient.SendcellsResult: ...

        @override
        def _new_client(
            self, server: _DynamicCapabilityServer
        ) -> _GridInterfaceModule._CallbackInterfaceModule.CallbackClient: ...
        class Server(_DynamicCapabilityServer):
            class SendcellsResult(_DynamicStructBuilder):
                @property
                def locations(self) -> LocationListBuilder: ...
                @locations.setter
                def locations(
                    self,
                    value: LocationListBuilder | LocationListReader | Sequence[Any],
                ) -> None: ...
                @overload
                def init(
                    self, field: Literal["locations"], size: int | None = None
                ) -> LocationListBuilder: ...
                @overload
                def init(self, field: str, size: int | None = None) -> Any: ...

            class SendcellsResultTuple(NamedTuple):
                locations: LocationListBuilder | LocationListReader

            class SendcellsParams(Protocol):
                maxCount: int

            class SendcellsCallContext(Protocol):
                params: (
                    _GridInterfaceModule._CallbackInterfaceModule.Server.SendcellsParams
                )
                @property
                def results(
                    self,
                ) -> (
                    _GridInterfaceModule._CallbackInterfaceModule.Server.SendcellsResult
                ): ...

            def sendCells(
                self,
                maxCount: int,
                _context: _GridInterfaceModule._CallbackInterfaceModule.Server.SendcellsCallContext,
                **kwargs: Any,
            ) -> Awaitable[
                Sequence[LocationBuilder | LocationReader]
                | _GridInterfaceModule._CallbackInterfaceModule.Server.SendcellsResultTuple
                | None
            ]: ...
            def sendCells_context(
                self,
                context: _GridInterfaceModule._CallbackInterfaceModule.Server.SendcellsCallContext,
            ) -> Awaitable[None]: ...

        class CallbackClient(_DynamicCapabilityClient):
            class SendcellsResult(Awaitable[SendcellsResult], Protocol):
                locations: LocationListReader

            def sendCells(
                self, maxCount: int | None = None
            ) -> _GridInterfaceModule._CallbackInterfaceModule.CallbackClient.SendcellsResult: ...
            def sendCells_request(
                self, maxCount: int | None = None
            ) -> _GridInterfaceModule._CallbackInterfaceModule.SendcellsRequest: ...

    Callback: _CallbackInterfaceModule
    type CallbackClient = _GridInterfaceModule._CallbackInterfaceModule.CallbackClient
    type CallbackServer = _GridInterfaceModule._CallbackInterfaceModule.Server
    class ClosestvalueatRequest(Protocol):
        latlonCoord: LatLonCoordBuilder
        ignoreNoData: bool
        resolution: ResolutionBuilder
        agg: AggregationEnum
        returnRowCols: bool
        includeAggParts: bool
        @overload
        def init(self, name: Literal["latlonCoord"]) -> LatLonCoordBuilder: ...
        @overload
        def init(self, name: Literal["resolution"]) -> ResolutionBuilder: ...
        @overload
        def init(self, name: str, size: int = ...) -> Any: ...
        def send(self) -> _GridInterfaceModule.GridClient.ClosestvalueatResult: ...

    class ResolutionRequest(Protocol):
        def send(self) -> _GridInterfaceModule.GridClient.ResolutionResult: ...

    class DimensionRequest(Protocol):
        def send(self) -> _GridInterfaceModule.GridClient.DimensionResult: ...

    class NodatavalueRequest(Protocol):
        def send(self) -> _GridInterfaceModule.GridClient.NodatavalueResult: ...

    class ValueatRequest(Protocol):
        row: int
        col: int
        resolution: ResolutionBuilder
        agg: AggregationEnum
        includeAggParts: bool
        @overload
        def init(self, name: Literal["resolution"]) -> ResolutionBuilder: ...
        @overload
        def init(self, name: str, size: int = ...) -> Any: ...
        def send(self) -> _GridInterfaceModule.GridClient.ValueatResult: ...

    class LatlonboundsRequest(Protocol):
        useCellCenter: bool
        def send(self) -> _GridInterfaceModule.GridClient.LatlonboundsResult: ...

    class StreamcellsRequest(Protocol):
        topLeft: RowColBuilder
        bottomRight: RowColBuilder
        @overload
        def init(self, name: Literal["topLeft"]) -> RowColBuilder: ...
        @overload
        def init(self, name: Literal["bottomRight"]) -> RowColBuilder: ...
        @overload
        def init(self, name: str, size: int = ...) -> Any: ...
        def send(self) -> _GridInterfaceModule.GridClient.StreamcellsResult: ...

    class UnitRequest(Protocol):
        def send(self) -> _GridInterfaceModule.GridClient.UnitResult: ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _GridInterfaceModule.GridClient: ...
    class Server(
        _IdentifiableInterfaceModule.Server, _PersistentInterfaceModule.Server
    ):
        class ClosestvalueatResult(_DynamicStructBuilder):
            @property
            def val(self) -> ValueBuilder: ...
            @val.setter
            def val(
                self, value: ValueBuilder | ValueReader | dict[str, Any]
            ) -> None: ...
            @property
            def tl(self) -> RowColBuilder: ...
            @tl.setter
            def tl(
                self, value: RowColBuilder | RowColReader | dict[str, Any]
            ) -> None: ...
            @property
            def br(self) -> RowColBuilder: ...
            @br.setter
            def br(
                self, value: RowColBuilder | RowColReader | dict[str, Any]
            ) -> None: ...
            @property
            def aggParts(self) -> AggregationPartListBuilder: ...
            @aggParts.setter
            def aggParts(
                self,
                value: AggregationPartListBuilder
                | AggregationPartListReader
                | Sequence[Any],
            ) -> None: ...
            @overload
            def init(
                self, field: Literal["val"], size: int | None = None
            ) -> ValueBuilder: ...
            @overload
            def init(
                self, field: Literal["tl"], size: int | None = None
            ) -> RowColBuilder: ...
            @overload
            def init(
                self, field: Literal["br"], size: int | None = None
            ) -> RowColBuilder: ...
            @overload
            def init(
                self, field: Literal["aggParts"], size: int | None = None
            ) -> AggregationPartListBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...

        class ResolutionResult(_DynamicStructBuilder):
            @property
            def res(self) -> ResolutionBuilder: ...
            @res.setter
            def res(
                self, value: ResolutionBuilder | ResolutionReader | dict[str, Any]
            ) -> None: ...
            @overload
            def init(
                self, field: Literal["res"], size: int | None = None
            ) -> ResolutionBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...

        class DimensionResult(_DynamicStructBuilder):
            @property
            def rows(self) -> int: ...
            @rows.setter
            def rows(self, value: int) -> None: ...
            @property
            def cols(self) -> int: ...
            @cols.setter
            def cols(self, value: int) -> None: ...

        class NodatavalueResult(_DynamicStructBuilder):
            @property
            def nodata(self) -> ValueBuilder: ...
            @nodata.setter
            def nodata(
                self, value: ValueBuilder | ValueReader | dict[str, Any]
            ) -> None: ...
            @overload
            def init(
                self, field: Literal["nodata"], size: int | None = None
            ) -> ValueBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...

        class ValueatResult(_DynamicStructBuilder):
            @property
            def val(self) -> ValueBuilder: ...
            @val.setter
            def val(
                self, value: ValueBuilder | ValueReader | dict[str, Any]
            ) -> None: ...
            @property
            def aggParts(self) -> AggregationPartListBuilder: ...
            @aggParts.setter
            def aggParts(
                self,
                value: AggregationPartListBuilder
                | AggregationPartListReader
                | Sequence[Any],
            ) -> None: ...
            @overload
            def init(
                self, field: Literal["val"], size: int | None = None
            ) -> ValueBuilder: ...
            @overload
            def init(
                self, field: Literal["aggParts"], size: int | None = None
            ) -> AggregationPartListBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...

        class LatlonboundsResult(_DynamicStructBuilder):
            @property
            def tl(self) -> LatLonCoordBuilder: ...
            @tl.setter
            def tl(
                self, value: LatLonCoordBuilder | LatLonCoordReader | dict[str, Any]
            ) -> None: ...
            @property
            def tr(self) -> LatLonCoordBuilder: ...
            @tr.setter
            def tr(
                self, value: LatLonCoordBuilder | LatLonCoordReader | dict[str, Any]
            ) -> None: ...
            @property
            def br(self) -> LatLonCoordBuilder: ...
            @br.setter
            def br(
                self, value: LatLonCoordBuilder | LatLonCoordReader | dict[str, Any]
            ) -> None: ...
            @property
            def bl(self) -> LatLonCoordBuilder: ...
            @bl.setter
            def bl(
                self, value: LatLonCoordBuilder | LatLonCoordReader | dict[str, Any]
            ) -> None: ...
            @overload
            def init(
                self, field: Literal["tl"], size: int | None = None
            ) -> LatLonCoordBuilder: ...
            @overload
            def init(
                self, field: Literal["tr"], size: int | None = None
            ) -> LatLonCoordBuilder: ...
            @overload
            def init(
                self, field: Literal["br"], size: int | None = None
            ) -> LatLonCoordBuilder: ...
            @overload
            def init(
                self, field: Literal["bl"], size: int | None = None
            ) -> LatLonCoordBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...

        class StreamcellsResult(_DynamicStructBuilder):
            @property
            def callback(
                self,
            ) -> (
                _GridInterfaceModule._CallbackInterfaceModule.Server
                | _GridInterfaceModule._CallbackInterfaceModule.CallbackClient
            ): ...
            @callback.setter
            def callback(
                self,
                value: _GridInterfaceModule._CallbackInterfaceModule.Server
                | _GridInterfaceModule._CallbackInterfaceModule.CallbackClient,
            ) -> None: ...

        class UnitResult(_DynamicStructBuilder):
            @property
            def unit(self) -> str: ...
            @unit.setter
            def unit(self, value: str) -> None: ...

        class ClosestvalueatResultTuple(NamedTuple):
            val: ValueBuilder | ValueReader
            tl: RowColBuilder | RowColReader
            br: RowColBuilder | RowColReader
            aggParts: AggregationPartListBuilder | AggregationPartListReader

        class ResolutionResultTuple(NamedTuple):
            res: ResolutionBuilder | ResolutionReader

        class DimensionResultTuple(NamedTuple):
            rows: int
            cols: int

        class NodatavalueResultTuple(NamedTuple):
            nodata: ValueBuilder | ValueReader

        class ValueatResultTuple(NamedTuple):
            val: ValueBuilder | ValueReader
            aggParts: AggregationPartListBuilder | AggregationPartListReader

        class LatlonboundsResultTuple(NamedTuple):
            tl: LatLonCoordBuilder | LatLonCoordReader
            tr: LatLonCoordBuilder | LatLonCoordReader
            br: LatLonCoordBuilder | LatLonCoordReader
            bl: LatLonCoordBuilder | LatLonCoordReader

        class StreamcellsResultTuple(NamedTuple):
            callback: (
                _GridInterfaceModule._CallbackInterfaceModule.Server
                | _GridInterfaceModule._CallbackInterfaceModule.CallbackClient
            )

        class UnitResultTuple(NamedTuple):
            unit: str

        class ClosestvalueatParams(Protocol):
            latlonCoord: LatLonCoordReader
            ignoreNoData: bool
            resolution: ResolutionReader
            agg: AggregationEnum
            returnRowCols: bool
            includeAggParts: bool

        class ClosestvalueatCallContext(Protocol):
            params: _GridInterfaceModule.Server.ClosestvalueatParams
            @property
            def results(self) -> _GridInterfaceModule.Server.ClosestvalueatResult: ...

        class ResolutionParams(Protocol): ...

        class ResolutionCallContext(Protocol):
            params: _GridInterfaceModule.Server.ResolutionParams
            @property
            def results(self) -> _GridInterfaceModule.Server.ResolutionResult: ...

        class DimensionParams(Protocol): ...

        class DimensionCallContext(Protocol):
            params: _GridInterfaceModule.Server.DimensionParams
            @property
            def results(self) -> _GridInterfaceModule.Server.DimensionResult: ...

        class NodatavalueParams(Protocol): ...

        class NodatavalueCallContext(Protocol):
            params: _GridInterfaceModule.Server.NodatavalueParams
            @property
            def results(self) -> _GridInterfaceModule.Server.NodatavalueResult: ...

        class ValueatParams(Protocol):
            row: int
            col: int
            resolution: ResolutionReader
            agg: AggregationEnum
            includeAggParts: bool

        class ValueatCallContext(Protocol):
            params: _GridInterfaceModule.Server.ValueatParams
            @property
            def results(self) -> _GridInterfaceModule.Server.ValueatResult: ...

        class LatlonboundsParams(Protocol):
            useCellCenter: bool

        class LatlonboundsCallContext(Protocol):
            params: _GridInterfaceModule.Server.LatlonboundsParams
            @property
            def results(self) -> _GridInterfaceModule.Server.LatlonboundsResult: ...

        class StreamcellsParams(Protocol):
            topLeft: RowColReader
            bottomRight: RowColReader

        class StreamcellsCallContext(Protocol):
            params: _GridInterfaceModule.Server.StreamcellsParams
            @property
            def results(self) -> _GridInterfaceModule.Server.StreamcellsResult: ...

        class UnitParams(Protocol): ...

        class UnitCallContext(Protocol):
            params: _GridInterfaceModule.Server.UnitParams
            @property
            def results(self) -> _GridInterfaceModule.Server.UnitResult: ...

        def closestValueAt(
            self,
            latlonCoord: LatLonCoordReader,
            ignoreNoData: bool,
            resolution: ResolutionReader,
            agg: AggregationEnum,
            returnRowCols: bool,
            includeAggParts: bool,
            _context: _GridInterfaceModule.Server.ClosestvalueatCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            _GridInterfaceModule.Server.ClosestvalueatResultTuple | None
        ]: ...
        def closestValueAt_context(
            self, context: _GridInterfaceModule.Server.ClosestvalueatCallContext
        ) -> Awaitable[None]: ...
        def resolution(
            self,
            _context: _GridInterfaceModule.Server.ResolutionCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            _GridInterfaceModule._ResolutionStructModule.Builder
            | _GridInterfaceModule.Server.ResolutionResultTuple
            | None
        ]: ...
        def resolution_context(
            self, context: _GridInterfaceModule.Server.ResolutionCallContext
        ) -> Awaitable[None]: ...
        def dimension(
            self,
            _context: _GridInterfaceModule.Server.DimensionCallContext,
            **kwargs: Any,
        ) -> Awaitable[_GridInterfaceModule.Server.DimensionResultTuple | None]: ...
        def dimension_context(
            self, context: _GridInterfaceModule.Server.DimensionCallContext
        ) -> Awaitable[None]: ...
        def noDataValue(
            self,
            _context: _GridInterfaceModule.Server.NodatavalueCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            _GridInterfaceModule._ValueStructModule.Builder
            | _GridInterfaceModule.Server.NodatavalueResultTuple
            | None
        ]: ...
        def noDataValue_context(
            self, context: _GridInterfaceModule.Server.NodatavalueCallContext
        ) -> Awaitable[None]: ...
        def valueAt(
            self,
            row: int,
            col: int,
            resolution: ResolutionReader,
            agg: AggregationEnum,
            includeAggParts: bool,
            _context: _GridInterfaceModule.Server.ValueatCallContext,
            **kwargs: Any,
        ) -> Awaitable[_GridInterfaceModule.Server.ValueatResultTuple | None]: ...
        def valueAt_context(
            self, context: _GridInterfaceModule.Server.ValueatCallContext
        ) -> Awaitable[None]: ...
        def latLonBounds(
            self,
            useCellCenter: bool,
            _context: _GridInterfaceModule.Server.LatlonboundsCallContext,
            **kwargs: Any,
        ) -> Awaitable[_GridInterfaceModule.Server.LatlonboundsResultTuple | None]: ...
        def latLonBounds_context(
            self, context: _GridInterfaceModule.Server.LatlonboundsCallContext
        ) -> Awaitable[None]: ...
        def streamCells(
            self,
            topLeft: RowColReader,
            bottomRight: RowColReader,
            _context: _GridInterfaceModule.Server.StreamcellsCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            _GridInterfaceModule._CallbackInterfaceModule.Server
            | _GridInterfaceModule.Server.StreamcellsResultTuple
            | None
        ]: ...
        def streamCells_context(
            self, context: _GridInterfaceModule.Server.StreamcellsCallContext
        ) -> Awaitable[None]: ...
        def unit(
            self, _context: _GridInterfaceModule.Server.UnitCallContext, **kwargs: Any
        ) -> Awaitable[str | _GridInterfaceModule.Server.UnitResultTuple | None]: ...
        def unit_context(
            self, context: _GridInterfaceModule.Server.UnitCallContext
        ) -> Awaitable[None]: ...

    class GridClient(
        _IdentifiableInterfaceModule.IdentifiableClient,
        _PersistentInterfaceModule.PersistentClient,
    ):
        class ClosestvalueatResult(Awaitable[ClosestvalueatResult], Protocol):
            val: ValueReader
            tl: RowColReader
            br: RowColReader
            aggParts: AggregationPartListReader

        class ResolutionResult(Awaitable[ResolutionResult], Protocol):
            res: ResolutionReader

        class DimensionResult(Awaitable[DimensionResult], Protocol):
            rows: int
            cols: int

        class NodatavalueResult(Awaitable[NodatavalueResult], Protocol):
            nodata: ValueReader

        class ValueatResult(Awaitable[ValueatResult], Protocol):
            val: ValueReader
            aggParts: AggregationPartListReader

        class LatlonboundsResult(Awaitable[LatlonboundsResult], Protocol):
            tl: LatLonCoordReader
            tr: LatLonCoordReader
            br: LatLonCoordReader
            bl: LatLonCoordReader

        class StreamcellsResult(Awaitable[StreamcellsResult], Protocol):
            callback: _GridInterfaceModule._CallbackInterfaceModule.CallbackClient

        class UnitResult(Awaitable[UnitResult], Protocol):
            unit: str

        def closestValueAt(
            self,
            latlonCoord: LatLonCoordBuilder
            | LatLonCoordReader
            | dict[str, Any]
            | None = None,
            ignoreNoData: bool | None = None,
            resolution: ResolutionBuilder
            | ResolutionReader
            | dict[str, Any]
            | None = None,
            agg: AggregationEnum | None = None,
            returnRowCols: bool | None = None,
            includeAggParts: bool | None = None,
        ) -> _GridInterfaceModule.GridClient.ClosestvalueatResult: ...
        def resolution(self) -> _GridInterfaceModule.GridClient.ResolutionResult: ...
        def dimension(self) -> _GridInterfaceModule.GridClient.DimensionResult: ...
        def noDataValue(self) -> _GridInterfaceModule.GridClient.NodatavalueResult: ...
        def valueAt(
            self,
            row: int | None = None,
            col: int | None = None,
            resolution: ResolutionBuilder
            | ResolutionReader
            | dict[str, Any]
            | None = None,
            agg: AggregationEnum | None = None,
            includeAggParts: bool | None = None,
        ) -> _GridInterfaceModule.GridClient.ValueatResult: ...
        def latLonBounds(
            self, useCellCenter: bool | None = None
        ) -> _GridInterfaceModule.GridClient.LatlonboundsResult: ...
        def streamCells(
            self,
            topLeft: RowColBuilder | RowColReader | dict[str, Any] | None = None,
            bottomRight: RowColBuilder | RowColReader | dict[str, Any] | None = None,
        ) -> _GridInterfaceModule.GridClient.StreamcellsResult: ...
        def unit(self) -> _GridInterfaceModule.GridClient.UnitResult: ...
        def closestValueAt_request(
            self,
            latlonCoord: LatLonCoordBuilder | None = None,
            ignoreNoData: bool | None = None,
            resolution: ResolutionBuilder | None = None,
            agg: AggregationEnum | None = None,
            returnRowCols: bool | None = None,
            includeAggParts: bool | None = None,
        ) -> _GridInterfaceModule.ClosestvalueatRequest: ...
        def resolution_request(self) -> _GridInterfaceModule.ResolutionRequest: ...
        def dimension_request(self) -> _GridInterfaceModule.DimensionRequest: ...
        def noDataValue_request(self) -> _GridInterfaceModule.NodatavalueRequest: ...
        def valueAt_request(
            self,
            row: int | None = None,
            col: int | None = None,
            resolution: ResolutionBuilder | None = None,
            agg: AggregationEnum | None = None,
            includeAggParts: bool | None = None,
        ) -> _GridInterfaceModule.ValueatRequest: ...
        def latLonBounds_request(
            self, useCellCenter: bool | None = None
        ) -> _GridInterfaceModule.LatlonboundsRequest: ...
        def streamCells_request(
            self,
            topLeft: RowColBuilder | None = None,
            bottomRight: RowColBuilder | None = None,
        ) -> _GridInterfaceModule.StreamcellsRequest: ...
        def unit_request(self) -> _GridInterfaceModule.UnitRequest: ...

class _LocationList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> LocationReader: ...
        @override
        def __iter__(self) -> Iterator[LocationReader]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> LocationBuilder: ...
        @override
        def __setitem__(
            self, key: int, value: LocationReader | LocationBuilder | dict[str, Any]
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[LocationBuilder]: ...
        @override
        def init(self, index: int, size: int | None = None) -> LocationBuilder: ...

class _AggregationPartList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> AggregationPartReader: ...
        @override
        def __iter__(self) -> Iterator[AggregationPartReader]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> AggregationPartBuilder: ...
        @override
        def __setitem__(
            self,
            key: int,
            value: AggregationPartReader | AggregationPartBuilder | dict[str, Any],
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[AggregationPartBuilder]: ...
        @override
        def init(
            self, index: int, size: int | None = None
        ) -> AggregationPartBuilder: ...

Grid: _GridInterfaceModule

# Top-level type aliases for use in type annotations
type AggregationEnum = (
    int
    | Literal[
        "none",
        "wAvg",
        "wMedian",
        "min",
        "max",
        "sum",
        "iAvg",
        "iMedian",
        "avg",
        "median",
        "wSum",
        "iSum",
        "wMin",
        "iMin",
        "wMax",
        "iMax",
    ]
)
type AggregationPartBuilder = _GridInterfaceModule._AggregationPartStructModule.Builder
type AggregationPartListBuilder = _AggregationPartList.Builder
type AggregationPartListReader = _AggregationPartList.Reader
type AggregationPartReader = _GridInterfaceModule._AggregationPartStructModule.Reader
type CallbackClient = _GridInterfaceModule._CallbackInterfaceModule.CallbackClient
type CallbackServer = _GridInterfaceModule._CallbackInterfaceModule.Server
type ClosestvalueatResult = _GridInterfaceModule.GridClient.ClosestvalueatResult
type DimensionResult = _GridInterfaceModule.GridClient.DimensionResult
type GridClient = _GridInterfaceModule.GridClient
type GridServer = _GridInterfaceModule.Server
type LatlonboundsResult = _GridInterfaceModule.GridClient.LatlonboundsResult
type LocationBuilder = _GridInterfaceModule._LocationStructModule.Builder
type LocationListBuilder = _LocationList.Builder
type LocationListReader = _LocationList.Reader
type LocationReader = _GridInterfaceModule._LocationStructModule.Reader
type NodatavalueResult = _GridInterfaceModule.GridClient.NodatavalueResult
type ResolutionBuilder = _GridInterfaceModule._ResolutionStructModule.Builder
type ResolutionReader = _GridInterfaceModule._ResolutionStructModule.Reader
type ResolutionResult = _GridInterfaceModule.GridClient.ResolutionResult
type RowColBuilder = _GridInterfaceModule._RowColStructModule.Builder
type RowColReader = _GridInterfaceModule._RowColStructModule.Reader
type SendcellsResult = (
    _GridInterfaceModule._CallbackInterfaceModule.CallbackClient.SendcellsResult
)
type StreamcellsResult = _GridInterfaceModule.GridClient.StreamcellsResult
type UnitResult = _GridInterfaceModule.GridClient.UnitResult
type ValueBuilder = _GridInterfaceModule._ValueStructModule.Builder
type ValueReader = _GridInterfaceModule._ValueStructModule.Reader
type ValueatResult = _GridInterfaceModule.GridClient.ValueatResult
