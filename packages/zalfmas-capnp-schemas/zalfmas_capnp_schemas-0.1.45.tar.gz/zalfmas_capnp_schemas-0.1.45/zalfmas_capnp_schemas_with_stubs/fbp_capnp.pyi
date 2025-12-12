"""This is an automatically generated stub for `fbp.capnp`."""

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
from .common_capnp import _IdentifiableInterfaceModule
from .persistence_capnp import _PersistentInterfaceModule
from .service_capnp import _StoppableInterfaceModule
from .common_capnp import IdInformationReader, IdInformationBuilder
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

class _IPStructModule(_StructModule):
    class _KVStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def key(self) -> str: ...
            @property
            def desc(self) -> str: ...
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
            def desc(self) -> str: ...
            @desc.setter
            def desc(self, value: str) -> None: ...
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
            desc: str | None = None,
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
    class _TypeEnumModule:
        standard: int
        openBracket: int
        closeBracket: int

    Type: _TypeEnumModule
    class Reader(_DynamicStructReader):
        @property
        def attributes(self) -> KVListReader: ...
        @property
        def content(self) -> _DynamicObjectReader: ...
        @property
        def type(self) -> IPTypeEnum: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> IPBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def attributes(self) -> KVListBuilder: ...
        @attributes.setter
        def attributes(
            self, value: KVListBuilder | KVListReader | dict[str, Any]
        ) -> None: ...
        @property
        def content(self) -> _DynamicObjectBuilder: ...
        @content.setter
        def content(self, value: AnyPointer) -> None: ...
        @property
        def type(self) -> IPTypeEnum: ...
        @type.setter
        def type(self, value: IPTypeEnum) -> None: ...
        @override
        def init(
            self, field: Literal["attributes"], size: int | None = None
        ) -> KVListBuilder: ...
        @override
        def as_reader(self) -> IPReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        attributes: KVListBuilder | dict[str, Any] | None = None,
        content: AnyPointer | None = None,
        type: IPTypeEnum | None = None,
        **kwargs: Any,
    ) -> IPBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[IPReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[IPReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[IPBuilder]: ...
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
    ) -> IPReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> IPReader: ...

IP: _IPStructModule

class _IIPStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def content(self) -> _DynamicObjectReader: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> IIPBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def content(self) -> _DynamicObjectBuilder: ...
        @content.setter
        def content(self, value: AnyPointer) -> None: ...
        @override
        def as_reader(self) -> IIPReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        content: AnyPointer | None = None,
        **kwargs: Any,
    ) -> IIPBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[IIPReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[IIPReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[IIPBuilder]: ...
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
    ) -> IIPReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> IIPReader: ...

IIP: _IIPStructModule

class _ChannelInterfaceModule(_IdentifiableInterfaceModule, _PersistentInterfaceModule):
    class _CloseSemanticsEnumModule:
        fbp: int
        no: int

    CloseSemantics: _CloseSemanticsEnumModule
    class _MsgStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def value(self) -> _DynamicObjectReader: ...
            @property
            def done(self) -> None: ...
            @property
            def noMsg(self) -> None: ...
            @override
            def which(self) -> Literal["value", "done", "noMsg"]: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> MsgBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def value(self) -> _DynamicObjectReader: ...
            @value.setter
            def value(self, value: AnyPointer) -> None: ...
            @property
            def done(self) -> None: ...
            @done.setter
            def done(self, value: None) -> None: ...
            @property
            def noMsg(self) -> None: ...
            @noMsg.setter
            def noMsg(self, value: None) -> None: ...
            @override
            def which(self) -> Literal["value", "done", "noMsg"]: ...
            @override
            def as_reader(self) -> MsgReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            value: AnyPointer | None = None,
            done: None | None = None,
            noMsg: None | None = None,
            **kwargs: Any,
        ) -> MsgBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[MsgReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[MsgReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[MsgBuilder]: ...
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
        ) -> MsgReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> MsgReader: ...

    type MsgReader = _MsgStructModule.Reader
    type MsgBuilder = _MsgStructModule.Builder
    Msg: _MsgStructModule
    class _ReaderInterfaceModule(
        _IdentifiableInterfaceModule, _PersistentInterfaceModule
    ):
        class ReadRequest(Protocol):
            def send(
                self,
            ) -> (
                _ChannelInterfaceModule._ReaderInterfaceModule.ReaderClient.ReadResult
            ): ...

        class CloseRequest(Protocol):
            def send(
                self,
            ) -> (
                _ChannelInterfaceModule._ReaderInterfaceModule.ReaderClient.CloseResult
            ): ...

        class ReadifmsgRequest(Protocol):
            def send(
                self,
            ) -> _ChannelInterfaceModule._ReaderInterfaceModule.ReaderClient.ReadifmsgResult: ...

        @override
        def _new_client(
            self, server: _DynamicCapabilityServer
        ) -> _ChannelInterfaceModule._ReaderInterfaceModule.ReaderClient: ...
        class Server(
            _IdentifiableInterfaceModule.Server, _PersistentInterfaceModule.Server
        ):
            class ReadResult(Awaitable[ReadResult], Protocol):
                value: AnyPointer
                done: None
                noMsg: None
                def which(self) -> Literal["value", "done", "noMsg"]: ...

            class CloseResult(Awaitable[None], Protocol): ...

            class ReadifmsgResult(Awaitable[ReadifmsgResult], Protocol):
                value: AnyPointer
                done: None
                noMsg: None
                def which(self) -> Literal["value", "done", "noMsg"]: ...

            class ReadResultTuple(NamedTuple):
                value: AnyPointer
                done: None
                noMsg: None

            class ReadifmsgResultTuple(NamedTuple):
                value: AnyPointer
                done: None
                noMsg: None

            class ReadParams(Protocol): ...

            class ReadCallContext(Protocol):
                params: _ChannelInterfaceModule._ReaderInterfaceModule.Server.ReadParams
                @property
                def results(self) -> MsgBuilder: ...

            class CloseParams(Protocol): ...

            class CloseCallContext(Protocol):
                params: (
                    _ChannelInterfaceModule._ReaderInterfaceModule.Server.CloseParams
                )

            class ReadifmsgParams(Protocol): ...

            class ReadifmsgCallContext(Protocol):
                params: _ChannelInterfaceModule._ReaderInterfaceModule.Server.ReadifmsgParams
                @property
                def results(self) -> MsgBuilder: ...

            def read(
                self,
                _context: _ChannelInterfaceModule._ReaderInterfaceModule.Server.ReadCallContext,
                **kwargs: Any,
            ) -> Awaitable[
                _ChannelInterfaceModule._ReaderInterfaceModule.Server.ReadResultTuple
                | None
            ]: ...
            def read_context(
                self,
                context: _ChannelInterfaceModule._ReaderInterfaceModule.Server.ReadCallContext,
            ) -> Awaitable[None]: ...
            def close(
                self,
                _context: _ChannelInterfaceModule._ReaderInterfaceModule.Server.CloseCallContext,
                **kwargs: Any,
            ) -> Awaitable[None]: ...
            def close_context(
                self,
                context: _ChannelInterfaceModule._ReaderInterfaceModule.Server.CloseCallContext,
            ) -> Awaitable[None]: ...
            def readIfMsg(
                self,
                _context: _ChannelInterfaceModule._ReaderInterfaceModule.Server.ReadifmsgCallContext,
                **kwargs: Any,
            ) -> Awaitable[
                _ChannelInterfaceModule._ReaderInterfaceModule.Server.ReadifmsgResultTuple
                | None
            ]: ...
            def readIfMsg_context(
                self,
                context: _ChannelInterfaceModule._ReaderInterfaceModule.Server.ReadifmsgCallContext,
            ) -> Awaitable[None]: ...

        class ReaderClient(
            _IdentifiableInterfaceModule.IdentifiableClient,
            _PersistentInterfaceModule.PersistentClient,
        ):
            class ReadResult(Awaitable[ReadResult], Protocol):
                value: _DynamicObjectReader
                done: None
                noMsg: None
                def which(self) -> Literal["value", "done", "noMsg"]: ...

            class CloseResult(Awaitable[None], Protocol): ...

            class ReadifmsgResult(Awaitable[ReadifmsgResult], Protocol):
                value: _DynamicObjectReader
                done: None
                noMsg: None
                def which(self) -> Literal["value", "done", "noMsg"]: ...

            def read(
                self,
            ) -> (
                _ChannelInterfaceModule._ReaderInterfaceModule.ReaderClient.ReadResult
            ): ...
            def close(
                self,
            ) -> (
                _ChannelInterfaceModule._ReaderInterfaceModule.ReaderClient.CloseResult
            ): ...
            def readIfMsg(
                self,
            ) -> _ChannelInterfaceModule._ReaderInterfaceModule.ReaderClient.ReadifmsgResult: ...
            def read_request(
                self,
            ) -> _ChannelInterfaceModule._ReaderInterfaceModule.ReadRequest: ...
            def close_request(
                self,
            ) -> _ChannelInterfaceModule._ReaderInterfaceModule.CloseRequest: ...
            def readIfMsg_request(
                self,
            ) -> _ChannelInterfaceModule._ReaderInterfaceModule.ReadifmsgRequest: ...

    Reader: _ReaderInterfaceModule
    type ReaderClient = _ChannelInterfaceModule._ReaderInterfaceModule.ReaderClient
    type ReaderServer = _ChannelInterfaceModule._ReaderInterfaceModule.Server
    class _WriterInterfaceModule(
        _IdentifiableInterfaceModule, _PersistentInterfaceModule
    ):
        class WriteRequest(Protocol):
            value: AnyPointer
            done: None
            noMsg: None
            def send(
                self,
            ) -> (
                _ChannelInterfaceModule._WriterInterfaceModule.WriterClient.WriteResult
            ): ...

        class CloseRequest(Protocol):
            def send(
                self,
            ) -> (
                _ChannelInterfaceModule._WriterInterfaceModule.WriterClient.CloseResult
            ): ...

        class WriteifspaceRequest(Protocol):
            value: AnyPointer
            done: None
            noMsg: None
            def send(
                self,
            ) -> _ChannelInterfaceModule._WriterInterfaceModule.WriterClient.WriteifspaceResult: ...

        @override
        def _new_client(
            self, server: _DynamicCapabilityServer
        ) -> _ChannelInterfaceModule._WriterInterfaceModule.WriterClient: ...
        class Server(
            _IdentifiableInterfaceModule.Server, _PersistentInterfaceModule.Server
        ):
            class WriteResult(Awaitable[None], Protocol): ...
            class CloseResult(Awaitable[None], Protocol): ...

            class WriteifspaceResult(_DynamicStructBuilder):
                @property
                def success(self) -> bool: ...
                @success.setter
                def success(self, value: bool) -> None: ...

            class WriteifspaceResultTuple(NamedTuple):
                success: bool

            class WriteParams(Protocol):
                value: AnyPointer
                done: None
                noMsg: None

            class WriteCallContext(Protocol):
                params: (
                    _ChannelInterfaceModule._WriterInterfaceModule.Server.WriteParams
                )

            class CloseParams(Protocol): ...

            class CloseCallContext(Protocol):
                params: (
                    _ChannelInterfaceModule._WriterInterfaceModule.Server.CloseParams
                )

            class WriteifspaceParams(Protocol):
                value: AnyPointer
                done: None
                noMsg: None

            class WriteifspaceCallContext(Protocol):
                params: _ChannelInterfaceModule._WriterInterfaceModule.Server.WriteifspaceParams
                @property
                def results(
                    self,
                ) -> _ChannelInterfaceModule._WriterInterfaceModule.Server.WriteifspaceResult: ...

            def write(
                self,
                value: AnyPointer,
                done: None,
                noMsg: None,
                _context: _ChannelInterfaceModule._WriterInterfaceModule.Server.WriteCallContext,
                **kwargs: Any,
            ) -> Awaitable[None]: ...
            def write_context(
                self,
                context: _ChannelInterfaceModule._WriterInterfaceModule.Server.WriteCallContext,
            ) -> Awaitable[None]: ...
            def close(
                self,
                _context: _ChannelInterfaceModule._WriterInterfaceModule.Server.CloseCallContext,
                **kwargs: Any,
            ) -> Awaitable[None]: ...
            def close_context(
                self,
                context: _ChannelInterfaceModule._WriterInterfaceModule.Server.CloseCallContext,
            ) -> Awaitable[None]: ...
            def writeIfSpace(
                self,
                value: AnyPointer,
                done: None,
                noMsg: None,
                _context: _ChannelInterfaceModule._WriterInterfaceModule.Server.WriteifspaceCallContext,
                **kwargs: Any,
            ) -> Awaitable[
                bool
                | _ChannelInterfaceModule._WriterInterfaceModule.Server.WriteifspaceResultTuple
                | None
            ]: ...
            def writeIfSpace_context(
                self,
                context: _ChannelInterfaceModule._WriterInterfaceModule.Server.WriteifspaceCallContext,
            ) -> Awaitable[None]: ...

        class WriterClient(
            _IdentifiableInterfaceModule.IdentifiableClient,
            _PersistentInterfaceModule.PersistentClient,
        ):
            class WriteResult(Awaitable[None], Protocol): ...
            class CloseResult(Awaitable[None], Protocol): ...

            class WriteifspaceResult(Awaitable[WriteifspaceResult], Protocol):
                success: bool

            def write(
                self,
                value: AnyPointer | None = None,
                done: None | None = None,
                noMsg: None | None = None,
            ) -> (
                _ChannelInterfaceModule._WriterInterfaceModule.WriterClient.WriteResult
            ): ...
            def close(
                self,
            ) -> (
                _ChannelInterfaceModule._WriterInterfaceModule.WriterClient.CloseResult
            ): ...
            def writeIfSpace(
                self,
                value: AnyPointer | None = None,
                done: None | None = None,
                noMsg: None | None = None,
            ) -> _ChannelInterfaceModule._WriterInterfaceModule.WriterClient.WriteifspaceResult: ...
            def write_request(
                self,
                value: AnyPointer | None = None,
                done: None | None = None,
                noMsg: None | None = None,
            ) -> _ChannelInterfaceModule._WriterInterfaceModule.WriteRequest: ...
            def close_request(
                self,
            ) -> _ChannelInterfaceModule._WriterInterfaceModule.CloseRequest: ...
            def writeIfSpace_request(
                self,
                value: AnyPointer | None = None,
                done: None | None = None,
                noMsg: None | None = None,
            ) -> _ChannelInterfaceModule._WriterInterfaceModule.WriteifspaceRequest: ...

    Writer: _WriterInterfaceModule
    type WriterClient = _ChannelInterfaceModule._WriterInterfaceModule.WriterClient
    type WriterServer = _ChannelInterfaceModule._WriterInterfaceModule.Server
    class _StartupInfoStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def bufferSize(self) -> int: ...
            @property
            def closeSemantics(self) -> ChannelCloseSemanticsEnum: ...
            @property
            def channelSR(self) -> str: ...
            @property
            def readerSRs(self) -> TextListReader: ...
            @property
            def writerSRs(self) -> TextListReader: ...
            @property
            def channel(self) -> _ChannelInterfaceModule.ChannelClient: ...
            @property
            def readers(self) -> ReaderClientListReader: ...
            @property
            def writers(self) -> WriterClientListReader: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> StartupInfoBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def bufferSize(self) -> int: ...
            @bufferSize.setter
            def bufferSize(self, value: int) -> None: ...
            @property
            def closeSemantics(self) -> ChannelCloseSemanticsEnum: ...
            @closeSemantics.setter
            def closeSemantics(self, value: ChannelCloseSemanticsEnum) -> None: ...
            @property
            def channelSR(self) -> str: ...
            @channelSR.setter
            def channelSR(self, value: str) -> None: ...
            @property
            def readerSRs(self) -> TextListBuilder: ...
            @readerSRs.setter
            def readerSRs(
                self, value: TextListBuilder | TextListReader | dict[str, Any]
            ) -> None: ...
            @property
            def writerSRs(self) -> TextListBuilder: ...
            @writerSRs.setter
            def writerSRs(
                self, value: TextListBuilder | TextListReader | dict[str, Any]
            ) -> None: ...
            @property
            def channel(self) -> _ChannelInterfaceModule.ChannelClient: ...
            @channel.setter
            def channel(
                self,
                value: _ChannelInterfaceModule.ChannelClient
                | _ChannelInterfaceModule.Server,
            ) -> None: ...
            @property
            def readers(self) -> ReaderClientListBuilder: ...
            @readers.setter
            def readers(
                self,
                value: ReaderClientListBuilder
                | ReaderClientListReader
                | dict[str, Any],
            ) -> None: ...
            @property
            def writers(self) -> WriterClientListBuilder: ...
            @writers.setter
            def writers(
                self,
                value: WriterClientListBuilder
                | WriterClientListReader
                | dict[str, Any],
            ) -> None: ...
            @override
            @overload
            def init(
                self, field: Literal["readerSRs"], size: int | None = None
            ) -> TextListBuilder: ...
            @overload
            def init(
                self, field: Literal["writerSRs"], size: int | None = None
            ) -> TextListBuilder: ...
            @overload
            def init(
                self, field: Literal["readers"], size: int | None = None
            ) -> ReaderClientListBuilder: ...
            @overload
            def init(
                self, field: Literal["writers"], size: int | None = None
            ) -> WriterClientListBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...
            @override
            def as_reader(self) -> StartupInfoReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            bufferSize: int | None = None,
            closeSemantics: ChannelCloseSemanticsEnum | None = None,
            channelSR: str | None = None,
            readerSRs: TextListBuilder | dict[str, Any] | None = None,
            writerSRs: TextListBuilder | dict[str, Any] | None = None,
            channel: _ChannelInterfaceModule.ChannelClient
            | _ChannelInterfaceModule.Server
            | None = None,
            readers: ReaderClientListBuilder | dict[str, Any] | None = None,
            writers: WriterClientListBuilder | dict[str, Any] | None = None,
            **kwargs: Any,
        ) -> StartupInfoBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[StartupInfoReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[StartupInfoReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[StartupInfoBuilder]: ...
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
        ) -> StartupInfoReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> StartupInfoReader: ...

    type StartupInfoReader = _StartupInfoStructModule.Reader
    type StartupInfoBuilder = _StartupInfoStructModule.Builder
    StartupInfo: _StartupInfoStructModule
    class SetbuffersizeRequest(Protocol):
        size: int
        def send(self) -> _ChannelInterfaceModule.ChannelClient.SetbuffersizeResult: ...

    class ReaderRequest(Protocol):
        def send(self) -> _ChannelInterfaceModule.ChannelClient.ReaderResult: ...

    class WriterRequest(Protocol):
        def send(self) -> _ChannelInterfaceModule.ChannelClient.WriterResult: ...

    class EndpointsRequest(Protocol):
        def send(self) -> _ChannelInterfaceModule.ChannelClient.EndpointsResult: ...

    class SetautoclosesemanticsRequest(Protocol):
        cs: ChannelCloseSemanticsEnum
        def send(
            self,
        ) -> _ChannelInterfaceModule.ChannelClient.SetautoclosesemanticsResult: ...

    class CloseRequest(Protocol):
        waitForEmptyBuffer: bool
        def send(self) -> _ChannelInterfaceModule.ChannelClient.CloseResult: ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _ChannelInterfaceModule.ChannelClient: ...
    class Server(
        _IdentifiableInterfaceModule.Server, _PersistentInterfaceModule.Server
    ):
        class SetbuffersizeResult(Awaitable[None], Protocol): ...

        class ReaderResult(_DynamicStructBuilder):
            @property
            def r(
                self,
            ) -> (
                _ChannelInterfaceModule._ReaderInterfaceModule.Server
                | _ChannelInterfaceModule._ReaderInterfaceModule.ReaderClient
            ): ...
            @r.setter
            def r(
                self,
                value: _ChannelInterfaceModule._ReaderInterfaceModule.Server
                | _ChannelInterfaceModule._ReaderInterfaceModule.ReaderClient,
            ) -> None: ...

        class WriterResult(_DynamicStructBuilder):
            @property
            def w(
                self,
            ) -> (
                _ChannelInterfaceModule._WriterInterfaceModule.Server
                | _ChannelInterfaceModule._WriterInterfaceModule.WriterClient
            ): ...
            @w.setter
            def w(
                self,
                value: _ChannelInterfaceModule._WriterInterfaceModule.Server
                | _ChannelInterfaceModule._WriterInterfaceModule.WriterClient,
            ) -> None: ...

        class EndpointsResult(_DynamicStructBuilder):
            @property
            def r(
                self,
            ) -> (
                _ChannelInterfaceModule._ReaderInterfaceModule.Server
                | _ChannelInterfaceModule._ReaderInterfaceModule.ReaderClient
            ): ...
            @r.setter
            def r(
                self,
                value: _ChannelInterfaceModule._ReaderInterfaceModule.Server
                | _ChannelInterfaceModule._ReaderInterfaceModule.ReaderClient,
            ) -> None: ...
            @property
            def w(
                self,
            ) -> (
                _ChannelInterfaceModule._WriterInterfaceModule.Server
                | _ChannelInterfaceModule._WriterInterfaceModule.WriterClient
            ): ...
            @w.setter
            def w(
                self,
                value: _ChannelInterfaceModule._WriterInterfaceModule.Server
                | _ChannelInterfaceModule._WriterInterfaceModule.WriterClient,
            ) -> None: ...

        class SetautoclosesemanticsResult(Awaitable[None], Protocol): ...
        class CloseResult(Awaitable[None], Protocol): ...

        class ReaderResultTuple(NamedTuple):
            r: (
                _ChannelInterfaceModule._ReaderInterfaceModule.Server
                | _ChannelInterfaceModule._ReaderInterfaceModule.ReaderClient
            )

        class WriterResultTuple(NamedTuple):
            w: (
                _ChannelInterfaceModule._WriterInterfaceModule.Server
                | _ChannelInterfaceModule._WriterInterfaceModule.WriterClient
            )

        class EndpointsResultTuple(NamedTuple):
            r: (
                _ChannelInterfaceModule._ReaderInterfaceModule.Server
                | _ChannelInterfaceModule._ReaderInterfaceModule.ReaderClient
            )
            w: (
                _ChannelInterfaceModule._WriterInterfaceModule.Server
                | _ChannelInterfaceModule._WriterInterfaceModule.WriterClient
            )

        class SetbuffersizeParams(Protocol):
            size: int

        class SetbuffersizeCallContext(Protocol):
            params: _ChannelInterfaceModule.Server.SetbuffersizeParams

        class ReaderParams(Protocol): ...

        class ReaderCallContext(Protocol):
            params: _ChannelInterfaceModule.Server.ReaderParams
            @property
            def results(self) -> _ChannelInterfaceModule.Server.ReaderResult: ...

        class WriterParams(Protocol): ...

        class WriterCallContext(Protocol):
            params: _ChannelInterfaceModule.Server.WriterParams
            @property
            def results(self) -> _ChannelInterfaceModule.Server.WriterResult: ...

        class EndpointsParams(Protocol): ...

        class EndpointsCallContext(Protocol):
            params: _ChannelInterfaceModule.Server.EndpointsParams
            @property
            def results(self) -> _ChannelInterfaceModule.Server.EndpointsResult: ...

        class SetautoclosesemanticsParams(Protocol):
            cs: ChannelCloseSemanticsEnum

        class SetautoclosesemanticsCallContext(Protocol):
            params: _ChannelInterfaceModule.Server.SetautoclosesemanticsParams

        class CloseParams(Protocol):
            waitForEmptyBuffer: bool

        class CloseCallContext(Protocol):
            params: _ChannelInterfaceModule.Server.CloseParams

        def setBufferSize(
            self,
            size: int,
            _context: _ChannelInterfaceModule.Server.SetbuffersizeCallContext,
            **kwargs: Any,
        ) -> Awaitable[None]: ...
        def setBufferSize_context(
            self, context: _ChannelInterfaceModule.Server.SetbuffersizeCallContext
        ) -> Awaitable[None]: ...
        def reader(
            self,
            _context: _ChannelInterfaceModule.Server.ReaderCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            _ChannelInterfaceModule._ReaderInterfaceModule.Server
            | _ChannelInterfaceModule.Server.ReaderResultTuple
            | None
        ]: ...
        def reader_context(
            self, context: _ChannelInterfaceModule.Server.ReaderCallContext
        ) -> Awaitable[None]: ...
        def writer(
            self,
            _context: _ChannelInterfaceModule.Server.WriterCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            _ChannelInterfaceModule._WriterInterfaceModule.Server
            | _ChannelInterfaceModule.Server.WriterResultTuple
            | None
        ]: ...
        def writer_context(
            self, context: _ChannelInterfaceModule.Server.WriterCallContext
        ) -> Awaitable[None]: ...
        def endpoints(
            self,
            _context: _ChannelInterfaceModule.Server.EndpointsCallContext,
            **kwargs: Any,
        ) -> Awaitable[_ChannelInterfaceModule.Server.EndpointsResultTuple | None]: ...
        def endpoints_context(
            self, context: _ChannelInterfaceModule.Server.EndpointsCallContext
        ) -> Awaitable[None]: ...
        def setAutoCloseSemantics(
            self,
            cs: ChannelCloseSemanticsEnum,
            _context: _ChannelInterfaceModule.Server.SetautoclosesemanticsCallContext,
            **kwargs: Any,
        ) -> Awaitable[None]: ...
        def setAutoCloseSemantics_context(
            self,
            context: _ChannelInterfaceModule.Server.SetautoclosesemanticsCallContext,
        ) -> Awaitable[None]: ...
        def close(
            self,
            waitForEmptyBuffer: bool,
            _context: _ChannelInterfaceModule.Server.CloseCallContext,
            **kwargs: Any,
        ) -> Awaitable[None]: ...
        def close_context(
            self, context: _ChannelInterfaceModule.Server.CloseCallContext
        ) -> Awaitable[None]: ...

    class ChannelClient(
        _IdentifiableInterfaceModule.IdentifiableClient,
        _PersistentInterfaceModule.PersistentClient,
    ):
        class SetbuffersizeResult(Awaitable[None], Protocol): ...

        class ReaderResult(Awaitable[ReaderResult], Protocol):
            r: _ChannelInterfaceModule._ReaderInterfaceModule.ReaderClient

        class WriterResult(Awaitable[WriterResult], Protocol):
            w: _ChannelInterfaceModule._WriterInterfaceModule.WriterClient

        class EndpointsResult(Awaitable[EndpointsResult], Protocol):
            r: _ChannelInterfaceModule._ReaderInterfaceModule.ReaderClient
            w: _ChannelInterfaceModule._WriterInterfaceModule.WriterClient

        class SetautoclosesemanticsResult(Awaitable[None], Protocol): ...
        class CloseResult(Awaitable[None], Protocol): ...

        def setBufferSize(
            self, size: int | None = None
        ) -> _ChannelInterfaceModule.ChannelClient.SetbuffersizeResult: ...
        def reader(self) -> _ChannelInterfaceModule.ChannelClient.ReaderResult: ...
        def writer(self) -> _ChannelInterfaceModule.ChannelClient.WriterResult: ...
        def endpoints(
            self,
        ) -> _ChannelInterfaceModule.ChannelClient.EndpointsResult: ...
        def setAutoCloseSemantics(
            self, cs: ChannelCloseSemanticsEnum | None = None
        ) -> _ChannelInterfaceModule.ChannelClient.SetautoclosesemanticsResult: ...
        def close(
            self, waitForEmptyBuffer: bool | None = None
        ) -> _ChannelInterfaceModule.ChannelClient.CloseResult: ...
        def setBufferSize_request(
            self, size: int | None = None
        ) -> _ChannelInterfaceModule.SetbuffersizeRequest: ...
        def reader_request(self) -> _ChannelInterfaceModule.ReaderRequest: ...
        def writer_request(self) -> _ChannelInterfaceModule.WriterRequest: ...
        def endpoints_request(self) -> _ChannelInterfaceModule.EndpointsRequest: ...
        def setAutoCloseSemantics_request(
            self, cs: ChannelCloseSemanticsEnum | None = None
        ) -> _ChannelInterfaceModule.SetautoclosesemanticsRequest: ...
        def close_request(
            self, waitForEmptyBuffer: bool | None = None
        ) -> _ChannelInterfaceModule.CloseRequest: ...

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

class _ReaderClientList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> ReaderClient: ...
        @override
        def __iter__(self) -> Iterator[ReaderClient]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> ReaderClient: ...
        @override
        def __setitem__(
            self,
            key: int,
            value: ReaderClient | _ChannelInterfaceModule._ReaderInterfaceModule.Server,
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[ReaderClient]: ...

class _WriterClientList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> WriterClient: ...
        @override
        def __iter__(self) -> Iterator[WriterClient]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> WriterClient: ...
        @override
        def __setitem__(
            self,
            key: int,
            value: WriterClient | _ChannelInterfaceModule._WriterInterfaceModule.Server,
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[WriterClient]: ...

Channel: _ChannelInterfaceModule

class _StartChannelsServiceInterfaceModule(_IdentifiableInterfaceModule):
    class _ParamsStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def name(self) -> str: ...
            @property
            def noOfChannels(self) -> int: ...
            @property
            def noOfReaders(self) -> int: ...
            @property
            def noOfWriters(self) -> int: ...
            @property
            def readerSrts(self) -> TextListReader: ...
            @property
            def writerSrts(self) -> TextListReader: ...
            @property
            def bufferSize(self) -> int: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> ParamsBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def name(self) -> str: ...
            @name.setter
            def name(self, value: str) -> None: ...
            @property
            def noOfChannels(self) -> int: ...
            @noOfChannels.setter
            def noOfChannels(self, value: int) -> None: ...
            @property
            def noOfReaders(self) -> int: ...
            @noOfReaders.setter
            def noOfReaders(self, value: int) -> None: ...
            @property
            def noOfWriters(self) -> int: ...
            @noOfWriters.setter
            def noOfWriters(self, value: int) -> None: ...
            @property
            def readerSrts(self) -> TextListBuilder: ...
            @readerSrts.setter
            def readerSrts(
                self, value: TextListBuilder | TextListReader | dict[str, Any]
            ) -> None: ...
            @property
            def writerSrts(self) -> TextListBuilder: ...
            @writerSrts.setter
            def writerSrts(
                self, value: TextListBuilder | TextListReader | dict[str, Any]
            ) -> None: ...
            @property
            def bufferSize(self) -> int: ...
            @bufferSize.setter
            def bufferSize(self, value: int) -> None: ...
            @override
            @overload
            def init(
                self, field: Literal["readerSrts"], size: int | None = None
            ) -> TextListBuilder: ...
            @overload
            def init(
                self, field: Literal["writerSrts"], size: int | None = None
            ) -> TextListBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...
            @override
            def as_reader(self) -> ParamsReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            name: str | None = None,
            noOfChannels: int | None = None,
            noOfReaders: int | None = None,
            noOfWriters: int | None = None,
            readerSrts: TextListBuilder | dict[str, Any] | None = None,
            writerSrts: TextListBuilder | dict[str, Any] | None = None,
            bufferSize: int | None = None,
            **kwargs: Any,
        ) -> ParamsBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[ParamsReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[ParamsReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[ParamsBuilder]: ...
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
        ) -> ParamsReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> ParamsReader: ...

    type ParamsReader = _ParamsStructModule.Reader
    type ParamsBuilder = _ParamsStructModule.Builder
    Params: _ParamsStructModule
    class StartRequest(Protocol):
        name: str
        noOfChannels: int
        noOfReaders: int
        noOfWriters: int
        readerSrts: TextListBuilder | TextListReader | Sequence[Any]
        writerSrts: TextListBuilder | TextListReader | Sequence[Any]
        bufferSize: int
        @overload
        def init(
            self, name: Literal["readerSrts"], size: int = ...
        ) -> TextListBuilder: ...
        @overload
        def init(
            self, name: Literal["writerSrts"], size: int = ...
        ) -> TextListBuilder: ...
        @overload
        def init(self, name: str, size: int = ...) -> Any: ...
        def send(
            self,
        ) -> (
            _StartChannelsServiceInterfaceModule.StartChannelsServiceClient.StartResult
        ): ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _StartChannelsServiceInterfaceModule.StartChannelsServiceClient: ...
    class Server(_IdentifiableInterfaceModule.Server):
        class StartResult(_DynamicStructBuilder):
            @property
            def startupInfos(self) -> StartupInfoListBuilder: ...
            @startupInfos.setter
            def startupInfos(
                self,
                value: StartupInfoListBuilder | StartupInfoListReader | Sequence[Any],
            ) -> None: ...
            @property
            def stop(
                self,
            ) -> (
                _StoppableInterfaceModule.Server
                | _StoppableInterfaceModule.StoppableClient
            ): ...
            @stop.setter
            def stop(
                self,
                value: _StoppableInterfaceModule.Server
                | _StoppableInterfaceModule.StoppableClient,
            ) -> None: ...
            @overload
            def init(
                self, field: Literal["startupInfos"], size: int | None = None
            ) -> StartupInfoListBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...

        class StartResultTuple(NamedTuple):
            startupInfos: StartupInfoListBuilder | StartupInfoListReader
            stop: (
                _StoppableInterfaceModule.Server
                | _StoppableInterfaceModule.StoppableClient
            )

        class StartParams(Protocol):
            name: str
            noOfChannels: int
            noOfReaders: int
            noOfWriters: int
            readerSrts: TextListReader
            writerSrts: TextListReader
            bufferSize: int

        class StartCallContext(Protocol):
            params: _StartChannelsServiceInterfaceModule.Server.StartParams
            @property
            def results(
                self,
            ) -> _StartChannelsServiceInterfaceModule.Server.StartResult: ...

        def start(
            self,
            name: str,
            noOfChannels: int,
            noOfReaders: int,
            noOfWriters: int,
            readerSrts: TextListReader,
            writerSrts: TextListReader,
            bufferSize: int,
            _context: _StartChannelsServiceInterfaceModule.Server.StartCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            _StartChannelsServiceInterfaceModule.Server.StartResultTuple | None
        ]: ...
        def start_context(
            self, context: _StartChannelsServiceInterfaceModule.Server.StartCallContext
        ) -> Awaitable[None]: ...

    class StartChannelsServiceClient(_IdentifiableInterfaceModule.IdentifiableClient):
        class StartResult(Awaitable[StartResult], Protocol):
            startupInfos: StartupInfoListReader
            stop: _StoppableInterfaceModule.StoppableClient

        def start(
            self,
            name: str | None = None,
            noOfChannels: int | None = None,
            noOfReaders: int | None = None,
            noOfWriters: int | None = None,
            readerSrts: TextListBuilder | TextListReader | Sequence[Any] | None = None,
            writerSrts: TextListBuilder | TextListReader | Sequence[Any] | None = None,
            bufferSize: int | None = None,
        ) -> (
            _StartChannelsServiceInterfaceModule.StartChannelsServiceClient.StartResult
        ): ...
        def start_request(
            self,
            name: str | None = None,
            noOfChannels: int | None = None,
            noOfReaders: int | None = None,
            noOfWriters: int | None = None,
            readerSrts: TextListBuilder | TextListReader | Sequence[Any] | None = None,
            writerSrts: TextListBuilder | TextListReader | Sequence[Any] | None = None,
            bufferSize: int | None = None,
        ) -> _StartChannelsServiceInterfaceModule.StartRequest: ...

class _StartupInfoList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> StartupInfoReader: ...
        @override
        def __iter__(self) -> Iterator[StartupInfoReader]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> StartupInfoBuilder: ...
        @override
        def __setitem__(
            self,
            key: int,
            value: StartupInfoReader | StartupInfoBuilder | dict[str, Any],
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[StartupInfoBuilder]: ...
        @override
        def init(self, index: int, size: int | None = None) -> StartupInfoBuilder: ...

StartChannelsService: _StartChannelsServiceInterfaceModule

class _NameAndSRList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> NameAndSRReader: ...
        @override
        def __iter__(self) -> Iterator[NameAndSRReader]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> NameAndSRBuilder: ...
        @override
        def __setitem__(
            self, key: int, value: NameAndSRReader | NameAndSRBuilder | dict[str, Any]
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[NameAndSRBuilder]: ...
        @override
        def init(self, index: int, size: int | None = None) -> NameAndSRBuilder: ...

class _PortInfosStructModule(_StructModule):
    class _NameAndSRStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def name(self) -> str: ...
            @property
            def sr(self) -> str: ...
            @property
            def srs(self) -> TextListReader: ...
            @override
            def which(self) -> Literal["sr", "srs"]: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> NameAndSRBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def name(self) -> str: ...
            @name.setter
            def name(self, value: str) -> None: ...
            @property
            def sr(self) -> str: ...
            @sr.setter
            def sr(self, value: str) -> None: ...
            @property
            def srs(self) -> TextListBuilder: ...
            @srs.setter
            def srs(
                self, value: TextListBuilder | TextListReader | dict[str, Any]
            ) -> None: ...
            @override
            def which(self) -> Literal["sr", "srs"]: ...
            @override
            def init(
                self, field: Literal["srs"], size: int | None = None
            ) -> TextListBuilder: ...
            @override
            def as_reader(self) -> NameAndSRReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            name: str | None = None,
            sr: str | None = None,
            srs: TextListBuilder | dict[str, Any] | None = None,
            **kwargs: Any,
        ) -> NameAndSRBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[NameAndSRReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[NameAndSRReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[NameAndSRBuilder]: ...
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
        ) -> NameAndSRReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> NameAndSRReader: ...

    type NameAndSRReader = _NameAndSRStructModule.Reader
    type NameAndSRBuilder = _NameAndSRStructModule.Builder
    NameAndSR: _NameAndSRStructModule
    class Reader(_DynamicStructReader):
        @property
        def inPorts(self) -> NameAndSRListReader: ...
        @property
        def outPorts(self) -> NameAndSRListReader: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> PortInfosBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def inPorts(self) -> NameAndSRListBuilder: ...
        @inPorts.setter
        def inPorts(
            self, value: NameAndSRListBuilder | NameAndSRListReader | dict[str, Any]
        ) -> None: ...
        @property
        def outPorts(self) -> NameAndSRListBuilder: ...
        @outPorts.setter
        def outPorts(
            self, value: NameAndSRListBuilder | NameAndSRListReader | dict[str, Any]
        ) -> None: ...
        @override
        @overload
        def init(
            self, field: Literal["inPorts"], size: int | None = None
        ) -> NameAndSRListBuilder: ...
        @overload
        def init(
            self, field: Literal["outPorts"], size: int | None = None
        ) -> NameAndSRListBuilder: ...
        @overload
        def init(self, field: str, size: int | None = None) -> Any: ...
        @override
        def as_reader(self) -> PortInfosReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        inPorts: NameAndSRListBuilder | dict[str, Any] | None = None,
        outPorts: NameAndSRListBuilder | dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> PortInfosBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[PortInfosReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[PortInfosReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[PortInfosBuilder]: ...
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
    ) -> PortInfosReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> PortInfosReader: ...

PortInfos: _PortInfosStructModule

class _PortList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> PortReader: ...
        @override
        def __iter__(self) -> Iterator[PortReader]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> PortBuilder: ...
        @override
        def __setitem__(
            self, key: int, value: PortReader | PortBuilder | dict[str, Any]
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[PortBuilder]: ...
        @override
        def init(self, index: int, size: int | None = None) -> PortBuilder: ...

class _ComponentStructModule(_StructModule):
    class _RunnableInterfaceModule(_IdentifiableInterfaceModule):
        class StartRequest(Protocol):
            portInfosReaderSr: str
            name: str
            def send(
                self,
            ) -> _ComponentStructModule._RunnableInterfaceModule.RunnableClient.StartResult: ...

        class StopRequest(Protocol):
            def send(
                self,
            ) -> _ComponentStructModule._RunnableInterfaceModule.RunnableClient.StopResult: ...

        @override
        def _new_client(
            self, server: _DynamicCapabilityServer
        ) -> _ComponentStructModule._RunnableInterfaceModule.RunnableClient: ...
        class Server(_IdentifiableInterfaceModule.Server):
            class StartResult(_DynamicStructBuilder):
                @property
                def success(self) -> bool: ...
                @success.setter
                def success(self, value: bool) -> None: ...

            class StopResult(_DynamicStructBuilder):
                @property
                def success(self) -> bool: ...
                @success.setter
                def success(self, value: bool) -> None: ...

            class StartResultTuple(NamedTuple):
                success: bool

            class StopResultTuple(NamedTuple):
                success: bool

            class StartParams(Protocol):
                portInfosReaderSr: str
                name: str

            class StartCallContext(Protocol):
                params: (
                    _ComponentStructModule._RunnableInterfaceModule.Server.StartParams
                )
                @property
                def results(
                    self,
                ) -> (
                    _ComponentStructModule._RunnableInterfaceModule.Server.StartResult
                ): ...

            class StopParams(Protocol): ...

            class StopCallContext(Protocol):
                params: (
                    _ComponentStructModule._RunnableInterfaceModule.Server.StopParams
                )
                @property
                def results(
                    self,
                ) -> (
                    _ComponentStructModule._RunnableInterfaceModule.Server.StopResult
                ): ...

            def start(
                self,
                portInfosReaderSr: str,
                name: str,
                _context: _ComponentStructModule._RunnableInterfaceModule.Server.StartCallContext,
                **kwargs: Any,
            ) -> Awaitable[
                bool
                | _ComponentStructModule._RunnableInterfaceModule.Server.StartResultTuple
                | None
            ]: ...
            def start_context(
                self,
                context: _ComponentStructModule._RunnableInterfaceModule.Server.StartCallContext,
            ) -> Awaitable[None]: ...
            def stop(
                self,
                _context: _ComponentStructModule._RunnableInterfaceModule.Server.StopCallContext,
                **kwargs: Any,
            ) -> Awaitable[
                bool
                | _ComponentStructModule._RunnableInterfaceModule.Server.StopResultTuple
                | None
            ]: ...
            def stop_context(
                self,
                context: _ComponentStructModule._RunnableInterfaceModule.Server.StopCallContext,
            ) -> Awaitable[None]: ...

        class RunnableClient(_IdentifiableInterfaceModule.IdentifiableClient):
            class StartResult(Awaitable[StartResult], Protocol):
                success: bool

            class StopResult(Awaitable[StopResult], Protocol):
                success: bool

            def start(
                self, portInfosReaderSr: str | None = None, name: str | None = None
            ) -> _ComponentStructModule._RunnableInterfaceModule.RunnableClient.StartResult: ...
            def stop(
                self,
            ) -> _ComponentStructModule._RunnableInterfaceModule.RunnableClient.StopResult: ...
            def start_request(
                self, portInfosReaderSr: str | None = None, name: str | None = None
            ) -> _ComponentStructModule._RunnableInterfaceModule.StartRequest: ...
            def stop_request(
                self,
            ) -> _ComponentStructModule._RunnableInterfaceModule.StopRequest: ...

    Runnable: _RunnableInterfaceModule
    type RunnableClient = _ComponentStructModule._RunnableInterfaceModule.RunnableClient
    type RunnableServer = _ComponentStructModule._RunnableInterfaceModule.Server
    class _RunnableFactoryInterfaceModule(_IdentifiableInterfaceModule):
        class CreateRequest(Protocol):
            def send(
                self,
            ) -> _ComponentStructModule._RunnableFactoryInterfaceModule.RunnableFactoryClient.CreateResult: ...

        @override
        def _new_client(
            self, server: _DynamicCapabilityServer
        ) -> (
            _ComponentStructModule._RunnableFactoryInterfaceModule.RunnableFactoryClient
        ): ...
        class Server(_IdentifiableInterfaceModule.Server):
            class CreateResult(_DynamicStructBuilder):
                @property
                def r(
                    self,
                ) -> (
                    _ComponentStructModule._RunnableInterfaceModule.Server
                    | _ComponentStructModule._RunnableInterfaceModule.RunnableClient
                ): ...
                @r.setter
                def r(
                    self,
                    value: _ComponentStructModule._RunnableInterfaceModule.Server
                    | _ComponentStructModule._RunnableInterfaceModule.RunnableClient,
                ) -> None: ...

            class CreateResultTuple(NamedTuple):
                r: (
                    _ComponentStructModule._RunnableInterfaceModule.Server
                    | _ComponentStructModule._RunnableInterfaceModule.RunnableClient
                )

            class CreateParams(Protocol): ...

            class CreateCallContext(Protocol):
                params: _ComponentStructModule._RunnableFactoryInterfaceModule.Server.CreateParams
                @property
                def results(
                    self,
                ) -> _ComponentStructModule._RunnableFactoryInterfaceModule.Server.CreateResult: ...

            def create(
                self,
                _context: _ComponentStructModule._RunnableFactoryInterfaceModule.Server.CreateCallContext,
                **kwargs: Any,
            ) -> Awaitable[
                _ComponentStructModule._RunnableInterfaceModule.Server
                | _ComponentStructModule._RunnableFactoryInterfaceModule.Server.CreateResultTuple
                | None
            ]: ...
            def create_context(
                self,
                context: _ComponentStructModule._RunnableFactoryInterfaceModule.Server.CreateCallContext,
            ) -> Awaitable[None]: ...

        class RunnableFactoryClient(_IdentifiableInterfaceModule.IdentifiableClient):
            class CreateResult(Awaitable[CreateResult], Protocol):
                r: _ComponentStructModule._RunnableInterfaceModule.RunnableClient

            def create(
                self,
            ) -> _ComponentStructModule._RunnableFactoryInterfaceModule.RunnableFactoryClient.CreateResult: ...
            def create_request(
                self,
            ) -> (
                _ComponentStructModule._RunnableFactoryInterfaceModule.CreateRequest
            ): ...

    RunnableFactory: _RunnableFactoryInterfaceModule
    type RunnableFactoryClient = (
        _ComponentStructModule._RunnableFactoryInterfaceModule.RunnableFactoryClient
    )
    type RunnableFactoryServer = (
        _ComponentStructModule._RunnableFactoryInterfaceModule.Server
    )
    class _ComponentTypeEnumModule:
        standard: int
        iip: int
        subflow: int
        view: int

    ComponentType: _ComponentTypeEnumModule
    class _PortStructModule(_StructModule):
        class _PortTypeEnumModule:
            standard: int

        PortType: _PortTypeEnumModule
        class _ContentTypeEnumModule:
            structuredText: int

        ContentType: _ContentTypeEnumModule
        class Reader(_DynamicStructReader):
            @property
            def name(self) -> str: ...
            @property
            def contentType(self) -> str: ...
            @property
            def type(self) -> ComponentPortPortTypeEnum: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> PortBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def name(self) -> str: ...
            @name.setter
            def name(self, value: str) -> None: ...
            @property
            def contentType(self) -> str: ...
            @contentType.setter
            def contentType(self, value: str) -> None: ...
            @property
            def type(self) -> ComponentPortPortTypeEnum: ...
            @type.setter
            def type(self, value: ComponentPortPortTypeEnum) -> None: ...
            @override
            def as_reader(self) -> PortReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            name: str | None = None,
            contentType: str | None = None,
            type: ComponentPortPortTypeEnum | None = None,
            **kwargs: Any,
        ) -> PortBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[PortReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[PortReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[PortBuilder]: ...
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
        ) -> PortReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> PortReader: ...

    type PortReader = _PortStructModule.Reader
    type PortBuilder = _PortStructModule.Builder
    Port: _PortStructModule
    class Reader(_DynamicStructReader):
        @property
        def info(self) -> IdInformationReader: ...
        @property
        def type(self) -> ComponentComponentTypeEnum: ...
        @property
        def inPorts(self) -> PortListReader: ...
        @property
        def outPorts(self) -> PortListReader: ...
        @property
        def runFactory(
            self,
        ) -> (
            _ComponentStructModule._RunnableFactoryInterfaceModule.RunnableFactoryClient
        ): ...
        @property
        def defaultConfig(self) -> str: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> ComponentBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def info(self) -> IdInformationBuilder: ...
        @info.setter
        def info(
            self, value: IdInformationBuilder | IdInformationReader | dict[str, Any]
        ) -> None: ...
        @property
        def type(self) -> ComponentComponentTypeEnum: ...
        @type.setter
        def type(self, value: ComponentComponentTypeEnum) -> None: ...
        @property
        def inPorts(self) -> PortListBuilder: ...
        @inPorts.setter
        def inPorts(
            self, value: PortListBuilder | PortListReader | dict[str, Any]
        ) -> None: ...
        @property
        def outPorts(self) -> PortListBuilder: ...
        @outPorts.setter
        def outPorts(
            self, value: PortListBuilder | PortListReader | dict[str, Any]
        ) -> None: ...
        @property
        def runFactory(
            self,
        ) -> (
            _ComponentStructModule._RunnableFactoryInterfaceModule.RunnableFactoryClient
        ): ...
        @runFactory.setter
        def runFactory(
            self,
            value: _ComponentStructModule._RunnableFactoryInterfaceModule.RunnableFactoryClient
            | _ComponentStructModule._RunnableFactoryInterfaceModule.Server,
        ) -> None: ...
        @property
        def defaultConfig(self) -> str: ...
        @defaultConfig.setter
        def defaultConfig(self, value: str) -> None: ...
        @override
        @overload
        def init(
            self, field: Literal["info"], size: int | None = None
        ) -> IdInformationBuilder: ...
        @overload
        def init(
            self, field: Literal["inPorts"], size: int | None = None
        ) -> PortListBuilder: ...
        @overload
        def init(
            self, field: Literal["outPorts"], size: int | None = None
        ) -> PortListBuilder: ...
        @overload
        def init(self, field: str, size: int | None = None) -> Any: ...
        @override
        def as_reader(self) -> ComponentReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        info: IdInformationBuilder | dict[str, Any] | None = None,
        type: ComponentComponentTypeEnum | None = None,
        inPorts: PortListBuilder | dict[str, Any] | None = None,
        outPorts: PortListBuilder | dict[str, Any] | None = None,
        runFactory: _ComponentStructModule._RunnableFactoryInterfaceModule.RunnableFactoryClient
        | _ComponentStructModule._RunnableFactoryInterfaceModule.Server
        | None = None,
        defaultConfig: str | None = None,
        **kwargs: Any,
    ) -> ComponentBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[ComponentReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[ComponentReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[ComponentBuilder]: ...
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
    ) -> ComponentReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> ComponentReader: ...

Component: _ComponentStructModule

# Top-level type aliases for use in type annotations
type ChannelClient = _ChannelInterfaceModule.ChannelClient
type ChannelCloseSemanticsEnum = int | Literal["fbp", "no"]
type ChannelServer = _ChannelInterfaceModule.Server
type CloseResult = _ChannelInterfaceModule.ChannelClient.CloseResult
type ComponentBuilder = _ComponentStructModule.Builder
type ComponentComponentTypeEnum = int | Literal["standard", "iip", "subflow", "view"]
type ComponentPortContentTypeEnum = int | Literal["structuredText"]
type ComponentPortPortTypeEnum = int | Literal["standard"]
type ComponentReader = _ComponentStructModule.Reader
type CreateResult = _ComponentStructModule._RunnableFactoryInterfaceModule.RunnableFactoryClient.CreateResult
type EndpointsResult = _ChannelInterfaceModule.ChannelClient.EndpointsResult
type IIPBuilder = _IIPStructModule.Builder
type IIPReader = _IIPStructModule.Reader
type IPBuilder = _IPStructModule.Builder
type IPReader = _IPStructModule.Reader
type IPTypeEnum = int | Literal["standard", "openBracket", "closeBracket"]
type KVBuilder = _IPStructModule._KVStructModule.Builder
type KVListBuilder = _KVList.Builder
type KVListReader = _KVList.Reader
type KVReader = _IPStructModule._KVStructModule.Reader
type MsgBuilder = _ChannelInterfaceModule._MsgStructModule.Builder
type MsgReader = _ChannelInterfaceModule._MsgStructModule.Reader
type NameAndSRBuilder = _PortInfosStructModule._NameAndSRStructModule.Builder
type NameAndSRListBuilder = _NameAndSRList.Builder
type NameAndSRListReader = _NameAndSRList.Reader
type NameAndSRReader = _PortInfosStructModule._NameAndSRStructModule.Reader
type ParamsBuilder = _StartChannelsServiceInterfaceModule._ParamsStructModule.Builder
type ParamsReader = _StartChannelsServiceInterfaceModule._ParamsStructModule.Reader
type PortBuilder = _ComponentStructModule._PortStructModule.Builder
type PortInfosBuilder = _PortInfosStructModule.Builder
type PortInfosReader = _PortInfosStructModule.Reader
type PortListBuilder = _PortList.Builder
type PortListReader = _PortList.Reader
type PortReader = _ComponentStructModule._PortStructModule.Reader
type ReadResult = _ChannelInterfaceModule._ReaderInterfaceModule.ReaderClient.ReadResult
type ReaderClient = _ChannelInterfaceModule._ReaderInterfaceModule.ReaderClient
type ReaderClientListBuilder = _ReaderClientList.Builder
type ReaderClientListReader = _ReaderClientList.Reader
type ReaderResult = _ChannelInterfaceModule.ChannelClient.ReaderResult
type ReaderServer = _ChannelInterfaceModule._ReaderInterfaceModule.Server
type ReadifmsgResult = (
    _ChannelInterfaceModule._ReaderInterfaceModule.ReaderClient.ReadifmsgResult
)
type RunnableClient = _ComponentStructModule._RunnableInterfaceModule.RunnableClient
type RunnableFactoryClient = (
    _ComponentStructModule._RunnableFactoryInterfaceModule.RunnableFactoryClient
)
type RunnableFactoryServer = (
    _ComponentStructModule._RunnableFactoryInterfaceModule.Server
)
type RunnableServer = _ComponentStructModule._RunnableInterfaceModule.Server
type SetautoclosesemanticsResult = (
    _ChannelInterfaceModule.ChannelClient.SetautoclosesemanticsResult
)
type SetbuffersizeResult = _ChannelInterfaceModule.ChannelClient.SetbuffersizeResult
type StartChannelsServiceClient = (
    _StartChannelsServiceInterfaceModule.StartChannelsServiceClient
)
type StartChannelsServiceServer = _StartChannelsServiceInterfaceModule.Server
type StartResult = (
    _ComponentStructModule._RunnableInterfaceModule.RunnableClient.StartResult
)
type StartupInfoBuilder = _ChannelInterfaceModule._StartupInfoStructModule.Builder
type StartupInfoListBuilder = _StartupInfoList.Builder
type StartupInfoListReader = _StartupInfoList.Reader
type StartupInfoReader = _ChannelInterfaceModule._StartupInfoStructModule.Reader
type StopResult = (
    _ComponentStructModule._RunnableInterfaceModule.RunnableClient.StopResult
)
type TextListBuilder = _TextList.Builder
type TextListReader = _TextList.Reader
type WriteResult = (
    _ChannelInterfaceModule._WriterInterfaceModule.WriterClient.WriteResult
)
type WriteifspaceResult = (
    _ChannelInterfaceModule._WriterInterfaceModule.WriterClient.WriteifspaceResult
)
type WriterClient = _ChannelInterfaceModule._WriterInterfaceModule.WriterClient
type WriterClientListBuilder = _WriterClientList.Builder
type WriterClientListReader = _WriterClientList.Reader
type WriterResult = _ChannelInterfaceModule.ChannelClient.WriterResult
type WriterServer = _ChannelInterfaceModule._WriterInterfaceModule.Server
