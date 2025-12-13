# Obz AI - Copyright (C) 2025 Alethia XAI Sp. z o.o.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

from scipy.stats import skew, kurtosis
from typing import List, Optional
import numpy as np
import torch

from obzai.data_inspection.extractors.extractor import Extractor, register_extractor


class FeatureRegistry:
    """
    Registry for feature extraction functions.
    """
    _features = {}

    @classmethod
    def register(cls, name: str):
        def decorator(func):
            cls._features[name] = func
            return func
        return decorator

    @classmethod
    def get_features(cls, names: Optional[List[str]] = None):
        if names is None:
            return cls._features
        return {name: cls._features[name] for name in names if name in cls._features}

    @classmethod
    def list_features(cls):
        return list(cls._features.keys())


class FirstOrderExtractor(Extractor):
    """
    Extracts first-order statistical features from images, inspired by PyRadiomics.
    Features can be easily extended and subsetted.
    """
    def __init__(self, 
                 features: List[str] = ["entropy", "min", "max", "10th_percentile", 
                                        "90th_percentile", "mean", "median", 
                                        "interquartile_range", "range", "mean_absolute_deviation", 
                                        "robust_mean_absolute_deviation", "root_mean_square", 
                                        "skewness", "kurtosis", "variance", "uniformity"]):
        
        if not isinstance(features, list) or len(features) == 0: 
            raise ValueError("Expected provided feature names to be a non-empty list.")

        self.feature_functions = FeatureRegistry.get_features(features)
        self.feature_names = list(self.feature_functions.keys())
        self.feat_ids = [i for i in range(1, len(self.feature_names) + 1)]
        self.id = 1
        self.name = self.__class__.__name__

    @FeatureRegistry.register("entropy")
    def get_entropy(self, image: torch.Tensor) -> torch.Tensor:
        hist = torch.histc(image, bins=256, min=0, max=1)
        hist = hist / hist.sum()
        return -(hist * torch.log2(hist + 1e-6)).sum()

    @FeatureRegistry.register("min")
    def get_min_value(self, image: torch.Tensor) -> torch.Tensor:
        return image.min()

    @FeatureRegistry.register("max")
    def get_max_value(self, image: torch.Tensor) -> torch.Tensor:
        return image.max()

    @FeatureRegistry.register("10th_percentile")
    def get_10th_percentile(self, image: torch.Tensor) -> torch.Tensor:
        return torch.quantile(image.flatten(), 0.1)

    @FeatureRegistry.register("90th_percentile")
    def get_90th_percentile(self, image: torch.Tensor) -> torch.Tensor:
        return torch.quantile(image.flatten(), 0.9)

    @FeatureRegistry.register("mean")
    def mean(self, image: torch.Tensor) -> torch.Tensor:
        return torch.mean(image)

    @FeatureRegistry.register("median")
    def median(self, image: torch.Tensor) -> torch.Tensor:
        return torch.median(image)

    @FeatureRegistry.register("interquartile_range")
    def get_interquartile_range(self, image: torch.Tensor) -> torch.Tensor:
        q3 = torch.quantile(image.flatten(), 0.75)
        q1 = torch.quantile(image.flatten(), 0.25)
        return q3 - q1

    @FeatureRegistry.register("range")
    def get_range(self, image: torch.Tensor) -> torch.Tensor:
        return image.max() - image.min()

    @FeatureRegistry.register("mean_absolute_deviation")
    def get_mean_absolute_deviation(self, image: torch.Tensor) -> torch.Tensor:
        mean = torch.mean(image)
        return torch.mean(torch.abs(image - mean))

    @FeatureRegistry.register("robust_mean_absolute_deviation")
    def get_robust_mean_absolute_deviation(self, image: torch.Tensor) -> torch.Tensor:
        prcnt10 = self.get_10th_percentile(image)
        prcnt90 = self.get_90th_percentile(image)
        arr_subset = image[(image >= prcnt10) & (image <= prcnt90)]
        return torch.mean(torch.abs(arr_subset - torch.mean(arr_subset)))

    @FeatureRegistry.register("root_mean_square")
    def get_root_mean_square(self, image: torch.Tensor) -> torch.Tensor:
        return torch.sqrt(torch.mean(image ** 2))

    @FeatureRegistry.register("skewness")
    def get_skewness(self, image: torch.Tensor) -> torch.Tensor:
        res = skew(image.flatten().detach().cpu().numpy())
        return torch.tensor(res)

    @FeatureRegistry.register("kurtosis")
    def get_kurtosis(self, image: torch.Tensor) -> torch.Tensor:
        res = kurtosis(image.flatten().detach().cpu().numpy())
        return torch.tensor(res)

    @FeatureRegistry.register("variance")
    def get_variance(self, image: torch.Tensor) -> torch.Tensor:
        return torch.var(image)

    @FeatureRegistry.register("uniformity")
    def get_uniformity(self, image: torch.Tensor) -> torch.Tensor:
        hist = torch.histc(image, bins=256, min=0, max=1)
        hist = hist / hist.sum()
        return (hist ** 2).sum()

    def _compute_features_for_image(self, image: torch.Tensor) -> torch.Tensor:
        """
        Computes chosen first-order statistical features for a single image.
        """
        features = [func(self, image) for func in self.feature_functions.values()]
        return torch.stack(features)

    def extract(self, image_batch: torch.Tensor) -> np.ndarray:
        """
        Extracts image features.
        """
        image_batch = self._process_batch(image_batch, ensure_grayscale=True, ensure_scale=True)
        features = []
        for idx in range(len(image_batch)):
            feat = self._compute_features_for_image(image_batch[idx])
            features.append(feat)
        return torch.stack(features, dim=0).numpy()

    def get_config(self):
        return {
            "class": self.__class__.__name__,
            "module": self.__module__,
            "features": self.feature_names
        }

    @classmethod
    def _from_config(cls, config, device=None):
        features = config.get("features", None)
        return cls(features=features) if features is not None else cls()


# Register in the extractor registry for checkpoint reconstruction.
register_extractor(FirstOrderExtractor)
