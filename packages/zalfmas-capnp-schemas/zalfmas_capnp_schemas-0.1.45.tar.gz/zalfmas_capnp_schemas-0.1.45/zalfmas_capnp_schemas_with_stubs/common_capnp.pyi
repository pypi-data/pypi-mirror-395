"""This is an automatically generated stub for `common.capnp`."""

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
from collections.abc import Iterator, Awaitable, Callable
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

# Type alias for Capability parameters
type Capability = (
    _DynamicCapabilityClient
    | _DynamicCapabilityServer
    | _DynamicObjectReader
    | _DynamicObjectBuilder
)

class _IdInformationStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def id(self) -> str: ...
        @property
        def name(self) -> str: ...
        @property
        def description(self) -> str: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> IdInformationBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def id(self) -> str: ...
        @id.setter
        def id(self, value: str) -> None: ...
        @property
        def name(self) -> str: ...
        @name.setter
        def name(self, value: str) -> None: ...
        @property
        def description(self) -> str: ...
        @description.setter
        def description(self, value: str) -> None: ...
        @override
        def as_reader(self) -> IdInformationReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        id: str | None = None,
        name: str | None = None,
        description: str | None = None,
        **kwargs: Any,
    ) -> IdInformationBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[IdInformationReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[IdInformationReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[IdInformationBuilder]: ...
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
    ) -> IdInformationReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> IdInformationReader: ...

IdInformation: _IdInformationStructModule

class _IdentifiableInterfaceModule(_InterfaceModule):
    class InfoRequest(Protocol):
        def send(
            self,
        ) -> _IdentifiableInterfaceModule.IdentifiableClient.InfoResult: ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _IdentifiableInterfaceModule.IdentifiableClient: ...
    class Server(_DynamicCapabilityServer):
        class InfoResult(Awaitable[InfoResult], Protocol):
            id: str
            name: str
            description: str

        class InfoResultTuple(NamedTuple):
            id: str
            name: str
            description: str

        class InfoParams(Protocol): ...

        class InfoCallContext(Protocol):
            params: _IdentifiableInterfaceModule.Server.InfoParams
            @property
            def results(self) -> IdInformationBuilder: ...

        def info(
            self,
            _context: _IdentifiableInterfaceModule.Server.InfoCallContext,
            **kwargs: Any,
        ) -> Awaitable[_IdentifiableInterfaceModule.Server.InfoResultTuple | None]: ...
        def info_context(
            self, context: _IdentifiableInterfaceModule.Server.InfoCallContext
        ) -> Awaitable[None]: ...

    class IdentifiableClient(_DynamicCapabilityClient):
        class InfoResult(Awaitable[InfoResult], Protocol):
            id: str
            name: str
            description: str

        def info(
            self,
        ) -> _IdentifiableInterfaceModule.IdentifiableClient.InfoResult: ...
        def info_request(self) -> _IdentifiableInterfaceModule.InfoRequest: ...

Identifiable: _IdentifiableInterfaceModule

class _StructuredTextStructModule(_StructModule):
    class _TypeEnumModule:
        unstructured: int
        json: int
        xml: int
        toml: int
        sturdyRef: int

    Type: _TypeEnumModule
    class _StructuredTextStructureStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def none(self) -> None: ...
            @property
            def json(self) -> None: ...
            @property
            def xml(self) -> None: ...
            @property
            def toml(self) -> None: ...
            @override
            def which(self) -> Literal["none", "json", "xml", "toml"]: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> StructuredTextStructureBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def none(self) -> None: ...
            @none.setter
            def none(self, value: None) -> None: ...
            @property
            def json(self) -> None: ...
            @json.setter
            def json(self, value: None) -> None: ...
            @property
            def xml(self) -> None: ...
            @xml.setter
            def xml(self, value: None) -> None: ...
            @property
            def toml(self) -> None: ...
            @toml.setter
            def toml(self, value: None) -> None: ...
            @override
            def which(self) -> Literal["none", "json", "xml", "toml"]: ...
            @override
            def as_reader(self) -> StructuredTextStructureReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            none: None | None = None,
            json: None | None = None,
            xml: None | None = None,
            toml: None | None = None,
            **kwargs: Any,
        ) -> StructuredTextStructureBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[StructuredTextStructureReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[StructuredTextStructureReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[StructuredTextStructureBuilder]: ...
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
        ) -> StructuredTextStructureReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> StructuredTextStructureReader: ...

    type StructuredTextStructureReader = _StructuredTextStructureStructModule.Reader
    type StructuredTextStructureBuilder = _StructuredTextStructureStructModule.Builder
    StructuredTextStructure: _StructuredTextStructureStructModule
    class Reader(_DynamicStructReader):
        @property
        def value(self) -> str: ...
        @property
        def structure(self) -> StructuredTextStructureReader: ...
        @property
        def type(self) -> StructuredTextTypeEnum: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> StructuredTextBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def value(self) -> str: ...
        @value.setter
        def value(self, value: str) -> None: ...
        @property
        def structure(self) -> StructuredTextStructureBuilder: ...
        @structure.setter
        def structure(
            self,
            value: StructuredTextStructureBuilder
            | StructuredTextStructureReader
            | dict[str, Any],
        ) -> None: ...
        @property
        def type(self) -> StructuredTextTypeEnum: ...
        @type.setter
        def type(self, value: StructuredTextTypeEnum) -> None: ...
        @override
        def init(
            self, field: Literal["structure"], size: int | None = None
        ) -> StructuredTextStructureBuilder: ...
        @override
        def as_reader(self) -> StructuredTextReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        value: str | None = None,
        structure: StructuredTextStructureBuilder | dict[str, Any] | None = None,
        type: StructuredTextTypeEnum | None = None,
        **kwargs: Any,
    ) -> StructuredTextBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[StructuredTextReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[StructuredTextReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[StructuredTextBuilder]: ...
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
    ) -> StructuredTextReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> StructuredTextReader: ...

StructuredText: _StructuredTextStructModule

class _Float64List:
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

class _Int64List:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> int: ...
        @override
        def __iter__(self) -> Iterator[int]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> int: ...
        @override
        def __setitem__(self, key: int, value: int) -> None: ...
        @override
        def __iter__(self) -> Iterator[int]: ...

class _Int32List:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> int: ...
        @override
        def __iter__(self) -> Iterator[int]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> int: ...
        @override
        def __setitem__(self, key: int, value: int) -> None: ...
        @override
        def __iter__(self) -> Iterator[int]: ...

class _Int16List:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> int: ...
        @override
        def __iter__(self) -> Iterator[int]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> int: ...
        @override
        def __setitem__(self, key: int, value: int) -> None: ...
        @override
        def __iter__(self) -> Iterator[int]: ...

class _Int8List:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> int: ...
        @override
        def __iter__(self) -> Iterator[int]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> int: ...
        @override
        def __setitem__(self, key: int, value: int) -> None: ...
        @override
        def __iter__(self) -> Iterator[int]: ...

class _Uint64List:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> int: ...
        @override
        def __iter__(self) -> Iterator[int]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> int: ...
        @override
        def __setitem__(self, key: int, value: int) -> None: ...
        @override
        def __iter__(self) -> Iterator[int]: ...

class _Uint32List:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> int: ...
        @override
        def __iter__(self) -> Iterator[int]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> int: ...
        @override
        def __setitem__(self, key: int, value: int) -> None: ...
        @override
        def __iter__(self) -> Iterator[int]: ...

class _Uint16List:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> int: ...
        @override
        def __iter__(self) -> Iterator[int]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> int: ...
        @override
        def __setitem__(self, key: int, value: int) -> None: ...
        @override
        def __iter__(self) -> Iterator[int]: ...

class _Uint8List:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> int: ...
        @override
        def __iter__(self) -> Iterator[int]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> int: ...
        @override
        def __setitem__(self, key: int, value: int) -> None: ...
        @override
        def __iter__(self) -> Iterator[int]: ...

class _BoolList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> bool: ...
        @override
        def __iter__(self) -> Iterator[bool]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> bool: ...
        @override
        def __setitem__(self, key: int, value: bool) -> None: ...
        @override
        def __iter__(self) -> Iterator[bool]: ...

class _TextList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> str: ...
        @override
        def __iter__(self) -> Iterator[str]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> str: ...
        @override
        def __setitem__(self, key: int, value: str) -> None: ...
        @override
        def __iter__(self) -> Iterator[str]: ...

class _DataList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> bytes: ...
        @override
        def __iter__(self) -> Iterator[bytes]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> bytes: ...
        @override
        def __setitem__(self, key: int, value: bytes) -> None: ...
        @override
        def __iter__(self) -> Iterator[bytes]: ...

class _AnyPointerList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> _DynamicObjectReader: ...
        @override
        def __iter__(self) -> Iterator[_DynamicObjectReader]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> _DynamicObjectBuilder: ...
        @override
        def __setitem__(self, key: int, value: AnyPointer) -> None: ...
        @override
        def __iter__(self) -> Iterator[_DynamicObjectBuilder]: ...

class _PairStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def fst(self) -> _DynamicObjectReader: ...
        @property
        def snd(self) -> _DynamicObjectReader: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> PairBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def fst(self) -> _DynamicObjectReader: ...
        @fst.setter
        def fst(self, value: AnyPointer) -> None: ...
        @property
        def snd(self) -> _DynamicObjectReader: ...
        @snd.setter
        def snd(self, value: AnyPointer) -> None: ...
        @override
        def as_reader(self) -> PairReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        fst: AnyPointer | None = None,
        snd: AnyPointer | None = None,
        **kwargs: Any,
    ) -> PairBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[PairReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[PairReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[PairBuilder]: ...
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
    ) -> PairReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> PairReader: ...

Pair: _PairStructModule

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

class _ValueStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def f64(self) -> float: ...
        @property
        def f32(self) -> float: ...
        @property
        def i64(self) -> int: ...
        @property
        def i32(self) -> int: ...
        @property
        def i16(self) -> int: ...
        @property
        def i8(self) -> int: ...
        @property
        def ui64(self) -> int: ...
        @property
        def ui32(self) -> int: ...
        @property
        def ui16(self) -> int: ...
        @property
        def ui8(self) -> int: ...
        @property
        def b(self) -> bool: ...
        @property
        def t(self) -> str: ...
        @property
        def d(self) -> bytes: ...
        @property
        def p(self) -> _DynamicObjectReader: ...
        @property
        def cap(self) -> _DynamicObjectReader: ...
        @property
        def lf64(self) -> Float64ListReader: ...
        @property
        def lf32(self) -> Float32ListReader: ...
        @property
        def li64(self) -> Int64ListReader: ...
        @property
        def li32(self) -> Int32ListReader: ...
        @property
        def li16(self) -> Int16ListReader: ...
        @property
        def li8(self) -> Int8ListReader: ...
        @property
        def lui64(self) -> Uint64ListReader: ...
        @property
        def lui32(self) -> Uint32ListReader: ...
        @property
        def lui16(self) -> Uint16ListReader: ...
        @property
        def lui8(self) -> Uint8ListReader: ...
        @property
        def lb(self) -> BoolListReader: ...
        @property
        def lt(self) -> TextListReader: ...
        @property
        def ld(self) -> DataListReader: ...
        @property
        def lcap(self) -> AnyPointerListReader: ...
        @property
        def lpair(self) -> PairListReader: ...
        @override
        def which(
            self,
        ) -> Literal[
            "f64",
            "f32",
            "i64",
            "i32",
            "i16",
            "i8",
            "ui64",
            "ui32",
            "ui16",
            "ui8",
            "b",
            "t",
            "d",
            "p",
            "cap",
            "lf64",
            "lf32",
            "li64",
            "li32",
            "li16",
            "li8",
            "lui64",
            "lui32",
            "lui16",
            "lui8",
            "lb",
            "lt",
            "ld",
            "lcap",
            "lpair",
        ]: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> ValueBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def f64(self) -> float: ...
        @f64.setter
        def f64(self, value: float) -> None: ...
        @property
        def f32(self) -> float: ...
        @f32.setter
        def f32(self, value: float) -> None: ...
        @property
        def i64(self) -> int: ...
        @i64.setter
        def i64(self, value: int) -> None: ...
        @property
        def i32(self) -> int: ...
        @i32.setter
        def i32(self, value: int) -> None: ...
        @property
        def i16(self) -> int: ...
        @i16.setter
        def i16(self, value: int) -> None: ...
        @property
        def i8(self) -> int: ...
        @i8.setter
        def i8(self, value: int) -> None: ...
        @property
        def ui64(self) -> int: ...
        @ui64.setter
        def ui64(self, value: int) -> None: ...
        @property
        def ui32(self) -> int: ...
        @ui32.setter
        def ui32(self, value: int) -> None: ...
        @property
        def ui16(self) -> int: ...
        @ui16.setter
        def ui16(self, value: int) -> None: ...
        @property
        def ui8(self) -> int: ...
        @ui8.setter
        def ui8(self, value: int) -> None: ...
        @property
        def b(self) -> bool: ...
        @b.setter
        def b(self, value: bool) -> None: ...
        @property
        def t(self) -> str: ...
        @t.setter
        def t(self, value: str) -> None: ...
        @property
        def d(self) -> bytes: ...
        @d.setter
        def d(self, value: bytes) -> None: ...
        @property
        def p(self) -> _DynamicObjectBuilder: ...
        @p.setter
        def p(self, value: AnyPointer) -> None: ...
        @property
        def cap(self) -> _DynamicObjectReader: ...
        @cap.setter
        def cap(self, value: Capability) -> None: ...
        @property
        def lf64(self) -> Float64ListBuilder: ...
        @lf64.setter
        def lf64(
            self, value: Float64ListBuilder | Float64ListReader | dict[str, Any]
        ) -> None: ...
        @property
        def lf32(self) -> Float32ListBuilder: ...
        @lf32.setter
        def lf32(
            self, value: Float32ListBuilder | Float32ListReader | dict[str, Any]
        ) -> None: ...
        @property
        def li64(self) -> Int64ListBuilder: ...
        @li64.setter
        def li64(
            self, value: Int64ListBuilder | Int64ListReader | dict[str, Any]
        ) -> None: ...
        @property
        def li32(self) -> Int32ListBuilder: ...
        @li32.setter
        def li32(
            self, value: Int32ListBuilder | Int32ListReader | dict[str, Any]
        ) -> None: ...
        @property
        def li16(self) -> Int16ListBuilder: ...
        @li16.setter
        def li16(
            self, value: Int16ListBuilder | Int16ListReader | dict[str, Any]
        ) -> None: ...
        @property
        def li8(self) -> Int8ListBuilder: ...
        @li8.setter
        def li8(
            self, value: Int8ListBuilder | Int8ListReader | dict[str, Any]
        ) -> None: ...
        @property
        def lui64(self) -> Uint64ListBuilder: ...
        @lui64.setter
        def lui64(
            self, value: Uint64ListBuilder | Uint64ListReader | dict[str, Any]
        ) -> None: ...
        @property
        def lui32(self) -> Uint32ListBuilder: ...
        @lui32.setter
        def lui32(
            self, value: Uint32ListBuilder | Uint32ListReader | dict[str, Any]
        ) -> None: ...
        @property
        def lui16(self) -> Uint16ListBuilder: ...
        @lui16.setter
        def lui16(
            self, value: Uint16ListBuilder | Uint16ListReader | dict[str, Any]
        ) -> None: ...
        @property
        def lui8(self) -> Uint8ListBuilder: ...
        @lui8.setter
        def lui8(
            self, value: Uint8ListBuilder | Uint8ListReader | dict[str, Any]
        ) -> None: ...
        @property
        def lb(self) -> BoolListBuilder: ...
        @lb.setter
        def lb(
            self, value: BoolListBuilder | BoolListReader | dict[str, Any]
        ) -> None: ...
        @property
        def lt(self) -> TextListBuilder: ...
        @lt.setter
        def lt(
            self, value: TextListBuilder | TextListReader | dict[str, Any]
        ) -> None: ...
        @property
        def ld(self) -> DataListBuilder: ...
        @ld.setter
        def ld(
            self, value: DataListBuilder | DataListReader | dict[str, Any]
        ) -> None: ...
        @property
        def lcap(self) -> AnyPointerListBuilder: ...
        @lcap.setter
        def lcap(
            self, value: AnyPointerListBuilder | AnyPointerListReader | dict[str, Any]
        ) -> None: ...
        @property
        def lpair(self) -> PairListBuilder: ...
        @lpair.setter
        def lpair(
            self, value: PairListBuilder | PairListReader | dict[str, Any]
        ) -> None: ...
        @override
        def which(
            self,
        ) -> Literal[
            "f64",
            "f32",
            "i64",
            "i32",
            "i16",
            "i8",
            "ui64",
            "ui32",
            "ui16",
            "ui8",
            "b",
            "t",
            "d",
            "p",
            "cap",
            "lf64",
            "lf32",
            "li64",
            "li32",
            "li16",
            "li8",
            "lui64",
            "lui32",
            "lui16",
            "lui8",
            "lb",
            "lt",
            "ld",
            "lcap",
            "lpair",
        ]: ...
        @override
        @overload
        def init(
            self, field: Literal["lf64"], size: int | None = None
        ) -> Float64ListBuilder: ...
        @overload
        def init(
            self, field: Literal["lf32"], size: int | None = None
        ) -> Float32ListBuilder: ...
        @overload
        def init(
            self, field: Literal["li64"], size: int | None = None
        ) -> Int64ListBuilder: ...
        @overload
        def init(
            self, field: Literal["li32"], size: int | None = None
        ) -> Int32ListBuilder: ...
        @overload
        def init(
            self, field: Literal["li16"], size: int | None = None
        ) -> Int16ListBuilder: ...
        @overload
        def init(
            self, field: Literal["li8"], size: int | None = None
        ) -> Int8ListBuilder: ...
        @overload
        def init(
            self, field: Literal["lui64"], size: int | None = None
        ) -> Uint64ListBuilder: ...
        @overload
        def init(
            self, field: Literal["lui32"], size: int | None = None
        ) -> Uint32ListBuilder: ...
        @overload
        def init(
            self, field: Literal["lui16"], size: int | None = None
        ) -> Uint16ListBuilder: ...
        @overload
        def init(
            self, field: Literal["lui8"], size: int | None = None
        ) -> Uint8ListBuilder: ...
        @overload
        def init(
            self, field: Literal["lb"], size: int | None = None
        ) -> BoolListBuilder: ...
        @overload
        def init(
            self, field: Literal["lt"], size: int | None = None
        ) -> TextListBuilder: ...
        @overload
        def init(
            self, field: Literal["ld"], size: int | None = None
        ) -> DataListBuilder: ...
        @overload
        def init(
            self, field: Literal["lcap"], size: int | None = None
        ) -> AnyPointerListBuilder: ...
        @overload
        def init(
            self, field: Literal["lpair"], size: int | None = None
        ) -> PairListBuilder: ...
        @overload
        def init(self, field: str, size: int | None = None) -> Any: ...
        @override
        def as_reader(self) -> ValueReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        f64: float | None = None,
        f32: float | None = None,
        i64: int | None = None,
        i32: int | None = None,
        i16: int | None = None,
        i8: int | None = None,
        ui64: int | None = None,
        ui32: int | None = None,
        ui16: int | None = None,
        ui8: int | None = None,
        b: bool | None = None,
        t: str | None = None,
        d: bytes | None = None,
        p: AnyPointer | None = None,
        cap: Capability | None = None,
        lf64: Float64ListBuilder | dict[str, Any] | None = None,
        lf32: Float32ListBuilder | dict[str, Any] | None = None,
        li64: Int64ListBuilder | dict[str, Any] | None = None,
        li32: Int32ListBuilder | dict[str, Any] | None = None,
        li16: Int16ListBuilder | dict[str, Any] | None = None,
        li8: Int8ListBuilder | dict[str, Any] | None = None,
        lui64: Uint64ListBuilder | dict[str, Any] | None = None,
        lui32: Uint32ListBuilder | dict[str, Any] | None = None,
        lui16: Uint16ListBuilder | dict[str, Any] | None = None,
        lui8: Uint8ListBuilder | dict[str, Any] | None = None,
        lb: BoolListBuilder | dict[str, Any] | None = None,
        lt: TextListBuilder | dict[str, Any] | None = None,
        ld: DataListBuilder | dict[str, Any] | None = None,
        lcap: AnyPointerListBuilder | dict[str, Any] | None = None,
        lpair: PairListBuilder | dict[str, Any] | None = None,
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

Value: _ValueStructModule

class _HolderInterfaceModule(_InterfaceModule):
    class ValueRequest(Protocol):
        def send(self) -> _HolderInterfaceModule.HolderClient.ValueResult: ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _HolderInterfaceModule.HolderClient: ...
    class Server(_DynamicCapabilityServer):
        class ValueResult(_DynamicStructBuilder):
            @property
            def value(self) -> AnyPointer: ...
            @value.setter
            def value(self, value: AnyPointer) -> None: ...

        class ValueResultTuple(NamedTuple):
            value: AnyPointer

        class ValueParams(Protocol): ...

        class ValueCallContext(Protocol):
            params: _HolderInterfaceModule.Server.ValueParams
            @property
            def results(self) -> _HolderInterfaceModule.Server.ValueResult: ...

        def value(
            self,
            _context: _HolderInterfaceModule.Server.ValueCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            AnyPointer | _HolderInterfaceModule.Server.ValueResultTuple | None
        ]: ...
        def value_context(
            self, context: _HolderInterfaceModule.Server.ValueCallContext
        ) -> Awaitable[None]: ...

    class HolderClient(_DynamicCapabilityClient):
        class ValueResult(Awaitable[ValueResult], Protocol):
            value: _DynamicObjectReader

        def value(self) -> _HolderInterfaceModule.HolderClient.ValueResult: ...
        def value_request(self) -> _HolderInterfaceModule.ValueRequest: ...

Holder: _HolderInterfaceModule

class _IdentifiableHolderInterfaceModule(
    _IdentifiableInterfaceModule, _HolderInterfaceModule
):
    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _IdentifiableHolderInterfaceModule.IdentifiableHolderClient: ...
    class Server(
        _IdentifiableInterfaceModule.Server, _HolderInterfaceModule.Server
    ): ...
    class IdentifiableHolderClient(
        _IdentifiableInterfaceModule.IdentifiableClient,
        _HolderInterfaceModule.HolderClient,
    ): ...

IdentifiableHolder: _IdentifiableHolderInterfaceModule

# Top-level type aliases for use in type annotations
type AnyPointerListBuilder = _AnyPointerList.Builder
type AnyPointerListReader = _AnyPointerList.Reader
type BoolListBuilder = _BoolList.Builder
type BoolListReader = _BoolList.Reader
type DataListBuilder = _DataList.Builder
type DataListReader = _DataList.Reader
type Float32ListBuilder = _Float32List.Builder
type Float32ListReader = _Float32List.Reader
type Float64ListBuilder = _Float64List.Builder
type Float64ListReader = _Float64List.Reader
type HolderClient = _HolderInterfaceModule.HolderClient
type HolderServer = _HolderInterfaceModule.Server
type IdInformationBuilder = _IdInformationStructModule.Builder
type IdInformationReader = _IdInformationStructModule.Reader
type IdentifiableClient = _IdentifiableInterfaceModule.IdentifiableClient
type IdentifiableHolderClient = (
    _IdentifiableHolderInterfaceModule.IdentifiableHolderClient
)
type IdentifiableHolderServer = _IdentifiableHolderInterfaceModule.Server
type IdentifiableServer = _IdentifiableInterfaceModule.Server
type InfoResult = _IdentifiableInterfaceModule.IdentifiableClient.InfoResult
type Int16ListBuilder = _Int16List.Builder
type Int16ListReader = _Int16List.Reader
type Int32ListBuilder = _Int32List.Builder
type Int32ListReader = _Int32List.Reader
type Int64ListBuilder = _Int64List.Builder
type Int64ListReader = _Int64List.Reader
type Int8ListBuilder = _Int8List.Builder
type Int8ListReader = _Int8List.Reader
type PairBuilder = _PairStructModule.Builder
type PairListBuilder = _PairList.Builder
type PairListReader = _PairList.Reader
type PairReader = _PairStructModule.Reader
type StructuredTextBuilder = _StructuredTextStructModule.Builder
type StructuredTextReader = _StructuredTextStructModule.Reader
type StructuredTextStructureBuilder = (
    _StructuredTextStructModule._StructuredTextStructureStructModule.Builder
)
type StructuredTextStructureReader = (
    _StructuredTextStructModule._StructuredTextStructureStructModule.Reader
)
type StructuredTextTypeEnum = (
    int | Literal["unstructured", "json", "xml", "toml", "sturdyRef"]
)
type TextListBuilder = _TextList.Builder
type TextListReader = _TextList.Reader
type Uint16ListBuilder = _Uint16List.Builder
type Uint16ListReader = _Uint16List.Reader
type Uint32ListBuilder = _Uint32List.Builder
type Uint32ListReader = _Uint32List.Reader
type Uint64ListBuilder = _Uint64List.Builder
type Uint64ListReader = _Uint64List.Reader
type Uint8ListBuilder = _Uint8List.Builder
type Uint8ListReader = _Uint8List.Reader
type ValueBuilder = _ValueStructModule.Builder
type ValueReader = _ValueStructModule.Reader
type ValueResult = _HolderInterfaceModule.HolderClient.ValueResult
