from __future__ import annotations

import json
from enum import Enum

import pandas as pd
from pydantic import (
    field_validator,
    model_validator,
    ConfigDict,
    BaseModel,
    ValidationError,
    Field,
    conlist,
    TypeAdapter,
)
from pydantic.functional_validators import BeforeValidator
import typing as t
from typing import Optional

from pydantic_core.core_schema import ValidationInfo
from typing_extensions import Annotated, TypeAlias
from typing import List

from warnings import warn
import os

RAISE_DEPRECATION_WARNING = {"true": True, "false": False}[os.getenv("RAISE_DEPRECATION_WARNING", "false").lower()]


T = t.TypeVar("T")


def create_optionally_discriminant_union(union: T, discriminator: str) -> T:
    def allow_missing_discriminator(v):
        if discriminator not in v:
            return TypeAdapter(union).validate_python(v)
        return v

    return Annotated[
        union,
        Field(discriminator=discriminator),
        BeforeValidator(allow_missing_discriminator),
    ]


def get_deprecator(msg: str) -> BeforeValidator:
    """Use this in an Annotated type to trigger a DeprecationWarning when a deprecated field is passed explicitly.

    :meta private:
    """

    def warn_deprecation_on_instantiation(v: T, info: ValidationInfo) -> T:
        message = f"`{info.field_name}` is deprecated. " + msg
        if RAISE_DEPRECATION_WARNING:
            raise DeprecationWarning(message)
        warn(message, category=DeprecationWarning)
        return v

    return BeforeValidator(warn_deprecation_on_instantiation)


class SolverConfig(BaseModel):
    r"""Parameters that control optimization solver operation

    :meta private:
    """

    time_limit: Annotated[float, Field(ge=0.0)] = 8.0
    r"""time limit applied to solution of a single optimization window

    - Units: seconds
    - Example: 8 for 8s
    """

    mip_gap_rel_tolerance: Annotated[float, Field(ge=0.0)] = 0.0
    r"""relative difference between MIP best integer solution and optimal solution

    For example, to instruct Tyba to stop as soon as it has found a feasible integer solution
    proven to be within five percent of optimal, set the initial_mip_gap_tolerance to 0.05

    - Units: fraction
    - Example: 0.05 for 5% MIP gap tolerance
    """

    mip_gap_abs_tolerance: Annotated[float, Field(ge=0.0)] = 0.0
    r"""absolute difference between MIP best integer solution and optimal solution
    """

    verbose: bool = False
    r"""controls verbosity of solver output"""

    presolve: bool = True
    r"""controls whether the solver applies presolve techniques before optimization"""


class StrictSolverConfig(SolverConfig):

    time_limit: Annotated[float, Field(ge=0.0, le=20.0)] = 8.0


class StorageCoupling(str, Enum):
    r"""Enum class for selecting coupling bus for hybrid systems"""

    ac = "ac"
    r"""indicates the BESS and generator are coupled at the medium voltage AC bus"""
    dc = "dc"
    r"""indicates the BESS and generator are coupled together at the DC inputs of the generator inverter"""
    hv_ac = "hv_ac"
    r"""indicates the BESS and generator are coupled at the high voltage AC bus, e.g. the outlet of the 
    GSU/substation"""


class SingleAxisTracking(BaseModel):
    r"""N-S oriented single axis tracker model"""

    tracking_type: t.Literal["SAT"] = "SAT"
    r"""Used by the API for model-type discrimination, can be ignored
    """

    rotation_limit: float = 45.0
    r"""The limit of rotation angle for a single axis tracker. Assumed to be symmetric around 0\ |degrees|
    (tracker horizontal) 

    - Unit: degrees
    - Example: 45 for range of +45\ |degrees| to -45\ |degrees|  
    
    .. |degrees| unicode:: U+00B0
    """

    backtrack: bool = True
    r"""Backtracking eliminates shading between rows of single-axis-tracking arrays (within the :attr:`rotation_limit`)
    by altering the rotation angle of the tracker.

    - Format as a Boolean
    - Example: True to enable backtracking
    """


class FixedTilt(BaseModel):
    r"""Fixed tilt array model"""

    tracking_type: t.Literal["FT"] = "FT"
    r"""Used by the API for model-type discrimination, can be ignored"""
    tilt: float
    r"""The angle of orientation for a fixed tilt array relative to horizontal, with positive angles tilting the array
    towards the azimuth and negative angles tilting it away.

    - Unit: degrees
    - Example: 30 for 30\ |degrees|
    """


TrackingTypes = create_optionally_discriminant_union(
    t.Union[FixedTilt, SingleAxisTracking], discriminator="tracking_type"
)


class ScalarUtilization(BaseModel):
    r"""The quantity of an Ancillary Services capacity award that is dispatched by the grid operator.

    Most operators require sufficient State of Charge to meet AS obligations throughout the day, however the amount
    that a system gets dispatched is unknown in advance. To account for this, we allow you to model a range of
    uncertainty using the following parameters and ensure State of Charge feasibility over an entire horizon.
    Please contact us with further questions on this concept (more detailed explanations coming soon).

    The ScalarUtilization class applies a single uncertainty range for the entire simulation. This is useful for
    scenarios where more detailed utilization information isn't available or accurate. For example, applying historical
    utilization averages to a forecast simulation. To be able to apply utilization ranges as a time series, use
    :class:`TimeSeriesUtilization`
    """

    actual: float
    r"""The modeled dispatched capacity for the base case analysis. 

    - Units: fraction of capacity award for the specific service
    - Example values: 0.20 (20%) for regulation markets, 0.05 (5%) for reserves markets
    """
    lower: float
    r"""The lower bound dispatched capacity.

    - Units: fraction of capacity award for the specific service
    - Example values: 0.0 indicating no operations 
    """
    upper: float
    r"""The upper bound dispatched capacity.

    - Units: fraction of capacity award for the specific service
    - Example values: 1.0 (100%) indicating that sufficient state of charge needs to be reserved to meet
      full capacity award.
    """

    @field_validator("actual", "lower", "upper")
    @classmethod
    def between_0_and_1(cls, v: float):
        assert 0 <= v <= 1, "must be between 0 and 1"
        return v

    @model_validator(mode="after")
    def check_ordering(self: ScalarUtilization):
        assert self.lower <= self.actual, "lower must be less than or equal to actual utilization"
        assert self.actual <= self.upper, "actual must be less than or equal to upper utilization"
        return self


def _check_lengths(strs_lists: t.Dict[str, list]):
    str1 = next(iter(strs_lists.keys()))
    len1 = len(next(iter(strs_lists.values())))
    for k, v in strs_lists.items():
        assert len(v) == len1, f"{str1} and {k} must be the same length"


class TimeSeriesUtilization(BaseModel):
    r"""The quantity of an Ancillary Services capacity award that is dispatched by the grid operator.

    The TimeSeriesUtilization class applies a unique utilization scenario to each reserve market time interval.
    This is useful for scenarios with corresponding price and utilization, or when you want to be able to vary the
    utilization over time.

    For more information on utilization generally, see the :class:`ScalarUtilization` docs
    """

    actual: t.List[float]
    r"""The modeled dispatched capacity for the base case analysis. 

    - Units: fraction of capacity award for the specific service
    - Example values: 0.20 (20%) for regulation markets, 0.05 (5%) for reserves markets
    """
    lower: t.List[float]
    r"""The lower bound dispatched capacity.

    - Units: fraction of capacity award for the specific service
    - Example values: 0.0 indicating no operations
    """
    upper: t.List[float]
    r"""The upper bound dispatched capacity.

    - Units: fraction of capacity award for the specific service
    - Example values: 1.0 (100%) indicating that sufficient state of charge needs to be reserved to meet
      full capacity award.
    """

    @field_validator("actual", "lower", "upper")
    @classmethod
    def between_0_and_1(cls, vs: t.List[float]) -> t.List[float]:
        assert all(0 <= v <= 1 for v in vs), "must be between 0 and 1"
        return vs

    @model_validator(mode="after")
    def check_ordering(self: TimeSeriesUtilization):
        df = pd.DataFrame(self.model_dump())
        assert (df["lower"] <= df["actual"]).all(), "lower must be less than or equal to actual utilization"
        assert (df["actual"] <= df["upper"]).all(), "actual must be less than or equal to upper utilization"
        return self

    @model_validator(mode="after")
    def check_length(self: TimeSeriesUtilization):
        _check_lengths({"actual": self.actual, "lower": self.lower, "upper": self.upper})
        return self

    def __len__(self) -> int:
        return len(self.actual)


class BaseReserveMarket(BaseModel):
    price: t.List[float]
    r"""The capacity prices for this specific service. Used in dispatch co-optimization. Assumed to be hourly. The
    list length must be equivalent to the hourly sum of all battery terms.

    - Units: $/MW
    - Values length: if the project is a 1-year project, the list must be 8760-values long
    """
    deployment_price: t.Optional[t.List[float]] = None
    r"""The deployment/utilization prices for this specific service. This is the price paid for actual deployment
    (called/utilized energy), separate from the capacity price. If specified, deployment revenue replaces RTM 
    settlement for the deployed portion. Unlike :attr:`price`, this follows real-time market granularity (typically
    5-minute intervals), not hourly. The list length must match the RTM price length.

    - Units: $/MWh
    - Values length: must match RTM price length (e.g., 288 values for a 24-hour day with 5-minute intervals)
    """
    offer_cap: t.Union[float, t.List[float]]
    r"""The maximum storage capacity that can be bid for this specific service in each interval. Specific offer values
    will be allocated by the dispatch optimization algorithm. Can be a single float (applied to all intervals) or a
    time series list (assumed to be hourly). If a list, the length must match the price length.

    - Units: kW
    - Maximum value: 200% of nameplate power
    """
    obligation: t.Optional[t.List[float]] = None
    r"""Time series of already-cleared reserve market obligations. If provided, reserve markets participation is treated
    as a constraint on real-time market participation, instead of reserve market participation being co-optimized. 
    
    - Assumed to be hourly
    - Must have same length as :attr:`price`
    - Positive-only values
    - Units: kW
    """

    @model_validator(mode="after")
    def check_obligation_length(self):
        if self.obligation:
            _check_lengths({"price": self.price, "obligation": self.obligation})
        if isinstance(self.offer_cap, list):
            _check_lengths({"price": self.price, "offer_cap": self.offer_cap})
        return self

    def __len__(self) -> int:
        return len(self.price)


class ReserveMarket(BaseReserveMarket):
    r"""General class for different types of Ancillary Services.

    This will be a dictionary item in either the :attr:`~ReserveMarkets.up` or :attr:`~ReserveMarkets.down` field of
    :class:`ReserveMarkets` depending on the service.
    """

    utilization: t.Union[ScalarUtilization, TimeSeriesUtilization]
    r"""Sub-model to account for utilization uncertainty. See :class:`ScalarUtilization`. If using
    :class:`TimeSeriesUtilization`, must be same length as :attr:`price`.
    """
    duration_requirement: float = Field(0.0, description="market requirement for offer duration (hours)")
    r"""The duration for which a reserve offer must be sustainable, given a BESS’s SOE. For example, for a
    duration_requirement of 1 hour, a 10MW / 2hr battery with a current SOE of 5MWh would only be allowed to offer
    5MW to the reg-up market, as this is the output it could sustain for 1 hour. This only applies to “up” markets.

    - Units: hours
    - Default: 0 hours
    - Recommended values:
      - ERCOT reg-up: 1 hour
      - ERCOT reserves (RRS): 1 hour
    """

    @model_validator(mode="after")
    def check_length(self: ReserveMarket):
        if isinstance(self.utilization, TimeSeriesUtilization):
            _check_lengths({"price": self.price, "utilization": self.utilization})
        if self.obligation:
            _check_lengths({"price": self.price, "obligation": self.obligation})
        return self


class SymmetricReserveMarket(BaseReserveMarket):
    """Convenience interface that immediately gets broken up into two ReserveMarkets constrained to be symmetric."""

    up_utilization: t.Union[ScalarUtilization, TimeSeriesUtilization]
    down_utilization: t.Union[ScalarUtilization, TimeSeriesUtilization]
    up_duration_requirement: float = 0.0
    down_duration_requirement: float = 0.0

    @model_validator(mode="after")
    def check_utilization_length(self):
        if isinstance(self.up_utilization, TimeSeriesUtilization):
            _check_lengths({"price": self.price, "up_utilization": self.up_utilization})
        if isinstance(self.down_utilization, TimeSeriesUtilization):
            _check_lengths({"price": self.price, "down_utilization": self.down_utilization})
        return self


class ReserveMarkets(BaseModel):
    r"""Container for holding ancillary/reserve market inputs"""

    up: t.Dict[str, ReserveMarket] = {}
    r"""dictionary of reserve markets, where each key is the market name and the corresponding value is the
    :class:`ReserveMarket` object.
    
    For example:
    
    .. code-block:: python

        {
            'reg_up': ReserveMarket(...),
            'rrs': ReserveMarket(...)
        }
    """
    down: t.Dict[str, ReserveMarket] = {}
    r"""dictionary of reserve markets, where each key is the market name and the corresponding value is the
        :class:`ReserveMarket` object. See :attr:`up` for example
    """

    symmetric: t.Dict[str, SymmetricReserveMarket] = {}
    r"""dictionary of symmetric reserve markets, where each key is the market name and the corresponding value is the
        :class:`SymmetricReserveMarket` object.
        
    For example:
    
    .. code-block:: python

        {
            'reg': SymmetricReserveMarket(...),
        }
    """

    @model_validator(mode="after")
    def check_length(self: ReserveMarkets):
        assert (
            len(set(map(len, (self.up | self.down | self.symmetric).values()))) == 1
        ), "all reserve markets must contain data of the same length"
        return self

    @model_validator(mode="after")
    def check_consistent_utilization_types(self: ReserveMarkets):
        utilization_types = set(type(m.utilization) for m in (self.up | self.down).values())
        for m in self.symmetric.values():
            utilization_types.update({type(m.up_utilization), type(m.down_utilization)})
        assert len(utilization_types) == 1, f"""
            Only one utilization format may be provided across reserve markets, got {utilization_types}.
        """
        return self

    def __len__(self) -> int:
        return len(next(iter((self.up | self.down | self.symmetric).values())))


class DARTPrices(BaseModel):
    r"""Energy prices used for the energy arbitrage application."""

    rtm: conlist(float, min_length=1)
    r"""Real-time market prices. Prices correspond to the time interval given by
    :attr:`PVStorageModel.time_interval_mins` or :attr:`StandaloneStorageModel.time_interval_mins`.
    The list length must match the sum of all battery terms when given in the chosen time interval.
        
    - For example: if the project has 2 batteries, each with a 1-year term, and the chosen interval is 15min,
      the list must be (2 battery years) * (8760*4 intervals per year) = 70080 values long
    """
    dam: conlist(float, min_length=1)
    r"""Hourly Day-Ahead prices. The list length must match the hourly sum of all battery terms.
        
    - For example: if the project is a 1-year, hourly project, the list must be 8760-values long
    """
    imbalance: t.Optional[conlist(float, min_length=1)] = None
    r"""Imbalance market or payment prices. Intended for modeling e.g. ERCOT's Real Time On-line Reserve Price Adder
    (RTORPA). Prices correspond to the time interval given by :attr:`PVStorageModel.time_interval_mins` or
    :attr:`StandaloneStorageModel.time_interval_mins` and list length must match :attr:`rtm`
    """


