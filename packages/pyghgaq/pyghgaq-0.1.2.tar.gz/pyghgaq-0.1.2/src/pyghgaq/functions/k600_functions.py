import numpy as np
from pint.facets.plain import PlainQuantity

from pyghgaq.functions.units import Q_
from pyghgaq.registry.registry import register_k600


@register_k600("VP2013")
def k600_VP2013(
    u10: PlainQuantity, area: PlainQuantity, units: dict[str, str] = {}
) -> PlainQuantity:
    """Calculates gas transfer coefficient k600 from Vachon and Prairie 2013

    Parameters
    ----------
    u10: Wind velocity at 10m  (ms-1)
    area: Lake area (km2)

    Return
    ------
    k600 : velocity transfer coefficient (cmh-1)
    """
    u10 = u10.to("m/s")
    area = area.to("km^2")
    k600 = 2.51 + 1.48 * u10.magnitude + 0.39 * u10.magnitude * np.log10(area.magnitude)
    return Q_(k600, "cm h^-1")


@register_k600("MA2010-NB")
def k600_MA2010_NB(u10: PlainQuantity, units: dict[str, str] = {}) -> PlainQuantity:
    """Calculates gas transfer coefficient from McIntyre et al. 2010 negative bouyancy

    Parameters
    ----------
    u10: Wind velocity at 10m  (ms-1)

    Return
    ------
    k600 : velocity transfer coefficient (cmh-1)
    """
    u10 = u10.to("m/s")
    return Q_(2 + 2.04 * u10.magnitude, "cm h^-1")


@register_k600("MA2010-PB")
def k600_MA2010_PB(u10: PlainQuantity, units: dict[str, str] = {}) -> PlainQuantity:
    """Calculates gas transfer coefficient from McIntyre et al. 2010 positive bouyancy

    Parameters
    ----------
    u10: Wind velocity at 10m  (ms-1)

    Return
    ------
    k600 : velocity transfer coefficient (cmh-1)
    """
    u10 = u10.to("m/s")
    return Q_(1.74 * u10.magnitude - 0.15, "cm h^-1")


@register_k600("MA2010-MB")
def k600_MA2010_MB(u10: PlainQuantity, units: dict[str, str] = {}) -> PlainQuantity:
    """Calculates gas transfer coefficient from McIntyre et al. 2010 mixed model

    Parameters
    ----------
    u10: Wind velocity at 10m  (ms-1)

    Return
    ------
    k600 : velocity transfer coefficient (cmh-1)
    """
    u10 = u10.to("m/s")
    return Q_(2.25 * u10.magnitude + 0.16, "cm h^-1")


@register_k600("CC1998")
def k600_CC1998(u10: PlainQuantity, units: dict[str, str] = {}) -> PlainQuantity:
    """Calculates gas transfer coefficient from Cole and Caraco 1998.

    Parameters
    ----------
    u10_ms  : Wind velocity at 10m  (ms-1)

    Return
    ------
    k600 : velocity transfer coefficient (cmh-1)
    """

    u10 = u10.to("m/s")
    return Q_(2.07 + 0.215 * u10.magnitude**1.7, "cm h^-1")


def kgas_k600(
    varname: str,
    temp: PlainQuantity,
    k: PlainQuantity,
    u10: PlainQuantity,
    units: dict[str, str] = {},
    a: int = 1,
) -> PlainQuantity:
    """Calculates gas transfer coefficient kgas from k600 or vicecersa

    Parameters:
    ----------
    varname : gas name
    temp_c : water temperature (degC)
    k : gas transfer coefficient k600 or kgas
    u10 : wind speed at 10 m in (ms-1)
    units: units for each paramenter
    a: if a ==  1 calculates kgas from k600
       if a == -1 calcualtes k600 from kgas

    Return
    ------
    kgas : velocity transfer coefficient (md-1)
    """

    from pyghgaq.functions.functions import schmidt_number

    u10 = u10.to("m/s")
    temp = temp.to("degC")
    k = k.to("m/d")
    # Prairie and del Giorgo 2013
    if isinstance(u10.magnitude, float) or isinstance(u10.magnitude, int):
        n = 1 / 2 if u10.magnitude > 3.7 else 2 / 3
    else:
        n = np.ones(len(u10.magnitude)) * 1 / 2
        n = np.where(u10.magnitude > 3.7, n, 2 / 3.0)
    sch = schmidt_number(varname, temp)
    return k * (600 / sch) ** (n * a)
