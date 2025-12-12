"""This is an automatically generated stub for `web-berest-data-import.capnp`."""

from __future__ import annotations
from capnp.lib.capnp import (
    _DynamicCapabilityClient,
    _DynamicCapabilityServer,
    _DynamicStructBuilder,
    _InterfaceModule,
)
from collections.abc import Awaitable
from typing import override, Protocol, Any, NamedTuple

class _DWLABImportInterfaceModule(_InterfaceModule):
    class ImportdataRequest(Protocol):
        id: str
        dwla: bytes
        dwlb: bytes
        def send(
            self,
        ) -> _DWLABImportInterfaceModule.DWLABImportClient.ImportdataResult: ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _DWLABImportInterfaceModule.DWLABImportClient: ...
    class Server(_DynamicCapabilityServer):
        class ImportdataResult(_DynamicStructBuilder):
            @property
            def id(self) -> str: ...
            @id.setter
            def id(self, value: str) -> None: ...
            @property
            def successA(self) -> bool: ...
            @successA.setter
            def successA(self, value: bool) -> None: ...
            @property
            def successB(self) -> bool: ...
            @successB.setter
            def successB(self, value: bool) -> None: ...

        class ImportdataResultTuple(NamedTuple):
            id: str
            successA: bool
            successB: bool

        class ImportdataParams(Protocol):
            id: str
            dwla: bytes
            dwlb: bytes

        class ImportdataCallContext(Protocol):
            params: _DWLABImportInterfaceModule.Server.ImportdataParams
            @property
            def results(
                self,
            ) -> _DWLABImportInterfaceModule.Server.ImportdataResult: ...

        def importData(
            self,
            id: str,
            dwla: bytes,
            dwlb: bytes,
            _context: _DWLABImportInterfaceModule.Server.ImportdataCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            _DWLABImportInterfaceModule.Server.ImportdataResultTuple | None
        ]: ...
        def importData_context(
            self, context: _DWLABImportInterfaceModule.Server.ImportdataCallContext
        ) -> Awaitable[None]: ...

    class DWLABImportClient(_DynamicCapabilityClient):
        class ImportdataResult(Awaitable[ImportdataResult], Protocol):
            id: str
            successA: bool
            successB: bool

        def importData(
            self,
            id: str | None = None,
            dwla: bytes | None = None,
            dwlb: bytes | None = None,
        ) -> _DWLABImportInterfaceModule.DWLABImportClient.ImportdataResult: ...
        def importData_request(
            self,
            id: str | None = None,
            dwla: bytes | None = None,
            dwlb: bytes | None = None,
        ) -> _DWLABImportInterfaceModule.ImportdataRequest: ...

DWLABImport: _DWLABImportInterfaceModule

# Top-level type aliases for use in type annotations
type DWLABImportClient = _DWLABImportInterfaceModule.DWLABImportClient
type DWLABImportServer = _DWLABImportInterfaceModule.Server
type ImportdataResult = _DWLABImportInterfaceModule.DWLABImportClient.ImportdataResult
