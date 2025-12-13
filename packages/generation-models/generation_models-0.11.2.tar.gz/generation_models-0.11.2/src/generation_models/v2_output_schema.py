from __future__ import annotations
import typing as t
from pydantic import BaseModel, field_validator
from .unit_types import kW, V, dec, Wm2, deg, degC, kWh, Whm2, m2
from .generation_models import SolarResource
from .v0_output_schema import MarketAwardsTimeSeries, OptimizerTimeSeries, StandaloneStorageModelSimpleResults
import numpy as np


class BaseTimeSeries(BaseModel):
    r""":meta private:"""

    def default_include(self):
        r""":meta private:"""
        return {k: True for k in self.model_json_schema()["required"]}

    @field_validator("*", mode="after")
    @classmethod
    def is_finite(cls, value: list[float]) -> list[float]:
        if isinstance(value, list) and not np.isfinite(np.array(value)).all():
            raise ValueError("Time series can only contain finite values")
        return value


class BusTimeSeries(BaseTimeSeries):
    r"""-"""

    power: t.List[kW]


class DCBusTimeSeries(BusTimeSeries):
    r"""-"""

    voltage: t.List[V]


class InverterTimeSeries(BaseTimeSeries):
    r"""-"""

    clipping_loss: t.List[kW]

    efficiency: t.List[dec]

    tare_loss: t.List[kW]

    consumption_loss: t.List[kW]


class TransformerTimeSeries(BaseTimeSeries):
    r"""-"""

    total_loss: t.List[kW]

    load_loss: t.Optional[t.List[kW]] = None

    no_load_loss: t.Optional[t.List[kW]] = None


class ACWiringTimeSeries(BaseTimeSeries):
    r"""-"""

    loss: t.List[kW]


class TransmissionTimeSeries(BaseTimeSeries):
    r"""-"""

    loss: t.List[kW]


class POITimeSeries(BaseTimeSeries):
    r"""-"""

    power_pre_clip: t.List[kW]

    power_pre_adjustment: t.List[kW]

    power: t.List[kW]

    power_positive: t.List[kW]

    power_negative: t.List[kW]


class PVTimeSeries(BaseTimeSeries):
    r"""-"""

    ghi: t.List[Wm2]

    tracker_rotation_angle: t.Optional[t.List[deg]] = None

    front_poa_nominal: t.Optional[t.List[Wm2]] = None

    front_poa_shaded: t.Optional[t.List[Wm2]] = None

    front_poa_shaded_soiled: t.Optional[t.List[Wm2]] = None

    front_poa: t.List[Wm2]

    rear_poa: t.List[Wm2]

    poa_effective: t.List[Wm2]

    poa_effective_power: t.Optional[t.List[kW]] = None

    cell_temperature_quasi_steady: t.Optional[t.List[degC]] = None

    cell_temperature: t.Optional[t.List[degC]] = None

    module_efficiency: t.Optional[t.List[dec]] = None

    dc_shading_loss: t.Optional[t.List[kW]] = None

    dc_snow_loss: t.Optional[t.List[kW]] = None

    mppt_window_loss: t.Optional[t.List[kW]] = None

    gross_dc_power: t.List[kW]

    dc_power_undegraded: t.Optional[t.List[kW]] = None

    dc_power: t.Optional[t.List[kW]] = None

    dc_voltage: t.Optional[t.List[V]] = None


class BESSTimeSeries(BaseTimeSeries):
    r"""-"""

    internal_energy: t.List[kWh]

    internal_energy_max: t.List[kWh]

    limit: t.List[kW]

    output: t.List[kW]


class CoupledBESSTimeSeries(BESSTimeSeries):
    r"""-"""

    excess_power_at_coupling: t.List[kW]

    captured_excess_at_coupling: t.List[kW]


class BESSHVACTimeSeries(BaseTimeSeries):
    r"""-"""

    loss: t.List[kW]


class PowerFlowTimeSeries(BaseModel):
    r""":meta private:"""

    dc_bus: t.Optional[DCBusTimeSeries] = None

    inverter: t.Optional[InverterTimeSeries] = None

    lv_bus: t.Optional[BusTimeSeries] = None

    mv_xfmr: t.Optional[TransformerTimeSeries] = None

    mv_bus: t.Optional[BusTimeSeries] = None

    ac_wiring: t.Optional[ACWiringTimeSeries] = None

    hv_xfmr: t.Optional[TransformerTimeSeries] = None

    export_bus: BusTimeSeries

    transmission: TransmissionTimeSeries

    poi: POITimeSeries

    def default_include(self):
        r""":meta private:"""
        return {k: getattr(self, k).default_include() for k in self.model_dump(exclude_none=True).keys()}


class Year1Waterfall(BaseModel):
    r""":meta private:"""

    dc_bus_energy: t.Optional[kWh] = None
    inverter_clipping: t.Optional[dec] = None
    inverter_consumption: t.Optional[dec] = None
    inverter_tare: t.Optional[dec] = None
    inverter_efficiency: t.Optional[dec] = None
    lv_bus_energy: t.Optional[kWh] = None
    mv_transformer: t.Optional[dec] = None
    mv_bus_energy: t.Optional[kWh] = None
    ac_wiring: t.Optional[dec] = None
    hv_transformer: t.Optional[dec] = None
    export_bus_energy: kWh
    transmission: dec
    poi_clipping: dec
    poi_adjustment: dec
    poi_energy: kWh

    @field_validator("*", mode="after")
    @classmethod
    def is_finite(cls, value: float) -> float:
        if not np.isfinite(value):
            raise ValueError("Waterfall values must be finite")
        return value


