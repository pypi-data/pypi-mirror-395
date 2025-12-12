"""This is an automatically generated stub for `persistence.capnp`."""

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
from .common_capnp import _IdentifiableInterfaceModule
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

# Type alias for Capability parameters
type Capability = (
    _DynamicCapabilityClient
    | _DynamicCapabilityServer
    | _DynamicObjectReader
    | _DynamicObjectBuilder
)

class _VatIdStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def publicKey0(self) -> int: ...
        @property
        def publicKey1(self) -> int: ...
        @property
        def publicKey2(self) -> int: ...
        @property
        def publicKey3(self) -> int: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> VatIdBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def publicKey0(self) -> int: ...
        @publicKey0.setter
        def publicKey0(self, value: int) -> None: ...
        @property
        def publicKey1(self) -> int: ...
        @publicKey1.setter
        def publicKey1(self, value: int) -> None: ...
        @property
        def publicKey2(self) -> int: ...
        @publicKey2.setter
        def publicKey2(self, value: int) -> None: ...
        @property
        def publicKey3(self) -> int: ...
        @publicKey3.setter
        def publicKey3(self, value: int) -> None: ...
        @override
        def as_reader(self) -> VatIdReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        publicKey0: int | None = None,
        publicKey1: int | None = None,
        publicKey2: int | None = None,
        publicKey3: int | None = None,
        **kwargs: Any,
    ) -> VatIdBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[VatIdReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[VatIdReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[VatIdBuilder]: ...
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
    ) -> VatIdReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> VatIdReader: ...

VatId: _VatIdStructModule

class _AddressStructModule(_StructModule):
    class _AddressIp6StructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def lower64(self) -> int: ...
            @property
            def upper64(self) -> int: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> AddressIp6Builder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def lower64(self) -> int: ...
            @lower64.setter
            def lower64(self, value: int) -> None: ...
            @property
            def upper64(self) -> int: ...
            @upper64.setter
            def upper64(self, value: int) -> None: ...
            @override
            def as_reader(self) -> AddressIp6Reader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            lower64: int | None = None,
            upper64: int | None = None,
            **kwargs: Any,
        ) -> AddressIp6Builder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[AddressIp6Reader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[AddressIp6Reader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[AddressIp6Builder]: ...
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
        ) -> AddressIp6Reader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AddressIp6Reader: ...

    type AddressIp6Reader = _AddressIp6StructModule.Reader
    type AddressIp6Builder = _AddressIp6StructModule.Builder
    AddressIp6: _AddressIp6StructModule
    class Reader(_DynamicStructReader):
        @property
        def ip6(self) -> AddressIp6Reader: ...
        @property
        def port(self) -> int: ...
        @property
        def host(self) -> str: ...
        @override
        def which(self) -> Literal["ip6", "host"]: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> AddressBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def ip6(self) -> AddressIp6Builder: ...
        @ip6.setter
        def ip6(
            self, value: AddressIp6Builder | AddressIp6Reader | dict[str, Any]
        ) -> None: ...
        @property
        def port(self) -> int: ...
        @port.setter
        def port(self, value: int) -> None: ...
        @property
        def host(self) -> str: ...
        @host.setter
        def host(self, value: str) -> None: ...
        @override
        def which(self) -> Literal["ip6", "host"]: ...
        @override
        def init(
            self, field: Literal["ip6"], size: int | None = None
        ) -> AddressIp6Builder: ...
        @override
        def as_reader(self) -> AddressReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ip6: AddressIp6Builder | dict[str, Any] | None = None,
        port: int | None = None,
        host: str | None = None,
        **kwargs: Any,
    ) -> AddressBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[AddressReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[AddressReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[AddressBuilder]: ...
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
    ) -> AddressReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AddressReader: ...

Address: _AddressStructModule

class _VatPathStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def id(self) -> VatIdReader: ...
        @property
        def address(self) -> AddressReader: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> VatPathBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def id(self) -> VatIdBuilder: ...
        @id.setter
        def id(self, value: VatIdBuilder | VatIdReader | dict[str, Any]) -> None: ...
        @property
        def address(self) -> AddressBuilder: ...
        @address.setter
        def address(
            self, value: AddressBuilder | AddressReader | dict[str, Any]
        ) -> None: ...
        @override
        @overload
        def init(
            self, field: Literal["id"], size: int | None = None
        ) -> VatIdBuilder: ...
        @overload
        def init(
            self, field: Literal["address"], size: int | None = None
        ) -> AddressBuilder: ...
        @overload
        def init(self, field: str, size: int | None = None) -> Any: ...
        @override
        def as_reader(self) -> VatPathReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        id: VatIdBuilder | dict[str, Any] | None = None,
        address: AddressBuilder | dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> VatPathBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[VatPathReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[VatPathReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[VatPathBuilder]: ...
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
    ) -> VatPathReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> VatPathReader: ...

VatPath: _VatPathStructModule

class _SturdyRefStructModule(_StructModule):
    class _OwnerStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def guid(self) -> str: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> OwnerBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def guid(self) -> str: ...
            @guid.setter
            def guid(self, value: str) -> None: ...
            @override
            def as_reader(self) -> OwnerReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            guid: str | None = None,
            **kwargs: Any,
        ) -> OwnerBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[OwnerReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[OwnerReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[OwnerBuilder]: ...
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
        ) -> OwnerReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> OwnerReader: ...

    type OwnerReader = _OwnerStructModule.Reader
    type OwnerBuilder = _OwnerStructModule.Builder
    Owner: _OwnerStructModule
    class _TokenStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def text(self) -> str: ...
            @property
            def data(self) -> bytes: ...
            @override
            def which(self) -> Literal["text", "data"]: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> TokenBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def text(self) -> str: ...
            @text.setter
            def text(self, value: str) -> None: ...
            @property
            def data(self) -> bytes: ...
            @data.setter
            def data(self, value: bytes) -> None: ...
            @override
            def which(self) -> Literal["text", "data"]: ...
            @override
            def as_reader(self) -> TokenReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            text: str | None = None,
            data: bytes | None = None,
            **kwargs: Any,
        ) -> TokenBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[TokenReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[TokenReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[TokenBuilder]: ...
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
        ) -> TokenReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> TokenReader: ...

    type TokenReader = _TokenStructModule.Reader
    type TokenBuilder = _TokenStructModule.Builder
    Token: _TokenStructModule
    class Reader(_DynamicStructReader):
        @property
        def vat(self) -> VatPathReader: ...
        @property
        def localRef(self) -> TokenReader: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> SturdyRefBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def vat(self) -> VatPathBuilder: ...
        @vat.setter
        def vat(
            self, value: VatPathBuilder | VatPathReader | dict[str, Any]
        ) -> None: ...
        @property
        def localRef(self) -> TokenBuilder: ...
        @localRef.setter
        def localRef(
            self, value: TokenBuilder | TokenReader | dict[str, Any]
        ) -> None: ...
        @override
        @overload
        def init(
            self, field: Literal["vat"], size: int | None = None
        ) -> VatPathBuilder: ...
        @overload
        def init(
            self, field: Literal["localRef"], size: int | None = None
        ) -> TokenBuilder: ...
        @overload
        def init(self, field: str, size: int | None = None) -> Any: ...
        @override
        def as_reader(self) -> SturdyRefReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        vat: VatPathBuilder | dict[str, Any] | None = None,
        localRef: TokenBuilder | dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> SturdyRefBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[SturdyRefReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[SturdyRefReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[SturdyRefBuilder]: ...
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
    ) -> SturdyRefReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> SturdyRefReader: ...

SturdyRef: _SturdyRefStructModule

class _HeartbeatInterfaceModule(_InterfaceModule):
    class BeatRequest(Protocol):
        def send(self) -> _HeartbeatInterfaceModule.HeartbeatClient.BeatResult: ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _HeartbeatInterfaceModule.HeartbeatClient: ...
    class Server(_DynamicCapabilityServer):
        class BeatResult(Awaitable[None], Protocol): ...
        class BeatParams(Protocol): ...

        class BeatCallContext(Protocol):
            params: _HeartbeatInterfaceModule.Server.BeatParams

        def beat(
            self,
            _context: _HeartbeatInterfaceModule.Server.BeatCallContext,
            **kwargs: Any,
        ) -> Awaitable[None]: ...
        def beat_context(
            self, context: _HeartbeatInterfaceModule.Server.BeatCallContext
        ) -> Awaitable[None]: ...

    class HeartbeatClient(_DynamicCapabilityClient):
        class BeatResult(Awaitable[None], Protocol): ...

        def beat(self) -> _HeartbeatInterfaceModule.HeartbeatClient.BeatResult: ...
        def beat_request(self) -> _HeartbeatInterfaceModule.BeatRequest: ...

Heartbeat: _HeartbeatInterfaceModule

class _PersistentInterfaceModule(_InterfaceModule):
    class _SaveParamsStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def sealFor(self) -> OwnerReader: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> SaveParamsBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def sealFor(self) -> OwnerBuilder: ...
            @sealFor.setter
            def sealFor(
                self, value: OwnerBuilder | OwnerReader | dict[str, Any]
            ) -> None: ...
            @override
            def init(
                self, field: Literal["sealFor"], size: int | None = None
            ) -> OwnerBuilder: ...
            @override
            def as_reader(self) -> SaveParamsReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            sealFor: OwnerBuilder | dict[str, Any] | None = None,
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
            def sturdyRef(self) -> SturdyRefReader: ...
            @property
            def unsaveSR(self) -> SturdyRefReader: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> SaveResultsBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def sturdyRef(self) -> SturdyRefBuilder: ...
            @sturdyRef.setter
            def sturdyRef(
                self, value: SturdyRefBuilder | SturdyRefReader | dict[str, Any]
            ) -> None: ...
            @property
            def unsaveSR(self) -> SturdyRefBuilder: ...
            @unsaveSR.setter
            def unsaveSR(
                self, value: SturdyRefBuilder | SturdyRefReader | dict[str, Any]
            ) -> None: ...
            @override
            @overload
            def init(
                self, field: Literal["sturdyRef"], size: int | None = None
            ) -> SturdyRefBuilder: ...
            @overload
            def init(
                self, field: Literal["unsaveSR"], size: int | None = None
            ) -> SturdyRefBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...
            @override
            def as_reader(self) -> SaveResultsReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            sturdyRef: SturdyRefBuilder | dict[str, Any] | None = None,
            unsaveSR: SturdyRefBuilder | dict[str, Any] | None = None,
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
    class _ReleaseSturdyRefInterfaceModule(_InterfaceModule):
        class ReleaseRequest(Protocol):
            def send(
                self,
            ) -> _PersistentInterfaceModule._ReleaseSturdyRefInterfaceModule.ReleaseSturdyRefClient.ReleaseResult: ...

        @override
        def _new_client(
            self, server: _DynamicCapabilityServer
        ) -> _PersistentInterfaceModule._ReleaseSturdyRefInterfaceModule.ReleaseSturdyRefClient: ...
        class Server(_DynamicCapabilityServer):
            class ReleaseResult(_DynamicStructBuilder):
                @property
                def success(self) -> bool: ...
                @success.setter
                def success(self, value: bool) -> None: ...

            class ReleaseResultTuple(NamedTuple):
                success: bool

            class ReleaseParams(Protocol): ...

            class ReleaseCallContext(Protocol):
                params: _PersistentInterfaceModule._ReleaseSturdyRefInterfaceModule.Server.ReleaseParams
                @property
                def results(
                    self,
                ) -> _PersistentInterfaceModule._ReleaseSturdyRefInterfaceModule.Server.ReleaseResult: ...

            def release(
                self,
                _context: _PersistentInterfaceModule._ReleaseSturdyRefInterfaceModule.Server.ReleaseCallContext,
                **kwargs: Any,
            ) -> Awaitable[
                bool
                | _PersistentInterfaceModule._ReleaseSturdyRefInterfaceModule.Server.ReleaseResultTuple
                | None
            ]: ...
            def release_context(
                self,
                context: _PersistentInterfaceModule._ReleaseSturdyRefInterfaceModule.Server.ReleaseCallContext,
            ) -> Awaitable[None]: ...

        class ReleaseSturdyRefClient(_DynamicCapabilityClient):
            class ReleaseResult(Awaitable[ReleaseResult], Protocol):
                success: bool

            def release(
                self,
            ) -> _PersistentInterfaceModule._ReleaseSturdyRefInterfaceModule.ReleaseSturdyRefClient.ReleaseResult: ...
            def release_request(
                self,
            ) -> _PersistentInterfaceModule._ReleaseSturdyRefInterfaceModule.ReleaseRequest: ...

    ReleaseSturdyRef: _ReleaseSturdyRefInterfaceModule
    type ReleaseSturdyRefClient = _PersistentInterfaceModule._ReleaseSturdyRefInterfaceModule.ReleaseSturdyRefClient
    type ReleaseSturdyRefServer = (
        _PersistentInterfaceModule._ReleaseSturdyRefInterfaceModule.Server
    )
    class SaveRequest(Protocol):
        sealFor: OwnerBuilder
        @overload
        def init(self, name: Literal["sealFor"]) -> OwnerBuilder: ...
        @overload
        def init(self, name: str, size: int = ...) -> Any: ...
        def send(self) -> _PersistentInterfaceModule.PersistentClient.SaveResult: ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _PersistentInterfaceModule.PersistentClient: ...
    class Server(_DynamicCapabilityServer):
        class SaveResult(Awaitable[SaveResult], Protocol):
            sturdyRef: SturdyRefBuilder | SturdyRefReader
            unsaveSR: SturdyRefBuilder | SturdyRefReader

        class SaveResultTuple(NamedTuple):
            sturdyRef: SturdyRefBuilder | SturdyRefReader
            unsaveSR: SturdyRefBuilder | SturdyRefReader

        class SaveParams(Protocol):
            sealFor: OwnerReader

        class SaveCallContext(Protocol):
            params: _PersistentInterfaceModule.Server.SaveParams
            @property
            def results(self) -> SaveResultsBuilder: ...

        def save(
            self,
            sealFor: OwnerReader,
            _context: _PersistentInterfaceModule.Server.SaveCallContext,
            **kwargs: Any,
        ) -> Awaitable[_PersistentInterfaceModule.Server.SaveResultTuple | None]: ...
        def save_context(
            self, context: _PersistentInterfaceModule.Server.SaveCallContext
        ) -> Awaitable[None]: ...

    class PersistentClient(_DynamicCapabilityClient):
        class SaveResult(Awaitable[SaveResult], Protocol):
            sturdyRef: SturdyRefReader
            unsaveSR: SturdyRefReader

        def save(
            self, sealFor: OwnerBuilder | OwnerReader | dict[str, Any] | None = None
        ) -> _PersistentInterfaceModule.PersistentClient.SaveResult: ...
        def save_request(
            self, sealFor: OwnerBuilder | None = None
        ) -> _PersistentInterfaceModule.SaveRequest: ...

Persistent: _PersistentInterfaceModule

class _RestorerInterfaceModule(_InterfaceModule):
    class _RestoreParamsStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def localRef(self) -> TokenReader: ...
            @property
            def sealedBy(self) -> OwnerReader: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> RestoreParamsBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def localRef(self) -> TokenBuilder: ...
            @localRef.setter
            def localRef(
                self, value: TokenBuilder | TokenReader | dict[str, Any]
            ) -> None: ...
            @property
            def sealedBy(self) -> OwnerBuilder: ...
            @sealedBy.setter
            def sealedBy(
                self, value: OwnerBuilder | OwnerReader | dict[str, Any]
            ) -> None: ...
            @override
            @overload
            def init(
                self, field: Literal["localRef"], size: int | None = None
            ) -> TokenBuilder: ...
            @overload
            def init(
                self, field: Literal["sealedBy"], size: int | None = None
            ) -> OwnerBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...
            @override
            def as_reader(self) -> RestoreParamsReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            localRef: TokenBuilder | dict[str, Any] | None = None,
            sealedBy: OwnerBuilder | dict[str, Any] | None = None,
            **kwargs: Any,
        ) -> RestoreParamsBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[RestoreParamsReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[RestoreParamsReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[RestoreParamsBuilder]: ...
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
        ) -> RestoreParamsReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> RestoreParamsReader: ...

    type RestoreParamsReader = _RestoreParamsStructModule.Reader
    type RestoreParamsBuilder = _RestoreParamsStructModule.Builder
    RestoreParams: _RestoreParamsStructModule
    class RestoreRequest(Protocol):
        localRef: TokenBuilder
        sealedBy: OwnerBuilder
        @overload
        def init(self, name: Literal["localRef"]) -> TokenBuilder: ...
        @overload
        def init(self, name: Literal["sealedBy"]) -> OwnerBuilder: ...
        @overload
        def init(self, name: str, size: int = ...) -> Any: ...
        def send(self) -> _RestorerInterfaceModule.RestorerClient.RestoreResult: ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _RestorerInterfaceModule.RestorerClient: ...
    class Server(_DynamicCapabilityServer):
        class RestoreResult(_DynamicStructBuilder):
            @property
            def cap(self) -> Capability: ...
            @cap.setter
            def cap(self, value: Capability) -> None: ...

        class RestoreResultTuple(NamedTuple):
            cap: Capability

        class RestoreParams(Protocol):
            localRef: TokenReader
            sealedBy: OwnerReader

        class RestoreCallContext(Protocol):
            params: _RestorerInterfaceModule.Server.RestoreParams
            @property
            def results(self) -> _RestorerInterfaceModule.Server.RestoreResult: ...

        def restore(
            self,
            localRef: TokenReader,
            sealedBy: OwnerReader,
            _context: _RestorerInterfaceModule.Server.RestoreCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            AnyPointer | _RestorerInterfaceModule.Server.RestoreResultTuple | None
        ]: ...
        def restore_context(
            self, context: _RestorerInterfaceModule.Server.RestoreCallContext
        ) -> Awaitable[None]: ...

    class RestorerClient(_DynamicCapabilityClient):
        class RestoreResult(Awaitable[RestoreResult], Protocol):
            cap: _DynamicObjectReader

        def restore(
            self,
            localRef: TokenBuilder | TokenReader | dict[str, Any] | None = None,
            sealedBy: OwnerBuilder | OwnerReader | dict[str, Any] | None = None,
        ) -> _RestorerInterfaceModule.RestorerClient.RestoreResult: ...
        def restore_request(
            self,
            localRef: TokenBuilder | None = None,
            sealedBy: OwnerBuilder | None = None,
        ) -> _RestorerInterfaceModule.RestoreRequest: ...

Restorer: _RestorerInterfaceModule

class _HostPortResolverInterfaceModule(
    _IdentifiableInterfaceModule, _RestorerInterfaceModule
):
    class _RegistrarInterfaceModule(_InterfaceModule):
        class _RegisterParamsStructModule(_StructModule):
            class Reader(_DynamicStructReader):
                @property
                def base64VatId(self) -> str: ...
                @property
                def host(self) -> str: ...
                @property
                def port(self) -> int: ...
                @property
                def alias(self) -> str: ...
                @property
                def identityProof(self) -> bytes: ...
                @override
                def as_builder(
                    self,
                    num_first_segment_words: int | None = None,
                    allocate_seg_callable: Callable[[int], bytearray] | None = None,
                ) -> RegisterParamsBuilder: ...

            class Builder(_DynamicStructBuilder):
                @property
                def base64VatId(self) -> str: ...
                @base64VatId.setter
                def base64VatId(self, value: str) -> None: ...
                @property
                def host(self) -> str: ...
                @host.setter
                def host(self, value: str) -> None: ...
                @property
                def port(self) -> int: ...
                @port.setter
                def port(self, value: int) -> None: ...
                @property
                def alias(self) -> str: ...
                @alias.setter
                def alias(self, value: str) -> None: ...
                @property
                def identityProof(self) -> bytes: ...
                @identityProof.setter
                def identityProof(self, value: bytes) -> None: ...
                @override
                def as_reader(self) -> RegisterParamsReader: ...

            @override
            def new_message(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
                base64VatId: str | None = None,
                host: str | None = None,
                port: int | None = None,
                alias: str | None = None,
                identityProof: bytes | None = None,
                **kwargs: Any,
            ) -> RegisterParamsBuilder: ...
            @override
            @overload
            def from_bytes(
                self,
                buf: bytes,
                traversal_limit_in_words: int | None = None,
                nesting_limit: int | None = None,
            ) -> AbstractContextManager[RegisterParamsReader]: ...
            @overload
            def from_bytes(
                self,
                buf: bytes,
                traversal_limit_in_words: int | None = None,
                nesting_limit: int | None = None,
                *,
                builder: Literal[False],
            ) -> AbstractContextManager[RegisterParamsReader]: ...
            @overload
            def from_bytes(
                self,
                buf: bytes,
                traversal_limit_in_words: int | None = None,
                nesting_limit: int | None = None,
                *,
                builder: Literal[True],
            ) -> AbstractContextManager[RegisterParamsBuilder]: ...
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
            ) -> RegisterParamsReader: ...
            @override
            def read_packed(
                self,
                file: IO[str] | IO[bytes],
                traversal_limit_in_words: int | None = None,
                nesting_limit: int | None = None,
            ) -> RegisterParamsReader: ...

        type RegisterParamsReader = _RegisterParamsStructModule.Reader
        type RegisterParamsBuilder = _RegisterParamsStructModule.Builder
        RegisterParams: _RegisterParamsStructModule
        class RegisterRequest(Protocol):
            base64VatId: str
            host: str
            port: int
            alias: str
            identityProof: bytes
            def send(
                self,
            ) -> _HostPortResolverInterfaceModule._RegistrarInterfaceModule.RegistrarClient.RegisterResult: ...

        @override
        def _new_client(
            self, server: _DynamicCapabilityServer
        ) -> (
            _HostPortResolverInterfaceModule._RegistrarInterfaceModule.RegistrarClient
        ): ...
        class Server(_DynamicCapabilityServer):
            class RegisterResult(_DynamicStructBuilder):
                @property
                def heartbeat(
                    self,
                ) -> (
                    _HeartbeatInterfaceModule.Server
                    | _HeartbeatInterfaceModule.HeartbeatClient
                ): ...
                @heartbeat.setter
                def heartbeat(
                    self,
                    value: _HeartbeatInterfaceModule.Server
                    | _HeartbeatInterfaceModule.HeartbeatClient,
                ) -> None: ...
                @property
                def secsHeartbeatInterval(self) -> int: ...
                @secsHeartbeatInterval.setter
                def secsHeartbeatInterval(self, value: int) -> None: ...

            class RegisterResultTuple(NamedTuple):
                heartbeat: (
                    _HeartbeatInterfaceModule.Server
                    | _HeartbeatInterfaceModule.HeartbeatClient
                )
                secsHeartbeatInterval: int

            class RegisterParams(Protocol):
                base64VatId: str
                host: str
                port: int
                alias: str
                identityProof: bytes

            class RegisterCallContext(Protocol):
                params: _HostPortResolverInterfaceModule._RegistrarInterfaceModule.Server.RegisterParams
                @property
                def results(
                    self,
                ) -> _HostPortResolverInterfaceModule._RegistrarInterfaceModule.Server.RegisterResult: ...

            def register(
                self,
                base64VatId: str,
                host: str,
                port: int,
                alias: str,
                identityProof: bytes,
                _context: _HostPortResolverInterfaceModule._RegistrarInterfaceModule.Server.RegisterCallContext,
                **kwargs: Any,
            ) -> Awaitable[
                _HostPortResolverInterfaceModule._RegistrarInterfaceModule.Server.RegisterResultTuple
                | None
            ]: ...
            def register_context(
                self,
                context: _HostPortResolverInterfaceModule._RegistrarInterfaceModule.Server.RegisterCallContext,
            ) -> Awaitable[None]: ...

        class RegistrarClient(_DynamicCapabilityClient):
            class RegisterResult(Awaitable[RegisterResult], Protocol):
                heartbeat: _HeartbeatInterfaceModule.HeartbeatClient
                secsHeartbeatInterval: int

            def register(
                self,
                base64VatId: str | None = None,
                host: str | None = None,
                port: int | None = None,
                alias: str | None = None,
                identityProof: bytes | None = None,
            ) -> _HostPortResolverInterfaceModule._RegistrarInterfaceModule.RegistrarClient.RegisterResult: ...
            def register_request(
                self,
                base64VatId: str | None = None,
                host: str | None = None,
                port: int | None = None,
                alias: str | None = None,
                identityProof: bytes | None = None,
            ) -> _HostPortResolverInterfaceModule._RegistrarInterfaceModule.RegisterRequest: ...

    Registrar: _RegistrarInterfaceModule
    type RegistrarClient = (
        _HostPortResolverInterfaceModule._RegistrarInterfaceModule.RegistrarClient
    )
    type RegistrarServer = (
        _HostPortResolverInterfaceModule._RegistrarInterfaceModule.Server
    )
    class ResolveRequest(Protocol):
        id: str
        def send(
            self,
        ) -> _HostPortResolverInterfaceModule.HostPortResolverClient.ResolveResult: ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _HostPortResolverInterfaceModule.HostPortResolverClient: ...
    class Server(_IdentifiableInterfaceModule.Server, _RestorerInterfaceModule.Server):
        class ResolveResult(_DynamicStructBuilder):
            @property
            def host(self) -> str: ...
            @host.setter
            def host(self, value: str) -> None: ...
            @property
            def port(self) -> int: ...
            @port.setter
            def port(self, value: int) -> None: ...

        class ResolveResultTuple(NamedTuple):
            host: str
            port: int

        class ResolveParams(Protocol):
            id: str

        class ResolveCallContext(Protocol):
            params: _HostPortResolverInterfaceModule.Server.ResolveParams
            @property
            def results(
                self,
            ) -> _HostPortResolverInterfaceModule.Server.ResolveResult: ...

        def resolve(
            self,
            id: str,
            _context: _HostPortResolverInterfaceModule.Server.ResolveCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            _HostPortResolverInterfaceModule.Server.ResolveResultTuple | None
        ]: ...
        def resolve_context(
            self, context: _HostPortResolverInterfaceModule.Server.ResolveCallContext
        ) -> Awaitable[None]: ...

    class HostPortResolverClient(
        _IdentifiableInterfaceModule.IdentifiableClient,
        _RestorerInterfaceModule.RestorerClient,
    ):
        class ResolveResult(Awaitable[ResolveResult], Protocol):
            host: str
            port: int

        def resolve(
            self, id: str | None = None
        ) -> _HostPortResolverInterfaceModule.HostPortResolverClient.ResolveResult: ...
        def resolve_request(
            self, id: str | None = None
        ) -> _HostPortResolverInterfaceModule.ResolveRequest: ...

HostPortResolver: _HostPortResolverInterfaceModule

class _GatewayInterfaceModule(_IdentifiableInterfaceModule, _RestorerInterfaceModule):
    class _RegResultsStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def sturdyRef(self) -> SturdyRefReader: ...
            @property
            def heartbeat(self) -> _HeartbeatInterfaceModule.HeartbeatClient: ...
            @property
            def secsHeartbeatInterval(self) -> int: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> RegResultsBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def sturdyRef(self) -> SturdyRefBuilder: ...
            @sturdyRef.setter
            def sturdyRef(
                self, value: SturdyRefBuilder | SturdyRefReader | dict[str, Any]
            ) -> None: ...
            @property
            def heartbeat(self) -> _HeartbeatInterfaceModule.HeartbeatClient: ...
            @heartbeat.setter
            def heartbeat(
                self,
                value: _HeartbeatInterfaceModule.HeartbeatClient
                | _HeartbeatInterfaceModule.Server,
            ) -> None: ...
            @property
            def secsHeartbeatInterval(self) -> int: ...
            @secsHeartbeatInterval.setter
            def secsHeartbeatInterval(self, value: int) -> None: ...
            @override
            def init(
                self, field: Literal["sturdyRef"], size: int | None = None
            ) -> SturdyRefBuilder: ...
            @override
            def as_reader(self) -> RegResultsReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            sturdyRef: SturdyRefBuilder | dict[str, Any] | None = None,
            heartbeat: _HeartbeatInterfaceModule.HeartbeatClient
            | _HeartbeatInterfaceModule.Server
            | None = None,
            secsHeartbeatInterval: int | None = None,
            **kwargs: Any,
        ) -> RegResultsBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[RegResultsReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[RegResultsReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[RegResultsBuilder]: ...
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
        ) -> RegResultsReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> RegResultsReader: ...

    type RegResultsReader = _RegResultsStructModule.Reader
    type RegResultsBuilder = _RegResultsStructModule.Builder
    RegResults: _RegResultsStructModule
    class RegisterRequest(Protocol):
        cap: AnyPointer
        def send(self) -> _GatewayInterfaceModule.GatewayClient.RegisterResult: ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _GatewayInterfaceModule.GatewayClient: ...
    class Server(_IdentifiableInterfaceModule.Server, _RestorerInterfaceModule.Server):
        class RegisterResult(Awaitable[RegisterResult], Protocol):
            sturdyRef: SturdyRefBuilder | SturdyRefReader
            heartbeat: (
                _HeartbeatInterfaceModule.Server
                | _HeartbeatInterfaceModule.HeartbeatClient
            )
            secsHeartbeatInterval: int

        class RegisterResultTuple(NamedTuple):
            sturdyRef: SturdyRefBuilder | SturdyRefReader
            heartbeat: (
                _HeartbeatInterfaceModule.Server
                | _HeartbeatInterfaceModule.HeartbeatClient
            )
            secsHeartbeatInterval: int

        class RegisterParams(Protocol):
            cap: AnyPointer

        class RegisterCallContext(Protocol):
            params: _GatewayInterfaceModule.Server.RegisterParams
            @property
            def results(self) -> RegResultsBuilder: ...

        def register(
            self,
            cap: AnyPointer,
            _context: _GatewayInterfaceModule.Server.RegisterCallContext,
            **kwargs: Any,
        ) -> Awaitable[_GatewayInterfaceModule.Server.RegisterResultTuple | None]: ...
        def register_context(
            self, context: _GatewayInterfaceModule.Server.RegisterCallContext
        ) -> Awaitable[None]: ...

    class GatewayClient(
        _IdentifiableInterfaceModule.IdentifiableClient,
        _RestorerInterfaceModule.RestorerClient,
    ):
        class RegisterResult(Awaitable[RegisterResult], Protocol):
            sturdyRef: SturdyRefReader
            heartbeat: _HeartbeatInterfaceModule.HeartbeatClient
            secsHeartbeatInterval: int

        def register(
            self, cap: AnyPointer | None = None
        ) -> _GatewayInterfaceModule.GatewayClient.RegisterResult: ...
        def register_request(
            self, cap: AnyPointer | None = None
        ) -> _GatewayInterfaceModule.RegisterRequest: ...

Gateway: _GatewayInterfaceModule

# Top-level type aliases for use in type annotations
type AddressBuilder = _AddressStructModule.Builder
type AddressIp6Builder = _AddressStructModule._AddressIp6StructModule.Builder
type AddressIp6Reader = _AddressStructModule._AddressIp6StructModule.Reader
type AddressReader = _AddressStructModule.Reader
type BeatResult = _HeartbeatInterfaceModule.HeartbeatClient.BeatResult
type GatewayClient = _GatewayInterfaceModule.GatewayClient
type GatewayServer = _GatewayInterfaceModule.Server
type HeartbeatClient = _HeartbeatInterfaceModule.HeartbeatClient
type HeartbeatServer = _HeartbeatInterfaceModule.Server
type HostPortResolverClient = _HostPortResolverInterfaceModule.HostPortResolverClient
type HostPortResolverServer = _HostPortResolverInterfaceModule.Server
type OwnerBuilder = _SturdyRefStructModule._OwnerStructModule.Builder
type OwnerReader = _SturdyRefStructModule._OwnerStructModule.Reader
type PersistentClient = _PersistentInterfaceModule.PersistentClient
type PersistentServer = _PersistentInterfaceModule.Server
type RegResultsBuilder = _GatewayInterfaceModule._RegResultsStructModule.Builder
type RegResultsReader = _GatewayInterfaceModule._RegResultsStructModule.Reader
type RegisterParamsBuilder = _HostPortResolverInterfaceModule._RegistrarInterfaceModule._RegisterParamsStructModule.Builder
type RegisterParamsReader = _HostPortResolverInterfaceModule._RegistrarInterfaceModule._RegisterParamsStructModule.Reader
type RegisterResult = _GatewayInterfaceModule.GatewayClient.RegisterResult
type RegistrarClient = (
    _HostPortResolverInterfaceModule._RegistrarInterfaceModule.RegistrarClient
)
type RegistrarServer = _HostPortResolverInterfaceModule._RegistrarInterfaceModule.Server
type ReleaseResult = _PersistentInterfaceModule._ReleaseSturdyRefInterfaceModule.ReleaseSturdyRefClient.ReleaseResult
type ReleaseSturdyRefClient = (
    _PersistentInterfaceModule._ReleaseSturdyRefInterfaceModule.ReleaseSturdyRefClient
)
type ReleaseSturdyRefServer = (
    _PersistentInterfaceModule._ReleaseSturdyRefInterfaceModule.Server
)
type ResolveResult = (
    _HostPortResolverInterfaceModule.HostPortResolverClient.ResolveResult
)
type RestoreParamsBuilder = _RestorerInterfaceModule._RestoreParamsStructModule.Builder
type RestoreParamsReader = _RestorerInterfaceModule._RestoreParamsStructModule.Reader
type RestoreResult = _RestorerInterfaceModule.RestorerClient.RestoreResult
type RestorerClient = _RestorerInterfaceModule.RestorerClient
type RestorerServer = _RestorerInterfaceModule.Server
type SaveParamsBuilder = _PersistentInterfaceModule._SaveParamsStructModule.Builder
type SaveParamsReader = _PersistentInterfaceModule._SaveParamsStructModule.Reader
type SaveResult = _PersistentInterfaceModule.PersistentClient.SaveResult
type SaveResultsBuilder = _PersistentInterfaceModule._SaveResultsStructModule.Builder
type SaveResultsReader = _PersistentInterfaceModule._SaveResultsStructModule.Reader
type SturdyRefBuilder = _SturdyRefStructModule.Builder
type SturdyRefReader = _SturdyRefStructModule.Reader
type TokenBuilder = _SturdyRefStructModule._TokenStructModule.Builder
type TokenReader = _SturdyRefStructModule._TokenStructModule.Reader
type VatIdBuilder = _VatIdStructModule.Builder
type VatIdReader = _VatIdStructModule.Reader
type VatPathBuilder = _VatPathStructModule.Builder
type VatPathReader = _VatPathStructModule.Reader