def _check_time_interval(sub_hourly, hourly, time_interval_mins, subhourly_str, hourly_str):
    rt_intervals_per_hour, err = divmod(len(sub_hourly), len(hourly))
    assert err == 0, f"length of {hourly_str} must divide length of {subhourly_str}"
    assert (
        60 / rt_intervals_per_hour == time_interval_mins
    ), f"lengths of {subhourly_str} and {hourly_str} must reflect time_interval_mins"


class DARTPriceScenarios(BaseModel):
    r""":meta private:"""

    # TODO: Still want docstrings for devs at some point
    rtm: Annotated[List[Annotated[List[float], Field(min_length=1)]], Field(min_length=1)]
    dam: Annotated[List[Annotated[List[float], Field(min_length=1)]], Field(min_length=1)]
    weights: t.List[float]

    @model_validator(mode="after")
    def check_lengths(self):
        assert len(self.dam) == len(self.rtm) == len(self.weights)
        return self

    def __len__(self):
        return len(self.rtm[0])


class MarketBase(BaseModel):
    r"""Base class for Model classes with market-based optimization

    :meta private:
    """

    energy_prices: t.Union[DARTPrices, t.List[float], DARTPriceScenarios]
    r"""The energy prices used for storage dispatch optimization. This can either be a single energy price timeseries or
    two energy price timeseries (i.e corresponding to DA & RT markets):

    - Single energy market timeseries: Provide a list of prices. Prices correspond to the time interval given by
      :attr:`time_interval_mins`. The list length must match the sum of all battery terms when given in the chosen
      time interval. For example: if the project is a 1-year, hourly project, the list should be 8760 values long.
      A half-year term modeled with a time interval of 15 minutes, requires a list of 17520 energy prices.
    - Two energy market timeseries: Provide a :class:`DARTPrices` object
    """
    storage_inputs: MultiStorageInputs
    r"""Submodel for BESS design, market participation and optimization"""
    reserve_markets: t.Optional[ReserveMarkets] = None
    r"""A sub-model to handle the specification of reserve market/ancillary market inputs.
    """
    total_up_offer_cap: Annotated[t.Optional[float], Field(gt=0)] = None
    r"""Maximum total capacity that can be offered across all upward reserve/ancillary markets combined.
    
    This constraint applies to the sum of all upward reserve market offers (e.g., regulation up, spinning reserves, 
    non-spinning reserves).
    
    - Units: kW
    """
    total_down_offer_cap: Annotated[t.Optional[float], Field(gt=0)] = None
    r"""Maximum total capacity that can be offered across all downward reserve/ancillary markets combined.
    
    This constraint applies to the sum of all downward reserve market offers (e.g., regulation down). 
    
    - Units: kW
    """
    time_interval_mins: int = 60
    r"""The number of minutes per real-time market interval.

    - Use 60 for an hourly run
    - Use 5 for a five-minute run

    Note: :attr:`StorageSolverOptions.window` and :attr:`StorageSolverOptions.step` values will adjust accordingly
    """
    load_peak_reduction: t.Optional[LoadPeakReduction] = None
    r"""A sub-model to handle the specification of load reduction inputs
    """
    dam_award: t.Optional[t.List[float]] = None
    r"""List of system dispatch values awarded in the day ahead market. These values are used when re-optimizing
    real-time market operations.
    
    - Units are kW
    - Positive values represent system export
    - Time interval is assumed to be hourly corresponding with Day Ahead market 
    
    :meta private:
    """

    @model_validator(mode="after")
    def validate_dam_award(self):
        if self.dam_award is not None:
            assert isinstance(
                self.energy_prices, (DARTPrices, DARTPriceScenarios)
            ), "When providing a dam_award, separate DAM and RTM prices are required."
            if isinstance(self.energy_prices, DARTPriceScenarios):
                rtm_prices = self.energy_prices.rtm[0]
            else:
                rtm_prices = self.energy_prices.rtm
            _check_time_interval(
                sub_hourly=rtm_prices,
                hourly=self.dam_award,
                time_interval_mins=self.time_interval_mins,
                subhourly_str="rtm prices",
                hourly_str="dam awards",
            )
        return self

    @model_validator(mode="after")
    def check_time_interval(self):
        if isinstance(self.energy_prices, DARTPrices):
            _check_time_interval(
                self.energy_prices.rtm,
                self.energy_prices.dam,
                self.time_interval_mins,
                "rtm prices",
                "dam prices",
            )
        return self

    @model_validator(mode="after")
    def check_length(self):
        if self.reserve_markets:
            if isinstance(self.energy_prices, DARTPriceScenarios):
                dam_prices = self.energy_prices.dam[0]
                rtm_prices = self.energy_prices.rtm[0]
            elif isinstance(self.energy_prices, DARTPrices):
                dam_prices = self.energy_prices.dam
                rtm_prices = self.energy_prices.rtm
            else:
                # Single energy price list - use it for both
                dam_prices = self.energy_prices
                rtm_prices = self.energy_prices

            _check_lengths(
                {
                    "dam prices": dam_prices,
                    "reserve market data": self.reserve_markets,
                }
            )

            # Check deployment_price lengths match RTM prices
            for market_dict in [self.reserve_markets.up, self.reserve_markets.down]:
                if market_dict:
                    for market_name, market in market_dict.items():
                        if market.deployment_price is not None:
                            _check_lengths(
                                {
                                    "rtm prices": rtm_prices,
                                    f"deployment_price for {market_name}": market.deployment_price,
                                }
                            )

        if self.load_peak_reduction:
            if isinstance(self.energy_prices, DARTPrices):
                rtm = self.energy_prices.rtm
            elif isinstance(self.energy_prices, DARTPriceScenarios):
                rtm = self.energy_prices.rtm[0]
            else:
                rtm = self.energy_prices
            _check_lengths({"rtm prices": rtm, "peak reduction data": self.load_peak_reduction})
        return self

    @model_validator(mode="after")
    def check_symmetric_reserves_usage(self):
        if self.reserve_markets and self.reserve_markets.symmetric:
            assert (
                self.storage_inputs.symmetric_reg is None
            ), "Cannot use both symmetric_reg=True and symmetric reserve markets. Use SymmetricReserveMarket instead of symmetric_reg."
        return self


class SolarResourceTimeSeries(BaseModel):
    r"""Irradiance and environmental time series data

    - The interval for all time series is assumed to match :attr:`PVGenerationModel.time_interval_mins`.
    - All time-series must be the same length.
    - For sub-hourly data, the timestamp represented by the :attr:`year`, :attr:`month`, :attr:`day`, :attr:`hour` and
      :attr:`minute` attributes represents the beginning of the time interval, as well as the time to be used for sun
      position calculations. For hourly data, the beginning of the time interval is given by :attr:`hour`.
      :attr:`minute` indicates the point within the interval to be used for determining sun position.
    - The irradiance and weather values represent average values across the interval. Timestamps are assumed to be in
      local *standard* time and should not consider Daylight Savings Time or include leap days. To model a leap day
      (e.g. for a back-cast with aligned price and irradiance data), repeat timestamps for 2/28.
    - Typical Year (TY) solar resource data represents the "typical" resource in a location such that the
      data can be tiled across all the years of a project's lifetime. Data is **assumed** to be typical if it spans 8760
      hours and :attr:`~PVGenerationModel.project_term` and :attr:`~PVGenerationModel.project_term_units` equate to a
      whole number of years. TY data should:
      - represent one full year of data (8760 hours)
      - not contain any leap days
      - start with the 0th hour of January 1st.
    """

    year: t.List[int]
    r"""Year value of the interval-beginning timestamp
    
    - 4 digit integer.
    """
    month: t.List[int]
    r"""Month value of interval-beginning timestamp
        
    - Possible values: 1-12.
    """
    day: t.List[int]
    r"""Day value of interval-beginning timestamp
        
    - Possible values: 1-31
    """
    hour: t.List[int]
    r"""Hour value of interval-beginning timestamp
        
    - Possible values: 0-23
    """
    minute: t.List[int]
    r"""Minute values of interval-beginning timestamp, or for hourly simulations, the minute associated with desired sun
    position
    
    - Possible values: 0-59
    - For hourly simulations, in almost all cases, this should be 30 for all intervals (the midpoint of the hour) 
    """
    tdew: t.List[float]
    r"""Dew point temperature

    - Units: |degrees|\ C
    """
    df: t.List[float]
    r"""`Diffuse Horizontal Irradiance <df_>`_
    
    .. _df: https://pvpmc.sandia.gov/modeling-steps/1-weather-design-inputs/irradiance-and-insolation-2/diffuse-
        horizontal-irradiance/

    - Units: W/m\ :sup:`2`
    """
    dn: t.List[float]
    r"""`Direct Normal Irradiance <dn_>`_
    
    .. _dn: https://pvpmc.sandia.gov/modeling-steps/1-weather-design-inputs/irradiance-and-insolation-2/direct-
        normal-irradiance/

    - Units: W/m\ :sup:`2`
    """
    gh: t.List[float]
    r"""`Global Horizontal Irradiance <gh_>`_
    
    .. _gh: https://pvpmc.sandia.gov/modeling-steps/1-weather-design-inputs/irradiance-and-insolation-2/global-
        horizontal-irradiance/

    - Units: W/m\ :sup:`2`
    """
    pres: t.List[float]
    r"""Ambient pressure

    - Units: milibar
    """
    tdry: t.List[float]
    r"""Ambient Temperature (dry bulb)

    - Units: |degrees|\ C
    """
    wdir: t.List[float]
    r"""Wind direction

    - Units: degrees east of north, with a wind from the north having a value of 0.0
    """
    wspd: t.List[float]
    r"""Wind speed

    - Units: meter per second
    """
    alb: t.Optional[t.List[float]] = None
    r"""`Surface albedo <alb_>`_
    
    .. _alb: https://pvpmc.sandia.gov/modeling-steps/1-weather-design-inputs/plane-of-array-poa-irradiance/
        calculating-poa-irradiance/poa-ground-reflected/albedo/

    - Units: ratio of reflected GHI
    - Default value is 0.2
    """
    snow: t.Optional[t.List[float]] = None
    r"""Snow depth

    - Units: centimeters
    """

    @model_validator(mode="before")
    @classmethod
    def check_lengths(cls, values):
        try:
            _check_lengths({k: v for k, v in values.items() if v is not None})
        except AssertionError:
            raise AssertionError("solar resource time series data must have consistent lengths")
        return values

    def __len__(self) -> int:
        return len(self.year)


class SolarResource(BaseModel):
    r"""Sub-model for full specification of solar resource inputs"""

    latitude: float
    r"""Geographic coordinate for the North-South position of the resource in decimal degrees 

    - Example: 38.0 for 38.0\ |degrees|\ N
    """
    longitude: float
    r"""Geographic coordinate for the East-West position of the resource in decimal degrees

    - Example: -80.0 for 80.0\ |degrees|\ W
    """
    time_zone_offset: float
    r"""The UTC offset for the amount of time subtracted from or added to the UTC timezone. This is used in conjuction
    with the local-standard timestamps contained in :attr:`data`

    - Example: -8.0 for UTC-8:00 (Pacific Standard Time)
    """
    elevation: float
    r"""Height above (or below) sea level.

    - Units: meters
    - Example: 358.0 for 358 meters above sea level
    """
    data: SolarResourceTimeSeries
    r"""Solar resource time series data, see :class:`SolarResourceTimeSeries` for gotchas (e.g. Typical Year 
    constraints)"""
    monthly_albedo: t.Optional[t.List[float]] = None
    r"""Surface albedo is the fraction of the Global Horizontal Irradiance that reflects, `more detail here <alb_>`_.
    If provided, this value overrides the hourly albedo value in SolarResourceTimeSeries.

    - Units: ratio
    - Format as a 12 element list of floats
    - Example: [0.2] * 12 for 12 months of 0.2 albedo
    - Default value is 0.2
    """

    def __len__(self) -> int:
        return len(self.data)


class PSMRegion(str, Enum):
    r"""Region / satellite system to query for irradiance data."""

    NorthAmerica = "North America"
    r"""Irradiance data from the GOES satellite system"""
    AsiaPacific = "Asia/Pacific"
    r"""Irradiance data from the Himawari satellite system"""
    EuropeAfricaAsia = "Europe/Africa/Asia"
    r"""Irradiance data from the Meteosat Prime Meridian satellite system"""


class SolarResourceLocation(BaseModel):
    r"""Location inputs class for pulling PSM solar resource data from the `NSRDB <https://nsrdb.nrel.gov/>`__"""

    latitude: float
    r"""Geographic coordinate for the North-South position of the resource in decimal degrees 

    - Example: 38.0 for 38.0\ |degrees|\ N
    """
    longitude: float
    r"""Geographic coordinate for the East-West position of the resource in decimal degrees

    - Example: -80.0 for 80.0\ |degrees|\ W
    """
    region: PSMRegion = PSMRegion.NorthAmerica
    r"""regional data set to be queried"""
    model_config = ConfigDict(extra="forbid")


class FileComponent(BaseModel):
    r"""Equipment inputs class for using inverter/pv module files that have already been uploaded to Tyba, e.g. via
    the Webapp
    """

    path: str
    r"""Path in Tyba database to uploaded file. Please contact Tyba for assistance in determining the correct file path
    """


