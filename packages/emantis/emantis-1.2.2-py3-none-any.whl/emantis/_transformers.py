"""Module with some classes to transform data before emulation.

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
from sklearn import decomposition, preprocessing


class PCATransformer:
    """PCA Transformer.

    Parameters
    ----------
    pca_components: int or float or str or None, default=None
        The number of PCA components to use.
        This parameter is passed down as the ``n_components`` of the
        `scikit-learn <https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html>`_
        library.
    scale_data_mean : bool, default=True
        If True, center the data before the PCA.
    scale_data_std : bool, default=True
        If True, scale data to unit variance before the PCA.
    std_niter : int, default=1000
        The number of Monte Carlo steps used
        to propagate errors through the PCA.
        Must be > 1.
    pca_extra_args: `sklearn.decomposition.PCA` parameters, optional
        Additional parameters for the PCA.
    random_seed: int or None, default=None
        The random seed used to initialize random generators.
        Pass an int in order to obtain reproducible results.

    """

    def __init__(
        self,
        pca_components: int | float | str | None = None,
        scale_data_mean: bool = True,
        scale_data_std: bool = True,
        std_niter: int = 100,
        random_seed: int | None = None,
        **pca_extra_args,
    ) -> None:
        # Number of PCA components to keep.
        self.n_components = pca_components

        # Scaler used before fitting the PCA.
        self.data_scaler = preprocessing.StandardScaler(
            with_mean=scale_data_mean, with_std=scale_data_std
        )

        # Scaler used to propagate errors (i.e. no shift).
        self.data_std_scaler = preprocessing.StandardScaler(
            with_mean=False, with_std=scale_data_std
        )

        # Scikit-learn pca object.
        self.pca = decomposition.PCA(n_components=self.n_components, **pca_extra_args)

        # Number of PCA coefficients, once the PCA has been fitted.
        self.n_pca: int | None = None

        self.std_niter = std_niter

        # Random seed.
        self.random_seed = random_seed

    def fit(self, data) -> None:
        """Fit the PCA transformer.

        Parameters
        ----------
        data : array of shape (n_samples, n_features)
            The data array, where `n_samples` is the number of samples
            and `n_features` is the number of features.

        """
        # Fit the data scalers.
        self.data_scaler.fit(data)
        self.data_std_scaler.fit(data)
        # Scale the data before fitting the PCA.
        data_scaled = self.data_scaler.transform(data)

        # Fit the PCA.
        self.pca.fit(data_scaled)

        # Get number of PCA coefficients.
        self.n_pca = self.pca.explained_variance_ratio_.shape[0]

    def transform(
        self,
        data: npt.NDArray,
    ) -> npt.NDArray:
        """Perform the PCA transformation.

        Parameters
        ----------
        data : array of shape (n_samples, n_features)
            The data array, where `n_samples` is the number of samples
            and `n_features` is the number of features.

        Returns
        -------
        data_transformed : array of shape (n_samples, n_components)
            The transformed data array, where `n_samples` is the number of samples
            and `n_components` is the number of PCA components.

        """
        # Transform data (scaling + PCA).
        data_transformed = self.pca.transform(self.data_scaler.transform(data))

        return data_transformed

    def inverse_transform(
        self,
        data_transformed: npt.NDArray,
    ) -> npt.NDArray:
        """Perform the inverse PCA transformation.

        Parameters
        ----------
        data_transformed : array of shape (n_samples, n_components)
            A data array in the transformed space, where `n_samples` is the number
            of samples and `n_components` is the number of PCA components.

        Returns
        -------
        data_original : array of shape (n_samples, n_features)
            The original data array, which would be transformed into `data_transformed`,
            where `n_samples` is the number of samples
            and `n_features` is the number of features.

        """
        # Inverse transform data (inverse PCA + inverse scaling).
        data_original = self.data_scaler.inverse_transform(
            self.pca.inverse_transform(data_transformed)
        )

        return data_original

    def propagate_std(
        self,
        data: npt.NDArray,
        data_std: npt.NDArray,
    ) -> npt.NDArray:
        """Propagate data standard deviation through PCA transformation.

        Parameters
        ----------
        data : array of shape (n_samples, n_features)
            The data array, where `n_samples` is the number of samples
            and `n_features` is the number of features.
        data_std : array of shape (n_samples, n_features)
            The data standard deviation array, where `n_samples` is the number
            of samples and `n_features` is the number of features.

        Returns
        -------
        data_transformed : array of shape (n_samples, n_components)
            The transformed data standard deviation array,
            where `n_samples` is the number of samples
            and `n_components` is the number of PCA components.

        """
        # TODO: Optimize: make analytical or vectorize.
        # Propagate errors through the transformation.
        # Monte Carlo propagation.
        data_transformed_iter = []
        rng = np.random.default_rng(seed=self.random_seed)
        for _ in range(self.std_niter):
            data_iter = data + rng.normal(loc=0, scale=data_std)
            data_transformed_iter.append(
                self.pca.transform(self.data_scaler.transform(data_iter))
            )

        data_transformed_std = np.std(data_transformed_iter, axis=0, ddof=1)

        # Analytic propagation. WARNING: does not seem to work very well.
        # NEEDS MORE TESTING.
        # data_transformed_std = np.dot(
        #     self.data_std_scaler.transform(data_std), np.abs(self.pca.components_.T)
        # )

        return data_transformed_std

    def inverse_propagate_std(
        self,
        data_transformed: npt.NDArray,
        data_transformed_std: npt.NDArray,
    ) -> npt.NDArray:
        """Propagate data standard deviation through the inverse PCA transformation.

        Parameters
        ----------
        data_transformed : array of shape (n_samples, n_components)
            A data array in the transformed space,
            where `n_samples` is the number of samples
            and `n_components` is the number of PCA components.
        data_transformed_std : array of shape (n_samples, n_components)
            The standard deviation array of the data in the transformed space,
            where `n_samples` is the number of samples
            and `n_components` is the number of PCA components.

        Returns
        -------
        data_original_std : array of shape (n_samples, n_features), default=None
            The standard deviation of the original data array,
            which would be transformed into `data_transformed`,
            where `n_samples` is the number of samples
            and `n_features` is the number of features.

        """
        # TODO: Optimize: make analytical or vectorize.
        # Propagate errors through inverse transformation.
        # Monte Carlo propagation.
        data_original_iter = []
        rng = np.random.default_rng(seed=self.random_seed)
        for _ in range(self.std_niter):
            data_iter = data_transformed + rng.normal(loc=0, scale=data_transformed_std)
            data_original_iter.append(
                self.data_scaler.inverse_transform(
                    self.pca.inverse_transform(data_iter)
                )
            )

        data_original_std = np.std(data_original_iter, axis=0, ddof=1)

        # Analytic propagation. WARNING: does not seem to work very well.
        # NEEDS MORE TESTING.
        # elif self.std_niter == -1:
        #     data_original_std = self.data_std_scaler.inverse_transform(
        #         np.dot(data_transformed_std, np.abs(self.pca.components_))
        #     )

        # else:
        #     data_original_std = self.data_scaler.inverse_transform(
        #         np.dot(data_transformed_std, np.abs(self.pca.components_))
        #         + self.pca.mean_
        #     )
        #     norm_pca = self.data_scaler.inverse_transform(
        #         self.pca.inverse_transform([0 for _ in range(self.n_pca)]).reshape(
        #             1, -1
        #         )
        #     )
        #     data_original_std -= norm_pca

        return data_original_std
