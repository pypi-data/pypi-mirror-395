"""Module implementing emulators for the matter power spectrum.

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

import numpy as np
import numpy.typing as npt

from emantis._gp_emulation import (
    GaussianProcessEmulator1D,
    GaussianProcessEmulator1Dx1D,
)
from emantis._read_data import (
    read_cosmo_params,
    read_cosmo_params_from_file,
    read_cosmo_params_range,
    read_cosmo_params_range_from_file,
    read_data_array_from_file_txt,
    read_data_binned,
    read_emulation_config,
    read_emulation_config_from_file,
)
from emantis._utils_inputs import convert_cosmo_params_from_As_to_sigma8

_NL_BOOST_MODELS = ["wCDM"]
_NL_MG_BOOST_MODELS = ["fR", "fR_v1"]
_SIGMA8_MODELS = ["LCDM", "wCDM"]


class Sigma8Emulator(GaussianProcessEmulator1D):
    """Emulator for sigma8.

    Parameters
    ----------
    model : str
        Type of cosmological model.

        'LCDM'
            Standard (flat) LCDM.
        'wCDM'
            Dark energy with constant equation of state parameter,
    random_seed : int or None, default=None
        A random seed used for different random generators.
    verbose : bool, default=True
        Whether to activate or not verbose output.
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
        model,
        random_seed: int | None = None,
        verbose: bool = True,
        use_persistent_storage: bool = True,
    ) -> None:
        # Check model.
        if model not in _SIGMA8_MODELS:
            raise ValueError(f"`model` must be one of: {_SIGMA8_MODELS}.")

        # Read emulation config.
        config_emu_dict = read_emulation_config_from_file(
            f"sigma8/sigma8_{model}_emulation_config.toml"
        )

        # Read cosmo params.
        cosmo_params = read_cosmo_params_from_file(f"sigma8/cosmo_params_{model}.txt")
        # Read cosmo params ranges.
        cosmo_params_range = read_cosmo_params_range_from_file(
            f"sigma8/cosmo_params_{model}_config.toml"
        )

        # Read training data.
        data = read_data_array_from_file_txt(f"sigma8/sigma8_{model}_data.txt")

        super().__init__(
            params=cosmo_params,
            data=data,
            params_range=cosmo_params_range,
            config_emu_dict=config_emu_dict,
            use_persistent_storage=True,
            persistent_storage_key=f"sigma8_{model}",
            random_seed=random_seed,
            verbose=verbose,
            ignore_training_warnings=use_persistent_storage,
            logger_name=f"e-MANTIS:sigma8:{model}",
        )

    def predict_sigma8(
        self,
        cosmo_params: dict[str, float | list[float] | npt.NDArray],
    ) -> npt.NDArray:
        """Predict the value of sigma8.

        Calling the function to give predictions for ``n_cosmo`` models at once
        is significantly faster than calling it ``n_cosmo`` times for a single model.

        Parameters
        ----------
        cosmo_params : dict
            A dictionary passing the cosmological parameters.

        Returns
        -------
        sigma8 : ndarray
            Predicted values of sigma8.
            The output is an array of shape (n_cosmo,), where ``n_cosmo``
            is the number of input cosmological models.

        """
        sigma8 = self._predict_observable(cosmo_params)
        return sigma8

    @property
    def params_range(self) -> dict:
        """dict: Allowed emulation range for each cosmological parameter."""
        assert self._params_range is not None
        return self._params_range


