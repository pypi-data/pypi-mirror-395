"""This is an automatically generated stub for `climate.capnp`."""

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
    _InterfaceModule,
    _StructModule,
)
from contextlib import AbstractContextManager
from .common_capnp import IdInformationReader, IdInformationBuilder
from .date_capnp import DateReader, DateBuilder
from .common_capnp import PairReader, PairBuilder
from .common_capnp import _IdentifiableInterfaceModule
from .persistence_capnp import _PersistentInterfaceModule
from .geo_capnp import LatLonCoordReader, LatLonCoordBuilder
from collections.abc import Iterator, Sequence, Awaitable, Callable
from typing import Literal, overload, override, Protocol, Any, IO, NamedTuple

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

class _GCMEnumModule:
    cccmaCanEsm2: int
    ichecEcEarth: int
    ipslIpslCm5AMr: int
    mirocMiroc5: int
    mpiMMpiEsmLr: int
    gfdlEsm4: int
    ipslCm6aLr: int
    mpiEsm12Hr: int
    mriEsm20: int
    ukesm10Ll: int
    gswp3W5E5: int
    mohcHadGem2Es: int

class _RCMEnumModule:
    clmcomCclm4817: int
    gericsRemo2015: int
    knmiRacmo22E: int
    smhiRca4: int
    clmcomBtuCclm4817: int
    mpiCscRemo2009: int
    uhohWrf361H: int

class _SSPEnumModule:
    ssp1: int
    ssp2: int
    ssp3: int
    ssp4: int
    ssp5: int

class _RCPEnumModule:
    rcp19: int
    rcp26: int
    rcp34: int
    rcp45: int
    rcp60: int
    rcp70: int
    rcp85: int

