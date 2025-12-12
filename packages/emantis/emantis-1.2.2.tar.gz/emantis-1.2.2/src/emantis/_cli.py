"""A script to train all the emulators from e-mantis.

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

import joblib

from emantis.halo_mass_function import (
    _FOF_B_VALUES,
    _HMF_MODELS,
    _SO_DELTAC_VALUES,
    HMFEmulator,
)
from emantis.matter_power_spectrum import (
    _NL_BOOST_MODELS,
    _NL_MG_BOOST_MODELS,
    _SIGMA8_MODELS,
    NonLinearBoostEmulator,
    NonLinearMGBoostEmulator,
    Sigma8Emulator,
)

n_jobs_max = 6
n_jobs = min(joblib.cpu_count(), n_jobs_max)


# TODO: add some input argument such as:
# - number of cpus
# - type of emulators to train
# Use typer package, see: https://packaging.python.org/en/latest/guides/creating-command-line-tools/
def train_all_emulators():
    print(f"Will train all emulators using {n_jobs} processes.\n")

    print("----- Train matter_power_spectrum emulators -----\n")

    for model in _SIGMA8_MODELS:
        emu = Sigma8Emulator(model=model)
        emu.train(n_jobs=1)
        print("\n----------\n")

    for model in _NL_BOOST_MODELS:
        emu = NonLinearBoostEmulator(model=model)
        emu.train_all(n_jobs=n_jobs)
        print("\n----------\n")

    for model in _NL_MG_BOOST_MODELS:
        emu = NonLinearMGBoostEmulator(model=model)
        emu.train_all(n_jobs=n_jobs)
        print("\n----------\n")

    print("----- Train halo_mass_function emulators -----\n")

    # HMF emulators.
    for model in _HMF_MODELS:
        # FOF.
        for b in _FOF_B_VALUES:
            emu = HMFEmulator(model=model, mass_def=f"b{b}")
            emu.train_all(n_jobs=n_jobs)
            print("\n----------\n")
        for deltac in _SO_DELTAC_VALUES:
            emu = HMFEmulator(model=model, mass_def=f"{deltac}c")
            emu.train_all(n_jobs=n_jobs)
            print("\n----------\n")
