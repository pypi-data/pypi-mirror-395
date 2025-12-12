# PyGHGaq 

This package contains different methods and properties to estimate GHG (CH<sub>4</sub> and CO<sub>2</sub>) emissions and concentrations for aquatic ecosystems

Implemented methods:
* Flux through the water-air interface
* Gas transfer coefficient (k<sub>600</sub>) using different models:
    * MacIntyre et al. 2010 (positive bouyancy, negative bouyancy and mixed).
    * Cole and Caraco 1998.
    * Vachon and Prairie 2013.
* Calculations to transfor k<sub>600</sub> to k<sub>gas</sub> and viceversa.
* Schmidt number.
* Henry's coefficient corrected by temperature and salt.
* Saturation concentration in water.


## Installation
```sh
pip install pyghgaq
```

## Usage

```python
import pyghgaq
import numpy as np

temp = np.random.random(30)
u = np.random.random(30)
cw = np.random.random(30)
cgas = np.random.random(30)
hcpch4 = pyghgaq.henry_coefficient("CH4", temp_c=temp)
k600_ms = pyghgaq.k600("VP2013", u10_ms=1, area_km2=1)
kgas_ms = pyghgaq.k600_to_kx("CO2", temp, k600_ms, u)
co2flux = pyghgaq.atm_diff_flux(cgas, cw, kgas_ms)
```

### Units

Units are managed using `Pint`. They can be changed by default for all the package as
```python
    from pyghgaq.functions.units import DEFAULT_INPUT_UNITS

    DEFAULT_INPUT_UNITS["WindSpeed"] = "m/s"
    DEFAULT_INPUT_UNITS["kgas"] = "m/d"
```
or by function as:
```python
    atmf = pyg.atm_diff_flux(0, 1, 2, units={"kgas": "m/s"})
```

## IMPORTANT
This package is still under delvelopment