class NonLinearBoostEmulator(GaussianProcessEmulator1Dx1D):
    """Emulator for the nonlinear matter power spectrum boost.

    The nonlinear boost defined as the ratio of the nonlinear
    matter power spectrum and the linear one.

    Parameters
    ----------
    model : str
        Type of cosmological model.

        'wCDM'
            Dark energy with constant equation of state parameter.
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
        model: str = "wCDM",
        random_seed: int | None = None,
        n_jobs: int = 1,
        verbose: bool = True,
        use_persistent_storage: bool = True,
    ) -> None:
        # Check model.
        if model not in _NL_BOOST_MODELS:
            raise ValueError(f"`model` must be one of: {_NL_BOOST_MODELS}.")

        # Observable name and simulation suite version.
        observable = "matter_power_spectrum_nl_boost"
        sim_version = 2

        # Read emulation configuration.
        config_emu_dict = read_emulation_config(observable, model, sim_version)

        # Read cosmological parameters.
        cosmo_params = read_cosmo_params(model, sim_version)
        # Read range of cosmological parameters.
        cosmo_params_range = read_cosmo_params_range(model, sim_version)

        # Read training data.
        (
            aexp_nodes,
            data,
            data_std,
            data_bins,
            gp_std_factor,
        ) = read_data_binned(
            observable,
            model,
            sim_version,
            prefix=None,
            read_data_std=False,
            read_gp_std_factor=False,
        )

        super().__init__(
            params=cosmo_params,
            data=data,
            data_bins=data_bins,
            data_nodes=aexp_nodes,
            data_std=data_std,
            gp_std_factor=gp_std_factor,
            params_range=cosmo_params_range,
            config_emu=config_emu_dict,
            use_persistent_storage=use_persistent_storage,
            persistent_storage_key=f"{observable}_{model}",
            random_seed=random_seed,
            n_jobs=n_jobs,
            verbose=verbose,
            ignore_training_warnings=True,
            logger_name=f"e-MANTIS:Pk_nl:{model}",
        )

        self._sigma8_emulator = Sigma8Emulator(
            model=model, random_seed=random_seed, verbose=verbose
        )

    def predict_boost(
        self,
        cosmo_params: dict[str, float | list[float] | npt.NDArray],
        aexp: float | list[float] | npt.NDArray,
        k: float | list[float] | npt.NDArray | None = None,
        squeeze: bool = True,
    ) -> npt.NDArray:
        """Predict the nonlinear matter power spectrum boost.

        The boost is defined as the ratio of the nonlinear matter power spectrum
        with respect to the linear one.

        Multiple sets of cosmological parameters can be passed at once
        by giving them in the form of arrays or lists (see tutorial).
        This function will return a prediction for each entry.
        Calling the function to give predictions for N models at once
        is significantly faster than calling it N times for a single model.

        Additionally, multiple scale factors per model can be requested at once.
        If `aexp` has ``n_aexp`` entries,
        then ``n_aexp`` outputs will be given for each model.

        Parameters
        ----------
        cosmo_params : dict
            A dictionary passing the cosmological parameters.
        aexp : float or list or array of shape (n_aexp,)
            Scale factor values.
        k : float or list or array of shape (n_k,) or None, default=None
            The wavenumber values at which to output
            the nonlinear matter power spectrum boost in units of h/Mpc.
            The same wavenumber values are used
            for all cosmological models and scale factors.
            If ``None``, the default emulator bins will be used.
        squeeze : bool, default=True
            If ``True``, remove axes of length one from the output array.

        Returns
        -------
        pred : ndarray
            Predicted nonlinear matter power spectrum boost at the input wavenumbers,
            cosmological models, and scale factor values.
            The output is an array of shape (n_aexp, n_cosmo, n_k),
            where ``n_aexp`` is the number of scale factor values
            per cosmological model,
            ``n_cosmo`` is the number of cosmological models,
            and ``n_k`` the number of wavenumber values.
            By default the output array is squeezed to remove axes of length one.
            This behaviour can be changed with the `squeeze` parameter.

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
            params=cosmo_params,
            node_var=aexp,
            bins=k,
            return_std=False,
            squeeze=squeeze,
        )

    @property
    def kbins(self):
        """Ndarray of shape (N,): Default wavenumber bins of the emulator.

        In units of h/Mpc.
        """
        # WARNING: this assumes that all aexp nodes share the same bins.
        # We simply return the bins of the first aexp node.
        return self._emulator_nodes[self.aexp_nodes[0]]._data_bins

    @property
    def aexp_nodes(self):
        """list: The training scale factor nodes of the emulator."""
        return self._data_nodes

    @property
    def params_range(self) -> dict:
        """dict: Allowed emulation range for each cosmological parameter."""
        assert self._params_range is not None
        return self._params_range