class _EnsembleMemberStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def r(self) -> int: ...
        @property
        def i(self) -> int: ...
        @property
        def p(self) -> int: ...
        @property
        def f(self) -> int: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> EnsembleMemberBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def r(self) -> int: ...
        @r.setter
        def r(self, value: int) -> None: ...
        @property
        def i(self) -> int: ...
        @i.setter
        def i(self, value: int) -> None: ...
        @property
        def p(self) -> int: ...
        @p.setter
        def p(self, value: int) -> None: ...
        @property
        def f(self) -> int: ...
        @f.setter
        def f(self, value: int) -> None: ...
        @override
        def as_reader(self) -> EnsembleMemberReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        r: int | None = None,
        i: int | None = None,
        p: int | None = None,
        f: int | None = None,
        **kwargs: Any,
    ) -> EnsembleMemberBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[EnsembleMemberReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[EnsembleMemberReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[EnsembleMemberBuilder]: ...
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
    ) -> EnsembleMemberReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> EnsembleMemberReader: ...

EnsembleMember: _EnsembleMemberStructModule

class _IdInformationList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> IdInformationReader: ...
        @override
        def __iter__(self) -> Iterator[IdInformationReader]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> IdInformationBuilder: ...
        @override
        def __setitem__(
            self,
            key: int,
            value: IdInformationReader | IdInformationBuilder | dict[str, Any],
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[IdInformationBuilder]: ...
        @override
        def init(self, index: int, size: int | None = None) -> IdInformationBuilder: ...

class _PairList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> PairReader: ...
        @override
        def __iter__(self) -> Iterator[PairReader]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> PairBuilder: ...
        @override
        def __setitem__(
            self, key: int, value: PairReader | PairBuilder | dict[str, Any]
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[PairBuilder]: ...
        @override
        def init(self, index: int, size: int | None = None) -> PairBuilder: ...

class _EntryList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> EntryReader: ...
        @override
        def __iter__(self) -> Iterator[EntryReader]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> EntryBuilder: ...
        @override
        def __setitem__(
            self, key: int, value: EntryReader | EntryBuilder | dict[str, Any]
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[EntryBuilder]: ...
        @override
        def init(self, index: int, size: int | None = None) -> EntryBuilder: ...

class _MetadataStructModule(_StructModule):
    class _SupportedInterfaceModule(_InterfaceModule):
        class CategoriesRequest(Protocol):
            def send(
                self,
            ) -> _MetadataStructModule._SupportedInterfaceModule.SupportedClient.CategoriesResult: ...

        class SupportedvaluesRequest(Protocol):
            typeId: str
            def send(
                self,
            ) -> _MetadataStructModule._SupportedInterfaceModule.SupportedClient.SupportedvaluesResult: ...

        @override
        def _new_client(
            self, server: _DynamicCapabilityServer
        ) -> _MetadataStructModule._SupportedInterfaceModule.SupportedClient: ...
        class Server(_DynamicCapabilityServer):
            class CategoriesResult(_DynamicStructBuilder):
                @property
                def types(self) -> IdInformationListBuilder: ...
                @types.setter
                def types(
                    self,
                    value: IdInformationListBuilder
                    | IdInformationListReader
                    | Sequence[Any],
                ) -> None: ...
                @overload
                def init(
                    self, field: Literal["types"], size: int | None = None
                ) -> IdInformationListBuilder: ...
                @overload
                def init(self, field: str, size: int | None = None) -> Any: ...

            class SupportedvaluesResult(_DynamicStructBuilder):
                @property
                def values(self) -> IdInformationListBuilder: ...
                @values.setter
                def values(
                    self,
                    value: IdInformationListBuilder
                    | IdInformationListReader
                    | Sequence[Any],
                ) -> None: ...
                @overload
                def init(
                    self, field: Literal["values"], size: int | None = None
                ) -> IdInformationListBuilder: ...
                @overload
                def init(self, field: str, size: int | None = None) -> Any: ...

            class CategoriesResultTuple(NamedTuple):
                types: IdInformationListBuilder | IdInformationListReader

            class SupportedvaluesResultTuple(NamedTuple):
                values: IdInformationListBuilder | IdInformationListReader

            class CategoriesParams(Protocol): ...

            class CategoriesCallContext(Protocol):
                params: _MetadataStructModule._SupportedInterfaceModule.Server.CategoriesParams
                @property
                def results(
                    self,
                ) -> _MetadataStructModule._SupportedInterfaceModule.Server.CategoriesResult: ...

            class SupportedvaluesParams(Protocol):
                typeId: str

            class SupportedvaluesCallContext(Protocol):
                params: _MetadataStructModule._SupportedInterfaceModule.Server.SupportedvaluesParams
                @property
                def results(
                    self,
                ) -> _MetadataStructModule._SupportedInterfaceModule.Server.SupportedvaluesResult: ...

            def categories(
                self,
                _context: _MetadataStructModule._SupportedInterfaceModule.Server.CategoriesCallContext,
                **kwargs: Any,
            ) -> Awaitable[
                Sequence[IdInformationBuilder | IdInformationReader]
                | _MetadataStructModule._SupportedInterfaceModule.Server.CategoriesResultTuple
                | None
            ]: ...
            def categories_context(
                self,
                context: _MetadataStructModule._SupportedInterfaceModule.Server.CategoriesCallContext,
            ) -> Awaitable[None]: ...
            def supportedValues(
                self,
                typeId: str,
                _context: _MetadataStructModule._SupportedInterfaceModule.Server.SupportedvaluesCallContext,
                **kwargs: Any,
            ) -> Awaitable[
                Sequence[IdInformationBuilder | IdInformationReader]
                | _MetadataStructModule._SupportedInterfaceModule.Server.SupportedvaluesResultTuple
                | None
            ]: ...
            def supportedValues_context(
                self,
                context: _MetadataStructModule._SupportedInterfaceModule.Server.SupportedvaluesCallContext,
            ) -> Awaitable[None]: ...

        class SupportedClient(_DynamicCapabilityClient):
            class CategoriesResult(Awaitable[CategoriesResult], Protocol):
                types: IdInformationListReader

            class SupportedvaluesResult(Awaitable[SupportedvaluesResult], Protocol):
                values: IdInformationListReader

            def categories(
                self,
            ) -> _MetadataStructModule._SupportedInterfaceModule.SupportedClient.CategoriesResult: ...
            def supportedValues(
                self, typeId: str | None = None
            ) -> _MetadataStructModule._SupportedInterfaceModule.SupportedClient.SupportedvaluesResult: ...
            def categories_request(
                self,
            ) -> _MetadataStructModule._SupportedInterfaceModule.CategoriesRequest: ...
            def supportedValues_request(
                self, typeId: str | None = None
            ) -> (
                _MetadataStructModule._SupportedInterfaceModule.SupportedvaluesRequest
            ): ...

    Supported: _SupportedInterfaceModule
    type SupportedClient = (
        _MetadataStructModule._SupportedInterfaceModule.SupportedClient
    )
    type SupportedServer = _MetadataStructModule._SupportedInterfaceModule.Server
    class _ValueStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def text(self) -> str: ...
            @property
            def float(self) -> float: ...
            @property
            def int(self) -> int: ...
            @property
            def bool(self) -> bool: ...
            @property
            def date(self) -> DateReader: ...
            @override
            def which(self) -> Literal["text", "float", "int", "bool", "date"]: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> ValueBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def text(self) -> str: ...
            @text.setter
            def text(self, value: str) -> None: ...
            @property
            def float(self) -> float: ...
            @float.setter
            def float(self, value: float) -> None: ...
            @property
            def int(self) -> int: ...
            @int.setter
            def int(self, value: int) -> None: ...
            @property
            def bool(self) -> bool: ...
            @bool.setter
            def bool(self, value: bool) -> None: ...
            @property
            def date(self) -> DateBuilder: ...
            @date.setter
            def date(
                self, value: DateBuilder | DateReader | dict[str, Any]
            ) -> None: ...
            @override
            def which(self) -> Literal["text", "float", "int", "bool", "date"]: ...
            @override
            def init(
                self, field: Literal["date"], size: int | None = None
            ) -> DateBuilder: ...
            @override
            def as_reader(self) -> ValueReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            text: str | None = None,
            float: float | None = None,
            int: int | None = None,
            bool: bool | None = None,
            date: DateBuilder | dict[str, Any] | None = None,
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
    class _EntryStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def gcm(self) -> GCMEnum: ...
            @property
            def rcm(self) -> RCMEnum: ...
            @property
            def historical(self) -> None: ...
            @property
            def rcp(self) -> RCPEnum: ...
            @property
            def ssp(self) -> SSPEnum: ...
            @property
            def ensMem(self) -> EnsembleMemberReader: ...
            @property
            def version(self) -> str: ...
            @property
            def start(self) -> DateReader: ...
            @property
            def end(self) -> DateReader: ...
            @property
            def co2(self) -> float: ...
            @property
            def picontrol(self) -> None: ...
            @property
            def description(self) -> str: ...
            @override
            def which(
                self,
            ) -> Literal[
                "gcm",
                "rcm",
                "historical",
                "rcp",
                "ssp",
                "ensMem",
                "version",
                "start",
                "end",
                "co2",
                "picontrol",
                "description",
            ]: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> EntryBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def gcm(self) -> GCMEnum: ...
            @gcm.setter
            def gcm(self, value: GCMEnum) -> None: ...
            @property
            def rcm(self) -> RCMEnum: ...
            @rcm.setter
            def rcm(self, value: RCMEnum) -> None: ...
            @property
            def historical(self) -> None: ...
            @historical.setter
            def historical(self, value: None) -> None: ...
            @property
            def rcp(self) -> RCPEnum: ...
            @rcp.setter
            def rcp(self, value: RCPEnum) -> None: ...
            @property
            def ssp(self) -> SSPEnum: ...
            @ssp.setter
            def ssp(self, value: SSPEnum) -> None: ...
            @property
            def ensMem(self) -> EnsembleMemberBuilder: ...
            @ensMem.setter
            def ensMem(
                self,
                value: EnsembleMemberBuilder | EnsembleMemberReader | dict[str, Any],
            ) -> None: ...
            @property
            def version(self) -> str: ...
            @version.setter
            def version(self, value: str) -> None: ...
            @property
            def start(self) -> DateBuilder: ...
            @start.setter
            def start(
                self, value: DateBuilder | DateReader | dict[str, Any]
            ) -> None: ...
            @property
            def end(self) -> DateBuilder: ...
            @end.setter
            def end(self, value: DateBuilder | DateReader | dict[str, Any]) -> None: ...
            @property
            def co2(self) -> float: ...
            @co2.setter
            def co2(self, value: float) -> None: ...
            @property
            def picontrol(self) -> None: ...
            @picontrol.setter
            def picontrol(self, value: None) -> None: ...
            @property
            def description(self) -> str: ...
            @description.setter
            def description(self, value: str) -> None: ...
            @override
            def which(
                self,
            ) -> Literal[
                "gcm",
                "rcm",
                "historical",
                "rcp",
                "ssp",
                "ensMem",
                "version",
                "start",
                "end",
                "co2",
                "picontrol",
                "description",
            ]: ...
            @override
            @overload
            def init(
                self, field: Literal["ensMem"], size: int | None = None
            ) -> EnsembleMemberBuilder: ...
            @overload
            def init(
                self, field: Literal["start"], size: int | None = None
            ) -> DateBuilder: ...
            @overload
            def init(
                self, field: Literal["end"], size: int | None = None
            ) -> DateBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...
            @override
            def as_reader(self) -> EntryReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            gcm: GCMEnum | None = None,
            rcm: RCMEnum | None = None,
            historical: None | None = None,
            rcp: RCPEnum | None = None,
            ssp: SSPEnum | None = None,
            ensMem: EnsembleMemberBuilder | dict[str, Any] | None = None,
            version: str | None = None,
            start: DateBuilder | dict[str, Any] | None = None,
            end: DateBuilder | dict[str, Any] | None = None,
            co2: float | None = None,
            picontrol: None | None = None,
            description: str | None = None,
            **kwargs: Any,
        ) -> EntryBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[EntryReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[EntryReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[EntryBuilder]: ...
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
        ) -> EntryReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> EntryReader: ...

    type EntryReader = _EntryStructModule.Reader
    type EntryBuilder = _EntryStructModule.Builder
    Entry: _EntryStructModule
    class _InformationInterfaceModule(_InterfaceModule):
        class ForoneRequest(Protocol):
            entry: EntryBuilder
            @overload
            def init(self, name: Literal["entry"]) -> EntryBuilder: ...
            @overload
            def init(self, name: str, size: int = ...) -> Any: ...
            def send(
                self,
            ) -> _MetadataStructModule._InformationInterfaceModule.InformationClient.ForoneResult: ...

        class ForallRequest(Protocol):
            def send(
                self,
            ) -> _MetadataStructModule._InformationInterfaceModule.InformationClient.ForallResult: ...

        @override
        def _new_client(
            self, server: _DynamicCapabilityServer
        ) -> _MetadataStructModule._InformationInterfaceModule.InformationClient: ...
        class Server(_DynamicCapabilityServer):
            class ForoneResult(Awaitable[ForoneResult], Protocol):
                id: str
                name: str
                description: str

            class ForallResult(_DynamicStructBuilder):
                @property
                def all(self) -> PairListBuilder: ...
                @all.setter
                def all(
                    self, value: PairListBuilder | PairListReader | Sequence[Any]
                ) -> None: ...
                @overload
                def init(
                    self, field: Literal["all"], size: int | None = None
                ) -> PairListBuilder: ...
                @overload
                def init(self, field: str, size: int | None = None) -> Any: ...

            class ForoneResultTuple(NamedTuple):
                id: str
                name: str
                description: str

            class ForallResultTuple(NamedTuple):
                all: PairListBuilder | PairListReader

            class ForoneParams(Protocol):
                entry: EntryReader

            class ForoneCallContext(Protocol):
                params: _MetadataStructModule._InformationInterfaceModule.Server.ForoneParams
                @property
                def results(self) -> IdInformationBuilder: ...

            class ForallParams(Protocol): ...

            class ForallCallContext(Protocol):
                params: _MetadataStructModule._InformationInterfaceModule.Server.ForallParams
                @property
                def results(
                    self,
                ) -> _MetadataStructModule._InformationInterfaceModule.Server.ForallResult: ...

            def forOne(
                self,
                entry: EntryReader,
                _context: _MetadataStructModule._InformationInterfaceModule.Server.ForoneCallContext,
                **kwargs: Any,
            ) -> Awaitable[
                _MetadataStructModule._InformationInterfaceModule.Server.ForoneResultTuple
                | None
            ]: ...
            def forOne_context(
                self,
                context: _MetadataStructModule._InformationInterfaceModule.Server.ForoneCallContext,
            ) -> Awaitable[None]: ...
            def forAll(
                self,
                _context: _MetadataStructModule._InformationInterfaceModule.Server.ForallCallContext,
                **kwargs: Any,
            ) -> Awaitable[
                Sequence[PairBuilder | PairReader]
                | _MetadataStructModule._InformationInterfaceModule.Server.ForallResultTuple
                | None
            ]: ...
            def forAll_context(
                self,
                context: _MetadataStructModule._InformationInterfaceModule.Server.ForallCallContext,
            ) -> Awaitable[None]: ...

        class InformationClient(_DynamicCapabilityClient):
            class ForoneResult(Awaitable[ForoneResult], Protocol):
                id: str
                name: str
                description: str

            class ForallResult(Awaitable[ForallResult], Protocol):
                all: PairListReader

            def forOne(
                self, entry: EntryBuilder | EntryReader | dict[str, Any] | None = None
            ) -> _MetadataStructModule._InformationInterfaceModule.InformationClient.ForoneResult: ...
            def forAll(
                self,
            ) -> _MetadataStructModule._InformationInterfaceModule.InformationClient.ForallResult: ...
            def forOne_request(
                self, entry: EntryBuilder | None = None
            ) -> _MetadataStructModule._InformationInterfaceModule.ForoneRequest: ...
            def forAll_request(
                self,
            ) -> _MetadataStructModule._InformationInterfaceModule.ForallRequest: ...

    Information: _InformationInterfaceModule
    type InformationClient = (
        _MetadataStructModule._InformationInterfaceModule.InformationClient
    )
    type InformationServer = _MetadataStructModule._InformationInterfaceModule.Server
    class Reader(_DynamicStructReader):
        @property
        def entries(self) -> EntryListReader: ...
        @property
        def info(
            self,
        ) -> _MetadataStructModule._InformationInterfaceModule.InformationClient: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> MetadataBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def entries(self) -> EntryListBuilder: ...
        @entries.setter
        def entries(
            self, value: EntryListBuilder | EntryListReader | dict[str, Any]
        ) -> None: ...
        @property
        def info(
            self,
        ) -> _MetadataStructModule._InformationInterfaceModule.InformationClient: ...
        @info.setter
        def info(
            self,
            value: _MetadataStructModule._InformationInterfaceModule.InformationClient
            | _MetadataStructModule._InformationInterfaceModule.Server,
        ) -> None: ...
        @override
        def init(
            self, field: Literal["entries"], size: int | None = None
        ) -> EntryListBuilder: ...
        @override
        def as_reader(self) -> MetadataReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        entries: EntryListBuilder | dict[str, Any] | None = None,
        info: _MetadataStructModule._InformationInterfaceModule.InformationClient
        | _MetadataStructModule._InformationInterfaceModule.Server
        | None = None,
        **kwargs: Any,
    ) -> MetadataBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[MetadataReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[MetadataReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[MetadataBuilder]: ...
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
    ) -> MetadataReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> MetadataReader: ...

Metadata: _MetadataStructModule

class _DatasetInterfaceModule(_IdentifiableInterfaceModule, _PersistentInterfaceModule):
    class _GetLocationsCallbackInterfaceModule(_InterfaceModule):
        class NextlocationsRequest(Protocol):
            maxCount: int
            def send(
                self,
            ) -> _DatasetInterfaceModule._GetLocationsCallbackInterfaceModule.GetLocationsCallbackClient.NextlocationsResult: ...

        @override
        def _new_client(
            self, server: _DynamicCapabilityServer
        ) -> _DatasetInterfaceModule._GetLocationsCallbackInterfaceModule.GetLocationsCallbackClient: ...
        class Server(_DynamicCapabilityServer):
            class NextlocationsResult(_DynamicStructBuilder):
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

            class NextlocationsResultTuple(NamedTuple):
                locations: LocationListBuilder | LocationListReader

            class NextlocationsParams(Protocol):
                maxCount: int

            class NextlocationsCallContext(Protocol):
                params: _DatasetInterfaceModule._GetLocationsCallbackInterfaceModule.Server.NextlocationsParams
                @property
                def results(
                    self,
                ) -> _DatasetInterfaceModule._GetLocationsCallbackInterfaceModule.Server.NextlocationsResult: ...

            def nextLocations(
                self,
                maxCount: int,
                _context: _DatasetInterfaceModule._GetLocationsCallbackInterfaceModule.Server.NextlocationsCallContext,
                **kwargs: Any,
            ) -> Awaitable[
                Sequence[LocationBuilder | LocationReader]
                | _DatasetInterfaceModule._GetLocationsCallbackInterfaceModule.Server.NextlocationsResultTuple
                | None
            ]: ...
            def nextLocations_context(
                self,
                context: _DatasetInterfaceModule._GetLocationsCallbackInterfaceModule.Server.NextlocationsCallContext,
            ) -> Awaitable[None]: ...

        class GetLocationsCallbackClient(_DynamicCapabilityClient):
            class NextlocationsResult(Awaitable[NextlocationsResult], Protocol):
                locations: LocationListReader

            def nextLocations(
                self, maxCount: int | None = None
            ) -> _DatasetInterfaceModule._GetLocationsCallbackInterfaceModule.GetLocationsCallbackClient.NextlocationsResult: ...
            def nextLocations_request(
                self, maxCount: int | None = None
            ) -> _DatasetInterfaceModule._GetLocationsCallbackInterfaceModule.NextlocationsRequest: ...

    GetLocationsCallback: _GetLocationsCallbackInterfaceModule
    type GetLocationsCallbackClient = _DatasetInterfaceModule._GetLocationsCallbackInterfaceModule.GetLocationsCallbackClient
    type GetLocationsCallbackServer = (
        _DatasetInterfaceModule._GetLocationsCallbackInterfaceModule.Server
    )
    class MetadataRequest(Protocol):
        def send(self) -> _DatasetInterfaceModule.DatasetClient.MetadataResult: ...

    class ClosesttimeseriesatRequest(Protocol):
        latlon: LatLonCoordBuilder
        @overload
        def init(self, name: Literal["latlon"]) -> LatLonCoordBuilder: ...
        @overload
        def init(self, name: str, size: int = ...) -> Any: ...
        def send(
            self,
        ) -> _DatasetInterfaceModule.DatasetClient.ClosesttimeseriesatResult: ...

    class TimeseriesatRequest(Protocol):
        locationId: str
        def send(self) -> _DatasetInterfaceModule.DatasetClient.TimeseriesatResult: ...

    class LocationsRequest(Protocol):
        def send(self) -> _DatasetInterfaceModule.DatasetClient.LocationsResult: ...

    class StreamlocationsRequest(Protocol):
        startAfterLocationId: str
        def send(
            self,
        ) -> _DatasetInterfaceModule.DatasetClient.StreamlocationsResult: ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _DatasetInterfaceModule.DatasetClient: ...
    class Server(
        _IdentifiableInterfaceModule.Server, _PersistentInterfaceModule.Server
    ):
        class MetadataResult(Awaitable[MetadataResult], Protocol):
            entries: EntryListBuilder | EntryListReader
            info: (
                _MetadataStructModule._InformationInterfaceModule.Server
                | _MetadataStructModule._InformationInterfaceModule.InformationClient
            )

        class ClosesttimeseriesatResult(_DynamicStructBuilder):
            @property
            def timeSeries(
                self,
            ) -> (
                _TimeSeriesInterfaceModule.Server
                | _TimeSeriesInterfaceModule.TimeSeriesClient
            ): ...
            @timeSeries.setter
            def timeSeries(
                self,
                value: _TimeSeriesInterfaceModule.Server
                | _TimeSeriesInterfaceModule.TimeSeriesClient,
            ) -> None: ...

        class TimeseriesatResult(_DynamicStructBuilder):
            @property
            def timeSeries(
                self,
            ) -> (
                _TimeSeriesInterfaceModule.Server
                | _TimeSeriesInterfaceModule.TimeSeriesClient
            ): ...
            @timeSeries.setter
            def timeSeries(
                self,
                value: _TimeSeriesInterfaceModule.Server
                | _TimeSeriesInterfaceModule.TimeSeriesClient,
            ) -> None: ...

        class LocationsResult(_DynamicStructBuilder):
            @property
            def locations(self) -> LocationListBuilder: ...
            @locations.setter
            def locations(
                self, value: LocationListBuilder | LocationListReader | Sequence[Any]
            ) -> None: ...
            @overload
            def init(
                self, field: Literal["locations"], size: int | None = None
            ) -> LocationListBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...

        class StreamlocationsResult(_DynamicStructBuilder):
            @property
            def locationsCallback(
                self,
            ) -> (
                _DatasetInterfaceModule._GetLocationsCallbackInterfaceModule.Server
                | _DatasetInterfaceModule._GetLocationsCallbackInterfaceModule.GetLocationsCallbackClient
            ): ...
            @locationsCallback.setter
            def locationsCallback(
                self,
                value: _DatasetInterfaceModule._GetLocationsCallbackInterfaceModule.Server
                | _DatasetInterfaceModule._GetLocationsCallbackInterfaceModule.GetLocationsCallbackClient,
            ) -> None: ...

        class MetadataResultTuple(NamedTuple):
            entries: EntryListBuilder | EntryListReader
            info: (
                _MetadataStructModule._InformationInterfaceModule.Server
                | _MetadataStructModule._InformationInterfaceModule.InformationClient
            )

        class ClosesttimeseriesatResultTuple(NamedTuple):
            timeSeries: (
                _TimeSeriesInterfaceModule.Server
                | _TimeSeriesInterfaceModule.TimeSeriesClient
            )

        class TimeseriesatResultTuple(NamedTuple):
            timeSeries: (
                _TimeSeriesInterfaceModule.Server
                | _TimeSeriesInterfaceModule.TimeSeriesClient
            )

        class LocationsResultTuple(NamedTuple):
            locations: LocationListBuilder | LocationListReader

        class StreamlocationsResultTuple(NamedTuple):
            locationsCallback: (
                _DatasetInterfaceModule._GetLocationsCallbackInterfaceModule.Server
                | _DatasetInterfaceModule._GetLocationsCallbackInterfaceModule.GetLocationsCallbackClient
            )

        class MetadataParams(Protocol): ...

        class MetadataCallContext(Protocol):
            params: _DatasetInterfaceModule.Server.MetadataParams
            @property
            def results(self) -> MetadataBuilder: ...

        class ClosesttimeseriesatParams(Protocol):
            latlon: LatLonCoordReader

        class ClosesttimeseriesatCallContext(Protocol):
            params: _DatasetInterfaceModule.Server.ClosesttimeseriesatParams
            @property
            def results(
                self,
            ) -> _DatasetInterfaceModule.Server.ClosesttimeseriesatResult: ...

        class TimeseriesatParams(Protocol):
            locationId: str

        class TimeseriesatCallContext(Protocol):
            params: _DatasetInterfaceModule.Server.TimeseriesatParams
            @property
            def results(self) -> _DatasetInterfaceModule.Server.TimeseriesatResult: ...

        class LocationsParams(Protocol): ...

        class LocationsCallContext(Protocol):
            params: _DatasetInterfaceModule.Server.LocationsParams
            @property
            def results(self) -> _DatasetInterfaceModule.Server.LocationsResult: ...

        class StreamlocationsParams(Protocol):
            startAfterLocationId: str

        class StreamlocationsCallContext(Protocol):
            params: _DatasetInterfaceModule.Server.StreamlocationsParams
            @property
            def results(
                self,
            ) -> _DatasetInterfaceModule.Server.StreamlocationsResult: ...

        def metadata(
            self,
            _context: _DatasetInterfaceModule.Server.MetadataCallContext,
            **kwargs: Any,
        ) -> Awaitable[_DatasetInterfaceModule.Server.MetadataResultTuple | None]: ...
        def metadata_context(
            self, context: _DatasetInterfaceModule.Server.MetadataCallContext
        ) -> Awaitable[None]: ...
        def closestTimeSeriesAt(
            self,
            latlon: LatLonCoordReader,
            _context: _DatasetInterfaceModule.Server.ClosesttimeseriesatCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            _TimeSeriesInterfaceModule.Server
            | _DatasetInterfaceModule.Server.ClosesttimeseriesatResultTuple
            | None
        ]: ...
        def closestTimeSeriesAt_context(
            self, context: _DatasetInterfaceModule.Server.ClosesttimeseriesatCallContext
        ) -> Awaitable[None]: ...
        def timeSeriesAt(
            self,
            locationId: str,
            _context: _DatasetInterfaceModule.Server.TimeseriesatCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            _TimeSeriesInterfaceModule.Server
            | _DatasetInterfaceModule.Server.TimeseriesatResultTuple
            | None
        ]: ...
        def timeSeriesAt_context(
            self, context: _DatasetInterfaceModule.Server.TimeseriesatCallContext
        ) -> Awaitable[None]: ...
        def locations(
            self,
            _context: _DatasetInterfaceModule.Server.LocationsCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            Sequence[LocationBuilder | LocationReader]
            | _DatasetInterfaceModule.Server.LocationsResultTuple
            | None
        ]: ...
        def locations_context(
            self, context: _DatasetInterfaceModule.Server.LocationsCallContext
        ) -> Awaitable[None]: ...
        def streamLocations(
            self,
            startAfterLocationId: str,
            _context: _DatasetInterfaceModule.Server.StreamlocationsCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            _DatasetInterfaceModule._GetLocationsCallbackInterfaceModule.Server
            | _DatasetInterfaceModule.Server.StreamlocationsResultTuple
            | None
        ]: ...
        def streamLocations_context(
            self, context: _DatasetInterfaceModule.Server.StreamlocationsCallContext
        ) -> Awaitable[None]: ...

    class DatasetClient(
        _IdentifiableInterfaceModule.IdentifiableClient,
        _PersistentInterfaceModule.PersistentClient,
    ):
        class MetadataResult(Awaitable[MetadataResult], Protocol):
            entries: EntryListReader
            info: _MetadataStructModule._InformationInterfaceModule.InformationClient

        class ClosesttimeseriesatResult(Awaitable[ClosesttimeseriesatResult], Protocol):
            timeSeries: _TimeSeriesInterfaceModule.TimeSeriesClient

        class TimeseriesatResult(Awaitable[TimeseriesatResult], Protocol):
            timeSeries: _TimeSeriesInterfaceModule.TimeSeriesClient

        class LocationsResult(Awaitable[LocationsResult], Protocol):
            locations: LocationListReader

        class StreamlocationsResult(Awaitable[StreamlocationsResult], Protocol):
            locationsCallback: _DatasetInterfaceModule._GetLocationsCallbackInterfaceModule.GetLocationsCallbackClient

        def metadata(self) -> _DatasetInterfaceModule.DatasetClient.MetadataResult: ...
        def closestTimeSeriesAt(
            self,
            latlon: LatLonCoordBuilder
            | LatLonCoordReader
            | dict[str, Any]
            | None = None,
        ) -> _DatasetInterfaceModule.DatasetClient.ClosesttimeseriesatResult: ...
        def timeSeriesAt(
            self, locationId: str | None = None
        ) -> _DatasetInterfaceModule.DatasetClient.TimeseriesatResult: ...
        def locations(
            self,
        ) -> _DatasetInterfaceModule.DatasetClient.LocationsResult: ...
        def streamLocations(
            self, startAfterLocationId: str | None = None
        ) -> _DatasetInterfaceModule.DatasetClient.StreamlocationsResult: ...
        def metadata_request(self) -> _DatasetInterfaceModule.MetadataRequest: ...
        def closestTimeSeriesAt_request(
            self, latlon: LatLonCoordBuilder | None = None
        ) -> _DatasetInterfaceModule.ClosesttimeseriesatRequest: ...
        def timeSeriesAt_request(
            self, locationId: str | None = None
        ) -> _DatasetInterfaceModule.TimeseriesatRequest: ...
        def locations_request(self) -> _DatasetInterfaceModule.LocationsRequest: ...
        def streamLocations_request(
            self, startAfterLocationId: str | None = None
        ) -> _DatasetInterfaceModule.StreamlocationsRequest: ...

class _TimeSeriesInterfaceModule(
    _IdentifiableInterfaceModule, _PersistentInterfaceModule
):
    class _ResolutionEnumModule:
        daily: int
        hourly: int

    Resolution: _ResolutionEnumModule
    class ResolutionRequest(Protocol):
        def send(
            self,
        ) -> _TimeSeriesInterfaceModule.TimeSeriesClient.ResolutionResult: ...

    class RangeRequest(Protocol):
        def send(self) -> _TimeSeriesInterfaceModule.TimeSeriesClient.RangeResult: ...

    class HeaderRequest(Protocol):
        def send(self) -> _TimeSeriesInterfaceModule.TimeSeriesClient.HeaderResult: ...

    class DataRequest(Protocol):
        def send(self) -> _TimeSeriesInterfaceModule.TimeSeriesClient.DataResult: ...

    class DatatRequest(Protocol):
        def send(self) -> _TimeSeriesInterfaceModule.TimeSeriesClient.DatatResult: ...

    class SubrangeRequest(Protocol):
        start: DateBuilder
        end: DateBuilder
        @overload
        def init(self, name: Literal["start"]) -> DateBuilder: ...
        @overload
        def init(self, name: Literal["end"]) -> DateBuilder: ...
        @overload
        def init(self, name: str, size: int = ...) -> Any: ...
        def send(
            self,
        ) -> _TimeSeriesInterfaceModule.TimeSeriesClient.SubrangeResult: ...

    class SubheaderRequest(Protocol):
        elements: ElementEnumListBuilder | ElementEnumListReader | Sequence[Any]
        @overload
        def init(
            self, name: Literal["elements"], size: int = ...
        ) -> ElementEnumListBuilder: ...
        @overload
        def init(self, name: str, size: int = ...) -> Any: ...
        def send(
            self,
        ) -> _TimeSeriesInterfaceModule.TimeSeriesClient.SubheaderResult: ...

    class MetadataRequest(Protocol):
        def send(
            self,
        ) -> _TimeSeriesInterfaceModule.TimeSeriesClient.MetadataResult: ...

    class LocationRequest(Protocol):
        def send(
            self,
        ) -> _TimeSeriesInterfaceModule.TimeSeriesClient.LocationResult: ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _TimeSeriesInterfaceModule.TimeSeriesClient: ...
    class Server(
        _IdentifiableInterfaceModule.Server, _PersistentInterfaceModule.Server
    ):
        class ResolutionResult(_DynamicStructBuilder):
            @property
            def resolution(self) -> TimeSeriesResolutionEnum: ...
            @resolution.setter
            def resolution(self, value: TimeSeriesResolutionEnum) -> None: ...

        class RangeResult(_DynamicStructBuilder):
            @property
            def startDate(self) -> DateBuilder: ...
            @startDate.setter
            def startDate(
                self, value: DateBuilder | DateReader | dict[str, Any]
            ) -> None: ...
            @property
            def endDate(self) -> DateBuilder: ...
            @endDate.setter
            def endDate(
                self, value: DateBuilder | DateReader | dict[str, Any]
            ) -> None: ...
            @overload
            def init(
                self, field: Literal["startDate"], size: int | None = None
            ) -> DateBuilder: ...
            @overload
            def init(
                self, field: Literal["endDate"], size: int | None = None
            ) -> DateBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...

        class HeaderResult(_DynamicStructBuilder):
            @property
            def header(self) -> ElementEnumListBuilder: ...
            @header.setter
            def header(
                self,
                value: ElementEnumListBuilder | ElementEnumListReader | Sequence[Any],
            ) -> None: ...
            @overload
            def init(
                self, field: Literal["header"], size: int | None = None
            ) -> ElementEnumListBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...

        class DataResult(_DynamicStructBuilder):
            @property
            def data(self) -> Float32ListListBuilder: ...
            @data.setter
            def data(
                self,
                value: Float32ListListBuilder | Float32ListListReader | Sequence[Any],
            ) -> None: ...
            @overload
            def init(
                self, field: Literal["data"], size: int | None = None
            ) -> Float32ListListBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...

        class DatatResult(_DynamicStructBuilder):
            @property
            def data(self) -> Float32ListListBuilder: ...
            @data.setter
            def data(
                self,
                value: Float32ListListBuilder | Float32ListListReader | Sequence[Any],
            ) -> None: ...
            @overload
            def init(
                self, field: Literal["data"], size: int | None = None
            ) -> Float32ListListBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...

        class SubrangeResult(_DynamicStructBuilder):
            @property
            def timeSeries(
                self,
            ) -> (
                _TimeSeriesInterfaceModule.Server
                | _TimeSeriesInterfaceModule.TimeSeriesClient
            ): ...
            @timeSeries.setter
            def timeSeries(
                self,
                value: _TimeSeriesInterfaceModule.Server
                | _TimeSeriesInterfaceModule.TimeSeriesClient,
            ) -> None: ...

        class SubheaderResult(_DynamicStructBuilder):
            @property
            def timeSeries(
                self,
            ) -> (
                _TimeSeriesInterfaceModule.Server
                | _TimeSeriesInterfaceModule.TimeSeriesClient
            ): ...
            @timeSeries.setter
            def timeSeries(
                self,
                value: _TimeSeriesInterfaceModule.Server
                | _TimeSeriesInterfaceModule.TimeSeriesClient,
            ) -> None: ...

        class MetadataResult(Awaitable[MetadataResult], Protocol):
            entries: EntryListBuilder | EntryListReader
            info: (
                _MetadataStructModule._InformationInterfaceModule.Server
                | _MetadataStructModule._InformationInterfaceModule.InformationClient
            )

        class LocationResult(Awaitable[LocationResult], Protocol):
            id: IdInformationBuilder | IdInformationReader
            heightNN: float
            latlon: LatLonCoordBuilder | LatLonCoordReader
            timeSeries: (
                _TimeSeriesInterfaceModule.Server
                | _TimeSeriesInterfaceModule.TimeSeriesClient
            )
            customData: KVListBuilder | KVListReader

        class ResolutionResultTuple(NamedTuple):
            resolution: TimeSeriesResolutionEnum

        class RangeResultTuple(NamedTuple):
            startDate: DateBuilder | DateReader
            endDate: DateBuilder | DateReader

        class HeaderResultTuple(NamedTuple):
            header: ElementEnumListBuilder | ElementEnumListReader

        class DataResultTuple(NamedTuple):
            data: Float32ListListBuilder | Float32ListListReader

        class DatatResultTuple(NamedTuple):
            data: Float32ListListBuilder | Float32ListListReader

        class SubrangeResultTuple(NamedTuple):
            timeSeries: (
                _TimeSeriesInterfaceModule.Server
                | _TimeSeriesInterfaceModule.TimeSeriesClient
            )

        class SubheaderResultTuple(NamedTuple):
            timeSeries: (
                _TimeSeriesInterfaceModule.Server
                | _TimeSeriesInterfaceModule.TimeSeriesClient
            )

        class MetadataResultTuple(NamedTuple):
            entries: EntryListBuilder | EntryListReader
            info: (
                _MetadataStructModule._InformationInterfaceModule.Server
                | _MetadataStructModule._InformationInterfaceModule.InformationClient
            )

        class LocationResultTuple(NamedTuple):
            id: IdInformationBuilder | IdInformationReader
            heightNN: float
            latlon: LatLonCoordBuilder | LatLonCoordReader
            timeSeries: (
                _TimeSeriesInterfaceModule.Server
                | _TimeSeriesInterfaceModule.TimeSeriesClient
            )
            customData: KVListBuilder | KVListReader

        class ResolutionParams(Protocol): ...

        class ResolutionCallContext(Protocol):
            params: _TimeSeriesInterfaceModule.Server.ResolutionParams
            @property
            def results(self) -> _TimeSeriesInterfaceModule.Server.ResolutionResult: ...

        class RangeParams(Protocol): ...

        class RangeCallContext(Protocol):
            params: _TimeSeriesInterfaceModule.Server.RangeParams
            @property
            def results(self) -> _TimeSeriesInterfaceModule.Server.RangeResult: ...

        class HeaderParams(Protocol): ...

        class HeaderCallContext(Protocol):
            params: _TimeSeriesInterfaceModule.Server.HeaderParams
            @property
            def results(self) -> _TimeSeriesInterfaceModule.Server.HeaderResult: ...

        class DataParams(Protocol): ...

        class DataCallContext(Protocol):
            params: _TimeSeriesInterfaceModule.Server.DataParams
            @property
            def results(self) -> _TimeSeriesInterfaceModule.Server.DataResult: ...

        class DatatParams(Protocol): ...

        class DatatCallContext(Protocol):
            params: _TimeSeriesInterfaceModule.Server.DatatParams
            @property
            def results(self) -> _TimeSeriesInterfaceModule.Server.DatatResult: ...

        class SubrangeParams(Protocol):
            start: DateReader
            end: DateReader

        class SubrangeCallContext(Protocol):
            params: _TimeSeriesInterfaceModule.Server.SubrangeParams
            @property
            def results(self) -> _TimeSeriesInterfaceModule.Server.SubrangeResult: ...

        class SubheaderParams(Protocol):
            elements: ElementEnumListReader

        class SubheaderCallContext(Protocol):
            params: _TimeSeriesInterfaceModule.Server.SubheaderParams
            @property
            def results(self) -> _TimeSeriesInterfaceModule.Server.SubheaderResult: ...

        class MetadataParams(Protocol): ...

        class MetadataCallContext(Protocol):
            params: _TimeSeriesInterfaceModule.Server.MetadataParams
            @property
            def results(self) -> MetadataBuilder: ...

        class LocationParams(Protocol): ...

        class LocationCallContext(Protocol):
            params: _TimeSeriesInterfaceModule.Server.LocationParams
            @property
            def results(self) -> LocationBuilder: ...

        def resolution(
            self,
            _context: _TimeSeriesInterfaceModule.Server.ResolutionCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            TimeSeriesResolutionEnum
            | _TimeSeriesInterfaceModule.Server.ResolutionResultTuple
            | None
        ]: ...
        def resolution_context(
            self, context: _TimeSeriesInterfaceModule.Server.ResolutionCallContext
        ) -> Awaitable[None]: ...
        def range(
            self,
            _context: _TimeSeriesInterfaceModule.Server.RangeCallContext,
            **kwargs: Any,
        ) -> Awaitable[_TimeSeriesInterfaceModule.Server.RangeResultTuple | None]: ...
        def range_context(
            self, context: _TimeSeriesInterfaceModule.Server.RangeCallContext
        ) -> Awaitable[None]: ...
        def header(
            self,
            _context: _TimeSeriesInterfaceModule.Server.HeaderCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            Sequence[ElementEnum]
            | _TimeSeriesInterfaceModule.Server.HeaderResultTuple
            | None
        ]: ...
        def header_context(
            self, context: _TimeSeriesInterfaceModule.Server.HeaderCallContext
        ) -> Awaitable[None]: ...
        def data(
            self,
            _context: _TimeSeriesInterfaceModule.Server.DataCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            Sequence[Sequence[float]]
            | _TimeSeriesInterfaceModule.Server.DataResultTuple
            | None
        ]: ...
        def data_context(
            self, context: _TimeSeriesInterfaceModule.Server.DataCallContext
        ) -> Awaitable[None]: ...
        def dataT(
            self,
            _context: _TimeSeriesInterfaceModule.Server.DatatCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            Sequence[Sequence[float]]
            | _TimeSeriesInterfaceModule.Server.DatatResultTuple
            | None
        ]: ...
        def dataT_context(
            self, context: _TimeSeriesInterfaceModule.Server.DatatCallContext
        ) -> Awaitable[None]: ...
        def subrange(
            self,
            start: DateReader,
            end: DateReader,
            _context: _TimeSeriesInterfaceModule.Server.SubrangeCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            _TimeSeriesInterfaceModule.Server
            | _TimeSeriesInterfaceModule.Server.SubrangeResultTuple
            | None
        ]: ...
        def subrange_context(
            self, context: _TimeSeriesInterfaceModule.Server.SubrangeCallContext
        ) -> Awaitable[None]: ...
        def subheader(
            self,
            elements: ElementEnumListReader,
            _context: _TimeSeriesInterfaceModule.Server.SubheaderCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            _TimeSeriesInterfaceModule.Server
            | _TimeSeriesInterfaceModule.Server.SubheaderResultTuple
            | None
        ]: ...
        def subheader_context(
            self, context: _TimeSeriesInterfaceModule.Server.SubheaderCallContext
        ) -> Awaitable[None]: ...
        def metadata(
            self,
            _context: _TimeSeriesInterfaceModule.Server.MetadataCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            _TimeSeriesInterfaceModule.Server.MetadataResultTuple | None
        ]: ...
        def metadata_context(
            self, context: _TimeSeriesInterfaceModule.Server.MetadataCallContext
        ) -> Awaitable[None]: ...
        def location(
            self,
            _context: _TimeSeriesInterfaceModule.Server.LocationCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            _TimeSeriesInterfaceModule.Server.LocationResultTuple | None
        ]: ...
        def location_context(
            self, context: _TimeSeriesInterfaceModule.Server.LocationCallContext
        ) -> Awaitable[None]: ...

    class TimeSeriesClient(
        _IdentifiableInterfaceModule.IdentifiableClient,
        _PersistentInterfaceModule.PersistentClient,
    ):
        class ResolutionResult(Awaitable[ResolutionResult], Protocol):
            resolution: TimeSeriesResolutionEnum

        class RangeResult(Awaitable[RangeResult], Protocol):
            startDate: DateReader
            endDate: DateReader

        class HeaderResult(Awaitable[HeaderResult], Protocol):
            header: ElementEnumListReader

        class DataResult(Awaitable[DataResult], Protocol):
            data: Float32ListListReader

        class DatatResult(Awaitable[DatatResult], Protocol):
            data: Float32ListListReader

        class SubrangeResult(Awaitable[SubrangeResult], Protocol):
            timeSeries: _TimeSeriesInterfaceModule.TimeSeriesClient

        class SubheaderResult(Awaitable[SubheaderResult], Protocol):
            timeSeries: _TimeSeriesInterfaceModule.TimeSeriesClient

        class MetadataResult(Awaitable[MetadataResult], Protocol):
            entries: EntryListReader
            info: _MetadataStructModule._InformationInterfaceModule.InformationClient

        class LocationResult(Awaitable[LocationResult], Protocol):
            id: IdInformationReader
            heightNN: float
            latlon: LatLonCoordReader
            timeSeries: _TimeSeriesInterfaceModule.TimeSeriesClient
            customData: KVListReader

        def resolution(
            self,
        ) -> _TimeSeriesInterfaceModule.TimeSeriesClient.ResolutionResult: ...
        def range(self) -> _TimeSeriesInterfaceModule.TimeSeriesClient.RangeResult: ...
        def header(
            self,
        ) -> _TimeSeriesInterfaceModule.TimeSeriesClient.HeaderResult: ...
        def data(self) -> _TimeSeriesInterfaceModule.TimeSeriesClient.DataResult: ...
        def dataT(self) -> _TimeSeriesInterfaceModule.TimeSeriesClient.DatatResult: ...
        def subrange(
            self,
            start: DateBuilder | DateReader | dict[str, Any] | None = None,
            end: DateBuilder | DateReader | dict[str, Any] | None = None,
        ) -> _TimeSeriesInterfaceModule.TimeSeriesClient.SubrangeResult: ...
        def subheader(
            self,
            elements: ElementEnumListBuilder
            | ElementEnumListReader
            | Sequence[Any]
            | None = None,
        ) -> _TimeSeriesInterfaceModule.TimeSeriesClient.SubheaderResult: ...
        def metadata(
            self,
        ) -> _TimeSeriesInterfaceModule.TimeSeriesClient.MetadataResult: ...
        def location(
            self,
        ) -> _TimeSeriesInterfaceModule.TimeSeriesClient.LocationResult: ...
        def resolution_request(
            self,
        ) -> _TimeSeriesInterfaceModule.ResolutionRequest: ...
        def range_request(self) -> _TimeSeriesInterfaceModule.RangeRequest: ...
        def header_request(self) -> _TimeSeriesInterfaceModule.HeaderRequest: ...
        def data_request(self) -> _TimeSeriesInterfaceModule.DataRequest: ...
        def dataT_request(self) -> _TimeSeriesInterfaceModule.DatatRequest: ...
        def subrange_request(
            self, start: DateBuilder | None = None, end: DateBuilder | None = None
        ) -> _TimeSeriesInterfaceModule.SubrangeRequest: ...
        def subheader_request(
            self,
            elements: ElementEnumListBuilder
            | ElementEnumListReader
            | Sequence[Any]
            | None = None,
        ) -> _TimeSeriesInterfaceModule.SubheaderRequest: ...
        def metadata_request(self) -> _TimeSeriesInterfaceModule.MetadataRequest: ...
        def location_request(self) -> _TimeSeriesInterfaceModule.LocationRequest: ...

class _ElementEnumModule:
    tmin: int
    tavg: int
    tmax: int
    precip: int
    globrad: int
    wind: int
    sunhours: int
    cloudamount: int
    relhumid: int
    airpress: int
    vaporpress: int
    co2: int
    o3: int
    et0: int
    dewpointTemp: int
    specificHumidity: int
    snowfallFlux: int
    surfaceDownwellingLongwaveRadiation: int
    potET: int

class _ElementEnumList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> ElementEnum: ...
        @override
        def __iter__(self) -> Iterator[ElementEnum]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> ElementEnum: ...
        @override
        def __setitem__(self, key: int, value: ElementEnum) -> None: ...
        @override
        def __iter__(self) -> Iterator[ElementEnum]: ...

class _Float32List:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> float: ...
        @override
        def __iter__(self) -> Iterator[float]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> float: ...
        @override
        def __setitem__(self, key: int, value: float) -> None: ...
        @override
        def __iter__(self) -> Iterator[float]: ...

class _Float32ListList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> Float32ListReader: ...
        @override
        def __iter__(self) -> Iterator[Float32ListReader]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> Float32ListBuilder: ...
        @override
        def __setitem__(
            self,
            key: int,
            value: Float32ListReader | Float32ListBuilder | Sequence[Any],
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[Float32ListBuilder]: ...
        @override
        def init(self, index: int, size: int | None = None) -> Float32ListBuilder: ...

class _KVList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> KVReader: ...
        @override
        def __iter__(self) -> Iterator[KVReader]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> KVBuilder: ...
        @override
        def __setitem__(
            self, key: int, value: KVReader | KVBuilder | dict[str, Any]
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[KVBuilder]: ...
        @override
        def init(self, index: int, size: int | None = None) -> KVBuilder: ...

TimeSeries: _TimeSeriesInterfaceModule

class _LocationStructModule(_StructModule):
    class _KVStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def key(self) -> str: ...
            @property
            def value(self) -> _DynamicObjectReader: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> KVBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def key(self) -> str: ...
            @key.setter
            def key(self, value: str) -> None: ...
            @property
            def value(self) -> _DynamicObjectBuilder: ...
            @value.setter
            def value(self, value: AnyPointer) -> None: ...
            @override
            def as_reader(self) -> KVReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            key: str | None = None,
            value: AnyPointer | None = None,
            **kwargs: Any,
        ) -> KVBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[KVReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[KVReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[KVBuilder]: ...
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
        ) -> KVReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> KVReader: ...

    type KVReader = _KVStructModule.Reader
    type KVBuilder = _KVStructModule.Builder
    KV: _KVStructModule
    class Reader(_DynamicStructReader):
        @property
        def id(self) -> IdInformationReader: ...
        @property
        def heightNN(self) -> float: ...
        @property
        def latlon(self) -> LatLonCoordReader: ...
        @property
        def timeSeries(self) -> _TimeSeriesInterfaceModule.TimeSeriesClient: ...
        @property
        def customData(self) -> KVListReader: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> LocationBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def id(self) -> IdInformationBuilder: ...
        @id.setter
        def id(
            self, value: IdInformationBuilder | IdInformationReader | dict[str, Any]
        ) -> None: ...
        @property
        def heightNN(self) -> float: ...
        @heightNN.setter
        def heightNN(self, value: float) -> None: ...
        @property
        def latlon(self) -> LatLonCoordBuilder: ...
        @latlon.setter
        def latlon(
            self, value: LatLonCoordBuilder | LatLonCoordReader | dict[str, Any]
        ) -> None: ...
        @property
        def timeSeries(self) -> _TimeSeriesInterfaceModule.TimeSeriesClient: ...
        @timeSeries.setter
        def timeSeries(
            self,
            value: _TimeSeriesInterfaceModule.TimeSeriesClient
            | _TimeSeriesInterfaceModule.Server,
        ) -> None: ...
        @property
        def customData(self) -> KVListBuilder: ...
        @customData.setter
        def customData(
            self, value: KVListBuilder | KVListReader | dict[str, Any]
        ) -> None: ...
        @override
        @overload
        def init(
            self, field: Literal["id"], size: int | None = None
        ) -> IdInformationBuilder: ...
        @overload
        def init(
            self, field: Literal["latlon"], size: int | None = None
        ) -> LatLonCoordBuilder: ...
        @overload
        def init(
            self, field: Literal["customData"], size: int | None = None
        ) -> KVListBuilder: ...
        @overload
        def init(self, field: str, size: int | None = None) -> Any: ...
        @override
        def as_reader(self) -> LocationReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        id: IdInformationBuilder | dict[str, Any] | None = None,
        heightNN: float | None = None,
        latlon: LatLonCoordBuilder | dict[str, Any] | None = None,
        timeSeries: _TimeSeriesInterfaceModule.TimeSeriesClient
        | _TimeSeriesInterfaceModule.Server
        | None = None,
        customData: KVListBuilder | dict[str, Any] | None = None,
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

Location: _LocationStructModule

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

Dataset: _DatasetInterfaceModule

class _MetaPlusDataStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def meta(self) -> MetadataReader: ...
        @property
        def data(self) -> _DatasetInterfaceModule.DatasetClient: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> MetaPlusDataBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def meta(self) -> MetadataBuilder: ...
        @meta.setter
        def meta(
            self, value: MetadataBuilder | MetadataReader | dict[str, Any]
        ) -> None: ...
        @property
        def data(self) -> _DatasetInterfaceModule.DatasetClient: ...
        @data.setter
        def data(
            self,
            value: _DatasetInterfaceModule.DatasetClient
            | _DatasetInterfaceModule.Server,
        ) -> None: ...
        @override
        def init(
            self, field: Literal["meta"], size: int | None = None
        ) -> MetadataBuilder: ...
        @override
        def as_reader(self) -> MetaPlusDataReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        meta: MetadataBuilder | dict[str, Any] | None = None,
        data: _DatasetInterfaceModule.DatasetClient
        | _DatasetInterfaceModule.Server
        | None = None,
        **kwargs: Any,
    ) -> MetaPlusDataBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[MetaPlusDataReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[MetaPlusDataReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[MetaPlusDataBuilder]: ...
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
    ) -> MetaPlusDataReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> MetaPlusDataReader: ...

MetaPlusData: _MetaPlusDataStructModule

class _TimeSeriesDataStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def data(self) -> Float32ListListReader: ...
        @property
        def isTransposed(self) -> bool: ...
        @property
        def header(self) -> ElementEnumListReader: ...
        @property
        def startDate(self) -> DateReader: ...
        @property
        def endDate(self) -> DateReader: ...
        @property
        def resolution(self) -> TimeSeriesResolutionEnum: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> TimeSeriesDataBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def data(self) -> Float32ListListBuilder: ...
        @data.setter
        def data(
            self, value: Float32ListListBuilder | Float32ListListReader | dict[str, Any]
        ) -> None: ...
        @property
        def isTransposed(self) -> bool: ...
        @isTransposed.setter
        def isTransposed(self, value: bool) -> None: ...
        @property
        def header(self) -> ElementEnumListBuilder: ...
        @header.setter
        def header(
            self, value: ElementEnumListBuilder | ElementEnumListReader | dict[str, Any]
        ) -> None: ...
        @property
        def startDate(self) -> DateBuilder: ...
        @startDate.setter
        def startDate(
            self, value: DateBuilder | DateReader | dict[str, Any]
        ) -> None: ...
        @property
        def endDate(self) -> DateBuilder: ...
        @endDate.setter
        def endDate(self, value: DateBuilder | DateReader | dict[str, Any]) -> None: ...
        @property
        def resolution(self) -> TimeSeriesResolutionEnum: ...
        @resolution.setter
        def resolution(self, value: TimeSeriesResolutionEnum) -> None: ...
        @override
        @overload
        def init(
            self, field: Literal["startDate"], size: int | None = None
        ) -> DateBuilder: ...
        @overload
        def init(
            self, field: Literal["endDate"], size: int | None = None
        ) -> DateBuilder: ...
        @overload
        def init(
            self, field: Literal["data"], size: int | None = None
        ) -> Float32ListListBuilder: ...
        @overload
        def init(
            self, field: Literal["header"], size: int | None = None
        ) -> ElementEnumListBuilder: ...
        @overload
        def init(self, field: str, size: int | None = None) -> Any: ...
        @override
        def as_reader(self) -> TimeSeriesDataReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        data: Float32ListListBuilder | dict[str, Any] | None = None,
        isTransposed: bool | None = None,
        header: ElementEnumListBuilder | dict[str, Any] | None = None,
        startDate: DateBuilder | dict[str, Any] | None = None,
        endDate: DateBuilder | dict[str, Any] | None = None,
        resolution: TimeSeriesResolutionEnum | None = None,
        **kwargs: Any,
    ) -> TimeSeriesDataBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[TimeSeriesDataReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[TimeSeriesDataReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[TimeSeriesDataBuilder]: ...
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
    ) -> TimeSeriesDataReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> TimeSeriesDataReader: ...

TimeSeriesData: _TimeSeriesDataStructModule

class _ServiceInterfaceModule(_IdentifiableInterfaceModule, _PersistentInterfaceModule):
    class GetavailabledatasetsRequest(Protocol):
        def send(
            self,
        ) -> _ServiceInterfaceModule.ServiceClient.GetavailabledatasetsResult: ...

    class GetdatasetsforRequest(Protocol):
        template: MetadataBuilder
        @overload
        def init(self, name: Literal["template"]) -> MetadataBuilder: ...
        @overload
        def init(self, name: str, size: int = ...) -> Any: ...
        def send(
            self,
        ) -> _ServiceInterfaceModule.ServiceClient.GetdatasetsforResult: ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _ServiceInterfaceModule.ServiceClient: ...
    class Server(
        _IdentifiableInterfaceModule.Server, _PersistentInterfaceModule.Server
    ):
        class GetavailabledatasetsResult(_DynamicStructBuilder):
            @property
            def datasets(self) -> MetaPlusDataListBuilder: ...
            @datasets.setter
            def datasets(
                self,
                value: MetaPlusDataListBuilder | MetaPlusDataListReader | Sequence[Any],
            ) -> None: ...
            @overload
            def init(
                self, field: Literal["datasets"], size: int | None = None
            ) -> MetaPlusDataListBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...

        class GetdatasetsforResult(_DynamicStructBuilder):
            @property
            def datasets(self) -> DatasetClientListBuilder: ...
            @datasets.setter
            def datasets(
                self,
                value: DatasetClientListBuilder
                | DatasetClientListReader
                | Sequence[Any],
            ) -> None: ...
            @overload
            def init(
                self, field: Literal["datasets"], size: int | None = None
            ) -> DatasetClientListBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...

        class GetavailabledatasetsResultTuple(NamedTuple):
            datasets: MetaPlusDataListBuilder | MetaPlusDataListReader

        class GetdatasetsforResultTuple(NamedTuple):
            datasets: DatasetClientListBuilder | DatasetClientListReader

        class GetavailabledatasetsParams(Protocol): ...

        class GetavailabledatasetsCallContext(Protocol):
            params: _ServiceInterfaceModule.Server.GetavailabledatasetsParams
            @property
            def results(
                self,
            ) -> _ServiceInterfaceModule.Server.GetavailabledatasetsResult: ...

        class GetdatasetsforParams(Protocol):
            template: MetadataReader

        class GetdatasetsforCallContext(Protocol):
            params: _ServiceInterfaceModule.Server.GetdatasetsforParams
            @property
            def results(
                self,
            ) -> _ServiceInterfaceModule.Server.GetdatasetsforResult: ...

        def getAvailableDatasets(
            self,
            _context: _ServiceInterfaceModule.Server.GetavailabledatasetsCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            Sequence[MetaPlusDataBuilder | MetaPlusDataReader]
            | _ServiceInterfaceModule.Server.GetavailabledatasetsResultTuple
            | None
        ]: ...
        def getAvailableDatasets_context(
            self,
            context: _ServiceInterfaceModule.Server.GetavailabledatasetsCallContext,
        ) -> Awaitable[None]: ...
        def getDatasetsFor(
            self,
            template: MetadataReader,
            _context: _ServiceInterfaceModule.Server.GetdatasetsforCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            Sequence[_DatasetInterfaceModule]
            | _ServiceInterfaceModule.Server.GetdatasetsforResultTuple
            | None
        ]: ...
        def getDatasetsFor_context(
            self, context: _ServiceInterfaceModule.Server.GetdatasetsforCallContext
        ) -> Awaitable[None]: ...

    class ServiceClient(
        _IdentifiableInterfaceModule.IdentifiableClient,
        _PersistentInterfaceModule.PersistentClient,
    ):
        class GetavailabledatasetsResult(
            Awaitable[GetavailabledatasetsResult], Protocol
        ):
            datasets: MetaPlusDataListReader

        class GetdatasetsforResult(Awaitable[GetdatasetsforResult], Protocol):
            datasets: DatasetClientListReader

        def getAvailableDatasets(
            self,
        ) -> _ServiceInterfaceModule.ServiceClient.GetavailabledatasetsResult: ...
        def getDatasetsFor(
            self,
            template: MetadataBuilder | MetadataReader | dict[str, Any] | None = None,
        ) -> _ServiceInterfaceModule.ServiceClient.GetdatasetsforResult: ...
        def getAvailableDatasets_request(
            self,
        ) -> _ServiceInterfaceModule.GetavailabledatasetsRequest: ...
        def getDatasetsFor_request(
            self, template: MetadataBuilder | None = None
        ) -> _ServiceInterfaceModule.GetdatasetsforRequest: ...

class _MetaPlusDataList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> MetaPlusDataReader: ...
        @override
        def __iter__(self) -> Iterator[MetaPlusDataReader]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> MetaPlusDataBuilder: ...
        @override
        def __setitem__(
            self,
            key: int,
            value: MetaPlusDataReader | MetaPlusDataBuilder | dict[str, Any],
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[MetaPlusDataBuilder]: ...
        @override
        def init(self, index: int, size: int | None = None) -> MetaPlusDataBuilder: ...

class _DatasetClientList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> DatasetClient: ...
        @override
        def __iter__(self) -> Iterator[DatasetClient]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> DatasetClient: ...
        @override
        def __setitem__(
            self, key: int, value: DatasetClient | _DatasetInterfaceModule.Server
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[DatasetClient]: ...

Service: _ServiceInterfaceModule

class _CSVTimeSeriesFactoryInterfaceModule(_IdentifiableInterfaceModule):
    class _CSVConfigStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def sep(self) -> str: ...
            @property
            def headerMap(self) -> PairListReader: ...
            @property
            def skipLinesToHeader(self) -> int: ...
            @property
            def skipLinesFromHeaderToData(self) -> int: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> CSVConfigBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def sep(self) -> str: ...
            @sep.setter
            def sep(self, value: str) -> None: ...
            @property
            def headerMap(self) -> PairListBuilder: ...
            @headerMap.setter
            def headerMap(
                self, value: PairListBuilder | PairListReader | dict[str, Any]
            ) -> None: ...
            @property
            def skipLinesToHeader(self) -> int: ...
            @skipLinesToHeader.setter
            def skipLinesToHeader(self, value: int) -> None: ...
            @property
            def skipLinesFromHeaderToData(self) -> int: ...
            @skipLinesFromHeaderToData.setter
            def skipLinesFromHeaderToData(self, value: int) -> None: ...
            @override
            def init(
                self, field: Literal["headerMap"], size: int | None = None
            ) -> PairListBuilder: ...
            @override
            def as_reader(self) -> CSVConfigReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            sep: str | None = None,
            headerMap: PairListBuilder | dict[str, Any] | None = None,
            skipLinesToHeader: int | None = None,
            skipLinesFromHeaderToData: int | None = None,
            **kwargs: Any,
        ) -> CSVConfigBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[CSVConfigReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[CSVConfigReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[CSVConfigBuilder]: ...
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
        ) -> CSVConfigReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> CSVConfigReader: ...

    type CSVConfigReader = _CSVConfigStructModule.Reader
    type CSVConfigBuilder = _CSVConfigStructModule.Builder
    CSVConfig: _CSVConfigStructModule
    class CreateRequest(Protocol):
        csvData: str
        config: CSVConfigBuilder
        @overload
        def init(self, name: Literal["config"]) -> CSVConfigBuilder: ...
        @overload
        def init(self, name: str, size: int = ...) -> Any: ...
        def send(
            self,
        ) -> (
            _CSVTimeSeriesFactoryInterfaceModule.CSVTimeSeriesFactoryClient.CreateResult
        ): ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _CSVTimeSeriesFactoryInterfaceModule.CSVTimeSeriesFactoryClient: ...
    class Server(_IdentifiableInterfaceModule.Server):
        class CreateResult(_DynamicStructBuilder):
            @property
            def timeseries(
                self,
            ) -> (
                _TimeSeriesInterfaceModule.Server
                | _TimeSeriesInterfaceModule.TimeSeriesClient
            ): ...
            @timeseries.setter
            def timeseries(
                self,
                value: _TimeSeriesInterfaceModule.Server
                | _TimeSeriesInterfaceModule.TimeSeriesClient,
            ) -> None: ...
            @property
            def error(self) -> str: ...
            @error.setter
            def error(self, value: str) -> None: ...

        class CreateResultTuple(NamedTuple):
            timeseries: (
                _TimeSeriesInterfaceModule.Server
                | _TimeSeriesInterfaceModule.TimeSeriesClient
            )
            error: str

        class CreateParams(Protocol):
            csvData: str
            config: CSVConfigReader

        class CreateCallContext(Protocol):
            params: _CSVTimeSeriesFactoryInterfaceModule.Server.CreateParams
            @property
            def results(
                self,
            ) -> _CSVTimeSeriesFactoryInterfaceModule.Server.CreateResult: ...

        def create(
            self,
            csvData: str,
            config: CSVConfigReader,
            _context: _CSVTimeSeriesFactoryInterfaceModule.Server.CreateCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            _CSVTimeSeriesFactoryInterfaceModule.Server.CreateResultTuple | None
        ]: ...
        def create_context(
            self, context: _CSVTimeSeriesFactoryInterfaceModule.Server.CreateCallContext
        ) -> Awaitable[None]: ...

    class CSVTimeSeriesFactoryClient(_IdentifiableInterfaceModule.IdentifiableClient):
        class CreateResult(Awaitable[CreateResult], Protocol):
            timeseries: _TimeSeriesInterfaceModule.TimeSeriesClient
            error: str

        def create(
            self,
            csvData: str | None = None,
            config: CSVConfigBuilder | CSVConfigReader | dict[str, Any] | None = None,
        ) -> (
            _CSVTimeSeriesFactoryInterfaceModule.CSVTimeSeriesFactoryClient.CreateResult
        ): ...
        def create_request(
            self, csvData: str | None = None, config: CSVConfigBuilder | None = None
        ) -> _CSVTimeSeriesFactoryInterfaceModule.CreateRequest: ...

CSVTimeSeriesFactory: _CSVTimeSeriesFactoryInterfaceModule

class _AlterTimeSeriesWrapperInterfaceModule(_TimeSeriesInterfaceModule):
    class _AlterTypeEnumModule:
        add: int
        mul: int

    AlterType: _AlterTypeEnumModule
    class _AlteredStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def element(self) -> ElementEnum: ...
            @property
            def value(self) -> float: ...
            @property
            def type(self) -> AlterTimeSeriesWrapperAlterTypeEnum: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> AlteredBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def element(self) -> ElementEnum: ...
            @element.setter
            def element(self, value: ElementEnum) -> None: ...
            @property
            def value(self) -> float: ...
            @value.setter
            def value(self, value: float) -> None: ...
            @property
            def type(self) -> AlterTimeSeriesWrapperAlterTypeEnum: ...
            @type.setter
            def type(self, value: AlterTimeSeriesWrapperAlterTypeEnum) -> None: ...
            @override
            def as_reader(self) -> AlteredReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            element: ElementEnum | None = None,
            value: float | None = None,
            type: AlterTimeSeriesWrapperAlterTypeEnum | None = None,
            **kwargs: Any,
        ) -> AlteredBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[AlteredReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[AlteredReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[AlteredBuilder]: ...
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
        ) -> AlteredReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AlteredReader: ...

    type AlteredReader = _AlteredStructModule.Reader
    type AlteredBuilder = _AlteredStructModule.Builder
    Altered: _AlteredStructModule
    class WrappedtimeseriesRequest(Protocol):
        def send(
            self,
        ) -> _AlterTimeSeriesWrapperInterfaceModule.AlterTimeSeriesWrapperClient.WrappedtimeseriesResult: ...

    class AlteredelementsRequest(Protocol):
        def send(
            self,
        ) -> _AlterTimeSeriesWrapperInterfaceModule.AlterTimeSeriesWrapperClient.AlteredelementsResult: ...

    class AlterRequest(Protocol):
        desc: AlteredBuilder
        asNewTimeSeries: bool
        @overload
        def init(self, name: Literal["desc"]) -> AlteredBuilder: ...
        @overload
        def init(self, name: str, size: int = ...) -> Any: ...
        def send(
            self,
        ) -> _AlterTimeSeriesWrapperInterfaceModule.AlterTimeSeriesWrapperClient.AlterResult: ...

    class RemoveRequest(Protocol):
        alteredElement: ElementEnum
        def send(
            self,
        ) -> _AlterTimeSeriesWrapperInterfaceModule.AlterTimeSeriesWrapperClient.RemoveResult: ...

    class ReplacewrappedtimeseriesRequest(Protocol):
        timeSeries: TimeSeriesClient | _TimeSeriesInterfaceModule.Server
        def send(
            self,
        ) -> _AlterTimeSeriesWrapperInterfaceModule.AlterTimeSeriesWrapperClient.ReplacewrappedtimeseriesResult: ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _AlterTimeSeriesWrapperInterfaceModule.AlterTimeSeriesWrapperClient: ...
    class Server(_TimeSeriesInterfaceModule.Server):
        class WrappedtimeseriesResult(_DynamicStructBuilder):
            @property
            def timeSeries(
                self,
            ) -> (
                _TimeSeriesInterfaceModule.Server
                | _TimeSeriesInterfaceModule.TimeSeriesClient
            ): ...
            @timeSeries.setter
            def timeSeries(
                self,
                value: _TimeSeriesInterfaceModule.Server
                | _TimeSeriesInterfaceModule.TimeSeriesClient,
            ) -> None: ...

        class AlteredelementsResult(_DynamicStructBuilder):
            @property
            def list(self) -> AlteredListBuilder: ...
            @list.setter
            def list(
                self, value: AlteredListBuilder | AlteredListReader | Sequence[Any]
            ) -> None: ...
            @overload
            def init(
                self, field: Literal["list"], size: int | None = None
            ) -> AlteredListBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...

        class AlterResult(_DynamicStructBuilder):
            @property
            def timeSeries(
                self,
            ) -> (
                _TimeSeriesInterfaceModule.Server
                | _TimeSeriesInterfaceModule.TimeSeriesClient
            ): ...
            @timeSeries.setter
            def timeSeries(
                self,
                value: _TimeSeriesInterfaceModule.Server
                | _TimeSeriesInterfaceModule.TimeSeriesClient,
            ) -> None: ...

        class RemoveResult(Awaitable[None], Protocol): ...
        class ReplacewrappedtimeseriesResult(Awaitable[None], Protocol): ...

        class WrappedtimeseriesResultTuple(NamedTuple):
            timeSeries: (
                _TimeSeriesInterfaceModule.Server
                | _TimeSeriesInterfaceModule.TimeSeriesClient
            )

        class AlteredelementsResultTuple(NamedTuple):
            list: AlteredListBuilder | AlteredListReader

        class AlterResultTuple(NamedTuple):
            timeSeries: (
                _TimeSeriesInterfaceModule.Server
                | _TimeSeriesInterfaceModule.TimeSeriesClient
            )

        class WrappedtimeseriesParams(Protocol): ...

        class WrappedtimeseriesCallContext(Protocol):
            params: (
                _AlterTimeSeriesWrapperInterfaceModule.Server.WrappedtimeseriesParams
            )
            @property
            def results(
                self,
            ) -> (
                _AlterTimeSeriesWrapperInterfaceModule.Server.WrappedtimeseriesResult
            ): ...

        class AlteredelementsParams(Protocol): ...

        class AlteredelementsCallContext(Protocol):
            params: _AlterTimeSeriesWrapperInterfaceModule.Server.AlteredelementsParams
            @property
            def results(
                self,
            ) -> (
                _AlterTimeSeriesWrapperInterfaceModule.Server.AlteredelementsResult
            ): ...

        class AlterParams(Protocol):
            desc: AlteredReader
            asNewTimeSeries: bool

        class AlterCallContext(Protocol):
            params: _AlterTimeSeriesWrapperInterfaceModule.Server.AlterParams
            @property
            def results(
                self,
            ) -> _AlterTimeSeriesWrapperInterfaceModule.Server.AlterResult: ...

        class RemoveParams(Protocol):
            alteredElement: ElementEnum

        class RemoveCallContext(Protocol):
            params: _AlterTimeSeriesWrapperInterfaceModule.Server.RemoveParams

        class ReplacewrappedtimeseriesParams(Protocol):
            timeSeries: TimeSeriesClient

        class ReplacewrappedtimeseriesCallContext(Protocol):
            params: _AlterTimeSeriesWrapperInterfaceModule.Server.ReplacewrappedtimeseriesParams

        def wrappedTimeSeries(
            self,
            _context: _AlterTimeSeriesWrapperInterfaceModule.Server.WrappedtimeseriesCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            _TimeSeriesInterfaceModule.Server
            | _AlterTimeSeriesWrapperInterfaceModule.Server.WrappedtimeseriesResultTuple
            | None
        ]: ...
        def wrappedTimeSeries_context(
            self,
            context: _AlterTimeSeriesWrapperInterfaceModule.Server.WrappedtimeseriesCallContext,
        ) -> Awaitable[None]: ...
        def alteredElements(
            self,
            _context: _AlterTimeSeriesWrapperInterfaceModule.Server.AlteredelementsCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            Sequence[AlteredBuilder | AlteredReader]
            | _AlterTimeSeriesWrapperInterfaceModule.Server.AlteredelementsResultTuple
            | None
        ]: ...
        def alteredElements_context(
            self,
            context: _AlterTimeSeriesWrapperInterfaceModule.Server.AlteredelementsCallContext,
        ) -> Awaitable[None]: ...
        def alter(
            self,
            desc: AlteredReader,
            asNewTimeSeries: bool,
            _context: _AlterTimeSeriesWrapperInterfaceModule.Server.AlterCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            _TimeSeriesInterfaceModule.Server
            | _AlterTimeSeriesWrapperInterfaceModule.Server.AlterResultTuple
            | None
        ]: ...
        def alter_context(
            self,
            context: _AlterTimeSeriesWrapperInterfaceModule.Server.AlterCallContext,
        ) -> Awaitable[None]: ...
        def remove(
            self,
            alteredElement: ElementEnum,
            _context: _AlterTimeSeriesWrapperInterfaceModule.Server.RemoveCallContext,
            **kwargs: Any,
        ) -> Awaitable[None]: ...
        def remove_context(
            self,
            context: _AlterTimeSeriesWrapperInterfaceModule.Server.RemoveCallContext,
        ) -> Awaitable[None]: ...
        def replaceWrappedTimeSeries(
            self,
            timeSeries: TimeSeriesClient,
            _context: _AlterTimeSeriesWrapperInterfaceModule.Server.ReplacewrappedtimeseriesCallContext,
            **kwargs: Any,
        ) -> Awaitable[None]: ...
        def replaceWrappedTimeSeries_context(
            self,
            context: _AlterTimeSeriesWrapperInterfaceModule.Server.ReplacewrappedtimeseriesCallContext,
        ) -> Awaitable[None]: ...

    class AlterTimeSeriesWrapperClient(_TimeSeriesInterfaceModule.TimeSeriesClient):
        class WrappedtimeseriesResult(Awaitable[WrappedtimeseriesResult], Protocol):
            timeSeries: _TimeSeriesInterfaceModule.TimeSeriesClient

        class AlteredelementsResult(Awaitable[AlteredelementsResult], Protocol):
            list: AlteredListReader

        class AlterResult(Awaitable[AlterResult], Protocol):
            timeSeries: _TimeSeriesInterfaceModule.TimeSeriesClient

        class RemoveResult(Awaitable[None], Protocol): ...
        class ReplacewrappedtimeseriesResult(Awaitable[None], Protocol): ...

        def wrappedTimeSeries(
            self,
        ) -> _AlterTimeSeriesWrapperInterfaceModule.AlterTimeSeriesWrapperClient.WrappedtimeseriesResult: ...
        def alteredElements(
            self,
        ) -> _AlterTimeSeriesWrapperInterfaceModule.AlterTimeSeriesWrapperClient.AlteredelementsResult: ...
        def alter(
            self,
            desc: AlteredBuilder | AlteredReader | dict[str, Any] | None = None,
            asNewTimeSeries: bool | None = None,
        ) -> _AlterTimeSeriesWrapperInterfaceModule.AlterTimeSeriesWrapperClient.AlterResult: ...
        def remove(
            self, alteredElement: ElementEnum | None = None
        ) -> _AlterTimeSeriesWrapperInterfaceModule.AlterTimeSeriesWrapperClient.RemoveResult: ...
        def replaceWrappedTimeSeries(
            self,
            timeSeries: TimeSeriesClient
            | _TimeSeriesInterfaceModule.Server
            | None = None,
        ) -> _AlterTimeSeriesWrapperInterfaceModule.AlterTimeSeriesWrapperClient.ReplacewrappedtimeseriesResult: ...
        def wrappedTimeSeries_request(
            self,
        ) -> _AlterTimeSeriesWrapperInterfaceModule.WrappedtimeseriesRequest: ...
        def alteredElements_request(
            self,
        ) -> _AlterTimeSeriesWrapperInterfaceModule.AlteredelementsRequest: ...
        def alter_request(
            self,
            desc: AlteredBuilder | None = None,
            asNewTimeSeries: bool | None = None,
        ) -> _AlterTimeSeriesWrapperInterfaceModule.AlterRequest: ...
        def remove_request(
            self, alteredElement: ElementEnum | None = None
        ) -> _AlterTimeSeriesWrapperInterfaceModule.RemoveRequest: ...
        def replaceWrappedTimeSeries_request(
            self,
            timeSeries: TimeSeriesClient
            | _TimeSeriesInterfaceModule.Server
            | None = None,
        ) -> _AlterTimeSeriesWrapperInterfaceModule.ReplacewrappedtimeseriesRequest: ...

class _AlteredList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> AlteredReader: ...
        @override
        def __iter__(self) -> Iterator[AlteredReader]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> AlteredBuilder: ...
        @override
        def __setitem__(
            self, key: int, value: AlteredReader | AlteredBuilder | dict[str, Any]
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[AlteredBuilder]: ...
        @override
        def init(self, index: int, size: int | None = None) -> AlteredBuilder: ...

AlterTimeSeriesWrapper: _AlterTimeSeriesWrapperInterfaceModule

class _AlterTimeSeriesWrapperFactoryInterfaceModule(_IdentifiableInterfaceModule):
    class WrapRequest(Protocol):
        timeSeries: TimeSeriesClient | _TimeSeriesInterfaceModule.Server
        def send(
            self,
        ) -> _AlterTimeSeriesWrapperFactoryInterfaceModule.AlterTimeSeriesWrapperFactoryClient.WrapResult: ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _AlterTimeSeriesWrapperFactoryInterfaceModule.AlterTimeSeriesWrapperFactoryClient: ...
    class Server(_IdentifiableInterfaceModule.Server):
        class WrapResult(_DynamicStructBuilder):
            @property
            def wrapper(
                self,
            ) -> (
                _AlterTimeSeriesWrapperInterfaceModule.Server
                | _AlterTimeSeriesWrapperInterfaceModule.AlterTimeSeriesWrapperClient
            ): ...
            @wrapper.setter
            def wrapper(
                self,
                value: _AlterTimeSeriesWrapperInterfaceModule.Server
                | _AlterTimeSeriesWrapperInterfaceModule.AlterTimeSeriesWrapperClient,
            ) -> None: ...

        class WrapResultTuple(NamedTuple):
            wrapper: (
                _AlterTimeSeriesWrapperInterfaceModule.Server
                | _AlterTimeSeriesWrapperInterfaceModule.AlterTimeSeriesWrapperClient
            )

        class WrapParams(Protocol):
            timeSeries: TimeSeriesClient

        class WrapCallContext(Protocol):
            params: _AlterTimeSeriesWrapperFactoryInterfaceModule.Server.WrapParams
            @property
            def results(
                self,
            ) -> _AlterTimeSeriesWrapperFactoryInterfaceModule.Server.WrapResult: ...

        def wrap(
            self,
            timeSeries: TimeSeriesClient,
            _context: _AlterTimeSeriesWrapperFactoryInterfaceModule.Server.WrapCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            _AlterTimeSeriesWrapperInterfaceModule.Server
            | _AlterTimeSeriesWrapperFactoryInterfaceModule.Server.WrapResultTuple
            | None
        ]: ...
        def wrap_context(
            self,
            context: _AlterTimeSeriesWrapperFactoryInterfaceModule.Server.WrapCallContext,
        ) -> Awaitable[None]: ...

    class AlterTimeSeriesWrapperFactoryClient(
        _IdentifiableInterfaceModule.IdentifiableClient
    ):
        class WrapResult(Awaitable[WrapResult], Protocol):
            wrapper: _AlterTimeSeriesWrapperInterfaceModule.AlterTimeSeriesWrapperClient

        def wrap(
            self,
            timeSeries: TimeSeriesClient
            | _TimeSeriesInterfaceModule.Server
            | None = None,
        ) -> _AlterTimeSeriesWrapperFactoryInterfaceModule.AlterTimeSeriesWrapperFactoryClient.WrapResult: ...
        def wrap_request(
            self,
            timeSeries: TimeSeriesClient
            | _TimeSeriesInterfaceModule.Server
            | None = None,
        ) -> _AlterTimeSeriesWrapperFactoryInterfaceModule.WrapRequest: ...

AlterTimeSeriesWrapperFactory: _AlterTimeSeriesWrapperFactoryInterfaceModule

# Top-level type aliases for use in type annotations
type AlterResult = (
    _AlterTimeSeriesWrapperInterfaceModule.AlterTimeSeriesWrapperClient.AlterResult
)
type AlterTimeSeriesWrapperAlterTypeEnum = int | Literal["add", "mul"]
type AlterTimeSeriesWrapperClient = (
    _AlterTimeSeriesWrapperInterfaceModule.AlterTimeSeriesWrapperClient
)
type AlterTimeSeriesWrapperFactoryClient = (
    _AlterTimeSeriesWrapperFactoryInterfaceModule.AlterTimeSeriesWrapperFactoryClient
)
type AlterTimeSeriesWrapperFactoryServer = (
    _AlterTimeSeriesWrapperFactoryInterfaceModule.Server
)
type AlterTimeSeriesWrapperServer = _AlterTimeSeriesWrapperInterfaceModule.Server
type AlteredBuilder = (
    _AlterTimeSeriesWrapperInterfaceModule._AlteredStructModule.Builder
)
type AlteredListBuilder = _AlteredList.Builder
type AlteredListReader = _AlteredList.Reader
type AlteredReader = _AlterTimeSeriesWrapperInterfaceModule._AlteredStructModule.Reader
type AlteredelementsResult = _AlterTimeSeriesWrapperInterfaceModule.AlterTimeSeriesWrapperClient.AlteredelementsResult
type CSVConfigBuilder = (
    _CSVTimeSeriesFactoryInterfaceModule._CSVConfigStructModule.Builder
)
type CSVConfigReader = (
    _CSVTimeSeriesFactoryInterfaceModule._CSVConfigStructModule.Reader
)
type CSVTimeSeriesFactoryClient = (
    _CSVTimeSeriesFactoryInterfaceModule.CSVTimeSeriesFactoryClient
)
type CSVTimeSeriesFactoryServer = _CSVTimeSeriesFactoryInterfaceModule.Server
type CategoriesResult = (
    _MetadataStructModule._SupportedInterfaceModule.SupportedClient.CategoriesResult
)
type ClosesttimeseriesatResult = (
    _DatasetInterfaceModule.DatasetClient.ClosesttimeseriesatResult
)
type CreateResult = (
    _CSVTimeSeriesFactoryInterfaceModule.CSVTimeSeriesFactoryClient.CreateResult
)
type DataResult = _TimeSeriesInterfaceModule.TimeSeriesClient.DataResult
type DatasetClient = _DatasetInterfaceModule.DatasetClient
type DatasetClientListBuilder = _DatasetClientList.Builder
type DatasetClientListReader = _DatasetClientList.Reader
type DatasetServer = _DatasetInterfaceModule.Server
type DatatResult = _TimeSeriesInterfaceModule.TimeSeriesClient.DatatResult
type ElementEnum = (
    int
    | Literal[
        "tmin",
        "tavg",
        "tmax",
        "precip",
        "globrad",
        "wind",
        "sunhours",
        "cloudamount",
        "relhumid",
        "airpress",
        "vaporpress",
        "co2",
        "o3",
        "et0",
        "dewpointTemp",
        "specificHumidity",
        "snowfallFlux",
        "surfaceDownwellingLongwaveRadiation",
        "potET",
    ]
)
type ElementEnumListBuilder = _ElementEnumList.Builder
type ElementEnumListReader = _ElementEnumList.Reader
type EnsembleMemberBuilder = _EnsembleMemberStructModule.Builder
type EnsembleMemberReader = _EnsembleMemberStructModule.Reader
type EntryBuilder = _MetadataStructModule._EntryStructModule.Builder
type EntryListBuilder = _EntryList.Builder
type EntryListReader = _EntryList.Reader
type EntryReader = _MetadataStructModule._EntryStructModule.Reader
type Float32ListBuilder = _Float32List.Builder
type Float32ListListBuilder = _Float32ListList.Builder
type Float32ListListReader = _Float32ListList.Reader
type Float32ListReader = _Float32List.Reader
type ForallResult = (
    _MetadataStructModule._InformationInterfaceModule.InformationClient.ForallResult
)
type ForoneResult = (
    _MetadataStructModule._InformationInterfaceModule.InformationClient.ForoneResult
)
type GCMEnum = (
    int
    | Literal[
        "cccmaCanEsm2",
        "ichecEcEarth",
        "ipslIpslCm5AMr",
        "mirocMiroc5",
        "mpiMMpiEsmLr",
        "gfdlEsm4",
        "ipslCm6aLr",
        "mpiEsm12Hr",
        "mriEsm20",
        "ukesm10Ll",
        "gswp3W5E5",
        "mohcHadGem2Es",
    ]
)
type GetLocationsCallbackClient = _DatasetInterfaceModule._GetLocationsCallbackInterfaceModule.GetLocationsCallbackClient
type GetLocationsCallbackServer = (
    _DatasetInterfaceModule._GetLocationsCallbackInterfaceModule.Server
)
type GetavailabledatasetsResult = (
    _ServiceInterfaceModule.ServiceClient.GetavailabledatasetsResult
)
type GetdatasetsforResult = _ServiceInterfaceModule.ServiceClient.GetdatasetsforResult
type HeaderResult = _TimeSeriesInterfaceModule.TimeSeriesClient.HeaderResult
type IdInformationListBuilder = _IdInformationList.Builder
type IdInformationListReader = _IdInformationList.Reader
type InformationClient = (
    _MetadataStructModule._InformationInterfaceModule.InformationClient
)
type InformationServer = _MetadataStructModule._InformationInterfaceModule.Server
type KVBuilder = _LocationStructModule._KVStructModule.Builder
type KVListBuilder = _KVList.Builder
type KVListReader = _KVList.Reader
type KVReader = _LocationStructModule._KVStructModule.Reader
type LocationBuilder = _LocationStructModule.Builder
type LocationListBuilder = _LocationList.Builder
type LocationListReader = _LocationList.Reader
type LocationReader = _LocationStructModule.Reader
type LocationResult = _TimeSeriesInterfaceModule.TimeSeriesClient.LocationResult
type LocationsResult = _DatasetInterfaceModule.DatasetClient.LocationsResult
type MetaPlusDataBuilder = _MetaPlusDataStructModule.Builder
type MetaPlusDataListBuilder = _MetaPlusDataList.Builder
type MetaPlusDataListReader = _MetaPlusDataList.Reader
type MetaPlusDataReader = _MetaPlusDataStructModule.Reader
type MetadataBuilder = _MetadataStructModule.Builder
type MetadataReader = _MetadataStructModule.Reader
type MetadataResult = _DatasetInterfaceModule.DatasetClient.MetadataResult
type NextlocationsResult = _DatasetInterfaceModule._GetLocationsCallbackInterfaceModule.GetLocationsCallbackClient.NextlocationsResult
type PairListBuilder = _PairList.Builder
type PairListReader = _PairList.Reader
type RCMEnum = (
    int
    | Literal[
        "clmcomCclm4817",
        "gericsRemo2015",
        "knmiRacmo22E",
        "smhiRca4",
        "clmcomBtuCclm4817",
        "mpiCscRemo2009",
        "uhohWrf361H",
    ]
)
type RCPEnum = (
    int | Literal["rcp19", "rcp26", "rcp34", "rcp45", "rcp60", "rcp70", "rcp85"]
)
type RangeResult = _TimeSeriesInterfaceModule.TimeSeriesClient.RangeResult
type RemoveResult = (
    _AlterTimeSeriesWrapperInterfaceModule.AlterTimeSeriesWrapperClient.RemoveResult
)
type ReplacewrappedtimeseriesResult = _AlterTimeSeriesWrapperInterfaceModule.AlterTimeSeriesWrapperClient.ReplacewrappedtimeseriesResult
type ResolutionResult = _TimeSeriesInterfaceModule.TimeSeriesClient.ResolutionResult
type SSPEnum = int | Literal["ssp1", "ssp2", "ssp3", "ssp4", "ssp5"]
type ServiceClient = _ServiceInterfaceModule.ServiceClient
type ServiceServer = _ServiceInterfaceModule.Server
type StreamlocationsResult = _DatasetInterfaceModule.DatasetClient.StreamlocationsResult
type SubheaderResult = _TimeSeriesInterfaceModule.TimeSeriesClient.SubheaderResult
type SubrangeResult = _TimeSeriesInterfaceModule.TimeSeriesClient.SubrangeResult
type SupportedClient = _MetadataStructModule._SupportedInterfaceModule.SupportedClient
type SupportedServer = _MetadataStructModule._SupportedInterfaceModule.Server
type SupportedvaluesResult = _MetadataStructModule._SupportedInterfaceModule.SupportedClient.SupportedvaluesResult
type TimeSeriesClient = _TimeSeriesInterfaceModule.TimeSeriesClient
type TimeSeriesDataBuilder = _TimeSeriesDataStructModule.Builder
type TimeSeriesDataReader = _TimeSeriesDataStructModule.Reader
type TimeSeriesResolutionEnum = int | Literal["daily", "hourly"]
type TimeSeriesServer = _TimeSeriesInterfaceModule.Server
type TimeseriesatResult = _DatasetInterfaceModule.DatasetClient.TimeseriesatResult
type ValueBuilder = _MetadataStructModule._ValueStructModule.Builder
type ValueReader = _MetadataStructModule._ValueStructModule.Reader
type WrapResult = _AlterTimeSeriesWrapperFactoryInterfaceModule.AlterTimeSeriesWrapperFactoryClient.WrapResult
type WrappedtimeseriesResult = _AlterTimeSeriesWrapperInterfaceModule.AlterTimeSeriesWrapperClient.WrappedtimeseriesResult
