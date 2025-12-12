"""Module able to emulate matter power spectrum related quantities.

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

import os
import warnings
from importlib.resources import as_file, files

import h5py
import numpy as np
from sklearn import decomposition, preprocessing
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern
from sklearn.multioutput import MultiOutputRegressor

DATADIR = "data/fofr_matter_power_boost"
GPR_KERNEL = Matern(length_scale=[1.0, 1.0, 1.0], nu=2.5)
NPCA = 5


# TODO: raise deprecation warning when this class is initialized.
class FofrBoost:
    """An emulator for the nonlinear matter power spectrum boost in f(R) gravity.

    Attributes
    ----------
    n_jobs: int or None, default=None
        Maximum number of independent processes used to train the emulator.
        Predictions always use ``n_jobs=1``, since they are already fast
        and the parallelism overhead is not worth it.
        Additional parallelism might be used (via Numpy, SciPy, OpenMP),
        even when ``n_jobs=1``.
        See the scikit-learn `documentation <https://scikit-learn.org/stable/computing/parallelism.html#parallelism>`_
        for more details.
    verbose: bool, default=True
        Whether to activate or not verbose output.

    """

    def __init__(
        self, n_jobs=None, verbose=True, extrapolate_aexp=False, extrapolate_low_k=False
    ):
        """Initialise the emulator."""
        self._emu_aexp_node = {
            0.3333: {},
            0.3650: {},
            0.4000: {},
            0.4167: {},
            0.4444: {},
            0.4762: {},
            0.5000: {},
            0.5263: {},
            0.5556: {},
            0.5882: {},
            0.6250: {},
            0.6667: {},
            0.7042: {},
            0.7692: {},
            0.8000: {},
            0.8696: {},
            0.9091: {},
            0.9524: {},
            1: {},
        }
        """dict: The pca, data scaler and gpr instances for each scale factor node.

        Empty dict = not trained yet.
        """

        # Extrapolation settings.
        self.extrapolate_aexp = extrapolate_aexp
        self.extrapolate_low_k = extrapolate_low_k

        #: dict: The emulation range for each cosmological parameter and scale factor.
        self._emulation_range = {
            "omega_m": [0.2365, 0.3941],
            "sigma8_lcdm": [0.6083, 1.0140],
            "logfR0": [4, 7],
            "aexp": [0.3333, 1],
        }

        # Import data resources.
        self._resources = files("emantis")

        # Read centres and edges of the wavenumber bins.
        with as_file(self._resources / DATADIR / "kbins.h5") as h5:  # noqa: SIM117
            with h5py.File(h5) as f:
                self._kbins = f["kbins_centres"][:]
                self._kbins_edges = f["kbins_edges"][:]

        # Read cosmological parameters of the training nodes.
        with as_file(self._resources / DATADIR / "cosmo_params.txt") as txt:
            x_train = np.loadtxt(txt)
            x_train[:, 2] = -np.log10(x_train[:, 2])

        # Scale the training cosmological parameters to a zero mean
        # unit variance distribution and store the scaler
        # and obtained distribution for later usage.
        #: sklearn.preprocessing.StandardScaler: Scaler to rescale cosmo. parameters.
        self._scaler_x_train = preprocessing.StandardScaler().fit(x_train)
        #: array of shape (nmodels, 3): Rescaled training cosmological parameters.
        self._x_train_scaled = self._scaler_x_train.transform(x_train)

        self.verbose = verbose

        self.n_jobs = n_jobs

    def predict_boost(self, omega_m, sigma8_lcdm, logfR0, aexp, k=None):
        """Predict the nonlinear matter power spectrum boost in f(R) gravity.

        Multiple cosmological models can be passed at once by
        giving `omega_m`, `sigma8_lcdm` and `logfR0` in the form of arrays.
        This function will return a prediction for the matter power
        spectrum boost for each entry.
        Calling the function to predict the boost for N models at once
        is significantly faster than calling it N times for a single model.

        .. warning::

           The three parameters `omega_m`, `sigma8_lcdm` and `logfR0`
           must always have the same shape.

        Additionally, multiple scale factors per cosmological model
        can be requested at once.
        If *aexp* has ``naexp`` entries, then ``naexp`` outputs will be given
        for each cosmological model.

        The emulator training will be performed as necessary each time a new
        scale factor node is requested (or needed for scale factor interpolation)
        for the first time.
        Alternatively, :py:func:`~emantis.powerspectrum_matter.FofrBoost.train_all`
        can be called once in order to
        train all scale factor nodes before requesting any predictions.
        The training is fast and should not take more than
        a few seconds per scale factor node
        on a standard laptop processor.

        .. versionchanged:: 1.0.4

            It is now possible to request the boost at specific wavenumbers.

        .. versionchanged:: 1.0.2

           Multiple scale factor support.

        Parameters
        ----------
        omega_m : float or array-like
            Present-day total matter density parameter Omega_m.
        sigma8_lcdm : float or array-like
            Present-day root-mean-square linear matter fluctuation averaged
            over a sphere of radius 8 Mpc/h,
            assuming a LCDM linear evolution.
        logfR0 : float or array-like
            Modified gravity parameter -log10(|fR0|),
            where fR0 is the present-day background value of the scalaron field.
        aexp : float or array-like
            Cosmological scale factor.
        k: float or array-like, default=None
            The wavenumbers at which to output the boost.
            If None, predictions are given at the wavenumber bins
            used to train the emulator.
            Otherwise, the boost is linearly interpolated
            in log10(k) at the requested wavenumbers.
            The same wavenumbers are used for all models and scale factors.

        Returns
        -------
        boost_pred : ndarray of shape (nbink) or (naexp, nmodels, nbink)
            Predicted matter power spectrum boost.
            If a single model has been requested,
            the output is a 1D array of shape (nbink,),
            where ``nbink`` is the number of wavenumber bins.
            If more than one cosmological model,
            or more than one scale factor, are requested,
            then the output is a 3D array of shape (naexp, nmodels, nbink),
            where ``naexp`` is the number of scale factors per model and
            ``nmodels`` is the number of cosmological models.

        """
        # Check that the requested scale factors, cosmological parameters
        # and wavenumbers are within the allowed emulation space.
        self._check_params(omega_m, sigma8_lcdm, logfR0, aexp, k)

        # Properly format the input parameters before feeding
        # them to the emulator.
        cosmo_params = self._read_cosmo_params(omega_m, sigma8_lcdm, logfR0)

        # Convert aexp to array.
        aexp = np.ravel(np.array([aexp]))

        # Number of requested scale factors.
        naexp = aexp.shape[0]

        # Number of samples to predict.
        nmodels = cosmo_params.shape[0]

        # Find the scale factor nodes required to make predictions.
        aexp_nodes, aexp_neighbours = self._find_aexp_nodes(aexp)

        # Empty dict used to store the scale factor nodes boost predictions.
        boost_aexp_nodes = {}

        # Precompute the boosts for each of the required scale factor nodes.
        for a in aexp_nodes:
            boost_aexp_nodes[a] = self._predict_boost_aexp_node(a, cosmo_params)

        # Initialise the prediction array.
        boost_pred = np.empty((naexp, nmodels, self.kbins.shape[0]))

        # Fill the prediction array with the boost for each requested scale factors.
        for i, a in enumerate(aexp):
            # Check if the requested scale factor
            # is part of the precomputed training nodes.
            if a in boost_aexp_nodes:
                boost_pred[i] = boost_aexp_nodes[a]
            else:
                # For scale factors outside the precomputed training nodes,
                # linearly interpolate between the two closest
                # precomputed scale factor nodes.
                aexp_low, aexp_up = aexp_neighbours[a][0], aexp_neighbours[a][1]
                boost_pred[i] = self._lin_interp(
                    a,
                    aexp_low,
                    aexp_up,
                    boost_aexp_nodes[aexp_low],
                    boost_aexp_nodes[aexp_up],
                )

        # If specific wavenumbers have been requested,
        # interpolate the binned boost linearly in log10(k).
        if k is not None:
            boost_pred = self._interp_boost_k(k, boost_pred)

        # Force boost >= 1.
        np.clip(
            boost_pred,
            a_min=1,
            a_max=None,
            out=boost_pred,
        )

        # If a single cosmological model and a single scale factor
        # have been requested then return a 1D array.
        if nmodels * naexp == 1:
            return np.ravel(boost_pred)
        else:
            return boost_pred

    def train_all(self):
        """Trains the emulator at all scale factor nodes.

        The training is fast.
        It should not take more than a few seconds per scale factor node
        on a standard laptop processor.

        Once this function has been called, no further training of the
        emulator is needed.
        """
        if self.verbose:
            print("All scale factor nodes will be trained.")
        for aexp in self.aexp_nodes:
            self._train_emu_aexp_node(aexp)
        if self.verbose:
            print(
                "Training completed!"
                " No more training will be required for this emulator instance."
            )

    @property
    def extrapolate_aexp(self):
        """bool, default=False: Activate scale factor extrapolation.

        If True, the emulator will linearly extrapolate
        the power spectrum boost for scale factors
        below the emulation range.
        The extrapolation is constrained to ensure a boost
        larger or equal to unity at all scales.
        """
        return self._extrapolate_aexp

    @extrapolate_aexp.setter
    def extrapolate_aexp(self, boolean):
        # If the user activates scale factor extrapolation, print a warning.
        if boolean:
            warnings.warn(
                "You have activated scale factor extrapolation.\n"
                "It comes with no guarantees in terms of accuracy.\n"
                "It should only be used for scale factors"
                " near the emulation boundary.\n"
                "It is better to use the new interface"
                " matter_power_spectrum.NonLinearBoostMGEmulator, which uses"
                " simulation data at lower scale factors.",
                stacklevel=2,
            )
        self._extrapolate_aexp = boolean

    @property
    def extrapolate_low_k(self):
        """bool, default=False: Activate wavenumber extrapolation.

        If True, the boost is extrapolated linearly in log10(k)
        for wavenumbers below the emulation range.
        The extrapolation is constrained to ensure a boost
        larger or equal to unity at all scales.
        """
        return self._extrapolate_low_k

    @extrapolate_low_k.setter
    def extrapolate_low_k(self, boolean):
        self._extrapolate_low_k = boolean

    @property
    def emulation_range(self):
        """dict: The emulation range in the form of a dictionary.

        Available fields are: ``omega_m``, ``sigma8_lcdm``, ``logfR0`` and ``aexp``.
        """
        return self._emulation_range

    @property
    def kbins(self):
        """Ndarray of shape (90,): Default wavenumber bin centres.

        A 1D array containing the centres
        of the wavenumber bins of the training power spectrum boost
        in units of comoving h/Mpc.
        """
        return self._kbins

    @property
    def kbins_edges(self):
        """Ndarray of shape (91,): Default wavenumber bin edges.

        A 1D array containing the edges
        of the wavenumber bins of the training power spectrum boost
        in units of comoving h/Mpc.
        """
        return self._kbins_edges

    @property
    def aexp_nodes(self):
        """list: The training scale factor nodes of the emulator."""
        return sorted(self._emu_aexp_node.keys())

    def _interp_boost_k(self, k, boost_pred):
        """Interpolate the boost predictions linearly in log10(k).

        This function also extrapolates the boost below the emulation
        range if extrapolate_low_k=True.
        In such case, the boost is constrained to be larger or equal
        to unity at all scales.

        Parameters
        ----------
        k : float or array-like
            The wavenumbers at which to interpolate/extrapolate the predicted boost.
        boost_pred : ndarray of shape (naexp, nmodels, nbink_pred)
            The predicted boost to interpolate/extrapolate.

        Returns
        -------
        boost_pred_interp : ndarray of shape (naexp, nmodels, nbink_interp)
            The interpolated/extrapolated boosts at the requested wavenumbers.

        """
        # Convert k to array.
        k = np.ravel(np.array(k))
        nbinsk = k.shape[0]

        # Initialise empty array for the interpolated predictions.
        boost_pred_interp = np.zeros((boost_pred.shape[0], boost_pred.shape[1], nbinsk))

        # Wavenumbers within interpolation range.
        index_interp = (k >= self.kbins[0]) & (k <= self.kbins[-1])
        # This check is not necessary, but it can save some time.
        if self.extrapolate_low_k:
            # Wavenumbers below the interpolation range.
            index_extrap_low = k < self.kbins[0]

        # Interpolate/extrapolate the boost at each scale factor and model.
        for i in range(boost_pred.shape[0]):
            for j in range(boost_pred.shape[1]):
                # Interpolate (linear in log10(k)).
                boost_pred_interp[i, j][index_interp] = np.interp(
                    np.log10(k[index_interp]),
                    np.log10(self.kbins),
                    boost_pred[i, j],
                )
                # Again, this check is not necessary, but it can save some time.
                if self.extrapolate_low_k:
                    # Extrapolate below (linear in log10(k)).
                    boost_pred_interp[i, j][index_extrap_low] = self._lin_interp(
                        np.log10(k[index_extrap_low]),
                        np.log10(self.kbins[0]),
                        np.log10(self.kbins[1]),
                        boost_pred[i, j][0],
                        boost_pred[i, j][1],
                    )

        return boost_pred_interp

    # TODO: maybe move this to a separate "utils" module.
    def _lin_interp(self, x0, x1, x2, y1, y2):
        """Perform a linear interpolation.

        Linearly interpolates at location *x0* between two nodes *x1* and *x2*, with
        values *y1* and *y2* respectively.

        It assumes that *x1* < *x0* < *x2*.

        Parameters
        ----------
        x0 : float
            The location at which the interpolation is returned.
        x1 : float
            The lower interpolation node.
        x2 : float
            The upper interpolation node.
        y1 : float
            The value at *x1*.
        y2 : float
            The value at *x2*.

        Returns
        -------
        y0 : float
            The interpolated value at *x0*.

        """
        y0 = y1 + (x0 - x1) * (y2 - y1) / (x2 - x1)

        return y0

    def _find_aexp_nodes(self, aexp):
        """Find the scale factors nodes required to make predictions.

        In addition to the required scale factor nodes,
        this function also returns the neighbouring nodes
        of each the requested non-node scale factors.

        Parameters
        ----------
        aexp : float or array-like
            The scale factors for which predictions have been requested.

        Returns
        -------
        aexp_nodes : float or array-like
            The scale factor nodes necessary to make the requested predictions.
            *aexp_nodes* is a sorted 1D array with unique elements.
        aexp_neighbours : dict
            The neighbouring nodes for each of the requested non-node scale factors.

        """
        # Initialise the output data structures.
        aexp_nodes = []
        aexp_neighbours = {}

        # Loop over all the requested scale factors.
        for a in aexp:
            # If the scale factor is an emulator node
            # add it to the list of required nodes.
            if a in self.aexp_nodes:
                aexp_nodes.append(a)
            # Otherwise find the two closest nodes
            # and add them to the list of required nodes
            # and to the neighbours dict.
            else:
                aexp_low, aexp_up = self._find_neighbour_aexp_nodes(a)
                aexp_nodes.extend([aexp_low, aexp_up])
                aexp_neighbours[a] = [aexp_low, aexp_up]

        # Sort and remove duplicate entries in the required nodes list.
        aexp_nodes = np.unique(aexp_nodes)

        return aexp_nodes, aexp_neighbours

    def _check_params(self, omega_m, sigma8_lcdm, logfR0, aexp, k):
        """Check the validity of the input parameters.

        Verify that the requested cosmological parameters, scale factor
        and wavenumbers are within the allowed emulation range.
        Raises an exception if at least one of the provided parameters
        is not valid.

        Parameters
        ----------
        omega_m : float or array-like
            Present-day total matter density parameter Omega_m.
        sigma8_lcdm : float or array-like
            Present-day root-mean-square linear matter fluctuation averaged
            over a sphere of radius 8 Mpc/h,
            assuming a LCDM linear evolution.
        logfR0 : float or array-like
            Modified gravity parameter -log10(|fR0|),
            where fR0 is the present-day background value of the scalaron field.
        aexp : float
            Cosmological scale factor.
        k : float or array-like
            Wavenumber in units of h/Mpc.

        Raises
        ------
        ValueError
            If input cosmological parameters, wavenumber, or scale factor
            are outside the emulation range.

        """
        # TODO: Reject only the particular models outside the emulation range
        # and give predictions for those that are valid.
        # Right now all models are rejected even if
        # a single one of the requested models is unvalid.

        # Check wavenumber if provided and extrapolation is deactivated.
        if k is not None:
            k_min, k_max = np.min(k), np.max(k)
            if (k_min < self.kbins[0]) and not self.extrapolate_low_k:
                raise ValueError(
                    f"Requested wavenumber, k={k_min:.4f},"
                    " is outside the emulation range"
                    f" ({self.kbins[0]:.4f} <= k"
                    f" <= {self.kbins[-1]:.4f}).\n"
                    "It is possible to extrapolate linearly in log10(k)"
                    " to smaller wavenumbers by setting"
                    " extrapolate_low_k=True."
                )

            if k_max > self.kbins[-1]:
                raise ValueError(
                    f"Requested wavenumber, k={k_max:.4f},"
                    " is outside the emulation range"
                    f" ({self.kbins[0]:.4f} <= k"
                    f" <= {self.kbins[-1]:.4f})."
                )

        # Check scale factor.
        aexp_min, aexp_max = np.min(aexp), np.max(aexp)
        if (aexp_min < self.emulation_range["aexp"][0]) and not self.extrapolate_aexp:
            raise ValueError(
                f"Requested scale factor, aexp={aexp_min:.4f},"
                " is outside the emulation range"
                f" ({self.emulation_range['aexp'][0]:.4f} <= aexp"
                f" <= {self.emulation_range['aexp'][1]:.4f}).\n"
                "To get predictions at smaller scale factors"
                " use the updated interface"
                " matter_power_spectrum.NonLinearBoostMGEmulator."
            )

        if aexp_max > self.emulation_range["aexp"][1]:
            raise ValueError(
                f"Requested scale factor, aexp={aexp_max:.4f},"
                " is outside the emulation range"
                f" ({self.emulation_range['aexp'][0]:.4f} <= aexp"
                f" <= {self.emulation_range['aexp'][1]:.4f})."
            )

        # Check omega_m.
        omega_m_min, omega_m_max = np.min(omega_m), np.max(omega_m)
        if omega_m_min < self.emulation_range["omega_m"][0]:
            raise ValueError(
                f"Requested omega_m, omega_m={omega_m_min:.4f},"
                " is outside the emulation range"
                f" ({self.emulation_range['omega_m'][0]:.4f} <= omega_m"
                f" <= {self.emulation_range['omega_m'][1]:.4f})."
            )

        if omega_m_max > self.emulation_range["omega_m"][1]:
            raise ValueError(
                f"Requested omega_m, omega_m={omega_m_max:.4f},"
                " is outside the emulation range"
                f" ({self.emulation_range['omega_m'][0]:.4f} <= omega_m"
                f" <= {self.emulation_range['omega_m'][1]:.4f})."
            )

        # Check sigma8_lcdm.
        sigma8_lcdm_min, sigma8_lcdm_max = np.min(sigma8_lcdm), np.max(sigma8_lcdm)
        if sigma8_lcdm_min < self.emulation_range["sigma8_lcdm"][0]:
            raise ValueError(
                f"Requested sigma8_lcdm, sigma8_lcdm={sigma8_lcdm_min:.4f},"
                " is outside the emulation range"
                f" ({self.emulation_range['sigma8_lcdm'][0]:.4f} <= sigma8_lcdm"
                f" <= {self.emulation_range['sigma8_lcdm'][1]:.4f})."
            )

        if sigma8_lcdm_max > self.emulation_range["sigma8_lcdm"][1]:
            raise ValueError(
                f"Requested sigma8_lcdm, sigma8_lcdm={sigma8_lcdm_max:.4f},"
                " is outside the emulation range"
                f" ({self.emulation_range['sigma8_lcdm'][0]:.4f} <= sigma8_lcdm"
                f" <= {self.emulation_range['sigma8_lcdm'][1]:.4f})."
            )

        # Check logfR0.
        logfR0_min, logfR0_max = np.min(logfR0), np.max(logfR0)
        if logfR0_min < self.emulation_range["logfR0"][0]:
            raise ValueError(
                f"Requested logfR0, logfR0={logfR0_min:.4f},"
                " is outside the emulation range"
                f" ({self.emulation_range['logfR0'][0]:.4f} <= logfR0"
                f" <= {self.emulation_range['logfR0'][1]:.4f})."
            )

        if logfR0_max > self.emulation_range["logfR0"][1]:
            raise ValueError(
                f"Requested logfR0, logfR0={logfR0_max:.4f},"
                " is outside the emulation range"
                f" ({self.emulation_range['logfR0'][0]:.4f} <= logfR0"
                f" <= {self.emulation_range['logfR0'][1]:.4f})."
            )

    # TODO: allow for different shapes in the parameters input.
    # eg.: 1 float and 2 arrays of shame shape.
    def _read_cosmo_params(self, omega_m, sigma8_lcdm, logfR0):
        """Read the input cosmological parameters and transform them.

        Parameters
        ----------
        omega_m : float or array-like
            Present-day total matter density parameter Omega_m.
        sigma8_lcdm : float or array-like
            Present-day root-mean-square linear matter fluctuation averaged
            over a sphere of radius 8 Mpc/h,
            assuming a LCDM linear evolution.
        logfR0 : float or array-like
            Modified gravity parameter -log10(|fR0|),
            where fR0 is the present-day background value of the scalaron field.

        Returns
        -------
        cosmo_params : ndarray
            Array containing the rescaled input cosmological parameters
            of shape (3,) if a single sample is given
            or (nmodels, 3) if ``nmodels`` are given.

        """
        cosmo_params = np.array([omega_m, sigma8_lcdm, logfR0])

        # Check if a single or multiple samples are requested
        # and rescale the cosmological parameters accordingly.
        if cosmo_params.ndim == 1:
            cosmo_params = self._scaler_x_train.transform(cosmo_params.reshape(1, -1))
        else:
            cosmo_params = self._scaler_x_train.transform(cosmo_params.T)

        return cosmo_params

    def _find_neighbour_aexp_nodes(self, aexp):
        """Find neighbouring scale factor nodes.

        This function finds the two closest scale factor nodes in order
        to linearly interpolate the predicted boost between them.

        If the requested scale factor is below the smallest scale factor
        node, this function returns the two closest nodes, so that they can
        be used for extrapolation.

        Parameters
        ----------
        aexp : float
            The scale factor at which the user is requesting a prediction.

        Returns
        -------
        aexp_low : float
            The lower neighbouring scale factor node.
        aexp_up : float
            The upper neighbouring scale factor node.

        """
        # If aexp is below the smallest node, return the two smallest nodes
        # so they can be used for extrapolation.
        if aexp < self.aexp_nodes[0]:
            return self.aexp_nodes[0], self.aexp_nodes[1]

        # Otherwise, search for the neighbouring nodes.
        cont = True
        i = 0
        while cont:
            if self.aexp_nodes[i] > aexp:
                aexp_up, aexp_low = self.aexp_nodes[i - 1], self.aexp_nodes[i]
                cont = False
            i += 1
        return aexp_low, aexp_up

    def _predict_boost_aexp_node(self, aexp, cosmo_params):
        """Predict the boost at a training scale factor node.

        Parameters
        ----------
        aexp : float
            The scale factor node at which a prediction is required.
        cosmo_params : ndarray
            Array containing the requested cosmological parameters
            of shape (3,) if a single sample is requested
            or (nmodels, 3) if ``nmodels`` are requested.

        Returns
        -------
        boost_pred : ndarray
            An array of shape (90) or (nmodels, 90) containing
            the predicted boost at the requested scale factor for each
            input cosmological model.

        """
        # Check if the emulator has already been trained
        # for this scale factor node and if not train it.
        if not self._emu_aexp_node[aexp]:
            self._train_emu_aexp_node(aexp)

        # Predict the power spectrum boost using the trained GPR instance.

        # Predict the PCA coefficients
        boost_pred_reduced = self._emu_aexp_node[aexp]["GPR"].predict(cosmo_params)

        # Reconstruct the boost from the predicted PCA coefficients
        boost_pred_scaled = self._emu_aexp_node[aexp]["PCA"].inverse_transform(
            boost_pred_reduced
        )
        boost_pred = self._emu_aexp_node[aexp]["scaler_y"].inverse_transform(
            boost_pred_scaled
        )

        return boost_pred

    def _train_emu_aexp_node(self, aexp):
        """Train the emulator at a scale factor node.

        This function reads the training data at a given scale factor node.
        It then fits the standard scaler and uses it to scale the training data.
        It performs the PCA decomposition on the scaled training data.
        Finally, it initialises and trains a GPR instance per PCA coefficient.

        Parameters
        ----------
        aexp : float
            The scale factor node at which the emulator needs to be trained.

        """
        # Ignore warnings during training.
        warnings.simplefilter("ignore")
        # # Also for subprocesses.
        os.environ["PYTHONWARNINGS"] = "ignore"

        if self.verbose:
            print(f"Training the emulator at aexp={aexp:.4f}...", flush=True, end=" ")

        # Read the training power spectrum boosts.
        with as_file(self._resources / DATADIR / "power_boosts_train.h5") as h5:  # noqa: SIM117
            with h5py.File(h5) as f:
                y_train = f[f"power_boosts_aexp_{aexp:.4f}"][:]

        # Scale the training data to a unit variance zero mean distribution
        # and store the scaler for later usage.
        self._emu_aexp_node[aexp]["scaler_y"] = preprocessing.StandardScaler().fit(
            y_train
        )
        y_train_scaled = self._emu_aexp_node[aexp]["scaler_y"].transform(y_train)

        # Initialise the PCA instance and store it for later usage.
        self._emu_aexp_node[aexp]["PCA"] = decomposition.PCA(
            n_components=NPCA, svd_solver="full"
        )

        # Perform the PCA decomposition.
        self._emu_aexp_node[aexp]["PCA"].fit(y_train_scaled)
        y_train_reduced = self._emu_aexp_node[aexp]["PCA"].transform(y_train_scaled)

        # Initialise the GPR instance.
        self._emu_aexp_node[aexp]["GPR"] = MultiOutputRegressor(
            GaussianProcessRegressor(
                kernel=GPR_KERNEL, n_restarts_optimizer=0, normalize_y=True
            ),
            n_jobs=self.n_jobs,
        )

        # Train the GPR instance.
        self._emu_aexp_node[aexp]["GPR"].fit(self._x_train_scaled, y_train_reduced)

        # Set n_jobs=1.
        self._emu_aexp_node[aexp]["GPR"].n_jobs = 1

        # Turn warnings back on.
        warnings.simplefilter("default")
        os.environ["PYTHONWARNINGS"] = "default"

        if self.verbose:
            print("done.")