class PVModuleCEC(BaseModel):
    r"""Inputs for modeling PV module/array performance using the CEC module model, which is an extension of the
    `Desoto 5-parameter model <desoto_>`_. More information on how the model is implemented in NREL SAM (and by
    extension Tyba) can be found in Section 10.4 of the
    `SAM Photovoltaic Model Technical Reference Update <sam_tech_ref_>`_.

    .. _desoto: https://pvpmc.sandia.gov/modeling-steps/2-dc-module-iv/single-diode-equivalent-circuit-models/de-soto-
        five-parameter-module-model/
    .. _sam_tech_ref: https://www.nrel.gov/docs/fy18osti/67399.pdf
    """

    bifacial: bool
    r"""Whether or not the module is bifacial"""
    a_c: float
    r"""Module area

    - Units: m\ :sup:`2`
    - Example value: 2.17 m\ :sup:`2`
    """
    n_s: float
    r"""Number of cells

    - Example value: 72
    """
    i_sc_ref: float
    r"""Short circuit current at STC

    - Units: Adc
    - Example value: 11.3 Adc
    """
    v_oc_ref: float
    r"""Open circuit voltage at STC

    - Units: Vdc
    - Example value: 48.6 Vdc
    """
    i_mp_ref: float
    r"""Max power current at STC

    - Units: Adc
    - Example value: 10.8 Adc
    """
    v_mp_ref: float
    r"""Max power voltage at STC

    - Units: Vdc
    - Example value: 40.1Vdc
    """
    alpha_sc: float
    r"""Temperature coefficient of short circuit current

    - Denormalize the CEC Data-sheet :math:`\\alpha` value as follows:
        - :math:`\\alpha = {\\alpha_{CEC}}*{I_{sc}/100}`
    - Units: A/K
    - Example value: 0.00461 A/K
    """
    beta_oc: float
    r"""Temperature coefficient of open circuit voltage

    - Denormalize the CEC Data-sheet :math:`\\beta` value as follows:
        - :math:`\\beta = {\\beta_{CEC}}*{V_{oc}/100}`
    - Units: V/K
    - Example value: -0.1406 V/K
    """
    t_noct: float
    r"""Nominal operating cell temperature

    - Units: |degrees|\ C
    - Example value: 44.0\ |degrees|\ C
    """
    a_ref: float
    r"""Ideality factor at STC

    - Units: V
    - Example value: 1.81 V
    """
    i_l_ref: float
    r"""Light current at STC

    - Units: A
    - Example value: 11.47 A
    """
    i_o_ref: float
    r"""Diode saturation current at STC

    - Units: A
    - Example value: 2.63e-11 A
    """
    r_s: float
    r"""Reference series resistance
    
    - Units: :math:`\\Omega`
    - Example value: 0.27\ :math:`\\Omega`
    """
    r_sh_ref: float
    r"""Reference shunt resistance

    - Units: :math:`\\Omega`
    - Example value: 453.56\ :math:`\\Omega`
    """
    adjust: float
    r"""Temperature coefficient adjustment factor

    - Format as a float that represents the percentage
    - Example value: 7.64 for 7.64%
    """
    gamma_r: float
    r"""Temperature coefficient of maximum power

    - Units:  %/\ |degrees|\ C
    - Example value: -0.36%/\ |degrees|\ CC
    """
    bifacial_transmission_factor: float
    r"""Fraction of irradiance incident on the front surface of the array that passes through and strikes the ground
    (and thus contributes to backside irradiance). Such transmission can be due to e.g. gaps between modules,
    module/cell borders for glass-glass modules etc. Sometimes estimated as the ratio of the area light can pass
    through to the total bounding area of the array frontside collector surface

    - Ignored if :attr:`bifacial` is ``False``
    - Format as a float that represents the decimal value
    - Example value: 0.2 for 20%
    """
    bifaciality: float
    r"""Rear-side to front-side efficiency ratio. 

    - Ignored if :attr:`bifacial` is ``False``
    - Format as a float that represents the decimal value
    - Example value: 0.68 for 68%
    """
    bifacial_ground_clearance_height: float
    r"""Height from the ground to the bottom of the PV array. For tracking systems, this is the height at a zero-degree
    tilt

    - Ignored if :attr:`bifacial` is ``False``
    - Units: m
    - Example value: 0 m
    """


class MermoudModuleTech(str, Enum):
    r"""Enum class for selecting module technology input to :attr:`PVModuleMermoudLejeune.tech`"""

    SiMono = "mtSiMono"
    r"""Monocrystalline Silicon"""
    SiPoly = "mtSiPoly"
    r"""Polycrystalline Silicon"""
    CdTe = "mtCdTe"
    r"""Thin-film Cadmium-Telluride"""
    CIS = "mtCIS"
    r"""Copper Indium Gallium Selenide"""
    uCSi_aSiH = "mtuCSi_aSiH"
    r"""Amorphous Silicon"""


class PVModuleMermoudLejeune(BaseModel):
    r"""Inputs for modeling PV module/array performance using the `Mermoud-Legeune (aka PVsyst) model <mermoud_>`_.
    Instances can be generated from PAN files using :func:`tyba_client.io.pv_module_from_pan`

    .. _mermoud: https://pvpmc.sandia.gov/modeling-steps/2-dc-module-iv/single-diode-equivalent-circuit-models/
        pvsyst-module-model/
    """

    bifacial: bool
    r"""Whether or not the module is bifacial"""
    bifacial_transmission_factor: float
    r"""Fraction of irradiance incident on the front surface of the array that passes through and strikes the ground
    (and thus contributes to backside irradiance). Such transmission can be due to e.g. gaps between modules,
    module/cell borders for glass-glass modules etc. Sometimes estimated as the ratio of the area light can pass
    through to the total bounding area of the array frontside collector surface

    - Ignored if :attr:`bifacial` is ``False``
    - Format as a float that represents the decimal value
    - Example value: 0.2 for 20%
    """
    bifaciality: float
    r"""Rear-side to front-side efficiency ratio. 

    - Ignored if :attr:`bifacial` is ``False``
    - Format as a float that represents the decimal value
    - Example value: 0.68 for 68%
    """
    bifacial_ground_clearance_height: float
    r"""Height from the ground to the bottom of the PV array. For tracking systems, this is the height at a zero-degree
    tilt

    - Ignored if :attr:`bifacial` is ``False``
    - Units: m
    - Example value: 0 m
    """
    tech: MermoudModuleTech
    r"""Input for selecting module technology, which determines :math:`E_g` and :math:`\\frac{d^2}{\\mu_{\\tau, eff}}`
    used in the single diode equation. Values are chosen based on recommendations in the
    `PVSyst User Guide <pvsyst_guide_module_model_>`_. Note that a custom value for
    :math:`\\frac{d^2}{\\mu_{\\tau, eff}}` can also be provided with the :attr:`custom_d2_mu_tau` input.
    
    .. _pvsyst_guide_module_model: https://www.pvsyst.com/help/index.html?pvmodule_model.htm
    """
    iam_c_cs_iam_value: t.Optional[t.List[float]] = None
    r"""Incident angle modifier factors

    - Corresponds to :attr:`iam_c_cs_inc_angle`
    - Units: unitless
    - Example values: [1.0, 1.0, 0.95, 0.85, 0.6, 0.2, 0.]
    """
    iam_c_cs_inc_angle: t.Optional[t.List[float]] = None
    r"""Incident angle modifier angles

    - Corresponds to :attr:`iam_c_cs_iam_value`
    - Units: degrees
    - Example values: [0, 15, 30, 45, 60, 75, 90]
    """
    i_mp_ref: float
    r"""Max power current at reference conditions (set by :attr:`s_ref` and :attr:`t_ref`)

    - Units: Adc
    - Example value: 10.8 Adc
    """
    i_sc_ref: float
    r"""Short circuit current at reference conditions (set by :attr:`s_ref` and :attr:`t_ref`)

    - Units: Adc
    - Example value: 11.3 Adc
    """
    length: float
    r"""Long dimension of solar module

    - Units: m
    - Example value: 1.956m
    """
    n_diodes: int
    r"""Number of diodes in solar cell

    - Units: quantity
    - Example value: 3
    """
    n_parallel: int
    r"""Number of cells in parallel

    - Units: quantity
    - Example value: 1
    """
    n_series: int
    r"""Number of cells in series

    - Units: quantity
    - Example value: 72
    """
    r_s: float
    r"""Reference series resistance
    
    - Units: :math:`\\Omega`
    - Example value: 0.27
    """
    r_sh_0: float
    r"""Shunt resistance in 0 irradiance

    - Units: :math:`\\Omega`
    - Example value: 2500
    """
    r_sh_exp: float
    r"""Shunt resistance exponential factor

    - Units: :math:`\\Omega`
    - Example value: 5.5
    """
    r_sh_ref: float
    r"""Shunt resistance at reference conditions (set by :attr:`s_ref` and :attr:`t_ref`)

    - Units: :math:`\\Omega`
    - Example value: 600
    """
    s_ref: float
    r"""Reference irradiance. In almost all cases this should be 1000 W/m\ :sup:`2` corresponding to STC 

    - Units: W/m\ :sup:`2`
    - Example value: 1000
    """
    t_c_fa_alpha: float
    r"""Faiman thermal model absorptivity. Referred to as "Alpha" in the `PVsyst User Guide <pvsyst_guide_thermal_>`_.
    
    .. _pvsyst_guide_thermal: https://www.pvsyst.com/help/thermal_loss.htm

    - Units: unitless
    - Example value: 0.90
    """
    t_ref: float
    r"""Reference temperature. In almost all cases this should be 25\ |degrees|\ C corresponding to STC

    - Units: |degrees|\ C
    - Example value: 25.0
    """
    v_mp_ref: float
    r"""Max power voltage at reference conditions (set by :attr:`s_ref` and :attr:`t_ref`)

    - Units: Vdc
    - Example value: 40.1Vdc
    """
    v_oc_ref: float
    r"""Open circuit voltage at reference conditions (set by :attr:`s_ref` and :attr:`t_ref`)

    - Units: Vdc
    - Example value: 48.6Vdc
    """
    width: float
    r"""Short dimension of solar module

    - Units: m
    - Example value: 0.992 m
    """
    alpha_sc: float
    r"""Temperature coefficient of short circuit current

    - Units: A/K
    - Example value: 0.00461 A/K
    """
    beta_oc: float
    r"""Temperature coefficient of open circuit voltage

    - Units: V/K
    - Example value: -0.1406 V/K
    """
    mu_n: float
    r"""Temperature coefficient of diode non-ideality factor

    - Units: 1/K
    - Example value: -0.0007 1/K
    """
    n_0: float
    r"""Diode non-ideality factor

    - Units: 1/K
    - Example value: 0.967
    """
    custom_d2_mu_tau: t.Optional[float] = None
    r"""Custom recombination loss coefficient. If not set, the value of :math:`\\frac{d^2}{\\mu_{\\tau, eff}}` is chosen
    based on :attr:`tech`

    - Units: V
    - Example value: 1.4 V
    """


class BaseInverter(BaseModel):
    r"""Base class for inverter model input classes

    :meta private:
    """

    mppt_low: float
    r"""Minimum MPPT DC Voltage

    - Units: Vdc
    - Example value: 1003 Vdc
    """
    mppt_high: float
    r"""Maximum MPPT DC Voltage

    - Units: Vdc
    - Example value: 1200 Vdc
    """
    paco: float
    r"""Maximum AC power

    - Units: Wac
    - Example value: 4198240 Wac
    """
    vdco: float
    r"""Nominal DC Voltage

    - Units: Vdc
    - Example value: 1062 Vdc
    """
    pnt: float
    r"""Standby/Nighttime power use

    - Units: Wac
    - Example value: 1259.47 Wac
    """
    includes_xfmr: bool = False
    r"""Indicate whether inverter model includes a medium voltage transformer. If set to ``True``, then
    :attr:`ACLosses.mv_transformer` should be ``None`` or MV transformer losses will be double counted.
    """


class Inverter(BaseInverter):
    r"""Inputs for modeling inverter performance using the `Sandia Inverter Model <sandia_inverter_>`_.

    .. _sandia_inverter: https://pvpmc.sandia.gov/modeling-steps/dc-to-ac-conversion/sandia-inverter-model/
    """

    pso: float
    r"""Power use during operation

    - Units: Wdc
    - Example value: 6429 Wdc
    """
    pdco: float
    r"""Maximum DC power

    - Units: Wdc
    - Example value: 4272031 Wdc
    """
    c0: float
    r"""First Sandia Coefficients

    - Units: 1/Wac
    - Example value: 2.84059e-9  1/Wac
    """
    c1: float
    r"""Second Sandia Coefficient

    - Units: 1/Vdc
    - Example values: 1.1e-5
    """
    c2: float
    r"""Third Sandia Coefficient

    - Units: 1/Vdc
    - Example values: 0.001713
    """
    c3: float
    r"""Fourth Sandia Coefficient

    - Units: 1/Vdc
    - Example values: 0.001056
    """
    vdcmax: float
    r"""Maximum DC Voltage

    - Units: Vdc
    - Example value: 1200 Vdc
    """


class ONDTemperatureDerateCurve(BaseModel):
    r"""Temperature derate inputs for use with :class:`ONDInverter`. Maximum AC power is assumed to vary linearly
    between the points, as explained in the `PVSyst User Guide <pvsyst_inv_temp_derate_>`_.

    .. _pvsyst_inv_temp_derate: https://www.pvsyst.com/help/index.html?inverter_outputparameter.htm
    """

    ambient_temp: t.List[float]
    r"""Temperatures in the derate curve, corresponding to :attr:`max_ac_power`
    
    - Units: |degrees|\ C
    - Example values: [25.0, 50.0, 60.0]
    """
    max_ac_power: t.List[float]
    r"""Maximum AC output values in the derate  curve, corresponding to :attr:`ambient_temp`
    
    - Units: W
    - Example values: [14000, 12000, 10000]
    """


class ONDEfficiencyCurve(BaseModel):
    r"""Efficiency curve inputs for use with :class:`ONDInverter`"""

    dc_power: t.List[float]
    r"""List of input DC power values. First value must equal to :attr:`ONDInverter.dc_turn_on`
    
    - Units: W
    - Examples values: [0.0, 200.0, 300.0, 600.0, 1000.0]
    """
    ac_power: t.List[float]
    r"""List of output AC power values corresponding to the values in :attr:`dc_power`
    
    - Units: W
    - Example values: [0.0, 199.0, 298.0, 596.0, 1090.0]
    """


class ONDInverter(BaseInverter):
    r"""Inputs for modeling inverter performance using the `PVSyst/OND model <pvsyst_inv_>`_. Instances can be
    generated from OND files using :func:`tyba_client.io.inverter_from_ond`.

    .. _pvsyst_inv: https://www.pvsyst.com/help/index.html?inverter_inputmodel.htm
    """

    temp_derate_curve: ONDTemperatureDerateCurve
    r"""Curve of maximum AC power vs ambient temperature"""
    nominal_voltages: t.List[float]
    r"""DC voltage values that correspond to the curves provided in :attr:`power_curves`. Must have 3 voltages.
    
    - Units: Vdc
    - Example values: [900.0, 1200.0, 1500.0]
    """
    power_curves: t.List[ONDEfficiencyCurve]
    r"""DC vs AC power curves that correspond to the dc voltages in :attr:`nominal_voltages`. Must have 3 curves. First
    DC power value in each curve must equal to :attr:`dc_turn_on`
    """
    dc_turn_on: float
    r"""Minimum DC power value that must be provided for AC power to be produced by inverter.
    
    - Units: W
    - Example value: 100.0
    """
    aux_loss: t.Optional[float] = None
    r"""Additional losses applied after efficiency and clipping when AC power is above
    :attr:`aux_loss_threshold`. This can be used to represent e.g. fan losses. However, some manufacturers include the
    "Aux_Loss" value in the OND file for reporting purposes even though the aux loss effect is represented in the
    :attr:`power_curves`. In this case, :attr:`aux_loss` should be ``None``. Consult with your inverter manufacturer for
    clarification.
    
    - Units: W
    - Example value: 100.0
    """
    aux_loss_threshold: t.Optional[float] = None
    r"""DC power threshold above which the loss in :attr:`aux_loss` gets applied.
    
    - Units: W
    - Example value: 200.0
    """

    @model_validator(mode="after")
    def check_sufficient_power_curves_voltages(self):
        assert (
            len(self.power_curves) == len(self.nominal_voltages) == 3
        ), "3 power curves and corresponding voltages required for OND model"
        return self

    @model_validator(mode="after")
    def check_aux_loss_etc(self):
        if (self.aux_loss is None) != (self.aux_loss_threshold is None):
            raise AssertionError("either both or neither of aux_loss and aux_loss_threshold must be provided")
        return self


