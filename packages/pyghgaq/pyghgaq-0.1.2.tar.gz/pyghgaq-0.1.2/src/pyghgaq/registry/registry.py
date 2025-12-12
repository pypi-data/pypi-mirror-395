import inspect
from copy import deepcopy
from functools import wraps
from inspect import signature
from typing import Any, Callable

import numpy as np

from pyghgaq.functions.type_utils import Numeric
from pyghgaq.functions.units import Q_

type exporterfunc = Callable[..., np.ndarray | float]
type exporterhcp = dict[str, dict[str, Callable]]
type exporterk600 = dict[str, exporterfunc]
exportershcp: exporterhcp = {}
exportersk600: exporterk600 = {}
exporterssh: exporterk600 = {}


def register_hcp(varname: str, salt: str):
    def decorator(func: Callable[..., Any]):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        exportershcp.setdefault(varname, {})[salt] = wrapper
        return func

    return decorator


def register_k600(method: str):
    def decorator(func: Callable[..., Any]):
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)

        exportersk600[method] = wrapper
        return wrapper

    return decorator


def register_schmidt(method: str):
    def decorator(func: Callable[..., Any]):
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)

        exporterssh[method] = wrapper
        return wrapper

    return decorator


# Assume Q_, to_si, and Numeric are imported/defined elsewhere


def enforce_units(unit_getter: Callable, unit_map: dict[str, str] = {}):
    """
    Decorator that fetches defaults dynamically and respects user overrides.
    """

    def decorator(func):
        # 1. Get the parameter names the function expects (e.g., 'atmpress', 'catm', 'hcp')
        param_names = [
            name
            for name, param in signature(func).parameters.items()
            if name != "units"  # Exclude the units dict itself
        ]

        @wraps(func)
        def wrapper(*args, **kwargs):
            sig = signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()

            # --- Dynamic Defaults & Merging Logic ---

            # A. Get the CURRENT default units dictionary
            # (called at runtime, so it reflects any global change)
            current_defaults = unit_getter()

            # B. Get the user-provided explicit units from the function arguments
            # This is the dictionary the user passed to the function (e.g., csat(..., units={'atmpress': 'psi'}))
            user_overrides = bound.arguments.get("units", {})

            # C. Create the FINAL effective units for this call:
            # Start with defaults, then OVERRIDE with user-provided units.
            effective_units = {}
            for param_name in param_names:

                # 1. Use user override if provided
                if param_name in user_overrides:
                    effective_units[param_name] = user_overrides[param_name]

                # 2. Otherwise, use the current default
                else:
                    name = param_name
                    if param_name in unit_map:
                        name = unit_map.get(param_name)

                    if name in current_defaults:
                        effective_units[param_name] = current_defaults[name]
                    else:
                        if name not in ['kwargs'] and not isinstance(bound.arguments[param_name], str):
                            print(f'Units not found for: {param_name}')


            # --- Unit Enforcement ---

            # Loop through the FINAL effective units for conversion
            for name, exp_unit in effective_units.items():
                if name in bound.arguments and isinstance(
                    bound.arguments[name], Numeric
                ):
                    # NOTE: Since you're using 'effective_units' here,
                    # you only need to convert to SI *if the value is a plain number*.

                    # If the argument value is NOT already a Pint Quantity (i.e., it's a raw number)
                    # we must treat it as being in the 'exp_unit' (which is either the default or the override).

                    # This section handles the automatic tagging and conversion
                    bound.arguments[name] = Q_(bound.arguments[name], exp_unit)
                    # bound.arguments[name] = to_si(
                    #     bound.arguments[name]
                    # )  # Assuming to_si converts to base SI units

            return func(*bound.args, **bound.kwargs)

        return wrapper

    return decorator


# def enforce_units(**expected_units):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             from inspect import signature
#
#             sig = signature(func)
#             bound = sig.bind(*args, **kwargs)
#             bound.apply_defaults()
#
#             for name, exp_unit in expected_units.items():
#                 if name in bound.arguments and isinstance(
#                     bound.arguments[name], Numeric
#                 ):
#                     if name in bound.arguments["units"]:
#                         bound.arguments[name] = Q_(
#                             bound.arguments[name], bound.arguments["units"][name]
#                         )
#                     bound.arguments[name] = to_si(bound.arguments[name], exp_unit)
#             return func(*bound.args, **bound.kwargs)
#
#         return wrapper
#
#     return decorator


def warn_default_units(func):
    @wraps(func)
    def wrapper(*args, units=None, **kwargs):
        # Retrieve the default units from the function signature
        sig = inspect.signature(func)
        param = sig.parameters.get("units")
        if param is None or param.default is None:
            # No default units defined in the function
            default_units = {}
        else:
            default_units = deepcopy(param.default)  # copy to avoid mutation

        if units is None:
            units = {}

        # Warn for each default unit not explicitly provided by the user
        for key, default in default_units.items():
            if key not in units:
                print(f"Assuming {key} = '{default}' (default)")

        # Merge user-provided units with defaults
        merged_units = {**default_units, **units}

        # Call the original function with the merged units
        return func(*args, units=merged_units, **kwargs)

    return wrapper
