"""Module implementing Gaussian Process based emulators.

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

import logging
import os
import platform
import shelve
import sys
import warnings
from copy import deepcopy
from importlib.resources import as_file, files
from typing import get_args

import numpy as np
import numpy.typing as npt
import scipy
import sklearn
from joblib import Parallel, delayed
from scipy.interpolate import BSpline, make_interp_spline
from sklearn import preprocessing
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import (
    RBF,
    ConstantKernel,
    Kernel,
    Matern,
    WhiteKernel,
)
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold

from emantis import _utils, _utils_inputs
from emantis._transformers import PCATransformer
from emantis._types import _DATA_TYPES, ConfigGPE1D, ConfigGPE1Dx1D

RESOURCES = files("emantis")


class BaseEmulator:
    """A base emulator class meant to be inherited.

    Parameters
    ----------
    params_range : dict or None, default=None
        A dict. with the emulation range of each input parameter.
        If ``None``, the emulator only accepts input parameters in the form of an array
        and it will never check if the requested input parameters
        are within the emulation range.
        WARNING: the order of the parameters in the dict matters.
    random_seed: int or None, default=None
        The random seed used to initialize random generators.
    n_jobs: int, default=1
        Maximum number of independent processes used to train the emulator.
        A value of -1 uses all available cores.
        Predictions always use `n_jobs=1`,
        since they are already fast and the parallelism overhead is not worth it.
        Additional parallelism might be used (via Numpy, SciPy, OpenMP),
        even when `n_jobs=1`.
        See the scikit-learn `documentation <https://scikit-learn.org/stable/computing/parallelism.html#parallelism>`_
        for more details.
    logger_name : str, default='e-MANTIS'
        Name used by the logging system.
    logger_time : bool, default=False
        If ``True``, add the current time to the beginning of each logger message.
    verbose : bool, default=True
        Whether to activate or not verbose output.
        If ``True``, set logger level to INFO.
        If ``False``, set logger level to WARNING.
    ignore_training_warnings : bool, default=False
        If ``True``, deactivate warnings during the emulator training.

    Attributes
    ----------
    _logger : logging.Logger
        The logger instance.
    _ignore_training_warnings : bool
        Option to deactivate warnings during the emulator training.
    _random_numbers : npt.NDArray
        A 1D array with cached random numbers.

    """

    _counter = 0
    """int: Counter counting the number of instances.

    Used when necessary to ensure a different logger name per BaseEmulator instance.
    """

    def __init__(
        self,
        params_range: dict[str, dict[str, float]] | None = None,
        random_seed: int | None = None,
        n_jobs: int = 1,
        logger_name: str = "e-MANTIS",
        logger_time: bool = False,
        verbose: bool = True,
        ignore_training_warnings: bool = False,
    ) -> None:
        # Get params names and range.
        self._params_range = params_range

        # Set random seed (which also initializes the random generator).
        self.random_seed = random_seed

        # Number of jobs.
        self.n_jobs = n_jobs

        # Set up logger name.
        if logger_time:
            logger_format: str = f"%(asctime)s {logger_name}: %(message)s"
        else:
            logger_format = f"{logger_name}: %(message)s"

        # Increase instance counter.
        BaseEmulator._counter += 1

        # Get logger using instance counter in the name,
        # so that different instances do not mix their loggers.
        # Note: the instance counter is not used in the displayed logger name,
        # different instances might display the same name.
        self._logger = logging.getLogger(f"{logger_name}_{BaseEmulator._counter}")

        # Set up logger handler.
        handler = logging.StreamHandler(sys.stdout)
        fm = logging.Formatter(logger_format, datefmt="%H:%M:%S")
        handler.setFormatter(fm)

        # Add logger handler.
        self._logger.addHandler(handler)

        # Verbosity.
        self.verbose = verbose

        # Training warnings.
        self._ignore_training_warnings = ignore_training_warnings

        # Initial random numbers.
        self._random_numbers = self._random_generator.normal(loc=0, scale=1, size=10)

    @property
    def params_range(self) -> dict | None:
        """Dict or None: Allowed range for each cosmological parameter."""
        return self._params_range

    @property
    def random_seed(self) -> int | None:
        """Int or None: The random seed used to initialize random generators.

        If set to a new value, the random generator is reinitialized with the new seed.
        Any cached random number will be regenerated.
        """
        return self._random_seed

    @random_seed.setter
    def random_seed(self, value: int | None) -> None:
        self._random_seed = value
        self._random_generator = np.random.default_rng(value)
        self._random_numbers = self._random_generator.normal(loc=0, scale=1, size=10)

    @property
    def n_jobs(self) -> int:
        """int: Maximum number of independent processes used to train the emulator.

        A value of -1 uses all available cores.
        Predictions always use `n_jobs=1`,
        since they are already fast and the parallelism overhead is not worth it.
        Additional parallelism might be used (via Numpy, SciPy, OpenMP),
        even when `n_jobs=1`.
        See the scikit-learn `documentation <https://scikit-learn.org/stable/computing/parallelism.html#parallelism>`_
        for more details.
        """
        return self._n_jobs

    @n_jobs.setter
    def n_jobs(self, value: int) -> None:
        self._n_jobs = value

    @property
    def verbose(self) -> bool:
        """bool: Variable controlling output verbosity.

        If ``True``, set logger level to INFO.
        If ``False``, set logger level to WARNING.
        """
        return self._verbose

    @verbose.setter
    def verbose(self, value: bool) -> None:
        if value:
            self._logger.setLevel(logging.INFO)
        else:
            self._logger.setLevel(logging.WARNING)
        self._verbose = value

    def _format_input_params_to_array(
        self,
        input_params: dict[str, float | list[float] | npt.NDArray] | npt.NDArray,
    ) -> npt.NDArray:
        """Format input parameters to an array.

        The input `input_params` can be an array or a dict.

        If the input is an array it is returned as is.
        If `required_params_range` is not ``None``, check the range of each parameter.
        If `required_params_names` is not ``None``, it will assume that
        the parameters are ordered as in `required_params_range`.
        Otherwise, it will assume that the parameters are ordered
        as the keys of `required_params_range`.

        If the input is a dict, it will convert it into an array.
        First, it orders the input parameters according to `required_params_names`.
        At the same time, it checks that the provided dict entries have valid names, and
        that all the required parameters are present.
        If `required_params_names` is ``None``, it raises an exception.
        If `required_params_range` is not ``None``, it will check
        the range of each parameter.

        When checking the range of the parameters,
        it raises an exception if one sample is out of range.

        Parameters
        ----------
        input_params : dict or ndarray of shape (n_samples, n_params)
            A dictionary with the input parameters.

        Returns
        -------
        params_array : ndarray of shape (n_params,) or (n_samples, n_params)
            Array containing the input parameters, where `n_params` is the number
            of parameters and `n_samples` the number of inputs per parameter.

        Raises
        ------
        TypeError
            If `input_params` is a dict, but this instance was not initialized with
            a `params_range` dict.
        ValueError
            If the number of values in `input_params` for different
            parameters is not compatible.

        """
        if isinstance(input_params, np.ndarray):
            params_array = input_params

            # Ensure correct array shape.
            if params_array.ndim == 1:
                params_array = params_array.reshape(1, -1)

            # Check each parameter range if necessary.
            if self.params_range is not None:
                # Loop over all parameters.
                for i, param_name in enumerate(self.params_range):
                    _utils_inputs.check_emulation_range(
                        params_array[:, i],
                        self.params_range[param_name]["min_value"],
                        self.params_range[param_name]["max_value"],
                        param_name,
                    )

        elif isinstance(input_params, dict):
            if self.params_range is None:
                raise TypeError(
                    """This instance only accepts the 'params' argument
                    in the form of an array, since the 'params_range' argument
                    was not provided when instantiated."""
                )

            # First check names (and range) of input parameters.
            self._check_input_params_dict(input_params)

            # Init. counter for the number of samples per parameter.
            n_samples: int = 1
            # First loop over all parameters in the input dict. in order
            # to check how many values have been passed for each of them.
            for param_name in input_params:
                # Recover the set of values for a given parameter
                # in the form of a 1D array.
                param_array = _utils_inputs.format_input_to_1d_array(
                    input_params[param_name], param_name
                )
                n: int = param_array.shape[0]
                if n > n_samples:
                    if n_samples == 1:
                        n_samples = n
                    else:
                        # TODO: custom exception or better error message.
                        raise ValueError("Wrong format for input parameters.")

            # Init. final params array.
            params_array = np.zeros((n_samples, len(self.params_range)))
            # Second loop over all parameters in order
            # to gather them in an array.
            for i, param_name in enumerate(self.params_range):
                # Recover the set of values for a given parameter
                # in the form of a 1D array.
                # TODO: optimize: avoid recomputing this.
                param_array = _utils_inputs.format_input_to_1d_array(
                    input_params[param_name], param_name
                )
                n = param_array.shape[0]
                if n == 1:
                    param_array = np.array([param_array[0] for k in range(n_samples)])
                params_array[:, i] = param_array
        else:
            raise TypeError("Argument 'params' must be a dict or a ndarray.")

        return params_array

    def _check_input_params_dict(
        self,
        input_params_dict: dict[str, float | list[float] | npt.NDArray],
        check_range: bool = True,
    ) -> None:
        """Check input parameter dict.

        Check that the input parameters have valid names,
        and that all the required parameters have been provided.

        Can also check the range of the input parameters (see `required_params_range`).

        Parameters
        ----------
        input_params_dict : dict
            A dictionary with the input parameters.
        check_range : bool, default=True
            If ``True`` check that the input parameters are within
            the allowed emulation range.

        Raises
        ------
        TypeError
            If this instance was not initialized with a `params_range` dict.
        KeyError
            If the keys of `input_params_dict` do not match
            those of the attribute `params_range`.

        """
        if self.params_range is None:
            raise TypeError(
                """This instance only accepts the 'params' argument
                in the form of an array, since the 'params_range' argument
                was not provided when instantiated."""
            )

        # Check that all the provided parameter names are valid.
        for param in input_params_dict:
            if param not in self.params_range:
                raise KeyError(f"The provided parameter '{param}' is not supported.")

        # Check that all the required parameters
        # have been provided.
        for param in self.params_range:
            if param not in input_params_dict:
                raise KeyError(f"The parameter '{param}' is missing.")

        # Check emulation range.
        if check_range:
            # Loop over input parameters.
            for param_name in input_params_dict:
                _utils_inputs.check_emulation_range(
                    input_params_dict[param_name],
                    self.params_range[param_name]["min_value"],
                    self.params_range[param_name]["max_value"],
                    param_name,
                )


class GaussianProcessEmulator1D(BaseEmulator):
    """A Gaussian process based cosmological emulator for a 1D observable.

    Two types of 1D data are supported:
        - binned: binned data
        - bspline: coefficients of a B-spline decomposition

    The 1D data dimensionality can be reduced by a PCA before doing the emulation.
    This is optional.

    Finally, each PCA coefficient, B-spline coefficient,
    or data bin is emulated by a Gaussian process independently from the others.
    """

    def __init__(
        self,
        params: npt.NDArray,
        data: npt.NDArray,
        data_bins: npt.NDArray | None = None,
        data_std: npt.NDArray | None = None,
        bspline_degree: int | None = None,
        gp_std_factor: npt.NDArray | None = None,
        config_emu_dict: dict | None = None,
        config_emu: ConfigGPE1D | None = None,
        use_persistent_storage: bool = False,
        persistent_storage_key: str = "my_emulator",
        **base_emulator_kwargs,
    ) -> None:
        """Initialize the emulator.

        Parameters
        ----------
        params : ndarray of shape (n_models, n_params)
            The parameters of each training model,
            where ``n_models`` is the number of training models,
            and ``n_params`` is the number of parameters per model.
        data : ndarray of shape (n_samples, n_data)
            The 1D training data for each training model,
            where ``n_models`` is the number of training models,
            and ``n_data`` is the number of data points per training model.
        data_bins : ndarray of shape (n_data,) or None, default=None
            The data bins or B-spline decomposition knots of the training data,
            where ``n_data`` is the number of data points per training model.
        data_std : ndarray of shape (n_models, n_data) or None, default=None
            The standard errors of the training data for each training model,
            where ``n_models`` is the number of training models,
            and ``n_data`` is the number of data points per training model.
            If ``None``, no data errors will be included
            in the Gaussian process regression.
        bspline_degree : int or None, default=None
            The degree of the splines.
            Only relevant when the provided 1D data
            are coefficients of a B-spline decomposition,
            in which case this argument is mandatory.
        gp_std_factor : ndarray of shape (n_data,) or None, default=None
            An array of multiplicative factors,
            which are applied to the output standard deviation of each Gaussian process,
            where ``n_data`` is the number of data points per training model.
        config_emu_dict : dict or None, default=None
            The configuration of the emulator in the form of a dictionary.
        config_emu : _types.ConfigGPE1D or None, default=None
            The configuration of the emulator.
            Has the priority over `config_emu_dict`.
            If both are ``None``, the default settings are used.
        use_persistent_storage : bool, default=False
            If ``True``, save trained emulator to a local persistent storage database,
            based on the pickle protocol.
            If a trained emulator is already present in the database,
            load it and skip emulator training.
            If ``False``, never load previously trained emulator from the
            persistent storage database.
        persistent_storage_key : str, default="my_emulator"
            Key used to identify the emulator in the local persistent storage database.
            Be sure to give a unique key to each emulator,
            otherwise unexpected things will happen.
        **base_emulator_kwargs
            Arguments passed to :py:class:`~emantis._gp_emulation.BaseEmulator`.

        Raises
        ------
        ValueError
            If `data_std` is provided and ``y_transform=="log10"``
            in the `config_emu` or `config_emu_dict` provided settings.
        ValueError
            If type of data is bspline and `data_bins` is not provided.

        """
        # Init. base emulator parent.
        super().__init__(**base_emulator_kwargs)

        # Persistent storage options.
        self.use_persistent_storage = use_persistent_storage
        self.persistent_storage_key = persistent_storage_key

        # Read emulation config.
        # config_emu has the priority over config_emu_dict
        if config_emu is None:
            if config_emu_dict is None:
                config_emu_dict = {}
            self._config_emu = ConfigGPE1D(**config_emu_dict)
        else:
            self._config_emu = config_emu

        self._params = params

        # TODO: solve this compatibility problem.
        if (
            self._config_emu.data.data_type == "binned"
            and self._config_emu.data.binned.y_transform == "log10"
            and data_std is not None
        ):
            raise ValueError(
                "Input log10 transformation (`y_transform`)"
                " is not compatible with input data_std."
            )

        self._data = data

        self._data_bins = data_bins

        if self._config_emu.data.data_type == "bspline" and self._data_bins is None:
            raise ValueError(
                "For data of type `bspline` you must provide a value for `data_bins`."
            )

        self._data_std = data_std
        self._gp_std_factor = gp_std_factor

        # No need for PCA if there is a single target.
        if self._data.shape[1] == 1:
            self._config_emu.pca.do_pca = False

        if bspline_degree is not None:
            self._bspline_degree = bspline_degree

        # Init. PCA transformer.
        if self._config_emu.pca.do_pca:
            self._pca_transformer = PCATransformer(
                self._config_emu.pca.pca_n_components,
                self._config_emu.pca.pca_scale_data_mean,
                self._config_emu.pca.pca_scale_data_std,
                self._config_emu.pca.niter,
                self.random_seed,
            )
            self._gp_n_outputs = (
                self._config_emu.pca.pca_n_components
                if self._config_emu.pca.pca_n_components is not None
                else data.shape[1]
            )
        else:
            self._gp_n_outputs = data.shape[1]

        # Set up the GP kernel.
        if not isinstance(self._config_emu.gp.kernel_nu, list):
            kernel_nu_list = [
                self._config_emu.gp.kernel_nu for _ in range(self._gp_n_outputs)
            ]
        else:
            kernel_nu_list = self._config_emu.gp.kernel_nu

        if not isinstance(self._config_emu.gp.kernel_white, list):
            kernel_white_list = [
                self._config_emu.gp.kernel_white for _ in range(self._gp_n_outputs)
            ]
        else:
            kernel_white_list = self._config_emu.gp.kernel_white

        self._kernel_list = [
            self._get_gp_kernel(
                kernel_nu_list[i], kernel_white_list[i], self._params.shape[1]
            )
            for i in range(self._gp_n_outputs)
        ]

        # Init. parameter scaler.
        self._params_scaler = preprocessing.StandardScaler()

        # Init. empty list to contain of GPR.
        # Don't know the actual number of GP outputs yet.
        self._gp_regressor_list: list[GaussianProcessRegressor] = []

    def _get_gp_kernel(
        self, kernel_nu: float, kernel_white: bool, n_params: int
    ) -> Kernel:
        if kernel_nu == -1:
            kernel = ConstantKernel(
                constant_value=1, constant_value_bounds=(1e-10, 1e10)
            ) * RBF(
                length_scale=[1 for i in range(n_params)],
                length_scale_bounds=(1e-10, 1e10),
            )
        else:
            kernel = ConstantKernel(
                constant_value=1, constant_value_bounds=(1e-10, 1e10)
            ) * Matern(
                length_scale=[1 for i in range(n_params)],
                length_scale_bounds=(1e-10, 1e10),
                nu=kernel_nu,
            )
        if kernel_white:
            kernel += WhiteKernel()

        return kernel

    def train(self, n_jobs: int | None = None) -> None:
        """Train the emulator.

        Any previous training will be overwritten,
        including in the local persistent storage.

        Parameters
        ----------
        n_jobs: int or None, default=None
            Maximum number of independent processes used to train each emulator node.
            A value of -1 uses all available cores.
            If ``None``, use the value passed when
            this emulator instance was initialized.
            Additional parallelism might be used (via Numpy, SciPy, OpenMP),
            even when `n_jobs=1`.
            See the scikit-learn `documentation <https://scikit-learn.org/stable/computing/parallelism.html#parallelism>`_
            for more details.

        """
        if n_jobs is None:
            n_jobs = self.n_jobs

        self._logger.info("Training the emulator...")

        self._train(self._params, self._data, self._data_std, n_jobs)

        # TODO: include emantis version somewhere.
        # This would allow for instance to force a retraining
        # of the emulator when the emantis version changes.
        # Not mandatory but good to avoid problems.
        # Difficulty: how to delete exisiting trained objects
        # from the previous version when the emantis version was
        # not tracked.
        # Open shelve.
        if self.use_persistent_storage:
            with as_file(RESOURCES / "data/emulator_storage") as myfile:
                # TODO: this conversion with as_posix()
                # is required only for python < 3.11.
                # Remove it if support for python 3.10 is dropped.
                filename = myfile.as_posix()
                with shelve.open(filename) as db:
                    # Store input parameters scaler.
                    db[f"{self.persistent_storage_key}_params_scaler"] = (
                        self._params_scaler
                    )
                    # Store PCA transformer.
                    if self._config_emu.pca.do_pca:
                        db[f"{self.persistent_storage_key}_pca_transformer"] = (
                            self._pca_transformer
                        )
                    # Store GPs.
                    db[f"{self.persistent_storage_key}_gp_regressor_list"] = (
                        self._gp_regressor_list
                    )

                    # Store python, numpy, scipy, and sklearn versions.
                    db[f"{self.persistent_storage_key}_emulator_python_version"] = (
                        platform.python_version()
                    )
                    db[f"{self.persistent_storage_key}_emulator_numpy_version"] = (
                        np.__version__
                    )
                    db[f"{self.persistent_storage_key}_emulator_scipy_version"] = (
                        scipy.__version__
                    )
                    db[f"{self.persistent_storage_key}_emulator_sklearn_version"] = (
                        sklearn.__version__
                    )

                    self._logger.info(
                        "...saved emulator to local persistent storage..."
                    )

        self._logger.info("...training completed.")

    def _predict_observable(
        self,
        params: npt.NDArray | dict,
        bins: float | list[float] | npt.NDArray | None = None,
        return_std: bool = False,
        extrapolate_bins_low: bool = False,
        extrapolate_bins_high: bool = False,
        check_params: bool = True,
        squeeze: bool = True,
    ) -> npt.NDArray | tuple[npt.NDArray, npt.NDArray]:
        """Compute emulator predictions.

        Parameters
        ----------
        params : ndarray of shape (n_models, n_params) or dict
            The parameters, where `n_models` is the number of different models requested
            and `n_params` is the number of parameters.
            A dict is only accepted when `check_params=True` (see below).
        bins : float or list or ndarray of shape (n_bins,) or None, default=None
            The bins at which predictions are requested,
            where `n_bins` is the number of bins.
        return_std : bool, default=False
            If ``True``, also return the standard deviation of the predictions.
            Might slow down the computation.
        extrapolate_bins_low : bool, default=False
            If ``True``, extrapolate the predictions for values of `bins`
            below the emulation range.
            If ``False``, an exception will be raised if values
            below the emulation range are requested.
        extrapolate_bins_high : bool, default=False
            If ``True``, extrapolate the predictions for values of `bins`
            above the emulation range.
            If ``False``, an exception will be raised if values
            above the emulation range are requested.
        check_params : bool, default=True
            If ``True``, validate the provided `params`.
            An exception is raised if some of them are missing
            and/or out of the emulation range.
            If ``False``, `params` must be an array and not a dict.
        squeeze : bool, default=True
            If ``True``, remove axes of length one from `pred`.

        Returns
        -------
        pred : ndarray of shape (n_models, n_bins)
            The emulator predictions.
        std : ndarray of shape (n_models, n_bins)
            The standard deviation of the predictions.
            Only returned when `return_std` is ``True``.

        Raises
        ------
        ValueError
            If `bins` is provided but this instance was not initialized
            with a `data_bins`.
        ValueError
            If data type is bspline and values for `bins` have not been provided.
        TypeError
            If `check_params` is ``False`` and `params` is not an array.

        """
        # Convert bins to a 1D array.
        if bins is not None:
            if self._data_bins is None:
                raise ValueError("This instance does not accept the `bins` argument.")

            bins_array = _utils_inputs.format_input_to_1d_array(
                bins, self._config_emu.data.variable_name
            )

            # Check bin range.
            _utils_inputs.check_emulation_range(
                bins_array,
                self._bin_range()[0] if not extrapolate_bins_low else None,
                self._bin_range()[1] if not extrapolate_bins_high else None,
                self._config_emu.data.variable_name,
            )
        else:
            if self._config_emu.data.data_type == "bspline":
                raise ValueError(
                    "For data type `bspline` you must provide bin values with `bins`."
                )

            bins_array = None

        if not check_params and not isinstance(params, np.ndarray):
            raise TypeError("If `check_params=False`, then `params` must be an array.")

        if check_params:
            # Format input params array,
            # while checking for provided parameters and ranges.
            params_array = self._format_input_params_to_array(
                params,
            )
        else:
            params_array = params

        # Get GPR predictions.
        pred_gp: npt.NDArray
        std_gp: npt.NDArray
        if return_std:
            pred_gp, std_gp = self._predict_gp(params_array, return_std=True)
            if self._gp_std_factor is not None:
                std_gp *= self._gp_std_factor
        else:
            pred_gp = self._predict_gp(params_array, return_std=False)

        # Transform GPR predictions.
        pred = self._transform_gp_prediction(pred_gp, x=bins_array)

        # Squeeze output(s) if necessary.
        if squeeze:
            pred = np.squeeze(pred)

        # Propagate GPR std if requested.
        if return_std:
            std = self._propagate_gp_std(pred_gp, std_gp, x=bins_array)
            # Squeeze output(s) if necessary.
            if squeeze:
                std = np.squeeze(std)

            return pred, std

        return pred

    # TODO: docstring.
    def leave_one_out(
        self,
        x: float | list[float] | npt.NDArray | None = None,
        leave_out_models: list[int] | None = None,
        excluded_models: list[int] | None = None,
        batch_size: int = 1,
        n_jobs: int | None = None,
        return_std: bool = False,
        return_gp: bool = False,
        **kwargs_joblib,
    ) -> npt.NDArray | tuple[npt.NDArray, npt.NDArray]:
        # Save current emulator state.
        emulator = deepcopy(self._gp_regressor_list)
        if self._config_emu.pca.do_pca:
            pca_transformer = deepcopy(self._pca_transformer)

        if excluded_models is None:
            excluded_models = []

        if leave_out_models is None:
            leave_out_models = list(range(self._params.shape[0]))

        if n_jobs is None:
            n_jobs = self.n_jobs

        if len(leave_out_models) % batch_size != 0:
            raise ValueError("batch_size not compatible with number of models")

        models = []
        nbatch = len(leave_out_models) // batch_size
        for i in range(nbatch):
            models += [
                [leave_out_models[i * batch_size + j] for j in range(batch_size)]
            ]

        result = Parallel(n_jobs=n_jobs, **kwargs_joblib)(
            delayed(self._leave_one_out_single)(
                n, x, excluded_models, return_std, return_gp
            )
            for n in models
        )

        if return_std:
            predictions, errors = zip(*result, strict=True)
        else:
            predictions = result

        pred_array = predictions[0]
        for elt in predictions[1:]:
            pred_array = np.vstack((pred_array, elt))

        if return_std:
            std_array = errors[0]
            for elt in errors[1:]:
                std_array = np.vstack((std_array, elt))

        # Restore previous emulator state.
        self._gp_regressor_list = emulator
        if self._config_emu.pca.do_pca:
            self._pca_transformer = pca_transformer

        if return_std:
            return pred_array, std_array

        return pred_array

    def kfold_cross_validation_score(
        self,
        n_splits: int = 5,
        shuffle: bool = True,
        target_std: npt.NDArray | None = None,
        n_jobs: int | None = None,
        **kwargs_joblib,
    ) -> list[float]:
        """Compute a mean squared error cross-validation score.

        The emulator dataset is split into k different folds.
        Pairs of training/validation sets are built using k-1 folds
        for training and the remaining fold for validation.
        For each of the k pairs, a mean squared error validation score is computed
        using :py::meth:`~emantis._gp_emulation.validation_score`.

        At the end of the procedure,
        the emulator is returned to its previous training state.

        Parameters
        ----------
        n_splits : int, default=5
            The number of folds. Must be at least 2.
        shuffle : bool, default=True
            If ``True``, shuffle the data before splitting into folds.
        n_jobs: int or None, default=None
            Maximum number of independent processes used to parallelize the procedure.
            The parallelization is done over the different folds,
            such that setting `n_jobs` larger than `n_splits`
            will not speed up the computation further.
            A value of -1 uses all available cores.
            If ``None``, use the value passed when
            this emulator instance was initialized.
            Additional parallelism might be used (via Numpy, SciPy, OpenMP),
            even when `n_jobs=1`.
            See the scikit-learn `documentation <https://scikit-learn.org/stable/computing/parallelism.html#parallelism>`_
            for more details.
        **kwargs_joblib
            Arguments passed to `Parallel` function from `joblib`.

        Returns
        -------
        score : list[float]
            The list of mean squared error scores for each fold.

        """
        if self._config_emu.data.data_type == "bspline":
            raise NotImplementedError(
                "This function not yet compatible with bspline data."
            )

        if n_jobs is None:
            n_jobs = self.n_jobs

        kfold = KFold(n_splits=n_splits, shuffle=shuffle)
        kfold_iterator = kfold.split(self._params)

        # Compute validation scores for each fold.
        scores = Parallel(n_jobs=n_jobs, **kwargs_joblib)(
            delayed(self.validation_score)(models[0], models[1], target_std)
            for models in kfold_iterator
        )

        return scores

    def kfold_cross_validation_predictions(
        self,
        n_splits: int = 5,
        shuffle: bool = True,
        n_jobs: int | None = None,
        **kwargs_joblib,
    ) -> tuple[npt.NDArray, npt.NDArray]:
        """Compute cross-validation emulator predictions.

        The emulator dataset is split into k different folds.
        Pairs of training/validation sets are built using k-1 folds
        for training and the remaining fold for validation.
        The predictions of the emulator for the validation set
        of each fold are stacked together and returned in a single array.
        The validation data of each fold is also returned.

        At the end of the procedure,
        the emulator is returned to its previous training state.

        Parameters
        ----------
        n_splits : int, default=5
            The number of folds. Must be at least 2.
        shuffle : bool, default=True
            If ``True``, shuffle the data before splitting into folds.
        n_jobs: int or None, default=None
            Maximum number of independent processes used to parallelize the procedure.
            The parallelization is done over the different folds,
            such that setting `n_jobs` larger than `n_splits`
            will not speed up the computation further.
            A value of -1 uses all available cores.
            If ``None``, use the value passed
            when this emulator instance was initialized.
            Additional parallelism might be used (via Numpy, SciPy, OpenMP),
            even when `n_jobs=1`.
            See the scikit-learn `documentation <https://scikit-learn.org/stable/computing/parallelism.html#parallelism>`_
            for more details.
        **kwargs_joblib
            Arguments passed to `Parallel` function from `joblib`.

        Returns
        -------
        pred_val : ndarray of shape (n_models, n_outputs)
            The emulator predictions for each fold stacked together,
            where `n_models` is the total number of models
            available and `n_outputs` is the number of outputs of the emulator.
        data_val : ndarray of shape (n_models, n_outputs)
            The validation data of each fold stacked together.

        """
        if self._config_emu.data.data_type == "bspline":
            raise NotImplementedError(
                "This function not yet compatible with bspline data."
            )

        if n_jobs is None:
            n_jobs = self.n_jobs

        kfold = KFold(n_splits=n_splits, shuffle=shuffle)
        kfold_iterator = kfold.split(self._params)

        # Compute validation predictions for all the folds.
        res = Parallel(n_jobs=n_jobs, **kwargs_joblib)(
            delayed(self.validation_prediction)(
                models[0],
                models[1],
            )
            for models in kfold_iterator
        )
        res = [elt for elt in zip(*res, strict=True)]

        # Stack all validation predictions
        # and data into an array of shape (n_models, n_outputs).
        predictions = np.vstack(res[0])
        data = np.vstack(res[1])

        return predictions, data

    def kfold_cross_validation_covariance(
        self,
        n_splits: int = 5,
        shuffle: bool = True,
        n_jobs: int | None = None,
        **kwargs_joblib,
    ) -> npt.NDArray:
        """Compute a cross-validation covariance.

        The emulator dataset is split into k different folds.
        Pairs of training/validation sets are built using k-1 folds
        for training and the remaining fold for validation.
        A covariance is computed using the difference between
        validation set data and emulator predictions.
        The data from all the folds is stacked together before computing the covariance.

        At the end of the procedure,
        the emulator is returned to its previous training state.

        Parameters
        ----------
        n_splits : int, default=5
            The number of folds. Must be at least 2.
        shuffle : bool, default=True
            If ``True``, shuffle the data before splitting into folds.
        n_jobs: int or None, default=None
            Maximum number of independent processes used to parallelize the procedure.
            The parallelization is done over the different folds,
            such that setting `n_jobs` larger than `n_splits`
            will not speed up the computation further.
            A value of -1 uses all available cores.
            If ``None``, use the value passed when
            this emulator instance was initialized.
            Additional parallelism might be used (via Numpy, SciPy, OpenMP),
            even when `n_jobs=1`.
            See the scikit-learn `documentation <https://scikit-learn.org/stable/computing/parallelism.html#parallelism>`_
            for more details.
        **kwargs_joblib
            Arguments passed to `Parallel` function from `joblib`.

        Returns
        -------
        covariance : ndarray of shape (n_outputs, n_outputs)
            The covariance matrix,
            where `n_outputs` is the number of outputs of the emulator.

        """
        if self._config_emu.data.data_type == "bspline":
            raise NotImplementedError(
                "This function not yet compatible with bspline data."
            )

        if n_jobs is None:
            n_jobs = self.n_jobs

        predictions, data = self.kfold_cross_validation_predictions(
            n_splits=n_splits,
            shuffle=shuffle,
            n_jobs=n_jobs,
            **kwargs_joblib,
        )

        # Compute difference between validation predictions and data.
        diff = predictions - data

        # Compute covariance matrix.
        cov = np.cov(diff, rowvar=False, ddof=1)

        return cov

    def validation_score(
        self,
        train_models: npt.NDArray,
        val_models: npt.NDArray,
        target_std: npt.NDArray | None = None,
    ) -> float:
        """Compute a mean squared error validation score.

        The emulator is trained on a training set and evaluated on a validation set.
        The mean squared error score computed on the validation set is returned.

        If the emulator has multiple outputs,
        the score is averaged over all the outputs.
        The emulator outputs are scaled to a zero mean and
        unit variance distribution before computing the score,
        such that each output has an equivalent contribution to the final score.
        The mean and variance for this scaling are computed from the training set.

        At the end of the procedure,
        the emulator is returned to its previous training state.

        Parameters
        ----------
        train_models : ndarray of shape (n_train,)
            The training set indices, where `n_train` is the number of samples.
        val_models : ndarray of shape (n_val,)
            The validation set indices, where `n_val` is the number of samples.

        Returns
        -------
        score : float
            The mean squared error score.

        """
        if self._config_emu.data.data_type == "bspline":
            raise NotImplementedError(
                "This function not yet compatible with bspline data."
            )

        # Get predictions for validation set.
        pred_val, data_val = self.validation_prediction(train_models, val_models)

        # Scale outputs with training set data.
        data_train = self._data[train_models]
        scaler = preprocessing.StandardScaler().fit(data_train)

        data_val = scaler.transform(data_val)
        pred_val = scaler.transform(pred_val)

        if target_std is not None:
            target_std /= scaler.scale_

            data_val /= target_std
            pred_val /= target_std

        # Compute mean squared error score.
        score = mean_squared_error(
            data_val,
            pred_val,
            multioutput="uniform_average",
        )

        return score

    def validation_prediction(
        self,
        train_models: npt.NDArray,
        val_models: npt.NDArray,
    ) -> tuple[npt.NDArray, npt.NDArray]:
        """Compute emulator predictions for a validation set.

        The emulator is trained on a training set and evaluated on a validation set.

        At the end of the procedure,
        the emulator is returned to its previous training state.

        Parameters
        ----------
        train_models : ndarray of shape (n_train,)
            The training set indices, where `n_train` is the number of samples.
        val_models : ndarray of shape (n_val,)
            The validation set indices, where `n_val` is the number of samples.

        Returns
        -------
        pred_val : ndarray of shape (n_val, n_outputs)
            The emulator prediction for the validation set,
            where `n_val` is the number of samples
            in the validation set and
            `n_outputs` is the number of outputs of the emulator.
        data_val : ndarray of shape (n_val, n_outputs)
            The data of the validation set.

        """
        if self._config_emu.data.data_type == "bspline":
            raise NotImplementedError(
                "This function not yet compatible with bspline data."
            )

        # Save current emulator state.
        emulator = deepcopy(self._gp_regressor_list)
        if self._config_emu.pca.do_pca:
            pca_transformer = deepcopy(self._pca_transformer)

        # Select training set data.
        params_train = self._params[train_models]
        data_train = self._data[train_models]

        if self._data_std is not None:
            data_train_std = self._data_std[train_models]
        else:
            data_train_std = None

        # Fit GPR.
        self._train(
            params=params_train,
            data=data_train,
            data_std=data_train_std,
            n_jobs=1,
        )

        # Get predictions for validation set.
        params_val = self._params[val_models]
        pred_val = self._predict_observable(params_val, squeeze=False)

        # Select validation data (only in order to return it).
        data_val = self._data[val_models]

        # Restore previous emulator state.
        self._gp_regressor_list = emulator
        if self._config_emu.pca.do_pca:
            self._pca_transformer = pca_transformer

        return pred_val, data_val

    def _bin_range(self) -> tuple[float, float]:
        """tuple: The minimum and maximum bin range.

        The first element of the tuple gives the minimum,
        and the second element the maximum.

        Returns
        -------
        bin_min : float
            The minimum bin range.
        bin_max : float
            The maximum bin range.
        """
        assert self._config_emu.data.data_type in get_args(_DATA_TYPES)

        if self._config_emu.data.data_type == "binned":
            if self._data_bins is None:
                return 0, 0

            bins = self._data_bins

        elif self._config_emu.data.data_type == "bspline":
            assert self._data_bins is not None

            bins = _utils.inverse_simple_transform(
                self._data_bins,
                self._config_emu.data.bspline.x_transform,
            )

        bin_min: float = np.min(bins)
        bin_max: float = np.max(bins)

        return bin_min, bin_max

    def _fit_gp(
        self,
        kernel: Kernel,
        params: npt.NDArray,
        data: npt.NDArray,
        data_std: npt.NDArray | None = None,
    ) -> GaussianProcessRegressor:
        if self._ignore_training_warnings:
            # Ignore warnings during training.
            warnings.simplefilter("ignore")
            # Also for subprocesses.
            os.environ["PYTHONWARNINGS"] = "ignore"

        # Include data errors or not.
        alpha = data_std**2 if data_std is not None else 1e-10

        # Init. GPR.
        gp = GaussianProcessRegressor(
            kernel=kernel,
            alpha=alpha,
            n_restarts_optimizer=self._config_emu.gp.n_restarts_optimizer,
            random_state=self.random_seed,
            normalize_y=self._config_emu.gp.normalize_y,
        )

        # Fit GPR.
        gp.fit(params, data)

        if self._ignore_training_warnings:
            # Turn warnings back on.
            warnings.simplefilter("default")
            os.environ["PYTHONWARNINGS"] = "default"
        return gp

    def _train(
        self,
        params: npt.NDArray,
        data: npt.NDArray,
        data_std: npt.NDArray | None = None,
        n_jobs: int | None = None,
    ) -> None:
        # Fit parameter scaler.
        self._params_scaler.fit(params)

        # Scale parameters.
        params_scaled = self._params_scaler.transform(params)

        # For "binned" data, apply a transformation if requested.
        if self._config_emu.data.data_type == "binned":
            data = _utils.simple_transform(
                data, self._config_emu.data.binned.y_transform
            )

        # Fit PCA and transform data.
        if self._config_emu.pca.do_pca:
            # Fit PCA.
            self._pca_transformer.fit(data)

            # Transform data_std if required.
            # WARNING: data_std must be done BEFORE data.
            if data_std is not None:
                data_std = self._pca_transformer.propagate_std(data, data_std)

            # Transform data.
            # WARNING: data_std must be done BEFORE data.
            data = self._pca_transformer.transform(data)

        # Init. and fit GPR.
        if data_std is not None:
            self._gp_regressor_list = Parallel(n_jobs=n_jobs)(
                delayed(self._fit_gp)(
                    self._kernel_list[i], params_scaled, data[:, i], data_std[:, i]
                )
                for i in range(self._gp_n_outputs)
            )
        else:
            self._gp_regressor_list = Parallel(n_jobs=n_jobs)(
                delayed(self._fit_gp)(self._kernel_list[i], params_scaled, data[:, i])
                for i in range(self._gp_n_outputs)
            )

    def _load_from_persistent_storage(self):
        """Load emulator from local persistent storage."""
        with as_file(RESOURCES / "data/emulator_storage") as myfile:
            # TODO: this conversion with as_posix() is required only for python < 3.11.
            # Remove it if support for python 3.10 is dropped.
            filename = myfile.as_posix()
            with shelve.open(filename) as db:
                # Read input parameters scaler.
                self._params_scaler = db[f"{self.persistent_storage_key}_params_scaler"]
                # Read PCA transformer.
                if self._config_emu.pca.do_pca:
                    self._pca_transformer = db[
                        f"{self.persistent_storage_key}_pca_transformer"
                    ]
                # Read GPs.
                self._gp_regressor_list = db[
                    f"{self.persistent_storage_key}_gp_regressor_list"
                ]

                self._logger.info("Loaded emulator from local persistent storage.")

    def load_train_emulator(self, n_jobs: int | None = None):
        """Try to load the emulator from the local persistent storage.

        If loading fails, or persistent storage usage is not activated,
        train the emulator.

        If persistent storage usage is disabled,
        this function is equivalent to
        :py:meth:`~emantis._gp_emulation.GaussianProcessEmulator1D.train`.
        """
        if n_jobs is None:
            n_jobs = self.n_jobs

        if self.use_persistent_storage:
            # Try to load emulator from local persistent storage.
            try:
                self._load_from_persistent_storage()

            # If no emulator present in the local persistent storage do the training.
            except KeyError:
                self.train(n_jobs=n_jobs)

            # If the emulator is present but something went wrong in retrieving it.
            except Exception:
                with as_file(RESOURCES / "data/emulator_storage") as myfile:
                    # TODO: this conversion with as_posix()
                    # is required only for python < 3.11.
                    # Remove it if support for python 3.10 is dropped.
                    filename = myfile.as_posix()
                    with shelve.open(filename) as db:
                        self._logger.info(
                            "Emulator found in local persistent storage,"
                            " but failed to load it.\n"
                            f"Package versions used to train the emulator: "
                            f"python {db[f'{self.persistent_storage_key}_emulator_python_version']}, "  # noqa: E501
                            f"numpy {db[f'{self.persistent_storage_key}_emulator_numpy_version']}, "  # noqa: E501
                            f"scipy {db[f'{self.persistent_storage_key}_emulator_scipy_version']}, "  # noqa: E501
                            f"sklearn {db[f'{self.persistent_storage_key}_emulator_sklearn_version']}.\n"  # noqa: E501
                            f"Current package versions: python {platform.python_version()}, numpy {np.__version__}, scipy {scipy.__version__}, sklearn {sklearn.__version__}.\n"  # noqa: E501
                            "Emulator will be trained again from scratch."
                        )

                self.train(n_jobs=n_jobs)
        else:
            self.train(n_jobs=n_jobs)

    def _predict_gp(
        self, params: npt.NDArray, return_std: bool = False
    ) -> npt.NDArray | tuple[npt.NDArray, npt.NDArray]:
        """Compute GP predictions.

        Parameters
        ----------
        params : ndarray of shape (n_models, n_params)
            The parameters, where `n_models` is the number of different models requested
            and `n_params` is the number of parameters.
        return_std : bool, default=False
            If ``True``, also return the standard deviation of the predictions.

        Returns
        -------
        pred_gp : array-like of shape (n_models, n_outputs)
            The GP predictions,
            where `n_models` is the number of different models requested
            and `n_outputs` is the number of GP outputs.
        std_gp : array-like (n_models, n_outputs)
            The standard deviation of the GP predictions.
            Only returned when `return_std` is ``True``.

        """
        # Number of models.
        n_models = params.shape[0]

        # Train emulator (or load from local persistent storage) if necessary.
        if not self._gp_regressor_list:
            self.load_train_emulator()

        # Format input params array, while checking for provided parameters and ranges.
        params_array = self._format_input_params_to_array(params)

        # Scale input parameters.
        params_array_scaled = self._params_scaler.transform(params_array)

        # Init. empty arrays to collect GP predictions.
        pred_gp = np.empty((n_models, self._gp_n_outputs))
        if return_std:
            std_gp = np.empty((n_models, self._gp_n_outputs))

        # Get GP predictions.
        for i in range(self._gp_n_outputs):
            if return_std:
                pred_gp[:, i], std_gp[:, i] = self._gp_regressor_list[i].predict(
                    params_array_scaled, return_std=True
                )
            else:
                pred_gp[:, i] = self._gp_regressor_list[i].predict(
                    params_array_scaled, return_std=False
                )

        if return_std:
            return pred_gp, std_gp

        return pred_gp

    def _propagate_gp_std(
        self,
        pred_gp: npt.NDArray,
        std_gp: npt.NDArray,
        x: npt.NDArray | None = None,
    ) -> npt.NDArray:
        """Propagate the standard deviation from the GP to the final prediction.

        Parameters
        ----------
        pred_gp : ndarray of shape (n_models, M)
            The prediction of the GPR.
        std_gp : ndarray of shape (n_models, M)
            The standard deviation predicted by the GPR.
        x : ndarray of shape (N,) or None, default=None
            The bins of the main variable at which to output
            the prediction for the observable of interest.

        Returns
        -------
        std : ndarray of shape (n_models, N)
            The errors on the final prediction at the requested bins.

        """
        # Number of random iterations.
        niter = self._config_emu.emulator_std.niter

        # Target shape for random numbers.
        eps_shape = (niter, std_gp.shape[1])

        # Use existing random numbers if possible.
        # TODO: this does not seem to be the bottleneck,
        # so this cache is not very useful as of now.
        # The bottleneck seems to be the broadcasting
        # + _transform_gp_prediction of everything.
        if self._random_numbers.shape == eps_shape:
            eps = self._random_numbers

        # Generate random numbers with shape (n_iter,).
        else:
            eps = self._random_generator.normal(loc=0, scale=1, size=eps_shape)
            # Save them for later.
            self._random_numbers = eps

        # Broadcast random numbers from (n_iter, M) to (n_models, n_iter, M).
        eps = np.broadcast_to(eps, (std_gp.shape[0], eps.shape[0], eps.shape[1]))

        # Swap axes (n_models, n_iter, M) to (n_iter, n_models, M).
        eps = np.swapaxes(eps, axis1=0, axis2=1)

        # Broadcast GP predictions from (n_models, M) to (n_iter, n_models, M).
        pred_gp = np.broadcast_to(pred_gp, eps.shape)

        # Broadcast GP std predictions from (n_models, M) to (n_iter, n_models, M).
        std_gp = np.broadcast_to(std_gp, eps.shape)

        # Transform perturbed GP predictions to desired bin values.
        pred_random = self._transform_gp_prediction(pred_gp + eps * std_gp, x=x)

        # Compute standard deviation of the perturbed predictions.
        std = np.std(pred_random, axis=0, ddof=1)

        return std

    def _transform_gp_prediction(
        self, pred_gp: npt.NDArray, x: npt.NDArray | None
    ) -> npt.NDArray:
        """Transform the output from the GPR to a final prediction at fixed bin values.

        Parameters
        ----------
        pred_gp : ndarray of shape (..., M)
            The prediction of the GPR, where `M` is the number of GP outputs.
        x : ndarray of shape (N,) or None, default=None
            The bins of the main variable at which to output
            the prediction for the observable of interest.

        Returns
        -------
        pred : ndarray of shape (..., N)
            The final prediction at the requested bins.

        Raises
        ------
        ValueError
            If data type is bspline and values for `x` are not provided.
        ValueError
            If data type, as defined in the emulator config, is not supported.
            Possible values: bspline, binned.

        """
        # Inverse PCA.
        if self._config_emu.pca.do_pca:
            # Get array shape (..., M).
            pred_gp_shape = list(pred_gp.shape)

            # Reshape before PCA inverse transformation (-1, M).
            pred_gp = pred_gp.reshape(-1, pred_gp_shape[-1])

            # Inverse PCA.
            pred_gp = self._pca_transformer.inverse_transform(pred_gp)

            # Build final shape (..., N).
            pred_gp_shape[-1] = pred_gp.shape[-1]

            # Reshape.
            pred_gp = pred_gp.reshape(pred_gp_shape)

        # Deal with binned emulation data.
        if self._config_emu.data.data_type == "binned":
            # Return at the default emulator bins.
            if x is None:
                # Inverse transform predictions.
                pred = _utils.inverse_simple_transform(
                    pred_gp, self._config_emu.data.binned.y_transform
                )
                return pred

            else:
                assert self._data_bins is not None

                # Transform target bins before linear interpolation.
                x_target = _utils.simple_transform(
                    x, self._config_emu.data.binned.x_interp_type
                )
                # Transform prediction bins before linear interpolation.
                x_data = _utils.simple_transform(
                    self._data_bins,
                    self._config_emu.data.binned.x_interp_type,
                )

                # Transform predictions before linear interpolation.
                y_data = _utils.simple_transform(
                    pred_gp, self._config_emu.data.binned.y_interp_type
                )

                # Build linear interpolant.
                spl = make_interp_spline(x_data, y_data, k=1, axis=-1)

                # Interpolate.
                pred = spl(x_target)

                # Inverse transform interpolated predictions
                # after linear interpolation.
                pred = _utils.inverse_simple_transform(
                    pred, self._config_emu.data.binned.y_interp_type
                )

                # Inverse transform predictions.
                pred = _utils.inverse_simple_transform(
                    pred, self._config_emu.data.binned.y_transform
                )

        # Get final prediction from emulated BSpline coefficients.
        elif self._config_emu.data.data_type == "bspline":
            if x is None:
                raise ValueError(
                    "For data type `bspline` you must provide bin values `x`."
                )

            # Transform bins before BSpline evaluation.
            x_target = _utils.simple_transform(
                x, self._config_emu.data.bspline.x_transform
            )

            # Build BSplines.
            spl = BSpline(self._data_bins, pred_gp, self._bspline_degree, axis=-1)

            # Evaluate BSplines.
            pred = spl(x_target)

            # Inverse transform BSplines evaluations.
            pred = _utils.inverse_simple_transform(
                pred, self._config_emu.data.bspline.y_transform
            )

        else:
            raise ValueError(
                "Unsupported data type. Possible values are: binned or bspline."
            )

        return pred

    # TODO: type and docstring.
    def _leave_one_out_single(
        self,
        leave_models,
        x=None,
        excluded_models=None,
        return_std=False,
        return_gp=False,
    ):
        if excluded_models is None:
            excluded_models = []

        # Remove leave-out models parameter array.
        params_train = np.delete(self._params, leave_models, axis=0)
        # Remove extra models from parameter array.
        params_train = np.delete(params_train, excluded_models, axis=0)

        # Remove leave-out models from data array.
        data_train = np.delete(self._data, leave_models, axis=0)
        # Remove extra models from data array.
        data_train = np.delete(data_train, excluded_models, axis=0)

        # Same thing for data_std if necessary.
        if self._data_std is not None:
            data_train_std = np.delete(self._data_std, leave_models, axis=0)
            data_train_std = np.delete(data_train_std, excluded_models, axis=0)
        else:
            data_train_std = None

        # Fit GPR.
        self._train(
            params=params_train,
            data=data_train,
            data_std=data_train_std,
            n_jobs=1,
        )

        # Get parameters of the leave-out models.
        params_test = self._params[leave_models, :]

        # Get predictions for the leave-out models.
        # If requested, return raw GP predictions.
        if return_gp:
            if return_std:
                pred_test, std_test = self._predict_gp(
                    params=params_test, return_std=True
                )
                return pred_test, std_test
            else:
                pred_test = self._predict_gp(params=params_test, return_std=False)

        # Otherwise, return full observable predictions.
        else:
            if return_std:
                pred_test, std_test = self._predict_observable(
                    params_test, bins=x, return_std=True
                )
                return pred_test, std_test

            pred_test = self._predict_observable(params_test, bins=x, return_std=False)
            return pred_test


class GaussianProcessEmulator1Dx1D(BaseEmulator):
    """A Gaussian process based cosmological emulator for a 1Dx1D observable."""

    def __init__(
        self,
        params: npt.NDArray,
        data: dict,
        data_bins: dict,
        data_nodes: list,
        data_std: dict | None = None,
        bspline_degree: dict | None = None,
        gp_std_factor: dict | None = None,
        config_emu: dict | None = None,
        use_persistent_storage: bool = False,
        persistent_storage_key: str = "my_emulator",
        **base_emulator_kwargs,
    ) -> None:
        """Initialize the emulator.

        Parameters
        ----------
        params : array-like of shape (n_samples, n_params)
            The parameters representing the training data.
        data : dict
            The training data at each node.
        data_bins : dict
            The bins or bspline knots of the training data at each node.
        data_nodes : list
            The values of the nodes.
        data_std : dict or None, default=None
            The standard errors of the training data at each node.
        bspline_degree : dict or None, default=None
            The degree of the bpslines at each node.
        gp_std_factor : dict or None, default=None
            An array of multiplicative factors,
            which are applied to the output std of each GP at each node.
        config_emu : dict or None, default=None
            The configuration dict. If ``None``, use default settings.
        use_persistent_storage : bool, default=False
            If ``True``, save trained emulator to a local persistent storage database,
            based on the pickle protocol.
            If a trained emulator is already present in the database,
            load it and skip emulator training.
            If ``False``, never load previously trained emulator from the
            persistent storage database.
        persistent_storage_key : str, default="my_emulator"
            Key used to identify the emulator in the local persistent storage database.
            Be sure to give a unique key to each emulator,
            otherwise unexpected things will happen.
        **base_emulator_kwargs
            Arguments passed to :py:class:`~emantis._gp_emulation.BaseEmulator`.

        """
        # Get node values.
        self._data_nodes = data_nodes

        # Read emulation config.
        if config_emu is None:
            config_emu = {}
        self._config_emu = ConfigGPE1Dx1D(**config_emu)

        # Init. empty dict used to store emulator nodes.
        self._emulator_nodes: dict[float, GaussianProcessEmulator1D] = {}

        # Default logger name if not provided.
        if not base_emulator_kwargs["logger_name"]:
            base_emulator_kwargs["logger_name"] = "e-MANTIS"

        # Init. all the emulator nodes.
        for elt in data_nodes:
            # Modified base emulator options for the GaussianProcessEmulator1D node.
            base_emulator_kwargs_node = base_emulator_kwargs.copy()
            base_emulator_kwargs_node["logger_name"] = (
                f"{base_emulator_kwargs['logger_name']}:{self._config_emu.config_node.variable_name}_{elt}"
            )

            self._emulator_nodes[elt] = GaussianProcessEmulator1D(
                params,
                data[elt],
                data_bins[elt],
                data_std=data_std[elt] if data_std is not None else None,
                bspline_degree=(
                    bspline_degree[elt] if bspline_degree is not None else None
                ),
                config_emu=self._config_emu.config_gpe_1D,
                gp_std_factor=gp_std_factor[elt] if gp_std_factor is not None else None,
                use_persistent_storage=use_persistent_storage,
                persistent_storage_key=f"{persistent_storage_key}_{self._config_emu.config_node.variable_name}_{elt}",
                **base_emulator_kwargs_node,
            )

        # Init. base emulator.
        super().__init__(**base_emulator_kwargs)

    @BaseEmulator.random_seed.setter
    def random_seed(self, value: int | None) -> None:
        for elt in self._data_nodes:
            self._emulator_nodes[elt].random_seed = value
        BaseEmulator.random_seed.fset(self, value)
        self._random_generator = np.random.default_rng(value)

    @BaseEmulator.n_jobs.setter
    def n_jobs(self, value: int) -> None:
        for elt in self._data_nodes:
            self._emulator_nodes[elt].n_jobs = value
        BaseEmulator.n_jobs.fset(self, value)

    @BaseEmulator.verbose.setter
    def verbose(self, value: bool) -> None:
        for elt in self._data_nodes:
            self._emulator_nodes[elt].verbose = value
        BaseEmulator.verbose.fset(self, value)

    @property
    def _node_var_range(self) -> tuple[float, float]:
        node_var_min: float = min(self._data_nodes)
        node_var_max: float = max(self._data_nodes)

        return node_var_min, node_var_max

    def train_all(self, n_jobs: int | None = None) -> None:
        """Train all the emulator nodes.

        Any previous training will be overwritten,
        including in the local persistent storage.

        Parameters
        ----------
        n_jobs: int or None, default=None
            Maximum number of independent processes used to train each emulator node.
            A value of -1 uses all available cores.
            If ``None``, use the value passed when
            this emulator instance was initialized.
            Additional parallelism might be used (via Numpy, SciPy, OpenMP),
            even when `n_jobs=1`.
            See the scikit-learn `documentation <https://scikit-learn.org/stable/computing/parallelism.html#parallelism>`_
            for more details.

        """
        self._logger.info(
            f"All {self._config_emu.config_node.variable_name}"
            " emulator nodes will be trained."
        )

        # TODO: try to do this in parallel with joblib.
        # Complication: recover trained emulator from child process,
        # the train_node function needs to return it.
        for node in self._data_nodes:
            self._emulator_nodes[node].train(n_jobs=n_jobs)

        self._logger.info("All training completed!")

    def load_train_all(self, n_jobs: int | None = None) -> None:
        """Load all trained emulator nodes from the local persistent storage.

        If the loading fails for some nodes, or if persistent storage usage is disabled,
        trains from scratch the required nodes.

        Parameters
        ----------
        n_jobs: int or None, default=None
            Maximum number of independent processes used to train each emulator node.
            A value of -1 uses all available cores.
            If ``None``, use the value passed when
            this emulator instance was initialized.
            Additional parallelism might be used (via Numpy, SciPy, OpenMP),
            even when `n_jobs=1`.
            See the scikit-learn `documentation <https://scikit-learn.org/stable/computing/parallelism.html#parallelism>`_
            for more details.

        """
        self._logger.info(
            f"All {self._config_emu.config_node.variable_name}"
            " emulator nodes will be loaded/trained."
        )

        for node in self._data_nodes:
            self._emulator_nodes[node].load_train_emulator(n_jobs=n_jobs)

        self._logger.info("All loading/training completed!")

    def range(self, parameter: str, **kwargs) -> tuple[float, float]:
        """Give emulation range for a given parameter.

        Parameters
        ----------
        parameter : str
            The name of the parameter for which to return the emulation range.

        Returns
        -------
        min_value : float
            The minimum emulation range for the requested parameter.
        max_value : float
            The maximum emulation range for the requested parameter.

        Raises
        ------
        TypeError
            If optional input args are missing.
            For some parameters, certain extra input args need to be passed.
        ValueError
            If `parameter`is not a valid parameter name.

        """
        # If the variable is the data bin.
        if parameter == self._config_emu.config_gpe_1D.data.variable_name:
            # If the range is not node dependent, return the range of the first node.
            if self._config_emu.config_node.constant_data1D_range:
                return self._bin_range(self._data_nodes[0])

            # Else, the user needs to specify the node as an argument to this function.
            if self._config_emu.config_node.variable_name not in kwargs:
                raise TypeError(
                    f"To get the range for {parameter},"
                    " the additional keyword argument"
                    f" `{self._config_emu.config_node.variable_name}` is required."
                )
            return self._bin_range(kwargs[self._config_emu.config_node.variable_name])

        # If the variable is the emulator node.
        elif parameter == self._config_emu.config_node.variable_name:
            return self._node_var_range

        # If the params_range dict has been provided at the initialization.
        elif self.params_range is not None:
            # If the variable is an input parameter.
            if parameter in self.params_range:
                min_value = self.params_range[parameter]["min_value"]
                max_value = self.params_range[parameter]["max_value"]

                return min_value, max_value
            # Otherwise, raise an exception since the variable is unknown.
            else:
                raise ValueError(f"Unknown variable: {parameter}.")
        # Otherwise, raise an exception since the variable is unknown.
        # Note that the params have not been checked, since the params_range
        # has not been provided at the initialization.
        else:
            raise ValueError(
                f"Unknown variable: {parameter}.\n"
                "Note: the params_range dict was not provided"
                " at the initialization of this instance."
            )

    def _predict_observable(
        self,
        params: dict[str, float | list[float] | npt.NDArray],
        node_var: float | list[float] | npt.NDArray,
        bins: float | list[float] | npt.NDArray | None = None,
        return_std: bool = False,
        squeeze: bool = True,
        extrapolate_bins_low: bool = False,
        extrapolate_bins_high: bool = False,
    ) -> npt.NDArray:
        """Predict the observable of interest.

        Multiple sets of parameters can be passed at once
        by giving them in the form of arrays (or lists).
        This function will return a prediction
        for the observable of interest for each entry.
        Calling the function to give predictions for ``n_cosmo`` models at once
        is significantly faster than calling it ``n_cosmo`` times for a single model.

        Additionally, multiple node_var per model can be requested at once.
        If *node_var* has ``n_node_vars`` entries,
        then ``n_node_vars`` outputs will be given for each model.

        Parameters
        ----------
        params : dict
            A dictionary passing the input parameters.
        node_var : float or list or array of shape (n_node_var,)
            Node variable values.
        bins : float or list or array of shape (n_bins,) or None, default=None
            The bins of the main variable at which to output
            the prediction for the observable of interest.
            It can represent for instance the wavenumber
            in the case of the matter power spectrum
            or the halo mass in the case of the halo mass function.
            The same binning is used for all models and node_var values.
        return_std : bool, default=False
            If ``True``, also return the standard deviation of the predictions.
            Might slow down the computation.
        squeeze : bool, default=True
            If ``True``, remove axes of length one from `pred`.

        Returns
        -------
        pred : ndarray
            Predicted observable at the input bins, models and node_var values.
            The output is an array of shape (n_node_var, n_models, n_bins),
            where ``n_node_vars`` is the number of node_var values per model,
            ``n_models`` is the number of models, and ``n_bins`` the number of binsTrue.
        pred_std : ndarray (returned only of `return_std` is ``True``)
            The standard deviation of the predicted statistic at the input halo masses,
            cosmological models, and node_var values.
            Same shape as `pred`.

        """
        # Convert nodes to an array.
        node_var_array = _utils_inputs.format_input_to_1d_array(
            node_var, self._config_emu.config_node.variable_name
        )

        # Number of requested node_var values.
        n_node_vars: int = node_var_array.shape[0]

        # Check node range.
        _utils_inputs.check_emulation_range(
            node_var_array,
            *self._node_var_range,
            self._config_emu.config_node.variable_name,
        )

        if bins is not None:
            # Convert bins to an array (used just to check number of bins).
            bin_array = _utils_inputs.format_input_to_1d_array(
                bins, self._config_emu.config_gpe_1D.data.variable_name
            )
        else:
            bin_array = None

        # Format input params array, while checking for provided parameters and ranges.
        params_array = self._format_input_params_to_array(
            params,
        )

        # Number of samples to predict.
        n_models = params_array.shape[0]

        # Find the node_var nodes required to make predictions.
        node_var_nodes, node_var_neighbours = self._find_nodes(node_var_array)

        # Empty dict used to store node_var nodes predictions.
        pred_node_var_nodes = {}
        if return_std:
            std_node_var_nodes = {}

        # Precompute the predictions for each of the required node_var nodes.
        node_var_value: float
        for node_var_value in node_var_nodes:
            if return_std:
                (
                    pred_node_var_nodes[node_var_value],
                    std_node_var_nodes[node_var_value],
                ) = self._emulator_nodes[node_var_value]._predict_observable(
                    params_array,
                    bins=bin_array,
                    return_std=True,
                    extrapolate_bins_low=extrapolate_bins_low,
                    extrapolate_bins_high=extrapolate_bins_high,
                    check_params=False,
                    squeeze=False,
                )
            else:
                pred_node_var_nodes[node_var_value] = self._emulator_nodes[
                    node_var_value
                ]._predict_observable(
                    params_array,
                    bins=bin_array,
                    extrapolate_bins_low=extrapolate_bins_low,
                    extrapolate_bins_high=extrapolate_bins_high,
                    check_params=False,
                    squeeze=False,
                )

        # Number of output bins/values.
        n_bins = pred_node_var_nodes[node_var_nodes[0]].shape[1]

        # Initialise the prediction array.
        pred = np.empty((n_node_vars, n_models, n_bins))
        if return_std:
            std = np.empty((n_node_vars, n_models, n_bins))

        # Fill the prediction array with the predictions
        # for each requested node_var values.
        for i, node_var_value in enumerate(node_var_array):
            # Check if the requested node_var is part of the precomputed training nodes.
            if node_var_value in pred_node_var_nodes:
                pred[i] = pred_node_var_nodes[node_var_value]
                if return_std:
                    std[i] = std_node_var_nodes[node_var_value]
            else:
                # For node_var values outside the precomputed training nodes,
                # interpolate between the two closest precomputed training nodes.
                node_low, node_up = (
                    node_var_neighbours[node_var_value][0],
                    node_var_neighbours[node_var_value][1],
                )

                # Make the interpolation (all models and bins at once).
                pred[i] = self._interp_pred_between_nodes(
                    node_var_value,
                    node_low,
                    node_up,
                    pred_node_var_nodes[node_low],
                    pred_node_var_nodes[node_up],
                )

                # Propagate std through node interpolation.
                if return_std:
                    std[i] = self._propagate_std_between_nodes(
                        node_var_value,
                        node_low,
                        node_up,
                        pred_node_var_nodes[node_low],
                        pred_node_var_nodes[node_up],
                        std_node_var_nodes[node_low],
                        std_node_var_nodes[node_up],
                    )

        # Squeeze output(s) if necessary.
        if squeeze:
            pred = np.squeeze(pred)
            if return_std:
                std = np.squeeze(std)

        if return_std:
            return pred, std
        return pred

    def _propagate_std_between_nodes(
        self,
        node_var: float,
        node_low: float,
        node_up: float,
        pred_low: npt.NDArray,
        pred_up: npt.NDArray,
        std_low: npt.NDArray,
        std_up: npt.NDArray,
    ) -> npt.NDArray:
        # TODO: apply same changes as to _propagate_gp_std
        # from GaussianProcessEmulator1D.
        # i.e.: use same random number for all models + eventually cache them.

        # Generate random numbers with shape (n_iter, n_models, n_bins).
        eps_low = self._random_generator.normal(
            loc=0,
            scale=std_low,
            size=(
                self._config_emu.config_node.niter,
                std_low.shape[0],
                std_low.shape[1],
            ),
        )
        eps_up = self._random_generator.normal(
            loc=0,
            scale=std_up,
            size=(
                self._config_emu.config_node.niter,
                std_up.shape[0],
                std_up.shape[1],
            ),
        )

        # Broadcast predictions from (n_models, n_bins) to (n_iter, n_models, n_bins).
        pred_low = np.broadcast_to(pred_low, eps_low.shape)
        pred_up = np.broadcast_to(pred_up, eps_up.shape)

        # Interpolate perturbed predictions between nodes.
        pred_random = self._interp_pred_between_nodes(
            node_var, node_low, node_up, pred_low + eps_low, pred_up + eps_up
        )

        # Compute standard deviation of the perturbed predictions.
        std = np.std(pred_random, axis=0, ddof=1)

        return std

    def _interp_pred_between_nodes(
        self,
        node_var: float,
        node_low: float,
        node_up: float,
        pred_low: float | npt.NDArray,
        pred_up: float | npt.NDArray,
    ) -> float | npt.NDArray:
        # Get node interpolation config.
        interp_node_x_type = self._config_emu.config_node.x_interp_type
        interp_node_y_type = self._config_emu.config_node.y_interp_type

        # Apply transformation to node_var values.
        node_var_tr = _utils.simple_transform(node_var, interp_node_x_type)
        node_low_tr = _utils.simple_transform(node_low, interp_node_x_type)
        node_up_tr = _utils.simple_transform(node_up, interp_node_x_type)

        # Apply transformation to predictions.
        pred_low_tr = _utils.simple_transform(pred_low, interp_node_y_type)
        pred_up_tr = _utils.simple_transform(pred_up, interp_node_y_type)

        # Interpolate.
        pred_interp = _utils.lin_interp(
            node_var_tr, node_low_tr, node_up_tr, pred_low_tr, pred_up_tr
        )

        # Inverse transform prediction.
        pred_interp = _utils.inverse_simple_transform(pred_interp, interp_node_y_type)

        return pred_interp

    def _bin_range(self, node_var) -> tuple[float, float]:
        # Check node range.
        node_var_min, node_var_max = self._node_var_range
        _utils_inputs.check_emulation_range(
            node_var,
            node_var_min,
            node_var_max,
            self._config_emu.config_node.variable_name,
        )

        # If node_var is one of the training nodes,
        # determine the bin range from the emulator node.
        if node_var in self._data_nodes:
            return self._emulator_nodes[node_var]._bin_range()

        # Otherwise, determine the intersection range between the bin range
        # of the two enclosing emulator nodes.
        else:
            # Find neighbouring nodes.
            node_low, node_up = self._find_neighbour_nodes(node_var)

            # Range for each neighbouring node.
            bin_min_low, bin_max_low = self._emulator_nodes[node_low]._bin_range()
            bin_min_up, bin_max_up = self._emulator_nodes[node_up]._bin_range()

            # Range of the intersection between both neighbouring nodes.
            bin_min: float = max(bin_min_low, bin_min_up)
            bin_max: float = min(bin_max_low, bin_max_up)

            return bin_min, bin_max

    def _find_nodes(self, node_var_array: npt.NDArray) -> tuple[npt.NDArray, dict]:
        """Find the nodes required to make predictions.

        In addition to the required nodes,
        this function also returns the neighbouring nodes
        of each of the requested non-node node_var values.

        Parameters
        ----------
        node_var_array : 1D array
            The node_var values for which predictions have been requested.

        Returns
        -------
        node_var_nodes : 1D array
            The node_var nodes necessary to make the requested predictions.
            *node_var_nodes* is a sorted 1D array with unique elements.
        node_neighbours : dict
            The neighbouring nodes for each of the requested non-node node_var values.

        """
        # Initialise the output data structures.
        node_var_nodes = []
        node_neighbours = {}

        # Loop over all the requested node_var values.
        for node_var in node_var_array:
            # If the node_var is an emulator node add it to the list of required nodes.
            if node_var in self._data_nodes:
                node_var_nodes.append(node_var)
            # Otherwise find the two closest nodes and add them to the list
            # of required nodes and to the neighbours dict.
            else:
                node_low, node_up = self._find_neighbour_nodes(node_var)
                node_var_nodes.extend([node_low, node_up])
                node_neighbours[node_var] = [node_low, node_up]

        # Sort and remove duplicate entries in the required nodes list.
        node_var_nodes_unique = np.unique(node_var_nodes)

        return node_var_nodes_unique, node_neighbours

    def _find_neighbour_nodes(self, node_var: float) -> tuple[float, float]:
        """Find neighbouring node_var nodes.

        This function finds the two closest node_var nodes in order
        to linearly interpolate the predicted observable between them.

        If the requested node_var is below the smallest node_var
        node, this function returns the two closest nodes, so that they can
        be used for extrapolation.

        Parameters
        ----------
        node_var : float
            The node_var value for we which we want to find the neighbours.

        Returns
        -------
        node_low : float
            The lower neighbouring node.
        node_up : float
            The upper neighbouring node.

        """
        # If node_var is below the smallest node, return the two smallest nodes
        # so they can be used for extrapolation.
        if node_var < self._node_var_range[0]:
            return self._data_nodes[0], self._data_nodes[1]

        # Otherwise, search for the neighbouring nodes.
        cont = True
        i = 0
        while cont:
            if self._data_nodes[i] > node_var:
                node_up, node_low = (
                    self._data_nodes[i - 1],
                    self._data_nodes[i],
                )
                cont = False
            i += 1
        return node_low, node_up
