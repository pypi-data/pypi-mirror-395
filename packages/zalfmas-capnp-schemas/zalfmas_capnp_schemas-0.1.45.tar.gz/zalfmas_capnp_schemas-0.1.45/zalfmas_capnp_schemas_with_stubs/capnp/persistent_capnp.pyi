"""This is an automatically generated stub for `persistent.capnp`."""

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
from collections.abc import Awaitable, Callable
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

class _PersistentInterfaceModule(_InterfaceModule):
    class _SaveParamsStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def sealFor(self) -> _DynamicObjectReader: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> SaveParamsBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def sealFor(self) -> _DynamicObjectReader: ...
            @sealFor.setter
            def sealFor(self, value: AnyPointer) -> None: ...
            @override
            def as_reader(self) -> SaveParamsReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            sealFor: AnyPointer | None = None,
            **kwargs: Any,
        ) -> SaveParamsBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[SaveParamsReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[SaveParamsReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[SaveParamsBuilder]: ...
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
        ) -> SaveParamsReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> SaveParamsReader: ...

    type SaveParamsReader = _SaveParamsStructModule.Reader
    type SaveParamsBuilder = _SaveParamsStructModule.Builder
    SaveParams: _SaveParamsStructModule
    class _SaveResultsStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def sturdyRef(self) -> _DynamicObjectReader: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> SaveResultsBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def sturdyRef(self) -> _DynamicObjectReader: ...
            @sturdyRef.setter
            def sturdyRef(self, value: AnyPointer) -> None: ...
            @override
            def as_reader(self) -> SaveResultsReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            sturdyRef: AnyPointer | None = None,
            **kwargs: Any,
        ) -> SaveResultsBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[SaveResultsReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[SaveResultsReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[SaveResultsBuilder]: ...
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
        ) -> SaveResultsReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> SaveResultsReader: ...

    type SaveResultsReader = _SaveResultsStructModule.Reader
    type SaveResultsBuilder = _SaveResultsStructModule.Builder
    SaveResults: _SaveResultsStructModule
    class SaveRequest(Protocol):
        sealFor: AnyPointer
        def send(self) -> _PersistentInterfaceModule.PersistentClient.SaveResult: ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _PersistentInterfaceModule.PersistentClient: ...
    class Server(_DynamicCapabilityServer):
        class SaveResult(Awaitable[SaveResult], Protocol):
            sturdyRef: AnyPointer

        class SaveResultTuple(NamedTuple):
            sturdyRef: AnyPointer

        class SaveParams(Protocol):
            sealFor: AnyPointer

        class SaveCallContext(Protocol):
            params: _PersistentInterfaceModule.Server.SaveParams
            @property
            def results(self) -> SaveResultsBuilder: ...

        def save(
            self,
            sealFor: AnyPointer,
            _context: _PersistentInterfaceModule.Server.SaveCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            AnyPointer | _PersistentInterfaceModule.Server.SaveResultTuple | None
        ]: ...
        def save_context(
            self, context: _PersistentInterfaceModule.Server.SaveCallContext
        ) -> Awaitable[None]: ...

    class PersistentClient(_DynamicCapabilityClient):
        class SaveResult(Awaitable[SaveResult], Protocol):
            sturdyRef: _DynamicObjectReader

        def save(
            self, sealFor: AnyPointer | None = None
        ) -> _PersistentInterfaceModule.PersistentClient.SaveResult: ...
        def save_request(
            self, sealFor: AnyPointer | None = None
        ) -> _PersistentInterfaceModule.SaveRequest: ...

Persistent: _PersistentInterfaceModule

# Top-level type aliases for use in type annotations
type PersistentClient = _PersistentInterfaceModule.PersistentClient
type PersistentServer = _PersistentInterfaceModule.Server
type SaveParamsBuilder = _PersistentInterfaceModule._SaveParamsStructModule.Builder
type SaveParamsReader = _PersistentInterfaceModule._SaveParamsStructModule.Reader
type SaveResult = _PersistentInterfaceModule.PersistentClient.SaveResult
type SaveResultsBuilder = _PersistentInterfaceModule._SaveResultsStructModule.Builder
type SaveResultsReader = _PersistentInterfaceModule._SaveResultsStructModule.Reader