InverterTypes = t.Union[Inverter, ONDInverter, str, FileComponent]
PVModuleTypes = t.Union[PVModuleCEC, PVModuleMermoudLejeune, str, FileComponent]


class Layout(BaseModel):
    r"""Inputs related to the configuration of PV modules within their racking"""

    orientation: t.Optional[str] = None
    r"""The orientation of the PV modules within their racking.

    - Possible values: "portrait" (length is vertical) or "landscape" (width is vertical)
    - Default is "portrait"
    """
    vertical: t.Optional[int] = None
    r"""The number of modules along the vertical axis (side) of the racking table.

    - Default value is 2
    """
    horizontal: t.Optional[int] = None
    r"""The number of modules along the horizontal axis (bottom) of the racking table per sub-array.

    - Default value is 48
    """
    aspect_ratio: t.Optional[float] = None
    r"""The ratio of the module length to module width.

    - Default value is 1.7
    """

    @model_validator(mode="after")
    def all_or_none(self):
        missing = [v is None for k, v in self.model_dump().items()]
        assert all(missing) or not any(missing), "Either all or no attributes must be assigned in Layout"
        return self


class Transformer(BaseModel):
    r"""Inputs for modeling transformers (both high (HV) and medium voltage (MV))"""

    rating: t.Optional[float] = None
    r"""The transformer’s rated power capacity. If set to `None`, the rated power capacity will be either: the total
    nominal AC inverter capacity (if inverters are modeled), or the :attr:`~BaseSystemDesign.poi_limit` 
    
    - Units: kW
    - Example value: 100000.0
    """
    load_loss: float
    r"""The transformer’s load-dependent loss factor (coil losses) when operating at the rated capacity

    - Units: unitless
    - Recommended values:
       - HV transformer/GSU = 0.007
       - MV transformer = 0.009
    
    """
    no_load_loss: float
    r"""The transformer's constant loss factor (core losses)

    - Units: unitless
    - Recommended values:
       - HV transformer/GSU = 0.002
       - MV transformer = 0.001
    """


class ACLosses(BaseModel):
    r"""Inputs related to system losses that occur downstream of the solar/BESS inverters"""

    ac_wiring: float = 0.01
    r"""Losses from MV AC wiring resistance between the inverter/MV transformer and the point of interconnection (or
    HV transformer if applicable).

    - Units: fraction
    """
    transmission: float = 0.0
    r"""Losses from HV AC wiring resistance, i.e. gen-tie wiring losses.

    - Units: fraction
    """
    # Feeds into nrel_sam.AdjustmentFactors rather than nrel_sam.Losses
    poi_adjustment: float = 0.0  # TODO: deprecate this?
    r"""Adjust AC power at POI to account for additional arbitrary losses. Intended to apply a
    constant haircut to model system availability, but can be used for other purposes as well.

    - Negative values can be used to represent power gains
    - Units: fraction
    - Given intended use of modeling availability, not applied during BESS optimization (if applicable) or to market
      offers and awards
    """
    transformer_load: Annotated[
        Optional[float],
        get_deprecator("transformer_load is deprecated and will be removed in the future. Use hv_transformer instead."),
    ] = None
    r"""Deprecated. Please use :attr:`hv_transformer`.
    
    `The high-voltage transformer's load-dependent loss factor (coil losses)`
    """
    transformer_no_load: Annotated[
        Optional[float],
        get_deprecator(
            "transformer_no_load is deprecated and will be removed in the future. Use hv_transformer instead."
        ),
    ] = None
    r"""Deprecated. Please use :attr:`hv_transformer`.
    
    `The high-voltage transformer's constant loss factor (core losses)`
    """
    hv_transformer: t.Optional[Transformer] = Transformer(
        load_loss=0.007,
        no_load_loss=0.002,
    )
    r"""Inputs for modeling a HV transformer/GSU. Setting to ``None`` assumes the system interconnection voltage is such
    that a GSU is not needed. For parameter recommendations, see :class:`Transformer`
    """
    mv_transformer: t.Optional[Transformer] = None
    r"""Inputs for modeling a MV transformer. If the inverter model given in the :attr:`~PVGenerationModel.inverter`
    attribute of :class:`PVGenerationModel`, :class:`DCExternalGenerationModel` or :class:`DownstreamSystem` includes
    MV transformer effects, then this should be set to ``None`` to avoid double-counting losses. Otherwise, a
    :class:`Transformer` object should be provided to ensure transformer losses are accounted for. For parameter
    recommendations, see :class:`Transformer`
    """

    @model_validator(mode="after")
    def check_repeated_hv_transformer(self):
        assert (
            self.transformer_load is None and self.transformer_no_load is None
        ) or self.hv_transformer is None, (
            "Cannot provide hv_transformer if transformer_load or transformer_no_load are provided"
        )
        return self


BoundedLossFactor: TypeAlias = Annotated[
    float,
    Field(ge=0, le=1.0),
]
"""float that must be between 0 and 1 inclusive"""


class DCLosses(BaseModel):
    r"""Inputs related to PV array losses that occur upstream of the solar inverters. For use (via :class:`Losses`) with
    :class:`PVGenerationModel`
    """

    dc_optimizer: BoundedLossFactor = 0.0
    r"""Losses from power equipment within the array, including DC optimizers and DC-DC converters.

    - Units: fraction
    - Min value: 0.0
    - Max value: 1.0
    """
    enable_snow_model: bool = False
    r"""Indicates whether NREL SAM's snow loss model should be activated. If ``True``,
    :attr:`~SolarResourceTimeSeries.snow` in :attr:`SolarResource.data` must be provided. 
    """
    dc_wiring: BoundedLossFactor = 0.02
    r"""Losses from DC wiring resistance within the array.

    - Units: fraction
    - Min value: 0.0
    - Max value: 1.0
    """
    soiling: conlist(Annotated[float, Field(ge=-1.0, le=1.0)], min_length=12, max_length=12) = Field(
        default_factory=lambda: 12 * [0.0]
    )
    r"""Monthly reduction in irradiance occurring from dust, dirt, or other substances on the surface of the module.
    If :attr:`enable_snow_model` is ``False``, this input should also be used to account for any snow losses.
    Similarly, this input can be used to approximate a combination of soiling and other effects (e.g. spectral) as a
    series of monthly gains and losses.

    - Units: fraction
    - Format as a list of 12 floats representing the decimal value of loss
    - Min monthly value: -1.0 (100% gain)
    - Max monthly value: 1.0 (100% loss)
    """
    diodes_connections: BoundedLossFactor = 0.005
    r"""Losses from voltage drops of diodes and electrical connections.

    - Units: fraction
    - Min value: 0.0
    - Max value: 1.0
    """
    mismatch: BoundedLossFactor = 0.01
    r"""Losses due to differences in the max power point of individual modules, as well as differences between
    strings. These differences can be due to manufacturing variation as well as varied shading across the array. Should
    include the net effect of backside mismatch for bifacial modules.

    - Units: fraction
    - Min value: 0.0
    - Max value: 1.0
    """
    nameplate: Annotated[float, Field(ge=-0.05, le=1.0)] = 0.0
    r"""Deviations between the nameplate rating provided by a manufacturer and actual/tested performance. This input
    could be used to represent positive binning tolerance or the situation where you need to model a PV module with a
    different wattage than the one you have model parameters for.

    - Units: fraction
    - Positive values represent a loss, negative values represent a gain
    - Min value: -0.05 (5% gain)
    - Max value: 1.0 (100% loss)
    - Example: A module with 405W nameplate power and +5% binning tolerance could be represented by a 400W module model
      and :math:`nameplate = 1 - (405/400)(1 + 0.05/2) = -0.0378`
    """

    rear_irradiance: BoundedLossFactor = 0.0
    r"""Losses associated with irradiance on the back surface of bifacial modules. Should be 0.0 for monofacial
    modules. This would include the effects of rearside rack-shading, soiling, etc. but mismatch should be accounted
    for in the :attr:`mismatch` input

    - Units: fraction
    - Min value: 0.0
    - Max value: 1.0
    """
    mppt_error: Annotated[
        BoundedLossFactor,
        get_deprecator("mppt_error is deprecated and will be removed in the future. Use tracking_error instead."),
    ] = 0.0
    r"""Deprecated (as well as misnamed). Use :attr:`tracking_error` instead
    """
    tracking_error: BoundedLossFactor = 0.0
    r"""Losses due to tracking system error in single-axis tracking systems. Should be 0.0 for fixed tilt systems.
    
    - Units: fraction
    - Min value: 0.0
    - Max value: 1.0
    """
    # Feeds into nrel_sam.AdjustmentFactors rather than nrel_sam.Losses
    lid: BoundedLossFactor = 0.0
    r"""Losses due to Light- and elevated Temperature-Induced Degradation.

    - Units: fraction
    - Min value: 0.0
    - Max value: 1.0
    """
    dc_array_adjustment: float = 0.0
    r"""Adjust DC power at inverter input to account for additional arbitrary losses or gains.

    - Negative values can be used to represent power gains
    - Units: fraction
    """

    @model_validator(mode="after")
    def check_tracker_losses(self):  # TODO: remove once mppt_error deprecated, equivalent to tracking_error
        assert self.mppt_error * self.tracking_error == 0.0, "Only one of mppt_error and tracking_error may be nonzero"
        return self


class Losses(ACLosses, DCLosses):
    r"""Container class that combines :class:`ACLosses` and :class:`DCLosses` for use with :class:`PVGenerationModel`"""

    model_config = ConfigDict(extra="forbid")


class DCProductionProfile(BaseModel):
    r"""Time series inputs associated with a DC generation source (e.g. PV array). For use with
    :class:`DCExternalGenerationModel`
    """

    power: t.List[float]
    r"""The net power at all DC-DC busbars for DC-Coupled systems, or all inverter MPP inputs for solar-only
    systems. This power will be divided by the number of inverters determined based on
    :attr:`DCExternalGenerationModel.inverter` and the system AC capacity before being passed through the inverter
    model in :attr:`DCExternalGenerationModel.inverter`

    - Should not consider any inverter clipping effects on DC power (since this clipping could be captured by a
      DC-coupled BESS and will be modeled in the inverter model anyways)
    - Assumed to include any aging/degradation effects
    - In PVSyst, this field is EArrayMPP (not EArray), though PVsyst does not consider degradation
    - Units: kW
    - Example: For a nameplate 100MWdc array at STC for 3 hours, the input would be [100000, 100000, 100000].
    """
    voltage: t.List[float]
    r"""The voltage at the DC-DC busbar for DC-Coupled systems or inverter MPP input for solar-only systems. Unlike
    :attr:`power`, total array voltage is not the sum of inverter DC voltages, so these values will not be divided
    before being passed into the inverter model.

    - In PVSyst, this field is Uarray
    - Units: V
    - Example: For a nominal 1500Vdc system, the max values should be somewhere near but below 1500V.
    """
    ambient_temp: t.Optional[t.List[float]] = None
    r"""Hourly ambient temperature. Used for inverter efficiency and HVAC model (when used).
    
    - Units: - Units: |degrees|\ C
    - Example values: [25.0, 35.0, 45.0]
    """

    @model_validator(mode="after")
    def check_length(self):
        _check_lengths({"power": self.power, "voltage": self.voltage})
        if self.ambient_temp:
            _check_lengths({"power": self.power, "ambient_temp": self.ambient_temp})
        return self

    def __len__(self) -> int:
        return len(self.power)


class BoundedSignal(BaseModel):
    r"""Container for any time series data associated with a signal that can have a range of values. For use with e.g.
    :attr:`ACProductionProfile.power`
    """

    min: t.List[float]
    r"""Time series of the lower bound of possible values the signal could take. For example, for PV array power,
    this might be a time series of P90 production.
    """

    actual: t.List[float]
    r"""Time series of the expected signal values. For example, for PV array power,
    this might be a time series of P50 production.
    """

    max: t.List[float]
    r"""Time series of the upper bound of possible values the signal could take. For example, for PV array power,
    this might be a time series of P05 production.
    """

    @model_validator(mode="after")
    def check_length(self):
        _check_lengths(self.model_dump())
        return self

    def __len__(self):
        return len(self.min)


class ACProductionProfile(BaseModel):
    r"""Time series inputs associated with an MV AC generation source (e.g. PV MV output, wind turbines etc.). For use
    with :class:`ACExternalGenerationModel`
    """

    power: t.Union[t.List[float], BoundedSignal]
    r"""The power at the MV AC bus (i.e. where a MV BESS system would tie-in). Can either be a time series of power
    values or a :class:`BoundedSignal` instance for modeling uncertain PV (or other) generation.

    - In PVSyst, this field is EOutInv if inverter modeling takes into account MV transformer losses. If not,
      use E_Grid with all models downstream of the mv transformer turned off or set to zero
    - Units: kW
    """
    ambient_temp: t.Optional[t.List[float]] = None
    r"""Hourly ambient temperature. Used for HVAC model if applicable.

    - Units: - Units: |degrees|\ C
    - Example values: [25.0, 35.0, 45.0]
    """
    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def check_length(self):
        if self.ambient_temp:
            _check_lengths({"power": self.power, "ambient_temp": self.ambient_temp})
        return self

    def __len__(self) -> int:
        return len(self.power)


ProductionProfile = t.Union[DCProductionProfile, ACProductionProfile]


class BaseSystemDesign(BaseModel):
    r"""Base class for system design objects"""

    dc_capacity: float
    r"""The total nameplate DC capacity of all the modules in a system.

    - Units: kWdc
    - Example: 1000.0 for a 1000 kWdc system
    """
    ac_capacity: float
    r"""The total nameplate AC capacity of all the inverters in a system.

    - Units: kWac
    - Example: 1000.0 for a 1,000 kWac system
    """
    poi_limit: float
    r"""The maximum injection capacity at the point of interconnection (usually defined by an interconnection
    agreement).

    - Units: kWac
    - Example: 1000.0 for a system with 1MW in interconnection capacity
    """


