"""A module implementing tests for the matter power spectrum emulators."""

import os

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["BLIS_NUM_THREADS"] = "1"

import joblib
import numpy as np
import pytest
from scipy.stats import qmc

from emantis import FofrBoost
from emantis.exceptions import EmulationRangeError
from emantis.matter_power_spectrum import (
    _NL_MG_BOOST_MODELS,
    _SIGMA8_MODELS,
    NonLinearMGBoostEmulator,
    Sigma8Emulator,
)

n_jobs_max = 6
n_jobs = min(joblib.cpu_count(), n_jobs_max)

# TODO: implement tests for NonLinearBoostEmulator.
# TODO: implement tests for the use of As as input parameter.


@pytest.mark.parametrize("model", _SIGMA8_MODELS)
class TestSigma8Emulator:
    """A class implementing tests for the sigma8 emulators."""

    def test_train(self, model):
        """Test the emulator training.

        It is better to run this test first, so that subsequent tests
        benefit from the trained emulators.
        """
        # Init. emulator.
        emu = Sigma8Emulator(model=model)

        # Train emulator.
        emu.train()

        # Check that instance has a trained emulator.
        assert bool(emu._gp_regressor_list)
        # Check consistency in the number of GP outputs.
        assert emu._gp_n_outputs == len(emu._gp_regressor_list)

    def test_predict(self, model):
        """Test emulator predictions.

        Compare emulator predictions to training data.
        """
        # Init. emulator.
        emu = Sigma8Emulator(model=model)

        # Check that params range dict is present.
        assert emu.params_range is not None

        # Load / train emulator.
        emu.load_train_emulator()

        # Get cosmological parameters of training models.
        cosmo_params = emu._params

        # Format into input dict. for the emulator.
        cosmo_params_dict = {
            param: cosmo_params[:, i] for i, param in enumerate(emu.params_range.keys())
        }

        # Get training data.
        data = emu._data

        # Get emulator predictions.
        pred = emu.predict_sigma8(cosmo_params_dict)

        # Check pred array shape.
        assert pred.shape == (data.shape[0],)

        # Check that mean absolute relative difference
        # between emulator and training data is smaller than 0.01%
        abs_rel_diff = np.abs((pred - data[:, 0]) / data[:, 0])
        mean_abs_rel_diff = np.mean(abs_rel_diff)

        assert mean_abs_rel_diff < 1e-3