# TODO: some things in this class are hardcoded assuming f(R) model.
# Needs modifications for future extension to other models (see TODOs).
class NonLinearMGBoostEmulator(GaussianProcessEmulator1Dx1D):
    """Emulator for the nonlinear matter power spectrum boost in modified gravity.

    The boost is defined as the ratio of the nonlinear
    matter power spectrum in modified gravity with respect to the nonlinear
    matter power spectrum in LCDM.

    Parameters
    ----------
    model : str
        Type of cosmological model.

        'fR'
            Hu & Sawicki f(R) gravity (limited to n=1).
            This is based on the extended e-MANTIS simulation suite.
        'fR_v1'
            Same as 'fR, but based on the first version
            of the e-MANTIS simulation suite.
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
        model: str = "fR",
        random_seed: int | None = None,
        n_jobs: int = 1,
        verbose: bool = True,
        use_persistent_storage: bool = True,
    ) -> None:
        # Check model.
        if model not in _NL_MG_BOOST_MODELS:
            raise ValueError(f"`model` must be one of: {_NL_MG_BOOST_MODELS}.")

        # Observable name.
        observable = "matter_power_spectrum_nl_mg_boost"

        # Sim. version.
        if "_v1" in model:
            model = "fR"
            sim_version = 1
            self._v1 = True
        else:
            sim_version = 2
            self._v1 = False

        # Read emulation configuration.
        config_emu_dict = read_emulation_config(observable, model, sim_version)

        # Read cosmological parameters.
        cosmo_params = read_cosmo_params(model, sim_version)
        # Read range of cosmological parameters.
        cosmo_params_range = read_cosmo_params_range(model, sim_version)

        # Read training data.
        (
            aexp_nodes,
            data,
            data_std,
            data_bins,
            gp_std_factor,
        ) = read_data_binned(
            observable,
            model,
            sim_version,
            prefix=None,
            read_data_std=False,
            read_gp_std_factor=False,
        )

        super().__init__(
            params=cosmo_params,
            data=data,
            data_bins=data_bins,
            data_nodes=aexp_nodes,
            data_std=data_std,
            gp_std_factor=gp_std_factor,
            params_range=cosmo_params_range,
            config_emu=config_emu_dict,
            use_persistent_storage=use_persistent_storage,
            persistent_storage_key=f"{observable}_{model}_v{sim_version}",
            random_seed=random_seed,
            n_jobs=n_jobs,
            verbose=verbose,
            ignore_training_warnings=True,
            logger_name=f"e-MANTIS:Pk_nl_mg:{model}",
        )

        self._sigma8_emulator = Sigma8Emulator(
            model="LCDM", random_seed=random_seed, verbose=verbose
        )

    def predict_boost(
        self,
        cosmo_params: dict[str, float | list[float] | npt.NDArray],
        aexp: float | list[float] | npt.NDArray,
        k: float | list[float] | npt.NDArray | None = None,
        squeeze: bool = True,
        extrapolate_k_low: bool = True,
        extrapolate_cosmo: bool = False,
    ) -> npt.NDArray:
        """Predict the nonlinear modified gravity matter power spectrum boost.

        The boost is defined as the ratio of the nonlinear matter power spectrum
        in modified gravity with respect to
        the nonlinear matter power spectrum in LCDM.

        Multiple sets of cosmological parameters can be passed at once
        by giving them in the form of arrays or lists (see tutorial).
        This function will return a prediction for each entry.
        Calling the function to give predictions for N models at once
        is significantly faster than calling it N times for a single model.

        Additionally, multiple scale factors per model can be requested at once.
        If `aexp` has ``n_aexp`` entries,
        then ``n_aexp`` outputs will be given for each model.

        Parameters
        ----------
        cosmo_params : dict
            A dictionary passing the cosmological parameters.
        aexp : float or list or array of shape (n_aexp,)
            Scale factor values.
        k : float or list or array of shape (n_k,) or None, default=None
            The wavenumber values at which to output
            the nonlinear matter power spectrum boost in units of h/Mpc.
            The same wavenumber values are used
            for all cosmological models and scale factors.
            If ``None``, the default emulator bins will be used.
        squeeze : bool, default=True
            If ``True``, remove axes of length one from the output array.
        extrapolate_k_low : bool, default=True
            Extrapolation to low wavenumber values.
            If ``True``, the emulator will extrapolate its predictions
            for wavenumber values below the minimum emulation range.
            This is extrapolation should be safe to use.
        extrapolate_cosmo : bool, optinal (default=False)
            Extrapolation in terms of cosmological parameters.
            If ``True``, do a constant extrapolation of the boost
            for cosmological parameters outside of the emulation range.
            Only for standard parameters,
            there is no extrapolation for the modified gravity parameters.

        Returns
        -------
        pred : ndarray
            Predicted nonlinear matter power spectrum boost at the input wavenumbers,
            cosmological models, and scale factor values.
            The output is an array of shape (n_aexp, n_cosmo, n_k),
            where ``n_aexp`` is the number of scale factor values
            per cosmological model,
            ``n_cosmo`` is the number of cosmological models,
            and ``n_k`` the number of wavenumber values.
            By default the output array is squeezed to remove axes of length one.
            This behaviour can be changed with the `squeeze` parameter.

        """
        # Check if A_s in present in the input cosmological parameters.
        if "A_s" in cosmo_params:
            # WARNING: Needs to be changed if multiple parameters
            # with sigma8 in the name are present.
            sigma8_name = [param for param in self.params_range if "sigma8" in param][0]
            cosmo_params = convert_cosmo_params_from_As_to_sigma8(
                cosmo_params, self._sigma8_emulator, sigma8_name, emu_v1=self._v1
            )

        # TODO: move this constants extrapolation to base emulator class.
        # Constant extrapolation in cosmological parameters.
        if extrapolate_cosmo:
            # Check input parameter names,
            # but skip the check of the emulation range.
            self._check_input_params_dict(cosmo_params, check_range=False)

            for param in self.params_range:
                # TODO: this assumes f(R) gravity.
                # Do not extrapolate logfR0.
                if param == "logfR0":
                    continue
                cosmo_params[param] = np.clip(
                    cosmo_params[param],
                    a_min=self.params_range[param]["min_value"],
                    a_max=self.params_range[param]["max_value"],
                )

        # TODO: the extrapolation and clipping to low k assumes f(R) model.
        # Needs to be modified for future extension to other models.
        # TODO: do this clipping at the level of the base emulator class.
        return np.clip(
            self._predict_observable(
                params=cosmo_params,
                node_var=aexp,
                bins=k,
                return_std=False,
                squeeze=squeeze,
                extrapolate_bins_low=extrapolate_k_low,
            ),
            a_min=1,
            a_max=None,
        )

    @property
    def kbins(self):
        """Ndarray of shape (N,): Default wavenumber bins of the emulator.

        In units of h/Mpc.
        """
        # WARNING: this assumes that all aexp nodes share the same bins.
        # We simply return the bins of the first aexp node.
        return self._emulator_nodes[self.aexp_nodes[0]]._data_bins

    @property
    def aexp_nodes(self):
        """list: The training scale factor nodes of the emulator."""
        return self._data_nodes

    @property
    def params_range(self) -> dict:
        """dict: Allowed emulation range for each cosmological parameter."""
        assert self._params_range is not None
        return self._params_range
