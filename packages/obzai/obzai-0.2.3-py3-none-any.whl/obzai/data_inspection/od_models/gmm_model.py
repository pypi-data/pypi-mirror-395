# Obz AI - Copyright (C) 2025 Alethia XAI Sp. z o.o.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
from typing import List
from sklearn.mixture import GaussianMixture

from obzai.data_inspection.od_models.base_od_model import _BaseODModel, register_od_model
from obzai.data_inspection.schemas.exceptions import ODModelError


class GMMModel(_BaseODModel):
    """
    The class implement Outlier Detection protocol utilizing Gaussian Mixture Models.
    """
    def __init__(self, n_components: int = 16, outlier_quantile: float = 0.01, **gmm_kwargs):
        """
        Creates an instance of GMMModel. 

        Args:
            n_components: Number of Gaussian Components
            outlier_quantile: Quantile required to set a outlier threshold
            **gmm_kwargs: Additional keyword arguments for the GaussianMixture constructor.
        """
        super().__init__(outlier_quantile=outlier_quantile, higher_scores_normal=True)
        self.gmm = GaussianMixture(n_components=n_components, **gmm_kwargs)

    def _fit_model(self, image_features: np.ndarray) -> None:
        """
        Model specific fitting method.
        """
        self.gmm.fit(image_features)

    def _score(self, image_features: np.ndarray) -> np.ndarray:
        """
        Model specific scoring method.
        """
        scores = self.gmm.score_samples(image_features)
        return scores.squeeze()

    def _serialize_model_state(self):
        return {
            "init_params": {
                "outlier_quantile": self.outlier_quantile,
                **self.gmm.get_params(deep=False)
            },
            "gmm_state": self.gmm
        }

    def _load_model_state(self, state):
        gmm_state = state.get("gmm_state")
        if gmm_state is None:
            raise ODModelError("Serialized state missing 'gmm_state'.")
        self.gmm = gmm_state


# Register in the OD model registry for checkpoint reconstruction.
register_od_model(GMMModel)