@pytest.mark.parametrize("model", _NL_MG_BOOST_MODELS)
class TestNonLinearMGBoostEmulator:
    """A class implementing tests for the nonlinear MG boost emulators."""

    def test_train(self, model):
        """Test the emulator training.

        It is better to run this test first, so that subsequent tests
        benefit from the trained emulators.
        """
        # Init. emulator.
        emu = NonLinearMGBoostEmulator(model=model, n_jobs=n_jobs)

        # Check that this dict. is not empty.
        assert bool(emu._emulator_nodes)

        # Train emulator at all scale factor nodes.
        emu.train_all()

        # Loop over scale factor nodes.
        for aexp in emu.aexp_nodes:
            # Check that each aexp node has a trained emulator.
            assert bool(emu._emulator_nodes[aexp]._gp_regressor_list)
            # Check consistency in the number of GP outputs for each aexp node.
            assert emu._emulator_nodes[aexp]._gp_n_outputs == len(
                emu._emulator_nodes[aexp]._gp_regressor_list
            )

    def test_predict(self, model):
        """Test emulator predictions.

        Compare emulator predictions to training data.
        """
        # Init. emulator.
        emu = NonLinearMGBoostEmulator(model=model, n_jobs=n_jobs)

        # Check that params range dict is present.
        assert emu.params_range is not None

        # Check wavenumber bins.
        assert emu.kbins is not None

        # Load / train emulator.
        emu.load_train_all()

        # Loop over scale factor nodes.
        for aexp in emu.aexp_nodes:
            # Get cosmological parameters of training models.
            cosmo_params = emu._emulator_nodes[aexp]._params

            # Format into input dict. for the emulator.
            cosmo_params_dict = {
                param: cosmo_params[:, i]
                for i, param in enumerate(emu.params_range.keys())
            }

            # Get training data.
            data = emu._emulator_nodes[aexp]._data

            # Get emulator predictions.
            pred = emu.predict_boost(cosmo_params_dict, aexp)

            # Check pred array shape.
            assert pred.shape == (data.shape[0], emu.kbins.shape[0])

            # Check that mean absolute relative difference
            # between emulator and training data is smaller than 0.1%
            abs_rel_diff = np.abs((pred - data) / data)
            mean_abs_rel_diff = np.mean(abs_rel_diff)

            assert mean_abs_rel_diff < 1e-3

    def test_predict_vector(self, model):
        """Test emulator predictions in vectorized mode.

        Compare vectorized predictions for multiple cosmological
        models to non-vectorized ones.

        The comparison is done for the cosmological parameters
        of the training data.
        """
        # Init. emulator.
        emu = NonLinearMGBoostEmulator(model=model, n_jobs=n_jobs)

        # Load / train emulator.
        emu.load_train_all()

        # Loop over scale factor nodes.
        for aexp in emu.aexp_nodes:
            # Get cosmological parameters of training models.
            cosmo_params = emu._emulator_nodes[aexp]._params

            # Format into input dict. for the emulator.
            cosmo_params_dict = {
                param: cosmo_params[:, i]
                for i, param in enumerate(emu.params_range.keys())
            }

            # Get emulator predictions
            # in vectorized mode.
            pred_vec = emu.predict_boost(cosmo_params_dict, aexp)

            # Init. arrays to store non-vectorized predictions.
            pred_nonvec = np.empty(pred_vec.shape)

            # Loop over cosmological models.
            for m in range(cosmo_params.shape[0]):
                # Input dict. with a single
                # cosmological model.
                cosmo_params_dict = {
                    param: cosmo_params[m, i]
                    for i, param in enumerate(emu.params_range.keys())
                }

                # Get emulator predictions
                # for a single cosmological model.
                pred_nonvec[m] = emu.predict_boost(cosmo_params_dict, aexp)

            # Check that mean absolute relative difference between
            # vector and non-vector predictions is smaller than 0.0001%
            abs_rel_diff = np.abs((pred_vec - pred_nonvec) / pred_nonvec)
            mean_abs_rel_diff = np.mean(abs_rel_diff)

            assert mean_abs_rel_diff < 1e-6

    def test_emulation_range_exception(self, model):
        """Test raised exceptions for input parameters out of emulation range."""
        # Init. emulator.
        emu = NonLinearMGBoostEmulator(model=model, n_jobs=n_jobs)

        # Load / train emulator.
        emu.load_train_all()

        # Get cosmological parameters of training data.
        aexp = emu.aexp_nodes[0]
        cosmo_params = emu._emulator_nodes[aexp]._params

        # Format into input dict. for the emulator.
        cosmo_params_dict = {
            param: cosmo_params[0, i] for i, param in enumerate(emu.params_range.keys())
        }

        # Scale factor out of range.
        with pytest.raises(EmulationRangeError):
            emu.predict_boost(cosmo_params_dict, aexp=4)

        # Wavenumber out of range.
        with pytest.raises(EmulationRangeError):
            emu.predict_boost(cosmo_params_dict, aexp=1, k=15)

        # Cosmology (Omega_m) out of range.
        cosmo_params_dict["Omega_m"] = 1
        with pytest.raises(EmulationRangeError):
            emu.predict_boost(cosmo_params_dict, aexp=1)


