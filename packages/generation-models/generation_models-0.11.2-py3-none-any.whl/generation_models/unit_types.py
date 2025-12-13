from __future__ import annotations
from typing_extensions import Annotated

# note the pattern here, we define a type to be used in the code (for devs benefit). The 2 strings are always
#  1) the type variable name and 2) the path to the variable
unit_types = [
    kW := Annotated[float, "kW", "unit_types.kW"],
    kWh := Annotated[float, "kWh", "unit_types.kWh"],
    V := Annotated[float, "V", "unit_types.V"],
    Wm2 := Annotated[float, "Wm2", "unit_types.Wm2"],
    Whm2 := Annotated[float, "Whm2", "unit_types.Whm2"],
    m2 := Annotated[float, "m2", "unit_types.m2"],
    deg := Annotated[float, "deg", "unit_types.deg"],
    degC := Annotated[float, "degC", "unit_types.degC"],
    dec := Annotated[float, "dec", "unit_types.dec"],
]