class PVSystemDesign(BaseSystemDesign):
    r"""Inputs for PV wiring and array configuration. A submodel for :attr:`PVGenerationModel.system_design`"""

    modules_per_string: t.Optional[int] = None
    r"""The number of modules connected in series for a single string. Generally Dependent on inverter and module
    selection. If not provided, a string size that keeps voltage within the inverter MPPT range is selected as part of
    the simulation.
    """
    strings_in_parallel: t.Optional[int] = None
    r"""The number of module strings connected in parallel to form an array. Generally dependent on `dc_capacity` and
    module selection. If not provided, Tyba will make an assumption as part of the simulation.
    """
    tracking: TrackingTypes
    r"""A sub-model to represent the PV racking design. Can be either :class:`FixedTilt` or :class:`SingleAxisTracking`
    """
    azimuth: t.Optional[float] = None
    r"""Orientation of the array towards the sun. Note that for fixed tilt systems, this means the direction in which
    the modules are tilted, whereas for single-axis tracking systems this means the direction of the axis of
    clock-wise rotation

    - Units: degrees east of north, with due north having a value of 0.0
    - Default value is 180\ |degrees| (due south) for the northern hemisphere and 0\ |degrees| (due north) for the
      southern hemisphere
    - Fixed Tilt Example: A northern hemisphere system with an azimuth of 190\ |degrees|
      would have all of its modules titled to face 10\ |degrees| west of due south
    - Single Axis Tracking Example: In the northern hemisphere, an azimuth of 180\ |degrees| (the default), would have
      the system tilted towards due east in the morning and due west in the evening. An azimuth of 190\ |degrees| would
      have the modules facing slightly south of east in the morning and slightly north of west in the evening 
    """
    gcr: float
    r"""The ratio of total module area to total land area. This is a measure of inter-row spacing, where a low
    ratio means the rows are more spread out and a higher ratio means the rows are tightly packed. Note that the tilt
    in fixed tilt systems is not to be taken into account (not a projected area in the numerator).

    - Example: 0.33
    """


class TermUnits(str, Enum):
    r"""Enum for indicating project term units"""

    hours = "hours"
    r"""Project term value is in units of hours"""
    days = "days"
    r"""Project term value is in units of days"""
    years = "years"
    r"""Project term value is in units of years"""


class ProjectTermMixin(BaseModel):
    r"""Mixin class used to add project term inputs to simulation classes

    :meta private:
    """

    project_term: int = 1
    r"""Integer value with units given by :attr:`project_term_units` that defines the project term (timespan) to be
    simulated.
    
    - For typical-year hybrid and solar-only simulations, the year-long time series in
      :attr:`solar_resource` will be tiled to match :attr:`project_term`. As such, the project term
      must represent a number of whole years
    - For all other hybrid and solar-only simulations, the project term must match the timespan represented by
      :attr:`time_interval_mins` and the length of the corresponding solar resource or power time series
    - For standalone storage simulations, the project term must match the timespan represented by
      :attr:`time_interval_mins` and the corresponding price time series
    """
    project_term_units: TermUnits = "years"
    r"""Units to be applied to :attr:`project_term` to define the term (timespan) to be simulated. See
    :attr:`project_term` for constraints
    
    """


class BaseGenerationModel(ProjectTermMixin):
    r"""Base class for generation model classes

    :meta private:
    """

    project_type: t.Literal["generation"] = "generation"
    r"""Used by the API for model-type discrimination, can be ignored"""
    time_interval_mins: int = 60
    r"""Time interval that corresponds to time series in :attr:`solar_resource` or :attr:`production_override`,
    whichever is applicable.
    
    - Units: minutes
    """


def scale_project_term_to_hours(project_term: int, project_term_units: TermUnits) -> int:
    r""":meta private:"""
    if project_term_units == "hours":
        return project_term
    elif project_term_units == "days":
        return 24 * project_term
    else:  # years
        return 8760 * project_term


def _check_time_interval_project_term(
    signal_len, signal_str, project_term, time_interval_mins, project_term_units: TermUnits
):
    """
    For more on why we treat project_term as an int and validate like we do check out this PR comment:
    https://github.com/Tyba-Energy/generation/pull/186#discussion_r1054578658. The broader PR has even more context
    should it be needed
    """
    signal_hours = int(signal_len * (time_interval_mins / 60))
    project_term_hours = scale_project_term_to_hours(project_term, project_term_units)
    assert project_term_hours == signal_hours, (
        f"project_term, project_term_units, time_interval_mins, and length of {signal_str} must be consistent; "
        f"got {project_term}, {project_term_units}, {time_interval_mins}, and {signal_len} respectively"
    )


class ExternalGenerationModel(BaseGenerationModel):
    r"""Base class for classes that represent AC or DC external generation sources

    :meta private:
    """

    losses: t.Union[ACLosses, Losses]
    r"""Submodel for losses that occur downstream of the bus associated with :attr:`production_override`
    """
    production_override: ProductionProfile
    r"""Submodel for time series (power etc) generated by external generation source
    """
    system_design: BaseSystemDesign
    r"""Submodel that defines system size for reporting, inverter sizing, and POI limiting
    """

    @model_validator(mode="after")
    def check_time_interval_project_term(self):
        _check_time_interval_project_term(
            len(self.production_override),
            "production_override",
            self.project_term,
            self.time_interval_mins,
            self.project_term_units,
        )
        return self

    def __len__(self) -> int:
        return len(self.production_override)


class Bus(str, Enum):
    r"""Enum class for selecting coupling bus for hybrid systems"""

    DC = "DC"
    r"""indicates the BESS and generator are coupled together at the DC inputs of the generator inverter"""
    MV = "MV"
    r"""indicates the BESS and generator are coupled at the medium voltage AC bus"""
    HV = "HV"
    r"""indicates the BESS and generator are coupled at the high voltage AC bus, e.g. the outlet of the 
    GSU/substation"""


class DownstreamSystem(BaseModel):
    r"""Submodel for detailed treatment of losses in standalone storage systems that aren't already considered as
    part of :attr:`~BatteryParams.charge_efficiency` and :attr:`~BatteryParams.discharge_efficiency`
    """

    losses: ACLosses  # still only ACLosses if modeling from inverter input, since almost every DC loss pertains to PV.
    r"""Submodel for post-inverter losses to be considered. Note that, depending on the coupling bus specified by
    :attr:`model_losses_from`, some of the attributes of :class:`ACLosses` will be ignored. For example, if the
    coupling bus is specified as high voltage, :attr:`~ACLosses.ac_wiring` and :attr:`~ACLosses.mv_transformer` will be
    ignored, since they are upstream of the coupling bus.
    """
    system_design: BaseSystemDesign
    r"""Submodel that defines system size for reporting, inverter sizing, and POI limiting
    """
    model_losses_from: Bus
    r"""Indicates the coupling bus downstream of which detailed loss modeling should occur. All losses/effects upstream
    of this bus are assumed to be rolled into :attr:`BatteryParams.charge_efficiency` and
    :attr:`BatteryParams.discharge_efficiency`
    """
    inverter: t.Optional[InverterTypes] = None
    r"""Inputs for inverter submodel. Required if :attr:`model_losses_from` is "DC", otherwise ignored. Can take
    multiple argument types:
    
    - An :class:`Inverter` or :class:`ONDInverter` object for full specification of the inverter model. In particular,
      use this type (along with :func:`tyba_client.io.inverter_from_ond`) if you are trying to model an inverter from 
      a local OND file
    - A string of the exact inverter name in Tyba's default inverter inventory (as shown in the web application)
    - A :class:`FileComponent` object that specifies the exact path of an OND file that was previously uploaded to
      Tyba via the web application
    """

    model_config = ConfigDict(protected_namespaces=())

    @model_validator(mode="after")
    def inverter_only_if_dc(self):
        if self.inverter is not None:
            assert self.model_losses_from == Bus.DC, "model_losses_from must be 'DC' if inverter is provided"
        return self


class ACExternalGenerationModel(ExternalGenerationModel):
    r"""Inputs for specifying an MV AC generation source, e.g. PV MV power from a non-Tyba source, wind power, etc.
    Intended to be passed into :attr:`PVStorageModel.pv_inputs` for hybrid simulations but can also be used as a
    simulation class for generation-only simulations. When used for a generation-only simulation,
    :class:`~generation_models.v0_output_schema.GenerationModelResults` is the results schema
    """

    generation_type: t.Literal["ExternalAC"] = "ExternalAC"
    r"""Used by the API for model-type discrimination, can be ignored"""
    losses: ACLosses = ACLosses()
    r"""Submodel for system losses. :attr:`ACLosses.mv_transformer` must be ``None`` since the
    :attr:`production_override` is assumed to be at medium voltage already.
    """
    production_override: ACProductionProfile
    r"""Submodel for time series related to generator power. Assumed to be power at the MV AC bus"""

    @field_validator("losses")
    @classmethod
    def no_mv_xfmr(cls, v: ACLosses):
        assert v.mv_transformer is None, (
            "losses.mv_transformer must be None, since the production_override provided in "
            "an ACExternalGenerationModel is assumed to be at the MV bus"
        )
        return v


class DCExternalGenerationModel(ExternalGenerationModel):
    r"""Inputs for specifying a DC generation source, e.g. PV array power from a non-Tyba source. Intended
    to be passed into :attr:`PVStorageModel.pv_inputs` for hybrid simulations but can also be used as a simulation
    class for generation-only simulations. When used for a generation-only simulation,
    :class:`~generation_models.v0_output_schema.GenerationModelResults` is the results schema
    """

    generation_type: t.Literal["ExternalDC"] = "ExternalDC"
    r"""Used by the API for model-type discrimination, can be ignored"""
    losses: Losses = Losses()
    r"""Submodel for system losses"""
    production_override: DCProductionProfile
    r"""Submodel for time series related to generator power.
    
    - Assumed to be at DC bus/inverter MPPT inputs
    - Assumed to include any aging/degradation effects
    """
    inverter: InverterTypes
    r"""Inputs for inverter submodel. Can take multiple argument types:
    
    - An :class:`Inverter` or :class:`ONDInverter` object for full specification of the inverter model. In particular,
      use this type (along with :func:`tyba_client.io.inverter_from_ond`) if you are trying to model an inverter from 
      a local OND file
    - A string of the exact inverter name in Tyba's default inverter inventory (as shown in the web application)
    - A :class:`FileComponent` object that specifies the exact path of an OND file that was previously uploaded to
      Tyba via the web application
    """


class ArrayDegradationMode(str, Enum):
    r"""Enum for specifying the PV array degradation approach to be used in a :class:`PVGenerationModel` or
    :class:`PVStorageModel` simulation
    """

    linear = "linear"
    r"""The degradation applied to each year of PV DC generation will increase linearly. The annual degradation derate
    is calculated as :math:`1-r_{degrad}*n_{year}` where :math:`r_{degrad}` is the degradation rate specified by
    :attr:`PVGenerationModel.array_degradation_rate` and :math:`n_{year}` is the count for the year in question.
    
    - Example: For a degradation rate of 0.005 (0.5%), the degradation derate applied to all time intervals of year 1 is
      :math:`1-0.005*1=0.995`
    """
    compounding = "compounding"
    r"""The degradation applied to each year of PV DC generation will be compounding. The degradation derate is
    calculated as :math:`(1-r_{degrad})^{n_{year}}` where :math:`r_{degrad}` is the degradation rate
    specified by :attr:`PVGenerationModel.array_degradation_rate` and :math:`n_{year}` is the count for the year
    in question.
    
    - Example: For a degradation rate of 0.005 (0.5%), the degradation derate applied to all time intervals of year 2 is
      :math:`(1-0.005)^2=0.99`
    """


def solar_resource_is_typical(solar_resource, time_interval_mins, project_term, project_term_units) -> bool:
    r""":meta private:"""
    if isinstance(solar_resource, (tuple, SolarResourceLocation)):
        return True
    if (
        isinstance(solar_resource, SolarResource)
        and (int(len(solar_resource) * time_interval_mins / 60) == 8760)
        and (scale_project_term_to_hours(project_term, project_term_units) % 8760 == 0)
        and (scale_project_term_to_hours(project_term, project_term_units) >= 8760)
    ):
        return True
    return False


def _pv_gen_len(solar_resource, time_interval_mins, project_term, project_term_units) -> int:
    if isinstance(solar_resource, SolarResource):
        if solar_resource_is_typical(solar_resource, time_interval_mins, project_term, project_term_units):
            return len(solar_resource) * int(scale_project_term_to_hours(project_term, project_term_units) / 8760)
        return len(solar_resource)
    return 8760 * int(scale_project_term_to_hours(project_term, project_term_units) / 8760)


class PVGenerationModel(BaseGenerationModel):
    r"""Simulation class for solar-only simulations, or can be passed into :attr:`PVStorageModel.pv_inputs` for
    hybrid simulations. When used for a solar-only simulation,
    :class:`~generation_models.v0_output_schema.GenerationModelResults` is the results
    schema
    """

    generation_type: t.Literal["PV"] = "PV"
    r"""Used by the API for model-type discrimination, can be ignored"""
    solar_resource: t.Union[SolarResource, t.Tuple[float, float], SolarResourceLocation]
    r"""Input for irradiance and weather time series and location information. Can take multiple argument types:
    
    - A :class:`SolarResource` object for full specification of solar resource. Must be used if resource does *not*
      represent a Typical Year (TY), but can also represent a TY. See :class:`SolarResourceTimeSeries` for more info.
    - A :class:`SolarResourceLocation` object. With this type, Tyba will pull TY solar resource data from
      the `NSRDB <https://nsrdb.nrel.gov/>`__ and use it in the simulation
    - A tuple of (latitude, longitude) where the values are in decimal degrees. This argument is
      equivalent to passing a :class:`SolarResourceLocation` object with :attr:`~SolarResourceLocation.region` equal to
      ``"North America"``
      
    Tiling of solar resource data to match the :attr:`project_term` is only supported for TY data
    """
    inverter: InverterTypes
    r"""Inputs for inverter submodel. Can take multiple argument types:
    
    - An :class:`Inverter` or :class:`ONDInverter` object for full specification of the inverter model. In particular,
      use this type (along with :func:`tyba_client.io.inverter_from_ond`) if you are trying to model an inverter from 
      a local OND file
    - A string of the exact inverter name in Tyba's default inverter inventory (as shown in the web application)
    - A :class:`FileComponent` object that specifies the exact path of an OND file that was previously uploaded to
      Tyba via the web application
    """
    pv_module: PVModuleTypes
    r"""Inputs for PV module/array submodel. Can take multiple argument types:
    
    - An :class:`PVModuleCEC` or :class:`PVModuleMermoudLejeune` object for full specification of the PV module model.
      In particular, use this type (along with :func:`tyba_client.io.pv_module_from_pan`) if you are trying to model
      a PV module from a local PAN file
    - A string of the exact PV module name in Tyba's default module inventory (as shown in the web application)
    - A :class:`FileComponent` object that specifies the exact path of a PAN file that was previously uploaded to
      Tyba via the web application"""
    layout: Layout = Layout()
    r"""Inputs that describe module/racking geometry"""
    losses: Losses = Losses()
    r"""Submodel for both array and AC-side losses"""
    system_design: PVSystemDesign
    r"""Inputs for system size and geometry"""
    array_degradation_rate: float = 0.005
    r"""Degradation rate applied annually to pre-inverter array DC power as specified by the
    :attr:`array_degradation_mode`. Ignored if :attr:`solar_resource` does not represent a Typical Year
    """
    array_degradation_mode: t.Optional[ArrayDegradationMode] = ArrayDegradationMode.linear
    r"""Method by which to apply :attr:`array_degradation_rate` to pre-inverter array DC power.
    
    - If ``None``, no degradation will be modeled
    - Only applicable if :attr:`solar_resource` represents a Typical Year, otherwise must be ``None``
    """

    def __len__(self) -> int:
        return _pv_gen_len(self.solar_resource, self.time_interval_mins, self.project_term, self.project_term_units)

    @model_validator(mode="after")
    def check_data_start_if_typical(self):
        if isinstance(self.solar_resource, SolarResource) and solar_resource_is_typical(
            self.solar_resource, self.time_interval_mins, self.project_term, self.project_term_units
        ):
            assert (
                self.solar_resource.data.month[0],
                self.solar_resource.data.day[0],
                self.solar_resource.data.hour[0],
            ) == (
                1,
                1,
                0,
            ), "solar resource data must start at Jan 1, hour 0 when typical solar resource is provided"
        return self

    @model_validator(mode="after")
    def check_time_interval_project_term(self):
        _check_time_interval_project_term(
            _pv_gen_len(
                self.solar_resource,
                self.time_interval_mins,
                self.project_term,
                self.project_term_units,
            ),
            "solar_resource",
            self.project_term,
            self.time_interval_mins,
            self.project_term_units,
        )
        return self

    @model_validator(mode="after")
    def check_degradation_mode_for_nontypical(self):
        if not solar_resource_is_typical(
            self.solar_resource, self.time_interval_mins, self.project_term, self.project_term_units
        ):
            assert (
                self.array_degradation_mode != "linear"
            ), "Linear PV array degradation not currently supported for non-typical year simulations"
        return self

    @model_validator(mode="after")
    def default_azimuth_from_location(self):
        system_design: PVSystemDesign = self.system_design
        solar_resource = self.solar_resource
        if system_design.azimuth is None:
            if isinstance(solar_resource, tuple):
                system_design.azimuth = 180.0 if solar_resource[0] >= 0.0 else 0.0
            elif isinstance(solar_resource, (SolarResource, SolarResourceLocation)):
                system_design.azimuth = 180.0 if solar_resource.latitude >= 0.0 else 0.0
            else:
                raise NotImplementedError("No default azimuth handling for this solar resource model")
        return self


