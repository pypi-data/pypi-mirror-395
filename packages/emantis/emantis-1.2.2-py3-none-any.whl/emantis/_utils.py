"""Module with some utility functions.

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

from typing import Literal, overload

import numpy as np
import numpy.typing as npt

# Supported types of simple transformations.
SIMPLE_TRANSFORM_TYPES = Literal["lin", "log10"]


def lin_interp(
    x0: float | npt.NDArray,
    x1: float | npt.NDArray,
    x2: float | npt.NDArray,
    y1: float | npt.NDArray,
    y2: float | npt.NDArray,
) -> float | npt.NDArray:
    """Perform a linear interpolation.

    Linearly interpolates at location `x0` between two nodes `x1` and `x2`, with
    values `y1` and `y2` respectively.

    It assumes that `x1` < `x0` < `x2`.

    Parameters
    ----------
    x0 : float or ndarray
        The location at which the interpolation is returned.
    x1 : float or ndarray
        The lower interpolation node.
    x2 : float or ndarray
        The upper interpolation node.
    y1 : float or ndarray
        The value at `x1`.
    y2 : float or ndarray
        The value at `x2`.

    Returns
    -------
    y0 : float or ndarray
        The interpolated value at `x0`.

    """
    y0 = y1 + (x0 - x1) * (y2 - y1) / (x2 - x1)

    return y0


@overload
def simple_transform(x: float, transform_type: SIMPLE_TRANSFORM_TYPES) -> float: ...


@overload
def simple_transform(
    x: npt.NDArray, transform_type: SIMPLE_TRANSFORM_TYPES
) -> npt.NDArray: ...


def simple_transform(
    x: float | npt.NDArray, transform_type: SIMPLE_TRANSFORM_TYPES
) -> float | npt.NDArray:
    """Apply a simple mathematical transformation to an input array.

    Parameters
    ----------
    x : float or ndarray
        The input array.
    transform_type : str
        The type of transformation, among:
            - lin: linear transformation, i.e. do nothing.
            - log10: base 10 logarithm.

    Returns
    -------
    x_transformed : float or ndarray
        The transformed array.

    """
    if transform_type == "lin":
        pass
    elif transform_type == "log10":
        x = np.log10(x)

    return x


@overload
def inverse_simple_transform(
    x: float, transform_type: SIMPLE_TRANSFORM_TYPES
) -> float: ...


@overload
def inverse_simple_transform(
    x: npt.NDArray, transform_type: SIMPLE_TRANSFORM_TYPES
) -> npt.NDArray: ...


def inverse_simple_transform(
    x: float | npt.NDArray, transform_type: SIMPLE_TRANSFORM_TYPES
) -> float | npt.NDArray:
    """Apply the inverse of simple mathematical transformation to an input array.

    Parameters
    ----------
    x : float or ndarray
        The input array.
    transform_type : str
        The type of transformation, among:
            - lin: linear transformation, i.e. do nothing.
            - log10: base 10 logarithm

    Returns
    -------
    x_transformed : float or ndarray
        The array obtained after the inverse transformation.

    """
    if transform_type == "lin":
        pass
    elif transform_type == "log10":
        x = 10 ** (x)

    return x
