"""This is an automatically generated stub for `registry.capnp`."""

from __future__ import annotations
from capnp.lib.capnp import (
    _DynamicCapabilityClient,
    _DynamicCapabilityServer,
    _DynamicStructBuilder,
    _DynamicStructReader,
    _DynamicListBuilder,
    _DynamicListReader,
    _InterfaceModule,
    _StructModule,
)
from .common_capnp import _IdentifiableInterfaceModule, IdentifiableClient
from .common_capnp import IdInformationReader, IdInformationBuilder
from contextlib import AbstractContextManager
from .persistence_capnp import VatIdReader, VatIdBuilder
from .persistence_capnp import _RestorerInterfaceModule
from .persistence_capnp import SturdyRefReader, SturdyRefBuilder
from collections.abc import Iterator, Sequence, Awaitable, Callable
from typing import Literal, overload, override, Protocol, Any, IO, NamedTuple

class _AdminInterfaceModule(_IdentifiableInterfaceModule):
    class AddcategoryRequest(Protocol):
        category: IdInformationBuilder
        upsert: bool
        @overload
        def init(self, name: Literal["category"]) -> IdInformationBuilder: ...
        @overload
        def init(self, name: str, size: int = ...) -> Any: ...
        def send(self) -> _AdminInterfaceModule.AdminClient.AddcategoryResult: ...

    class RemovecategoryRequest(Protocol):
        categoryId: str
        moveObjectsToCategoryId: str
        def send(self) -> _AdminInterfaceModule.AdminClient.RemovecategoryResult: ...

    class MoveobjectsRequest(Protocol):
        objectIds: TextListBuilder | TextListReader | Sequence[Any]
        toCatId: str
        @overload
        def init(
            self, name: Literal["objectIds"], size: int = ...
        ) -> TextListBuilder: ...
        @overload
        def init(self, name: str, size: int = ...) -> Any: ...
        def send(self) -> _AdminInterfaceModule.AdminClient.MoveobjectsResult: ...

    class RemoveobjectsRequest(Protocol):
        objectIds: TextListBuilder | TextListReader | Sequence[Any]
        @overload
        def init(
            self, name: Literal["objectIds"], size: int = ...
        ) -> TextListBuilder: ...
        @overload
        def init(self, name: str, size: int = ...) -> Any: ...
        def send(self) -> _AdminInterfaceModule.AdminClient.RemoveobjectsResult: ...

    class RegistryRequest(Protocol):
        def send(self) -> _AdminInterfaceModule.AdminClient.RegistryResult: ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _AdminInterfaceModule.AdminClient: ...
    class Server(_IdentifiableInterfaceModule.Server):
        class AddcategoryResult(_DynamicStructBuilder):
            @property
            def success(self) -> bool: ...
            @success.setter
            def success(self, value: bool) -> None: ...

        class RemovecategoryResult(_DynamicStructBuilder):
            @property
            def removedObjects(self) -> IdentifiableClientListBuilder: ...
            @removedObjects.setter
            def removedObjects(
                self,
                value: IdentifiableClientListBuilder
                | IdentifiableClientListReader
                | Sequence[Any],
            ) -> None: ...
            @overload
            def init(
                self, field: Literal["removedObjects"], size: int | None = None
            ) -> IdentifiableClientListBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...

        class MoveobjectsResult(_DynamicStructBuilder):
            @property
            def movedObjectIds(self) -> TextListBuilder: ...
            @movedObjectIds.setter
            def movedObjectIds(
                self, value: TextListBuilder | TextListReader | Sequence[Any]
            ) -> None: ...
            @overload
            def init(
                self, field: Literal["movedObjectIds"], size: int | None = None
            ) -> TextListBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...

        class RemoveobjectsResult(_DynamicStructBuilder):
            @property
            def removedObjects(self) -> IdentifiableClientListBuilder: ...
            @removedObjects.setter
            def removedObjects(
                self,
                value: IdentifiableClientListBuilder
                | IdentifiableClientListReader
                | Sequence[Any],
            ) -> None: ...
            @overload
            def init(
                self, field: Literal["removedObjects"], size: int | None = None
            ) -> IdentifiableClientListBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...

        class RegistryResult(_DynamicStructBuilder):
            @property
            def registry(
                self,
            ) -> (
                _RegistryInterfaceModule.Server
                | _RegistryInterfaceModule.RegistryClient
            ): ...
            @registry.setter
            def registry(
                self,
                value: _RegistryInterfaceModule.Server
                | _RegistryInterfaceModule.RegistryClient,
            ) -> None: ...

        class AddcategoryResultTuple(NamedTuple):
            success: bool

        class RemovecategoryResultTuple(NamedTuple):
            removedObjects: IdentifiableClientListBuilder | IdentifiableClientListReader

        class MoveobjectsResultTuple(NamedTuple):
            movedObjectIds: TextListBuilder | TextListReader

        class RemoveobjectsResultTuple(NamedTuple):
            removedObjects: IdentifiableClientListBuilder | IdentifiableClientListReader

        class RegistryResultTuple(NamedTuple):
            registry: (
                _RegistryInterfaceModule.Server
                | _RegistryInterfaceModule.RegistryClient
            )

        class AddcategoryParams(Protocol):
            category: IdInformationReader
            upsert: bool

        class AddcategoryCallContext(Protocol):
            params: _AdminInterfaceModule.Server.AddcategoryParams
            @property
            def results(self) -> _AdminInterfaceModule.Server.AddcategoryResult: ...

        class RemovecategoryParams(Protocol):
            categoryId: str
            moveObjectsToCategoryId: str

        class RemovecategoryCallContext(Protocol):
            params: _AdminInterfaceModule.Server.RemovecategoryParams
            @property
            def results(self) -> _AdminInterfaceModule.Server.RemovecategoryResult: ...

        class MoveobjectsParams(Protocol):
            objectIds: TextListReader
            toCatId: str

        class MoveobjectsCallContext(Protocol):
            params: _AdminInterfaceModule.Server.MoveobjectsParams
            @property
            def results(self) -> _AdminInterfaceModule.Server.MoveobjectsResult: ...

        class RemoveobjectsParams(Protocol):
            objectIds: TextListReader

        class RemoveobjectsCallContext(Protocol):
            params: _AdminInterfaceModule.Server.RemoveobjectsParams
            @property
            def results(self) -> _AdminInterfaceModule.Server.RemoveobjectsResult: ...

        class RegistryParams(Protocol): ...

        class RegistryCallContext(Protocol):
            params: _AdminInterfaceModule.Server.RegistryParams
            @property
            def results(self) -> _AdminInterfaceModule.Server.RegistryResult: ...

        def addCategory(
            self,
            category: IdInformationReader,
            upsert: bool,
            _context: _AdminInterfaceModule.Server.AddcategoryCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            bool | _AdminInterfaceModule.Server.AddcategoryResultTuple | None
        ]: ...
        def addCategory_context(
            self, context: _AdminInterfaceModule.Server.AddcategoryCallContext
        ) -> Awaitable[None]: ...
        def removeCategory(
            self,
            categoryId: str,
            moveObjectsToCategoryId: str,
            _context: _AdminInterfaceModule.Server.RemovecategoryCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            Sequence[_IdentifiableInterfaceModule]
            | _AdminInterfaceModule.Server.RemovecategoryResultTuple
            | None
        ]: ...
        def removeCategory_context(
            self, context: _AdminInterfaceModule.Server.RemovecategoryCallContext
        ) -> Awaitable[None]: ...
        def moveObjects(
            self,
            objectIds: TextListReader,
            toCatId: str,
            _context: _AdminInterfaceModule.Server.MoveobjectsCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            Sequence[str] | _AdminInterfaceModule.Server.MoveobjectsResultTuple | None
        ]: ...
        def moveObjects_context(
            self, context: _AdminInterfaceModule.Server.MoveobjectsCallContext
        ) -> Awaitable[None]: ...
        def removeObjects(
            self,
            objectIds: TextListReader,
            _context: _AdminInterfaceModule.Server.RemoveobjectsCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            Sequence[_IdentifiableInterfaceModule]
            | _AdminInterfaceModule.Server.RemoveobjectsResultTuple
            | None
        ]: ...
        def removeObjects_context(
            self, context: _AdminInterfaceModule.Server.RemoveobjectsCallContext
        ) -> Awaitable[None]: ...
        def registry(
            self,
            _context: _AdminInterfaceModule.Server.RegistryCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            _RegistryInterfaceModule.Server
            | _AdminInterfaceModule.Server.RegistryResultTuple
            | None
        ]: ...
        def registry_context(
            self, context: _AdminInterfaceModule.Server.RegistryCallContext
        ) -> Awaitable[None]: ...

    class AdminClient(_IdentifiableInterfaceModule.IdentifiableClient):
        class AddcategoryResult(Awaitable[AddcategoryResult], Protocol):
            success: bool

        class RemovecategoryResult(Awaitable[RemovecategoryResult], Protocol):
            removedObjects: IdentifiableClientListReader

        class MoveobjectsResult(Awaitable[MoveobjectsResult], Protocol):
            movedObjectIds: TextListReader

        class RemoveobjectsResult(Awaitable[RemoveobjectsResult], Protocol):
            removedObjects: IdentifiableClientListReader

        class RegistryResult(Awaitable[RegistryResult], Protocol):
            registry: _RegistryInterfaceModule.RegistryClient

        def addCategory(
            self,
            category: IdInformationBuilder
            | IdInformationReader
            | dict[str, Any]
            | None = None,
            upsert: bool | None = None,
        ) -> _AdminInterfaceModule.AdminClient.AddcategoryResult: ...
        def removeCategory(
            self,
            categoryId: str | None = None,
            moveObjectsToCategoryId: str | None = None,
        ) -> _AdminInterfaceModule.AdminClient.RemovecategoryResult: ...
        def moveObjects(
            self,
            objectIds: TextListBuilder | TextListReader | Sequence[Any] | None = None,
            toCatId: str | None = None,
        ) -> _AdminInterfaceModule.AdminClient.MoveobjectsResult: ...
        def removeObjects(
            self,
            objectIds: TextListBuilder | TextListReader | Sequence[Any] | None = None,
        ) -> _AdminInterfaceModule.AdminClient.RemoveobjectsResult: ...
        def registry(self) -> _AdminInterfaceModule.AdminClient.RegistryResult: ...
        def addCategory_request(
            self,
            category: IdInformationBuilder | None = None,
            upsert: bool | None = None,
        ) -> _AdminInterfaceModule.AddcategoryRequest: ...
        def removeCategory_request(
            self,
            categoryId: str | None = None,
            moveObjectsToCategoryId: str | None = None,
        ) -> _AdminInterfaceModule.RemovecategoryRequest: ...
        def moveObjects_request(
            self,
            objectIds: TextListBuilder | TextListReader | Sequence[Any] | None = None,
            toCatId: str | None = None,
        ) -> _AdminInterfaceModule.MoveobjectsRequest: ...
        def removeObjects_request(
            self,
            objectIds: TextListBuilder | TextListReader | Sequence[Any] | None = None,
        ) -> _AdminInterfaceModule.RemoveobjectsRequest: ...
        def registry_request(self) -> _AdminInterfaceModule.RegistryRequest: ...

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