GenerationModel = create_optionally_discriminant_union(
    union=t.Union[PVGenerationModel, DCExternalGenerationModel, ACExternalGenerationModel],
    discriminator="generation_type",
)


class TableCapDegradationModel(BaseModel):
    r"""Submodel for defining BESS energy capacity degradation as a table of values. Intended as a way to bring data in
    from a guaranteed capacity table included in a BESS purchase order/warranty. Note that although this model
    applies degradation based on time passing, it can account for both cycle and calendar degradation assuming the
    guaranteed cap table specifies an annual cycle count and this is similar to the annual cycle counts in the
    simulation
    """

    annual_capacity_derates: t.List[float]
    r"""List of end-of-year BESS energy capacity derates relative to initial BESS capacity, starting with year 0. At
    the end of each solver step as defined by :attr:`StorageSolverOptions.step`, the BESS capacity will be reduced
    based on time passed such that the capacity matches the list derate at the end of each simulation year.
    
    - First value in the list must be 1.0 (year 0 has no degradation)
    - Example: For annual derates [1.0, .9915, 0.9856] and an initial capacity of 100MWh, energy capacity will decrease
      linearly in a step-wise fashion until it is :math:`100*0.9915=99.15MWh` at the end of year 1 and
      :math:`100*0.9856=98.56MWh` at the end of year 2.
    - List length must be greater than or equal to :attr:`BatteryParams.term`
    """


class TableEffDegradationModel(BaseModel):
    r"""Submodel for defining BESS efficiency degradation as a table of values. Intended as a way to bring data in
    from a BESS purchase order/warranty. Note that although this model applies degradation based on time passing, it
    can account for both cycle and calendar degradation assuming the PO/warranty specifies an annual cycle count and
    this is similar to the annual cycle counts in the simulation
    """

    annual_efficiency_derates: t.List[float]
    r"""List of end-of-year BESS efficiency derates relative to initial BESS charge and discharge efficiency, starting
    with year 0. At the end of each solver step as defined by :attr:`StorageSolverOptions.step`, the BESS efficiency
    parameters will be reduced based on time passed such that the efficiency matches the list derate at the end of
    each simulation year.

    - First value in the list must be 1.0 (year 0 has no degradation)
    - Example: For annual derates [1.0, .9915, 0.9856] and an initial charge efficiency of 98.5%, efficiency will
      decrease linearly in a step-wise fashion until it is :math:`.985*0.9915=97.66\\%` at the end of year 1 and
      :math:`0.985*0.9856=97.08\\%` at the end of year 2.
    - List length must be greater than or equal to :attr:`BatteryParams.term`
    """


class BatteryHVACParams(BaseModel):
    r"""Submodel for more detailed estimation of BESS HVAC losses. Requires ambient temperature time series as a
    simulation input"""

    container_temperature: float
    r"""Target temperature that BESS container is assumed to be maintained at
    
    - Units: |degrees|\ C
    - Example value: 25\ |degrees|\ C
    """
    cop: float
    r"""The HVAC’s coefficient of performance.

    - Example value: 3.0
    """
    u_ambient: float
    r"""The heat transfer coefficient between ambient and the container

    - Units: W/Km\ :sup:`2`
    - Example value: 100.0W/Km\ :sup:`2`
    """
    discharge_efficiency_container: float
    r"""The portion of the BESS’s discharge efficiency driven by losses within the battery container, i.e., cell, rack
    and BMS losses.
    
    - Must be a greater than :attr:`~BatteryParams.discharge_efficiency`.
    - Units: fraction
    - Example value: 0.98
    """
    charge_efficiency_container: float
    r"""The portion of the BESS’s charge efficiency driven by losses within the battery container, i.e., cell, rack and
    BMS losses.
    
    - Must be greater than :attr:`~BatteryParams.charge_efficiency`
    - Units: fraction
    - Example value: 0.98
    """
    aux_xfmr_efficiency: float
    r"""The efficiency of the transformer stepping down from medium voltage to the voltage of the HVAC system.

    - Units: fraction
    - Example value: 0.99
    """
    container_surface_area: float = 20.0
    r"""Surface area of a single BESS container over which it exchanges heat with the ambient. Generally should
    consider area in contact with the ground, depending on how :attr:`u_ambient` has been determined
    
    - Units: m\ :sup:`2`
    - Example value: 20.0 
    """
    design_energy_per_container: float = 750.0
    r"""Design energy capacity per each BESS container. Used to estimate the number of containers in the BESS, and
    (along with :attr:`container_surface_area`) the corresponding total surface area available for heat transfer
    
    - Units: kWh
    - Example value: 750.0kWh
    """


class BoundedFloat(BaseModel):
    r""":meta private:"""

    actual: float
    min: float
    max: float


class BoundedFloatArray(BaseModel):
    r""":meta private:"""

    actual: t.List[float]
    min: t.List[float]
    max: t.List[float]

    def __len__(self) -> int:
        """Return the length of the actual array."""
        return len(self.actual)


class BatteryParams(BaseModel):
    r"""Inputs for modeling the physical performance of a BESS"""

    power_capacity: float
    r"""The maximum usable capacity of the battery to draw power to charge. Assumed to be equivalent for charge and
    discharge. For hybrid simulations, represents maximum power at coupling bus. For standalone storage simulations,
    represents maximum power at the point of interconnection or at the bus specified in
    :attr:`DownstreamSystem.model_losses_from` if applicable
    
    - Units: kW
    - Example value: 1000kW 
    """
    energy_capacity: float
    r"""The maximum usable capacity of the battery to store energy.
    
    - Units: kWh
    - Example value: 2000kWh
    """
    charge_efficiency: t.Union[float, BoundedFloat]
    r"""The percentage of energy stored for every kW of power drawn to charge. For hybrid simulations, should account
    for all losses up to the coupling bus. For standalone storage simulations, should account for all losses up to the
    point of interconnection or all losses up to the bus specified in :attr:`DownstreamSystem.model_losses_from`. If
    :attr:`hvac` is defined, *should not* account for BESS HVAC load.
    
    - Units: fraction
    - Example value: 0.965
    """
    discharge_efficiency: t.Union[float, BoundedFloat]
    r"""The percentage of energy discharged for every kW of power drawn to discharge. For hybrid simulations, should
    account for all losses up to the coupling bus. For standalone storage simulations, should account for all losses
    up to the point of interconnection or all losses up to the bus specified in
    :attr:`DownstreamSystem.model_losses_from`. If :attr:`hvac` is defined, *should not* account for BESS HVAC load.
    
    - Units: fraction
    - Example value: 0.965
    """
    self_discharge_rate: t.Optional[float] = None
    r"""Ratio of self-discharge power to SOE, applied when the battery is idle. If a value is provided, 
    self-discharge is calculated like: :math:`self_discharge_rate * SOE`. If ``None``, no self-discharge occurs.
    
    - Units: kW/kWh
    - Example value: 0.01
    """
    parasitic_soe_loss: t.Optional[float] = None
    r"""Constant power drain on SOE. This is only an internal SOE loss; it doesn't add to metered discharge.
    
    - Units: kW
    - Example value: 100kW
    """
    degradation_rate: t.Optional[float] = None
    r"""The approximate year over year (YoY) decrease in storage energy capacity due to cycling. Even though it is a YoY
    value, this specifies a throughput degradation model, meaning the battery degrades this percentage every
    :attr:`degradation_annual_cycles` cycles. At the end of each solver step as defined by
    :attr:`StorageSolverOptions.step`, the BESS capacity will be reduced
    based on the number of cycles that have occurred.
    
    - Either this parameter or :attr:`capacity_degradation_model` must be specified. To model no degradation, simply
      set to 0.0
    - Units: fraction
    - Example: for a :attr:`degradation_rate` of 1% and attr:`degradation_annual_cycles` of 261, a simulation step
      where 2.5 cycles occur will reduce the BESS capacity by :math:`(0.01/261)*2.5=0.00958\\%`
    """
    degradation_annual_cycles: float = 261  # cycle / work day
    r"""Assumed number of annual cycles corresponding to :attr:`degradation_rate`. See :attr:`degradation_rate` for more
    details"""
    hvac: t.Optional[BatteryHVACParams] = None
    r"""Submodel for more accurately modeling the efficiency of a BESS as a function of temperature.
    
    - Requires ambient temperature as a simulation input
    - If ``None``, HVAC losses should be accounted for in :attr:`charge_efficiency` and :attr:`discharge_efficiency`
    - HVAC losses are applied at the medium voltage (MV) bus for DC and MV-coupled systems, but at the HV bus for
      HV-coupled systems
    """
    capacity_degradation_model: t.Optional[TableCapDegradationModel] = None
    r"""Specification of the storage energy capacity degradation model. This can be used as an alternative to
    :attr:`degradation_rate` and :attr:`degradation_annual_cycles`. Currently, only models of type
    :class:`TableCapDegradationModel` are supported.
    
    - Either this parameter or :attr:`degradation_rate` must be specified. To model no degradation, use
      :attr:`degradation_rate` and set to 0.0
    - If specified, must include enough data to cover the battery :attr:`term`
    """
    efficiency_degradation_model: t.Optional[TableEffDegradationModel] = None
    r"""Specification of the storage charge and discharge efficiency degradation model. Current, only models of type
    TableEffDegradationModel are supported. If ``None``, no efficiency degradation is modeled
    
    - If specified, must include enough data to cover the battery :attr:`term`
    """
    term: t.Optional[float] = None
    r"""The number of years this specific battery will be active.

    - When multiple batteries are given in :attr:`MultiStorageInputs.batteries`, this parameter is required and used to
      specify replacement/augmentation
    - In this case, the total of all battery terms needs to match the timespan of :attr:`PVStorageModel.energy_prices`
      or :attr:`StandaloneStorageModel.energy_prices`
    - Only optional if a single battery is specified in :attr:`MultiStorageInputs.batteries`. In this case the term is
      assumed to be equivalent to the project term
    """

    @model_validator(mode="after")
    def dont_support_eff_deg_w_bounded_eff(self):
        if isinstance(self.discharge_efficiency, BoundedFloat) or isinstance(self.charge_efficiency, BoundedFloat):
            assert (
                self.efficiency_degradation_model is None
            ), "Efficiency degradation is not supported when using bounded efficiencies"
        return self

    @model_validator(mode="after")
    def check_cap_degradation_models(self):
        assert not (
            self.degradation_rate is None and self.capacity_degradation_model is None
        ), "Either degradation_rate or capacity_degradation_model must be specified"
        assert (
            self.degradation_rate is None or self.capacity_degradation_model is None
        ), "Only one of degradation_rate and capacity_degradation_model may be specified"
        return self

    @model_validator(mode="after")
    def check_degrad_table_length(self):
        term = self.term or 0  # validate against term if term is provided
        if self.capacity_degradation_model is not None:
            assert (
                len(self.capacity_degradation_model.annual_capacity_derates) - 1 >= term
            ), "annual_capacity_derates must be long enough to cover battery term"
        if self.efficiency_degradation_model is not None:
            assert (
                len(self.efficiency_degradation_model.annual_efficiency_derates) - 1 >= term
            ), "annual_efficiency_derates must be long enough to cover battery term"
        return self


class EnergyStrategy(str, Enum):
    r"""Enum for specifying energy market participation strategy"""

    da = "DA"
    r"""Make quantity-only bids into the day-ahead market and do not bid into the real-time market. Real-time
    participation will only cover day-ahead bids, but resource is still exposed to real-time prices if participating in
    ancillary/reserve markets with non-zero utilization
    """
    rt = "RT"
    r"""Make quantity-only bids into real-time market and do not bid into the day-ahead market
    """
    dart = "DART"
    r"""Make quantity-only bids into both the day-ahead and real-time markets
    """

    def to_ops_strategy(self) -> OpsStrategy:
        return {
            "DA": OpsStrategy.da_qo_only,
            "RT": OpsStrategy.rt_qo_only,
            "DART": OpsStrategy.dart_qo,
        }[self]


class BidOfferStrategy(str, Enum):
    r""":meta private:"""

    quantity_only = "quantity-only"
    price_quantity = "price-quantity"
    awarded = "awarded"


