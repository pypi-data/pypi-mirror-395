from pint import Quantity, UnitRegistry

ureg = UnitRegistry(autoconvert_offset_to_baseunit=True)
Q_ = ureg.Quantity # type: ignore[assignment]

__all__= ["ureg", "Q_", "Quantity"]

## HERE YOU CAN DEFINE MORE UNITS
ureg.formatter.default_format = "~P"
ureg.define("PSU = 1e-3")
ureg.define("ppb = 1e-9")

DEFAULT_INPUT_UNITS = {
    "WindSpeed": "m/s",
    "Temperature": "degC",
    "Diss_Gas_Concentration": "mmol m^-3",
    "Gas_Concentration": "ppm",
    "k600": "m/d",
    "kgas": "m/d",
    "k": "m/d",
    "Atm_Pressure": "hPa",
    "Salinity": "PSU",
    "Diff_Flux": "mmol m^-2 d^-1",
    "HenryCoeff": "mol m^-3 Pa^-1",
    "Area": "km^2",
    "height": "m"
}

def get_default_units():
    """Returns the CURRENT, editable default units dictionary."""
    return DEFAULT_INPUT_UNITS

def to_si(value, expected_unit):
    """
    Ensure `value` has units of `expected_unit`, then convert to SI.

    Parameters
    ----------
    value : float | pint.Quantity
        Value with or without units.
    expected_unit : str | pint.Unit
        Expected physical unit (e.g., 'm/s', 'K', 'Pa').

    Returns
    -------
    pint.Quantity
        Quantity converted to SI base units.
    """
    expected_unit = ureg.Unit(expected_unit)

    # If value is unitless, assign expected units
    if not isinstance(value, Quantity):
        q = Q_(value, expected_unit)
    else:
        q = value.to(str(expected_unit))
    return q
