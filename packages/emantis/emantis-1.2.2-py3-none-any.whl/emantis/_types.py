"""Module containing some useful types.

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

from typing import Literal

from pydantic import BaseModel, ConfigDict

from emantis._utils import SIMPLE_TRANSFORM_TYPES

# Supported types of input 1D data.
_DATA_TYPES = Literal["binned", "bspline"]

# Some custom pydantic classes used for the different configuration files. #####


class ConfigPCA(BaseModel):
    model_config = ConfigDict(extra="forbid")

    do_pca: bool = False
    pca_n_components: int | None = None
    pca_scale_data_mean: bool = True
    pca_scale_data_std: bool = True
    niter: int = 100


class ConfigGP(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kernel_nu: float | list[float] = -1
    kernel_white: bool | list[bool] = False
    normalize_y: bool = True
    n_restarts_optimizer: int = 0


class ConfigEmulatorStd(BaseModel):
    model_config = ConfigDict(extra="forbid")

    niter: int = 100


class ConfigDataBinned(BaseModel):
    model_config = ConfigDict(extra="forbid")

    y_transform: SIMPLE_TRANSFORM_TYPES = "lin"
    x_interp_type: SIMPLE_TRANSFORM_TYPES = "lin"
    y_interp_type: SIMPLE_TRANSFORM_TYPES = "lin"


class ConfigDataBspline(BaseModel):
    model_config = ConfigDict(extra="forbid")

    x_transform: SIMPLE_TRANSFORM_TYPES = "lin"
    y_transform: SIMPLE_TRANSFORM_TYPES = "lin"


class ConfigData1D(BaseModel):
    model_config = ConfigDict(extra="forbid")

    data_type: _DATA_TYPES = "binned"
    variable_name: str = "x"
    binned: ConfigDataBinned = ConfigDataBinned()
    bspline: ConfigDataBspline = ConfigDataBspline()


class ConfigGPE1D(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pca: ConfigPCA = ConfigPCA()
    gp: ConfigGP = ConfigGP()
    emulator_std: ConfigEmulatorStd = ConfigEmulatorStd()
    data: ConfigData1D = ConfigData1D()


class ConfigNode(BaseModel):
    model_config = ConfigDict(extra="forbid")

    x_interp_type: SIMPLE_TRANSFORM_TYPES = "lin"
    y_interp_type: SIMPLE_TRANSFORM_TYPES = "lin"
    variable_name: str = "node_var"
    niter: int = 100
    constant_data1D_range: bool = False


class ConfigGPE1Dx1D(BaseModel):
    model_config = ConfigDict(extra="forbid")

    config_gpe_1D: ConfigGPE1D = ConfigGPE1D()
    config_node: ConfigNode = ConfigNode()
