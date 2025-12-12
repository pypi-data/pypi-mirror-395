"""This is an automatically generated stub for `service.capnp`."""

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
from .common_capnp import _IdentifiableInterfaceModule, IdentifiableClient
from .common_capnp import IdInformationReader, IdInformationBuilder
from .common_capnp import PairReader, PairBuilder
from contextlib import AbstractContextManager
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

# Type alias for Capability parameters
type Capability = (
    _DynamicCapabilityClient
    | _DynamicCapabilityServer
    | _DynamicObjectReader
    | _DynamicObjectBuilder
)

class _AdminInterfaceModule(_IdentifiableInterfaceModule):
    class HeartbeatRequest(Protocol):
        def send(self) -> _AdminInterfaceModule.AdminClient.HeartbeatResult: ...

    class SettimeoutRequest(Protocol):
        seconds: int
        def send(self) -> _AdminInterfaceModule.AdminClient.SettimeoutResult: ...

    class StopRequest(Protocol):
        def send(self) -> _AdminInterfaceModule.AdminClient.StopResult: ...

    class IdentitiesRequest(Protocol):
        def send(self) -> _AdminInterfaceModule.AdminClient.IdentitiesResult: ...

    class UpdateidentityRequest(Protocol):
        oldId: str
        newInfo: IdInformationBuilder
        @overload
        def init(self, name: Literal["newInfo"]) -> IdInformationBuilder: ...
        @overload
        def init(self, name: str, size: int = ...) -> Any: ...
        def send(self) -> _AdminInterfaceModule.AdminClient.UpdateidentityResult: ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _AdminInterfaceModule.AdminClient: ...
    class Server(_IdentifiableInterfaceModule.Server):
        class HeartbeatResult(Awaitable[None], Protocol): ...
        class SettimeoutResult(Awaitable[None], Protocol): ...
        class StopResult(Awaitable[None], Protocol): ...

        class IdentitiesResult(_DynamicStructBuilder):
            @property
            def infos(self) -> IdInformationListBuilder: ...
            @infos.setter
            def infos(
                self,
                value: IdInformationListBuilder
                | IdInformationListReader
                | Sequence[Any],
            ) -> None: ...
            @overload
            def init(
                self, field: Literal["infos"], size: int | None = None
            ) -> IdInformationListBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...

        class UpdateidentityResult(Awaitable[None], Protocol): ...

        class IdentitiesResultTuple(NamedTuple):
            infos: IdInformationListBuilder | IdInformationListReader

        class HeartbeatParams(Protocol): ...

        class HeartbeatCallContext(Protocol):
            params: _AdminInterfaceModule.Server.HeartbeatParams

        class SettimeoutParams(Protocol):
            seconds: int

        class SettimeoutCallContext(Protocol):
            params: _AdminInterfaceModule.Server.SettimeoutParams

        class StopParams(Protocol): ...

        class StopCallContext(Protocol):
            params: _AdminInterfaceModule.Server.StopParams

        class IdentitiesParams(Protocol): ...

        class IdentitiesCallContext(Protocol):
            params: _AdminInterfaceModule.Server.IdentitiesParams
            @property
            def results(self) -> _AdminInterfaceModule.Server.IdentitiesResult: ...

        class UpdateidentityParams(Protocol):
            oldId: str
            newInfo: IdInformationReader

        class UpdateidentityCallContext(Protocol):
            params: _AdminInterfaceModule.Server.UpdateidentityParams

        def heartbeat(
            self,
            _context: _AdminInterfaceModule.Server.HeartbeatCallContext,
            **kwargs: Any,
        ) -> Awaitable[None]: ...
        def heartbeat_context(
            self, context: _AdminInterfaceModule.Server.HeartbeatCallContext
        ) -> Awaitable[None]: ...
        def setTimeout(
            self,
            seconds: int,
            _context: _AdminInterfaceModule.Server.SettimeoutCallContext,
            **kwargs: Any,
        ) -> Awaitable[None]: ...
        def setTimeout_context(
            self, context: _AdminInterfaceModule.Server.SettimeoutCallContext
        ) -> Awaitable[None]: ...
        def stop(
            self, _context: _AdminInterfaceModule.Server.StopCallContext, **kwargs: Any
        ) -> Awaitable[None]: ...
        def stop_context(
            self, context: _AdminInterfaceModule.Server.StopCallContext
        ) -> Awaitable[None]: ...
        def identities(
            self,
            _context: _AdminInterfaceModule.Server.IdentitiesCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            Sequence[IdInformationBuilder | IdInformationReader]
            | _AdminInterfaceModule.Server.IdentitiesResultTuple
            | None
        ]: ...
        def identities_context(
            self, context: _AdminInterfaceModule.Server.IdentitiesCallContext
        ) -> Awaitable[None]: ...
        def updateIdentity(
            self,
            oldId: str,
            newInfo: IdInformationReader,
            _context: _AdminInterfaceModule.Server.UpdateidentityCallContext,
            **kwargs: Any,
        ) -> Awaitable[None]: ...
        def updateIdentity_context(
            self, context: _AdminInterfaceModule.Server.UpdateidentityCallContext
        ) -> Awaitable[None]: ...

    class AdminClient(_IdentifiableInterfaceModule.IdentifiableClient):
        class HeartbeatResult(Awaitable[None], Protocol): ...
        class SettimeoutResult(Awaitable[None], Protocol): ...
        class StopResult(Awaitable[None], Protocol): ...

        class IdentitiesResult(Awaitable[IdentitiesResult], Protocol):
            infos: IdInformationListReader

        class UpdateidentityResult(Awaitable[None], Protocol): ...

        def heartbeat(self) -> _AdminInterfaceModule.AdminClient.HeartbeatResult: ...
        def setTimeout(
            self, seconds: int | None = None
        ) -> _AdminInterfaceModule.AdminClient.SettimeoutResult: ...
        def stop(self) -> _AdminInterfaceModule.AdminClient.StopResult: ...
        def identities(self) -> _AdminInterfaceModule.AdminClient.IdentitiesResult: ...
        def updateIdentity(
            self,
            oldId: str | None = None,
            newInfo: IdInformationBuilder
            | IdInformationReader
            | dict[str, Any]
            | None = None,
        ) -> _AdminInterfaceModule.AdminClient.UpdateidentityResult: ...
        def heartbeat_request(self) -> _AdminInterfaceModule.HeartbeatRequest: ...
        def setTimeout_request(
            self, seconds: int | None = None
        ) -> _AdminInterfaceModule.SettimeoutRequest: ...
        def stop_request(self) -> _AdminInterfaceModule.StopRequest: ...
        def identities_request(self) -> _AdminInterfaceModule.IdentitiesRequest: ...
        def updateIdentity_request(
            self, oldId: str | None = None, newInfo: IdInformationBuilder | None = None
        ) -> _AdminInterfaceModule.UpdateidentityRequest: ...

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