class MarketConfig(BaseModel):
    r""":meta private:"""

    da: t.Optional[BidOfferStrategy] = None
    rt: t.Optional[BidOfferStrategy] = None

    @field_validator("rt")
    @classmethod
    def valid_rt_configs(cls, v):
        if v not in {BidOfferStrategy.quantity_only, BidOfferStrategy.awarded, None}:
            raise ValueError("only quantity-only supported for RTM")
        return v

    @property
    def independent_dam(self) -> bool:
        return self.da is not None and self.rt is not None

    @property
    def value(self) -> str:
        r"""For symmetry with EnergyStrategy"""
        return json.dumps({"DAM": self.da.value, "RTM": self.rt.value})


def default_market_config_factory():
    return MarketConfig(
        da=BidOfferStrategy.quantity_only,
        rt=None,
    )


default_market_config = default_market_config_factory()


def translate_market_config_to_ops_strategy(v: MarketConfig) -> OpsStrategy:
    match v:
        case MarketConfig(da=BidOfferStrategy.price_quantity, rt=BidOfferStrategy.quantity_only):
            return OpsStrategy.dart_pq_qo
        case MarketConfig(da=BidOfferStrategy.awarded, rt=BidOfferStrategy.quantity_only):
            return OpsStrategy.rt_redispatch_qo
        case MarketConfig(da=BidOfferStrategy.quantity_only, rt=None):
            return OpsStrategy.da_qo_only
        case MarketConfig(da=None, rt=BidOfferStrategy.quantity_only):
            return OpsStrategy.rt_qo_only
        case MarketConfig(da=BidOfferStrategy.quantity_only, rt=BidOfferStrategy.quantity_only):
            return OpsStrategy.dart_qo
        case MarketConfig(da=BidOfferStrategy.awarded, rt=BidOfferStrategy.awarded) | MarketConfig(da=None, rt=None):
            return OpsStrategy.fixed_energy
    raise ValueError(f"Invalid energy strategy: {v}")


class OpsStrategy(str, Enum):
    fixed_energy = "no_energy"
    r"""Assume fixed awards in both energy markets. Ancillary services can still be offered."""
    da_qo_only = "da_qo_only"
    r"""Make quantity-only bids into the day-ahead energy and ancillary markets and do not bid into the real-time 
    market. Real-time participation will only cover day-ahead bids, but resource is still exposed to real-time 
    prices if participating in ancillary/reserve markets with non-zero utilization.
    """
    rt_qo_only = "rt_qo_only"
    r"""Make quantity-only bids into the real-time market and do not bid into the day-ahead market.
    """
    dart_qo = "dart_qo"
    r"""Make quantity-only bids into both the day-ahead and real-time markets.
    """

    dart_pq_qo = "dart_pq_qo"
    r"""Price-quantity bid-offers in DAM with quantity-only bid-offers in RTM
    """
    rt_redispatch_qo = "rt_redispatch_qo"
    r"""Quantity-only RTM bid-offers with DA & ancillaries already awarded.
    """
    rt_redispatch_qo_rtcb = "rt_redispatch_qo_rtcb"
    r"""Quantity-only RTM bid-offers with DA & ancillaries already awarded.
        The AS day-ahead obligations are treated as financial obligations only. They are not physically enforced.
    """


class PublicOpsStrategy(str, Enum):
    fixed_energy = OpsStrategy.fixed_energy.value
    da_qo_only = OpsStrategy.da_qo_only.value
    rt_qo_only = OpsStrategy.rt_qo_only.value
    dart_qo = OpsStrategy.dart_qo.value
    rt_redispatch_qo = OpsStrategy.rt_redispatch_qo.value


class StorageSolverOptions(BaseModel):
    r"""Inputs related to BESS market participation and optimization"""

    cycling_cost_adder: float = 0.0
    r"""A hurdle rate to add costs in the optimization framework to reduce cycling. This value is often set at around
    the Variable O&M cost or the expected cost of degradation.

    - Units: $/MWh
    - Example value: $15/MWh
    """
    annual_cycle_limit: t.Optional[float] = None
    r"""The maximum number of complete cycles per year. A cycle is measured as the throughput equivalent of the energy
    capacity fully charging and discharging. 

    - Units: N/A
    - Example value: 250
    """
    disable_intra_interval_variation: bool = True
    r""":meta private:"""
    window: t.Optional[int] = None
    r"""The number of time intervals that the optimization framework has knowledge of with respect to constraints. The
    optimization is rolling and optimizes for each :attr:`step` with the benefit of foresight into the broader window.

    - Default value: 24 (for a single day) for hourly runs
    """
    step: t.Optional[int] = None
    r"""The number of intervals of a single optimization period.

    - For example: for the default hourly run, a step of 24 means the optimization sets charge and discharge schedules
      for a single day.
    - Default value: 24 (for a single day) for hourly runs
    """
    flexible_solar: bool = False
    r"""Whether or not to include solar curtailment in Ancillary Services offers. Only relevant for
    :class:`PVStorageModel` simulations

    - ``True`` will allow for solar bids into AS markets
    - ``False`` will not. Ancillary Service participation will come exclusively from the battery in this scenario.
    """
    symmetric_reg: Annotated[
        Optional[bool],
        get_deprecator(
            "symmetric_reg is deprecated and will be removed in the future. Use SymmetricReserveMarket instead."
        ),
    ] = None
    r"""Deprecated, specify :class:`SymmetricReserveMarket` in :attr:`reserve_markets` instead.
    
    *Whether or not regulation markets are symmetric. This will depend on the market you are participating in.*
    
    - If ``True``, :attr:`ReserveMarkets.up` and :attr:`ReserveMarkets.down` must contain ``"reg_up"`` and
      ``"reg_down"`` items respectively. Their prices must also be equivalent.
    """
    energy_strategy: t.Optional[t.Union[EnergyStrategy, MarketConfig, PublicOpsStrategy]] = None
    r"""Specifies energy market participation strategy
    """
    dart: Annotated[
        Optional[bool],
        get_deprecator("dart is deprecated and will be removed in the future. Use energy_strategy instead."),
    ] = None
    r"""Deprecated, use :attr:`energy_strategy` to specify co-optimization
    
    *Whether or not to include DA/RT co-optimization in the Energy Markets*

    - *Default value: False*
    """
    uncertain_soe: bool = True
    r"""Whether or not to consider SOE at the beginning of each optimization window as uncertain or not
    
    :meta private:
    """
    dam_annual_cycle_limit: t.Optional[float] = None
    r""":meta private:"""
    no_virtual_trades: Annotated[
        t.Optional[bool],
        get_deprecator(
            "no_virtual_trades is deprecated and will be removed in the future. Use minimum_dam_coverage_fraction instead. "
            "(Setting minimum_dam_coverage_fraction to 1.0 is equivalent to no_virtual_trades=True) "
            "(Setting minimum_dam_coverage_fraction to 0.0 is equivalent to no_virtual_trades=False) "
        ),
    ] = None
    minimum_dam_coverage_fraction: Annotated[float, Field(ge=0.0, le=1.0)] = 0.0
    r"""Whether or not virtual trades should be considered during DA/RT co-optimization
    
    - Only relevant if :attr:`energy_strategy` is :attr:`~EnergyStrategy.dart`
    - Requires that :attr:`PVStorageModel.energy_prices`/:attr:`StandaloneStorageModel.energy_prices` is type
      :class:`DARTPrices`
    - If ``False``, real-time participation (i.e actual charge and discharge) is not required to cover day-ahead
      bids. Instead the optimizer assumes day-ahead bids can also be covered by buying energy in the real-time market.
      With perfect foresight of DA and RT prices, this approach seems highly lucrative, but doesn't reflect price
      uncertainty during actual operation and the associated level of market exposure
    - If ``True``, real-time participation is required to cover day-ahead market bids, but can participate beyond
      that. May still require real-time energy buys if participating in ancillary/reserve markets with non-zero
      utilization
    """
    # TODO: Allen to confirm ^
    initial_soe: t.Union[float, BoundedFloat] = 0.0
    r"""State-of-Energy of BESS at beginning of simulation
    
    - Units: kWh
    """
    duration_requirement_on_discharge: bool = True  # True for ERCOT
    r"""Whether :attr:`ReserveMarket.duration_requirement` applies to the entire reserve offer, or just the discharge
    side of the offer. ERCOT currently only constrains the discharge side. This means that if a BESS is offering to
    reduce the amount it is charging (rather than increasing the amount it is discharging) the offer will not be
    subject to the duration requirement."""
    no_stop_offers: bool = False
    r"""Whether or not reserve capacity can be called against a base point in the opposite direction. By default,
    if the battery is discharging, it can be called via a reg down award to discharge less (aka to "stop"). Setting
    `no_stop_offers=True` prevents this, such that battery cannot simultaneously have a discharging base point and a
    downward reserves award, nor a charging base point with an upward reserves award. This hurts the battery's ability
    to profit off of reserve markets, but makes for more conservative RT behavior."""
    solver_config: StrictSolverConfig = StrictSolverConfig()
    r"""Inputs related to how the solution is actually carried out
    
    :meta private:
    """
    robust_range_initial_soe: bool = False
    r"""Interpret a BoundedFloat passed as initial_soe as a set of three different SOE scenarios to model, using the 
    "actual" scenario to compute RT revenue
    
    :meta private:
    """
    rtm_bp_tol: t.Optional[float] = None
    r"""The tolerance in kW within which the optimizer will keep the RTM base point despite solar uncertainty. This is 
    only applicable when using uncertain solar."""
    rtm_bp_curtailable: bool = True  # TODO: False may break if solar exceeds limit
    r""":meta private:"""

    @model_validator(mode="before")
    @classmethod
    def coerce_virtual_trades(cls, values: dict) -> dict:
        """
        Coerce old no_virtual_trades into new minimum_dam_coverage_fraction
        """
        # Check which fields were explicitly set by the user
        tol_set = "minimum_dam_coverage_fraction" in values
        flag_set = "no_virtual_trades" in values and values.get("no_virtual_trades") is not None

        if tol_set and flag_set:
            raise ValueError("Only one of 'minimum_dam_coverage_fraction' or 'no_virtual_trades' can be set.")

        if flag_set and not tol_set:
            values["minimum_dam_coverage_fraction"] = 1.0 if values["no_virtual_trades"] else 0.0
            del values["no_virtual_trades"]

        return values

    @model_validator(mode="after")
    def coerce_energy_strategy_to_ops_strategy(self):
        assert not (self.dart is not None and self.energy_strategy is not None), (
            "Only one of `dart` or `energy_strategy` may be provided. `dart` is deprecated; use `energy_strategy`"
            " instead."
        )
        if self.energy_strategy is None:
            self.energy_strategy = OpsStrategy.dart_qo if self.dart else OpsStrategy.da_qo_only
            self.dart = None
        if isinstance(self.energy_strategy, EnergyStrategy):
            self.energy_strategy = self.energy_strategy.to_ops_strategy()
        elif isinstance(self.energy_strategy, MarketConfig):
            self.energy_strategy = translate_market_config_to_ops_strategy(self.energy_strategy)

        if self.energy_strategy != OpsStrategy.dart_qo:
            if self.dam_annual_cycle_limit is not None:
                raise ValueError("Must model separate dam and rtm markets if dam_annual_cycle_limit is set")
            if self.minimum_dam_coverage_fraction > 0.0:
                raise ValueError(
                    "Must model separate dam and rtm markets if minimum_dam_coverage_fraction is set to a >0 value"
                )
        return self


class MultiStorageInputs(StorageSolverOptions):
    r"""Inputs related to BESS design, market participation and optimization"""

    batteries: t.List[BatteryParams]
    r"""List of :class:`BatteryParams` objects that models replacement/augmentation of the BESS over a project's life.
    
    - Each :class:`BatteryParams` object is modeled for its :attr:`~BatteryParams.term` and then the BESS is assumed
      to be replaced and the SOE is assumed to be reset to :attr:`initial_soe`
    - To model a single battery over the project lifetime with no augmentation simply provide a list of length 1. In
      this case. :attr:`~BatteryParams.term` is ignored and the battery term is assumed to be equivalent to the project
      term.
    """

    @field_validator("batteries")
    @classmethod
    def check_battery_terms(cls, v):
        if len(v) > 1:  # don't worry about terms if there's only one battery
            for battery in v:
                assert battery.term, "if multiple batteries are provided, terms must also be provided"
        return v


def _get_price_str_and_price(values: MarketBase) -> t.Tuple[str, t.Union[t.List[float], DARTPriceScenarios]]:
    if isinstance(values.energy_prices, DARTPrices):
        return "rtm prices", values.energy_prices.rtm
    elif isinstance(values.energy_prices, DARTPriceScenarios):
        return "rtm price", values.energy_prices
    else:
        return "energy_prices", values.energy_prices


class PeakWindow(BaseModel):
    r"""Inputs that describe peak to be reduced as part of :class:`LoadPeakReduction`"""

    mask: t.List[bool]
    r"""Time series of boolean values where ``True`` indicates that a time intervals should be considered when
    calculating a peak load that will be valued at :attr:`price`.
    
    - List length must match RTM prices
    """
    price: float
    r"""Price to be applied to the peak load calculated for all the time intervals defined by :attr:`mask`
    """


class LoadPeakReduction(BaseModel):
    r"""Submodel for incorporating behind the meter (BTM) peak load/demand charge reduction in the BESS optimization
    for the purposes of reducing demand charges.
    """

    # TODO: Add docs at some point for devs
    load: t.List[float]
    r"""The BTM load that will be subject to peak reduction as part of BESS optimization
    
    - Units: kW
    - Values should match the RTM price time interval and list length
    """

    max_load: t.List[float]  # TODO: should be optional -- https://app.asana.com/0/1178990154879730/1203603348130562/f
    r"""Similar to :attr:`load` but only considered during the determination of load target peaks for the
    :attr:`seasonal_peak_windows` (as opposed to in the
    final optimization). An actual operating project will need to define e.g. a monthly target peak at the beginning of
    the month, when forecast uncertainty for later in the month is high. The difference between :attr:`max_load` and
    :attr:`load` can be used to reflect this imperfect foresight in the determination of target peaks. E.g.
    :attr:`max_load` might be a P05 estimate compared to :attr:`load` being a P50.
    
    - Units: kW
    - Ignored unless modeling :attr:`seasonal_peak_windows`
    - Values should match the RTM price time interval and list length
    - **Note that if both** :attr:`seasonal_peak_windows` **and** :attr:`daily_peak_windows` **are considered (such
      that a one-day simulation** :attr:`~StorageSolverOptions.window` **is used) :attr:`max_load` **should be at
      least 1.1 times** :attr:`load` **in order to ensure optimal behavior. Please contact Tyba if more detail is
      needed.**
    """
    # TODO: Confirm with Allen that the discussion of step size is accurate

    seasonal_peak_windows: t.List[PeakWindow] = []
    r"""List of :class:`PeakWindow` objects intended to represent demand charges that apply to time spans larger than
    the simulation window, e.g. monthly demand charges vs a 1-2 day simulation window. For each of these demand
    charges, prior to the main optimization calculation, a target peak is calculated that represents the maximum
    reduction that can be achieved for all intervals in the :attr:`PeakWindow.mask`. This target peak is then used in
    each window of the main optimization calculation. Care should be taken when transforming a tariff into
    :attr:`seasonal_peak_windows`. For example, consider a "winter on peak" monthly demand charge that
    applies from 6-10 and 15-19 on weekdays in months 1, 2, 3, 4, 11, and 12. This single charge would be represented
    by 6 :class:`PeakWindow` objects, where e.g. the month 1 :attr:`~PeakWindow.mask` would only have ``True`` values
    matching the tariff schedule in month 1, and ``False`` for all time intervals in all other months. 
    """
    daily_peak_windows: t.List[PeakWindow] = []
    r"""List of :class:`PeakWindow` objects intended to represent demand charges that apply to time spans equal to the
    simulation window, e.g. daily demand charges and a 1 day simulation window. Unlike :attr:`seasonal_peak_windows`,
    target peaks are not calculated and the peak power in each simulation window is minimized. As such, a
    "winter on peak" daily demand charge that applies from 6-10 and 15-19 on weekdays in months 1, 2, 3, 4, 11, and 12
    could be represented by a single :class:`PeakWindow` object, where each simulation window will consider a
    "submask" of :attr:`~PeakWindow.mask`.
    
    - **Note that peak reduction considers the entire simulation** :attr:`~StorageSolverOptions.window`, **so a 2 day
      simulation window will minimize the peak across both days. As such, to model daily demand charges, make sure to
      use a one-day simulation window. See** :attr:`max_load` **for more caveats.**
    """

    @model_validator(mode="after")
    def check_lengths(self):
        windows = [*self.seasonal_peak_windows, *self.daily_peak_windows]
        assert (
            windows
        ), "One or both of seasonal_peak_windows and daily_peak_windows must be provided when using load_peak_reduction"
        length = len(self.load)
        assert len(self.max_load) == length, "load and max_load must have same length"
        for window in windows:
            assert len(window.mask) == length, "peak masks must have same length as load"
        return self

    def __len__(self) -> int:
        return len(self.load)


