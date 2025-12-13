# Obz AI - Copyright (C) 2025 Alethia XAI Sp. z o.o.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
from typing import List
from sklearn.decomposition import PCA

from obzai.data_inspection.od_models.base_od_model import _BaseODModel, register_od_model
from obzai.data_inspection.schemas.exceptions import ODModelError


class PCARecModel(_BaseODModel):
    """
    The class implement Outlier Detection protocol utilizing PCA Reconstruction Loss.
    """
    def __init__(self, n_components: int = 64, outlier_quantile: float = 0.01, **pca_kwargs):
        """
        Creates an instance of PCAReconstructionModel. 

        Args:
            n_components: Dimensionality of latent space, aka number of PCA components
            outlier_quantile: Quantile required to set a outlier threshold
            **pca_kwargs: Additional keyword arguments for the PCA constructor.
        """
        super().__init__(outlier_quantile=outlier_quantile, higher_scores_normal=False)
        self.pca = PCA(n_components=n_components, **pca_kwargs)

    def _fit_model(self, image_features: np.ndarray) -> None:
        """
        Model specific fitting method.
        """
        self.pca.fit(image_features)

    def _score(self, image_features: np.ndarray) -> np.ndarray:
        """
        Model specific scoring method.
        """
        latent = self.pca.transform(image_features)
        reconstructed_data = self.pca.inverse_transform(latent)
        scores = np.mean((image_features - reconstructed_data)**2, axis=1)
        return scores.squeeze()

    def _serialize_model_state(self):
        return {
            "init_params": {
                "outlier_quantile": self.outlier_quantile,
                **self.pca.get_params(deep=False)
            },
            "pca_state": self.pca
        }

    def _load_model_state(self, state):
        pca_state = state.get("pca_state")
        if pca_state is None:
            raise ODModelError("Serialized state missing 'pca_state'.")
        self.pca = pca_state


# Register in the OD model registry for checkpoint reconstruction.
register_od_model(PCARecModel)
