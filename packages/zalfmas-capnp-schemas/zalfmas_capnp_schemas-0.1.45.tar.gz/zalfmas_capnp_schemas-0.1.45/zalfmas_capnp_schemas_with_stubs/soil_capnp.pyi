"""This is an automatically generated stub for `soil.capnp`."""

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
from contextlib import AbstractContextManager
from .common_capnp import _IdentifiableInterfaceModule
from .persistence_capnp import _PersistentInterfaceModule
from .geo_capnp import LatLonCoordReader, LatLonCoordBuilder
from collections.abc import Iterator, Sequence, Awaitable, Callable
from typing import Literal, overload, override, Protocol, Any, IO, NamedTuple

class _STypeEnumModule:
    unknown: int
    ka5: int

class _PropertyNameEnumModule:
    soilType: int
    sand: int
    clay: int
    silt: int
    pH: int
    sceleton: int
    organicCarbon: int
    organicMatter: int
    bulkDensity: int
    rawDensity: int
    fieldCapacity: int
    permanentWiltingPoint: int
    saturation: int
    soilMoisture: int
    soilWaterConductivityCoefficient: int
    ammonium: int
    nitrate: int
    cnRatio: int
    inGroundwater: int
    impenetrable: int

class _PropertyList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> PropertyReader: ...
        @override
        def __iter__(self) -> Iterator[PropertyReader]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> PropertyBuilder: ...
        @override
        def __setitem__(
            self, key: int, value: PropertyReader | PropertyBuilder | dict[str, Any]
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[PropertyBuilder]: ...
        @override
        def init(self, index: int, size: int | None = None) -> PropertyBuilder: ...

class _LayerStructModule(_StructModule):
    class _PropertyStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def name(self) -> PropertyNameEnum: ...
            @property
            def f32Value(self) -> float: ...
            @property
            def bValue(self) -> bool: ...
            @property
            def type(self) -> str: ...
            @property
            def unset(self) -> None: ...
            @override
            def which(self) -> Literal["f32Value", "bValue", "type", "unset"]: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> PropertyBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def name(self) -> PropertyNameEnum: ...
            @name.setter
            def name(self, value: PropertyNameEnum) -> None: ...
            @property
            def f32Value(self) -> float: ...
            @f32Value.setter
            def f32Value(self, value: float) -> None: ...
            @property
            def bValue(self) -> bool: ...
            @bValue.setter
            def bValue(self, value: bool) -> None: ...
            @property
            def type(self) -> str: ...
            @type.setter
            def type(self, value: str) -> None: ...
            @property
            def unset(self) -> None: ...
            @unset.setter
            def unset(self, value: None) -> None: ...
            @override
            def which(self) -> Literal["f32Value", "bValue", "type", "unset"]: ...
            @override
            def as_reader(self) -> PropertyReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            name: PropertyNameEnum | None = None,
            f32Value: float | None = None,
            bValue: bool | None = None,
            type: str | None = None,
            unset: None | None = None,
            **kwargs: Any,
        ) -> PropertyBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[PropertyReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[PropertyReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[PropertyBuilder]: ...
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
        ) -> PropertyReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> PropertyReader: ...

    type PropertyReader = _PropertyStructModule.Reader
    type PropertyBuilder = _PropertyStructModule.Builder
    Property: _PropertyStructModule
    class Reader(_DynamicStructReader):
        @property
        def properties(self) -> PropertyListReader: ...
        @property
        def size(self) -> float: ...
        @property
        def description(self) -> str: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> LayerBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def properties(self) -> PropertyListBuilder: ...
        @properties.setter
        def properties(
            self, value: PropertyListBuilder | PropertyListReader | dict[str, Any]
        ) -> None: ...
        @property
        def size(self) -> float: ...
        @size.setter
        def size(self, value: float) -> None: ...
        @property
        def description(self) -> str: ...
        @description.setter
        def description(self, value: str) -> None: ...
        @override
        def init(
            self, field: Literal["properties"], size: int | None = None
        ) -> PropertyListBuilder: ...
        @override
        def as_reader(self) -> LayerReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        properties: PropertyListBuilder | dict[str, Any] | None = None,
        size: float | None = None,
        description: str | None = None,
        **kwargs: Any,
    ) -> LayerBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[LayerReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[LayerReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[LayerBuilder]: ...
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
    ) -> LayerReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> LayerReader: ...

Layer: _LayerStructModule

class _PropertyNameEnumList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> PropertyNameEnum: ...
        @override
        def __iter__(self) -> Iterator[PropertyNameEnum]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> PropertyNameEnum: ...
        @override
        def __setitem__(self, key: int, value: PropertyNameEnum) -> None: ...
        @override
        def __iter__(self) -> Iterator[PropertyNameEnum]: ...

class _QueryStructModule(_StructModule):
    class _ResultStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def failed(self) -> bool: ...
            @property
            def mandatory(self) -> PropertyNameEnumListReader: ...
            @property
            def optional(self) -> PropertyNameEnumListReader: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> ResultBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def failed(self) -> bool: ...
            @failed.setter
            def failed(self, value: bool) -> None: ...
            @property
            def mandatory(self) -> PropertyNameEnumListBuilder: ...
            @mandatory.setter
            def mandatory(
                self,
                value: PropertyNameEnumListBuilder
                | PropertyNameEnumListReader
                | dict[str, Any],
            ) -> None: ...
            @property
            def optional(self) -> PropertyNameEnumListBuilder: ...
            @optional.setter
            def optional(
                self,
                value: PropertyNameEnumListBuilder
                | PropertyNameEnumListReader
                | dict[str, Any],
            ) -> None: ...
            @override
            @overload
            def init(
                self, field: Literal["mandatory"], size: int | None = None
            ) -> PropertyNameEnumListBuilder: ...
            @overload
            def init(
                self, field: Literal["optional"], size: int | None = None
            ) -> PropertyNameEnumListBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...
            @override
            def as_reader(self) -> ResultReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            failed: bool | None = None,
            mandatory: PropertyNameEnumListBuilder | dict[str, Any] | None = None,
            optional: PropertyNameEnumListBuilder | dict[str, Any] | None = None,
            **kwargs: Any,
        ) -> ResultBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[ResultReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[ResultReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[ResultBuilder]: ...
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
        ) -> ResultReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> ResultReader: ...

    type ResultReader = _ResultStructModule.Reader
    type ResultBuilder = _ResultStructModule.Builder
    Result: _ResultStructModule
    class Reader(_DynamicStructReader):
        @property
        def mandatory(self) -> PropertyNameEnumListReader: ...
        @property
        def optional(self) -> PropertyNameEnumListReader: ...
        @property
        def onlyRawData(self) -> bool: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> QueryBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def mandatory(self) -> PropertyNameEnumListBuilder: ...
        @mandatory.setter
        def mandatory(
            self,
            value: PropertyNameEnumListBuilder
            | PropertyNameEnumListReader
            | dict[str, Any],
        ) -> None: ...
        @property
        def optional(self) -> PropertyNameEnumListBuilder: ...
        @optional.setter
        def optional(
            self,
            value: PropertyNameEnumListBuilder
            | PropertyNameEnumListReader
            | dict[str, Any],
        ) -> None: ...
        @property
        def onlyRawData(self) -> bool: ...
        @onlyRawData.setter
        def onlyRawData(self, value: bool) -> None: ...
        @override
        @overload
        def init(
            self, field: Literal["mandatory"], size: int | None = None
        ) -> PropertyNameEnumListBuilder: ...
        @overload
        def init(
            self, field: Literal["optional"], size: int | None = None
        ) -> PropertyNameEnumListBuilder: ...
        @overload
        def init(self, field: str, size: int | None = None) -> Any: ...
        @override
        def as_reader(self) -> QueryReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        mandatory: PropertyNameEnumListBuilder | dict[str, Any] | None = None,
        optional: PropertyNameEnumListBuilder | dict[str, Any] | None = None,
        onlyRawData: bool | None = None,
        **kwargs: Any,
    ) -> QueryBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[QueryReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[QueryReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[QueryBuilder]: ...
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
    ) -> QueryReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> QueryReader: ...

Query: _QueryStructModule

class _LayerList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> LayerReader: ...
        @override
        def __iter__(self) -> Iterator[LayerReader]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> LayerBuilder: ...
        @override
        def __setitem__(
            self, key: int, value: LayerReader | LayerBuilder | dict[str, Any]
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[LayerBuilder]: ...
        @override
        def init(self, index: int, size: int | None = None) -> LayerBuilder: ...

class _ProfileDataStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def layers(self) -> LayerListReader: ...
        @property
        def percentageOfArea(self) -> float: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> ProfileDataBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def layers(self) -> LayerListBuilder: ...
        @layers.setter
        def layers(
            self, value: LayerListBuilder | LayerListReader | dict[str, Any]
        ) -> None: ...
        @property
        def percentageOfArea(self) -> float: ...
        @percentageOfArea.setter
        def percentageOfArea(self, value: float) -> None: ...
        @override
        def init(
            self, field: Literal["layers"], size: int | None = None
        ) -> LayerListBuilder: ...
        @override
        def as_reader(self) -> ProfileDataReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        layers: LayerListBuilder | dict[str, Any] | None = None,
        percentageOfArea: float | None = None,
        **kwargs: Any,
    ) -> ProfileDataBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[ProfileDataReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[ProfileDataReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[ProfileDataBuilder]: ...
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
    ) -> ProfileDataReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> ProfileDataReader: ...

ProfileData: _ProfileDataStructModule

class _ProfileInterfaceModule(_IdentifiableInterfaceModule, _PersistentInterfaceModule):
    class DataRequest(Protocol):
        def send(self) -> _ProfileInterfaceModule.ProfileClient.DataResult: ...

    class GeolocationRequest(Protocol):
        def send(self) -> _ProfileInterfaceModule.ProfileClient.GeolocationResult: ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _ProfileInterfaceModule.ProfileClient: ...
    class Server(
        _IdentifiableInterfaceModule.Server, _PersistentInterfaceModule.Server
    ):
        class DataResult(Awaitable[DataResult], Protocol):
            layers: LayerListBuilder | LayerListReader
            percentageOfArea: float

        class GeolocationResult(Awaitable[GeolocationResult], Protocol):
            lat: float
            lon: float

        class DataResultTuple(NamedTuple):
            layers: LayerListBuilder | LayerListReader
            percentageOfArea: float

        class GeolocationResultTuple(NamedTuple):
            lat: float
            lon: float

        class DataParams(Protocol): ...

        class DataCallContext(Protocol):
            params: _ProfileInterfaceModule.Server.DataParams
            @property
            def results(self) -> ProfileDataBuilder: ...

        class GeolocationParams(Protocol): ...

        class GeolocationCallContext(Protocol):
            params: _ProfileInterfaceModule.Server.GeolocationParams
            @property
            def results(self) -> LatLonCoordBuilder: ...

        def data(
            self,
            _context: _ProfileInterfaceModule.Server.DataCallContext,
            **kwargs: Any,
        ) -> Awaitable[_ProfileInterfaceModule.Server.DataResultTuple | None]: ...
        def data_context(
            self, context: _ProfileInterfaceModule.Server.DataCallContext
        ) -> Awaitable[None]: ...
        def geoLocation(
            self,
            _context: _ProfileInterfaceModule.Server.GeolocationCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            _ProfileInterfaceModule.Server.GeolocationResultTuple | None
        ]: ...
        def geoLocation_context(
            self, context: _ProfileInterfaceModule.Server.GeolocationCallContext
        ) -> Awaitable[None]: ...

    class ProfileClient(
        _IdentifiableInterfaceModule.IdentifiableClient,
        _PersistentInterfaceModule.PersistentClient,
    ):
        class DataResult(Awaitable[DataResult], Protocol):
            layers: LayerListReader
            percentageOfArea: float

        class GeolocationResult(Awaitable[GeolocationResult], Protocol):
            lat: float
            lon: float

        def data(self) -> _ProfileInterfaceModule.ProfileClient.DataResult: ...
        def geoLocation(
            self,
        ) -> _ProfileInterfaceModule.ProfileClient.GeolocationResult: ...
        def data_request(self) -> _ProfileInterfaceModule.DataRequest: ...
        def geoLocation_request(self) -> _ProfileInterfaceModule.GeolocationRequest: ...

Profile: _ProfileInterfaceModule

class _ServiceInterfaceModule(_IdentifiableInterfaceModule, _PersistentInterfaceModule):
    class _StreamInterfaceModule(_InterfaceModule):
        class NextprofilesRequest(Protocol):
            maxCount: int
            def send(
                self,
            ) -> _ServiceInterfaceModule._StreamInterfaceModule.StreamClient.NextprofilesResult: ...

        @override
        def _new_client(
            self, server: _DynamicCapabilityServer
        ) -> _ServiceInterfaceModule._StreamInterfaceModule.StreamClient: ...
        class Server(_DynamicCapabilityServer):
            class NextprofilesResult(_DynamicStructBuilder):
                @property
                def profiles(self) -> ProfileClientListBuilder: ...
                @profiles.setter
                def profiles(
                    self,
                    value: ProfileClientListBuilder
                    | ProfileClientListReader
                    | Sequence[Any],
                ) -> None: ...
                @overload
                def init(
                    self, field: Literal["profiles"], size: int | None = None
                ) -> ProfileClientListBuilder: ...
                @overload
                def init(self, field: str, size: int | None = None) -> Any: ...

            class NextprofilesResultTuple(NamedTuple):
                profiles: ProfileClientListBuilder | ProfileClientListReader

            class NextprofilesParams(Protocol):
                maxCount: int

            class NextprofilesCallContext(Protocol):
                params: _ServiceInterfaceModule._StreamInterfaceModule.Server.NextprofilesParams
                @property
                def results(
                    self,
                ) -> _ServiceInterfaceModule._StreamInterfaceModule.Server.NextprofilesResult: ...

            def nextProfiles(
                self,
                maxCount: int,
                _context: _ServiceInterfaceModule._StreamInterfaceModule.Server.NextprofilesCallContext,
                **kwargs: Any,
            ) -> Awaitable[
                Sequence[_ProfileInterfaceModule]
                | _ServiceInterfaceModule._StreamInterfaceModule.Server.NextprofilesResultTuple
                | None
            ]: ...
            def nextProfiles_context(
                self,
                context: _ServiceInterfaceModule._StreamInterfaceModule.Server.NextprofilesCallContext,
            ) -> Awaitable[None]: ...

        class StreamClient(_DynamicCapabilityClient):
            class NextprofilesResult(Awaitable[NextprofilesResult], Protocol):
                profiles: ProfileClientListReader

            def nextProfiles(
                self, maxCount: int | None = None
            ) -> _ServiceInterfaceModule._StreamInterfaceModule.StreamClient.NextprofilesResult: ...
            def nextProfiles_request(
                self, maxCount: int | None = None
            ) -> _ServiceInterfaceModule._StreamInterfaceModule.NextprofilesRequest: ...

    Stream: _StreamInterfaceModule
    type StreamClient = _ServiceInterfaceModule._StreamInterfaceModule.StreamClient
    type StreamServer = _ServiceInterfaceModule._StreamInterfaceModule.Server
    class CheckavailableparametersRequest(Protocol):
        mandatory: (
            PropertyNameEnumListBuilder | PropertyNameEnumListReader | Sequence[Any]
        )
        optional: (
            PropertyNameEnumListBuilder | PropertyNameEnumListReader | Sequence[Any]
        )
        onlyRawData: bool
        @overload
        def init(
            self, name: Literal["mandatory"], size: int = ...
        ) -> PropertyNameEnumListBuilder: ...
        @overload
        def init(
            self, name: Literal["optional"], size: int = ...
        ) -> PropertyNameEnumListBuilder: ...
        @overload
        def init(self, name: str, size: int = ...) -> Any: ...
        def send(
            self,
        ) -> _ServiceInterfaceModule.ServiceClient.CheckavailableparametersResult: ...

    class GetallavailableparametersRequest(Protocol):
        onlyRawData: bool
        def send(
            self,
        ) -> _ServiceInterfaceModule.ServiceClient.GetallavailableparametersResult: ...

    class ClosestprofilesatRequest(Protocol):
        coord: LatLonCoordBuilder
        query: QueryBuilder
        @overload
        def init(self, name: Literal["coord"]) -> LatLonCoordBuilder: ...
        @overload
        def init(self, name: Literal["query"]) -> QueryBuilder: ...
        @overload
        def init(self, name: str, size: int = ...) -> Any: ...
        def send(
            self,
        ) -> _ServiceInterfaceModule.ServiceClient.ClosestprofilesatResult: ...

    class StreamallprofilesRequest(Protocol):
        mandatory: (
            PropertyNameEnumListBuilder | PropertyNameEnumListReader | Sequence[Any]
        )
        optional: (
            PropertyNameEnumListBuilder | PropertyNameEnumListReader | Sequence[Any]
        )
        onlyRawData: bool
        @overload
        def init(
            self, name: Literal["mandatory"], size: int = ...
        ) -> PropertyNameEnumListBuilder: ...
        @overload
        def init(
            self, name: Literal["optional"], size: int = ...
        ) -> PropertyNameEnumListBuilder: ...
        @overload
        def init(self, name: str, size: int = ...) -> Any: ...
        def send(
            self,
        ) -> _ServiceInterfaceModule.ServiceClient.StreamallprofilesResult: ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _ServiceInterfaceModule.ServiceClient: ...
    class Server(
        _IdentifiableInterfaceModule.Server, _PersistentInterfaceModule.Server
    ):
        class CheckavailableparametersResult(
            Awaitable[CheckavailableparametersResult], Protocol
        ):
            failed: bool
            mandatory: PropertyNameEnumListBuilder | PropertyNameEnumListReader
            optional: PropertyNameEnumListBuilder | PropertyNameEnumListReader

        class GetallavailableparametersResult(_DynamicStructBuilder):
            @property
            def mandatory(self) -> PropertyNameEnumListBuilder: ...
            @mandatory.setter
            def mandatory(
                self,
                value: PropertyNameEnumListBuilder
                | PropertyNameEnumListReader
                | Sequence[Any],
            ) -> None: ...
            @property
            def optional(self) -> PropertyNameEnumListBuilder: ...
            @optional.setter
            def optional(
                self,
                value: PropertyNameEnumListBuilder
                | PropertyNameEnumListReader
                | Sequence[Any],
            ) -> None: ...
            @overload
            def init(
                self, field: Literal["mandatory"], size: int | None = None
            ) -> PropertyNameEnumListBuilder: ...
            @overload
            def init(
                self, field: Literal["optional"], size: int | None = None
            ) -> PropertyNameEnumListBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...

        class ClosestprofilesatResult(_DynamicStructBuilder):
            @property
            def profiles(self) -> ProfileClientListBuilder: ...
            @profiles.setter
            def profiles(
                self,
                value: ProfileClientListBuilder
                | ProfileClientListReader
                | Sequence[Any],
            ) -> None: ...
            @overload
            def init(
                self, field: Literal["profiles"], size: int | None = None
            ) -> ProfileClientListBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...

        class StreamallprofilesResult(_DynamicStructBuilder):
            @property
            def allProfiles(
                self,
            ) -> (
                _ServiceInterfaceModule._StreamInterfaceModule.Server
                | _ServiceInterfaceModule._StreamInterfaceModule.StreamClient
            ): ...
            @allProfiles.setter
            def allProfiles(
                self,
                value: _ServiceInterfaceModule._StreamInterfaceModule.Server
                | _ServiceInterfaceModule._StreamInterfaceModule.StreamClient,
            ) -> None: ...

        class CheckavailableparametersResultTuple(NamedTuple):
            failed: bool
            mandatory: PropertyNameEnumListBuilder | PropertyNameEnumListReader
            optional: PropertyNameEnumListBuilder | PropertyNameEnumListReader

        class GetallavailableparametersResultTuple(NamedTuple):
            mandatory: PropertyNameEnumListBuilder | PropertyNameEnumListReader
            optional: PropertyNameEnumListBuilder | PropertyNameEnumListReader

        class ClosestprofilesatResultTuple(NamedTuple):
            profiles: ProfileClientListBuilder | ProfileClientListReader

        class StreamallprofilesResultTuple(NamedTuple):
            allProfiles: (
                _ServiceInterfaceModule._StreamInterfaceModule.Server
                | _ServiceInterfaceModule._StreamInterfaceModule.StreamClient
            )

        class CheckavailableparametersParams(Protocol):
            mandatory: PropertyNameEnumListReader
            optional: PropertyNameEnumListReader
            onlyRawData: bool

        class CheckavailableparametersCallContext(Protocol):
            params: _ServiceInterfaceModule.Server.CheckavailableparametersParams
            @property
            def results(self) -> ResultBuilder: ...

        class GetallavailableparametersParams(Protocol):
            onlyRawData: bool

        class GetallavailableparametersCallContext(Protocol):
            params: _ServiceInterfaceModule.Server.GetallavailableparametersParams
            @property
            def results(
                self,
            ) -> _ServiceInterfaceModule.Server.GetallavailableparametersResult: ...

        class ClosestprofilesatParams(Protocol):
            coord: LatLonCoordReader
            query: QueryReader

        class ClosestprofilesatCallContext(Protocol):
            params: _ServiceInterfaceModule.Server.ClosestprofilesatParams
            @property
            def results(
                self,
            ) -> _ServiceInterfaceModule.Server.ClosestprofilesatResult: ...

        class StreamallprofilesParams(Protocol):
            mandatory: PropertyNameEnumListReader
            optional: PropertyNameEnumListReader
            onlyRawData: bool

        class StreamallprofilesCallContext(Protocol):
            params: _ServiceInterfaceModule.Server.StreamallprofilesParams
            @property
            def results(
                self,
            ) -> _ServiceInterfaceModule.Server.StreamallprofilesResult: ...

        def checkAvailableParameters(
            self,
            mandatory: PropertyNameEnumListReader,
            optional: PropertyNameEnumListReader,
            onlyRawData: bool,
            _context: _ServiceInterfaceModule.Server.CheckavailableparametersCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            _ServiceInterfaceModule.Server.CheckavailableparametersResultTuple | None
        ]: ...
        def checkAvailableParameters_context(
            self,
            context: _ServiceInterfaceModule.Server.CheckavailableparametersCallContext,
        ) -> Awaitable[None]: ...
        def getAllAvailableParameters(
            self,
            onlyRawData: bool,
            _context: _ServiceInterfaceModule.Server.GetallavailableparametersCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            _ServiceInterfaceModule.Server.GetallavailableparametersResultTuple | None
        ]: ...
        def getAllAvailableParameters_context(
            self,
            context: _ServiceInterfaceModule.Server.GetallavailableparametersCallContext,
        ) -> Awaitable[None]: ...
        def closestProfilesAt(
            self,
            coord: LatLonCoordReader,
            query: QueryReader,
            _context: _ServiceInterfaceModule.Server.ClosestprofilesatCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            Sequence[_ProfileInterfaceModule]
            | _ServiceInterfaceModule.Server.ClosestprofilesatResultTuple
            | None
        ]: ...
        def closestProfilesAt_context(
            self, context: _ServiceInterfaceModule.Server.ClosestprofilesatCallContext
        ) -> Awaitable[None]: ...
        def streamAllProfiles(
            self,
            mandatory: PropertyNameEnumListReader,
            optional: PropertyNameEnumListReader,
            onlyRawData: bool,
            _context: _ServiceInterfaceModule.Server.StreamallprofilesCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            _ServiceInterfaceModule._StreamInterfaceModule.Server
            | _ServiceInterfaceModule.Server.StreamallprofilesResultTuple
            | None
        ]: ...
        def streamAllProfiles_context(
            self, context: _ServiceInterfaceModule.Server.StreamallprofilesCallContext
        ) -> Awaitable[None]: ...

    class ServiceClient(
        _IdentifiableInterfaceModule.IdentifiableClient,
        _PersistentInterfaceModule.PersistentClient,
    ):
        class CheckavailableparametersResult(
            Awaitable[CheckavailableparametersResult], Protocol
        ):
            failed: bool
            mandatory: PropertyNameEnumListReader
            optional: PropertyNameEnumListReader

        class GetallavailableparametersResult(
            Awaitable[GetallavailableparametersResult], Protocol
        ):
            mandatory: PropertyNameEnumListReader
            optional: PropertyNameEnumListReader

        class ClosestprofilesatResult(Awaitable[ClosestprofilesatResult], Protocol):
            profiles: ProfileClientListReader

        class StreamallprofilesResult(Awaitable[StreamallprofilesResult], Protocol):
            allProfiles: _ServiceInterfaceModule._StreamInterfaceModule.StreamClient

        def checkAvailableParameters(
            self,
            mandatory: PropertyNameEnumListBuilder
            | PropertyNameEnumListReader
            | Sequence[Any]
            | None = None,
            optional: PropertyNameEnumListBuilder
            | PropertyNameEnumListReader
            | Sequence[Any]
            | None = None,
            onlyRawData: bool | None = None,
        ) -> _ServiceInterfaceModule.ServiceClient.CheckavailableparametersResult: ...
        def getAllAvailableParameters(
            self, onlyRawData: bool | None = None
        ) -> _ServiceInterfaceModule.ServiceClient.GetallavailableparametersResult: ...
        def closestProfilesAt(
            self,
            coord: LatLonCoordBuilder
            | LatLonCoordReader
            | dict[str, Any]
            | None = None,
            query: QueryBuilder | QueryReader | dict[str, Any] | None = None,
        ) -> _ServiceInterfaceModule.ServiceClient.ClosestprofilesatResult: ...
        def streamAllProfiles(
            self,
            mandatory: PropertyNameEnumListBuilder
            | PropertyNameEnumListReader
            | Sequence[Any]
            | None = None,
            optional: PropertyNameEnumListBuilder
            | PropertyNameEnumListReader
            | Sequence[Any]
            | None = None,
            onlyRawData: bool | None = None,
        ) -> _ServiceInterfaceModule.ServiceClient.StreamallprofilesResult: ...
        def checkAvailableParameters_request(
            self,
            mandatory: PropertyNameEnumListBuilder
            | PropertyNameEnumListReader
            | Sequence[Any]
            | None = None,
            optional: PropertyNameEnumListBuilder
            | PropertyNameEnumListReader
            | Sequence[Any]
            | None = None,
            onlyRawData: bool | None = None,
        ) -> _ServiceInterfaceModule.CheckavailableparametersRequest: ...
        def getAllAvailableParameters_request(
            self, onlyRawData: bool | None = None
        ) -> _ServiceInterfaceModule.GetallavailableparametersRequest: ...
        def closestProfilesAt_request(
            self,
            coord: LatLonCoordBuilder | None = None,
            query: QueryBuilder | None = None,
        ) -> _ServiceInterfaceModule.ClosestprofilesatRequest: ...
        def streamAllProfiles_request(
            self,
            mandatory: PropertyNameEnumListBuilder
            | PropertyNameEnumListReader
            | Sequence[Any]
            | None = None,
            optional: PropertyNameEnumListBuilder
            | PropertyNameEnumListReader
            | Sequence[Any]
            | None = None,
            onlyRawData: bool | None = None,
        ) -> _ServiceInterfaceModule.StreamallprofilesRequest: ...

class _ProfileClientList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> ProfileClient: ...
        @override
        def __iter__(self) -> Iterator[ProfileClient]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> ProfileClient: ...
        @override
        def __setitem__(
            self, key: int, value: ProfileClient | _ProfileInterfaceModule.Server
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[ProfileClient]: ...

Service: _ServiceInterfaceModule

# Top-level type aliases for use in type annotations
type CheckavailableparametersResult = (
    _ServiceInterfaceModule.ServiceClient.CheckavailableparametersResult
)
type ClosestprofilesatResult = (
    _ServiceInterfaceModule.ServiceClient.ClosestprofilesatResult
)
type DataResult = _ProfileInterfaceModule.ProfileClient.DataResult
type GeolocationResult = _ProfileInterfaceModule.ProfileClient.GeolocationResult
type GetallavailableparametersResult = (
    _ServiceInterfaceModule.ServiceClient.GetallavailableparametersResult
)
type LayerBuilder = _LayerStructModule.Builder
type LayerListBuilder = _LayerList.Builder
type LayerListReader = _LayerList.Reader
type LayerReader = _LayerStructModule.Reader
type NextprofilesResult = (
    _ServiceInterfaceModule._StreamInterfaceModule.StreamClient.NextprofilesResult
)
type ProfileClient = _ProfileInterfaceModule.ProfileClient
type ProfileClientListBuilder = _ProfileClientList.Builder
type ProfileClientListReader = _ProfileClientList.Reader
type ProfileDataBuilder = _ProfileDataStructModule.Builder
type ProfileDataReader = _ProfileDataStructModule.Reader
type ProfileServer = _ProfileInterfaceModule.Server
type PropertyBuilder = _LayerStructModule._PropertyStructModule.Builder
type PropertyListBuilder = _PropertyList.Builder
type PropertyListReader = _PropertyList.Reader
type PropertyNameEnum = (
    int
    | Literal[
        "soilType",
        "sand",
        "clay",
        "silt",
        "pH",
        "sceleton",
        "organicCarbon",
        "organicMatter",
        "bulkDensity",
        "rawDensity",
        "fieldCapacity",
        "permanentWiltingPoint",
        "saturation",
        "soilMoisture",
        "soilWaterConductivityCoefficient",
        "ammonium",
        "nitrate",
        "cnRatio",
        "inGroundwater",
        "impenetrable",
    ]
)
type PropertyNameEnumListBuilder = _PropertyNameEnumList.Builder
type PropertyNameEnumListReader = _PropertyNameEnumList.Reader
type PropertyReader = _LayerStructModule._PropertyStructModule.Reader
type QueryBuilder = _QueryStructModule.Builder
type QueryReader = _QueryStructModule.Reader
type ResultBuilder = _QueryStructModule._ResultStructModule.Builder
type ResultReader = _QueryStructModule._ResultStructModule.Reader
type STypeEnum = int | Literal["unknown", "ka5"]
type ServiceClient = _ServiceInterfaceModule.ServiceClient
type ServiceServer = _ServiceInterfaceModule.Server
type StreamClient = _ServiceInterfaceModule._StreamInterfaceModule.StreamClient
type StreamServer = _ServiceInterfaceModule._StreamInterfaceModule.Server
type StreamallprofilesResult = (
    _ServiceInterfaceModule.ServiceClient.StreamallprofilesResult
)