class TestNonLinearFofrBoostEmulators:
    """A class implementing tests for the nonlinear f(R) boost emulators.

    These are complementary tests to those of TestNonLinearMGBoostEmulator.
    """

    def test_new_interface_v1_vs_v2(self):
        """Test predictions from v1 and v2 version.

        The test is done within the emulation range of v1
        in terms of cosmological parameters and scale factors.

        The test cosmological models are generated with a Sobol sequence.
        """
        # Init. emulators.
        emu_v1 = NonLinearMGBoostEmulator(model="fR_v1", n_jobs=n_jobs)
        emu_v2 = NonLinearMGBoostEmulator(model="fR", n_jobs=n_jobs)

        # Load / train emulators.
        emu_v1.load_train_all()
        emu_v2.load_train_all()

        # Emulation range for v1 emulator.
        ranges = {}
        ranges["Omega_m"] = (0.2365, 0.3941)
        ranges["logfR0"] = (4, 7)
        ranges["sigma8_lcdm"] = (0.6083, 1.014)

        # Generate Sobol sequence (N=1024) within
        # the emulation range of v1 emulator.
        sobol_sampler = qmc.Sobol(d=3, scramble=True, rng=None)
        sobol_design = sobol_sampler.random_base2(m=10)

        l_bounds = []
        u_bounds = []

        for param in ranges:
            l_bounds.append(ranges[param][0])
            u_bounds.append(ranges[param][1])

        sobol_design = qmc.scale(sobol_design, l_bounds, u_bounds)

        # Create input dicts with cosmological parameters
        # from the Sobol sequence.
        cosmo_params_v1 = {}
        cosmo_params_v2 = {}
        for i, param in enumerate(ranges.keys()):
            cosmo_params_v1[param] = sobol_design[:, i]
            cosmo_params_v2[param] = sobol_design[:, i]

        cosmo_params_v2["h"] = 0.6736
        cosmo_params_v2["n_s"] = 0.9649
        cosmo_params_v2["Omega_b"] = 0.049302

        # Generate wavenumber array.
        kbins = np.geomspace(1e-3, 9.5, 100)

        # Generate scale factor array
        # using the emulation range from v1.
        aexp_list = np.linspace(emu_v1.aexp_nodes[0], emu_v1.aexp_nodes[-1], 100)

        # Loop over scale factor values.
        for aexp in aexp_list:
            # Get predictions from both emulators at default wavenumber bins.
            pred_v1 = emu_v1.predict_boost(cosmo_params_v1, aexp)
            pred_v2 = emu_v2.predict_boost(cosmo_params_v2, aexp)

            # Check that mean absolute relative difference
            # between both emulators is smaller than 1%.
            abs_rel_diff = np.abs((pred_v2 - pred_v1) / pred_v1)
            mean_abs_rel_diff = np.mean(abs_rel_diff)

            assert mean_abs_rel_diff < 1e-2

            # Same for other wavenumber bins.
            pred_v1 = emu_v1.predict_boost(cosmo_params_v1, aexp, k=kbins)
            pred_v2 = emu_v2.predict_boost(cosmo_params_v2, aexp, k=kbins)

            # Check that mean absolute relative difference
            # between both emulators is smaller than 1%.
            abs_rel_diff = np.abs((pred_v2 - pred_v1) / pred_v1)
            mean_abs_rel_diff = np.mean(abs_rel_diff)

            assert mean_abs_rel_diff < 1e-2

    def test_v1_new_vs_old_interface(self):
        """Compare new NonLinearMGBoostEmulator and old FofrBoost interface predictions.

        The comparison is done only for the v1 emulator from NonLinearMGBoostEmulator,
        since it is the one equivalent to FofrBoost.

        The test cosmological models are generated with a Sobol sequence.
        """
        # Init. emulator with new interface.
        emu = NonLinearMGBoostEmulator(model="fR_v1", n_jobs=n_jobs)

        # Load / train emulator.
        emu.load_train_all()

        # Init. old interface.
        emu_old = FofrBoost(n_jobs=n_jobs, extrapolate_low_k=True)

        # Emulation range emulator.
        ranges = {}
        ranges["Omega_m"] = (0.2365, 0.3941)
        ranges["logfR0"] = (4, 7)
        ranges["sigma8_lcdm"] = (0.6083, 1.014)

        # Generate Sobol sequence (N=1024) within
        # the emulation range.
        sobol_sampler = qmc.Sobol(d=3, scramble=True, rng=None)
        sobol_design = sobol_sampler.random_base2(m=10)

        l_bounds = []
        u_bounds = []

        for param in ranges:
            l_bounds.append(ranges[param][0])
            u_bounds.append(ranges[param][1])

        sobol_design = qmc.scale(sobol_design, l_bounds, u_bounds)

        # Create input dict. with cosmological parameters
        # from the Sobol sequence.
        cosmo_params = {}
        for i, param in enumerate(ranges.keys()):
            cosmo_params[param] = sobol_design[:, i]

        # Generate wavenumber array.
        kbins = np.geomspace(1e-3, 9.5, 100)

        # Generate scale factor array.
        aexp_list = np.linspace(emu_old.aexp_nodes[0], emu_old.aexp_nodes[-1], 100)

        # Loop over scale factor values.
        for aexp in aexp_list:
            # Get predictions from new interface for default wavenumber bins.
            pred = emu.predict_boost(cosmo_params, aexp)

            # Get predictions from old interface for default wavenumber bins.
            pred_old = emu_old.predict_boost(
                omega_m=cosmo_params["Omega_m"],
                sigma8_lcdm=cosmo_params["sigma8_lcdm"],
                logfR0=cosmo_params["logfR0"],
                aexp=aexp,
            )

            # Check that mean absolute relative difference
            # between both emulators is smaller than 0.5%.
            abs_rel_diff = np.abs((pred - pred_old) / pred_old)
            mean_abs_rel_diff = np.mean(abs_rel_diff)

            assert mean_abs_rel_diff < 5e-3

            # Same for other wavenumber bins.
            pred = emu.predict_boost(cosmo_params, aexp, k=kbins)
            pred_old = emu_old.predict_boost(
                omega_m=cosmo_params["Omega_m"],
                sigma8_lcdm=cosmo_params["sigma8_lcdm"],
                logfR0=cosmo_params["logfR0"],
                aexp=aexp,
                k=kbins,
            )

            # Check that mean absolute relative difference
            # between both emulators is smaller than 0.5%.
            abs_rel_diff = np.abs((pred - pred_old) / pred_old)
            mean_abs_rel_diff = np.mean(abs_rel_diff)

            assert mean_abs_rel_diff < 5e-3
