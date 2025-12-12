import importlib
import inspect
import pkgutil

import numpy as np
from pint.facets.plain import PlainQuantity

from pyghgaq.functions.read import read_constant
from pyghgaq.functions.type_utils import Numeric
from pyghgaq.functions.units import Q_, get_default_units
from pyghgaq.registry.registry import enforce_units


@enforce_units(
    unit_getter=get_default_units,
    unit_map={"windspeed": "WindSpeed", "height": "height"},
)
def uz_to_u10(
    windspeed: Numeric, height: float | int, units: dict[str, str] = {}
) -> PlainQuantity:
    constant = read_constant()
    cd = constant["Cd"]
    k = constant["k"]
    u10 = windspeed.to("m/s") * (1 + cd**0.5 / k * np.log(Q_(10, "m") / height))
    return u10


@enforce_units(
    unit_getter=get_default_units,
    unit_map={
        "atmpress": "Atm_Pressure",
        "catm": "Gas_Concentration",
        "temp": "Temperature",
    },
)
def csat(
    var: str,
    atmpress: Numeric,
    catm: Numeric,
    temp: Numeric,
    method: "str" = "Sanders",
    units: dict[str, str] = {},
    **kwargs,
) -> PlainQuantity:
    """
    Return
    -------
    Concentration of saturation in mmolm3
    """
    hcp = henry_coefficient(var, temp, method, units, **kwargs)
    return atmpress.to("Pa") * catm.to_base_units() * hcp.to("mmol m^-3 Pa^-1")


@enforce_units(
    unit_getter=get_default_units,
    unit_map={
        "flux": "Diff_Flux",
        "cw": "Diss_Gas_Concentration",
        "csat": "Diss_Gas_Concentration",
    },
)
def kgas(
    flux: Numeric,
    cw: Numeric,
    csat: Numeric,
    units: dict[str, str] = {},
) -> PlainQuantity:
    """
    Return
    ------
    kgas from flux and concentrations measurements.
    """

    return flux.to("mmol/m^2/d") / (cw.to("mmol/m^3") - csat.to("mmol/m^3"))


@enforce_units(
    unit_getter=get_default_units,
    unit_map={"csat": "Diss_Gas_Concentration", "cw": "Diss_Gas_Concentration"},
)
def atm_diff_flux(
    csat: Numeric,
    cw: Numeric,
    kgas: Numeric,
    units: dict[str, str] = {},
) -> PlainQuantity:
    """
    Returns
    -------
    Diffusive flux to/from the atmosphere
    """
    return kgas.to("m/d") * (cw.to("mmol m^-3") - csat.to("mmol m^-3"))


@enforce_units(
    unit_getter=get_default_units,
    unit_map={"temp": "Temperature", "catm": "Gas_Concentration", "salt": "Salinity"},
)
def henry_coefficient(
    varname: str,
    temp: Numeric,
    method: str = "Sanders",
    units: dict[str, str] = {},
    **kwargs,
) -> PlainQuantity:

    from pyghgaq import gases
    from pyghgaq.registry.registry import exportershcp

    gasnames = []
    for _, modulename, _ in pkgutil.iter_modules(gases.__path__):
        gasnames.append(modulename)

    if varname not in gasnames:
        raise ValueError(
            f"{varname} is not included as gas to be analyze \b Valid gases are {gasnames}"
        )

    importlib.import_module(f"pyghgaq.gases.{varname}")
    exporter = exportershcp.get(varname, {}).get(method)

    if exporter is None:
        raise ValueError(
            f"No method ='{method}' found for varname='{varname}' or '{varname}' is not included in functions \n Supported method for '{varname}' are {list(exportershcp.get(varname, {}).keys())}"
        )
    sig = inspect.signature(exporter)
    valid_kwargs = {k: v for k, v in kwargs.items() if k in sig.parameters}
    valid_kwargs.update({"units": units})
    return exporter(varname, temp, **valid_kwargs)


@enforce_units(unit_getter=get_default_units, unit_map={"u10": "WindSpeed"})
def k600(
    u10: Numeric, k600_method: str = "MA2010-NB", units: dict[str, str] = {}, **kwargs
) -> PlainQuantity:
    """Calculates gas transfer coefficient k600

    Return
    ------
    k600 : velocity transfer coefficient (md-1)
    """

    from pyghgaq.registry.registry import exportersk600

    importlib.import_module("pyghgaq.functions.k600_functions")

    exporter = exportersk600.get(k600_method)
    if exporter is None:
        raise ValueError(
            f"'{k600_method}' is not included as valid method in k600_models.py \n Supported methods are {list(exportersk600.keys())}"
        )

    sig = inspect.signature(exporter)
    valid_kwargs = {k: v for k, v in kwargs.items() if k in sig.parameters}
    return exporter(u10, **valid_kwargs).to("m/d")


@enforce_units(
    unit_getter=get_default_units, unit_map={"temp": "Temperature", "u10": "WindSpeed"}
)
def k600_to_kgas(
    varname: str,
    temp: Numeric,
    k: Numeric,
    u10: Numeric,
    units: dict[str, str] = {},
) -> PlainQuantity:
    """Calculates gas transfer coefficient kgas from k600

    Parameters:
    ----------
    varname : gas name
    k600 : normalized gas transfer coefficient k600
    temp : water temperature (degC)
    u10s : wind speed at 10 m in (ms-1)

    Return
    ------
    kgas : gas transfer coefficient
    """
    from pyghgaq.functions.k600_functions import kgas_k600

    return kgas_k600(varname, temp, k, u10, units, 1)


@enforce_units(
    unit_getter=get_default_units, unit_map={"u10": "WindSpeed", "temp": "Temperature"}
)
def kgas_to_k600(
    varname: str,
    kgas: Numeric,
    temp: Numeric,
    u10: Numeric,
    units: dict[str, str] = {},
) -> PlainQuantity:
    """Calculates normalized gas transfer coefficient k600 from kgas

    Parameters:
    ----------
    varname : gas name
    kgas : gas transfer coefficient for specific gas
    temp_c : water temperature (degC)
    u10_ms : wind speed at 10 m in (ms-1)

    Return
    ------
    k600 : normalized gas transfer coefficient
    """
    from pyghgaq.functions.k600_functions import kgas_k600

    return kgas_k600(varname, temp, kgas, u10, units, -1)


@enforce_units(unit_getter=get_default_units, unit_map={"temp": "Temperature"})
def schmidt_number(varname: str, temp: Numeric) -> float | np.ndarray:
    from pyghgaq.registry.registry import exporterssh

    """Calculates Schmidt number for gases

    Parameters:
    ----------
    varname : gas name
    temp_c : water temperature (degC)

    Return
    ------
    Schmidt number
    """

    return exporterssh[varname](temp)


if __name__ == "__main__":

    temp = np.random.random(30)
    u = np.random.random(30)
    cw = np.random.random(30)
    cgas = np.random.random(30)
    # hcpch4_a = henry_coefficient("CH4", temp_c=temp)
    # hcpch4_b = henry_coefficient(
    #     "CH4", "Weisenburg", temp_c=temp, catm_ppm=2, salt_psu=0
    # )
    # co2flux = atm_diff_flux(cgas, cw, kgas_ms)
