"""
e-MANTIS
========

e-MANTIS is a python package containing emulators providing theoretical predictions
for the nonlinear large-scale structure formation in the context of alternative
dark energy and gravity theories.
It uses Gaussian processes to perform a fast and accurate interpolation
between the outputs of high resolution cosmological N-body simulations.
The emulator supports multiple cosmological models and observables.
It is divided in multiple modules, each one focusing on a particular type of observable.

Available modules
-----------------

matter_power_spectrum
    Emulators for the matter power spectrum.
halo_mass_function
    Emulator for the halo mass function.
powerspectrum_matter
    Emulators for the matter power spectrum.
    Deprecated, use matter_power_spectrum instead.

"""  # noqa: D400, D205

import logging

from . import halo_mass_function, matter_power_spectrum
from .powerspectrum_matter import FofrBoost

# Capture warnings by the logging system.
logging.captureWarnings(True)

__all__ = ["FofrBoost", "matter_power_spectrum", "halo_mass_function"]