class _RegistryInterfaceModule(_IdentifiableInterfaceModule):
    class _EntryStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def categoryId(self) -> str: ...
            @property
            def ref(self) -> _IdentifiableInterfaceModule.IdentifiableClient: ...
            @property
            def name(self) -> str: ...
            @property
            def id(self) -> str: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> EntryBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def categoryId(self) -> str: ...
            @categoryId.setter
            def categoryId(self, value: str) -> None: ...
            @property
            def ref(self) -> _IdentifiableInterfaceModule.IdentifiableClient: ...
            @ref.setter
            def ref(
                self,
                value: _IdentifiableInterfaceModule.IdentifiableClient
                | _IdentifiableInterfaceModule.Server,
            ) -> None: ...
            @property
            def name(self) -> str: ...
            @name.setter
            def name(self, value: str) -> None: ...
            @property
            def id(self) -> str: ...
            @id.setter
            def id(self, value: str) -> None: ...
            @override
            def as_reader(self) -> EntryReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            categoryId: str | None = None,
            ref: _IdentifiableInterfaceModule.IdentifiableClient
            | _IdentifiableInterfaceModule.Server
            | None = None,
            name: str | None = None,
            id: str | None = None,
            **kwargs: Any,
        ) -> EntryBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[EntryReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[EntryReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[EntryBuilder]: ...
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
        ) -> EntryReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> EntryReader: ...

    type EntryReader = _EntryStructModule.Reader
    type EntryBuilder = _EntryStructModule.Builder
    Entry: _EntryStructModule
    class SupportedcategoriesRequest(Protocol):
        def send(
            self,
        ) -> _RegistryInterfaceModule.RegistryClient.SupportedcategoriesResult: ...

    class CategoryinfoRequest(Protocol):
        categoryId: str
        def send(
            self,
        ) -> _RegistryInterfaceModule.RegistryClient.CategoryinfoResult: ...

    class EntriesRequest(Protocol):
        categoryId: str
        def send(self) -> _RegistryInterfaceModule.RegistryClient.EntriesResult: ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _RegistryInterfaceModule.RegistryClient: ...
    class Server(_IdentifiableInterfaceModule.Server):
        class SupportedcategoriesResult(_DynamicStructBuilder):
            @property
            def cats(self) -> IdInformationListBuilder: ...
            @cats.setter
            def cats(
                self,
                value: IdInformationListBuilder
                | IdInformationListReader
                | Sequence[Any],
            ) -> None: ...
            @overload
            def init(
                self, field: Literal["cats"], size: int | None = None
            ) -> IdInformationListBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...

        class CategoryinfoResult(Awaitable[CategoryinfoResult], Protocol):
            id: str
            name: str
            description: str

        class EntriesResult(_DynamicStructBuilder):
            @property
            def entries(self) -> EntryListBuilder: ...
            @entries.setter
            def entries(
                self, value: EntryListBuilder | EntryListReader | Sequence[Any]
            ) -> None: ...
            @overload
            def init(
                self, field: Literal["entries"], size: int | None = None
            ) -> EntryListBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...

        class SupportedcategoriesResultTuple(NamedTuple):
            cats: IdInformationListBuilder | IdInformationListReader

        class CategoryinfoResultTuple(NamedTuple):
            id: str
            name: str
            description: str

        class EntriesResultTuple(NamedTuple):
            entries: EntryListBuilder | EntryListReader

        class SupportedcategoriesParams(Protocol): ...

        class SupportedcategoriesCallContext(Protocol):
            params: _RegistryInterfaceModule.Server.SupportedcategoriesParams
            @property
            def results(
                self,
            ) -> _RegistryInterfaceModule.Server.SupportedcategoriesResult: ...

        class CategoryinfoParams(Protocol):
            categoryId: str

        class CategoryinfoCallContext(Protocol):
            params: _RegistryInterfaceModule.Server.CategoryinfoParams
            @property
            def results(self) -> IdInformationBuilder: ...

        class EntriesParams(Protocol):
            categoryId: str

        class EntriesCallContext(Protocol):
            params: _RegistryInterfaceModule.Server.EntriesParams
            @property
            def results(self) -> _RegistryInterfaceModule.Server.EntriesResult: ...

        def supportedCategories(
            self,
            _context: _RegistryInterfaceModule.Server.SupportedcategoriesCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            Sequence[IdInformationBuilder | IdInformationReader]
            | _RegistryInterfaceModule.Server.SupportedcategoriesResultTuple
            | None
        ]: ...
        def supportedCategories_context(
            self,
            context: _RegistryInterfaceModule.Server.SupportedcategoriesCallContext,
        ) -> Awaitable[None]: ...
        def categoryInfo(
            self,
            categoryId: str,
            _context: _RegistryInterfaceModule.Server.CategoryinfoCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            _RegistryInterfaceModule.Server.CategoryinfoResultTuple | None
        ]: ...
        def categoryInfo_context(
            self, context: _RegistryInterfaceModule.Server.CategoryinfoCallContext
        ) -> Awaitable[None]: ...
        def entries(
            self,
            categoryId: str,
            _context: _RegistryInterfaceModule.Server.EntriesCallContext,
            **kwargs: Any,
        ) -> Awaitable[
            Sequence[EntryBuilder | EntryReader]
            | _RegistryInterfaceModule.Server.EntriesResultTuple
            | None
        ]: ...
        def entries_context(
            self, context: _RegistryInterfaceModule.Server.EntriesCallContext
        ) -> Awaitable[None]: ...

    class RegistryClient(_IdentifiableInterfaceModule.IdentifiableClient):
        class SupportedcategoriesResult(Awaitable[SupportedcategoriesResult], Protocol):
            cats: IdInformationListReader

        class CategoryinfoResult(Awaitable[CategoryinfoResult], Protocol):
            id: str
            name: str
            description: str

        class EntriesResult(Awaitable[EntriesResult], Protocol):
            entries: EntryListReader

        def supportedCategories(
            self,
        ) -> _RegistryInterfaceModule.RegistryClient.SupportedcategoriesResult: ...
        def categoryInfo(
            self, categoryId: str | None = None
        ) -> _RegistryInterfaceModule.RegistryClient.CategoryinfoResult: ...
        def entries(
            self, categoryId: str | None = None
        ) -> _RegistryInterfaceModule.RegistryClient.EntriesResult: ...
        def supportedCategories_request(
            self,
        ) -> _RegistryInterfaceModule.SupportedcategoriesRequest: ...
        def categoryInfo_request(
            self, categoryId: str | None = None
        ) -> _RegistryInterfaceModule.CategoryinfoRequest: ...
        def entries_request(
            self, categoryId: str | None = None
        ) -> _RegistryInterfaceModule.EntriesRequest: ...

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

class _EntryList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> EntryReader: ...
        @override
        def __iter__(self) -> Iterator[EntryReader]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> EntryBuilder: ...
        @override
        def __setitem__(
            self, key: int, value: EntryReader | EntryBuilder | dict[str, Any]
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[EntryBuilder]: ...
        @override
        def init(self, index: int, size: int | None = None) -> EntryBuilder: ...

Registry: _RegistryInterfaceModule
Admin: _AdminInterfaceModule

class _RegistrarInterfaceModule(_IdentifiableInterfaceModule):
    class _CrossDomainRestoreStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def vatId(self) -> VatIdReader: ...
            @property
            def restorer(self) -> _RestorerInterfaceModule.RestorerClient: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> CrossDomainRestoreBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def vatId(self) -> VatIdBuilder: ...
            @vatId.setter
            def vatId(
                self, value: VatIdBuilder | VatIdReader | dict[str, Any]
            ) -> None: ...
            @property
            def restorer(self) -> _RestorerInterfaceModule.RestorerClient: ...
            @restorer.setter
            def restorer(
                self,
                value: _RestorerInterfaceModule.RestorerClient
                | _RestorerInterfaceModule.Server,
            ) -> None: ...
            @override
            def init(
                self, field: Literal["vatId"], size: int | None = None
            ) -> VatIdBuilder: ...
            @override
            def as_reader(self) -> CrossDomainRestoreReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            vatId: VatIdBuilder | dict[str, Any] | None = None,
            restorer: _RestorerInterfaceModule.RestorerClient
            | _RestorerInterfaceModule.Server
            | None = None,
            **kwargs: Any,
        ) -> CrossDomainRestoreBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[CrossDomainRestoreReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[CrossDomainRestoreReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[CrossDomainRestoreBuilder]: ...
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
        ) -> CrossDomainRestoreReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> CrossDomainRestoreReader: ...

    type CrossDomainRestoreReader = _CrossDomainRestoreStructModule.Reader
    type CrossDomainRestoreBuilder = _CrossDomainRestoreStructModule.Builder
    CrossDomainRestore: _CrossDomainRestoreStructModule
    class _RegParamsStructModule(_StructModule):
        class Reader(_DynamicStructReader):
            @property
            def cap(self) -> _IdentifiableInterfaceModule.IdentifiableClient: ...
            @property
            def regName(self) -> str: ...
            @property
            def categoryId(self) -> str: ...
            @property
            def xDomain(self) -> CrossDomainRestoreReader: ...
            @override
            def as_builder(
                self,
                num_first_segment_words: int | None = None,
                allocate_seg_callable: Callable[[int], bytearray] | None = None,
            ) -> RegParamsBuilder: ...

        class Builder(_DynamicStructBuilder):
            @property
            def cap(self) -> _IdentifiableInterfaceModule.IdentifiableClient: ...
            @cap.setter
            def cap(
                self,
                value: _IdentifiableInterfaceModule.IdentifiableClient
                | _IdentifiableInterfaceModule.Server,
            ) -> None: ...
            @property
            def regName(self) -> str: ...
            @regName.setter
            def regName(self, value: str) -> None: ...
            @property
            def categoryId(self) -> str: ...
            @categoryId.setter
            def categoryId(self, value: str) -> None: ...
            @property
            def xDomain(self) -> CrossDomainRestoreBuilder: ...
            @xDomain.setter
            def xDomain(
                self,
                value: CrossDomainRestoreBuilder
                | CrossDomainRestoreReader
                | dict[str, Any],
            ) -> None: ...
            @override
            def init(
                self, field: Literal["xDomain"], size: int | None = None
            ) -> CrossDomainRestoreBuilder: ...
            @override
            def as_reader(self) -> RegParamsReader: ...

        @override
        def new_message(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
            cap: _IdentifiableInterfaceModule.IdentifiableClient
            | _IdentifiableInterfaceModule.Server
            | None = None,
            regName: str | None = None,
            categoryId: str | None = None,
            xDomain: CrossDomainRestoreBuilder | dict[str, Any] | None = None,
            **kwargs: Any,
        ) -> RegParamsBuilder: ...
        @override
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> AbstractContextManager[RegParamsReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[False],
        ) -> AbstractContextManager[RegParamsReader]: ...
        @overload
        def from_bytes(
            self,
            buf: bytes,
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
            *,
            builder: Literal[True],
        ) -> AbstractContextManager[RegParamsBuilder]: ...
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
        ) -> RegParamsReader: ...
        @override
        def read_packed(
            self,
            file: IO[str] | IO[bytes],
            traversal_limit_in_words: int | None = None,
            nesting_limit: int | None = None,
        ) -> RegParamsReader: ...

    type RegParamsReader = _RegParamsStructModule.Reader
    type RegParamsBuilder = _RegParamsStructModule.Builder
    RegParams: _RegParamsStructModule
    class _UnregisterInterfaceModule(_InterfaceModule):
        class UnregisterRequest(Protocol):
            def send(
                self,
            ) -> _RegistrarInterfaceModule._UnregisterInterfaceModule.UnregisterClient.UnregisterResult: ...

        @override
        def _new_client(
            self, server: _DynamicCapabilityServer
        ) -> _RegistrarInterfaceModule._UnregisterInterfaceModule.UnregisterClient: ...
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
                params: _RegistrarInterfaceModule._UnregisterInterfaceModule.Server.UnregisterParams
                @property
                def results(
                    self,
                ) -> _RegistrarInterfaceModule._UnregisterInterfaceModule.Server.UnregisterResult: ...

            def unregister(
                self,
                _context: _RegistrarInterfaceModule._UnregisterInterfaceModule.Server.UnregisterCallContext,
                **kwargs: Any,
            ) -> Awaitable[
                bool
                | _RegistrarInterfaceModule._UnregisterInterfaceModule.Server.UnregisterResultTuple
                | None
            ]: ...
            def unregister_context(
                self,
                context: _RegistrarInterfaceModule._UnregisterInterfaceModule.Server.UnregisterCallContext,
            ) -> Awaitable[None]: ...

        class UnregisterClient(_DynamicCapabilityClient):
            class UnregisterResult(Awaitable[UnregisterResult], Protocol):
                success: bool

            def unregister(
                self,
            ) -> _RegistrarInterfaceModule._UnregisterInterfaceModule.UnregisterClient.UnregisterResult: ...
            def unregister_request(
                self,
            ) -> (
                _RegistrarInterfaceModule._UnregisterInterfaceModule.UnregisterRequest
            ): ...

    Unregister: _UnregisterInterfaceModule
    type UnregisterClient = (
        _RegistrarInterfaceModule._UnregisterInterfaceModule.UnregisterClient
    )
    type UnregisterServer = _RegistrarInterfaceModule._UnregisterInterfaceModule.Server
    class RegisterRequest(Protocol):
        cap: IdentifiableClient | _IdentifiableInterfaceModule.Server
        regName: str
        categoryId: str
        xDomain: CrossDomainRestoreBuilder
        @overload
        def init(self, name: Literal["xDomain"]) -> CrossDomainRestoreBuilder: ...
        @overload
        def init(self, name: str, size: int = ...) -> Any: ...
        def send(self) -> _RegistrarInterfaceModule.RegistrarClient.RegisterResult: ...

    @override
    def _new_client(
        self, server: _DynamicCapabilityServer
    ) -> _RegistrarInterfaceModule.RegistrarClient: ...
    class Server(_IdentifiableInterfaceModule.Server):
        class RegisterResult(_DynamicStructBuilder):
            @property
            def unreg(
                self,
            ) -> (
                _RegistrarInterfaceModule._UnregisterInterfaceModule.Server
                | _RegistrarInterfaceModule._UnregisterInterfaceModule.UnregisterClient
            ): ...
            @unreg.setter
            def unreg(
                self,
                value: _RegistrarInterfaceModule._UnregisterInterfaceModule.Server
                | _RegistrarInterfaceModule._UnregisterInterfaceModule.UnregisterClient,
            ) -> None: ...
            @property
            def reregSR(self) -> SturdyRefBuilder: ...
            @reregSR.setter
            def reregSR(
                self, value: SturdyRefBuilder | SturdyRefReader | dict[str, Any]
            ) -> None: ...
            @overload
            def init(
                self, field: Literal["reregSR"], size: int | None = None
            ) -> SturdyRefBuilder: ...
            @overload
            def init(self, field: str, size: int | None = None) -> Any: ...

        class RegisterResultTuple(NamedTuple):
            unreg: (
                _RegistrarInterfaceModule._UnregisterInterfaceModule.Server
                | _RegistrarInterfaceModule._UnregisterInterfaceModule.UnregisterClient
            )
            reregSR: SturdyRefBuilder | SturdyRefReader

        class RegisterParams(Protocol):
            cap: IdentifiableClient
            regName: str
            categoryId: str
            xDomain: CrossDomainRestoreReader

        class RegisterCallContext(Protocol):
            params: _RegistrarInterfaceModule.Server.RegisterParams
            @property
            def results(self) -> _RegistrarInterfaceModule.Server.RegisterResult: ...

        def register(
            self,
            cap: IdentifiableClient,
            regName: str,
            categoryId: str,
            xDomain: CrossDomainRestoreReader,
            _context: _RegistrarInterfaceModule.Server.RegisterCallContext,
            **kwargs: Any,
        ) -> Awaitable[_RegistrarInterfaceModule.Server.RegisterResultTuple | None]: ...
        def register_context(
            self, context: _RegistrarInterfaceModule.Server.RegisterCallContext
        ) -> Awaitable[None]: ...

    class RegistrarClient(_IdentifiableInterfaceModule.IdentifiableClient):
        class RegisterResult(Awaitable[RegisterResult], Protocol):
            unreg: _RegistrarInterfaceModule._UnregisterInterfaceModule.UnregisterClient
            reregSR: SturdyRefReader

        def register(
            self,
            cap: IdentifiableClient | _IdentifiableInterfaceModule.Server | None = None,
            regName: str | None = None,
            categoryId: str | None = None,
            xDomain: CrossDomainRestoreBuilder
            | CrossDomainRestoreReader
            | dict[str, Any]
            | None = None,
        ) -> _RegistrarInterfaceModule.RegistrarClient.RegisterResult: ...
        def register_request(
            self,
            cap: IdentifiableClient | _IdentifiableInterfaceModule.Server | None = None,
            regName: str | None = None,
            categoryId: str | None = None,
            xDomain: CrossDomainRestoreBuilder | None = None,
        ) -> _RegistrarInterfaceModule.RegisterRequest: ...

Registrar: _RegistrarInterfaceModule

# Top-level type aliases for use in type annotations
type AddcategoryResult = _AdminInterfaceModule.AdminClient.AddcategoryResult
type AdminClient = _AdminInterfaceModule.AdminClient
type AdminServer = _AdminInterfaceModule.Server
type CategoryinfoResult = _RegistryInterfaceModule.RegistryClient.CategoryinfoResult
type CrossDomainRestoreBuilder = (
    _RegistrarInterfaceModule._CrossDomainRestoreStructModule.Builder
)
type CrossDomainRestoreReader = (
    _RegistrarInterfaceModule._CrossDomainRestoreStructModule.Reader
)
type EntriesResult = _RegistryInterfaceModule.RegistryClient.EntriesResult
type EntryBuilder = _RegistryInterfaceModule._EntryStructModule.Builder
type EntryListBuilder = _EntryList.Builder
type EntryListReader = _EntryList.Reader
type EntryReader = _RegistryInterfaceModule._EntryStructModule.Reader
type IdInformationListBuilder = _IdInformationList.Builder
type IdInformationListReader = _IdInformationList.Reader
type IdentifiableClientListBuilder = _IdentifiableClientList.Builder
type IdentifiableClientListReader = _IdentifiableClientList.Reader
type MoveobjectsResult = _AdminInterfaceModule.AdminClient.MoveobjectsResult
type RegParamsBuilder = _RegistrarInterfaceModule._RegParamsStructModule.Builder
type RegParamsReader = _RegistrarInterfaceModule._RegParamsStructModule.Reader
type RegisterResult = _RegistrarInterfaceModule.RegistrarClient.RegisterResult
type RegistrarClient = _RegistrarInterfaceModule.RegistrarClient
type RegistrarServer = _RegistrarInterfaceModule.Server
type RegistryClient = _RegistryInterfaceModule.RegistryClient
type RegistryResult = _AdminInterfaceModule.AdminClient.RegistryResult
type RegistryServer = _RegistryInterfaceModule.Server
type RemovecategoryResult = _AdminInterfaceModule.AdminClient.RemovecategoryResult
type RemoveobjectsResult = _AdminInterfaceModule.AdminClient.RemoveobjectsResult
type SupportedcategoriesResult = (
    _RegistryInterfaceModule.RegistryClient.SupportedcategoriesResult
)
type TextListBuilder = _TextList.Builder
type TextListReader = _TextList.Reader
type UnregisterClient = (
    _RegistrarInterfaceModule._UnregisterInterfaceModule.UnregisterClient
)
type UnregisterResult = _RegistrarInterfaceModule._UnregisterInterfaceModule.UnregisterClient.UnregisterResult
type UnregisterServer = _RegistrarInterfaceModule._UnregisterInterfaceModule.Server
