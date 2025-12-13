# Obz AI - Copyright (C) 2025 Alethia XAI Sp. z o.o.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

from typing import Dict, Any, List, Optional

from obzai.data_inspection.inspectors.base_data_inspector import _BaseDataInspector
from obzai.data_inspection.extractors import FirstOrderExtractor
from obzai.data_inspection.feature_pipeline import FeaturePipeline
from obzai.data_inspection.od_models import GMMModel
from obzai.data_inspection.schemas.types import FeatureType


class GMMInspector(_BaseDataInspector):
    def __init__(
        self,
        extractors: FirstOrderExtractor,
        n_components: int = 16,
        outlier_quantile: float = 0.01,
        **gmm_kwargs
        ):
        pipeline = FeaturePipeline(extractors, project_features=False)
        gmm_model = GMMModel(n_components=n_components, outlier_quantile=outlier_quantile, **gmm_kwargs)
        super().__init__(pipeline, gmm_model)
        
        self._name = "GMMInspector"
        self._logged_feature_type = FeatureType.INTERPRETABLE
        self._hyperparams = {"n_components": n_components, "outlier_quantile": outlier_quantile}

    @property
    def name(self) -> str:
        return self._name

    @property
    def logged_feature_type(self) -> FeatureType:
        return self._logged_feature_type
    
    @property
    def feature_names(self) -> Optional[List[str]]:
        return self.feature_pipeline.feature_names
    
    @property
    def hyperparams(self) -> Dict[str, Any]:
        return self._hyperparams
