"""This is an automatically generated stub for `crop.capnp`."""

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
)
from .common_capnp import _IdentifiableInterfaceModule
from .persistence_capnp import _PersistentInterfaceModule
from .common_capnp import (
    _IdInformationStructModule,
    IdInformationReader,
    IdInformationBuilder,
)
from .registry_capnp import _RegistryInterfaceModule
from collections.abc import Awaitable
from typing import Literal, overload, override, Protocol, Any, NamedTuple

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

class _CropInterfaceModule(_IdentifiableInterfaceModule, _PersistentInterfaceModule):
    class ParametersRequest(Protocol):
        def send(self) -> _CropInterfaceModule.CropClient.ParametersResult: ...

    class CultivarRequest(Protocol):
        def send(self) -> _CropInterfaceModule.CropClient.CultivarResult: ...

    class SpeciesRequest(Protocol):
        def send(self) -> _CropInterfaceModule.CropClient.SpeciesResult: ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _CropInterfaceModule.CropClient: ...
    class Server(
        _IdentifiableInterfaceModule.Server, _PersistentInterfaceModule.Server
    ):
        class ParametersResult(_DynamicStructBuilder):
            @property
            def params(self) -> AnyPointer: ...
            @params.setter
            def params(self, value: AnyPointer) -> None: ...

        class CultivarResult(_DynamicStructBuilder):
            @property
            def info(self) -> IdInformationBuilder: ...
            @info.setter
            def info(
                self, value: IdInformationBuilder | IdInformationReader | dict[str, Any]
            ) -> None: ...
            @overload
            def init(
                self, field: Literal["info"], size: int | None = None
            ) -> IdInformationBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...

        class SpeciesResult(_DynamicStructBuilder):
            @property
            def info(self) -> IdInformationBuilder: ...
            @info.setter
            def info(
                self, value: IdInformationBuilder | IdInformationReader | dict[str, Any]
            ) -> None: ...
            @overload
            def init(
                self, field: Literal["info"], size: int | None = None
            ) -> IdInformationBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...

        class ParametersResultTuple(NamedTuple):
            params: AnyPointer

        class CultivarResultTuple(NamedTuple):
            info: IdInformationBuilder | IdInformationReader

        class SpeciesResultTuple(NamedTuple):
            info: IdInformationBuilder | IdInformationReader

        class ParametersParams(Protocol): ...

        class ParametersCallContext(Protocol):
            params: _CropInterfaceModule.Server.ParametersParams
            @property
            def results(self) -> _CropInterfaceModule.Server.ParametersResult: ...

        class CultivarParams(Protocol): ...

        class CultivarCallContext(Protocol):
            params: _CropInterfaceModule.Server.CultivarParams
            @property
            def results(self) -> _CropInterfaceModule.Server.CultivarResult: ...

        class SpeciesParams(Protocol): ...

        class SpeciesCallContext(Protocol):
            params: _CropInterfaceModule.Server.SpeciesParams
            @property
            def results(self) -> _CropInterfaceModule.Server.SpeciesResult: ...

        def parameters(
            self,
            _context: _CropInterfaceModule.Server.ParametersCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            AnyPointer | _CropInterfaceModule.Server.ParametersResultTuple | None
        ]: ...
        def parameters_context(
            self, context: _CropInterfaceModule.Server.ParametersCallContext
        ) -> Awaitable[None]: ...
        def cultivar(
            self,
            _context: _CropInterfaceModule.Server.CultivarCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            _IdInformationStructModule.Builder
            | _CropInterfaceModule.Server.CultivarResultTuple
            | None
        ]: ...
        def cultivar_context(
            self, context: _CropInterfaceModule.Server.CultivarCallContext
        ) -> Awaitable[None]: ...
        def species(
            self,
            _context: _CropInterfaceModule.Server.SpeciesCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            _IdInformationStructModule.Builder
            | _CropInterfaceModule.Server.SpeciesResultTuple
            | None
        ]: ...
        def species_context(
            self, context: _CropInterfaceModule.Server.SpeciesCallContext
        ) -> Awaitable[None]: ...

    class CropClient(
        _IdentifiableInterfaceModule.IdentifiableClient,
        _PersistentInterfaceModule.PersistentClient,
    ):
        class ParametersResult(Awaitable[ParametersResult], Protocol):
            params: _DynamicObjectReader

        class CultivarResult(Awaitable[CultivarResult], Protocol):
            info: IdInformationReader

        class SpeciesResult(Awaitable[SpeciesResult], Protocol):
            info: IdInformationReader

        def parameters(self) -> _CropInterfaceModule.CropClient.ParametersResult: ...
        def cultivar(self) -> _CropInterfaceModule.CropClient.CultivarResult: ...
        def species(self) -> _CropInterfaceModule.CropClient.SpeciesResult: ...
        def parameters_request(self) -> _CropInterfaceModule.ParametersRequest: ...
        def cultivar_request(self) -> _CropInterfaceModule.CultivarRequest: ...
        def species_request(self) -> _CropInterfaceModule.SpeciesRequest: ...

Crop: _CropInterfaceModule

class _ServiceInterfaceModule(_RegistryInterfaceModule):
    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _ServiceInterfaceModule.ServiceClient: ...
    class Server(_RegistryInterfaceModule.Server): ...
    class ServiceClient(_RegistryInterfaceModule.RegistryClient): ...

Service: _ServiceInterfaceModule

# Top-level type aliases for use in type annotations
type CropClient = _CropInterfaceModule.CropClient
type CropServer = _CropInterfaceModule.Server
type CultivarResult = _CropInterfaceModule.CropClient.CultivarResult
type ParametersResult = _CropInterfaceModule.CropClient.ParametersResult
type ServiceClient = _ServiceInterfaceModule.ServiceClient
type ServiceServer = _ServiceInterfaceModule.Server
type SpeciesResult = _CropInterfaceModule.CropClient.SpeciesResult
