"""This is an automatically generated stub for `config.capnp`."""

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
)
from collections.abc import Awaitable
from typing import override, Protocol, Any, NamedTuple

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

class _ServiceInterfaceModule(_InterfaceModule):
    class NextconfigRequest(Protocol):
        def send(self) -> _ServiceInterfaceModule.ServiceClient.NextconfigResult: ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _ServiceInterfaceModule.ServiceClient: ...
    class Server(_DynamicCapabilityServer):
        class NextconfigResult(_DynamicStructBuilder):
            @property
            def config(self) -> AnyPointer: ...
            @config.setter
            def config(self, value: AnyPointer) -> None: ...
            @property
            def noFurtherConfigs(self) -> bool: ...
            @noFurtherConfigs.setter
            def noFurtherConfigs(self, value: bool) -> None: ...

        class NextconfigResultTuple(NamedTuple):
            config: AnyPointer
            noFurtherConfigs: bool

        class NextconfigParams(Protocol): ...

        class NextconfigCallContext(Protocol):
            params: _ServiceInterfaceModule.Server.NextconfigParams
            @property
            def results(self) -> _ServiceInterfaceModule.Server.NextconfigResult: ...

        def nextConfig(
            self,
            _context: _ServiceInterfaceModule.Server.NextconfigCallContext,
            **kwargs: Any,
        ) -> Awaitable[_ServiceInterfaceModule.Server.NextconfigResultTuple | None]: ...
        def nextConfig_context(
            self, context: _ServiceInterfaceModule.Server.NextconfigCallContext
        ) -> Awaitable[None]: ...

    class ServiceClient(_DynamicCapabilityClient):
        class NextconfigResult(Awaitable[NextconfigResult], Protocol):
            config: _DynamicObjectReader
            noFurtherConfigs: bool

        def nextConfig(
            self,
        ) -> _ServiceInterfaceModule.ServiceClient.NextconfigResult: ...
        def nextConfig_request(self) -> _ServiceInterfaceModule.NextconfigRequest: ...

Service: _ServiceInterfaceModule

# Top-level type aliases for use in type annotations
type NextconfigResult = _ServiceInterfaceModule.ServiceClient.NextconfigResult
type ServiceClient = _ServiceInterfaceModule.ServiceClient
type ServiceServer = _ServiceInterfaceModule.Server