Admin: _AdminInterfaceModule

class _SimpleFactoryInterfaceModule(_IdentifiableInterfaceModule):
    class CreateRequest(Protocol):
        def send(
            self,
        ) -> _SimpleFactoryInterfaceModule.SimpleFactoryClient.CreateResult: ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _SimpleFactoryInterfaceModule.SimpleFactoryClient: ...
    class Server(_IdentifiableInterfaceModule.Server):
        class CreateResult(_DynamicStructBuilder):
            @property
            def caps(self) -> IdentifiableClientListBuilder: ...
            @caps.setter
            def caps(
                self,
                value: IdentifiableClientListBuilder
                | IdentifiableClientListReader
                | Sequence[Any],
            ) -> None: ...
            @overload
            def init(
                self, field: Literal["caps"], size: int | None = None
            ) -> IdentifiableClientListBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...

        class CreateResultTuple(NamedTuple):
            caps: IdentifiableClientListBuilder | IdentifiableClientListReader

        class CreateParams(Protocol): ...

        class CreateCallContext(Protocol):
            params: _SimpleFactoryInterfaceModule.Server.CreateParams
            @property
            def results(self) -> _SimpleFactoryInterfaceModule.Server.CreateResult: ...

        def create(
            self,
            _context: _SimpleFactoryInterfaceModule.Server.CreateCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            Sequence[_IdentifiableInterfaceModule]
            | _SimpleFactoryInterfaceModule.Server.CreateResultTuple
            | None
        ]: ...
        def create_context(
            self, context: _SimpleFactoryInterfaceModule.Server.CreateCallContext
        ) -> Awaitable[None]: ...

    class SimpleFactoryClient(_IdentifiableInterfaceModule.IdentifiableClient):
        class CreateResult(Awaitable[CreateResult], Protocol):
            caps: IdentifiableClientListReader

        def create(
            self,
        ) -> _SimpleFactoryInterfaceModule.SimpleFactoryClient.CreateResult: ...
        def create_request(self) -> _SimpleFactoryInterfaceModule.CreateRequest: ...

