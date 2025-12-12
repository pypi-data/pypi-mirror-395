"""This is an automatically generated stub for `soil_params.capnp`."""

from __future__ import annotations
from capnp.lib.capnp import (
    _DynamicStructBuilder,
    _DynamicStructReader,
    _DynamicListBuilder,
    _DynamicListReader,
    _StructModule,
)
from contextlib import AbstractContextManager
from collections.abc import Iterator, Callable
from typing import Literal, overload, override, Any, IO

class _DataList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> DataReader: ...
        @override
        def __iter__(self) -> Iterator[DataReader]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> DataBuilder: ...
        @override
        def __setitem__(
            self, key: int, value: DataReader | DataBuilder | dict[str, Any]
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[DataBuilder]: ...
        @override
        def init(self, index: int, size: int | None = None) -> DataBuilder: ...

class _SoilCharacteristicDataStructModule(_StructModule):
    class _DataStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def soilType(self) -> str: ...
            @property
            def soilRawDensity(self) -> int: ...
            @property
            def airCapacity(self) -> int: ...
            @property
            def fieldCapacity(self) -> int: ...
            @property
            def nFieldCapacity(self) -> int: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> DataBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def soilType(self) -> str: ...
            @soilType.setter
            def soilType(self, value: str) -> None: ...
            @property
            def soilRawDensity(self) -> int: ...
            @soilRawDensity.setter
            def soilRawDensity(self, value: int) -> None: ...
            @property
            def airCapacity(self) -> int: ...
            @airCapacity.setter
            def airCapacity(self, value: int) -> None: ...
            @property
            def fieldCapacity(self) -> int: ...
            @fieldCapacity.setter
            def fieldCapacity(self, value: int) -> None: ...
            @property
            def nFieldCapacity(self) -> int: ...
            @nFieldCapacity.setter
            def nFieldCapacity(self, value: int) -> None: ...
            @override
            def as_reader(self) -> DataReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            soilType: str | None = None,
            soilRawDensity: int | None = None,
            airCapacity: int | None = None,
            fieldCapacity: int | None = None,
            nFieldCapacity: int | None = None,
            **kwargs: Any,
        ) -> DataBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[DataReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[DataReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[DataBuilder]: ...
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
        ) -> DataReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> DataReader: ...

    type DataReader = _DataStructModule.Reader
    type DataBuilder = _DataStructModule.Builder
    Data: _DataStructModule
    class Reader(_DynamicStructReader):
        @property
        def list(self) -> DataListReader: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> SoilCharacteristicDataBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def list(self) -> DataListBuilder: ...
        @list.setter
        def list(
            self, value: DataListBuilder | DataListReader | dict[str, Any]
        ) -> None: ...
        @override
        def init(
            self, field: Literal["list"], size: int | None = None
        ) -> DataListBuilder: ...
        @override
        def as_reader(self) -> SoilCharacteristicDataReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        list: DataListBuilder | dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> SoilCharacteristicDataBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[SoilCharacteristicDataReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[SoilCharacteristicDataReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[SoilCharacteristicDataBuilder]: ...
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
    ) -> SoilCharacteristicDataReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> SoilCharacteristicDataReader: ...

SoilCharacteristicData: _SoilCharacteristicDataStructModule

class _SoilCharacteristicModifierStructModule(_StructModule):
    class _DataStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def soilType(self) -> str: ...
            @property
            def organicMatter(self) -> float: ...
            @property
            def airCapacity(self) -> int: ...
            @property
            def fieldCapacity(self) -> int: ...
            @property
            def nFieldCapacity(self) -> int: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> DataBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def soilType(self) -> str: ...
            @soilType.setter
            def soilType(self, value: str) -> None: ...
            @property
            def organicMatter(self) -> float: ...
            @organicMatter.setter
            def organicMatter(self, value: float) -> None: ...
            @property
            def airCapacity(self) -> int: ...
            @airCapacity.setter
            def airCapacity(self, value: int) -> None: ...
            @property
            def fieldCapacity(self) -> int: ...
            @fieldCapacity.setter
            def fieldCapacity(self, value: int) -> None: ...
            @property
            def nFieldCapacity(self) -> int: ...
            @nFieldCapacity.setter
            def nFieldCapacity(self, value: int) -> None: ...
            @override
            def as_reader(self) -> DataReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            soilType: str | None = None,
            organicMatter: float | None = None,
            airCapacity: int | None = None,
            fieldCapacity: int | None = None,
            nFieldCapacity: int | None = None,
            **kwargs: Any,
        ) -> DataBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[DataReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[DataReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[DataBuilder]: ...
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
        ) -> DataReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> DataReader: ...

    type DataReader = _DataStructModule.Reader
    type DataBuilder = _DataStructModule.Builder
    Data: _DataStructModule
    class Reader(_DynamicStructReader):
        @property
        def list(self) -> DataListReader: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> SoilCharacteristicModifierBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def list(self) -> DataListBuilder: ...
        @list.setter
        def list(
            self, value: DataListBuilder | DataListReader | dict[str, Any]
        ) -> None: ...
        @override
        def init(
            self, field: Literal["list"], size: int | None = None
        ) -> DataListBuilder: ...
        @override
        def as_reader(self) -> SoilCharacteristicModifierReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        list: DataListBuilder | dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> SoilCharacteristicModifierBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[SoilCharacteristicModifierReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[SoilCharacteristicModifierReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[SoilCharacteristicModifierBuilder]: ...
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
    ) -> SoilCharacteristicModifierReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> SoilCharacteristicModifierReader: ...

SoilCharacteristicModifier: _SoilCharacteristicModifierStructModule

class _CapillaryRiseRateStructModule(_StructModule):
    class _DataStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def soilType(self) -> str: ...
            @property
            def distance(self) -> int: ...
            @property
            def rate(self) -> float: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> DataBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def soilType(self) -> str: ...
            @soilType.setter
            def soilType(self, value: str) -> None: ...
            @property
            def distance(self) -> int: ...
            @distance.setter
            def distance(self, value: int) -> None: ...
            @property
            def rate(self) -> float: ...
            @rate.setter
            def rate(self, value: float) -> None: ...
            @override
            def as_reader(self) -> DataReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            soilType: str | None = None,
            distance: int | None = None,
            rate: float | None = None,
            **kwargs: Any,
        ) -> DataBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[DataReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[DataReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[DataBuilder]: ...
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
        ) -> DataReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> DataReader: ...

    type DataReader = _DataStructModule.Reader
    type DataBuilder = _DataStructModule.Builder
    Data: _DataStructModule
    class Reader(_DynamicStructReader):
        @property
        def list(self) -> DataListReader: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> CapillaryRiseRateBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def list(self) -> DataListBuilder: ...
        @list.setter
        def list(
            self, value: DataListBuilder | DataListReader | dict[str, Any]
        ) -> None: ...
        @override
        def init(
            self, field: Literal["list"], size: int | None = None
        ) -> DataListBuilder: ...
        @override
        def as_reader(self) -> CapillaryRiseRateReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        list: DataListBuilder | dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> CapillaryRiseRateBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[CapillaryRiseRateReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[CapillaryRiseRateReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[CapillaryRiseRateBuilder]: ...
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
    ) -> CapillaryRiseRateReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> CapillaryRiseRateReader: ...

CapillaryRiseRate: _CapillaryRiseRateStructModule

# Top-level type aliases for use in type annotations
type CapillaryRiseRateBuilder = _CapillaryRiseRateStructModule.Builder
type CapillaryRiseRateReader = _CapillaryRiseRateStructModule.Reader
type DataBuilder = _CapillaryRiseRateStructModule._DataStructModule.Builder
type DataListBuilder = _DataList.Builder
type DataListReader = _DataList.Reader
type DataReader = _CapillaryRiseRateStructModule._DataStructModule.Reader
type SoilCharacteristicDataBuilder = _SoilCharacteristicDataStructModule.Builder
type SoilCharacteristicDataReader = _SoilCharacteristicDataStructModule.Reader
type SoilCharacteristicModifierBuilder = _SoilCharacteristicModifierStructModule.Builder
type SoilCharacteristicModifierReader = _SoilCharacteristicModifierStructModule.Reader
