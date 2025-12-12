"""Module used to load emulation data.

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

from importlib.resources import as_file, files

import h5py
import numpy as np
import numpy.typing as npt

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

RESOURCES = files("emantis")


def read_emulation_config_from_file(filepath: str) -> dict:
    # Read emulation data config.
    with as_file(RESOURCES / f"data/{filepath}") as mytoml, open(mytoml, "rb") as f:
        config_emu_dict: dict = tomllib.load(f)

    return config_emu_dict


def read_emulation_config(observable: str, model: str, sim_version: int) -> dict:
    # Emulation config file name.
    filepath = (
        f"{observable}/{observable}_{model}_emu_v{sim_version}_emulation_config.toml"
    )
    # Read emulation config.
    config_emu_dict = read_emulation_config_from_file(filepath)

    return config_emu_dict


def read_cosmo_params_from_file(filepath: str) -> npt.NDArray:
    # Read values of the cosmological parameters.
    with as_file(RESOURCES / f"data/{filepath}") as mytxt:
        cosmo_params = np.genfromtxt(mytxt, skip_header=1)

    return cosmo_params


def read_cosmo_params(model: str, sim_version: int) -> npt.NDArray:
    # File with cosmological parameters values.
    filepath = f"cosmo_params_{model}_emu_v{sim_version}.txt"
    # Read parameters.
    cosmo_params = read_cosmo_params_from_file(filepath)

    return cosmo_params


def read_cosmo_params_range_from_file(filepath: str) -> dict:
    # Read emulation range in terms of cosmological parameters.
    with as_file(RESOURCES / f"data/{filepath}") as mytoml, open(mytoml, "rb") as f:
        config_dict = tomllib.load(f)
        cosmo_params_range = config_dict["range"]

    return cosmo_params_range


def read_cosmo_params_range(model: str, sim_version: int) -> dict:
    # File with range of cosmological parameters.
    filepath = f"cosmo_params_{model}_emu_v{sim_version}_config.toml"
    # Read ranges.
    cosmo_params_range = read_cosmo_params_range_from_file(filepath)

    return cosmo_params_range


def read_data_array_from_file_txt(filepath: str) -> npt.NDArray:
    with as_file(RESOURCES / f"data/{filepath}") as mytxtfile:
        data = np.genfromtxt(mytxtfile)

    if data.ndim == 1:
        data = data.reshape(-1, 1)

    return data


def read_data_bspline(
    observable: str,
    model: str,
    sim_version: int,
    prefix: str | None = None,
    read_data_std: bool = False,
    read_gp_std_factor: bool = False,
) -> tuple[
    list[float],
    dict[float, npt.NDArray],
    dict[float, npt.NDArray] | None,
    dict[float, npt.NDArray],
    dict[float, int],
    dict[float, npt.NDArray] | None,
]:
    if prefix is None:
        prefix = ""

    # Init. empty dicts. to store the data at different scale factors.
    data = {}
    bspline_knots = {}
    bspline_degree = {}

    data_std = {} if read_data_std else None

    gp_std_factor = {} if read_gp_std_factor else None

    # Data filename.
    filename = f"{observable}_{model}_emu_v{sim_version}_data.h5"

    # Read data.
    with as_file(RESOURCES / f"data/{observable}/{filename}") as myh5file:  # noqa: SIM117
        with h5py.File(myh5file) as f:
            aexp_nodes = list(f[f"{prefix}/aexp_list"][:])
            for aexp in aexp_nodes:
                data[aexp] = f[f"{prefix}/data_aexp_{aexp:.4f}"][:]
                bspline_knots[aexp] = f[f"{prefix}/bspline_knots_aexp_{aexp:.4f}"][:]
                bspline_degree[aexp] = f[f"{prefix}/bspline_degree_aexp_{aexp:.4f}"][()]
                if read_data_std:
                    data_std[aexp] = f[f"{prefix}/data_std_aexp_{aexp:.4f}"][:]
                if read_gp_std_factor:
                    gp_std_factor[aexp] = f[f"{prefix}/gp_std_factor_aexp_{aexp:.4f}"][
                        :
                    ]

    return aexp_nodes, data, data_std, bspline_knots, bspline_degree, gp_std_factor


def read_data_binned(
    observable: str,
    model: str,
    sim_version: int,
    prefix: str | None = None,
    read_data_std: bool = False,
    read_gp_std_factor: bool = False,
) -> tuple[
    list[float],
    dict[float, npt.NDArray],
    dict[float, npt.NDArray] | None,
    dict[float, npt.NDArray],
    dict[float, npt.NDArray] | None,
]:
    if prefix is None:
        prefix = ""

    # Init. empty dicts. to store the data at different scale factors.
    data = {}
    data_bins = {}

    data_std = {} if read_data_std else None

    gp_std_factor = {} if read_gp_std_factor else None

    # Data filename.
    filename = f"{observable}_{model}_emu_v{sim_version}_data.h5"

    # Read data.
    with as_file(RESOURCES / f"data/{observable}/{filename}") as myh5file:  # noqa: SIM117
        with h5py.File(myh5file) as f:
            aexp_nodes = list(f[f"{prefix}/aexp_list"][:])
            for aexp in aexp_nodes:
                data[aexp] = f[f"{prefix}/data_aexp_{aexp:.4f}"][:]
                data_bins[aexp] = f[f"{prefix}/data_bins_aexp_{aexp:.4f}"][:]
                if read_data_std:
                    data_std[aexp] = f[f"{prefix}/data_std_aexp_{aexp:.4f}"][:]
                if read_gp_std_factor:
                    gp_std_factor[aexp] = f[f"{prefix}/gp_std_factor_aexp_{aexp:.4f}"][
                        :
                    ]

    return aexp_nodes, data, data_std, data_bins, gp_std_factor
