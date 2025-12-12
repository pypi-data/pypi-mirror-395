"""This is an automatically generated stub for `model.capnp`."""

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
from .common_capnp import _IdentifiableInterfaceModule, IdentifiableClient
from .climate_capnp import _TimeSeriesInterfaceModule, TimeSeriesClient
from .soil_capnp import _ProfileInterfaceModule
from .management_capnp import EventReader, EventBuilder
from .persistence_capnp import _PersistentInterfaceModule
from .service_capnp import _StoppableInterfaceModule
from .common_capnp import IdInformationBuilder
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

class _XYResultStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def xs(self) -> Float64ListReader: ...
        @property
        def ys(self) -> Float64ListReader: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> XYResultBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def xs(self) -> Float64ListBuilder: ...
        @xs.setter
        def xs(
            self, value: Float64ListBuilder | Float64ListReader | dict[str, Any]
        ) -> None: ...
        @property
        def ys(self) -> Float64ListBuilder: ...
        @ys.setter
        def ys(
            self, value: Float64ListBuilder | Float64ListReader | dict[str, Any]
        ) -> None: ...
        @override
        @overload
        def init(
            self, field: Literal["xs"], size: int | None = None
        ) -> Float64ListBuilder: ...
        @overload
        def init(
            self, field: Literal["ys"], size: int | None = None
        ) -> Float64ListBuilder: ...
        @overload
        def init(self, field: str, size: int | None = None) -> Any: ...
        @override
        def as_reader(self) -> XYResultReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        xs: Float64ListBuilder | dict[str, Any] | None = None,
        ys: Float64ListBuilder | dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> XYResultBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[XYResultReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[XYResultReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[XYResultBuilder]: ...
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
    ) -> XYResultReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> XYResultReader: ...

XYResult: _XYResultStructModule

class _StatStructModule(_StructModule):
    class _TypeEnumModule:
        min: int
        max: int
        sd: int
        avg: int
        median: int

    Type: _TypeEnumModule
    class Reader(_DynamicStructReader):
        @property
        def type(self) -> StatTypeEnum: ...
        @property
        def vs(self) -> Float64ListReader: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> StatBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def type(self) -> StatTypeEnum: ...
        @type.setter
        def type(self, value: StatTypeEnum) -> None: ...
        @property
        def vs(self) -> Float64ListBuilder: ...
        @vs.setter
        def vs(
            self, value: Float64ListBuilder | Float64ListReader | dict[str, Any]
        ) -> None: ...
        @override
        def init(
            self, field: Literal["vs"], size: int | None = None
        ) -> Float64ListBuilder: ...
        @override
        def as_reader(self) -> StatReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        type: StatTypeEnum | None = None,
        vs: Float64ListBuilder | dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> StatBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[StatReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[StatReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[StatBuilder]: ...
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
    ) -> StatReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> StatReader: ...

Stat: _StatStructModule

class _StatList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> StatReader: ...
        @override
        def __iter__(self) -> Iterator[StatReader]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> StatBuilder: ...
        @override
        def __setitem__(
            self, key: int, value: StatReader | StatBuilder | dict[str, Any]
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[StatBuilder]: ...
        @override
        def init(self, index: int, size: int | None = None) -> StatBuilder: ...

class _XYPlusResultStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def xy(self) -> XYResultReader: ...
        @property
        def stats(self) -> StatListReader: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> XYPlusResultBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def xy(self) -> XYResultBuilder: ...
        @xy.setter
        def xy(
            self, value: XYResultBuilder | XYResultReader | dict[str, Any]
        ) -> None: ...
        @property
        def stats(self) -> StatListBuilder: ...
        @stats.setter
        def stats(
            self, value: StatListBuilder | StatListReader | dict[str, Any]
        ) -> None: ...
        @override
        @overload
        def init(
            self, field: Literal["xy"], size: int | None = None
        ) -> XYResultBuilder: ...
        @overload
        def init(
            self, field: Literal["stats"], size: int | None = None
        ) -> StatListBuilder: ...
        @overload
        def init(self, field: str, size: int | None = None) -> Any: ...
        @override
        def as_reader(self) -> XYPlusResultReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        xy: XYResultBuilder | dict[str, Any] | None = None,
        stats: StatListBuilder | dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> XYPlusResultBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[XYPlusResultReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[XYPlusResultReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[XYPlusResultBuilder]: ...
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
    ) -> XYPlusResultReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> XYPlusResultReader: ...

XYPlusResult: _XYPlusResultStructModule

class _ClimateInstanceInterfaceModule(_IdentifiableInterfaceModule):
    class RunRequest(Protocol):
        timeSeries: TimeSeriesClient | _TimeSeriesInterfaceModule.Server
        def send(
            self,
        ) -> _ClimateInstanceInterfaceModule.ClimateInstanceClient.RunResult: ...

    class RunsetRequest(Protocol):
        dataset: (
            TimeSeriesClientListBuilder | TimeSeriesClientListReader | Sequence[Any]
        )
        @overload
        def init(
            self, name: Literal["dataset"], size: int = ...
        ) -> TimeSeriesClientListBuilder: ...
        @overload
        def init(self, name: str, size: int = ...) -> Any: ...
        def send(
            self,
        ) -> _ClimateInstanceInterfaceModule.ClimateInstanceClient.RunsetResult: ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _ClimateInstanceInterfaceModule.ClimateInstanceClient: ...
    class Server(_IdentifiableInterfaceModule.Server):
        class RunResult(_DynamicStructBuilder):
            @property
            def result(self) -> XYResultBuilder: ...
            @result.setter
            def result(
                self, value: XYResultBuilder | XYResultReader | dict[str, Any]
            ) -> None: ...
            @overload
            def init(
                self, field: Literal["result"], size: int | None = None
            ) -> XYResultBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...

        class RunsetResult(_DynamicStructBuilder):
            @property
            def result(self) -> XYPlusResultBuilder: ...
            @result.setter
            def result(
                self, value: XYPlusResultBuilder | XYPlusResultReader | dict[str, Any]
            ) -> None: ...
            @overload
            def init(
                self, field: Literal["result"], size: int | None = None
            ) -> XYPlusResultBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...

        class RunResultTuple(NamedTuple):
            result: XYResultBuilder | XYResultReader

        class RunsetResultTuple(NamedTuple):
            result: XYPlusResultBuilder | XYPlusResultReader

        class RunParams(Protocol):
            timeSeries: TimeSeriesClient

        class RunCallContext(Protocol):
            params: _ClimateInstanceInterfaceModule.Server.RunParams
            @property
            def results(self) -> _ClimateInstanceInterfaceModule.Server.RunResult: ...

        class RunsetParams(Protocol):
            dataset: TimeSeriesClientListReader

        class RunsetCallContext(Protocol):
            params: _ClimateInstanceInterfaceModule.Server.RunsetParams
            @property
            def results(
                self,
            ) -> _ClimateInstanceInterfaceModule.Server.RunsetResult: ...

        def run(
            self,
            timeSeries: TimeSeriesClient,
            _context: _ClimateInstanceInterfaceModule.Server.RunCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            _XYResultStructModule.Builder
            | _ClimateInstanceInterfaceModule.Server.RunResultTuple
            | None
        ]: ...
        def run_context(
            self, context: _ClimateInstanceInterfaceModule.Server.RunCallContext
        ) -> Awaitable[None]: ...
        def runSet(
            self,
            dataset: TimeSeriesClientListReader,
            _context: _ClimateInstanceInterfaceModule.Server.RunsetCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            _XYPlusResultStructModule.Builder
            | _ClimateInstanceInterfaceModule.Server.RunsetResultTuple
            | None
        ]: ...
        def runSet_context(
            self, context: _ClimateInstanceInterfaceModule.Server.RunsetCallContext
        ) -> Awaitable[None]: ...

    class ClimateInstanceClient(_IdentifiableInterfaceModule.IdentifiableClient):
        class RunResult(Awaitable[RunResult], Protocol):
            result: XYResultReader

        class RunsetResult(Awaitable[RunsetResult], Protocol):
            result: XYPlusResultReader

        def run(
            self,
            timeSeries: TimeSeriesClient
            | _TimeSeriesInterfaceModule.Server
            | None = None,
        ) -> _ClimateInstanceInterfaceModule.ClimateInstanceClient.RunResult: ...
        def runSet(
            self,
            dataset: TimeSeriesClientListBuilder
            | TimeSeriesClientListReader
            | Sequence[Any]
            | None = None,
        ) -> _ClimateInstanceInterfaceModule.ClimateInstanceClient.RunsetResult: ...
        def run_request(
            self,
            timeSeries: TimeSeriesClient
            | _TimeSeriesInterfaceModule.Server
            | None = None,
        ) -> _ClimateInstanceInterfaceModule.RunRequest: ...
        def runSet_request(
            self,
            dataset: TimeSeriesClientListBuilder
            | TimeSeriesClientListReader
            | Sequence[Any]
            | None = None,
        ) -> _ClimateInstanceInterfaceModule.RunsetRequest: ...

class _TimeSeriesClientList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> TimeSeriesClient: ...
        @override
        def __iter__(self) -> Iterator[TimeSeriesClient]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> TimeSeriesClient: ...
        @override
        def __setitem__(
            self, key: int, value: TimeSeriesClient | _TimeSeriesInterfaceModule.Server
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[TimeSeriesClient]: ...

ClimateInstance: _ClimateInstanceInterfaceModule

class _EventList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> EventReader: ...
        @override
        def __iter__(self) -> Iterator[EventReader]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> EventBuilder: ...
        @override
        def __setitem__(
            self, key: int, value: EventReader | EventBuilder | dict[str, Any]
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[EventBuilder]: ...
        @override
        def init(self, index: int, size: int | None = None) -> EventBuilder: ...

class _EnvStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def rest(self) -> _DynamicObjectReader: ...
        @property
        def timeSeries(self) -> _TimeSeriesInterfaceModule.TimeSeriesClient: ...
        @property
        def soilProfile(self) -> _ProfileInterfaceModule.ProfileClient: ...
        @property
        def mgmtEvents(self) -> EventListReader: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> EnvBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def rest(self) -> _DynamicObjectReader: ...
        @rest.setter
        def rest(self, value: AnyPointer) -> None: ...
        @property
        def timeSeries(self) -> _TimeSeriesInterfaceModule.TimeSeriesClient: ...
        @timeSeries.setter
        def timeSeries(
            self,
            value: _TimeSeriesInterfaceModule.TimeSeriesClient
            | _TimeSeriesInterfaceModule.Server,
        ) -> None: ...
        @property
        def soilProfile(self) -> _ProfileInterfaceModule.ProfileClient: ...
        @soilProfile.setter
        def soilProfile(
            self,
            value: _ProfileInterfaceModule.ProfileClient
            | _ProfileInterfaceModule.Server,
        ) -> None: ...
        @property
        def mgmtEvents(self) -> EventListBuilder: ...
        @mgmtEvents.setter
        def mgmtEvents(
            self, value: EventListBuilder | EventListReader | dict[str, Any]
        ) -> None: ...
        @override
        def init(
            self, field: Literal["mgmtEvents"], size: int | None = None
        ) -> EventListBuilder: ...
        @override
        def as_reader(self) -> EnvReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        rest: AnyPointer | None = None,
        timeSeries: _TimeSeriesInterfaceModule.TimeSeriesClient
        | _TimeSeriesInterfaceModule.Server
        | None = None,
        soilProfile: _ProfileInterfaceModule.ProfileClient
        | _ProfileInterfaceModule.Server
        | None = None,
        mgmtEvents: EventListBuilder | dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> EnvBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[EnvReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[EnvReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[EnvBuilder]: ...
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
    ) -> EnvReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> EnvReader: ...

Env: _EnvStructModule

class _EnvInstanceInterfaceModule(
    _IdentifiableInterfaceModule, _PersistentInterfaceModule, _StoppableInterfaceModule
):
    class RunRequest(Protocol):
        env: EnvBuilder
        @overload
        def init(self, name: Literal["env"]) -> EnvBuilder: ...
        @overload
        def init(self, name: str, size: int = ...) -> Any: ...
        def send(self) -> _EnvInstanceInterfaceModule.EnvInstanceClient.RunResult: ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _EnvInstanceInterfaceModule.EnvInstanceClient: ...
    class Server(
        _IdentifiableInterfaceModule.Server,
        _PersistentInterfaceModule.Server,
        _StoppableInterfaceModule.Server,
    ):
        class RunResult(_DynamicStructBuilder):
            @property
            def result(self) -> AnyPointer: ...
            @result.setter
            def result(self, value: AnyPointer) -> None: ...

        class RunResultTuple(NamedTuple):
            result: AnyPointer

        class RunParams(Protocol):
            env: EnvReader

        class RunCallContext(Protocol):
            params: _EnvInstanceInterfaceModule.Server.RunParams
            @property
            def results(self) -> _EnvInstanceInterfaceModule.Server.RunResult: ...

        def run(
            self,
            env: EnvReader,
            _context: _EnvInstanceInterfaceModule.Server.RunCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            AnyPointer | _EnvInstanceInterfaceModule.Server.RunResultTuple | None
        ]: ...
        def run_context(
            self, context: _EnvInstanceInterfaceModule.Server.RunCallContext
        ) -> Awaitable[None]: ...

    class EnvInstanceClient(
        _IdentifiableInterfaceModule.IdentifiableClient,
        _PersistentInterfaceModule.PersistentClient,
        _StoppableInterfaceModule.StoppableClient,
    ):
        class RunResult(Awaitable[RunResult], Protocol):
            result: _DynamicObjectReader

        def run(
            self, env: EnvBuilder | EnvReader | dict[str, Any] | None = None
        ) -> _EnvInstanceInterfaceModule.EnvInstanceClient.RunResult: ...
        def run_request(
            self, env: EnvBuilder | None = None
        ) -> _EnvInstanceInterfaceModule.RunRequest: ...

EnvInstance: _EnvInstanceInterfaceModule

class _EnvInstanceProxyInterfaceModule(_EnvInstanceInterfaceModule):
    class _UnregisterInterfaceModule(_InterfaceModule):
        class UnregisterRequest(Protocol):
            def send(
                self,
            ) -> _EnvInstanceProxyInterfaceModule._UnregisterInterfaceModule.UnregisterClient.UnregisterResult: ...

        @override
        def _new_client(
            self, server: _DynamicCapabilityServer
        ) -> (
            _EnvInstanceProxyInterfaceModule._UnregisterInterfaceModule.UnregisterClient
        ): ...
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
                params: _EnvInstanceProxyInterfaceModule._UnregisterInterfaceModule.Server.UnregisterParams
                @property
                def results(
                    self,
                ) -> _EnvInstanceProxyInterfaceModule._UnregisterInterfaceModule.Server.UnregisterResult: ...

            def unregister(
                self,
                _context: _EnvInstanceProxyInterfaceModule._UnregisterInterfaceModule.Server.UnregisterCallContext,
                **kwargs: Any,
            ) -> Awaitable[
                bool
                | _EnvInstanceProxyInterfaceModule._UnregisterInterfaceModule.Server.UnregisterResultTuple
                | None
            ]: ...
            def unregister_context(
                self,
                context: _EnvInstanceProxyInterfaceModule._UnregisterInterfaceModule.Server.UnregisterCallContext,
            ) -> Awaitable[None]: ...

        class UnregisterClient(_DynamicCapabilityClient):
            class UnregisterResult(Awaitable[UnregisterResult], Protocol):
                success: bool

            def unregister(
                self,
            ) -> _EnvInstanceProxyInterfaceModule._UnregisterInterfaceModule.UnregisterClient.UnregisterResult: ...
            def unregister_request(
                self,
            ) -> _EnvInstanceProxyInterfaceModule._UnregisterInterfaceModule.UnregisterRequest: ...

    Unregister: _UnregisterInterfaceModule
    type UnregisterClient = (
        _EnvInstanceProxyInterfaceModule._UnregisterInterfaceModule.UnregisterClient
    )
    type UnregisterServer = (
        _EnvInstanceProxyInterfaceModule._UnregisterInterfaceModule.Server
    )
    class RegisterenvinstanceRequest(Protocol):
        instance: EnvInstanceClient | _EnvInstanceInterfaceModule.Server
        def send(
            self,
        ) -> _EnvInstanceProxyInterfaceModule.EnvInstanceProxyClient.RegisterenvinstanceResult: ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _EnvInstanceProxyInterfaceModule.EnvInstanceProxyClient: ...
    class Server(_EnvInstanceInterfaceModule.Server):
        class RegisterenvinstanceResult(_DynamicStructBuilder):
            @property
            def unregister(
                self,
            ) -> (
                _EnvInstanceProxyInterfaceModule._UnregisterInterfaceModule.Server
                | _EnvInstanceProxyInterfaceModule._UnregisterInterfaceModule.UnregisterClient
            ): ...
            @unregister.setter
            def unregister(
                self,
                value: _EnvInstanceProxyInterfaceModule._UnregisterInterfaceModule.Server
                | _EnvInstanceProxyInterfaceModule._UnregisterInterfaceModule.UnregisterClient,
            ) -> None: ...

        class RegisterenvinstanceResultTuple(NamedTuple):
            unregister: (
                _EnvInstanceProxyInterfaceModule._UnregisterInterfaceModule.Server
                | _EnvInstanceProxyInterfaceModule._UnregisterInterfaceModule.UnregisterClient
            )

        class RegisterenvinstanceParams(Protocol):
            instance: EnvInstanceClient

        class RegisterenvinstanceCallContext(Protocol):
            params: _EnvInstanceProxyInterfaceModule.Server.RegisterenvinstanceParams
            @property
            def results(
                self,
            ) -> _EnvInstanceProxyInterfaceModule.Server.RegisterenvinstanceResult: ...

        def registerEnvInstance(
            self,
            instance: EnvInstanceClient,
            _context: _EnvInstanceProxyInterfaceModule.Server.RegisterenvinstanceCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            _EnvInstanceProxyInterfaceModule._UnregisterInterfaceModule.Server
            | _EnvInstanceProxyInterfaceModule.Server.RegisterenvinstanceResultTuple
            | None
        ]: ...
        def registerEnvInstance_context(
            self,
            context: _EnvInstanceProxyInterfaceModule.Server.RegisterenvinstanceCallContext,
        ) -> Awaitable[None]: ...

    class EnvInstanceProxyClient(_EnvInstanceInterfaceModule.EnvInstanceClient):
        class RegisterenvinstanceResult(Awaitable[RegisterenvinstanceResult], Protocol):
            unregister: _EnvInstanceProxyInterfaceModule._UnregisterInterfaceModule.UnregisterClient

        def registerEnvInstance(
            self,
            instance: EnvInstanceClient
            | _EnvInstanceInterfaceModule.Server
            | None = None,
        ) -> _EnvInstanceProxyInterfaceModule.EnvInstanceProxyClient.RegisterenvinstanceResult: ...
        def registerEnvInstance_request(
            self,
            instance: EnvInstanceClient
            | _EnvInstanceInterfaceModule.Server
            | None = None,
        ) -> _EnvInstanceProxyInterfaceModule.RegisterenvinstanceRequest: ...

EnvInstanceProxy: _EnvInstanceProxyInterfaceModule

class _InstanceFactoryInterfaceModule(_IdentifiableInterfaceModule):
    class ModelinfoRequest(Protocol):
        def send(
            self,
        ) -> _InstanceFactoryInterfaceModule.InstanceFactoryClient.ModelinfoResult: ...

    class NewinstanceRequest(Protocol):
        def send(
            self,
        ) -> (
            _InstanceFactoryInterfaceModule.InstanceFactoryClient.NewinstanceResult
        ): ...

    class NewinstancesRequest(Protocol):
        numberOfInstances: int
        def send(
            self,
        ) -> (
            _InstanceFactoryInterfaceModule.InstanceFactoryClient.NewinstancesResult
        ): ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _InstanceFactoryInterfaceModule.InstanceFactoryClient: ...
    class Server(_IdentifiableInterfaceModule.Server):
        class ModelinfoResult(Awaitable[ModelinfoResult], Protocol):
            id: str
            name: str
            description: str

        class NewinstanceResult(_DynamicStructBuilder):
            @property
            def instance(
                self,
            ) -> (
                _IdentifiableInterfaceModule.Server
                | _IdentifiableInterfaceModule.IdentifiableClient
            ): ...
            @instance.setter
            def instance(
                self,
                value: _IdentifiableInterfaceModule.Server
                | _IdentifiableInterfaceModule.IdentifiableClient,
            ) -> None: ...

        class NewinstancesResult(_DynamicStructBuilder):
            @property
            def instances(self) -> IdentifiableClientListBuilder: ...
            @instances.setter
            def instances(
                self,
                value: IdentifiableClientListBuilder
                | IdentifiableClientListReader
                | Sequence[Any],
            ) -> None: ...
            @overload
            def init(
                self, field: Literal["instances"], size: int | None = None
            ) -> IdentifiableClientListBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...

        class ModelinfoResultTuple(NamedTuple):
            id: str
            name: str
            description: str

        class NewinstanceResultTuple(NamedTuple):
            instance: (
                _IdentifiableInterfaceModule.Server
                | _IdentifiableInterfaceModule.IdentifiableClient
            )

        class NewinstancesResultTuple(NamedTuple):
            instances: IdentifiableClientListBuilder | IdentifiableClientListReader

        class ModelinfoParams(Protocol): ...

        class ModelinfoCallContext(Protocol):
            params: _InstanceFactoryInterfaceModule.Server.ModelinfoParams
            @property
            def results(self) -> IdInformationBuilder: ...

        class NewinstanceParams(Protocol): ...

        class NewinstanceCallContext(Protocol):
            params: _InstanceFactoryInterfaceModule.Server.NewinstanceParams
            @property
            def results(
                self,
            ) -> _InstanceFactoryInterfaceModule.Server.NewinstanceResult: ...

        class NewinstancesParams(Protocol):
            numberOfInstances: int

        class NewinstancesCallContext(Protocol):
            params: _InstanceFactoryInterfaceModule.Server.NewinstancesParams
            @property
            def results(
                self,
            ) -> _InstanceFactoryInterfaceModule.Server.NewinstancesResult: ...

        def modelInfo(
            self,
            _context: _InstanceFactoryInterfaceModule.Server.ModelinfoCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            _InstanceFactoryInterfaceModule.Server.ModelinfoResultTuple | None
        ]: ...
        def modelInfo_context(
            self, context: _InstanceFactoryInterfaceModule.Server.ModelinfoCallContext
        ) -> Awaitable[None]: ...
        def newInstance(
            self,
            _context: _InstanceFactoryInterfaceModule.Server.NewinstanceCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            _IdentifiableInterfaceModule.Server
            | _InstanceFactoryInterfaceModule.Server.NewinstanceResultTuple
            | None
        ]: ...
        def newInstance_context(
            self, context: _InstanceFactoryInterfaceModule.Server.NewinstanceCallContext
        ) -> Awaitable[None]: ...
        def newInstances(
            self,
            numberOfInstances: int,
            _context: _InstanceFactoryInterfaceModule.Server.NewinstancesCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            Sequence[_IdentifiableInterfaceModule]
            | _InstanceFactoryInterfaceModule.Server.NewinstancesResultTuple
            | None
        ]: ...
        def newInstances_context(
            self,
            context: _InstanceFactoryInterfaceModule.Server.NewinstancesCallContext,
        ) -> Awaitable[None]: ...

    class InstanceFactoryClient(_IdentifiableInterfaceModule.IdentifiableClient):
        class ModelinfoResult(Awaitable[ModelinfoResult], Protocol):
            id: str
            name: str
            description: str

        class NewinstanceResult(Awaitable[NewinstanceResult], Protocol):
            instance: _IdentifiableInterfaceModule.IdentifiableClient

        class NewinstancesResult(Awaitable[NewinstancesResult], Protocol):
            instances: IdentifiableClientListReader

        def modelInfo(
            self,
        ) -> _InstanceFactoryInterfaceModule.InstanceFactoryClient.ModelinfoResult: ...
        def newInstance(
            self,
        ) -> (
            _InstanceFactoryInterfaceModule.InstanceFactoryClient.NewinstanceResult
        ): ...
        def newInstances(
            self, numberOfInstances: int | None = None
        ) -> (
            _InstanceFactoryInterfaceModule.InstanceFactoryClient.NewinstancesResult
        ): ...
        def modelInfo_request(
            self,
        ) -> _InstanceFactoryInterfaceModule.ModelinfoRequest: ...
        def newInstance_request(
            self,
        ) -> _InstanceFactoryInterfaceModule.NewinstanceRequest: ...
        def newInstances_request(
            self, numberOfInstances: int | None = None
        ) -> _InstanceFactoryInterfaceModule.NewinstancesRequest: ...

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

InstanceFactory: _InstanceFactoryInterfaceModule

# Top-level type aliases for use in type annotations
type ClimateInstanceClient = _ClimateInstanceInterfaceModule.ClimateInstanceClient
type ClimateInstanceServer = _ClimateInstanceInterfaceModule.Server
type EnvBuilder = _EnvStructModule.Builder
type EnvInstanceClient = _EnvInstanceInterfaceModule.EnvInstanceClient
type EnvInstanceProxyClient = _EnvInstanceProxyInterfaceModule.EnvInstanceProxyClient
type EnvInstanceProxyServer = _EnvInstanceProxyInterfaceModule.Server
type EnvInstanceServer = _EnvInstanceInterfaceModule.Server
type EnvReader = _EnvStructModule.Reader
type EventListBuilder = _EventList.Builder
type EventListReader = _EventList.Reader
type Float64ListBuilder = _Float64List.Builder
type Float64ListReader = _Float64List.Reader
type IdentifiableClientListBuilder = _IdentifiableClientList.Builder
type IdentifiableClientListReader = _IdentifiableClientList.Reader
type InstanceFactoryClient = _InstanceFactoryInterfaceModule.InstanceFactoryClient
type InstanceFactoryServer = _InstanceFactoryInterfaceModule.Server
type ModelinfoResult = (
    _InstanceFactoryInterfaceModule.InstanceFactoryClient.ModelinfoResult
)
type NewinstanceResult = (
    _InstanceFactoryInterfaceModule.InstanceFactoryClient.NewinstanceResult
)
type NewinstancesResult = (
    _InstanceFactoryInterfaceModule.InstanceFactoryClient.NewinstancesResult
)
type RegisterenvinstanceResult = (
    _EnvInstanceProxyInterfaceModule.EnvInstanceProxyClient.RegisterenvinstanceResult
)
type RunResult = _EnvInstanceInterfaceModule.EnvInstanceClient.RunResult
type RunsetResult = _ClimateInstanceInterfaceModule.ClimateInstanceClient.RunsetResult
type StatBuilder = _StatStructModule.Builder
type StatListBuilder = _StatList.Builder
type StatListReader = _StatList.Reader
type StatReader = _StatStructModule.Reader
type StatTypeEnum = int | Literal["min", "max", "sd", "avg", "median"]
type TimeSeriesClientListBuilder = _TimeSeriesClientList.Builder
type TimeSeriesClientListReader = _TimeSeriesClientList.Reader
type UnregisterClient = (
    _EnvInstanceProxyInterfaceModule._UnregisterInterfaceModule.UnregisterClient
)
type UnregisterResult = _EnvInstanceProxyInterfaceModule._UnregisterInterfaceModule.UnregisterClient.UnregisterResult
type UnregisterServer = (
    _EnvInstanceProxyInterfaceModule._UnregisterInterfaceModule.Server
)
type XYPlusResultBuilder = _XYPlusResultStructModule.Builder
type XYPlusResultReader = _XYPlusResultStructModule.Reader
type XYResultBuilder = _XYResultStructModule.Builder
type XYResultReader = _XYResultStructModule.Reader
