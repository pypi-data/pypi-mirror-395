"""Module containing some custom exceptions.

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


class EmulationRangeError(ValueError):
    """Exception raised when one of the input parameters is outside the emulation range.

    It can be a cosmological parameter, or any other relevant variable.
    """

    def __init__(self, value, param, xmin, xmax):
        message = (
            f"Input {param} (={value}) is outside the emulation"
            f" range ({xmin} <= {param} <= {xmax})."
        )

        super().__init__(message)
