"""This is an automatically generated stub for `jobs.capnp`."""

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

class _JobStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def data(self) -> _DynamicObjectReader: ...
        @property
        def noFurtherJobs(self) -> bool: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> JobBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def data(self) -> _DynamicObjectReader: ...
        @data.setter
        def data(self, value: AnyPointer) -> None: ...
        @property
        def noFurtherJobs(self) -> bool: ...
        @noFurtherJobs.setter
        def noFurtherJobs(self, value: bool) -> None: ...
        @override
        def as_reader(self) -> JobReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        data: AnyPointer | None = None,
        noFurtherJobs: bool | None = None,
        **kwargs: Any,
    ) -> JobBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[JobReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[JobReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[JobBuilder]: ...
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
    ) -> JobReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> JobReader: ...

Job: _JobStructModule

class _ServiceInterfaceModule(_IdentifiableInterfaceModule, _PersistentInterfaceModule):
    class NextjobRequest(Protocol):
        def send(self) -> _ServiceInterfaceModule.ServiceClient.NextjobResult: ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _ServiceInterfaceModule.ServiceClient: ...
    class Server(
        _IdentifiableInterfaceModule.Server, _PersistentInterfaceModule.Server
    ):
        class NextjobResult(_DynamicStructBuilder):
            @property
            def job(self) -> JobBuilder: ...
            @job.setter
            def job(self, value: JobBuilder | JobReader | dict[str, Any]) -> None: ...
            @overload
            def init(
                self, field: Literal["job"], size: int | None = None
            ) -> JobBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...

        class NextjobResultTuple(NamedTuple):
            job: JobBuilder | JobReader

        class NextjobParams(Protocol): ...

        class NextjobCallContext(Protocol):
            params: _ServiceInterfaceModule.Server.NextjobParams
            @property
            def results(self) -> _ServiceInterfaceModule.Server.NextjobResult: ...

        def nextJob(
            self,
            _context: _ServiceInterfaceModule.Server.NextjobCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            _JobStructModule.Builder
            | _ServiceInterfaceModule.Server.NextjobResultTuple
            | None
        ]: ...
        def nextJob_context(
            self, context: _ServiceInterfaceModule.Server.NextjobCallContext
        ) -> Awaitable[None]: ...

    class ServiceClient(
        _IdentifiableInterfaceModule.IdentifiableClient,
        _PersistentInterfaceModule.PersistentClient,
    ):
        class NextjobResult(Awaitable[NextjobResult], Protocol):
            job: JobReader

        def nextJob(self) -> _ServiceInterfaceModule.ServiceClient.NextjobResult: ...
        def nextJob_request(self) -> _ServiceInterfaceModule.NextjobRequest: ...

Service: _ServiceInterfaceModule

# Top-level type aliases for use in type annotations
type JobBuilder = _JobStructModule.Builder
type JobReader = _JobStructModule.Reader
type NextjobResult = _ServiceInterfaceModule.ServiceClient.NextjobResult
type ServiceClient = _ServiceInterfaceModule.ServiceClient
type ServiceServer = _ServiceInterfaceModule.Server
