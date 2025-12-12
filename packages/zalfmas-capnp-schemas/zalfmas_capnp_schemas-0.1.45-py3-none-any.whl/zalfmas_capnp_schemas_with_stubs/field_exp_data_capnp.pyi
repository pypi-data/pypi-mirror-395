"""This is an automatically generated stub for `field_exp_data.capnp`."""

from __future__ import annotations
from capnp.lib.capnp import (
    _DynamicStructBuilder,
    _DynamicStructReader,
    _DynamicListBuilder,
    _DynamicListReader,
    _StructModule,
)
from contextlib import AbstractContextManager
from .soil_capnp import _ProfileInterfaceModule
from .climate_capnp import _TimeSeriesInterfaceModule
from .date_capnp import DateReader, DateBuilder
from collections.abc import Iterator, Callable
from typing import Literal, overload, override, Any, IO

class _WeatherStationStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def id(self) -> str: ...
        @property
        def name(self) -> str: ...
        @property
        def instituteName(self) -> str: ...
        @property
        def site(self) -> str: ...
        @property
        def country(self) -> str: ...
        @property
        def location2ndLevel(self) -> str: ...
        @property
        def location3rdLevel(self) -> str: ...
        @property
        def latitudeInDecDeg(self) -> float: ...
        @property
        def longitudeInDecDeg(self) -> float: ...
        @property
        def elevationM(self) -> float: ...
        @property
        def yearlyAvgTempInDegC(self) -> float: ...
        @property
        def amplitudeOfMonthlyAvgTempsInDegC(self) -> float: ...
        @property
        def tempSensorHeightInM(self) -> float: ...
        @property
        def refHeightWeatherMeasurementInM(self) -> float: ...
        @property
        def refHeightWindspeedMeasurementInM(self) -> float: ...
        @property
        def annualCO2ConcentrationInPPM(self) -> float: ...
        @property
        def notes(self) -> str: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> WeatherStationBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def id(self) -> str: ...
        @id.setter
        def id(self, value: str) -> None: ...
        @property
        def name(self) -> str: ...
        @name.setter
        def name(self, value: str) -> None: ...
        @property
        def instituteName(self) -> str: ...
        @instituteName.setter
        def instituteName(self, value: str) -> None: ...
        @property
        def site(self) -> str: ...
        @site.setter
        def site(self, value: str) -> None: ...
        @property
        def country(self) -> str: ...
        @country.setter
        def country(self, value: str) -> None: ...
        @property
        def location2ndLevel(self) -> str: ...
        @location2ndLevel.setter
        def location2ndLevel(self, value: str) -> None: ...
        @property
        def location3rdLevel(self) -> str: ...
        @location3rdLevel.setter
        def location3rdLevel(self, value: str) -> None: ...
        @property
        def latitudeInDecDeg(self) -> float: ...
        @latitudeInDecDeg.setter
        def latitudeInDecDeg(self, value: float) -> None: ...
        @property
        def longitudeInDecDeg(self) -> float: ...
        @longitudeInDecDeg.setter
        def longitudeInDecDeg(self, value: float) -> None: ...
        @property
        def elevationM(self) -> float: ...
        @elevationM.setter
        def elevationM(self, value: float) -> None: ...
        @property
        def yearlyAvgTempInDegC(self) -> float: ...
        @yearlyAvgTempInDegC.setter
        def yearlyAvgTempInDegC(self, value: float) -> None: ...
        @property
        def amplitudeOfMonthlyAvgTempsInDegC(self) -> float: ...
        @amplitudeOfMonthlyAvgTempsInDegC.setter
        def amplitudeOfMonthlyAvgTempsInDegC(self, value: float) -> None: ...
        @property
        def tempSensorHeightInM(self) -> float: ...
        @tempSensorHeightInM.setter
        def tempSensorHeightInM(self, value: float) -> None: ...
        @property
        def refHeightWeatherMeasurementInM(self) -> float: ...
        @refHeightWeatherMeasurementInM.setter
        def refHeightWeatherMeasurementInM(self, value: float) -> None: ...
        @property
        def refHeightWindspeedMeasurementInM(self) -> float: ...
        @refHeightWindspeedMeasurementInM.setter
        def refHeightWindspeedMeasurementInM(self, value: float) -> None: ...
        @property
        def annualCO2ConcentrationInPPM(self) -> float: ...
        @annualCO2ConcentrationInPPM.setter
        def annualCO2ConcentrationInPPM(self, value: float) -> None: ...
        @property
        def notes(self) -> str: ...
        @notes.setter
        def notes(self, value: str) -> None: ...
        @override
        def as_reader(self) -> WeatherStationReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        id: str | None = None,
        name: str | None = None,
        instituteName: str | None = None,
        site: str | None = None,
        country: str | None = None,
        location2ndLevel: str | None = None,
        location3rdLevel: str | None = None,
        latitudeInDecDeg: float | None = None,
        longitudeInDecDeg: float | None = None,
        elevationM: float | None = None,
        yearlyAvgTempInDegC: float | None = None,
        amplitudeOfMonthlyAvgTempsInDegC: float | None = None,
        tempSensorHeightInM: float | None = None,
        refHeightWeatherMeasurementInM: float | None = None,
        refHeightWindspeedMeasurementInM: float | None = None,
        annualCO2ConcentrationInPPM: float | None = None,
        notes: str | None = None,
        **kwargs: Any,
    ) -> WeatherStationBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[WeatherStationReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[WeatherStationReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[WeatherStationBuilder]: ...
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
    ) -> WeatherStationReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> WeatherStationReader: ...

WeatherStation: _WeatherStationStructModule

class _SoilMetadataStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def id(self) -> str: ...
        @property
        def name(self) -> str: ...
        @property
        def source(self) -> str: ...
        @property
        def depthInCM(self) -> int: ...
        @property
        def obstableDepthInCM(self) -> int: ...
        @property
        def depthOfTopsoilInCM(self) -> int: ...
        @property
        def drainageRatePerDay(self) -> float: ...
        @property
        def runoffCureNoSCS(self) -> float: ...
        @property
        def soilAvailableWaterContentInCM(self) -> float: ...
        @property
        def surfaceStoneCoverAsFraction(self) -> float: ...
        @property
        def soilAlbedo(self) -> float: ...
        @property
        def soilEvaporationLimitInMM(self) -> float: ...
        @property
        def mineralizationFactor(self) -> float: ...
        @property
        def soilFertilityOnFoto(self) -> float: ...
        @property
        def soilClassificationSystem(self) -> str: ...
        @property
        def soilTexture(self) -> str: ...
        @property
        def classification(self) -> str: ...
        @property
        def notes(self) -> str: ...
        @property
        def profile(self) -> _ProfileInterfaceModule.ProfileClient: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> SoilMetadataBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def id(self) -> str: ...
        @id.setter
        def id(self, value: str) -> None: ...
        @property
        def name(self) -> str: ...
        @name.setter
        def name(self, value: str) -> None: ...
        @property
        def source(self) -> str: ...
        @source.setter
        def source(self, value: str) -> None: ...
        @property
        def depthInCM(self) -> int: ...
        @depthInCM.setter
        def depthInCM(self, value: int) -> None: ...
        @property
        def obstableDepthInCM(self) -> int: ...
        @obstableDepthInCM.setter
        def obstableDepthInCM(self, value: int) -> None: ...
        @property
        def depthOfTopsoilInCM(self) -> int: ...
        @depthOfTopsoilInCM.setter
        def depthOfTopsoilInCM(self, value: int) -> None: ...
        @property
        def drainageRatePerDay(self) -> float: ...
        @drainageRatePerDay.setter
        def drainageRatePerDay(self, value: float) -> None: ...
        @property
        def runoffCureNoSCS(self) -> float: ...
        @runoffCureNoSCS.setter
        def runoffCureNoSCS(self, value: float) -> None: ...
        @property
        def soilAvailableWaterContentInCM(self) -> float: ...
        @soilAvailableWaterContentInCM.setter
        def soilAvailableWaterContentInCM(self, value: float) -> None: ...
        @property
        def surfaceStoneCoverAsFraction(self) -> float: ...
        @surfaceStoneCoverAsFraction.setter
        def surfaceStoneCoverAsFraction(self, value: float) -> None: ...
        @property
        def soilAlbedo(self) -> float: ...
        @soilAlbedo.setter
        def soilAlbedo(self, value: float) -> None: ...
        @property
        def soilEvaporationLimitInMM(self) -> float: ...
        @soilEvaporationLimitInMM.setter
        def soilEvaporationLimitInMM(self, value: float) -> None: ...
        @property
        def mineralizationFactor(self) -> float: ...
        @mineralizationFactor.setter
        def mineralizationFactor(self, value: float) -> None: ...
        @property
        def soilFertilityOnFoto(self) -> float: ...
        @soilFertilityOnFoto.setter
        def soilFertilityOnFoto(self, value: float) -> None: ...
        @property
        def soilClassificationSystem(self) -> str: ...
        @soilClassificationSystem.setter
        def soilClassificationSystem(self, value: str) -> None: ...
        @property
        def soilTexture(self) -> str: ...
        @soilTexture.setter
        def soilTexture(self, value: str) -> None: ...
        @property
        def classification(self) -> str: ...
        @classification.setter
        def classification(self, value: str) -> None: ...
        @property
        def notes(self) -> str: ...
        @notes.setter
        def notes(self, value: str) -> None: ...
        @property
        def profile(self) -> _ProfileInterfaceModule.ProfileClient: ...
        @profile.setter
        def profile(
            self,
            value: _ProfileInterfaceModule.ProfileClient
            | _ProfileInterfaceModule.Server,
        ) -> None: ...
        @override
        def as_reader(self) -> SoilMetadataReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        id: str | None = None,
        name: str | None = None,
        source: str | None = None,
        depthInCM: int | None = None,
        obstableDepthInCM: int | None = None,
        depthOfTopsoilInCM: int | None = None,
        drainageRatePerDay: float | None = None,
        runoffCureNoSCS: float | None = None,
        soilAvailableWaterContentInCM: float | None = None,
        surfaceStoneCoverAsFraction: float | None = None,
        soilAlbedo: float | None = None,
        soilEvaporationLimitInMM: float | None = None,
        mineralizationFactor: float | None = None,
        soilFertilityOnFoto: float | None = None,
        soilClassificationSystem: str | None = None,
        soilTexture: str | None = None,
        classification: str | None = None,
        notes: str | None = None,
        profile: _ProfileInterfaceModule.ProfileClient
        | _ProfileInterfaceModule.Server
        | None = None,
        **kwargs: Any,
    ) -> SoilMetadataBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[SoilMetadataReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[SoilMetadataReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[SoilMetadataBuilder]: ...
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
    ) -> SoilMetadataReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> SoilMetadataReader: ...

SoilMetadata: _SoilMetadataStructModule

class _FieldStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def id(self) -> str: ...
        @property
        def name(self) -> str: ...
        @property
        def latitudeInDecDeg(self) -> float: ...
        @property
        def longitudeInDecDeg(self) -> float: ...
        @property
        def elevationInM(self) -> float: ...
        @property
        def slopeDegreeInDeg(self) -> float: ...
        @property
        def drainageType(self) -> str: ...
        @property
        def distanceToWeatherStationInKM(self) -> float: ...
        @property
        def country(self) -> str: ...
        @property
        def subCountry(self) -> str: ...
        @property
        def subSubCountry(self) -> str: ...
        @property
        def notes(self) -> str: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> FieldBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def id(self) -> str: ...
        @id.setter
        def id(self, value: str) -> None: ...
        @property
        def name(self) -> str: ...
        @name.setter
        def name(self, value: str) -> None: ...
        @property
        def latitudeInDecDeg(self) -> float: ...
        @latitudeInDecDeg.setter
        def latitudeInDecDeg(self, value: float) -> None: ...
        @property
        def longitudeInDecDeg(self) -> float: ...
        @longitudeInDecDeg.setter
        def longitudeInDecDeg(self, value: float) -> None: ...
        @property
        def elevationInM(self) -> float: ...
        @elevationInM.setter
        def elevationInM(self, value: float) -> None: ...
        @property
        def slopeDegreeInDeg(self) -> float: ...
        @slopeDegreeInDeg.setter
        def slopeDegreeInDeg(self, value: float) -> None: ...
        @property
        def drainageType(self) -> str: ...
        @drainageType.setter
        def drainageType(self, value: str) -> None: ...
        @property
        def distanceToWeatherStationInKM(self) -> float: ...
        @distanceToWeatherStationInKM.setter
        def distanceToWeatherStationInKM(self, value: float) -> None: ...
        @property
        def country(self) -> str: ...
        @country.setter
        def country(self, value: str) -> None: ...
        @property
        def subCountry(self) -> str: ...
        @subCountry.setter
        def subCountry(self, value: str) -> None: ...
        @property
        def subSubCountry(self) -> str: ...
        @subSubCountry.setter
        def subSubCountry(self, value: str) -> None: ...
        @property
        def notes(self) -> str: ...
        @notes.setter
        def notes(self, value: str) -> None: ...
        @override
        def as_reader(self) -> FieldReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        id: str | None = None,
        name: str | None = None,
        latitudeInDecDeg: float | None = None,
        longitudeInDecDeg: float | None = None,
        elevationInM: float | None = None,
        slopeDegreeInDeg: float | None = None,
        drainageType: str | None = None,
        distanceToWeatherStationInKM: float | None = None,
        country: str | None = None,
        subCountry: str | None = None,
        subSubCountry: str | None = None,
        notes: str | None = None,
        **kwargs: Any,
    ) -> FieldBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[FieldReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[FieldReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[FieldBuilder]: ...
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
    ) -> FieldReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> FieldReader: ...

Field: _FieldStructModule

class _CultivarStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def id(self) -> str: ...
        @property
        def name(self) -> str: ...
        @property
        def accessionId(self) -> str: ...
        @property
        def accessionLocation(self) -> str: ...
        @property
        def cropIdentifierICASA(self) -> str: ...
        @property
        def seedLot(self) -> str: ...
        @property
        def breedingProgram(self) -> str: ...
        @property
        def originalName(self) -> str: ...
        @property
        def releaseYear(self) -> int: ...
        @property
        def synonym(self) -> str: ...
        @property
        def notes(self) -> str: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> CultivarBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def id(self) -> str: ...
        @id.setter
        def id(self, value: str) -> None: ...
        @property
        def name(self) -> str: ...
        @name.setter
        def name(self, value: str) -> None: ...
        @property
        def accessionId(self) -> str: ...
        @accessionId.setter
        def accessionId(self, value: str) -> None: ...
        @property
        def accessionLocation(self) -> str: ...
        @accessionLocation.setter
        def accessionLocation(self, value: str) -> None: ...
        @property
        def cropIdentifierICASA(self) -> str: ...
        @cropIdentifierICASA.setter
        def cropIdentifierICASA(self, value: str) -> None: ...
        @property
        def seedLot(self) -> str: ...
        @seedLot.setter
        def seedLot(self, value: str) -> None: ...
        @property
        def breedingProgram(self) -> str: ...
        @breedingProgram.setter
        def breedingProgram(self, value: str) -> None: ...
        @property
        def originalName(self) -> str: ...
        @originalName.setter
        def originalName(self, value: str) -> None: ...
        @property
        def releaseYear(self) -> int: ...
        @releaseYear.setter
        def releaseYear(self, value: int) -> None: ...
        @property
        def synonym(self) -> str: ...
        @synonym.setter
        def synonym(self, value: str) -> None: ...
        @property
        def notes(self) -> str: ...
        @notes.setter
        def notes(self, value: str) -> None: ...
        @override
        def as_reader(self) -> CultivarReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        id: str | None = None,
        name: str | None = None,
        accessionId: str | None = None,
        accessionLocation: str | None = None,
        cropIdentifierICASA: str | None = None,
        seedLot: str | None = None,
        breedingProgram: str | None = None,
        originalName: str | None = None,
        releaseYear: int | None = None,
        synonym: str | None = None,
        notes: str | None = None,
        **kwargs: Any,
    ) -> CultivarBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[CultivarReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[CultivarReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[CultivarBuilder]: ...
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
    ) -> CultivarReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> CultivarReader: ...

Cultivar: _CultivarStructModule

class _PlotStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def id(self) -> str: ...
        @property
        def cultivar(self) -> CultivarReader: ...
        @property
        def soil(self) -> SoilMetadataReader: ...
        @property
        def blockNumber(self) -> int: ...
        @property
        def plotNumber(self) -> int: ...
        @property
        def replicateNumber(self) -> int: ...
        @property
        def rowNumber(self) -> int: ...
        @property
        def columnNumber(self) -> int: ...
        @property
        def harvestMethod(self) -> str: ...
        @property
        def notes(self) -> str: ...
        @property
        def experimentId(self) -> str: ...
        @property
        def treatmentId(self) -> str: ...
        @property
        def cultivarId(self) -> str: ...
        @property
        def soilId(self) -> str: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> PlotBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def id(self) -> str: ...
        @id.setter
        def id(self, value: str) -> None: ...
        @property
        def cultivar(self) -> CultivarBuilder: ...
        @cultivar.setter
        def cultivar(
            self, value: CultivarBuilder | CultivarReader | dict[str, Any]
        ) -> None: ...
        @property
        def soil(self) -> SoilMetadataBuilder: ...
        @soil.setter
        def soil(
            self, value: SoilMetadataBuilder | SoilMetadataReader | dict[str, Any]
        ) -> None: ...
        @property
        def blockNumber(self) -> int: ...
        @blockNumber.setter
        def blockNumber(self, value: int) -> None: ...
        @property
        def plotNumber(self) -> int: ...
        @plotNumber.setter
        def plotNumber(self, value: int) -> None: ...
        @property
        def replicateNumber(self) -> int: ...
        @replicateNumber.setter
        def replicateNumber(self, value: int) -> None: ...
        @property
        def rowNumber(self) -> int: ...
        @rowNumber.setter
        def rowNumber(self, value: int) -> None: ...
        @property
        def columnNumber(self) -> int: ...
        @columnNumber.setter
        def columnNumber(self, value: int) -> None: ...
        @property
        def harvestMethod(self) -> str: ...
        @harvestMethod.setter
        def harvestMethod(self, value: str) -> None: ...
        @property
        def notes(self) -> str: ...
        @notes.setter
        def notes(self, value: str) -> None: ...
        @property
        def experimentId(self) -> str: ...
        @experimentId.setter
        def experimentId(self, value: str) -> None: ...
        @property
        def treatmentId(self) -> str: ...
        @treatmentId.setter
        def treatmentId(self, value: str) -> None: ...
        @property
        def cultivarId(self) -> str: ...
        @cultivarId.setter
        def cultivarId(self, value: str) -> None: ...
        @property
        def soilId(self) -> str: ...
        @soilId.setter
        def soilId(self, value: str) -> None: ...
        @override
        @overload
        def init(
            self, field: Literal["cultivar"], size: int | None = None
        ) -> CultivarBuilder: ...
        @overload
        def init(
            self, field: Literal["soil"], size: int | None = None
        ) -> SoilMetadataBuilder: ...
        @overload
        def init(self, field: str, size: int | None = None) -> Any: ...
        @override
        def as_reader(self) -> PlotReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        id: str | None = None,
        cultivar: CultivarBuilder | dict[str, Any] | None = None,
        soil: SoilMetadataBuilder | dict[str, Any] | None = None,
        blockNumber: int | None = None,
        plotNumber: int | None = None,
        replicateNumber: int | None = None,
        rowNumber: int | None = None,
        columnNumber: int | None = None,
        harvestMethod: str | None = None,
        notes: str | None = None,
        experimentId: str | None = None,
        treatmentId: str | None = None,
        cultivarId: str | None = None,
        soilId: str | None = None,
        **kwargs: Any,
    ) -> PlotBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[PlotReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[PlotReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[PlotBuilder]: ...
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
    ) -> PlotReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> PlotReader: ...

Plot: _PlotStructModule

class _PlotList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> PlotReader: ...
        @override
        def __iter__(self) -> Iterator[PlotReader]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> PlotBuilder: ...
        @override
        def __setitem__(
            self, key: int, value: PlotReader | PlotBuilder | dict[str, Any]
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[PlotBuilder]: ...
        @override
        def init(self, index: int, size: int | None = None) -> PlotBuilder: ...

class _ResidueStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def initialMeasureDate(self) -> DateReader: ...
        @property
        def incorporationDepth(self) -> int: ...
        @property
        def percentIncorporated(self) -> float: ...
        @property
        def prevCropCode(self) -> str: ...
        @property
        def aboveGroundWeight(self) -> float: ...
        @property
        def aboveGroundNConcentrationInPerc(self) -> float: ...
        @property
        def rootWeightPreviousCrop(self) -> float: ...
        @property
        def experimentId(self) -> str: ...
        @property
        def treatmentId(self) -> str: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> ResidueBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def initialMeasureDate(self) -> DateBuilder: ...
        @initialMeasureDate.setter
        def initialMeasureDate(
            self, value: DateBuilder | DateReader | dict[str, Any]
        ) -> None: ...
        @property
        def incorporationDepth(self) -> int: ...
        @incorporationDepth.setter
        def incorporationDepth(self, value: int) -> None: ...
        @property
        def percentIncorporated(self) -> float: ...
        @percentIncorporated.setter
        def percentIncorporated(self, value: float) -> None: ...
        @property
        def prevCropCode(self) -> str: ...
        @prevCropCode.setter
        def prevCropCode(self, value: str) -> None: ...
        @property
        def aboveGroundWeight(self) -> float: ...
        @aboveGroundWeight.setter
        def aboveGroundWeight(self, value: float) -> None: ...
        @property
        def aboveGroundNConcentrationInPerc(self) -> float: ...
        @aboveGroundNConcentrationInPerc.setter
        def aboveGroundNConcentrationInPerc(self, value: float) -> None: ...
        @property
        def rootWeightPreviousCrop(self) -> float: ...
        @rootWeightPreviousCrop.setter
        def rootWeightPreviousCrop(self, value: float) -> None: ...
        @property
        def experimentId(self) -> str: ...
        @experimentId.setter
        def experimentId(self, value: str) -> None: ...
        @property
        def treatmentId(self) -> str: ...
        @treatmentId.setter
        def treatmentId(self, value: str) -> None: ...
        @override
        def init(
            self, field: Literal["initialMeasureDate"], size: int | None = None
        ) -> DateBuilder: ...
        @override
        def as_reader(self) -> ResidueReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        initialMeasureDate: DateBuilder | dict[str, Any] | None = None,
        incorporationDepth: int | None = None,
        percentIncorporated: float | None = None,
        prevCropCode: str | None = None,
        aboveGroundWeight: float | None = None,
        aboveGroundNConcentrationInPerc: float | None = None,
        rootWeightPreviousCrop: float | None = None,
        experimentId: str | None = None,
        treatmentId: str | None = None,
        **kwargs: Any,
    ) -> ResidueBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[ResidueReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[ResidueReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[ResidueBuilder]: ...
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
    ) -> ResidueReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> ResidueReader: ...

Residue: _ResidueStructModule

class _InitialConditionsLayerStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def date(self) -> DateReader: ...
        @property
        def soilLayerTopDepthInCM(self) -> int: ...
        @property
        def soilLayerBaseDepthInCM(self) -> int: ...
        @property
        def waterConcentration(self) -> float: ...
        @property
        def totalNInKGperHA(self) -> float: ...
        @property
        def massNH4InKGperHA(self) -> float: ...
        @property
        def massNO3InKGperHA(self) -> float: ...
        @property
        def concNH4InPPM(self) -> float: ...
        @property
        def concNO3InPPM(self) -> float: ...
        @property
        def experimentId(self) -> str: ...
        @property
        def treatmentId(self) -> str: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> InitialConditionsLayerBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def date(self) -> DateBuilder: ...
        @date.setter
        def date(self, value: DateBuilder | DateReader | dict[str, Any]) -> None: ...
        @property
        def soilLayerTopDepthInCM(self) -> int: ...
        @soilLayerTopDepthInCM.setter
        def soilLayerTopDepthInCM(self, value: int) -> None: ...
        @property
        def soilLayerBaseDepthInCM(self) -> int: ...
        @soilLayerBaseDepthInCM.setter
        def soilLayerBaseDepthInCM(self, value: int) -> None: ...
        @property
        def waterConcentration(self) -> float: ...
        @waterConcentration.setter
        def waterConcentration(self, value: float) -> None: ...
        @property
        def totalNInKGperHA(self) -> float: ...
        @totalNInKGperHA.setter
        def totalNInKGperHA(self, value: float) -> None: ...
        @property
        def massNH4InKGperHA(self) -> float: ...
        @massNH4InKGperHA.setter
        def massNH4InKGperHA(self, value: float) -> None: ...
        @property
        def massNO3InKGperHA(self) -> float: ...
        @massNO3InKGperHA.setter
        def massNO3InKGperHA(self, value: float) -> None: ...
        @property
        def concNH4InPPM(self) -> float: ...
        @concNH4InPPM.setter
        def concNH4InPPM(self, value: float) -> None: ...
        @property
        def concNO3InPPM(self) -> float: ...
        @concNO3InPPM.setter
        def concNO3InPPM(self, value: float) -> None: ...
        @property
        def experimentId(self) -> str: ...
        @experimentId.setter
        def experimentId(self, value: str) -> None: ...
        @property
        def treatmentId(self) -> str: ...
        @treatmentId.setter
        def treatmentId(self, value: str) -> None: ...
        @override
        def init(
            self, field: Literal["date"], size: int | None = None
        ) -> DateBuilder: ...
        @override
        def as_reader(self) -> InitialConditionsLayerReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        date: DateBuilder | dict[str, Any] | None = None,
        soilLayerTopDepthInCM: int | None = None,
        soilLayerBaseDepthInCM: int | None = None,
        waterConcentration: float | None = None,
        totalNInKGperHA: float | None = None,
        massNH4InKGperHA: float | None = None,
        massNO3InKGperHA: float | None = None,
        concNH4InPPM: float | None = None,
        concNO3InPPM: float | None = None,
        experimentId: str | None = None,
        treatmentId: str | None = None,
        **kwargs: Any,
    ) -> InitialConditionsLayerBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[InitialConditionsLayerReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[InitialConditionsLayerReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[InitialConditionsLayerBuilder]: ...
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
    ) -> InitialConditionsLayerReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> InitialConditionsLayerReader: ...

InitialConditionsLayer: _InitialConditionsLayerStructModule

class _InitialConditionsLayerList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> InitialConditionsLayerReader: ...
        @override
        def __iter__(self) -> Iterator[InitialConditionsLayerReader]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> InitialConditionsLayerBuilder: ...
        @override
        def __setitem__(
            self,
            key: int,
            value: InitialConditionsLayerReader
            | InitialConditionsLayerBuilder
            | dict[str, Any],
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[InitialConditionsLayerBuilder]: ...
        @override
        def init(
            self, index: int, size: int | None = None
        ) -> InitialConditionsLayerBuilder: ...

class _PlantingEventStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def plantingDistribution(self) -> str: ...
        @property
        def rowSpacingInCM(self) -> float: ...
        @property
        def rowDirectionInArcDeg(self) -> float: ...
        @property
        def plantingDepthInMM(self) -> int: ...
        @property
        def plotLayout(self) -> str: ...
        @property
        def plantingDate(self) -> DateReader: ...
        @property
        def plantPopulationAtPlantingInNoPerM2(self) -> int: ...
        @property
        def averageEmergenceDate(self) -> DateReader: ...
        @property
        def averagePlantPopulationAtEmergenceInNoPerM2(self) -> int: ...
        @property
        def notes(self) -> str: ...
        @property
        def experimentId(self) -> str: ...
        @property
        def treatmentId(self) -> str: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> PlantingEventBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def plantingDistribution(self) -> str: ...
        @plantingDistribution.setter
        def plantingDistribution(self, value: str) -> None: ...
        @property
        def rowSpacingInCM(self) -> float: ...
        @rowSpacingInCM.setter
        def rowSpacingInCM(self, value: float) -> None: ...
        @property
        def rowDirectionInArcDeg(self) -> float: ...
        @rowDirectionInArcDeg.setter
        def rowDirectionInArcDeg(self, value: float) -> None: ...
        @property
        def plantingDepthInMM(self) -> int: ...
        @plantingDepthInMM.setter
        def plantingDepthInMM(self, value: int) -> None: ...
        @property
        def plotLayout(self) -> str: ...
        @plotLayout.setter
        def plotLayout(self, value: str) -> None: ...
        @property
        def plantingDate(self) -> DateBuilder: ...
        @plantingDate.setter
        def plantingDate(
            self, value: DateBuilder | DateReader | dict[str, Any]
        ) -> None: ...
        @property
        def plantPopulationAtPlantingInNoPerM2(self) -> int: ...
        @plantPopulationAtPlantingInNoPerM2.setter
        def plantPopulationAtPlantingInNoPerM2(self, value: int) -> None: ...
        @property
        def averageEmergenceDate(self) -> DateBuilder: ...
        @averageEmergenceDate.setter
        def averageEmergenceDate(
            self, value: DateBuilder | DateReader | dict[str, Any]
        ) -> None: ...
        @property
        def averagePlantPopulationAtEmergenceInNoPerM2(self) -> int: ...
        @averagePlantPopulationAtEmergenceInNoPerM2.setter
        def averagePlantPopulationAtEmergenceInNoPerM2(self, value: int) -> None: ...
        @property
        def notes(self) -> str: ...
        @notes.setter
        def notes(self, value: str) -> None: ...
        @property
        def experimentId(self) -> str: ...
        @experimentId.setter
        def experimentId(self, value: str) -> None: ...
        @property
        def treatmentId(self) -> str: ...
        @treatmentId.setter
        def treatmentId(self, value: str) -> None: ...
        @override
        @overload
        def init(
            self, field: Literal["plantingDate"], size: int | None = None
        ) -> DateBuilder: ...
        @overload
        def init(
            self, field: Literal["averageEmergenceDate"], size: int | None = None
        ) -> DateBuilder: ...
        @overload
        def init(self, field: str, size: int | None = None) -> Any: ...
        @override
        def as_reader(self) -> PlantingEventReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        plantingDistribution: str | None = None,
        rowSpacingInCM: float | None = None,
        rowDirectionInArcDeg: float | None = None,
        plantingDepthInMM: int | None = None,
        plotLayout: str | None = None,
        plantingDate: DateBuilder | dict[str, Any] | None = None,
        plantPopulationAtPlantingInNoPerM2: int | None = None,
        averageEmergenceDate: DateBuilder | dict[str, Any] | None = None,
        averagePlantPopulationAtEmergenceInNoPerM2: int | None = None,
        notes: str | None = None,
        experimentId: str | None = None,
        treatmentId: str | None = None,
        **kwargs: Any,
    ) -> PlantingEventBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[PlantingEventReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[PlantingEventReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[PlantingEventBuilder]: ...
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
    ) -> PlantingEventReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> PlantingEventReader: ...

PlantingEvent: _PlantingEventStructModule

class _PlantingEventList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> PlantingEventReader: ...
        @override
        def __iter__(self) -> Iterator[PlantingEventReader]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> PlantingEventBuilder: ...
        @override
        def __setitem__(
            self,
            key: int,
            value: PlantingEventReader | PlantingEventBuilder | dict[str, Any],
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[PlantingEventBuilder]: ...
        @override
        def init(self, index: int, size: int | None = None) -> PlantingEventBuilder: ...

class _HarvestEventStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def date(self) -> DateReader: ...
        @property
        def harvestMethod(self) -> str: ...
        @property
        def harvestArea(self) -> float: ...
        @property
        def notes(self) -> str: ...
        @property
        def comments(self) -> str: ...
        @property
        def experimentId(self) -> str: ...
        @property
        def treatmentId(self) -> str: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> HarvestEventBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def date(self) -> DateBuilder: ...
        @date.setter
        def date(self, value: DateBuilder | DateReader | dict[str, Any]) -> None: ...
        @property
        def harvestMethod(self) -> str: ...
        @harvestMethod.setter
        def harvestMethod(self, value: str) -> None: ...
        @property
        def harvestArea(self) -> float: ...
        @harvestArea.setter
        def harvestArea(self, value: float) -> None: ...
        @property
        def notes(self) -> str: ...
        @notes.setter
        def notes(self, value: str) -> None: ...
        @property
        def comments(self) -> str: ...
        @comments.setter
        def comments(self, value: str) -> None: ...
        @property
        def experimentId(self) -> str: ...
        @experimentId.setter
        def experimentId(self, value: str) -> None: ...
        @property
        def treatmentId(self) -> str: ...
        @treatmentId.setter
        def treatmentId(self, value: str) -> None: ...
        @override
        def init(
            self, field: Literal["date"], size: int | None = None
        ) -> DateBuilder: ...
        @override
        def as_reader(self) -> HarvestEventReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        date: DateBuilder | dict[str, Any] | None = None,
        harvestMethod: str | None = None,
        harvestArea: float | None = None,
        notes: str | None = None,
        comments: str | None = None,
        experimentId: str | None = None,
        treatmentId: str | None = None,
        **kwargs: Any,
    ) -> HarvestEventBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[HarvestEventReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[HarvestEventReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[HarvestEventBuilder]: ...
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
    ) -> HarvestEventReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> HarvestEventReader: ...

HarvestEvent: _HarvestEventStructModule

class _HarvestEventList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> HarvestEventReader: ...
        @override
        def __iter__(self) -> Iterator[HarvestEventReader]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> HarvestEventBuilder: ...
        @override
        def __setitem__(
            self,
            key: int,
            value: HarvestEventReader | HarvestEventBuilder | dict[str, Any],
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[HarvestEventBuilder]: ...
        @override
        def init(self, index: int, size: int | None = None) -> HarvestEventBuilder: ...

class _IrrigationEventStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def date(self) -> DateReader: ...
        @property
        def operation(self) -> str: ...
        @property
        def applicationDepth(self) -> int: ...
        @property
        def amount(self) -> int: ...
        @property
        def waterNConcentrationInPerc(self) -> float: ...
        @property
        def notes(self) -> str: ...
        @property
        def experimentId(self) -> str: ...
        @property
        def treatmentId(self) -> str: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> IrrigationEventBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def date(self) -> DateBuilder: ...
        @date.setter
        def date(self, value: DateBuilder | DateReader | dict[str, Any]) -> None: ...
        @property
        def operation(self) -> str: ...
        @operation.setter
        def operation(self, value: str) -> None: ...
        @property
        def applicationDepth(self) -> int: ...
        @applicationDepth.setter
        def applicationDepth(self, value: int) -> None: ...
        @property
        def amount(self) -> int: ...
        @amount.setter
        def amount(self, value: int) -> None: ...
        @property
        def waterNConcentrationInPerc(self) -> float: ...
        @waterNConcentrationInPerc.setter
        def waterNConcentrationInPerc(self, value: float) -> None: ...
        @property
        def notes(self) -> str: ...
        @notes.setter
        def notes(self, value: str) -> None: ...
        @property
        def experimentId(self) -> str: ...
        @experimentId.setter
        def experimentId(self, value: str) -> None: ...
        @property
        def treatmentId(self) -> str: ...
        @treatmentId.setter
        def treatmentId(self, value: str) -> None: ...
        @override
        def init(
            self, field: Literal["date"], size: int | None = None
        ) -> DateBuilder: ...
        @override
        def as_reader(self) -> IrrigationEventReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        date: DateBuilder | dict[str, Any] | None = None,
        operation: str | None = None,
        applicationDepth: int | None = None,
        amount: int | None = None,
        waterNConcentrationInPerc: float | None = None,
        notes: str | None = None,
        experimentId: str | None = None,
        treatmentId: str | None = None,
        **kwargs: Any,
    ) -> IrrigationEventBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[IrrigationEventReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[IrrigationEventReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[IrrigationEventBuilder]: ...
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
    ) -> IrrigationEventReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> IrrigationEventReader: ...

IrrigationEvent: _IrrigationEventStructModule

class _IrrigationEventList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> IrrigationEventReader: ...
        @override
        def __iter__(self) -> Iterator[IrrigationEventReader]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> IrrigationEventBuilder: ...
        @override
        def __setitem__(
            self,
            key: int,
            value: IrrigationEventReader | IrrigationEventBuilder | dict[str, Any],
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[IrrigationEventBuilder]: ...
        @override
        def init(
            self, index: int, size: int | None = None
        ) -> IrrigationEventBuilder: ...

class _FertilizerEventStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def date(self) -> DateReader: ...
        @property
        def applicationMethod(self) -> str: ...
        @property
        def applicationDepthInCM(self) -> int: ...
        @property
        def material(self) -> str: ...
        @property
        def appliedNInKGNPerHA(self) -> int: ...
        @property
        def appliedNO3InKGNperHA(self) -> int: ...
        @property
        def appliedNH4InKGNperHA(self) -> int: ...
        @property
        def notes(self) -> str: ...
        @property
        def experimentId(self) -> str: ...
        @property
        def treatmentId(self) -> str: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> FertilizerEventBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def date(self) -> DateBuilder: ...
        @date.setter
        def date(self, value: DateBuilder | DateReader | dict[str, Any]) -> None: ...
        @property
        def applicationMethod(self) -> str: ...
        @applicationMethod.setter
        def applicationMethod(self, value: str) -> None: ...
        @property
        def applicationDepthInCM(self) -> int: ...
        @applicationDepthInCM.setter
        def applicationDepthInCM(self, value: int) -> None: ...
        @property
        def material(self) -> str: ...
        @material.setter
        def material(self, value: str) -> None: ...
        @property
        def appliedNInKGNPerHA(self) -> int: ...
        @appliedNInKGNPerHA.setter
        def appliedNInKGNPerHA(self, value: int) -> None: ...
        @property
        def appliedNO3InKGNperHA(self) -> int: ...
        @appliedNO3InKGNperHA.setter
        def appliedNO3InKGNperHA(self, value: int) -> None: ...
        @property
        def appliedNH4InKGNperHA(self) -> int: ...
        @appliedNH4InKGNperHA.setter
        def appliedNH4InKGNperHA(self, value: int) -> None: ...
        @property
        def notes(self) -> str: ...
        @notes.setter
        def notes(self, value: str) -> None: ...
        @property
        def experimentId(self) -> str: ...
        @experimentId.setter
        def experimentId(self, value: str) -> None: ...
        @property
        def treatmentId(self) -> str: ...
        @treatmentId.setter
        def treatmentId(self, value: str) -> None: ...
        @override
        def init(
            self, field: Literal["date"], size: int | None = None
        ) -> DateBuilder: ...
        @override
        def as_reader(self) -> FertilizerEventReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        date: DateBuilder | dict[str, Any] | None = None,
        applicationMethod: str | None = None,
        applicationDepthInCM: int | None = None,
        material: str | None = None,
        appliedNInKGNPerHA: int | None = None,
        appliedNO3InKGNperHA: int | None = None,
        appliedNH4InKGNperHA: int | None = None,
        notes: str | None = None,
        experimentId: str | None = None,
        treatmentId: str | None = None,
        **kwargs: Any,
    ) -> FertilizerEventBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[FertilizerEventReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[FertilizerEventReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[FertilizerEventBuilder]: ...
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
    ) -> FertilizerEventReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> FertilizerEventReader: ...

FertilizerEvent: _FertilizerEventStructModule

class _FertilizerEventList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> FertilizerEventReader: ...
        @override
        def __iter__(self) -> Iterator[FertilizerEventReader]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> FertilizerEventBuilder: ...
        @override
        def __setitem__(
            self,
            key: int,
            value: FertilizerEventReader | FertilizerEventBuilder | dict[str, Any],
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[FertilizerEventBuilder]: ...
        @override
        def init(
            self, index: int, size: int | None = None
        ) -> FertilizerEventBuilder: ...

class _EnvironmentModificationStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def date(self) -> DateReader: ...
        @property
        def codeCO2(self) -> str: ...
        @property
        def valueCO2(self) -> int: ...
        @property
        def notes(self) -> str: ...
        @property
        def experimentId(self) -> str: ...
        @property
        def treatmentId(self) -> str: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> EnvironmentModificationBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def date(self) -> DateBuilder: ...
        @date.setter
        def date(self, value: DateBuilder | DateReader | dict[str, Any]) -> None: ...
        @property
        def codeCO2(self) -> str: ...
        @codeCO2.setter
        def codeCO2(self, value: str) -> None: ...
        @property
        def valueCO2(self) -> int: ...
        @valueCO2.setter
        def valueCO2(self, value: int) -> None: ...
        @property
        def notes(self) -> str: ...
        @notes.setter
        def notes(self, value: str) -> None: ...
        @property
        def experimentId(self) -> str: ...
        @experimentId.setter
        def experimentId(self, value: str) -> None: ...
        @property
        def treatmentId(self) -> str: ...
        @treatmentId.setter
        def treatmentId(self, value: str) -> None: ...
        @override
        def init(
            self, field: Literal["date"], size: int | None = None
        ) -> DateBuilder: ...
        @override
        def as_reader(self) -> EnvironmentModificationReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        date: DateBuilder | dict[str, Any] | None = None,
        codeCO2: str | None = None,
        valueCO2: int | None = None,
        notes: str | None = None,
        experimentId: str | None = None,
        treatmentId: str | None = None,
        **kwargs: Any,
    ) -> EnvironmentModificationBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[EnvironmentModificationReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[EnvironmentModificationReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[EnvironmentModificationBuilder]: ...
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
    ) -> EnvironmentModificationReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> EnvironmentModificationReader: ...

EnvironmentModification: _EnvironmentModificationStructModule

class _EnvironmentModificationList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> EnvironmentModificationReader: ...
        @override
        def __iter__(self) -> Iterator[EnvironmentModificationReader]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> EnvironmentModificationBuilder: ...
        @override
        def __setitem__(
            self,
            key: int,
            value: EnvironmentModificationReader
            | EnvironmentModificationBuilder
            | dict[str, Any],
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[EnvironmentModificationBuilder]: ...
        @override
        def init(
            self, index: int, size: int | None = None
        ) -> EnvironmentModificationBuilder: ...

class _TreatmentStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def id(self) -> str: ...
        @property
        def field(self) -> FieldReader: ...
        @property
        def weatherStation(self) -> WeatherStationReader: ...
        @property
        def weatherStationTimeseries(
            self,
        ) -> _TimeSeriesInterfaceModule.TimeSeriesClient: ...
        @property
        def name(self) -> str: ...
        @property
        def simulationStartDate(self) -> DateReader: ...
        @property
        def simulationEndDate(self) -> DateReader: ...
        @property
        def irrigationApplied(self) -> bool: ...
        @property
        def fertilizerApplied(self) -> bool: ...
        @property
        def irrigationLevel(self) -> int: ...
        @property
        def fertilizerLevel(self) -> int: ...
        @property
        def plantingDateLevel(self) -> int: ...
        @property
        def environmentalModificationsLevel(self) -> int: ...
        @property
        def initialConditionsLevel(self) -> int: ...
        @property
        def plantingDensityLevel(self) -> int: ...
        @property
        def numberOfBlocksOrReplicates(self) -> int: ...
        @property
        def notes(self) -> str: ...
        @property
        def plots(self) -> PlotListReader: ...
        @property
        def residue(self) -> ResidueReader: ...
        @property
        def initialConditionsLayers(self) -> InitialConditionsLayerListReader: ...
        @property
        def plantingEvents(self) -> PlantingEventListReader: ...
        @property
        def harvestEvents(self) -> HarvestEventListReader: ...
        @property
        def irrigationEvents(self) -> IrrigationEventListReader: ...
        @property
        def fertilizerEvents(self) -> FertilizerEventListReader: ...
        @property
        def environmentModifications(self) -> EnvironmentModificationListReader: ...
        @property
        def experimentId(self) -> str: ...
        @property
        def fieldId(self) -> str: ...
        @property
        def weatherStationId(self) -> str: ...
        @property
        def weatherStationDataset(self) -> str: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> TreatmentBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def id(self) -> str: ...
        @id.setter
        def id(self, value: str) -> None: ...
        @property
        def field(self) -> FieldBuilder: ...
        @field.setter
        def field(self, value: FieldBuilder | FieldReader | dict[str, Any]) -> None: ...
        @property
        def weatherStation(self) -> WeatherStationBuilder: ...
        @weatherStation.setter
        def weatherStation(
            self, value: WeatherStationBuilder | WeatherStationReader | dict[str, Any]
        ) -> None: ...
        @property
        def weatherStationTimeseries(
            self,
        ) -> _TimeSeriesInterfaceModule.TimeSeriesClient: ...
        @weatherStationTimeseries.setter
        def weatherStationTimeseries(
            self,
            value: _TimeSeriesInterfaceModule.TimeSeriesClient
            | _TimeSeriesInterfaceModule.Server,
        ) -> None: ...
        @property
        def name(self) -> str: ...
        @name.setter
        def name(self, value: str) -> None: ...
        @property
        def simulationStartDate(self) -> DateBuilder: ...
        @simulationStartDate.setter
        def simulationStartDate(
            self, value: DateBuilder | DateReader | dict[str, Any]
        ) -> None: ...
        @property
        def simulationEndDate(self) -> DateBuilder: ...
        @simulationEndDate.setter
        def simulationEndDate(
            self, value: DateBuilder | DateReader | dict[str, Any]
        ) -> None: ...
        @property
        def irrigationApplied(self) -> bool: ...
        @irrigationApplied.setter
        def irrigationApplied(self, value: bool) -> None: ...
        @property
        def fertilizerApplied(self) -> bool: ...
        @fertilizerApplied.setter
        def fertilizerApplied(self, value: bool) -> None: ...
        @property
        def irrigationLevel(self) -> int: ...
        @irrigationLevel.setter
        def irrigationLevel(self, value: int) -> None: ...
        @property
        def fertilizerLevel(self) -> int: ...
        @fertilizerLevel.setter
        def fertilizerLevel(self, value: int) -> None: ...
        @property
        def plantingDateLevel(self) -> int: ...
        @plantingDateLevel.setter
        def plantingDateLevel(self, value: int) -> None: ...
        @property
        def environmentalModificationsLevel(self) -> int: ...
        @environmentalModificationsLevel.setter
        def environmentalModificationsLevel(self, value: int) -> None: ...
        @property
        def initialConditionsLevel(self) -> int: ...
        @initialConditionsLevel.setter
        def initialConditionsLevel(self, value: int) -> None: ...
        @property
        def plantingDensityLevel(self) -> int: ...
        @plantingDensityLevel.setter
        def plantingDensityLevel(self, value: int) -> None: ...
        @property
        def numberOfBlocksOrReplicates(self) -> int: ...
        @numberOfBlocksOrReplicates.setter
        def numberOfBlocksOrReplicates(self, value: int) -> None: ...
        @property
        def notes(self) -> str: ...
        @notes.setter
        def notes(self, value: str) -> None: ...
        @property
        def plots(self) -> PlotListBuilder: ...
        @plots.setter
        def plots(
            self, value: PlotListBuilder | PlotListReader | dict[str, Any]
        ) -> None: ...
        @property
        def residue(self) -> ResidueBuilder: ...
        @residue.setter
        def residue(
            self, value: ResidueBuilder | ResidueReader | dict[str, Any]
        ) -> None: ...
        @property
        def initialConditionsLayers(self) -> InitialConditionsLayerListBuilder: ...
        @initialConditionsLayers.setter
        def initialConditionsLayers(
            self,
            value: InitialConditionsLayerListBuilder
            | InitialConditionsLayerListReader
            | dict[str, Any],
        ) -> None: ...
        @property
        def plantingEvents(self) -> PlantingEventListBuilder: ...
        @plantingEvents.setter
        def plantingEvents(
            self,
            value: PlantingEventListBuilder | PlantingEventListReader | dict[str, Any],
        ) -> None: ...
        @property
        def harvestEvents(self) -> HarvestEventListBuilder: ...
        @harvestEvents.setter
        def harvestEvents(
            self,
            value: HarvestEventListBuilder | HarvestEventListReader | dict[str, Any],
        ) -> None: ...
        @property
        def irrigationEvents(self) -> IrrigationEventListBuilder: ...
        @irrigationEvents.setter
        def irrigationEvents(
            self,
            value: IrrigationEventListBuilder
            | IrrigationEventListReader
            | dict[str, Any],
        ) -> None: ...
        @property
        def fertilizerEvents(self) -> FertilizerEventListBuilder: ...
        @fertilizerEvents.setter
        def fertilizerEvents(
            self,
            value: FertilizerEventListBuilder
            | FertilizerEventListReader
            | dict[str, Any],
        ) -> None: ...
        @property
        def environmentModifications(self) -> EnvironmentModificationListBuilder: ...
        @environmentModifications.setter
        def environmentModifications(
            self,
            value: EnvironmentModificationListBuilder
            | EnvironmentModificationListReader
            | dict[str, Any],
        ) -> None: ...
        @property
        def experimentId(self) -> str: ...
        @experimentId.setter
        def experimentId(self, value: str) -> None: ...
        @property
        def fieldId(self) -> str: ...
        @fieldId.setter
        def fieldId(self, value: str) -> None: ...
        @property
        def weatherStationId(self) -> str: ...
        @weatherStationId.setter
        def weatherStationId(self, value: str) -> None: ...
        @property
        def weatherStationDataset(self) -> str: ...
        @weatherStationDataset.setter
        def weatherStationDataset(self, value: str) -> None: ...
        @override
        @overload
        def init(
            self, field: Literal["field"], size: int | None = None
        ) -> FieldBuilder: ...
        @overload
        def init(
            self, field: Literal["weatherStation"], size: int | None = None
        ) -> WeatherStationBuilder: ...
        @overload
        def init(
            self, field: Literal["simulationStartDate"], size: int | None = None
        ) -> DateBuilder: ...
        @overload
        def init(
            self, field: Literal["simulationEndDate"], size: int | None = None
        ) -> DateBuilder: ...
        @overload
        def init(
            self, field: Literal["residue"], size: int | None = None
        ) -> ResidueBuilder: ...
        @overload
        def init(
            self, field: Literal["plots"], size: int | None = None
        ) -> PlotListBuilder: ...
        @overload
        def init(
            self, field: Literal["initialConditionsLayers"], size: int | None = None
        ) -> InitialConditionsLayerListBuilder: ...
        @overload
        def init(
            self, field: Literal["plantingEvents"], size: int | None = None
        ) -> PlantingEventListBuilder: ...
        @overload
        def init(
            self, field: Literal["harvestEvents"], size: int | None = None
        ) -> HarvestEventListBuilder: ...
        @overload
        def init(
            self, field: Literal["irrigationEvents"], size: int | None = None
        ) -> IrrigationEventListBuilder: ...
        @overload
        def init(
            self, field: Literal["fertilizerEvents"], size: int | None = None
        ) -> FertilizerEventListBuilder: ...
        @overload
        def init(
            self, field: Literal["environmentModifications"], size: int | None = None
        ) -> EnvironmentModificationListBuilder: ...
        @overload
        def init(self, field: str, size: int | None = None) -> Any: ...
        @override
        def as_reader(self) -> TreatmentReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        id: str | None = None,
        field: FieldBuilder | dict[str, Any] | None = None,
        weatherStation: WeatherStationBuilder | dict[str, Any] | None = None,
        weatherStationTimeseries: _TimeSeriesInterfaceModule.TimeSeriesClient
        | _TimeSeriesInterfaceModule.Server
        | None = None,
        name: str | None = None,
        simulationStartDate: DateBuilder | dict[str, Any] | None = None,
        simulationEndDate: DateBuilder | dict[str, Any] | None = None,
        irrigationApplied: bool | None = None,
        fertilizerApplied: bool | None = None,
        irrigationLevel: int | None = None,
        fertilizerLevel: int | None = None,
        plantingDateLevel: int | None = None,
        environmentalModificationsLevel: int | None = None,
        initialConditionsLevel: int | None = None,
        plantingDensityLevel: int | None = None,
        numberOfBlocksOrReplicates: int | None = None,
        notes: str | None = None,
        plots: PlotListBuilder | dict[str, Any] | None = None,
        residue: ResidueBuilder | dict[str, Any] | None = None,
        initialConditionsLayers: InitialConditionsLayerListBuilder
        | dict[str, Any]
        | None = None,
        plantingEvents: PlantingEventListBuilder | dict[str, Any] | None = None,
        harvestEvents: HarvestEventListBuilder | dict[str, Any] | None = None,
        irrigationEvents: IrrigationEventListBuilder | dict[str, Any] | None = None,
        fertilizerEvents: FertilizerEventListBuilder | dict[str, Any] | None = None,
        environmentModifications: EnvironmentModificationListBuilder
        | dict[str, Any]
        | None = None,
        experimentId: str | None = None,
        fieldId: str | None = None,
        weatherStationId: str | None = None,
        weatherStationDataset: str | None = None,
        **kwargs: Any,
    ) -> TreatmentBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[TreatmentReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[TreatmentReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[TreatmentBuilder]: ...
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
    ) -> TreatmentReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> TreatmentReader: ...

Treatment: _TreatmentStructModule

class _TreatmentList:
    class Reader(_DynamicListReader):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> TreatmentReader: ...
        @override
        def __iter__(self) -> Iterator[TreatmentReader]: ...

    class Builder(_DynamicListBuilder):
        @override
        def __len__(self) -> int: ...
        @override
        def __getitem__(self, key: int) -> TreatmentBuilder: ...
        @override
        def __setitem__(
            self, key: int, value: TreatmentReader | TreatmentBuilder | dict[str, Any]
        ) -> None: ...
        @override
        def __iter__(self) -> Iterator[TreatmentBuilder]: ...
        @override
        def init(self, index: int, size: int | None = None) -> TreatmentBuilder: ...

class _ExperimentDescriptionStructModule(_StructModule):
    class Reader(_DynamicStructReader):
        @property
        def id(self) -> str: ...
        @property
        def suiteId(self) -> str: ...
        @property
        def name(self) -> str: ...
        @property
        def researchInfrastructureName(self) -> str: ...
        @property
        def instituteName(self) -> str: ...
        @property
        def researchUnitName(self) -> str: ...
        @property
        def experimentalFacilityName(self) -> str: ...
        @property
        def siteName(self) -> str: ...
        @property
        def siteType(self) -> str: ...
        @property
        def mainExperimentFactor(self) -> str: ...
        @property
        def experimentalFactorCombinations(self) -> str: ...
        @property
        def experimentType(self) -> str: ...
        @property
        def managementType(self) -> str: ...
        @property
        def croppingSystem(self) -> str: ...
        @property
        def plantingYear(self) -> int: ...
        @property
        def harvestOperationYear(self) -> int: ...
        @property
        def notes(self) -> str: ...
        @property
        def treatments(self) -> TreatmentListReader: ...
        @override
        def as_builder(
            self,
            num_first_segment_words: int | None = None,
            allocate_seg_callable: Callable[[int], bytearray] | None = None,
        ) -> ExperimentDescriptionBuilder: ...

    class Builder(_DynamicStructBuilder):
        @property
        def id(self) -> str: ...
        @id.setter
        def id(self, value: str) -> None: ...
        @property
        def suiteId(self) -> str: ...
        @suiteId.setter
        def suiteId(self, value: str) -> None: ...
        @property
        def name(self) -> str: ...
        @name.setter
        def name(self, value: str) -> None: ...
        @property
        def researchInfrastructureName(self) -> str: ...
        @researchInfrastructureName.setter
        def researchInfrastructureName(self, value: str) -> None: ...
        @property
        def instituteName(self) -> str: ...
        @instituteName.setter
        def instituteName(self, value: str) -> None: ...
        @property
        def researchUnitName(self) -> str: ...
        @researchUnitName.setter
        def researchUnitName(self, value: str) -> None: ...
        @property
        def experimentalFacilityName(self) -> str: ...
        @experimentalFacilityName.setter
        def experimentalFacilityName(self, value: str) -> None: ...
        @property
        def siteName(self) -> str: ...
        @siteName.setter
        def siteName(self, value: str) -> None: ...
        @property
        def siteType(self) -> str: ...
        @siteType.setter
        def siteType(self, value: str) -> None: ...
        @property
        def mainExperimentFactor(self) -> str: ...
        @mainExperimentFactor.setter
        def mainExperimentFactor(self, value: str) -> None: ...
        @property
        def experimentalFactorCombinations(self) -> str: ...
        @experimentalFactorCombinations.setter
        def experimentalFactorCombinations(self, value: str) -> None: ...
        @property
        def experimentType(self) -> str: ...
        @experimentType.setter
        def experimentType(self, value: str) -> None: ...
        @property
        def managementType(self) -> str: ...
        @managementType.setter
        def managementType(self, value: str) -> None: ...
        @property
        def croppingSystem(self) -> str: ...
        @croppingSystem.setter
        def croppingSystem(self, value: str) -> None: ...
        @property
        def plantingYear(self) -> int: ...
        @plantingYear.setter
        def plantingYear(self, value: int) -> None: ...
        @property
        def harvestOperationYear(self) -> int: ...
        @harvestOperationYear.setter
        def harvestOperationYear(self, value: int) -> None: ...
        @property
        def notes(self) -> str: ...
        @notes.setter
        def notes(self, value: str) -> None: ...
        @property
        def treatments(self) -> TreatmentListBuilder: ...
        @treatments.setter
        def treatments(
            self, value: TreatmentListBuilder | TreatmentListReader | dict[str, Any]
        ) -> None: ...
        @override
        def init(
            self, field: Literal["treatments"], size: int | None = None
        ) -> TreatmentListBuilder: ...
        @override
        def as_reader(self) -> ExperimentDescriptionReader: ...

    @override
    def new_message(
        self,
        num_first_segment_words: int | None = None,
        allocate_seg_callable: Callable[[int], bytearray] | None = None,
        id: str | None = None,
        suiteId: str | None = None,
        name: str | None = None,
        researchInfrastructureName: str | None = None,
        instituteName: str | None = None,
        researchUnitName: str | None = None,
        experimentalFacilityName: str | None = None,
        siteName: str | None = None,
        siteType: str | None = None,
        mainExperimentFactor: str | None = None,
        experimentalFactorCombinations: str | None = None,
        experimentType: str | None = None,
        managementType: str | None = None,
        croppingSystem: str | None = None,
        plantingYear: int | None = None,
        harvestOperationYear: int | None = None,
        notes: str | None = None,
        treatments: TreatmentListBuilder | dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> ExperimentDescriptionBuilder: ...
    @override
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> AbstractContextManager[ExperimentDescriptionReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[False],
    ) -> AbstractContextManager[ExperimentDescriptionReader]: ...
    @overload
    def from_bytes(
        self,
        buf: bytes,
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
        *,
        builder: Literal[True],
    ) -> AbstractContextManager[ExperimentDescriptionBuilder]: ...
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
    ) -> ExperimentDescriptionReader: ...
    @override
    def read_packed(
        self,
        file: IO[str] | IO[bytes],
        traversal_limit_in_words: int | None = None,
        nesting_limit: int | None = None,
    ) -> ExperimentDescriptionReader: ...

ExperimentDescription: _ExperimentDescriptionStructModule

# Top-level type aliases for use in type annotations
type CultivarBuilder = _CultivarStructModule.Builder
type CultivarReader = _CultivarStructModule.Reader
type EnvironmentModificationBuilder = _EnvironmentModificationStructModule.Builder
type EnvironmentModificationListBuilder = _EnvironmentModificationList.Builder
type EnvironmentModificationListReader = _EnvironmentModificationList.Reader
type EnvironmentModificationReader = _EnvironmentModificationStructModule.Reader
type ExperimentDescriptionBuilder = _ExperimentDescriptionStructModule.Builder
type ExperimentDescriptionReader = _ExperimentDescriptionStructModule.Reader
type FertilizerEventBuilder = _FertilizerEventStructModule.Builder
type FertilizerEventListBuilder = _FertilizerEventList.Builder
type FertilizerEventListReader = _FertilizerEventList.Reader
type FertilizerEventReader = _FertilizerEventStructModule.Reader
type FieldBuilder = _FieldStructModule.Builder
type FieldReader = _FieldStructModule.Reader
type HarvestEventBuilder = _HarvestEventStructModule.Builder
type HarvestEventListBuilder = _HarvestEventList.Builder
type HarvestEventListReader = _HarvestEventList.Reader
type HarvestEventReader = _HarvestEventStructModule.Reader
type InitialConditionsLayerBuilder = _InitialConditionsLayerStructModule.Builder
type InitialConditionsLayerListBuilder = _InitialConditionsLayerList.Builder
type InitialConditionsLayerListReader = _InitialConditionsLayerList.Reader
type InitialConditionsLayerReader = _InitialConditionsLayerStructModule.Reader
type IrrigationEventBuilder = _IrrigationEventStructModule.Builder
type IrrigationEventListBuilder = _IrrigationEventList.Builder
type IrrigationEventListReader = _IrrigationEventList.Reader
type IrrigationEventReader = _IrrigationEventStructModule.Reader
type PlantingEventBuilder = _PlantingEventStructModule.Builder
type PlantingEventListBuilder = _PlantingEventList.Builder
type PlantingEventListReader = _PlantingEventList.Reader
type PlantingEventReader = _PlantingEventStructModule.Reader
type PlotBuilder = _PlotStructModule.Builder
type PlotListBuilder = _PlotList.Builder
type PlotListReader = _PlotList.Reader
type PlotReader = _PlotStructModule.Reader
type ResidueBuilder = _ResidueStructModule.Builder
type ResidueReader = _ResidueStructModule.Reader
type SoilMetadataBuilder = _SoilMetadataStructModule.Builder
type SoilMetadataReader = _SoilMetadataStructModule.Reader
type TreatmentBuilder = _TreatmentStructModule.Builder
type TreatmentListBuilder = _TreatmentList.Builder
type TreatmentListReader = _TreatmentList.Reader
type TreatmentReader = _TreatmentStructModule.Reader
type WeatherStationBuilder = _WeatherStationStructModule.Builder
type WeatherStationReader = _WeatherStationStructModule.Reader
