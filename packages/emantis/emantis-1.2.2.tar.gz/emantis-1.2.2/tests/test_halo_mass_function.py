"""A module implementing tests for the HMF emulators."""

import os

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["BLIS_NUM_THREADS"] = "1"

import joblib
import numpy as np
import pytest

from emantis.halo_mass_function import (
    _FOF_B_VALUES,
    _HMF_MODELS,
    _SO_DELTAC_VALUES,
    HMFEmulator,
)

n_jobs_max = 6
n_jobs = min(joblib.cpu_count(), n_jobs_max)

_HMF_MASS_DEF = [f"b{elt}" for elt in _FOF_B_VALUES] + [
    f"{elt}c" for elt in _SO_DELTAC_VALUES
]


@pytest.mark.parametrize("model", _HMF_MODELS)
@pytest.mark.parametrize("mass_def", _HMF_MASS_DEF)
class TestHMFEmulator:
    """A class implementing tests for the HMF emulators."""

    def test_train(self, model, mass_def):
        """Test the emulator training.

        It is better to run this test first, so that subsequent tests
        benefit from the trained emulators.
        """
        # Init. emulator.
        emu = HMFEmulator(model=model, mass_def=mass_def, n_jobs=n_jobs)

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

    def test_predict(self, model, mass_def):
        """Test emulator predictions.

        Compare emulator predictions to training data.
        """
        # Init. emulator.
        emu = HMFEmulator(model=model, mass_def=mass_def, n_jobs=n_jobs)

        # Check that params range dict is present.
        assert emu.params_range is not None

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

            # Generate mass bins spanning the whole emulation
            # range at the given scale factor.
            m_min, m_max = emu.range("mass_halo", aexp=aexp)
            m_bins = np.geomspace(m_min, m_max, 100)

            # Get training data and data_std.
            data = emu._emulator_nodes[aexp]._data
            data_std = emu._emulator_nodes[aexp]._data_std

            # Check that data_std is not None.
            assert data_std is not None

            # Transform training data from Bspline
            # basis to mass bins.
            data = emu._emulator_nodes[aexp]._transform_gp_prediction(data, x=m_bins)

            # Get emulator predictions.
            # Return pred_std even if it is not used
            # in this test other than for array shape check.
            pred, pred_std = emu.predict_hmf(
                m_bins, cosmo_params_dict, aexp, return_std=True
            )

            # Check pred array shape.
            assert pred.shape == (data.shape[0], m_bins.shape[0])
            assert pred_std.shape == (data.shape[0], m_bins.shape[0])

            # Computed absolute relative difference
            # between emulator predictions and training data.
            abs_rel_diff = np.abs((pred - data) / data)

            # Median absolute relative error in first mass bin smaller than 1%.
            assert np.median(abs_rel_diff[:, 0]) < 0.01

            # Median absolute relative error in last mass bin smaller than 10%.
            assert np.median(abs_rel_diff[:, -1]) < 0.1

            # Median absolute relative error across all mass bins smaller than 5%.
            assert np.median(abs_rel_diff) < 0.05

    def test_predict_vector(self, model, mass_def):
        """Test emulator predictions in vectorized mode.

        Compare vectorized predictions for multiple cosmological
        models to non-vectorized ones.

        The comparison is done for the cosmological parameters
        of the training data.
        """
        # Init. emulator.
        emu = HMFEmulator(model=model, mass_def=mass_def, n_jobs=n_jobs)

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

            # Generate mass bins spanning the whole emulation
            # range at the given scale factor.
            m_min, m_max = emu.range("mass_halo", aexp=aexp)
            m_bins = np.geomspace(m_min, m_max, 100)

            # Get emulator predictions (with std)
            # in vectorized mode.
            pred_vec, pred_std_vec = emu.predict_hmf(
                m_bins, cosmo_params_dict, aexp, return_std=True
            )

            # Init. arrays to store non-vectorized predictions.
            pred_nonvec = np.empty(pred_vec.shape)
            pred_std_nonvec = np.empty(pred_vec.shape)

            # Loop over cosmological models.
            for m in range(cosmo_params.shape[0]):
                # Input dict. with a single
                # cosmological model.
                cosmo_params_dict = {
                    param: cosmo_params[m, i]
                    for i, param in enumerate(emu.params_range.keys())
                }

                # Get emulator predictions (with std)
                # for a single cosmological model.
                pred_nonvec[m], pred_std_nonvec[m] = emu.predict_hmf(
                    m_bins, cosmo_params_dict, aexp, return_std=True
                )

            # Check that mean absolute relative difference between
            # vector and non-vector predictions is smaller than 0.0001%
            abs_rel_diff = np.abs((pred_vec - pred_nonvec) / pred_nonvec)
            mean_abs_rel_diff = np.mean(abs_rel_diff)

            assert mean_abs_rel_diff < 1e-6

            # Same for emulator std.
            abs_rel_diff = np.abs((pred_std_vec - pred_std_nonvec) / pred_std_nonvec)
            mean_abs_rel_diff = np.mean(abs_rel_diff)

            assert mean_abs_rel_diff < 1e-6

    def test_predict_with_std(self, model, mass_def):
        """Test emulator predictions when std is returned or not.

        The comparison is done for the cosmological parameters
        of the training data.
        """
        # Init. emulator.
        emu = HMFEmulator(model=model, mass_def=mass_def, n_jobs=n_jobs)

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

            # Generate mass bins spanning the whole emulation
            # range at the given scale factor.
            m_min, m_max = emu.range("mass_halo", aexp=aexp)
            m_bins = np.geomspace(m_min, m_max, 100)

            # Get emulator predictions with std.
            pred_with_std, _ = emu.predict_hmf(
                m_bins, cosmo_params_dict, aexp, return_std=True
            )

            # Get emulator predictions without std.
            pred_wo_std = emu.predict_hmf(
                m_bins, cosmo_params_dict, aexp, return_std=False
            )

            # Check that mean absolute relative difference between
            # the predictions with and without std is equal to zero.
            abs_rel_diff = np.abs((pred_with_std - pred_wo_std) / pred_wo_std)
            mean_abs_rel_diff = np.mean(abs_rel_diff)

            assert mean_abs_rel_diff == 0
