from __future__ import annotations

import pandas as pd
from generation_models import SolarResource, SolarResourceTimeSeries
import typing as t


def solar_resource_from_psm_csv(filename: str, monthly_albedo: t.Optional[t.List[float]] = None) -> SolarResource:
    """Generate a solar resource input object from a PSM/SAM-formatted CSV file. Info on the PSM/SAM data format can be
    found in section 1.1 of this
    `PDF <https://sam.nrel.gov/images/web_page_files/sam-help-2020-2-29-r2_weather_file_formats.pdf>`__.

    :param filename: filepath to the CSV file
    :param monthly_albedo: optional specification of monthly average albedos to be used alongside the data in the CSV
      file. See :attr:`~generation_models.generation_models.SolarResource.monthly_albedo` for more information.
    :return: :class:`~generation_models.generation_models.SolarResource` object that can be passed into the simulation
      via the :attr:`~generation_models.generation_models.PVGenerationModel.solar_resource` attribute
    """
    with open(filename) as f:
        _meta = [f.readline().split(",") for _ in range(2)]
        _data = pd.read_csv(f)
    meta = {k: v for k, v in zip(*_meta)}
    data = _data.rename(columns=psm_column_map)
    return SolarResource(
        latitude=float(meta["Latitude"]),
        longitude=float(meta["Longitude"]),
        elevation=float(meta["Elevation"]),
        time_zone_offset=float(meta["Time Zone"]),
        data=SolarResourceTimeSeries(**data.to_dict(orient="list")),
        monthly_albedo=monthly_albedo,
    )


psm_column_map = {
    "Year": "year",
    "Month": "month",
    "Day": "day",
    "Hour": "hour",
    "Minute": "minute",
    "GHI": "gh",
    "DNI": "dn",
    "DHI": "df",
    "POA": "poa",
    "Temperature": "tdry",
    # twet
    "Dew Point": "tdew",
    "Relative Humidity": "rhum",
    "Pressure": "pres",
    # Snow
    "Surface Albedo": "alb",
    # aod
    "Wind Speed": "wspd",
    "Wind Direction": "wdir",
}
