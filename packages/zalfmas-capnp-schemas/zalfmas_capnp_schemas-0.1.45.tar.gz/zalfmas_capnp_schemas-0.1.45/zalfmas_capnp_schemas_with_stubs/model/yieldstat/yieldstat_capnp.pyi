"""This is an automatically generated stub for `yieldstat.capnp`."""

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

class _ResultIdEnumModule:
    primaryYield: int
    dryMatter: int
    carbonInAboveGroundBiomass: int
    sumFertilizer: int
    sumIrrigation: int
    primaryYieldCU: int

class _RestInputStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def useDevTrend(self) -> bool: ...
        @property
        def useCO2Increase(self) -> bool: ...
        @property
        def dgm(self) -> float: ...
        @property
        def hft(self) -> int: ...
        @property
        def nft(self) -> int: ...
        @property
        def sft(self) -> int: ...
        @property
        def slope(self) -> int: ...
        @property
        def steino(self) -> int: ...
        @property
        def az(self) -> int: ...
        @property
        def klz(self) -> int: ...
        @property
        def stt(self) -> int: ...
        @property
        def germanFederalStates(self) -> int: ...
        @property
        def getDryYearWaterNeed(self) -> bool: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> RestInputBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def useDevTrend(self) -> bool: ...
        @useDevTrend.setter
        def useDevTrend(self, value: bool) -> None: ...
        @property
        def useCO2Increase(self) -> bool: ...
        @useCO2Increase.setter
        def useCO2Increase(self, value: bool) -> None: ...
        @property
        def dgm(self) -> float: ...
        @dgm.setter
        def dgm(self, value: float) -> None: ...
        @property
        def hft(self) -> int: ...
        @hft.setter
        def hft(self, value: int) -> None: ...
        @property
        def nft(self) -> int: ...
        @nft.setter
        def nft(self, value: int) -> None: ...
        @property
        def sft(self) -> int: ...
        @sft.setter
        def sft(self, value: int) -> None: ...
        @property
        def slope(self) -> int: ...
        @slope.setter
        def slope(self, value: int) -> None: ...
        @property
        def steino(self) -> int: ...
        @steino.setter
        def steino(self, value: int) -> None: ...
        @property
        def az(self) -> int: ...
        @az.setter
        def az(self, value: int) -> None: ...
        @property
        def klz(self) -> int: ...
        @klz.setter
        def klz(self, value: int) -> None: ...
        @property
        def stt(self) -> int: ...
        @stt.setter
        def stt(self, value: int) -> None: ...
        @property
        def germanFederalStates(self) -> int: ...
        @germanFederalStates.setter
        def germanFederalStates(self, value: int) -> None: ...
        @property
        def getDryYearWaterNeed(self) -> bool: ...
        @getDryYearWaterNeed.setter
        def getDryYearWaterNeed(self, value: bool) -> None: ...
        @override
        def as_reader(self) -> RestInputReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        useDevTrend: bool | None = None,
        useCO2Increase: bool | None = None,
        dgm: float | None = None,
        hft: int | None = None,
        nft: int | None = None,
        sft: int | None = None,
        slope: int | None = None,
        steino: int | None = None,
        az: int | None = None,
        klz: int | None = None,
        stt: int | None = None,
        germanFederalStates: int | None = None,
        getDryYearWaterNeed: bool | None = None,
        **kwargs: Any,
    ) -> RestInputBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[RestInputReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[RestInputReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[RestInputBuilder]: ...
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
    ) -> RestInputReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> RestInputReader: ...

RestInput: _RestInputStructModule

class _ResultToValueList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> ResultToValueReader: ...
        @override
        def __iter__(self) -> Iterator[ResultToValueReader]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> ResultToValueBuilder: ...
        @override
        def __setitem__(
            self,
            key: int,
            value: ResultToValueReader | ResultToValueBuilder | dict[str, Any],
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[ResultToValueBuilder]: ...
        @override
        def init(self, index: int, size: int | None = None) -> ResultToValueBuilder: ...

class _ResultStructModule(_StructModule):
    class _ResultToValueStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def id(self) -> ResultIdEnum: ...
            @property
            def value(self) -> float: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> ResultToValueBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def id(self) -> ResultIdEnum: ...
            @id.setter
            def id(self, value: ResultIdEnum) -> None: ...
            @property
            def value(self) -> float: ...
            @value.setter
            def value(self, value: float) -> None: ...
            @override
            def as_reader(self) -> ResultToValueReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            id: ResultIdEnum | None = None,
            value: float | None = None,
            **kwargs: Any,
        ) -> ResultToValueBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[ResultToValueReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[ResultToValueReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[ResultToValueBuilder]: ...
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
        ) -> ResultToValueReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> ResultToValueReader: ...

    type ResultToValueReader = _ResultToValueStructModule.Reader
    type ResultToValueBuilder = _ResultToValueStructModule.Builder
    ResultToValue: _ResultToValueStructModule
    class Reader(_DynamicStructReader):
        @property
        def cultivar(self) -> str: ...
        @property
        def isNoData(self) -> bool: ...
        @property
        def values(self) -> ResultToValueListReader: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> ResultBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def cultivar(self) -> str: ...
        @cultivar.setter
        def cultivar(self, value: str) -> None: ...
        @property
        def isNoData(self) -> bool: ...
        @isNoData.setter
        def isNoData(self, value: bool) -> None: ...
        @property
        def values(self) -> ResultToValueListBuilder: ...
        @values.setter
        def values(
            self,
            value: ResultToValueListBuilder | ResultToValueListReader | dict[str, Any],
        ) -> None: ...
        @override
        def init(
            self, field: Literal["values"], size: int | None = None
        ) -> ResultToValueListBuilder: ...
        @override
        def as_reader(self) -> ResultReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        cultivar: str | None = None,
        isNoData: bool | None = None,
        values: ResultToValueListBuilder | dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> ResultBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[ResultReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[ResultReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[ResultBuilder]: ...
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
    ) -> ResultReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> ResultReader: ...

Result: _ResultStructModule

class _YearToResultList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> YearToResultReader: ...
        @override
        def __iter__(self) -> Iterator[YearToResultReader]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> YearToResultBuilder: ...
        @override
        def __setitem__(
            self,
            key: int,
            value: YearToResultReader | YearToResultBuilder | dict[str, Any],
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[YearToResultBuilder]: ...
        @override
        def init(self, index: int, size: int | None = None) -> YearToResultBuilder: ...

class _OutputStructModule(_StructModule):
    class _YearToResultStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def year(self) -> int: ...
            @property
            def result(self) -> ResultReader: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> YearToResultBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def year(self) -> int: ...
            @year.setter
            def year(self, value: int) -> None: ...
            @property
            def result(self) -> ResultBuilder: ...
            @result.setter
            def result(
                self, value: ResultBuilder | ResultReader | dict[str, Any]
            ) -> None: ...
            @override
            def init(
                self, field: Literal["result"], size: int | None = None
            ) -> ResultBuilder: ...
            @override
            def as_reader(self) -> YearToResultReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            year: int | None = None,
            result: ResultBuilder | dict[str, Any] | None = None,
            **kwargs: Any,
        ) -> YearToResultBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[YearToResultReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[YearToResultReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[YearToResultBuilder]: ...
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
        ) -> YearToResultReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> YearToResultReader: ...

    type YearToResultReader = _YearToResultStructModule.Reader
    type YearToResultBuilder = _YearToResultStructModule.Builder
    YearToResult: _YearToResultStructModule
    class Reader(_DynamicStructReader):
        @property
        def id(self) -> str: ...
        @property
        def runFailed(self) -> bool: ...
        @property
        def reason(self) -> str: ...
        @property
        def results(self) -> YearToResultListReader: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> OutputBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def id(self) -> str: ...
        @id.setter
        def id(self, value: str) -> None: ...
        @property
        def runFailed(self) -> bool: ...
        @runFailed.setter
        def runFailed(self, value: bool) -> None: ...
        @property
        def reason(self) -> str: ...
        @reason.setter
        def reason(self, value: str) -> None: ...
        @property
        def results(self) -> YearToResultListBuilder: ...
        @results.setter
        def results(
            self,
            value: YearToResultListBuilder | YearToResultListReader | dict[str, Any],
        ) -> None: ...
        @override
        def init(
            self, field: Literal["results"], size: int | None = None
        ) -> YearToResultListBuilder: ...
        @override
        def as_reader(self) -> OutputReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        id: str | None = None,
        runFailed: bool | None = None,
        reason: str | None = None,
        results: YearToResultListBuilder | dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> OutputBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[OutputReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[OutputReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[OutputBuilder]: ...
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
    ) -> OutputReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> OutputReader: ...

Output: _OutputStructModule

# Top-level type aliases for use in type annotations
type OutputBuilder = _OutputStructModule.Builder
type OutputReader = _OutputStructModule.Reader
type RestInputBuilder = _RestInputStructModule.Builder
type RestInputReader = _RestInputStructModule.Reader
type ResultBuilder = _ResultStructModule.Builder
type ResultIdEnum = (
    int
    | Literal[
        "primaryYield",
        "dryMatter",
        "carbonInAboveGroundBiomass",
        "sumFertilizer",
        "sumIrrigation",
        "primaryYieldCU",
    ]
)
type ResultReader = _ResultStructModule.Reader
type ResultToValueBuilder = _ResultStructModule._ResultToValueStructModule.Builder
type ResultToValueListBuilder = _ResultToValueList.Builder
type ResultToValueListReader = _ResultToValueList.Reader
type ResultToValueReader = _ResultStructModule._ResultToValueStructModule.Reader
type YearToResultBuilder = _OutputStructModule._YearToResultStructModule.Builder
type YearToResultListBuilder = _YearToResultList.Builder
type YearToResultListReader = _YearToResultList.Reader
type YearToResultReader = _OutputStructModule._YearToResultStructModule.Reader