class _IdentifiableClientList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> IdentifiableClient: ...
        @override
        def __iter__(self) -> Iterator[IdentifiableClient]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> IdentifiableClient: ...
        @override
        def __setitem__(
            self,
            key: int,
            value: IdentifiableClient | _IdentifiableInterfaceModule.Server,
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[IdentifiableClient]: ...

SimpleFactory: _SimpleFactoryInterfaceModule

class _FactoryInterfaceModule(_IdentifiableInterfaceModule):
    class _CreateParamsStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def timeoutSeconds(self) -> int: ...
            @property
            def interfaceNameToRegistrySR(self) -> PairListReader: ...
            @property
            def msgPayload(self) -> _DynamicObjectReader: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> CreateParamsBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def timeoutSeconds(self) -> int: ...
            @timeoutSeconds.setter
            def timeoutSeconds(self, value: int) -> None: ...
            @property
            def interfaceNameToRegistrySR(self) -> PairListBuilder: ...
            @interfaceNameToRegistrySR.setter
            def interfaceNameToRegistrySR(
                self, value: PairListBuilder | PairListReader | dict[str, Any]
            ) -> None: ...
            @property
            def msgPayload(self) -> _DynamicObjectReader: ...
            @msgPayload.setter
            def msgPayload(self, value: AnyPointer) -> None: ...
            @override
            def init(
                self,
                field: Literal["interfaceNameToRegistrySR"],
                size: int | None = None,
            ) -> PairListBuilder: ...
            @override
            def as_reader(self) -> CreateParamsReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            timeoutSeconds: int | None = None,
            interfaceNameToRegistrySR: PairListBuilder | dict[str, Any] | None = None,
            msgPayload: AnyPointer | None = None,
            **kwargs: Any,
        ) -> CreateParamsBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[CreateParamsReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[CreateParamsReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[CreateParamsBuilder]: ...
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
        ) -> CreateParamsReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> CreateParamsReader: ...

    type CreateParamsReader = _CreateParamsStructModule.Reader
    type CreateParamsBuilder = _CreateParamsStructModule.Builder
    CreateParams: _CreateParamsStructModule
    class _AccessInfoStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def adminCap(self) -> _DynamicObjectReader: ...
            @property
            def serviceCaps(self) -> IdentifiableClientListReader: ...
            @property
            def error(self) -> str: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> AccessInfoBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def adminCap(self) -> _DynamicObjectReader: ...
            @adminCap.setter
            def adminCap(self, value: Capability) -> None: ...
            @property
            def serviceCaps(self) -> IdentifiableClientListBuilder: ...
            @serviceCaps.setter
            def serviceCaps(
                self,
                value: IdentifiableClientListBuilder
                | IdentifiableClientListReader
                | dict[str, Any],
            ) -> None: ...
            @property
            def error(self) -> str: ...
            @error.setter
            def error(self, value: str) -> None: ...
            @override
            def init(
                self, field: Literal["serviceCaps"], size: int | None = None
            ) -> IdentifiableClientListBuilder: ...
            @override
            def as_reader(self) -> AccessInfoReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            adminCap: Capability | None = None,
            serviceCaps: IdentifiableClientListBuilder | dict[str, Any] | None = None,
            error: str | None = None,
            **kwargs: Any,
        ) -> AccessInfoBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[AccessInfoReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[AccessInfoReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[AccessInfoBuilder]: ...
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
        ) -> AccessInfoReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AccessInfoReader: ...

    type AccessInfoReader = _AccessInfoStructModule.Reader
    type AccessInfoBuilder = _AccessInfoStructModule.Builder
    AccessInfo: _AccessInfoStructModule
    class CreateRequest(Protocol):
        timeoutSeconds: int
        interfaceNameToRegistrySR: PairListBuilder | PairListReader | Sequence[Any]
        msgPayload: AnyPointer
        @overload
        def init(
            self, name: Literal["interfaceNameToRegistrySR"], size: int = ...
        ) -> PairListBuilder: ...
        @overload
        def init(self, name: str, size: int = ...) -> Any: ...
        def send(self) -> _FactoryInterfaceModule.FactoryClient.CreateResult: ...

    class ServiceinterfacenamesRequest(Protocol):
        def send(
            self,
        ) -> _FactoryInterfaceModule.FactoryClient.ServiceinterfacenamesResult: ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _FactoryInterfaceModule.FactoryClient: ...
    class Server(_IdentifiableInterfaceModule.Server):
        class CreateResult(Awaitable[CreateResult], Protocol):
            adminCap: _DynamicCapabilityClient | _DynamicCapabilityServer
            serviceCaps: IdentifiableClientListBuilder | IdentifiableClientListReader
            error: str

        class ServiceinterfacenamesResult(_DynamicStructBuilder):
            @property
            def names(self) -> TextListBuilder: ...
            @names.setter
            def names(
                self, value: TextListBuilder | TextListReader | Sequence[Any]
            ) -> None: ...
            @overload
            def init(
                self, field: Literal["names"], size: int | None = None
            ) -> TextListBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...

        class CreateResultTuple(NamedTuple):
            adminCap: Capability
            serviceCaps: IdentifiableClientListBuilder | IdentifiableClientListReader
            error: str

        class ServiceinterfacenamesResultTuple(NamedTuple):
            names: TextListBuilder | TextListReader

        class CreateParams(Protocol):
            timeoutSeconds: int
            interfaceNameToRegistrySR: PairListReader
            msgPayload: AnyPointer

        class CreateCallContext(Protocol):
            params: _FactoryInterfaceModule.Server.CreateParams
            @property
            def results(self) -> AccessInfoBuilder: ...

        class ServiceinterfacenamesParams(Protocol): ...

        class ServiceinterfacenamesCallContext(Protocol):
            params: _FactoryInterfaceModule.Server.ServiceinterfacenamesParams
            @property
            def results(
                self,
            ) -> _FactoryInterfaceModule.Server.ServiceinterfacenamesResult: ...

        def create(
            self,
            timeoutSeconds: int,
            interfaceNameToRegistrySR: PairListReader,
            msgPayload: AnyPointer,
            _context: _FactoryInterfaceModule.Server.CreateCallContext,
            **kwargs: Any,
        ) -> Awaitable[_FactoryInterfaceModule.Server.CreateResultTuple | None]: ...
        def create_context(
            self, context: _FactoryInterfaceModule.Server.CreateCallContext
        ) -> Awaitable[None]: ...
        def serviceInterfaceNames(
            self,
            _context: _FactoryInterfaceModule.Server.ServiceinterfacenamesCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            Sequence[str]
            | _FactoryInterfaceModule.Server.ServiceinterfacenamesResultTuple
            | None
        ]: ...
        def serviceInterfaceNames_context(
            self,
            context: _FactoryInterfaceModule.Server.ServiceinterfacenamesCallContext,
        ) -> Awaitable[None]: ...

    class FactoryClient(_IdentifiableInterfaceModule.IdentifiableClient):
        class CreateResult(Awaitable[CreateResult], Protocol):
            adminCap: _DynamicCapabilityClient
            serviceCaps: IdentifiableClientListReader
            error: str

        class ServiceinterfacenamesResult(
            Awaitable[ServiceinterfacenamesResult], Protocol
        ):
            names: TextListReader

        def create(
            self,
            timeoutSeconds: int | None = None,
            interfaceNameToRegistrySR: PairListBuilder
            | PairListReader
            | Sequence[Any]
            | None = None,
            msgPayload: AnyPointer | None = None,
        ) -> _FactoryInterfaceModule.FactoryClient.CreateResult: ...
        def serviceInterfaceNames(
            self,
        ) -> _FactoryInterfaceModule.FactoryClient.ServiceinterfacenamesResult: ...
        def create_request(
            self,
            timeoutSeconds: int | None = None,
            interfaceNameToRegistrySR: PairListBuilder
            | PairListReader
            | Sequence[Any]
            | None = None,
            msgPayload: AnyPointer | None = None,
        ) -> _FactoryInterfaceModule.CreateRequest: ...
        def serviceInterfaceNames_request(
            self,
        ) -> _FactoryInterfaceModule.ServiceinterfacenamesRequest: ...

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

Factory: _FactoryInterfaceModule

class _StoppableInterfaceModule(_InterfaceModule):
    class StopRequest(Protocol):
        def send(self) -> _StoppableInterfaceModule.StoppableClient.StopResult: ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _StoppableInterfaceModule.StoppableClient: ...
    class Server(_DynamicCapabilityServer):
        class StopResult(_DynamicStructBuilder):
            @property
            def success(self) -> bool: ...
            @success.setter
            def success(self, value: bool) -> None: ...

        class StopResultTuple(NamedTuple):
            success: bool

        class StopParams(Protocol): ...

        class StopCallContext(Protocol):
            params: _StoppableInterfaceModule.Server.StopParams
            @property
            def results(self) -> _StoppableInterfaceModule.Server.StopResult: ...

        def stop(
            self,
            _context: _StoppableInterfaceModule.Server.StopCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            bool | _StoppableInterfaceModule.Server.StopResultTuple | None
        ]: ...
        def stop_context(
            self, context: _StoppableInterfaceModule.Server.StopCallContext
        ) -> Awaitable[None]: ...

    class StoppableClient(_DynamicCapabilityClient):
        class StopResult(Awaitable[StopResult], Protocol):
            success: bool

        def stop(self) -> _StoppableInterfaceModule.StoppableClient.StopResult: ...
        def stop_request(self) -> _StoppableInterfaceModule.StopRequest: ...

Stoppable: _StoppableInterfaceModule

# Top-level type aliases for use in type annotations
type AccessInfoBuilder = _FactoryInterfaceModule._AccessInfoStructModule.Builder
type AccessInfoReader = _FactoryInterfaceModule._AccessInfoStructModule.Reader
type AdminClient = _AdminInterfaceModule.AdminClient
type AdminServer = _AdminInterfaceModule.Server
type CreateParamsBuilder = _FactoryInterfaceModule._CreateParamsStructModule.Builder
type CreateParamsReader = _FactoryInterfaceModule._CreateParamsStructModule.Reader
type CreateResult = _FactoryInterfaceModule.FactoryClient.CreateResult
type FactoryClient = _FactoryInterfaceModule.FactoryClient
type FactoryServer = _FactoryInterfaceModule.Server
type HeartbeatResult = _AdminInterfaceModule.AdminClient.HeartbeatResult
type IdInformationListBuilder = _IdInformationList.Builder
type IdInformationListReader = _IdInformationList.Reader
type IdentifiableClientListBuilder = _IdentifiableClientList.Builder
type IdentifiableClientListReader = _IdentifiableClientList.Reader
type IdentitiesResult = _AdminInterfaceModule.AdminClient.IdentitiesResult
type PairListBuilder = _PairList.Builder
type PairListReader = _PairList.Reader
type ServiceinterfacenamesResult = (
    _FactoryInterfaceModule.FactoryClient.ServiceinterfacenamesResult
)
type SettimeoutResult = _AdminInterfaceModule.AdminClient.SettimeoutResult
type SimpleFactoryClient = _SimpleFactoryInterfaceModule.SimpleFactoryClient
type SimpleFactoryServer = _SimpleFactoryInterfaceModule.Server
type StopResult = _StoppableInterfaceModule.StoppableClient.StopResult
type StoppableClient = _StoppableInterfaceModule.StoppableClient
type StoppableServer = _StoppableInterfaceModule.Server
type TextListBuilder = _TextList.Builder
type TextListReader = _TextList.Reader
type UpdateidentityResult = _AdminInterfaceModule.AdminClient.UpdateidentityResult
