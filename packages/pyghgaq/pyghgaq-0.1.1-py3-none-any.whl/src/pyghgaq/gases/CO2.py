import numpy as np
from pint import Quantity
from pint.facets.plain import PlainQuantity

from pyghgaq.functions.read import read_constant
from pyghgaq.functions.units import Q_, get_default_units
from pyghgaq.registry.registry import enforce_units, register_hcp, register_schmidt


@register_hcp("CO2", "Wiesenburg")
@enforce_units(
    unit_getter=get_default_units,
    unit_map={"temp": "Temperature", "salt": "Salinity"},
)
def hcp_sal_co2(
    varname: str, temp: PlainQuantity, salt: PlainQuantity, units: dict[str, str] = {}
) -> PlainQuantity:

    temp = temp.to("K")
    salt = salt.to("PSU")

    constant = read_constant()
    A = constant[varname]["A"]
    B = constant[varname]["B"]

    salt = salt.magnitude
    temp = temp.magnitude

    hcp: PlainQuantity = Q_(
        np.exp(
            +A[0]
            + A[1] * 100 / temp
            + A[2] * np.log(temp / 100)
            + salt * (B[0] + B[1] * temp / 100 + B[2] * (temp / 100) ** 2)
        ),
        "mol l^-1 atm^-1",
    )
    return hcp.to("mol m^-3 Pa^-1")


@register_hcp("CO2", "Sanders")
def hcp_sanders(
    varname: str,
    temp: PlainQuantity,
    units: dict[str, str] = {},
) -> Quantity:
    constant = read_constant()
    temp = temp.to("K")
    hcp25 = Q_(constant[varname]["H_T25"], "mol m^-3 Pa^-1")
    dlnHcpd1_T = Q_(constant[varname]["dlnHdT"], "K")
    hcp_t = hcp25 * np.exp(dlnHcpd1_T * (1 / temp - 1 / Q_(298.15, "K")))
    return hcp_t


@register_schmidt("CO2")
def sch_number(temp: PlainQuantity) -> float | np.ndarray:
    constant = read_constant()
    const = constant["CO2"]["SCH"][::-1]
    return np.polyval(const, temp.magnitude)

@register_schmidt("CO2-salt")
def sch_number_salt(temp: PlainQuantity) -> float | np.ndarray:
    constant = read_constant()
    const = constant["CO2"]["SCH-salt"][::-1]
    return np.polyval(const, temp.magnitude)
