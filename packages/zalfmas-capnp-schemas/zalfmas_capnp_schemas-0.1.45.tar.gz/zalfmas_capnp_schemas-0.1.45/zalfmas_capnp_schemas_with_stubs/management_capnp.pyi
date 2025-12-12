"""This is an automatically generated stub for `management.capnp`."""

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
from .common_capnp import IdInformationReader, IdInformationBuilder
from .date_capnp import DateReader, DateBuilder
from .crop_capnp import _CropInterfaceModule
from .common_capnp import _IdentifiableInterfaceModule
from .persistence_capnp import _PersistentInterfaceModule
from .registry_capnp import _RegistryInterfaceModule
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

class _EventTypeEnumModule:
    sowing: int
    automaticSowing: int
    harvest: int
    automaticHarvest: int
    irrigation: int
    tillage: int
    organicFertilization: int
    mineralFertilization: int
    nDemandFertilization: int
    cutting: int
    setValue: int
    saveState: int

class _PlantOrganEnumModule:
    root: int
    leaf: int
    shoot: int
    fruit: int
    strukt: int
    sugar: int

class _EventStructModule(_StructModule):
    class _ExternalTypeEnumModule:
        sowing: int
        automaticSowing: int
        harvest: int
        automaticHarvest: int
        irrigation: int
        tillage: int
        organicFertilization: int
        mineralFertilization: int
        nDemandFertilization: int
        cutting: int

    ExternalType: _ExternalTypeEnumModule
    class _PhenoStageEnumModule:
        emergence: int
        flowering: int
        anthesis: int
        maturity: int

    PhenoStage: _PhenoStageEnumModule
    class _TypeStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def external(self) -> EventExternalTypeEnum: ...
            @property
            def internal(self) -> EventPhenoStageEnum: ...
            @override
            def which(self) -> Literal["external", "internal"]: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> TypeBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def external(self) -> EventExternalTypeEnum: ...
            @external.setter
            def external(self, value: EventExternalTypeEnum) -> None: ...
            @property
            def internal(self) -> EventPhenoStageEnum: ...
            @internal.setter
            def internal(self, value: EventPhenoStageEnum) -> None: ...
            @override
            def which(self) -> Literal["external", "internal"]: ...
            @override
            def as_reader(self) -> TypeReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            external: EventExternalTypeEnum | None = None,
            internal: EventPhenoStageEnum | None = None,
            **kwargs: Any,
        ) -> TypeBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[TypeReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[TypeReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[TypeBuilder]: ...
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
        ) -> TypeReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> TypeReader: ...

    type TypeReader = _TypeStructModule.Reader
    type TypeBuilder = _TypeStructModule.Builder
    Type: _TypeStructModule
    class _EventAtStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def date(self) -> DateReader: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> EventAtBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def date(self) -> DateBuilder: ...
            @date.setter
            def date(
                self, value: DateBuilder | DateReader | dict[str, Any]
            ) -> None: ...
            @override
            def init(
                self, field: Literal["date"], size: int | None = None
            ) -> DateBuilder: ...
            @override
            def as_reader(self) -> EventAtReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            date: DateBuilder | dict[str, Any] | None = None,
            **kwargs: Any,
        ) -> EventAtBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[EventAtReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[EventAtReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[EventAtBuilder]: ...
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
        ) -> EventAtReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> EventAtReader: ...

    type EventAtReader = _EventAtStructModule.Reader
    type EventAtBuilder = _EventAtStructModule.Builder
    EventAt: _EventAtStructModule
    class _EventBetweenStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def earliest(self) -> DateReader: ...
            @property
            def latest(self) -> DateReader: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> EventBetweenBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def earliest(self) -> DateBuilder: ...
            @earliest.setter
            def earliest(
                self, value: DateBuilder | DateReader | dict[str, Any]
            ) -> None: ...
            @property
            def latest(self) -> DateBuilder: ...
            @latest.setter
            def latest(
                self, value: DateBuilder | DateReader | dict[str, Any]
            ) -> None: ...
            @override
            @overload
            def init(
                self, field: Literal["earliest"], size: int | None = None
            ) -> DateBuilder: ...
            @overload
            def init(
                self, field: Literal["latest"], size: int | None = None
            ) -> DateBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...
            @override
            def as_reader(self) -> EventBetweenReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            earliest: DateBuilder | dict[str, Any] | None = None,
            latest: DateBuilder | dict[str, Any] | None = None,
            **kwargs: Any,
        ) -> EventBetweenBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[EventBetweenReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[EventBetweenReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[EventBetweenBuilder]: ...
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
        ) -> EventBetweenReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> EventBetweenReader: ...

    type EventBetweenReader = _EventBetweenStructModule.Reader
    type EventBetweenBuilder = _EventBetweenStructModule.Builder
    EventBetween: _EventBetweenStructModule
    class _EventAfterStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def event(self) -> TypeReader: ...
            @property
            def days(self) -> int: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> EventAfterBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def event(self) -> TypeBuilder: ...
            @event.setter
            def event(
                self, value: TypeBuilder | TypeReader | dict[str, Any]
            ) -> None: ...
            @property
            def days(self) -> int: ...
            @days.setter
            def days(self, value: int) -> None: ...
            @override
            def init(
                self, field: Literal["event"], size: int | None = None
            ) -> TypeBuilder: ...
            @override
            def as_reader(self) -> EventAfterReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            event: TypeBuilder | dict[str, Any] | None = None,
            days: int | None = None,
            **kwargs: Any,
        ) -> EventAfterBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[EventAfterReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[EventAfterReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[EventAfterBuilder]: ...
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
        ) -> EventAfterReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> EventAfterReader: ...

    type EventAfterReader = _EventAfterStructModule.Reader
    type EventAfterBuilder = _EventAfterStructModule.Builder
    EventAfter: _EventAfterStructModule
    class Reader(_DynamicStructReader):
        @property
        def type(self) -> EventExternalTypeEnum: ...
        @property
        def info(self) -> IdInformationReader: ...
        @property
        def at(self) -> EventAtReader: ...
        @property
        def between(self) -> EventBetweenReader: ...
        @property
        def after(self) -> EventAfterReader: ...
        @property
        def params(self) -> _DynamicObjectReader: ...
        @property
        def runAtStartOfDay(self) -> bool: ...
        @override
        def which(self) -> Literal["at", "between", "after"]: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> EventBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def type(self) -> EventExternalTypeEnum: ...
        @type.setter
        def type(self, value: EventExternalTypeEnum) -> None: ...
        @property
        def info(self) -> IdInformationBuilder: ...
        @info.setter
        def info(
            self, value: IdInformationBuilder | IdInformationReader | dict[str, Any]
        ) -> None: ...
        @property
        def at(self) -> EventAtBuilder: ...
        @at.setter
        def at(
            self, value: EventAtBuilder | EventAtReader | dict[str, Any]
        ) -> None: ...
        @property
        def between(self) -> EventBetweenBuilder: ...
        @between.setter
        def between(
            self, value: EventBetweenBuilder | EventBetweenReader | dict[str, Any]
        ) -> None: ...
        @property
        def after(self) -> EventAfterBuilder: ...
        @after.setter
        def after(
            self, value: EventAfterBuilder | EventAfterReader | dict[str, Any]
        ) -> None: ...
        @property
        def params(self) -> _DynamicObjectBuilder: ...
        @params.setter
        def params(self, value: AnyPointer) -> None: ...
        @property
        def runAtStartOfDay(self) -> bool: ...
        @runAtStartOfDay.setter
        def runAtStartOfDay(self, value: bool) -> None: ...
        @override
        def which(self) -> Literal["at", "between", "after"]: ...
        @override
        @overload
        def init(
            self, field: Literal["info"], size: int | None = None
        ) -> IdInformationBuilder: ...
        @overload
        def init(
            self, field: Literal["at"], size: int | None = None
        ) -> EventAtBuilder: ...
        @overload
        def init(
            self, field: Literal["between"], size: int | None = None
        ) -> EventBetweenBuilder: ...
        @overload
        def init(
            self, field: Literal["after"], size: int | None = None
        ) -> EventAfterBuilder: ...
        @overload
        def init(self, field: str, size: int | None = None) -> Any: ...
        @override
        def as_reader(self) -> EventReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        type: EventExternalTypeEnum | None = None,
        info: IdInformationBuilder | dict[str, Any] | None = None,
        at: EventAtBuilder | dict[str, Any] | None = None,
        between: EventBetweenBuilder | dict[str, Any] | None = None,
        after: EventAfterBuilder | dict[str, Any] | None = None,
        params: AnyPointer | None = None,
        runAtStartOfDay: bool | None = None,
        **kwargs: Any,
    ) -> EventBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[EventReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[EventReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[EventBuilder]: ...
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
    ) -> EventReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> EventReader: ...

Event: _EventStructModule

class _SpecList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> SpecReader: ...
        @override
        def __iter__(self) -> Iterator[SpecReader]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> SpecBuilder: ...
        @override
        def __setitem__(
            self, key: int, value: SpecReader | SpecBuilder | dict[str, Any]
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[SpecBuilder]: ...
        @override
        def init(self, index: int, size: int | None = None) -> SpecBuilder: ...

class _FertilizerInterfaceModule(
    _IdentifiableInterfaceModule, _PersistentInterfaceModule
):
    class NutrientsRequest(Protocol):
        def send(
            self,
        ) -> _FertilizerInterfaceModule.FertilizerClient.NutrientsResult: ...

    class ParametersRequest(Protocol):
        def send(
            self,
        ) -> _FertilizerInterfaceModule.FertilizerClient.ParametersResult: ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _FertilizerInterfaceModule.FertilizerClient: ...
    class Server(
        _IdentifiableInterfaceModule.Server, _PersistentInterfaceModule.Server
    ):
        class NutrientsResult(_DynamicStructBuilder):
            @property
            def nutrients(self) -> NutrientListBuilder: ...
            @nutrients.setter
            def nutrients(
                self, value: NutrientListBuilder | NutrientListReader | Sequence[Any]
            ) -> None: ...
            @overload
            def init(
                self, field: Literal["nutrients"], size: int | None = None
            ) -> NutrientListBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...

        class ParametersResult(_DynamicStructBuilder):
            @property
            def params(self) -> AnyPointer: ...
            @params.setter
            def params(self, value: AnyPointer) -> None: ...

        class NutrientsResultTuple(NamedTuple):
            nutrients: NutrientListBuilder | NutrientListReader

        class ParametersResultTuple(NamedTuple):
            params: AnyPointer

        class NutrientsParams(Protocol): ...

        class NutrientsCallContext(Protocol):
            params: _FertilizerInterfaceModule.Server.NutrientsParams
            @property
            def results(self) -> _FertilizerInterfaceModule.Server.NutrientsResult: ...

        class ParametersParams(Protocol): ...

        class ParametersCallContext(Protocol):
            params: _FertilizerInterfaceModule.Server.ParametersParams
            @property
            def results(self) -> _FertilizerInterfaceModule.Server.ParametersResult: ...

        def nutrients(
            self,
            _context: _FertilizerInterfaceModule.Server.NutrientsCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            Sequence[NutrientBuilder | NutrientReader]
            | _FertilizerInterfaceModule.Server.NutrientsResultTuple
            | None
        ]: ...
        def nutrients_context(
            self, context: _FertilizerInterfaceModule.Server.NutrientsCallContext
        ) -> Awaitable[None]: ...
        def parameters(
            self,
            _context: _FertilizerInterfaceModule.Server.ParametersCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            AnyPointer | _FertilizerInterfaceModule.Server.ParametersResultTuple | None
        ]: ...
        def parameters_context(
            self, context: _FertilizerInterfaceModule.Server.ParametersCallContext
        ) -> Awaitable[None]: ...

    class FertilizerClient(
        _IdentifiableInterfaceModule.IdentifiableClient,
        _PersistentInterfaceModule.PersistentClient,
    ):
        class NutrientsResult(Awaitable[NutrientsResult], Protocol):
            nutrients: NutrientListReader

        class ParametersResult(Awaitable[ParametersResult], Protocol):
            params: _DynamicObjectReader

        def nutrients(
            self,
        ) -> _FertilizerInterfaceModule.FertilizerClient.NutrientsResult: ...
        def parameters(
            self,
        ) -> _FertilizerInterfaceModule.FertilizerClient.ParametersResult: ...
        def nutrients_request(self) -> _FertilizerInterfaceModule.NutrientsRequest: ...
        def parameters_request(
            self,
        ) -> _FertilizerInterfaceModule.ParametersRequest: ...

class _NutrientStructModule(_StructModule):
    class _NameEnumModule:
        urea: int
        ammonia: int
        nitrate: int
        phosphorus: int
        potassium: int
        sulfate: int
        organicC: int
        organicN: int
        organicP: int
        organicNFast: int
        organicNSlow: int

    Name: _NameEnumModule
    class _UnitEnumModule:
        none: int
        fraction: int
        percent: int

    Unit: _UnitEnumModule
    class Reader(_DynamicStructReader):
        @property
        def nutrient(self) -> NutrientNameEnum: ...
        @property
        def value(self) -> float: ...
        @property
        def unit(self) -> NutrientUnitEnum: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> NutrientBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def nutrient(self) -> NutrientNameEnum: ...
        @nutrient.setter
        def nutrient(self, value: NutrientNameEnum) -> None: ...
        @property
        def value(self) -> float: ...
        @value.setter
        def value(self, value: float) -> None: ...
        @property
        def unit(self) -> NutrientUnitEnum: ...
        @unit.setter
        def unit(self, value: NutrientUnitEnum) -> None: ...
        @override
        def as_reader(self) -> NutrientReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        nutrient: NutrientNameEnum | None = None,
        value: float | None = None,
        unit: NutrientUnitEnum | None = None,
        **kwargs: Any,
    ) -> NutrientBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[NutrientReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[NutrientReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[NutrientBuilder]: ...
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
    ) -> NutrientReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> NutrientReader: ...

Nutrient: _NutrientStructModule

class _NutrientList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> NutrientReader: ...
        @override
        def __iter__(self) -> Iterator[NutrientReader]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> NutrientBuilder: ...
        @override
        def __setitem__(
            self, key: int, value: NutrientReader | NutrientBuilder | dict[str, Any]
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[NutrientBuilder]: ...
        @override
        def init(self, index: int, size: int | None = None) -> NutrientBuilder: ...

Fertilizer: _FertilizerInterfaceModule

class _ParamsStructModule(_StructModule):
    class _SowingStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def cultivar(self) -> str: ...
            @property
            def plantDensity(self) -> int: ...
            @property
            def crop(self) -> _CropInterfaceModule.CropClient: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> SowingBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def cultivar(self) -> str: ...
            @cultivar.setter
            def cultivar(self, value: str) -> None: ...
            @property
            def plantDensity(self) -> int: ...
            @plantDensity.setter
            def plantDensity(self, value: int) -> None: ...
            @property
            def crop(self) -> _CropInterfaceModule.CropClient: ...
            @crop.setter
            def crop(
                self,
                value: _CropInterfaceModule.CropClient | _CropInterfaceModule.Server,
            ) -> None: ...
            @override
            def as_reader(self) -> SowingReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            cultivar: str | None = None,
            plantDensity: int | None = None,
            crop: _CropInterfaceModule.CropClient
            | _CropInterfaceModule.Server
            | None = None,
            **kwargs: Any,
        ) -> SowingBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[SowingReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[SowingReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[SowingBuilder]: ...
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
        ) -> SowingReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> SowingReader: ...

    type SowingReader = _SowingStructModule.Reader
    type SowingBuilder = _SowingStructModule.Builder
    Sowing: _SowingStructModule
    class _AutomaticSowingStructModule(_StructModule):
        class _AvgSoilTempStructModule(_StructModule):
            class Reader(_DynamicStructReader):
                @property
                def soilDepthForAveraging(self) -> float: ...
                @property
                def daysInSoilTempWindow(self) -> int: ...
                @property
                def sowingIfAboveAvgSoilTemp(self) -> float: ...
                @override
                def as_builder(
                    self,
                    num_first_segment_words: int | None = None,
                    allocate_seg_callable: Callable[[int], bytearray] | None = None,
                ) -> AvgSoilTempBuilder: ...

            class Builder(_DynamicStructBuilder):
                @property
                def soilDepthForAveraging(self) -> float: ...
                @soilDepthForAveraging.setter
                def soilDepthForAveraging(self, value: float) -> None: ...
                @property
                def daysInSoilTempWindow(self) -> int: ...
                @daysInSoilTempWindow.setter
                def daysInSoilTempWindow(self, value: int) -> None: ...
                @property
                def sowingIfAboveAvgSoilTemp(self) -> float: ...
                @sowingIfAboveAvgSoilTemp.setter
                def sowingIfAboveAvgSoilTemp(self, value: float) -> None: ...
                @override
                def as_reader(self) -> AvgSoilTempReader: ...

            @override
            def new_message(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
                soilDepthForAveraging: float | None = None,
                daysInSoilTempWindow: int | None = None,
                sowingIfAboveAvgSoilTemp: float | None = None,
                **kwargs: Any,
            ) -> AvgSoilTempBuilder: ...
            @override
            @overload
            def from_bytes(
                self,
                buf: bytes,
                traversal_limit_in_words: int | None = None,
                nesting_limit: int | None = None,
            ) -> AbstractContextManager[AvgSoilTempReader]: ...
            @overload
            def from_bytes(
                self,
                buf: bytes,
                traversal_limit_in_words: int | None = None,
                nesting_limit: int | None = None,
                *,
                builder: Literal[False],
            ) -> AbstractContextManager[AvgSoilTempReader]: ...
            @overload
            def from_bytes(
                self,
                buf: bytes,
                traversal_limit_in_words: int | None = None,
                nesting_limit: int | None = None,
                *,
                builder: Literal[True],
            ) -> AbstractContextManager[AvgSoilTempBuilder]: ...
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
            ) -> AvgSoilTempReader: ...
            @override
            def read_packed(
                self,
                file: IO[str] | IO[bytes],
                traversal_limit_in_words: int | None = None,
                nesting_limit: int | None = None,
            ) -> AvgSoilTempReader: ...

        type AvgSoilTempReader = _AvgSoilTempStructModule.Reader
        type AvgSoilTempBuilder = _AvgSoilTempStructModule.Builder
        AvgSoilTemp: _AvgSoilTempStructModule
        class Reader(_DynamicStructReader):
            @property
            def minTempThreshold(self) -> float: ...
            @property
            def daysInTempWindow(self) -> int: ...
            @property
            def minPercentASW(self) -> float: ...
            @property
            def maxPercentASW(self) -> float: ...
            @property
            def max3dayPrecipSum(self) -> float: ...
            @property
            def maxCurrentDayPrecipSum(self) -> float: ...
            @property
            def tempSumAboveBaseTemp(self) -> float: ...
            @property
            def baseTemp(self) -> float: ...
            @property
            def avgSoilTemp(self) -> AvgSoilTempReader: ...
            @property
            def sowing(self) -> SowingReader: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> AutomaticSowingBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def minTempThreshold(self) -> float: ...
            @minTempThreshold.setter
            def minTempThreshold(self, value: float) -> None: ...
            @property
            def daysInTempWindow(self) -> int: ...
            @daysInTempWindow.setter
            def daysInTempWindow(self, value: int) -> None: ...
            @property
            def minPercentASW(self) -> float: ...
            @minPercentASW.setter
            def minPercentASW(self, value: float) -> None: ...
            @property
            def maxPercentASW(self) -> float: ...
            @maxPercentASW.setter
            def maxPercentASW(self, value: float) -> None: ...
            @property
            def max3dayPrecipSum(self) -> float: ...
            @max3dayPrecipSum.setter
            def max3dayPrecipSum(self, value: float) -> None: ...
            @property
            def maxCurrentDayPrecipSum(self) -> float: ...
            @maxCurrentDayPrecipSum.setter
            def maxCurrentDayPrecipSum(self, value: float) -> None: ...
            @property
            def tempSumAboveBaseTemp(self) -> float: ...
            @tempSumAboveBaseTemp.setter
            def tempSumAboveBaseTemp(self, value: float) -> None: ...
            @property
            def baseTemp(self) -> float: ...
            @baseTemp.setter
            def baseTemp(self, value: float) -> None: ...
            @property
            def avgSoilTemp(self) -> AvgSoilTempBuilder: ...
            @avgSoilTemp.setter
            def avgSoilTemp(
                self, value: AvgSoilTempBuilder | AvgSoilTempReader | dict[str, Any]
            ) -> None: ...
            @property
            def sowing(self) -> SowingBuilder: ...
            @sowing.setter
            def sowing(
                self, value: SowingBuilder | SowingReader | dict[str, Any]
            ) -> None: ...
            @override
            @overload
            def init(
                self, field: Literal["avgSoilTemp"], size: int | None = None
            ) -> AvgSoilTempBuilder: ...
            @overload
            def init(
                self, field: Literal["sowing"], size: int | None = None
            ) -> SowingBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...
            @override
            def as_reader(self) -> AutomaticSowingReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            minTempThreshold: float | None = None,
            daysInTempWindow: int | None = None,
            minPercentASW: float | None = None,
            maxPercentASW: float | None = None,
            max3dayPrecipSum: float | None = None,
            maxCurrentDayPrecipSum: float | None = None,
            tempSumAboveBaseTemp: float | None = None,
            baseTemp: float | None = None,
            avgSoilTemp: AvgSoilTempBuilder | dict[str, Any] | None = None,
            sowing: SowingBuilder | dict[str, Any] | None = None,
            **kwargs: Any,
        ) -> AutomaticSowingBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[AutomaticSowingReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[AutomaticSowingReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[AutomaticSowingBuilder]: ...
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
        ) -> AutomaticSowingReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AutomaticSowingReader: ...

    type AutomaticSowingReader = _AutomaticSowingStructModule.Reader
    type AutomaticSowingBuilder = _AutomaticSowingStructModule.Builder
    AutomaticSowing: _AutomaticSowingStructModule
    class _HarvestStructModule(_StructModule):
        class _CropUsageEnumModule:
            greenManure: int
            biomassProduction: int

        CropUsage: _CropUsageEnumModule
        class _OptCarbonMgmtDataStructModule(_StructModule):
            class Reader(_DynamicStructReader):
                @property
                def optCarbonConservation(self) -> bool: ...
                @property
                def cropImpactOnHumusBalance(self) -> float: ...
                @property
                def cropUsage(self) -> ParamsHarvestCropUsageEnum: ...
                @property
                def residueHeq(self) -> float: ...
                @property
                def organicFertilizerHeq(self) -> float: ...
                @property
                def maxResidueRecoverFraction(self) -> float: ...
                @override
                def as_builder(
                    self,
                    num_first_segment_words: int | None = None,
                    allocate_seg_callable: Callable[[int], bytearray] | None = None,
                ) -> OptCarbonMgmtDataBuilder: ...

            class Builder(_DynamicStructBuilder):
                @property
                def optCarbonConservation(self) -> bool: ...
                @optCarbonConservation.setter
                def optCarbonConservation(self, value: bool) -> None: ...
                @property
                def cropImpactOnHumusBalance(self) -> float: ...
                @cropImpactOnHumusBalance.setter
                def cropImpactOnHumusBalance(self, value: float) -> None: ...
                @property
                def cropUsage(self) -> ParamsHarvestCropUsageEnum: ...
                @cropUsage.setter
                def cropUsage(self, value: ParamsHarvestCropUsageEnum) -> None: ...
                @property
                def residueHeq(self) -> float: ...
                @residueHeq.setter
                def residueHeq(self, value: float) -> None: ...
                @property
                def organicFertilizerHeq(self) -> float: ...
                @organicFertilizerHeq.setter
                def organicFertilizerHeq(self, value: float) -> None: ...
                @property
                def maxResidueRecoverFraction(self) -> float: ...
                @maxResidueRecoverFraction.setter
                def maxResidueRecoverFraction(self, value: float) -> None: ...
                @override
                def as_reader(self) -> OptCarbonMgmtDataReader: ...

            @override
            def new_message(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
                optCarbonConservation: bool | None = None,
                cropImpactOnHumusBalance: float | None = None,
                cropUsage: ParamsHarvestCropUsageEnum | None = None,
                residueHeq: float | None = None,
                organicFertilizerHeq: float | None = None,
                maxResidueRecoverFraction: float | None = None,
                **kwargs: Any,
            ) -> OptCarbonMgmtDataBuilder: ...
            @override
            @overload
            def from_bytes(
                self,
                buf: bytes,
                traversal_limit_in_words: int | None = None,
                nesting_limit: int | None = None,
            ) -> AbstractContextManager[OptCarbonMgmtDataReader]: ...
            @overload
            def from_bytes(
                self,
                buf: bytes,
                traversal_limit_in_words: int | None = None,
                nesting_limit: int | None = None,
                *,
                builder: Literal[False],
            ) -> AbstractContextManager[OptCarbonMgmtDataReader]: ...
            @overload
            def from_bytes(
                self,
                buf: bytes,
                traversal_limit_in_words: int | None = None,
                nesting_limit: int | None = None,
                *,
                builder: Literal[True],
            ) -> AbstractContextManager[OptCarbonMgmtDataBuilder]: ...
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
            ) -> OptCarbonMgmtDataReader: ...
            @override
            def read_packed(
                self,
                file: IO[str] | IO[bytes],
                traversal_limit_in_words: int | None = None,
                nesting_limit: int | None = None,
            ) -> OptCarbonMgmtDataReader: ...

        type OptCarbonMgmtDataReader = _OptCarbonMgmtDataStructModule.Reader
        type OptCarbonMgmtDataBuilder = _OptCarbonMgmtDataStructModule.Builder
        OptCarbonMgmtData: _OptCarbonMgmtDataStructModule
        class Reader(_DynamicStructReader):
            @property
            def exported(self) -> bool: ...
            @property
            def optCarbMgmtData(self) -> OptCarbonMgmtDataReader: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> HarvestBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def exported(self) -> bool: ...
            @exported.setter
            def exported(self, value: bool) -> None: ...
            @property
            def optCarbMgmtData(self) -> OptCarbonMgmtDataBuilder: ...
            @optCarbMgmtData.setter
            def optCarbMgmtData(
                self,
                value: OptCarbonMgmtDataBuilder
                | OptCarbonMgmtDataReader
                | dict[str, Any],
            ) -> None: ...
            @override
            def init(
                self, field: Literal["optCarbMgmtData"], size: int | None = None
            ) -> OptCarbonMgmtDataBuilder: ...
            @override
            def as_reader(self) -> HarvestReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            exported: bool | None = None,
            optCarbMgmtData: OptCarbonMgmtDataBuilder | dict[str, Any] | None = None,
            **kwargs: Any,
        ) -> HarvestBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[HarvestReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[HarvestReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[HarvestBuilder]: ...
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
        ) -> HarvestReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> HarvestReader: ...

    type HarvestReader = _HarvestStructModule.Reader
    type HarvestBuilder = _HarvestStructModule.Builder
    Harvest: _HarvestStructModule
    class _AutomaticHarvestStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def minPercentASW(self) -> float: ...
            @property
            def maxPercentASW(self) -> float: ...
            @property
            def max3dayPrecipSum(self) -> float: ...
            @property
            def maxCurrentDayPrecipSum(self) -> float: ...
            @property
            def harvestTime(self) -> EventPhenoStageEnum: ...
            @property
            def harvest(self) -> HarvestReader: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> AutomaticHarvestBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def minPercentASW(self) -> float: ...
            @minPercentASW.setter
            def minPercentASW(self, value: float) -> None: ...
            @property
            def maxPercentASW(self) -> float: ...
            @maxPercentASW.setter
            def maxPercentASW(self, value: float) -> None: ...
            @property
            def max3dayPrecipSum(self) -> float: ...
            @max3dayPrecipSum.setter
            def max3dayPrecipSum(self, value: float) -> None: ...
            @property
            def maxCurrentDayPrecipSum(self) -> float: ...
            @maxCurrentDayPrecipSum.setter
            def maxCurrentDayPrecipSum(self, value: float) -> None: ...
            @property
            def harvestTime(self) -> EventPhenoStageEnum: ...
            @harvestTime.setter
            def harvestTime(self, value: EventPhenoStageEnum) -> None: ...
            @property
            def harvest(self) -> HarvestBuilder: ...
            @harvest.setter
            def harvest(
                self, value: HarvestBuilder | HarvestReader | dict[str, Any]
            ) -> None: ...
            @override
            def init(
                self, field: Literal["harvest"], size: int | None = None
            ) -> HarvestBuilder: ...
            @override
            def as_reader(self) -> AutomaticHarvestReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            minPercentASW: float | None = None,
            maxPercentASW: float | None = None,
            max3dayPrecipSum: float | None = None,
            maxCurrentDayPrecipSum: float | None = None,
            harvestTime: EventPhenoStageEnum | None = None,
            harvest: HarvestBuilder | dict[str, Any] | None = None,
            **kwargs: Any,
        ) -> AutomaticHarvestBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[AutomaticHarvestReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[AutomaticHarvestReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[AutomaticHarvestBuilder]: ...
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
        ) -> AutomaticHarvestReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AutomaticHarvestReader: ...

    type AutomaticHarvestReader = _AutomaticHarvestStructModule.Reader
    type AutomaticHarvestBuilder = _AutomaticHarvestStructModule.Builder
    AutomaticHarvest: _AutomaticHarvestStructModule
    class _CuttingStructModule(_StructModule):
        class _CLEnumModule:
            cut: int
            left: int

        CL: _CLEnumModule
        class _UnitEnumModule:
            percentage: int
            biomass: int
            lai: int

        Unit: _UnitEnumModule
        class _SpecStructModule(_StructModule):
            class Reader(_DynamicStructReader):
                @property
                def organ(self) -> PlantOrganEnum: ...
                @property
                def value(self) -> float: ...
                @property
                def unit(self) -> ParamsCuttingUnitEnum: ...
                @property
                def cutOrLeft(self) -> ParamsCuttingCLEnum: ...
                @property
                def exportPercentage(self) -> float: ...
                @override
                def as_builder(
                    self,
                    num_first_segment_words: int | None = None,
                    allocate_seg_callable: Callable[[int], bytearray] | None = None,
                ) -> SpecBuilder: ...

            class Builder(_DynamicStructBuilder):
                @property
                def organ(self) -> PlantOrganEnum: ...
                @organ.setter
                def organ(self, value: PlantOrganEnum) -> None: ...
                @property
                def value(self) -> float: ...
                @value.setter
                def value(self, value: float) -> None: ...
                @property
                def unit(self) -> ParamsCuttingUnitEnum: ...
                @unit.setter
                def unit(self, value: ParamsCuttingUnitEnum) -> None: ...
                @property
                def cutOrLeft(self) -> ParamsCuttingCLEnum: ...
                @cutOrLeft.setter
                def cutOrLeft(self, value: ParamsCuttingCLEnum) -> None: ...
                @property
                def exportPercentage(self) -> float: ...
                @exportPercentage.setter
                def exportPercentage(self, value: float) -> None: ...
                @override
                def as_reader(self) -> SpecReader: ...

            @override
            def new_message(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
                organ: PlantOrganEnum | None = None,
                value: float | None = None,
                unit: ParamsCuttingUnitEnum | None = None,
                cutOrLeft: ParamsCuttingCLEnum | None = None,
                exportPercentage: float | None = None,
                **kwargs: Any,
            ) -> SpecBuilder: ...
            @override
            @overload
            def from_bytes(
                self,
                buf: bytes,
                traversal_limit_in_words: int | None = None,
                nesting_limit: int | None = None,
            ) -> AbstractContextManager[SpecReader]: ...
            @overload
            def from_bytes(
                self,
                buf: bytes,
                traversal_limit_in_words: int | None = None,
                nesting_limit: int | None = None,
                *,
                builder: Literal[False],
            ) -> AbstractContextManager[SpecReader]: ...
            @overload
            def from_bytes(
                self,
                buf: bytes,
                traversal_limit_in_words: int | None = None,
                nesting_limit: int | None = None,
                *,
                builder: Literal[True],
            ) -> AbstractContextManager[SpecBuilder]: ...
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
            ) -> SpecReader: ...
            @override
            def read_packed(
                self,
                file: IO[str] | IO[bytes],
                traversal_limit_in_words: int | None = None,
                nesting_limit: int | None = None,
            ) -> SpecReader: ...

        type SpecReader = _SpecStructModule.Reader
        type SpecBuilder = _SpecStructModule.Builder
        Spec: _SpecStructModule
        class Reader(_DynamicStructReader):
            @property
            def cuttingSpec(self) -> SpecListReader: ...
            @property
            def cutMaxAssimilationRatePercentage(self) -> float: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> CuttingBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def cuttingSpec(self) -> SpecListBuilder: ...
            @cuttingSpec.setter
            def cuttingSpec(
                self, value: SpecListBuilder | SpecListReader | dict[str, Any]
            ) -> None: ...
            @property
            def cutMaxAssimilationRatePercentage(self) -> float: ...
            @cutMaxAssimilationRatePercentage.setter
            def cutMaxAssimilationRatePercentage(self, value: float) -> None: ...
            @override
            def init(
                self, field: Literal["cuttingSpec"], size: int | None = None
            ) -> SpecListBuilder: ...
            @override
            def as_reader(self) -> CuttingReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            cuttingSpec: SpecListBuilder | dict[str, Any] | None = None,
            cutMaxAssimilationRatePercentage: float | None = None,
            **kwargs: Any,
        ) -> CuttingBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[CuttingReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[CuttingReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[CuttingBuilder]: ...
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
        ) -> CuttingReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> CuttingReader: ...

    type CuttingReader = _CuttingStructModule.Reader
    type CuttingBuilder = _CuttingStructModule.Builder
    Cutting: _CuttingStructModule
    class _MineralFertilizationStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def fertilizer(self) -> _FertilizerInterfaceModule.FertilizerClient: ...
            @property
            def amount(self) -> float: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> MineralFertilizationBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def fertilizer(self) -> _FertilizerInterfaceModule.FertilizerClient: ...
            @fertilizer.setter
            def fertilizer(
                self,
                value: _FertilizerInterfaceModule.FertilizerClient
                | _FertilizerInterfaceModule.Server,
            ) -> None: ...
            @property
            def amount(self) -> float: ...
            @amount.setter
            def amount(self, value: float) -> None: ...
            @override
            def as_reader(self) -> MineralFertilizationReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            fertilizer: _FertilizerInterfaceModule.FertilizerClient
            | _FertilizerInterfaceModule.Server
            | None = None,
            amount: float | None = None,
            **kwargs: Any,
        ) -> MineralFertilizationBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[MineralFertilizationReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[MineralFertilizationReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[MineralFertilizationBuilder]: ...
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
        ) -> MineralFertilizationReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> MineralFertilizationReader: ...

    type MineralFertilizationReader = _MineralFertilizationStructModule.Reader
    type MineralFertilizationBuilder = _MineralFertilizationStructModule.Builder
    MineralFertilization: _MineralFertilizationStructModule
    class _NDemandFertilizationStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def nDemand(self) -> float: ...
            @property
            def fertilizer(self) -> _FertilizerInterfaceModule.FertilizerClient: ...
            @property
            def depth(self) -> float: ...
            @property
            def stage(self) -> int: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> NDemandFertilizationBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def nDemand(self) -> float: ...
            @nDemand.setter
            def nDemand(self, value: float) -> None: ...
            @property
            def fertilizer(self) -> _FertilizerInterfaceModule.FertilizerClient: ...
            @fertilizer.setter
            def fertilizer(
                self,
                value: _FertilizerInterfaceModule.FertilizerClient
                | _FertilizerInterfaceModule.Server,
            ) -> None: ...
            @property
            def depth(self) -> float: ...
            @depth.setter
            def depth(self, value: float) -> None: ...
            @property
            def stage(self) -> int: ...
            @stage.setter
            def stage(self, value: int) -> None: ...
            @override
            def as_reader(self) -> NDemandFertilizationReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            nDemand: float | None = None,
            fertilizer: _FertilizerInterfaceModule.FertilizerClient
            | _FertilizerInterfaceModule.Server
            | None = None,
            depth: float | None = None,
            stage: int | None = None,
            **kwargs: Any,
        ) -> NDemandFertilizationBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[NDemandFertilizationReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[NDemandFertilizationReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[NDemandFertilizationBuilder]: ...
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
        ) -> NDemandFertilizationReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> NDemandFertilizationReader: ...

    type NDemandFertilizationReader = _NDemandFertilizationStructModule.Reader
    type NDemandFertilizationBuilder = _NDemandFertilizationStructModule.Builder
    NDemandFertilization: _NDemandFertilizationStructModule
    class _OrganicFertilizationStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def fertilizer(self) -> _FertilizerInterfaceModule.FertilizerClient: ...
            @property
            def amount(self) -> float: ...
            @property
            def incorporation(self) -> bool: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> OrganicFertilizationBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def fertilizer(self) -> _FertilizerInterfaceModule.FertilizerClient: ...
            @fertilizer.setter
            def fertilizer(
                self,
                value: _FertilizerInterfaceModule.FertilizerClient
                | _FertilizerInterfaceModule.Server,
            ) -> None: ...
            @property
            def amount(self) -> float: ...
            @amount.setter
            def amount(self, value: float) -> None: ...
            @property
            def incorporation(self) -> bool: ...
            @incorporation.setter
            def incorporation(self, value: bool) -> None: ...
            @override
            def as_reader(self) -> OrganicFertilizationReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            fertilizer: _FertilizerInterfaceModule.FertilizerClient
            | _FertilizerInterfaceModule.Server
            | None = None,
            amount: float | None = None,
            incorporation: bool | None = None,
            **kwargs: Any,
        ) -> OrganicFertilizationBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[OrganicFertilizationReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[OrganicFertilizationReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[OrganicFertilizationBuilder]: ...
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
        ) -> OrganicFertilizationReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> OrganicFertilizationReader: ...

    type OrganicFertilizationReader = _OrganicFertilizationStructModule.Reader
    type OrganicFertilizationBuilder = _OrganicFertilizationStructModule.Builder
    OrganicFertilization: _OrganicFertilizationStructModule
    class _TillageStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def depth(self) -> float: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> TillageBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def depth(self) -> float: ...
            @depth.setter
            def depth(self, value: float) -> None: ...
            @override
            def as_reader(self) -> TillageReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            depth: float | None = None,
            **kwargs: Any,
        ) -> TillageBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[TillageReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[TillageReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[TillageBuilder]: ...
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
        ) -> TillageReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> TillageReader: ...

    type TillageReader = _TillageStructModule.Reader
    type TillageBuilder = _TillageStructModule.Builder
    Tillage: _TillageStructModule
    class _IrrigationStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def amount(self) -> float: ...
            @property
            def nutrientConcentrations(self) -> NutrientListReader: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> IrrigationBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def amount(self) -> float: ...
            @amount.setter
            def amount(self, value: float) -> None: ...
            @property
            def nutrientConcentrations(self) -> NutrientListBuilder: ...
            @nutrientConcentrations.setter
            def nutrientConcentrations(
                self, value: NutrientListBuilder | NutrientListReader | dict[str, Any]
            ) -> None: ...
            @override
            def init(
                self, field: Literal["nutrientConcentrations"], size: int | None = None
            ) -> NutrientListBuilder: ...
            @override
            def as_reader(self) -> IrrigationReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            amount: float | None = None,
            nutrientConcentrations: NutrientListBuilder | dict[str, Any] | None = None,
            **kwargs: Any,
        ) -> IrrigationBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[IrrigationReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[IrrigationReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[IrrigationBuilder]: ...
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
        ) -> IrrigationReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> IrrigationReader: ...

    type IrrigationReader = _IrrigationStructModule.Reader
    type IrrigationBuilder = _IrrigationStructModule.Builder
    Irrigation: _IrrigationStructModule
    class Reader(_DynamicStructReader):
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> ParamsBuilder: ...

    class Builder(_DynamicStructBuilder):
        @override
        def as_reader(self) -> ParamsReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
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

Params: _ParamsStructModule

class _FertilizerServiceInterfaceModule(_RegistryInterfaceModule):
    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _FertilizerServiceInterfaceModule.FertilizerServiceClient: ...
    class Server(_RegistryInterfaceModule.Server): ...
    class FertilizerServiceClient(_RegistryInterfaceModule.RegistryClient): ...

FertilizerService: _FertilizerServiceInterfaceModule

class _ServiceInterfaceModule(_IdentifiableInterfaceModule):
    class ManagementatRequest(Protocol):
        lat: float
        lon: float
        def send(self) -> _ServiceInterfaceModule.ServiceClient.ManagementatResult: ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _ServiceInterfaceModule.ServiceClient: ...
    class Server(_IdentifiableInterfaceModule.Server):
        class ManagementatResult(_DynamicStructBuilder):
            @property
            def mgmt(self) -> EventListBuilder: ...
            @mgmt.setter
            def mgmt(
                self, value: EventListBuilder | EventListReader | Sequence[Any]
            ) -> None: ...
            @overload
            def init(
                self, field: Literal["mgmt"], size: int | None = None
            ) -> EventListBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...

        class ManagementatResultTuple(NamedTuple):
            mgmt: EventListBuilder | EventListReader

        class ManagementatParams(Protocol):
            lat: float
            lon: float

        class ManagementatCallContext(Protocol):
            params: _ServiceInterfaceModule.Server.ManagementatParams
            @property
            def results(self) -> _ServiceInterfaceModule.Server.ManagementatResult: ...

        def managementAt(
            self,
            lat: float,
            lon: float,
            _context: _ServiceInterfaceModule.Server.ManagementatCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            Sequence[EventBuilder | EventReader]
            | _ServiceInterfaceModule.Server.ManagementatResultTuple
            | None
        ]: ...
        def managementAt_context(
            self, context: _ServiceInterfaceModule.Server.ManagementatCallContext
        ) -> Awaitable[None]: ...

    class ServiceClient(_IdentifiableInterfaceModule.IdentifiableClient):
        class ManagementatResult(Awaitable[ManagementatResult], Protocol):
            mgmt: EventListReader

        def managementAt(
            self, lat: float | None = None, lon: float | None = None
        ) -> _ServiceInterfaceModule.ServiceClient.ManagementatResult: ...
        def managementAt_request(
            self, lat: float | None = None, lon: float | None = None
        ) -> _ServiceInterfaceModule.ManagementatRequest: ...

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

Service: _ServiceInterfaceModule

# Top-level type aliases for use in type annotations
type AutomaticHarvestBuilder = _ParamsStructModule._AutomaticHarvestStructModule.Builder
type AutomaticHarvestReader = _ParamsStructModule._AutomaticHarvestStructModule.Reader
type AutomaticSowingBuilder = _ParamsStructModule._AutomaticSowingStructModule.Builder
type AutomaticSowingReader = _ParamsStructModule._AutomaticSowingStructModule.Reader
type AvgSoilTempBuilder = (
    _ParamsStructModule._AutomaticSowingStructModule._AvgSoilTempStructModule.Builder
)
type AvgSoilTempReader = (
    _ParamsStructModule._AutomaticSowingStructModule._AvgSoilTempStructModule.Reader
)
type CuttingBuilder = _ParamsStructModule._CuttingStructModule.Builder
type CuttingReader = _ParamsStructModule._CuttingStructModule.Reader
type EventAfterBuilder = _EventStructModule._EventAfterStructModule.Builder
type EventAfterReader = _EventStructModule._EventAfterStructModule.Reader
type EventAtBuilder = _EventStructModule._EventAtStructModule.Builder
type EventAtReader = _EventStructModule._EventAtStructModule.Reader
type EventBetweenBuilder = _EventStructModule._EventBetweenStructModule.Builder
type EventBetweenReader = _EventStructModule._EventBetweenStructModule.Reader
type EventBuilder = _EventStructModule.Builder
type EventExternalTypeEnum = (
    int
    | Literal[
        "sowing",
        "automaticSowing",
        "harvest",
        "automaticHarvest",
        "irrigation",
        "tillage",
        "organicFertilization",
        "mineralFertilization",
        "nDemandFertilization",
        "cutting",
    ]
)
type EventListBuilder = _EventList.Builder
type EventListReader = _EventList.Reader
type EventPhenoStageEnum = (
    int | Literal["emergence", "flowering", "anthesis", "maturity"]
)
type EventReader = _EventStructModule.Reader
type EventTypeEnum = (
    int
    | Literal[
        "sowing",
        "automaticSowing",
        "harvest",
        "automaticHarvest",
        "irrigation",
        "tillage",
        "organicFertilization",
        "mineralFertilization",
        "nDemandFertilization",
        "cutting",
        "setValue",
        "saveState",
    ]
)
type FertilizerClient = _FertilizerInterfaceModule.FertilizerClient
type FertilizerServer = _FertilizerInterfaceModule.Server
type FertilizerServiceClient = _FertilizerServiceInterfaceModule.FertilizerServiceClient
type FertilizerServiceServer = _FertilizerServiceInterfaceModule.Server
type HarvestBuilder = _ParamsStructModule._HarvestStructModule.Builder
type HarvestReader = _ParamsStructModule._HarvestStructModule.Reader
type IrrigationBuilder = _ParamsStructModule._IrrigationStructModule.Builder
type IrrigationReader = _ParamsStructModule._IrrigationStructModule.Reader
type ManagementatResult = _ServiceInterfaceModule.ServiceClient.ManagementatResult
type MineralFertilizationBuilder = (
    _ParamsStructModule._MineralFertilizationStructModule.Builder
)
type MineralFertilizationReader = (
    _ParamsStructModule._MineralFertilizationStructModule.Reader
)
type NDemandFertilizationBuilder = (
    _ParamsStructModule._NDemandFertilizationStructModule.Builder
)
type NDemandFertilizationReader = (
    _ParamsStructModule._NDemandFertilizationStructModule.Reader
)
type NutrientBuilder = _NutrientStructModule.Builder
type NutrientListBuilder = _NutrientList.Builder
type NutrientListReader = _NutrientList.Reader
type NutrientNameEnum = (
    int
    | Literal[
        "urea",
        "ammonia",
        "nitrate",
        "phosphorus",
        "potassium",
        "sulfate",
        "organicC",
        "organicN",
        "organicP",
        "organicNFast",
        "organicNSlow",
    ]
)
type NutrientReader = _NutrientStructModule.Reader
type NutrientUnitEnum = int | Literal["none", "fraction", "percent"]
type NutrientsResult = _FertilizerInterfaceModule.FertilizerClient.NutrientsResult
type OptCarbonMgmtDataBuilder = (
    _ParamsStructModule._HarvestStructModule._OptCarbonMgmtDataStructModule.Builder
)
type OptCarbonMgmtDataReader = (
    _ParamsStructModule._HarvestStructModule._OptCarbonMgmtDataStructModule.Reader
)
type OrganicFertilizationBuilder = (
    _ParamsStructModule._OrganicFertilizationStructModule.Builder
)
type OrganicFertilizationReader = (
    _ParamsStructModule._OrganicFertilizationStructModule.Reader
)
type ParametersResult = _FertilizerInterfaceModule.FertilizerClient.ParametersResult
type ParamsBuilder = _ParamsStructModule.Builder
type ParamsCuttingCLEnum = int | Literal["cut", "left"]
type ParamsCuttingUnitEnum = int | Literal["percentage", "biomass", "lai"]
type ParamsHarvestCropUsageEnum = int | Literal["greenManure", "biomassProduction"]
type ParamsReader = _ParamsStructModule.Reader
type PlantOrganEnum = int | Literal["root", "leaf", "shoot", "fruit", "strukt", "sugar"]
type ServiceClient = _ServiceInterfaceModule.ServiceClient
type ServiceServer = _ServiceInterfaceModule.Server
type SowingBuilder = _ParamsStructModule._SowingStructModule.Builder
type SowingReader = _ParamsStructModule._SowingStructModule.Reader
type SpecBuilder = _ParamsStructModule._CuttingStructModule._SpecStructModule.Builder
type SpecListBuilder = _SpecList.Builder
type SpecListReader = _SpecList.Reader
type SpecReader = _ParamsStructModule._CuttingStructModule._SpecStructModule.Reader
type TillageBuilder = _ParamsStructModule._TillageStructModule.Builder
type TillageReader = _ParamsStructModule._TillageStructModule.Reader
type TypeBuilder = _EventStructModule._TypeStructModule.Builder
type TypeReader = _EventStructModule._TypeStructModule.Reader
