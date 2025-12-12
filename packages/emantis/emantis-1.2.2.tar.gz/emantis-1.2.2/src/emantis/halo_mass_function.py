"""Module implementing an emulator for the halo mass function.

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

import numpy.typing as npt

from emantis._gp_emulation import GaussianProcessEmulator1Dx1D
from emantis._read_data import (
    read_cosmo_params,
    read_cosmo_params_range,
    read_data_bspline,
    read_emulation_config,
)
from emantis._utils_inputs import convert_cosmo_params_from_As_to_sigma8
from emantis.matter_power_spectrum import Sigma8Emulator

_HMF_MODELS = ["wCDM", "fR"]

_FOF_B_VALUES = [0.2]
_SO_DELTAC_VALUES = [200, 500, 1000]


class HMFEmulator(GaussianProcessEmulator1Dx1D):
    """Emulator for the halo mass function.

    Multiple types of cosmological models
    and dark matter halo definitions are supported.

    Parameters
    ----------
    model : str
        Type of cosmological model.

        'wCDM'
            Dark energy with constant equation of state parameter.
        'fR'
            Hu & Sawicki f(R) gravity (limited to n=1).
    mass_def : str
        Mass definition.

        For Friend-of-Friends haloes,
        parameterized by the linking length: 'b0.2'

        For Spherical Overdensity haloes, parameterized by
        the critical overdensity threshold: '200c', '500c', '1000c'.

    use_resolution_correction : bool, default=True
        Use the resolution correction for the low mass end of the HMF.
    random_seed : int or None, default=None
        A random seed used for different random generators.
    n_jobs : int, default=1
        Maximum number of independent processes used to train the emulator.
        A value of -1 uses all available cores.
        Predictions always use `n_jobs=1`,
        since they are already fast and the parallelism overhead is not worth it.
        Additional parallelism might be used (via Numpy, SciPy, OpenMP),
        even when `n_jobs=1`.
        See the scikit-learn `documentation <https://scikit-learn.org/stable/computing/parallelism.html#parallelism>`_
        for more details.
    verbose : bool, default=True
        Activate verbose output.
    use_persistent_storage : bool, default=True
        If ``True``, save trained emulator to a persistent storage database,
        based on the pickle protocol.
        If a trained emulator is already present in the database,
        load it and skip emulator training.
        If ``False``, never load previously trained emulator from the
        persistent storage database.

    """

    def __init__(
        self,
        model: str,
        mass_def: str,
        use_resolution_correction: bool = True,
        random_seed: int | None = None,
        n_jobs: int = 1,
        verbose: bool = True,
        use_persistent_storage: bool = True,
    ) -> None:
        # Check model.
        if model not in _HMF_MODELS:
            raise ValueError(f"`model` must be one of: {_HMF_MODELS}.")

        # Observable name and simulation suite version.
        observable = "halo_mass_function"
        sim_version = 2

        # Read emulation configuration.
        config_emu_dict = read_emulation_config(observable, model, sim_version)

        # Read cosmological parameters.
        cosmo_params = read_cosmo_params(model, sim_version)
        # Read range of cosmological parameters.
        cosmo_params_range = read_cosmo_params_range(model, sim_version)

        # Process mass_def.
        mass_def_string = self._process_mass_def(mass_def)

        # Read training data.
        data_prefix = f"{mass_def_string}/res_corr_{use_resolution_correction}"
        (
            aexp_nodes,
            data,
            data_std,
            bspline_knots,
            bspline_degree,
            gp_std_factor,
        ) = read_data_bspline(
            observable,
            model,
            sim_version,
            prefix=data_prefix,
            read_data_std=True,
            read_gp_std_factor=True,
        )

        super().__init__(
            params=cosmo_params,
            data=data,
            data_bins=bspline_knots,
            data_nodes=aexp_nodes,
            data_std=data_std,
            bspline_degree=bspline_degree,
            gp_std_factor=gp_std_factor,
            params_range=cosmo_params_range,
            config_emu=config_emu_dict,
            use_persistent_storage=use_persistent_storage,
            persistent_storage_key=f"{observable}_{model}_{mass_def}_res_corr_{use_resolution_correction}",
            random_seed=random_seed,
            n_jobs=n_jobs,
            verbose=verbose,
            ignore_training_warnings=True,
            logger_name=f"e-MANTIS:hmf:{model}:{mass_def}",
        )

        sigma8_emulator_model = {"fR": "LCDM", "wCDM": "wCDM"}
        self._sigma8_emulator = Sigma8Emulator(
            model=sigma8_emulator_model[model], random_seed=random_seed, verbose=verbose
        )

    def _process_mass_def(self, mass_def: str) -> str:
        """Process the user provided mass definition.

        Parameters
        ----------
        mass_def : str
            The mass definition string provided by the user.

        Returns
        -------
        mass_def_string : str
            The mass definition string required to read the emulation data.

        Raises
        ------
        ValueError
            If the provided `mass_def` is not supported.
        """
        # FoF haloes.
        if "b" in mass_def:
            # Read linking length.
            try:
                b_fof = float(mass_def.replace("b", ""))
            except ValueError as exc:
                raise ValueError("Incorrect `mass_def` value.") from exc
            # Check linking length.
            if b_fof not in _FOF_B_VALUES:
                raise ValueError(
                    "Unsupported linking length for FoF haloes."
                    f" Allowed values are: {_FOF_B_VALUES}."
                )
            mass_def_string = f"b_fof_{b_fof:g}"

        # SO haloes with overdensity threshold in critical density units.
        elif "c" in mass_def:
            # Read overdensity threshold.
            try:
                delta_c = float(mass_def.replace("c", ""))
            except ValueError as exc:
                raise ValueError("Incorrect `mass_def` value.") from exc
            # Check overdensity threshold.
            if delta_c not in _SO_DELTAC_VALUES:
                raise ValueError(
                    "Unsupported critical overdensity threshold for SO haloes."
                    f" Allowed values are: {_SO_DELTAC_VALUES}."
                )
            mass_def_string = f"deltac_{delta_c:g}"

        else:
            raise ValueError("Incorrect mass definition (`mass_def`).")

        return mass_def_string

    def predict_hmf(
        self,
        mass_halo: float | list[float] | npt.NDArray,
        cosmo_params: dict[str, float | list[float] | npt.NDArray],
        aexp: float | list[float] | npt.NDArray,
        return_std: bool = False,
        squeeze: bool = True,
        extrapolate_mass_halo_high: bool = False,
    ) -> npt.NDArray:
        """Predict the halo mass function.

        Multiple sets of cosmological parameters can be passed at once
        by giving them in the form of arrays or lists (see tutorial).
        This function will return a prediction
        for the halo mass function for each entry.
        Calling the function to give predictions for ``n_cosmo`` models at once
        is significantly faster than calling it ``n_cosmo`` times for a single model.

        Additionally, multiple scale factors per model can be requested at once.
        If `aexp` has ``n_aexp`` entries, then ``n_aexp`` outputs
        will be given for each model.

        Parameters
        ----------
        mass_halo : float or list or array of shape (n_mass,)
            The halo mass values at which to output
            the halo mass function in units of Msun/h.
            The same halo mass values are used
            for all cosmological models and scale factors.
        cosmo_params : dict
            A dictionary passing the cosmological parameters.
        aexp : float or list or array of shape (n_aexp,)
            Scale factor values.
        return_std : bool, default=False
            If ``True``, also return the standard deviation of the predictions.
            Might slow down the computation.
        squeeze : bool, default=True
            If ``True``, remove axes of length one from the output.
        extrapolate_mass_halo_high : bool, default=False
            Extrapolation to high masses.
            If ``True``, the emulator will extrapolate its predictions
            for masses above the maximum emulation range.
            This is provided for convenience and it is not
            an accurate nor reliable extrapolation.
            It should be used with caution and only in some specific cases
            where accuracy at high masses is not required.
            The extrapolation is done by a second order polynomial
            in log10(HMF)-log10(mass).

        Returns
        -------
        pred : ndarray
            Predicted halo mass function at the input halo masses,
            cosmological models, and scale factor values.
            The output is an array of shape (n_aexp, n_cosmo, n_mass),
            where ``n_aexp`` is the number of scale factor values
            per cosmological model,
            ``n_cosmo`` is the number of cosmological models,
            and ``n_mass`` the number of halo mass values.
            By default the output array is squeezed to remove axes of length one.
            This behaviour can be changed with the `squeeze` parameter.
        pred_std : ndarray (returned only of `return_std` is True)
            The standard deviation of the predicted halo mass function
            at the input halo masses, cosmological models, and scale factor values.
            Same shape as `pred`.

        """
        # Check if A_s in present in the input cosmological parameters.
        if "A_s" in cosmo_params:
            # Needs to be changed if multiple parameters
            # with sigma8 in the name are present.
            sigma8_name = [param for param in self.params_range if "sigma8" in param][0]
            cosmo_params = convert_cosmo_params_from_As_to_sigma8(
                cosmo_params, self._sigma8_emulator, sigma8_name
            )

        return self._predict_observable(
            bins=mass_halo,
            params=cosmo_params,
            node_var=aexp,
            return_std=return_std,
            squeeze=squeeze,
            extrapolate_bins_low=False,
            extrapolate_bins_high=extrapolate_mass_halo_high,
        )

    @property
    def aexp_nodes(self):
        """list: The training scale factor nodes of the emulator."""
        return self._data_nodes

    @property
    def params_range(self) -> dict:
        """dict: Allowed emulation range for each cosmological parameter."""
        assert self._params_range is not None
        return self._params_range
