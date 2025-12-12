"""This is an automatically generated stub for `cluster_admin_service.capnp`."""

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
from .common_capnp import _IdentifiableInterfaceModule
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

class _ModelInstanceFactoryClientList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> ModelInstanceFactoryClient: ...
        @override
        def __iter__(self) -> Iterator[ModelInstanceFactoryClient]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> ModelInstanceFactoryClient: ...
        @override
        def __setitem__(
            self,
            key: int,
            value: ModelInstanceFactoryClient
            | _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server,
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[ModelInstanceFactoryClient]: ...

class _ClusterStructModule(_StructModule):
    class _UnregisterInterfaceModule(_InterfaceModule):
        class UnregisterRequest(Protocol):
            def send(
                self,
            ) -> _ClusterStructModule._UnregisterInterfaceModule.UnregisterClient.UnregisterResult: ...

        @override
        def _new_client(
            self, server: _DynamicCapabilityServer
        ) -> _ClusterStructModule._UnregisterInterfaceModule.UnregisterClient: ...
        class Server(_DynamicCapabilityServer):
            class UnregisterResult(_DynamicStructBuilder):
                @property
                def success(self) -> bool: ...
                @success.setter
                def success(self, value: bool) -> None: ...

            class UnregisterResultTuple(NamedTuple):
                success: bool

            class UnregisterParams(Protocol): ...

            class UnregisterCallContext(Protocol):
                params: _ClusterStructModule._UnregisterInterfaceModule.Server.UnregisterParams
                @property
                def results(
                    self,
                ) -> _ClusterStructModule._UnregisterInterfaceModule.Server.UnregisterResult: ...

            def unregister(
                self,
                _context: _ClusterStructModule._UnregisterInterfaceModule.Server.UnregisterCallContext,
                **kwargs: Any,
            ) -> Awaitable[
                bool
                | _ClusterStructModule._UnregisterInterfaceModule.Server.UnregisterResultTuple
                | None
            ]: ...
            def unregister_context(
                self,
                context: _ClusterStructModule._UnregisterInterfaceModule.Server.UnregisterCallContext,
            ) -> Awaitable[None]: ...

        class UnregisterClient(_DynamicCapabilityClient):
            class UnregisterResult(Awaitable[UnregisterResult], Protocol):
                success: bool

            def unregister(
                self,
            ) -> _ClusterStructModule._UnregisterInterfaceModule.UnregisterClient.UnregisterResult: ...
            def unregister_request(
                self,
            ) -> _ClusterStructModule._UnregisterInterfaceModule.UnregisterRequest: ...

    Unregister: _UnregisterInterfaceModule
    type UnregisterClient = (
        _ClusterStructModule._UnregisterInterfaceModule.UnregisterClient
    )
    type UnregisterServer = _ClusterStructModule._UnregisterInterfaceModule.Server
    class _AdminMasterInterfaceModule(_IdentifiableInterfaceModule):
        class RegistermodelinstancefactoryRequest(Protocol):
            aModelId: str
            aFactory: (
                ModelInstanceFactoryClient
                | _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server
            )
            def send(
                self,
            ) -> _ClusterStructModule._AdminMasterInterfaceModule.AdminMasterClient.RegistermodelinstancefactoryResult: ...

        class AvailablemodelsRequest(Protocol):
            def send(
                self,
            ) -> _ClusterStructModule._AdminMasterInterfaceModule.AdminMasterClient.AvailablemodelsResult: ...

        @override
        def _new_client(
            self, server: _DynamicCapabilityServer
        ) -> _ClusterStructModule._AdminMasterInterfaceModule.AdminMasterClient: ...
        class Server(_IdentifiableInterfaceModule.Server):
            class RegistermodelinstancefactoryResult(_DynamicStructBuilder):
                @property
                def unregister(
                    self,
                ) -> (
                    _ClusterStructModule._UnregisterInterfaceModule.Server
                    | _ClusterStructModule._UnregisterInterfaceModule.UnregisterClient
                ): ...
                @unregister.setter
                def unregister(
                    self,
                    value: _ClusterStructModule._UnregisterInterfaceModule.Server
                    | _ClusterStructModule._UnregisterInterfaceModule.UnregisterClient,
                ) -> None: ...

            class AvailablemodelsResult(_DynamicStructBuilder):
                @property
                def factories(self) -> ModelInstanceFactoryClientListBuilder: ...
                @factories.setter
                def factories(
                    self,
                    value: ModelInstanceFactoryClientListBuilder
                    | ModelInstanceFactoryClientListReader
                    | Sequence[Any],
                ) -> None: ...
                @overload
                def init(
                    self, field: Literal["factories"], size: int | None = None
                ) -> ModelInstanceFactoryClientListBuilder: ...
                @overload
                def init(self, field: str, size: int | None = None) -> Any: ...

            class RegistermodelinstancefactoryResultTuple(NamedTuple):
                unregister: (
                    _ClusterStructModule._UnregisterInterfaceModule.Server
                    | _ClusterStructModule._UnregisterInterfaceModule.UnregisterClient
                )

            class AvailablemodelsResultTuple(NamedTuple):
                factories: (
                    ModelInstanceFactoryClientListBuilder
                    | ModelInstanceFactoryClientListReader
                )

            class RegistermodelinstancefactoryParams(Protocol):
                aModelId: str
                aFactory: ModelInstanceFactoryClient

            class RegistermodelinstancefactoryCallContext(Protocol):
                params: _ClusterStructModule._AdminMasterInterfaceModule.Server.RegistermodelinstancefactoryParams
                @property
                def results(
                    self,
                ) -> _ClusterStructModule._AdminMasterInterfaceModule.Server.RegistermodelinstancefactoryResult: ...

            class AvailablemodelsParams(Protocol): ...

            class AvailablemodelsCallContext(Protocol):
                params: _ClusterStructModule._AdminMasterInterfaceModule.Server.AvailablemodelsParams
                @property
                def results(
                    self,
                ) -> _ClusterStructModule._AdminMasterInterfaceModule.Server.AvailablemodelsResult: ...

            def registerModelInstanceFactory(
                self,
                aModelId: str,
                aFactory: ModelInstanceFactoryClient,
                _context: _ClusterStructModule._AdminMasterInterfaceModule.Server.RegistermodelinstancefactoryCallContext,
                **kwargs: Any,
            ) -> Awaitable[
                _ClusterStructModule._UnregisterInterfaceModule.Server
                | _ClusterStructModule._AdminMasterInterfaceModule.Server.RegistermodelinstancefactoryResultTuple
                | None
            ]: ...
            def registerModelInstanceFactory_context(
                self,
                context: _ClusterStructModule._AdminMasterInterfaceModule.Server.RegistermodelinstancefactoryCallContext,
            ) -> Awaitable[None]: ...
            def availableModels(
                self,
                _context: _ClusterStructModule._AdminMasterInterfaceModule.Server.AvailablemodelsCallContext,
                **kwargs: Any,
            ) -> Awaitable[
                Sequence[_ClusterStructModule._ModelInstanceFactoryInterfaceModule]
                | _ClusterStructModule._AdminMasterInterfaceModule.Server.AvailablemodelsResultTuple
                | None
            ]: ...
            def availableModels_context(
                self,
                context: _ClusterStructModule._AdminMasterInterfaceModule.Server.AvailablemodelsCallContext,
            ) -> Awaitable[None]: ...

        class AdminMasterClient(_IdentifiableInterfaceModule.IdentifiableClient):
            class RegistermodelinstancefactoryResult(
                Awaitable[RegistermodelinstancefactoryResult], Protocol
            ):
                unregister: (
                    _ClusterStructModule._UnregisterInterfaceModule.UnregisterClient
                )

            class AvailablemodelsResult(Awaitable[AvailablemodelsResult], Protocol):
                factories: ModelInstanceFactoryClientListReader

            def registerModelInstanceFactory(
                self,
                aModelId: str | None = None,
                aFactory: ModelInstanceFactoryClient
                | _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server
                | None = None,
            ) -> _ClusterStructModule._AdminMasterInterfaceModule.AdminMasterClient.RegistermodelinstancefactoryResult: ...
            def availableModels(
                self,
            ) -> _ClusterStructModule._AdminMasterInterfaceModule.AdminMasterClient.AvailablemodelsResult: ...
            def registerModelInstanceFactory_request(
                self,
                aModelId: str | None = None,
                aFactory: ModelInstanceFactoryClient
                | _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server
                | None = None,
            ) -> _ClusterStructModule._AdminMasterInterfaceModule.RegistermodelinstancefactoryRequest: ...
            def availableModels_request(
                self,
            ) -> (
                _ClusterStructModule._AdminMasterInterfaceModule.AvailablemodelsRequest
            ): ...

    class _ModelInstanceFactoryInterfaceModule(_IdentifiableInterfaceModule):
        class NewinstanceRequest(Protocol):
            def send(
                self,
            ) -> _ClusterStructModule._ModelInstanceFactoryInterfaceModule.ModelInstanceFactoryClient.NewinstanceResult: ...

        class NewinstancesRequest(Protocol):
            numberOfInstances: int
            def send(
                self,
            ) -> _ClusterStructModule._ModelInstanceFactoryInterfaceModule.ModelInstanceFactoryClient.NewinstancesResult: ...

        class NewcloudviazmqpipelineproxiesRequest(Protocol):
            numberOfInstances: int
            def send(
                self,
            ) -> _ClusterStructModule._ModelInstanceFactoryInterfaceModule.ModelInstanceFactoryClient.NewcloudviazmqpipelineproxiesResult: ...

        class NewcloudviaproxyRequest(Protocol):
            numberOfInstances: int
            def send(
                self,
            ) -> _ClusterStructModule._ModelInstanceFactoryInterfaceModule.ModelInstanceFactoryClient.NewcloudviaproxyResult: ...

        class ModelidRequest(Protocol):
            def send(
                self,
            ) -> _ClusterStructModule._ModelInstanceFactoryInterfaceModule.ModelInstanceFactoryClient.ModelidResult: ...

        class RegistermodelinstanceRequest(Protocol):
            instance: AnyPointer
            registrationToken: str
            def send(
                self,
            ) -> _ClusterStructModule._ModelInstanceFactoryInterfaceModule.ModelInstanceFactoryClient.RegistermodelinstanceResult: ...

        class RestoresturdyrefRequest(Protocol):
            sturdyRef: str
            def send(
                self,
            ) -> _ClusterStructModule._ModelInstanceFactoryInterfaceModule.ModelInstanceFactoryClient.RestoresturdyrefResult: ...

        @override
        def _new_client(
            self, server: _DynamicCapabilityServer
        ) -> _ClusterStructModule._ModelInstanceFactoryInterfaceModule.ModelInstanceFactoryClient: ...
        class Server(_IdentifiableInterfaceModule.Server):
            class NewinstanceResult(_DynamicStructBuilder):
                @property
                def instance(
                    self,
                ) -> (
                    _ClusterStructModule._ValueHolderInterfaceModule.Server
                    | _ClusterStructModule._ValueHolderInterfaceModule.ValueHolderClient
                ): ...
                @instance.setter
                def instance(
                    self,
                    value: _ClusterStructModule._ValueHolderInterfaceModule.Server
                    | _ClusterStructModule._ValueHolderInterfaceModule.ValueHolderClient,
                ) -> None: ...

            class NewinstancesResult(_DynamicStructBuilder):
                @property
                def instances(
                    self,
                ) -> (
                    _ClusterStructModule._ValueHolderInterfaceModule.Server
                    | _ClusterStructModule._ValueHolderInterfaceModule.ValueHolderClient
                ): ...
                @instances.setter
                def instances(
                    self,
                    value: _ClusterStructModule._ValueHolderInterfaceModule.Server
                    | _ClusterStructModule._ValueHolderInterfaceModule.ValueHolderClient,
                ) -> None: ...

            class NewcloudviazmqpipelineproxiesResult(_DynamicStructBuilder):
                @property
                def proxyAddresses(
                    self,
                ) -> (
                    _ClusterStructModule._ValueHolderInterfaceModule.Server
                    | _ClusterStructModule._ValueHolderInterfaceModule.ValueHolderClient
                ): ...
                @proxyAddresses.setter
                def proxyAddresses(
                    self,
                    value: _ClusterStructModule._ValueHolderInterfaceModule.Server
                    | _ClusterStructModule._ValueHolderInterfaceModule.ValueHolderClient,
                ) -> None: ...

            class NewcloudviaproxyResult(_DynamicStructBuilder):
                @property
                def proxy(
                    self,
                ) -> (
                    _ClusterStructModule._ValueHolderInterfaceModule.Server
                    | _ClusterStructModule._ValueHolderInterfaceModule.ValueHolderClient
                ): ...
                @proxy.setter
                def proxy(
                    self,
                    value: _ClusterStructModule._ValueHolderInterfaceModule.Server
                    | _ClusterStructModule._ValueHolderInterfaceModule.ValueHolderClient,
                ) -> None: ...

            class ModelidResult(_DynamicStructBuilder):
                @property
                def id(self) -> str: ...
                @id.setter
                def id(self, value: str) -> None: ...

            class RegistermodelinstanceResult(_DynamicStructBuilder):
                @property
                def unregister(
                    self,
                ) -> (
                    _ClusterStructModule._UnregisterInterfaceModule.Server
                    | _ClusterStructModule._UnregisterInterfaceModule.UnregisterClient
                ): ...
                @unregister.setter
                def unregister(
                    self,
                    value: _ClusterStructModule._UnregisterInterfaceModule.Server
                    | _ClusterStructModule._UnregisterInterfaceModule.UnregisterClient,
                ) -> None: ...

            class RestoresturdyrefResult(_DynamicStructBuilder):
                @property
                def cap(
                    self,
                ) -> (
                    _ClusterStructModule._ValueHolderInterfaceModule.Server
                    | _ClusterStructModule._ValueHolderInterfaceModule.ValueHolderClient
                ): ...
                @cap.setter
                def cap(
                    self,
                    value: _ClusterStructModule._ValueHolderInterfaceModule.Server
                    | _ClusterStructModule._ValueHolderInterfaceModule.ValueHolderClient,
                ) -> None: ...

            class NewinstanceResultTuple(NamedTuple):
                instance: (
                    _ClusterStructModule._ValueHolderInterfaceModule.Server
                    | _ClusterStructModule._ValueHolderInterfaceModule.ValueHolderClient
                )

            class NewinstancesResultTuple(NamedTuple):
                instances: (
                    _ClusterStructModule._ValueHolderInterfaceModule.Server
                    | _ClusterStructModule._ValueHolderInterfaceModule.ValueHolderClient
                )

            class NewcloudviazmqpipelineproxiesResultTuple(NamedTuple):
                proxyAddresses: (
                    _ClusterStructModule._ValueHolderInterfaceModule.Server
                    | _ClusterStructModule._ValueHolderInterfaceModule.ValueHolderClient
                )

            class NewcloudviaproxyResultTuple(NamedTuple):
                proxy: (
                    _ClusterStructModule._ValueHolderInterfaceModule.Server
                    | _ClusterStructModule._ValueHolderInterfaceModule.ValueHolderClient
                )

            class ModelidResultTuple(NamedTuple):
                id: str

            class RegistermodelinstanceResultTuple(NamedTuple):
                unregister: (
                    _ClusterStructModule._UnregisterInterfaceModule.Server
                    | _ClusterStructModule._UnregisterInterfaceModule.UnregisterClient
                )

            class RestoresturdyrefResultTuple(NamedTuple):
                cap: (
                    _ClusterStructModule._ValueHolderInterfaceModule.Server
                    | _ClusterStructModule._ValueHolderInterfaceModule.ValueHolderClient
                )

            class NewinstanceParams(Protocol): ...

            class NewinstanceCallContext(Protocol):
                params: _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.NewinstanceParams
                @property
                def results(
                    self,
                ) -> _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.NewinstanceResult: ...

            class NewinstancesParams(Protocol):
                numberOfInstances: int

            class NewinstancesCallContext(Protocol):
                params: _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.NewinstancesParams
                @property
                def results(
                    self,
                ) -> _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.NewinstancesResult: ...

            class NewcloudviazmqpipelineproxiesParams(Protocol):
                numberOfInstances: int

            class NewcloudviazmqpipelineproxiesCallContext(Protocol):
                params: _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.NewcloudviazmqpipelineproxiesParams
                @property
                def results(
                    self,
                ) -> _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.NewcloudviazmqpipelineproxiesResult: ...

            class NewcloudviaproxyParams(Protocol):
                numberOfInstances: int

            class NewcloudviaproxyCallContext(Protocol):
                params: _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.NewcloudviaproxyParams
                @property
                def results(
                    self,
                ) -> _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.NewcloudviaproxyResult: ...

            class ModelidParams(Protocol): ...

            class ModelidCallContext(Protocol):
                params: _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.ModelidParams
                @property
                def results(
                    self,
                ) -> _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.ModelidResult: ...

            class RegistermodelinstanceParams(Protocol):
                instance: AnyPointer
                registrationToken: str

            class RegistermodelinstanceCallContext(Protocol):
                params: _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.RegistermodelinstanceParams
                @property
                def results(
                    self,
                ) -> _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.RegistermodelinstanceResult: ...

            class RestoresturdyrefParams(Protocol):
                sturdyRef: str

            class RestoresturdyrefCallContext(Protocol):
                params: _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.RestoresturdyrefParams
                @property
                def results(
                    self,
                ) -> _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.RestoresturdyrefResult: ...

            def newInstance(
                self,
                _context: _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.NewinstanceCallContext,
                **kwargs: Any,
            ) -> Awaitable[
                _ClusterStructModule._ValueHolderInterfaceModule.Server
                | _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.NewinstanceResultTuple
                | None
            ]: ...
            def newInstance_context(
                self,
                context: _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.NewinstanceCallContext,
            ) -> Awaitable[None]: ...
            def newInstances(
                self,
                numberOfInstances: int,
                _context: _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.NewinstancesCallContext,
                **kwargs: Any,
            ) -> Awaitable[
                _ClusterStructModule._ValueHolderInterfaceModule.Server
                | _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.NewinstancesResultTuple
                | None
            ]: ...
            def newInstances_context(
                self,
                context: _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.NewinstancesCallContext,
            ) -> Awaitable[None]: ...
            def newCloudViaZmqPipelineProxies(
                self,
                numberOfInstances: int,
                _context: _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.NewcloudviazmqpipelineproxiesCallContext,
                **kwargs: Any,
            ) -> Awaitable[
                _ClusterStructModule._ValueHolderInterfaceModule.Server
                | _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.NewcloudviazmqpipelineproxiesResultTuple
                | None
            ]: ...
            def newCloudViaZmqPipelineProxies_context(
                self,
                context: _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.NewcloudviazmqpipelineproxiesCallContext,
            ) -> Awaitable[None]: ...
            def newCloudViaProxy(
                self,
                numberOfInstances: int,
                _context: _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.NewcloudviaproxyCallContext,
                **kwargs: Any,
            ) -> Awaitable[
                _ClusterStructModule._ValueHolderInterfaceModule.Server
                | _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.NewcloudviaproxyResultTuple
                | None
            ]: ...
            def newCloudViaProxy_context(
                self,
                context: _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.NewcloudviaproxyCallContext,
            ) -> Awaitable[None]: ...
            def modelId(
                self,
                _context: _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.ModelidCallContext,
                **kwargs: Any,
            ) -> Awaitable[
                str
                | _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.ModelidResultTuple
                | None
            ]: ...
            def modelId_context(
                self,
                context: _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.ModelidCallContext,
            ) -> Awaitable[None]: ...
            def registerModelInstance(
                self,
                instance: AnyPointer,
                registrationToken: str,
                _context: _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.RegistermodelinstanceCallContext,
                **kwargs: Any,
            ) -> Awaitable[
                _ClusterStructModule._UnregisterInterfaceModule.Server
                | _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.RegistermodelinstanceResultTuple
                | None
            ]: ...
            def registerModelInstance_context(
                self,
                context: _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.RegistermodelinstanceCallContext,
            ) -> Awaitable[None]: ...
            def restoreSturdyRef(
                self,
                sturdyRef: str,
                _context: _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.RestoresturdyrefCallContext,
                **kwargs: Any,
            ) -> Awaitable[
                _ClusterStructModule._ValueHolderInterfaceModule.Server
                | _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.RestoresturdyrefResultTuple
                | None
            ]: ...
            def restoreSturdyRef_context(
                self,
                context: _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server.RestoresturdyrefCallContext,
            ) -> Awaitable[None]: ...

        class ModelInstanceFactoryClient(
            _IdentifiableInterfaceModule.IdentifiableClient
        ):
            class NewinstanceResult(Awaitable[NewinstanceResult], Protocol):
                instance: (
                    _ClusterStructModule._ValueHolderInterfaceModule.ValueHolderClient
                )

            class NewinstancesResult(Awaitable[NewinstancesResult], Protocol):
                instances: (
                    _ClusterStructModule._ValueHolderInterfaceModule.ValueHolderClient
                )

            class NewcloudviazmqpipelineproxiesResult(
                Awaitable[NewcloudviazmqpipelineproxiesResult], Protocol
            ):
                proxyAddresses: (
                    _ClusterStructModule._ValueHolderInterfaceModule.ValueHolderClient
                )

            class NewcloudviaproxyResult(Awaitable[NewcloudviaproxyResult], Protocol):
                proxy: (
                    _ClusterStructModule._ValueHolderInterfaceModule.ValueHolderClient
                )

            class ModelidResult(Awaitable[ModelidResult], Protocol):
                id: str

            class RegistermodelinstanceResult(
                Awaitable[RegistermodelinstanceResult], Protocol
            ):
                unregister: (
                    _ClusterStructModule._UnregisterInterfaceModule.UnregisterClient
                )

            class RestoresturdyrefResult(Awaitable[RestoresturdyrefResult], Protocol):
                cap: _ClusterStructModule._ValueHolderInterfaceModule.ValueHolderClient

            def newInstance(
                self,
            ) -> _ClusterStructModule._ModelInstanceFactoryInterfaceModule.ModelInstanceFactoryClient.NewinstanceResult: ...
            def newInstances(
                self, numberOfInstances: int | None = None
            ) -> _ClusterStructModule._ModelInstanceFactoryInterfaceModule.ModelInstanceFactoryClient.NewinstancesResult: ...
            def newCloudViaZmqPipelineProxies(
                self, numberOfInstances: int | None = None
            ) -> _ClusterStructModule._ModelInstanceFactoryInterfaceModule.ModelInstanceFactoryClient.NewcloudviazmqpipelineproxiesResult: ...
            def newCloudViaProxy(
                self, numberOfInstances: int | None = None
            ) -> _ClusterStructModule._ModelInstanceFactoryInterfaceModule.ModelInstanceFactoryClient.NewcloudviaproxyResult: ...
            def modelId(
                self,
            ) -> _ClusterStructModule._ModelInstanceFactoryInterfaceModule.ModelInstanceFactoryClient.ModelidResult: ...
            def registerModelInstance(
                self,
                instance: AnyPointer | None = None,
                registrationToken: str | None = None,
            ) -> _ClusterStructModule._ModelInstanceFactoryInterfaceModule.ModelInstanceFactoryClient.RegistermodelinstanceResult: ...
            def restoreSturdyRef(
                self, sturdyRef: str | None = None
            ) -> _ClusterStructModule._ModelInstanceFactoryInterfaceModule.ModelInstanceFactoryClient.RestoresturdyrefResult: ...
            def newInstance_request(
                self,
            ) -> _ClusterStructModule._ModelInstanceFactoryInterfaceModule.NewinstanceRequest: ...
            def newInstances_request(
                self, numberOfInstances: int | None = None
            ) -> _ClusterStructModule._ModelInstanceFactoryInterfaceModule.NewinstancesRequest: ...
            def newCloudViaZmqPipelineProxies_request(
                self, numberOfInstances: int | None = None
            ) -> _ClusterStructModule._ModelInstanceFactoryInterfaceModule.NewcloudviazmqpipelineproxiesRequest: ...
            def newCloudViaProxy_request(
                self, numberOfInstances: int | None = None
            ) -> _ClusterStructModule._ModelInstanceFactoryInterfaceModule.NewcloudviaproxyRequest: ...
            def modelId_request(
                self,
            ) -> (
                _ClusterStructModule._ModelInstanceFactoryInterfaceModule.ModelidRequest
            ): ...
            def registerModelInstance_request(
                self,
                instance: AnyPointer | None = None,
                registrationToken: str | None = None,
            ) -> _ClusterStructModule._ModelInstanceFactoryInterfaceModule.RegistermodelinstanceRequest: ...
            def restoreSturdyRef_request(
                self, sturdyRef: str | None = None
            ) -> _ClusterStructModule._ModelInstanceFactoryInterfaceModule.RestoresturdyrefRequest: ...

    class _ValueHolderInterfaceModule(_InterfaceModule):
        class ValueRequest(Protocol):
            def send(
                self,
            ) -> _ClusterStructModule._ValueHolderInterfaceModule.ValueHolderClient.ValueResult: ...

        class ReleaseRequest(Protocol):
            def send(
                self,
            ) -> _ClusterStructModule._ValueHolderInterfaceModule.ValueHolderClient.ReleaseResult: ...

        @override
        def _new_client(
            self, server: _DynamicCapabilityServer
        ) -> _ClusterStructModule._ValueHolderInterfaceModule.ValueHolderClient: ...
        class Server(_DynamicCapabilityServer):
            class ValueResult(_DynamicStructBuilder):
                @property
                def val(self) -> AnyPointer: ...
                @val.setter
                def val(self, value: AnyPointer) -> None: ...

            class ReleaseResult(Awaitable[None], Protocol): ...

            class ValueResultTuple(NamedTuple):
                val: AnyPointer

            class ValueParams(Protocol): ...

            class ValueCallContext(Protocol):
                params: (
                    _ClusterStructModule._ValueHolderInterfaceModule.Server.ValueParams
                )
                @property
                def results(
                    self,
                ) -> (
                    _ClusterStructModule._ValueHolderInterfaceModule.Server.ValueResult
                ): ...

            class ReleaseParams(Protocol): ...

            class ReleaseCallContext(Protocol):
                params: _ClusterStructModule._ValueHolderInterfaceModule.Server.ReleaseParams

            def value(
                self,
                _context: _ClusterStructModule._ValueHolderInterfaceModule.Server.ValueCallContext,
                **kwargs: Any,
            ) -> Awaitable[
                AnyPointer
                | _ClusterStructModule._ValueHolderInterfaceModule.Server.ValueResultTuple
                | None
            ]: ...
            def value_context(
                self,
                context: _ClusterStructModule._ValueHolderInterfaceModule.Server.ValueCallContext,
            ) -> Awaitable[None]: ...
            def release(
                self,
                _context: _ClusterStructModule._ValueHolderInterfaceModule.Server.ReleaseCallContext,
                **kwargs: Any,
            ) -> Awaitable[None]: ...
            def release_context(
                self,
                context: _ClusterStructModule._ValueHolderInterfaceModule.Server.ReleaseCallContext,
            ) -> Awaitable[None]: ...

        class ValueHolderClient(_DynamicCapabilityClient):
            class ValueResult(Awaitable[ValueResult], Protocol):
                val: _DynamicObjectReader

            class ReleaseResult(Awaitable[None], Protocol): ...

            def value(
                self,
            ) -> _ClusterStructModule._ValueHolderInterfaceModule.ValueHolderClient.ValueResult: ...
            def release(
                self,
            ) -> _ClusterStructModule._ValueHolderInterfaceModule.ValueHolderClient.ReleaseResult: ...
            def value_request(
                self,
            ) -> _ClusterStructModule._ValueHolderInterfaceModule.ValueRequest: ...
            def release_request(
                self,
            ) -> _ClusterStructModule._ValueHolderInterfaceModule.ReleaseRequest: ...

    ValueHolder: _ValueHolderInterfaceModule
    type ValueHolderClient = (
        _ClusterStructModule._ValueHolderInterfaceModule.ValueHolderClient
    )
    type ValueHolderServer = _ClusterStructModule._ValueHolderInterfaceModule.Server
    ModelInstanceFactory: _ModelInstanceFactoryInterfaceModule
    type ModelInstanceFactoryClient = _ClusterStructModule._ModelInstanceFactoryInterfaceModule.ModelInstanceFactoryClient
    type ModelInstanceFactoryServer = (
        _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server
    )
    AdminMaster: _AdminMasterInterfaceModule
    type AdminMasterClient = (
        _ClusterStructModule._AdminMasterInterfaceModule.AdminMasterClient
    )
    type AdminMasterServer = _ClusterStructModule._AdminMasterInterfaceModule.Server
    class _UserMasterInterfaceModule(_IdentifiableInterfaceModule):
        class AvailablemodelsRequest(Protocol):
            def send(
                self,
            ) -> _ClusterStructModule._UserMasterInterfaceModule.UserMasterClient.AvailablemodelsResult: ...

        @override
        def _new_client(
            self, server: _DynamicCapabilityServer
        ) -> _ClusterStructModule._UserMasterInterfaceModule.UserMasterClient: ...
        class Server(_IdentifiableInterfaceModule.Server):
            class AvailablemodelsResult(_DynamicStructBuilder):
                @property
                def factories(self) -> ModelInstanceFactoryClientListBuilder: ...
                @factories.setter
                def factories(
                    self,
                    value: ModelInstanceFactoryClientListBuilder
                    | ModelInstanceFactoryClientListReader
                    | Sequence[Any],
                ) -> None: ...
                @overload
                def init(
                    self, field: Literal["factories"], size: int | None = None
                ) -> ModelInstanceFactoryClientListBuilder: ...
                @overload
                def init(self, field: str, size: int | None = None) -> Any: ...

            class AvailablemodelsResultTuple(NamedTuple):
                factories: (
                    ModelInstanceFactoryClientListBuilder
                    | ModelInstanceFactoryClientListReader
                )

            class AvailablemodelsParams(Protocol): ...

            class AvailablemodelsCallContext(Protocol):
                params: _ClusterStructModule._UserMasterInterfaceModule.Server.AvailablemodelsParams
                @property
                def results(
                    self,
                ) -> _ClusterStructModule._UserMasterInterfaceModule.Server.AvailablemodelsResult: ...

            def availableModels(
                self,
                _context: _ClusterStructModule._UserMasterInterfaceModule.Server.AvailablemodelsCallContext,
                **kwargs: Any,
            ) -> Awaitable[
                Sequence[_ClusterStructModule._ModelInstanceFactoryInterfaceModule]
                | _ClusterStructModule._UserMasterInterfaceModule.Server.AvailablemodelsResultTuple
                | None
            ]: ...
            def availableModels_context(
                self,
                context: _ClusterStructModule._UserMasterInterfaceModule.Server.AvailablemodelsCallContext,
            ) -> Awaitable[None]: ...

        class UserMasterClient(_IdentifiableInterfaceModule.IdentifiableClient):
            class AvailablemodelsResult(Awaitable[AvailablemodelsResult], Protocol):
                factories: ModelInstanceFactoryClientListReader

            def availableModels(
                self,
            ) -> _ClusterStructModule._UserMasterInterfaceModule.UserMasterClient.AvailablemodelsResult: ...
            def availableModels_request(
                self,
            ) -> (
                _ClusterStructModule._UserMasterInterfaceModule.AvailablemodelsRequest
            ): ...

    UserMaster: _UserMasterInterfaceModule
    type UserMasterClient = (
        _ClusterStructModule._UserMasterInterfaceModule.UserMasterClient
    )
    type UserMasterServer = _ClusterStructModule._UserMasterInterfaceModule.Server
    class _RuntimeInterfaceModule(_IdentifiableInterfaceModule):
        class RegistermodelinstancefactoryRequest(Protocol):
            aModelId: str
            aFactory: (
                ModelInstanceFactoryClient
                | _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server
            )
            def send(
                self,
            ) -> _ClusterStructModule._RuntimeInterfaceModule.RuntimeClient.RegistermodelinstancefactoryResult: ...

        class AvailablemodelsRequest(Protocol):
            def send(
                self,
            ) -> _ClusterStructModule._RuntimeInterfaceModule.RuntimeClient.AvailablemodelsResult: ...

        class NumberofcoresRequest(Protocol):
            def send(
                self,
            ) -> _ClusterStructModule._RuntimeInterfaceModule.RuntimeClient.NumberofcoresResult: ...

        class FreenumberofcoresRequest(Protocol):
            def send(
                self,
            ) -> _ClusterStructModule._RuntimeInterfaceModule.RuntimeClient.FreenumberofcoresResult: ...

        class ReservenumberofcoresRequest(Protocol):
            reserveCores: int
            aModelId: str
            def send(
                self,
            ) -> _ClusterStructModule._RuntimeInterfaceModule.RuntimeClient.ReservenumberofcoresResult: ...

        @override
        def _new_client(
            self, server: _DynamicCapabilityServer
        ) -> _ClusterStructModule._RuntimeInterfaceModule.RuntimeClient: ...
        class Server(_IdentifiableInterfaceModule.Server):
            class RegistermodelinstancefactoryResult(_DynamicStructBuilder):
                @property
                def unregister(
                    self,
                ) -> (
                    _ClusterStructModule._UnregisterInterfaceModule.Server
                    | _ClusterStructModule._UnregisterInterfaceModule.UnregisterClient
                ): ...
                @unregister.setter
                def unregister(
                    self,
                    value: _ClusterStructModule._UnregisterInterfaceModule.Server
                    | _ClusterStructModule._UnregisterInterfaceModule.UnregisterClient,
                ) -> None: ...

            class AvailablemodelsResult(_DynamicStructBuilder):
                @property
                def factories(self) -> ModelInstanceFactoryClientListBuilder: ...
                @factories.setter
                def factories(
                    self,
                    value: ModelInstanceFactoryClientListBuilder
                    | ModelInstanceFactoryClientListReader
                    | Sequence[Any],
                ) -> None: ...
                @overload
                def init(
                    self, field: Literal["factories"], size: int | None = None
                ) -> ModelInstanceFactoryClientListBuilder: ...
                @overload
                def init(self, field: str, size: int | None = None) -> Any: ...

            class NumberofcoresResult(_DynamicStructBuilder):
                @property
                def cores(self) -> int: ...
                @cores.setter
                def cores(self, value: int) -> None: ...

            class FreenumberofcoresResult(_DynamicStructBuilder):
                @property
                def cores(self) -> int: ...
                @cores.setter
                def cores(self, value: int) -> None: ...

            class ReservenumberofcoresResult(_DynamicStructBuilder):
                @property
                def reservedCores(self) -> int: ...
                @reservedCores.setter
                def reservedCores(self, value: int) -> None: ...

            class RegistermodelinstancefactoryResultTuple(NamedTuple):
                unregister: (
                    _ClusterStructModule._UnregisterInterfaceModule.Server
                    | _ClusterStructModule._UnregisterInterfaceModule.UnregisterClient
                )

            class AvailablemodelsResultTuple(NamedTuple):
                factories: (
                    ModelInstanceFactoryClientListBuilder
                    | ModelInstanceFactoryClientListReader
                )

            class NumberofcoresResultTuple(NamedTuple):
                cores: int

            class FreenumberofcoresResultTuple(NamedTuple):
                cores: int

            class ReservenumberofcoresResultTuple(NamedTuple):
                reservedCores: int

            class RegistermodelinstancefactoryParams(Protocol):
                aModelId: str
                aFactory: ModelInstanceFactoryClient

            class RegistermodelinstancefactoryCallContext(Protocol):
                params: _ClusterStructModule._RuntimeInterfaceModule.Server.RegistermodelinstancefactoryParams
                @property
                def results(
                    self,
                ) -> _ClusterStructModule._RuntimeInterfaceModule.Server.RegistermodelinstancefactoryResult: ...

            class AvailablemodelsParams(Protocol): ...

            class AvailablemodelsCallContext(Protocol):
                params: _ClusterStructModule._RuntimeInterfaceModule.Server.AvailablemodelsParams
                @property
                def results(
                    self,
                ) -> _ClusterStructModule._RuntimeInterfaceModule.Server.AvailablemodelsResult: ...

            class NumberofcoresParams(Protocol): ...

            class NumberofcoresCallContext(Protocol):
                params: _ClusterStructModule._RuntimeInterfaceModule.Server.NumberofcoresParams
                @property
                def results(
                    self,
                ) -> _ClusterStructModule._RuntimeInterfaceModule.Server.NumberofcoresResult: ...

            class FreenumberofcoresParams(Protocol): ...

            class FreenumberofcoresCallContext(Protocol):
                params: _ClusterStructModule._RuntimeInterfaceModule.Server.FreenumberofcoresParams
                @property
                def results(
                    self,
                ) -> _ClusterStructModule._RuntimeInterfaceModule.Server.FreenumberofcoresResult: ...

            class ReservenumberofcoresParams(Protocol):
                reserveCores: int
                aModelId: str

            class ReservenumberofcoresCallContext(Protocol):
                params: _ClusterStructModule._RuntimeInterfaceModule.Server.ReservenumberofcoresParams
                @property
                def results(
                    self,
                ) -> _ClusterStructModule._RuntimeInterfaceModule.Server.ReservenumberofcoresResult: ...

            def registerModelInstanceFactory(
                self,
                aModelId: str,
                aFactory: ModelInstanceFactoryClient,
                _context: _ClusterStructModule._RuntimeInterfaceModule.Server.RegistermodelinstancefactoryCallContext,
                **kwargs: Any,
            ) -> Awaitable[
                _ClusterStructModule._UnregisterInterfaceModule.Server
                | _ClusterStructModule._RuntimeInterfaceModule.Server.RegistermodelinstancefactoryResultTuple
                | None
            ]: ...
            def registerModelInstanceFactory_context(
                self,
                context: _ClusterStructModule._RuntimeInterfaceModule.Server.RegistermodelinstancefactoryCallContext,
            ) -> Awaitable[None]: ...
            def availableModels(
                self,
                _context: _ClusterStructModule._RuntimeInterfaceModule.Server.AvailablemodelsCallContext,
                **kwargs: Any,
            ) -> Awaitable[
                Sequence[_ClusterStructModule._ModelInstanceFactoryInterfaceModule]
                | _ClusterStructModule._RuntimeInterfaceModule.Server.AvailablemodelsResultTuple
                | None
            ]: ...
            def availableModels_context(
                self,
                context: _ClusterStructModule._RuntimeInterfaceModule.Server.AvailablemodelsCallContext,
            ) -> Awaitable[None]: ...
            def numberOfCores(
                self,
                _context: _ClusterStructModule._RuntimeInterfaceModule.Server.NumberofcoresCallContext,
                **kwargs: Any,
            ) -> Awaitable[
                int
                | _ClusterStructModule._RuntimeInterfaceModule.Server.NumberofcoresResultTuple
                | None
            ]: ...
            def numberOfCores_context(
                self,
                context: _ClusterStructModule._RuntimeInterfaceModule.Server.NumberofcoresCallContext,
            ) -> Awaitable[None]: ...
            def freeNumberOfCores(
                self,
                _context: _ClusterStructModule._RuntimeInterfaceModule.Server.FreenumberofcoresCallContext,
                **kwargs: Any,
            ) -> Awaitable[
                int
                | _ClusterStructModule._RuntimeInterfaceModule.Server.FreenumberofcoresResultTuple
                | None
            ]: ...
            def freeNumberOfCores_context(
                self,
                context: _ClusterStructModule._RuntimeInterfaceModule.Server.FreenumberofcoresCallContext,
            ) -> Awaitable[None]: ...
            def reserveNumberOfCores(
                self,
                reserveCores: int,
                aModelId: str,
                _context: _ClusterStructModule._RuntimeInterfaceModule.Server.ReservenumberofcoresCallContext,
                **kwargs: Any,
            ) -> Awaitable[
                int
                | _ClusterStructModule._RuntimeInterfaceModule.Server.ReservenumberofcoresResultTuple
                | None
            ]: ...
            def reserveNumberOfCores_context(
                self,
                context: _ClusterStructModule._RuntimeInterfaceModule.Server.ReservenumberofcoresCallContext,
            ) -> Awaitable[None]: ...

        class RuntimeClient(_IdentifiableInterfaceModule.IdentifiableClient):
            class RegistermodelinstancefactoryResult(
                Awaitable[RegistermodelinstancefactoryResult], Protocol
            ):
                unregister: (
                    _ClusterStructModule._UnregisterInterfaceModule.UnregisterClient
                )

            class AvailablemodelsResult(Awaitable[AvailablemodelsResult], Protocol):
                factories: ModelInstanceFactoryClientListReader

            class NumberofcoresResult(Awaitable[NumberofcoresResult], Protocol):
                cores: int

            class FreenumberofcoresResult(Awaitable[FreenumberofcoresResult], Protocol):
                cores: int

            class ReservenumberofcoresResult(
                Awaitable[ReservenumberofcoresResult], Protocol
            ):
                reservedCores: int

            def registerModelInstanceFactory(
                self,
                aModelId: str | None = None,
                aFactory: ModelInstanceFactoryClient
                | _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server
                | None = None,
            ) -> _ClusterStructModule._RuntimeInterfaceModule.RuntimeClient.RegistermodelinstancefactoryResult: ...
            def availableModels(
                self,
            ) -> _ClusterStructModule._RuntimeInterfaceModule.RuntimeClient.AvailablemodelsResult: ...
            def numberOfCores(
                self,
            ) -> _ClusterStructModule._RuntimeInterfaceModule.RuntimeClient.NumberofcoresResult: ...
            def freeNumberOfCores(
                self,
            ) -> _ClusterStructModule._RuntimeInterfaceModule.RuntimeClient.FreenumberofcoresResult: ...
            def reserveNumberOfCores(
                self, reserveCores: int | None = None, aModelId: str | None = None
            ) -> _ClusterStructModule._RuntimeInterfaceModule.RuntimeClient.ReservenumberofcoresResult: ...
            def registerModelInstanceFactory_request(
                self,
                aModelId: str | None = None,
                aFactory: ModelInstanceFactoryClient
                | _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server
                | None = None,
            ) -> _ClusterStructModule._RuntimeInterfaceModule.RegistermodelinstancefactoryRequest: ...
            def availableModels_request(
                self,
            ) -> (
                _ClusterStructModule._RuntimeInterfaceModule.AvailablemodelsRequest
            ): ...
            def numberOfCores_request(
                self,
            ) -> _ClusterStructModule._RuntimeInterfaceModule.NumberofcoresRequest: ...
            def freeNumberOfCores_request(
                self,
            ) -> (
                _ClusterStructModule._RuntimeInterfaceModule.FreenumberofcoresRequest
            ): ...
            def reserveNumberOfCores_request(
                self, reserveCores: int | None = None, aModelId: str | None = None
            ) -> (
                _ClusterStructModule._RuntimeInterfaceModule.ReservenumberofcoresRequest
            ): ...

    Runtime: _RuntimeInterfaceModule
    type RuntimeClient = _ClusterStructModule._RuntimeInterfaceModule.RuntimeClient
    type RuntimeServer = _ClusterStructModule._RuntimeInterfaceModule.Server
    class _ZmqPipelineAddressesStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def input(self) -> str: ...
            @property
            def output(self) -> str: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> ZmqPipelineAddressesBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def input(self) -> str: ...
            @input.setter
            def input(self, value: str) -> None: ...
            @property
            def output(self) -> str: ...
            @output.setter
            def output(self, value: str) -> None: ...
            @override
            def as_reader(self) -> ZmqPipelineAddressesReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            input: str | None = None,
            output: str | None = None,
            **kwargs: Any,
        ) -> ZmqPipelineAddressesBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[ZmqPipelineAddressesReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[ZmqPipelineAddressesReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[ZmqPipelineAddressesBuilder]: ...
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
        ) -> ZmqPipelineAddressesReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> ZmqPipelineAddressesReader: ...

    type ZmqPipelineAddressesReader = _ZmqPipelineAddressesStructModule.Reader
    type ZmqPipelineAddressesBuilder = _ZmqPipelineAddressesStructModule.Builder
    ZmqPipelineAddresses: _ZmqPipelineAddressesStructModule
    class Reader(_DynamicStructReader):
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> ClusterBuilder: ...

    class Builder(_DynamicStructBuilder):
        @override
        def as_reader(self) -> ClusterReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        **kwargs: Any,
    ) -> ClusterBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[ClusterReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[ClusterReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[ClusterBuilder]: ...
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
    ) -> ClusterReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> ClusterReader: ...

Cluster: _ClusterStructModule

# Top-level type aliases for use in type annotations
type AdminMasterClient = (
    _ClusterStructModule._AdminMasterInterfaceModule.AdminMasterClient
)
type AdminMasterServer = _ClusterStructModule._AdminMasterInterfaceModule.Server
type AvailablemodelsResult = (
    _ClusterStructModule._RuntimeInterfaceModule.RuntimeClient.AvailablemodelsResult
)
type ClusterBuilder = _ClusterStructModule.Builder
type ClusterReader = _ClusterStructModule.Reader
type FreenumberofcoresResult = (
    _ClusterStructModule._RuntimeInterfaceModule.RuntimeClient.FreenumberofcoresResult
)
type ModelInstanceFactoryClient = (
    _ClusterStructModule._ModelInstanceFactoryInterfaceModule.ModelInstanceFactoryClient
)
type ModelInstanceFactoryClientListBuilder = _ModelInstanceFactoryClientList.Builder
type ModelInstanceFactoryClientListReader = _ModelInstanceFactoryClientList.Reader
type ModelInstanceFactoryServer = (
    _ClusterStructModule._ModelInstanceFactoryInterfaceModule.Server
)
type ModelidResult = _ClusterStructModule._ModelInstanceFactoryInterfaceModule.ModelInstanceFactoryClient.ModelidResult
type NewcloudviaproxyResult = _ClusterStructModule._ModelInstanceFactoryInterfaceModule.ModelInstanceFactoryClient.NewcloudviaproxyResult
type NewcloudviazmqpipelineproxiesResult = _ClusterStructModule._ModelInstanceFactoryInterfaceModule.ModelInstanceFactoryClient.NewcloudviazmqpipelineproxiesResult
type NewinstanceResult = _ClusterStructModule._ModelInstanceFactoryInterfaceModule.ModelInstanceFactoryClient.NewinstanceResult
type NewinstancesResult = _ClusterStructModule._ModelInstanceFactoryInterfaceModule.ModelInstanceFactoryClient.NewinstancesResult
type NumberofcoresResult = (
    _ClusterStructModule._RuntimeInterfaceModule.RuntimeClient.NumberofcoresResult
)
type RegistermodelinstanceResult = _ClusterStructModule._ModelInstanceFactoryInterfaceModule.ModelInstanceFactoryClient.RegistermodelinstanceResult
type RegistermodelinstancefactoryResult = _ClusterStructModule._RuntimeInterfaceModule.RuntimeClient.RegistermodelinstancefactoryResult
type ReleaseResult = (
    _ClusterStructModule._ValueHolderInterfaceModule.ValueHolderClient.ReleaseResult
)
type ReservenumberofcoresResult = _ClusterStructModule._RuntimeInterfaceModule.RuntimeClient.ReservenumberofcoresResult
type RestoresturdyrefResult = _ClusterStructModule._ModelInstanceFactoryInterfaceModule.ModelInstanceFactoryClient.RestoresturdyrefResult
type RuntimeClient = _ClusterStructModule._RuntimeInterfaceModule.RuntimeClient
type RuntimeServer = _ClusterStructModule._RuntimeInterfaceModule.Server
type UnregisterClient = _ClusterStructModule._UnregisterInterfaceModule.UnregisterClient
type UnregisterResult = (
    _ClusterStructModule._UnregisterInterfaceModule.UnregisterClient.UnregisterResult
)
type UnregisterServer = _ClusterStructModule._UnregisterInterfaceModule.Server
type UserMasterClient = _ClusterStructModule._UserMasterInterfaceModule.UserMasterClient
type UserMasterServer = _ClusterStructModule._UserMasterInterfaceModule.Server
type ValueHolderClient = (
    _ClusterStructModule._ValueHolderInterfaceModule.ValueHolderClient
)
type ValueHolderServer = _ClusterStructModule._ValueHolderInterfaceModule.Server
type ValueResult = (
    _ClusterStructModule._ValueHolderInterfaceModule.ValueHolderClient.ValueResult
)
type ZmqPipelineAddressesBuilder = (
    _ClusterStructModule._ZmqPipelineAddressesStructModule.Builder
)
type ZmqPipelineAddressesReader = (
    _ClusterStructModule._ZmqPipelineAddressesStructModule.Reader
)
