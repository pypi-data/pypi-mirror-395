"""Module with some utility functions to handle user inputs.

Copyright (C) 2023 Iñigo Sáez-Casares

inigo.saez-casares@obspm.fr

This file is part of e-mantis.

e-mantis is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from copy import deepcopy

import numpy as np
import numpy.typing as npt

from emantis.exceptions import EmulationRangeError


def check_emulation_range(
    values: npt.ArrayLike, range_min: float | None, range_max: float | None, name: str
) -> None:
    """Verify that values for some arbitrary quantity are within the emulation range.

    Raises an EmulationRangeError exception if it's not the case.
    The exception will be raised if one or more values are outside the range.

    Parameters
    ----------
    values : array-like
        The values of the quantity of interest.
    range_min : float or None
        The minimum of the emulation range for the quantity of interest.
        If None, the minimum bound will not be checked.
    range_max : float or None
        The maximum of the emulation range for the quantity of interest.
        If None, the maximum bound will not be checked.
    name : str
        The name of the quantity of interest.

    Raises
    ------
    EmulationRangeError
        If input value is not within emulation range.

    """
    # Check minimum bound.
    if range_min is not None:
        min_value: float = np.min(values)
        if min_value < range_min:
            raise EmulationRangeError(min_value, name, range_min, range_max)

    # Check maximum bound.
    if range_max is not None:
        max_value: float = np.max(values)
        if max_value > range_max:
            raise EmulationRangeError(max_value, name, range_min, range_max)


def format_input_to_1d_array(
    x: float | list | npt.NDArray, x_name: str | None = None
) -> npt.NDArray:
    """Transform input into a 1D numpy array.

    Parameters
    ----------
    x : float or list or array of shape (N,)
        The input.
    x_name : str
        The name of the input variable, used to customize raised exception.

    Returns
    -------
    x_array : array of shape (N,)
        The input transformed into a numpy 1D array.

    Raises
    ------
    TypeError
        If input is not a float, list, or a 1D numpy array.

    """
    # Default x_name.
    if x_name is None:
        x_name = "x"
    # Check if x is an int or float (scalar).
    if not isinstance(x, bool) and isinstance(x, (int, float)):
        x_array = np.array([x])
    # Check if x is a list.
    elif isinstance(x, list):
        x_array = np.array(x)
    # Check if x is an array.
    elif isinstance(x, np.ndarray):
        # Check dimension.
        if x.ndim == 0:
            x_array = np.array([x])
        elif x.ndim == 1:
            x_array = x
        else:
            raise TypeError(f"{x_name} must be float, list or 1D array.")
    else:
        raise TypeError(f"{x_name} must be float, list or 1D array.")

    return x_array


def convert_cosmo_params_from_As_to_sigma8(
    cosmo_params: dict, sigma8_emulator, sigma8_name: str, emu_v1: bool = False
) -> dict:
    # If A_s not present do nothing.
    if "A_s" not in cosmo_params:
        return cosmo_params

    # Deepcopy of input cosmological parameters for sigma8 emulator.
    cosmo_params_sigma8_emu = deepcopy(cosmo_params)

    # If the cosmo_params are used by a v1 emulator
    # use the fiducial values for the missing
    # cosmological parameters.
    if emu_v1:
        cosmo_params_sigma8_emu["h"] = 0.6736
        cosmo_params_sigma8_emu["Omega_b"] = 0.049302
        cosmo_params_sigma8_emu["n_s"] = 0.9649

    # Rescale As -> ln(As*1e10).
    cosmo_params_sigma8_emu["A_s"] = np.log(
        format_input_to_1d_array(cosmo_params["A_s"], x_name="A_s") * 1e10
    )

    # Loop over input parameter names.
    for param in cosmo_params:
        # If sigma8 is also present raise an exception.
        if "sigma8" in param:
            raise ValueError(
                f"Input parameters `A_s` and `{param}` are incompatible."
                " Only one of them must be given."
            )

        # Delete parameters that are not needed for the sigma8 emulator.
        if param not in sigma8_emulator.params_range:
            del cosmo_params_sigma8_emu[param]

    # Compute sigma8 parameter.
    cosmo_params[sigma8_name] = sigma8_emulator.predict_sigma8(cosmo_params_sigma8_emu)

    # Delete A_s entry.
    del cosmo_params["A_s"]

    return cosmo_params