class GenerationPowerFlowTimeSeries(PowerFlowTimeSeries):
    r"""-"""

    pv: t.Optional[PVTimeSeries] = None


class GenerationYear1Waterfall(Year1Waterfall):
    r"""-"""

    ghi: t.Optional[Whm2] = None
    front_transposition: t.Optional[dec] = None
    front_shading: t.Optional[dec] = None
    front_soiling: t.Optional[dec] = None
    front_iam: t.Optional[dec] = None
    rear_poa: t.Optional[dec] = None
    rear_bifaciality: t.Optional[dec] = None
    poa_effective: t.Optional[Whm2] = None
    array_area: t.Optional[m2] = None
    poa_effective_energy: t.Optional[kWh] = None
    stc_pv_module_effeciency: t.Optional[dec] = None
    pv_dc_nominal_energy: t.Optional[kWh] = None
    non_stc_irradiance_temperature: t.Optional[dec] = None
    r"""this includes DC derate due to beam shading (electrical effect), will be broken out in the future"""
    mppt_clip: t.Optional[dec] = None
    snow: t.Optional[dec] = None
    pv_dc_gross_energy: t.Optional[kWh] = None
    nameplate: t.Optional[dec] = None
    lid: t.Optional[dec] = None
    mismatch: t.Optional[dec] = None
    diodes: t.Optional[dec] = None
    dc_optimizer: t.Optional[dec] = None
    tracking_error: t.Optional[dec] = None
    dc_wiring: t.Optional[dec] = None
    dc_adjustment: t.Optional[dec] = None


class StandalonePowerFlowTimesSeries(PowerFlowTimeSeries):
    r"""-"""

    bess: BESSTimeSeries

    bess_hvac: t.Optional[BESSHVACTimeSeries] = None


class StandaloneYear1Waterfall(Year1Waterfall):
    r"""-"""

    bess_efficiency: dec

    bess_hvac: t.Optional[dec] = None


class HybridPowerFlowTimeSeries(GenerationPowerFlowTimeSeries, StandalonePowerFlowTimesSeries):
    r"""-"""

    bess: CoupledBESSTimeSeries


class HybridYear1Waterfall(GenerationYear1Waterfall, StandaloneYear1Waterfall):
    r"""-"""

    excess_power_at_coupling: dec

    captured_excess_at_coupling: dec

    bess_efficiency_generation: dec


class BasePowerFlowModelResults(BaseModel):
    r""":meta private:"""

    power_flow: PowerFlowTimeSeries

    def default_dict(self):
        r""":meta private:"""
        inc = {k: True for k in self.model_json_schema()["required"]}
        inc["power_flow"] = self.power_flow.default_include()
        return self.model_dump(exclude_none=True, include=inc)


class GenerationModelResults(BasePowerFlowModelResults):
    r"""Results schema returned when a
    :class:`~generation_models.generation_models.PVGenerationModel`,
    :class:`~generation_models.generation_models.ACExternalGenerationModel` or
    :class:`~generation_models.generation_models.DCExternalGenerationModel` simulation is run"""

    power_flow: GenerationPowerFlowTimeSeries

    waterfall: GenerationYear1Waterfall

    warnings: t.Optional[t.List[str]] = None

    sam_raw: t.Optional[dict] = None

    solar_resource: t.Optional[SolarResource] = None

    def default_dict(self):
        dd = super().default_dict()
        dd["warnings"] = self.warnings
        return dd


class StandaloneModelResults(BasePowerFlowModelResults):
    r"""Results schema returned when a
    :class:`~generation_models.generation_models.StandaloneStorageModel` simulation is run with a
    :attr:`~generation_models.generation_models.StandaloneStorageModel.downstream_system` specified"""

    power_flow: StandalonePowerFlowTimesSeries

    waterfall: StandaloneYear1Waterfall

    market_awards: MarketAwardsTimeSeries

    warnings: t.List[str]

    optimizer: t.Optional[OptimizerTimeSeries] = None
    r""":meta private:"""


class HybridModelResults(BasePowerFlowModelResults):
    r"""Results schema returned when a
    :class:`~generation_models.generation_models.PVStorageModel` simulation is run"""

    power_flow: HybridPowerFlowTimeSeries

    waterfall: HybridYear1Waterfall

    market_awards: MarketAwardsTimeSeries

    warnings: t.List[str]

    optimizer: t.Optional[OptimizerTimeSeries] = None
    r""":meta private:"""

    solar_only: t.Optional[GenerationModelResults] = None


model_results_map = {
    "generation": GenerationModelResults,
    "hybrid": HybridModelResults,
    "standalone": StandaloneModelResults,
    "standalone_simple": StandaloneStorageModelSimpleResults,
}