class ImportExportLimitMixin(BaseModel):
    r"""Mixin class for applying import and export constraints to simulation class objects

    :meta private:
    """

    import_limit: t.Optional[t.List[float]] = None
    r"""Time series of limit values to be applied to import
    
    - Power values correspond to the time interval given by :attr:`time_interval_mins` and the list length must match
      RTM prices
    - All values should be <= 0
    - Units: kW
    - Example values: [-1000.0, -1000.0, 0, 0,] 
    """
    export_limit: t.Optional[t.List[float]] = None
    r"""Time series of limit values to be applied to export

    - Power values correspond to the time interval given by :attr:`time_interval_mins` and the list length must match
      RTM prices
    - All values should be >= 0
    - Units: kW
    - Example values: [1000.0, 1000.0, 0, 0,] 
    """

    @model_validator(mode="after")
    def validate_limits(self):
        if self.import_limit is not None:
            assert all([v <= 0 for v in self.import_limit]), "import_limit must be <= 0"
        if self.export_limit is not None:
            assert all([v >= 0 for v in self.export_limit]), "export_limit must be >= 0"
        return self

    @model_validator(mode="after")
    def check_import_export_lengths(self):
        for k in "import_limit", "export_limit":
            if limit := getattr(self, k):
                price_str, price = _get_price_str_and_price(self)
                _check_lengths({k: limit, price_str: price})
        return self


def _check_degrad_table_length(values: t.Union[PVStorageModel, StandaloneStorageModel]):
    if len(values.storage_inputs.batteries) == 1:
        battery = values.storage_inputs.batteries[0]
        pt = (
            scale_project_term_to_hours(
                values.project_term or values.pv_inputs.project_term,
                values.project_term_units or values.pv_inputs.project_term_units,
            )
            / 8760
        )
        for dm in "capacity", "efficiency":
            if dm_ob := getattr(battery, f"{dm}_degradation_model"):
                tbl_yrs = len(getattr(dm_ob, f"annual_{dm}_derates")) - 1
                assert tbl_yrs >= pt, f"annual_{dm}_derates must be long enough to cover project/battery term"
    return values


def _check_symmetric_reg_inputs(values: t.Union[PVStorageModel, StandaloneStorageModel]):
    if values.storage_inputs.symmetric_reg:
        assert values.reserve_markets, "when storage_inputs.symmetric_reg is True, reserve_markets must be provided"
        assert ("reg_up" in (values.reserve_markets.up or dict())) and (
            "reg_down" in (values.reserve_markets.down or dict())
        ), "when storage_inputs.symmetric_reg is True, both reg_up and reg_down reg markets must be provided"

    return values


def _check_redispatch_arguments(values):
    if values.storage_inputs.energy_strategy is OpsStrategy.rt_redispatch_qo:
        assert values.dam_award is not None, "DAM award must be provided if energy_strategy is rt_redispatch_qo"
        assert values.rtm_award is None, "RTM award must be None if energy_strategy is rt_redispatch_qo"


class PVStorageModel(ImportExportLimitMixin, MarketBase):
    r"""Simulation class for hybrid simulations.
    :class:`~generation_models.v0_output_schema.PVStorageModelResults` is the results schema"""

    project_type: t.Literal["hybrid"] = "hybrid"
    r"""Used by the API for model-type discrimination, can be ignored"""
    storage_coupling: StorageCoupling
    r"""Specify the point at which the BESS and generation source are coupled"""
    pv_inputs: GenerationModel
    r"""Submodel for PV or external power generation. Can be either a :class:`PVGenerationModel`,
    :class:`DCExternalGenerationModel`, or :class:`ACExternalGenerationModel` instance
    """
    enable_grid_charge_year: Annotated[t.Optional[float], Field(ge=0)] = None
    r"""The time in years after which grid-charging becomes allowed. The default `None` disallows grid-charging for
    the entirety of the simulation. This value is 0-indexed, i.e., a value of 5 will enable grid-charging at the start
    of the 6th year.

    Examples:
    - To allow grid-charging from the beginning of the term, set this to 0.
    - To disallow grid-charging for the entirety of the term, leave this set to None (the default).
    - To enable grid-charging after the project has been running for 5 years (at the start of the 6th year), set this to 5.
    - To enable grid-charging after the project has been running for 6 months, set this value to 0.5.
    """
    solar_revenue_adder: t.Optional[t.Union[t.List[float], float]] = None
    r"""Price (or prices) to be assigned as additional revenue earned by solar. Can be used to model Renewable Energy
    Credit (REC) revenue or Production Tax Credit (PTC) revenue.
    
    - Can be either a single price (applied uniformly to all time steps) or a list of prices
    - If provided as a list, prices correspond to the time interval given by :attr:`time_interval_mins` and the list
      length must match the sum of all battery terms when given in the chosen time interval.
    """

    @property
    def project_term(self) -> int:
        r"""Equivalent to e.g. :attr:`PVGenerationModel.project_term` provided in :attr:`pv_inputs`"""
        return self.pv_inputs.project_term

    @property
    def project_term_units(self) -> TermUnits:
        r"""Equivalent to :attr:`PVGenerationModel.project_term_units` provided in :attr:`pv_inputs`"""
        return self.pv_inputs.project_term_units

    @model_validator(mode="after")
    def check_dam_award_against_config(self):
        _check_redispatch_arguments(self)
        return self

    @model_validator(mode="after")
    def check_time_intervals(self):
        assert (
            self.time_interval_mins <= self.pv_inputs.time_interval_mins
        ), "price time_interval_mins must less than or equal to pv time_interval_mins"
        return self

    @model_validator(mode="after")
    def check_price_time_interval_against_pv_project_term(self):
        price_str, price = _get_price_str_and_price(self)
        _check_time_interval_project_term(
            len(price),
            price_str,
            self.pv_inputs.project_term,
            self.time_interval_mins,
            self.pv_inputs.project_term_units,
        )
        return self

    @model_validator(mode="after")
    def check_battery_terms(self):
        if len(self.storage_inputs.batteries) > 1:
            total_batt_yrs = sum(bat.term for bat in self.storage_inputs.batteries)
            assert (
                scale_project_term_to_hours(self.pv_inputs.project_term, self.pv_inputs.project_term_units)
                >= total_batt_yrs * 8760
            ), "project_term must be greater than or equal to the total battery terms"
        return self

    @model_validator(mode="after")
    def check_degrad_table_length(self):
        return _check_degrad_table_length(self)

    @model_validator(mode="after")
    def check_sym_reg_inputs(self):
        return _check_symmetric_reg_inputs(self)

    @model_validator(mode="after")
    def check_solar_adder_length(self):
        if self.solar_revenue_adder and isinstance(self.solar_revenue_adder, list):
            if isinstance(self.energy_prices, DARTPrices):
                rtm = self.energy_prices.rtm
            elif isinstance(self.energy_prices, DARTPriceScenarios):
                rtm = self.energy_prices.rtm[0]
            else:
                rtm = self.energy_prices
            _check_lengths({"rtm prices": rtm, "solar revenue adder": self.solar_revenue_adder})
        return self


class StandaloneStorageModel(ProjectTermMixin, ImportExportLimitMixin, MarketBase):
    r"""Simulation class for standalone storage simulations. The results schema is
    :class:`~generation_models.v0_output_schema.StandaloneStorageModelWithDownstreamResults` if
    a downstream system is specified, otherwise the schema
    is :class:`~generation_models.v0_output_schema.StandaloneStorageModelSimpleResults`"""

    parallel_chunks: t.Optional[int] = None
    r"""Number of parallel chunks to use for the simulation"""
    project_type: t.Literal["storage"] = "storage"
    r"""Used by the API for model-type discrimination, can be ignored"""
    downstream_system: t.Optional[DownstreamSystem] = None
    r"""Optional submodel for detailed treatment of losses. The point at which detailed losses are considered can be
    controlled with :attr:`DownstreamSystem.model_losses_from`
    """
    ambient_temp: t.Optional[t.Union[t.List[float], SolarResourceLocation]] = None
    r"""Optional ambient temperature data to be used with :attr:`BatteryParams.hvac`. Can take multiple argument types:
    
    - A time-series list of ambient temperature with length equivalent to the real-time market time-series in
      :attr:`energy_prices`
    - A :class:`SolarResourceLocation` object. With this type, Tyba will pull TY ambient temperature data from
      the `NSRDB <https://nsrdb.nrel.gov/>`__ and use it in the simulation. As such, additional requirements are placed
      on the data in :attr:`energy_prices` and :attr:`project_term`:
    
      - The data in :attr:`energy_prices` must represent a period starting in the 0th hour of January 1st (to align
        with the pulled ambient temperature data)
      - :attr:`project_term` must be equivalent to a number of whole years (so that the ambient temperature data can be
        tiled to match)
    
    - Units: |degrees|\ C
    """

    # note we don't allow a simple lat/lon tuple here^ because once things get converted to json you can't tell the
    # diff between a list and a tuple. Solar resource doesn't have that problem because it is never just a list

    @model_validator(mode="after")
    def check_dam_award_against_config(self):
        _check_redispatch_arguments(self)
        return self

    @model_validator(mode="after")
    def check_ambient_temp_length(self):
        if self.ambient_temp:
            if isinstance(self.ambient_temp, SolarResourceLocation):
                assert (scale_project_term_to_hours(self.project_term, self.project_term_units) % 8760 == 0) and (
                    scale_project_term_to_hours(self.project_term, self.project_term_units) >= 8760
                ), (
                    "project term must be equivalent to a number of whole years when ambient temperature data is based"
                    " on solar resource location"
                )
            else:
                price_str, price = _get_price_str_and_price(self)
                _check_lengths({price_str: price, "ambient_temp": self.ambient_temp})
        return self

    @model_validator(mode="after")
    def check_time_interval_project_term(self):
        price_str, price = _get_price_str_and_price(self)
        _check_time_interval_project_term(
            len(price), price_str, self.project_term, self.time_interval_mins, self.project_term_units
        )
        return self

    @model_validator(mode="after")
    def check_battery_and_project_terms(self):
        # only validate battery terms if a battery term is passed or multiple batteries are passed
        if len(self.storage_inputs.batteries) > 1 or self.storage_inputs.batteries[0].term is not None:
            total_batt_yrs = sum(bat.term for bat in self.storage_inputs.batteries)
            project_term_hours = scale_project_term_to_hours(self.project_term, self.project_term_units)
            total_battery_term_hours = int(total_batt_yrs * 8760)
            assert (
                project_term_hours == total_battery_term_hours
            ), "project_term must be consistent with the total battery terms"
            price_str, price = _get_price_str_and_price(self)
            price_hours = int(len(price) * (self.time_interval_mins / 60))
            assert (
                price_hours >= total_battery_term_hours
            ), f"length of {price_str} must be greater than total battery terms"
        return self

    @model_validator(mode="after")
    def check_degrad_table_length(self):
        return _check_degrad_table_length(self)

    @model_validator(mode="after")
    def check_sym_reg_inputs(self):
        return _check_symmetric_reg_inputs(self)


def get_pv_model(**data: t.Any) -> GenerationModel:
    r""":meta private:"""
    try:
        m = PVGenerationModel(**data)
    except ValidationError:
        try:
            m = DCExternalGenerationModel(**data)
        except ValidationError:
            m = ACExternalGenerationModel(**data)
    return m


def get_pv_storage_model(**data: t.Any) -> PVStorageModel:
    r""":meta private:"""
    return PVStorageModel(**data)


def get_standalone_storage_model(model: dict) -> StandaloneStorageModel:
    r""":meta private:"""
    return StandaloneStorageModel(**model)


JobModel = create_optionally_discriminant_union(
    union=t.Union[StandaloneStorageModel, PVStorageModel, GenerationModel], discriminator="project_type"
)


class ResultsFormat(str, Enum):
    r"""Desired format in which simulation results will be stored and returned"""

    v0 = "v0"
    r"""Default return format, see e.g.
    :class:`~generation_models.v0_output_schema.GenerationModelResults`
    """
    v1 = "v1"
    r"""Also known as bus format, similar to v0 but time_series power flow data is formatted as a dict with tuple keys
    
    - first key element approximately represents the associated hardware component and the second element
      indicates the signal name, e.g. ("inverter", "clipping_loss_kW") or ("mv_bus", "power_kW").
    - Inspection of returned result is required.
    """
    v2 = "v2"
    r"""Nested time series format, see e.g.
    :class:`~generation_models.v2_output_schema.GenerationModelResults`
    """


class AsyncModelBase(BaseModel):
    r""":meta private:"""

    id: str
    model: JobModel
    results_format: ResultsFormat = "v0"
    results_path: t.Optional[str] = None


class AsyncPVModel(AsyncModelBase):
    r""":meta private:"""

    id: str
    model: GenerationModel


class AsyncPVStorageModel(AsyncModelBase):
    r""":meta private:"""

    id: str
    model: PVStorageModel


class AsyncStandaloneStorageModel(AsyncModelBase):
    r""":meta private:"""

    id: str
    model: StandaloneStorageModel
