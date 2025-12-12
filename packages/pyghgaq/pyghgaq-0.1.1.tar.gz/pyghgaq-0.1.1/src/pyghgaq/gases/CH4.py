import numpy as np
from pint.facets.plain import PlainQuantity

from pyghgaq.functions.read import read_constant
from pyghgaq.functions.units import Q_, get_default_units
from pyghgaq.registry.registry import enforce_units, register_hcp, register_schmidt


@register_hcp("CH4", "Wiesenburg")
@enforce_units(
    unit_getter=get_default_units,
    unit_map={"temp": "Temperature", "salt": "Salinity", "catm": "Gas_Concentration"},
)
def hcp_sal_ch4(
    varname: str,
    temp: PlainQuantity,
    salt: PlainQuantity,
    catm: PlainQuantity,
    units: dict[str, str],
) -> PlainQuantity:

    salt = salt.to("PSU")
    temp = temp.to("K")
    catm = catm.to("ppm")

    constant = read_constant()
    A = constant[varname]["A"]
    B = constant[varname]["B"]

    salt = salt.magnitude
    fx = catm.to_base_units().magnitude
    temp = temp.magnitude

    c_molm3 = Q_(
        np.exp(
            +np.log(fx)
            + A[0]
            + A[1] * 100 / temp
            + A[2] * np.log(temp / 100)
            + A[3] * (temp / 100)
            + salt * (B[0] + B[1] * temp / 100 + B[2] * (temp / 100) ** 2)
        ),
        "nmol L^-1",
    )
    hcpsalt = c_molm3.to("mol m^-3") / (Q_(1, "atm").to("Pa") * fx)
    return hcpsalt


@register_hcp("CH4", "Sanders")
def hcp_sanders(
    varname: str,
    temp: PlainQuantity,
    units: dict[str, str],
) -> PlainQuantity:

    temp = temp.to("K")
    constant = read_constant()
    hcp25 = Q_(constant[varname]["H_T25"], "mol m^-3 Pa^-1")
    dlnHcpd1_T = Q_(constant[varname]["dlnHdT"], "K")
    hcp_t = hcp25 * np.exp(dlnHcpd1_T * (1 / temp - 1 / Q_(298.15, "K")))
    return hcp_t


@register_schmidt("CH4")
def sch_number(temp: PlainQuantity) -> np.ndarray | float:
    constant = read_constant()
    const = constant["CH4"]["SCH"][::-1]
    return np.polyval(const, temp.magnitude)

@register_schmidt("CH4-salt")
def sch_number_salt(temp: PlainQuantity) -> np.ndarray | float:
    constant = read_constant()
    const = constant["CH4"]["SCH-salt"][::-1]
    return np.polyval(const, temp.magnitude)
