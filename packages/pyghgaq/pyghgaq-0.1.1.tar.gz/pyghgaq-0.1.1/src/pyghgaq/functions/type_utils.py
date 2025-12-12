from __future__ import annotations

from typing import TypeAlias, TYPE_CHECKING

from pint import Quantity
from pint.facets.plain import PlainQuantity
import numpy as np

if TYPE_CHECKING:
    pass

Numeric: TypeAlias = float | np.ndarray | int | Quantity | PlainQuantity
