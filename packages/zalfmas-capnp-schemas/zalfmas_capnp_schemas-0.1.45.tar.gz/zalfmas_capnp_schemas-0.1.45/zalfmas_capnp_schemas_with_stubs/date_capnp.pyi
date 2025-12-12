"""This is an automatically generated stub for `date.capnp`."""

from __future__ import annotations
from capnp.lib.capnp import _DynamicStructBuilder, _DynamicStructReader, _StructModule
from contextlib import AbstractContextManager
from collections.abc import Callable
from typing import Literal, overload, override, Any, IO

class _DateStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def year(self) -> int: ...
        @property
        def month(self) -> int: ...
        @property
        def day(self) -> int: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> DateBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def year(self) -> int: ...
        @year.setter
        def year(self, value: int) -> None: ...
        @property
        def month(self) -> int: ...
        @month.setter
        def month(self, value: int) -> None: ...
        @property
        def day(self) -> int: ...
        @day.setter
        def day(self, value: int) -> None: ...
        @override
        def as_reader(self) -> DateReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        year: int | None = None,
        month: int | None = None,
        day: int | None = None,
        **kwargs: Any,
    ) -> DateBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[DateReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[DateReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[DateBuilder]: ...
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
    ) -> DateReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> DateReader: ...

Date: _DateStructModule

# Top-level type aliases for use in type annotations
type DateBuilder = _DateStructModule.Builder
type DateReader = _DateStructModule.Reader
