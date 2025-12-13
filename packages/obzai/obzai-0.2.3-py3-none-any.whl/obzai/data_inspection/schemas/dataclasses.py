# Obz AI - Copyright (C) 2025 Alethia XAI Sp. z o.o.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.


from typing import List, Optional, Dict, Any
from dataclasses import dataclass
import pandas as pd
import numpy as np

# Custom Types
from obzai.data_inspection.schemas.types import FeatureType


@dataclass
class DataInspectionResults:
    """
    Class specifying data inspector results.
    """
    inspector_id: str
    outliers: List[bool]
    scores: List[float]
    feature_type: FeatureType
    feature_names: List[str]
    raw_features: np.ndarray
    norm_features: np.ndarray
    pca_projections: Optional[np.ndarray] = None
    umap_projections: Optional[np.ndarray] = None

    def extract_features_data_for_example(self, idx: int) -> Dict[str, Any]:
        """
        Extracts ready to upload feature data for a single example.

        Args:
            idx: Index of the example in a batch.
        
        Returns:
            a dictionary containing features data for a particular image in batch.
        """
        # (1) Achieve Feature Vector
        feature_vector = self.raw_features[idx, :].tolist()

        # (2) If available, provide mapping: feature_name -> feature value
        if self.feature_type == "INTERPRETABLE":
            named_features = {
                feat_name: feat_value for feat_name, feat_value in zip(self.feature_names, feature_vector)
            }
        else:
            named_features = None

        # (3) If available, provide projected coordinates
        if (self.feature_type == "PROJECTION") and (self.pca_projections is not None) and (self.umap_projections) is not None:
            feature_projection = {
                "pca_projection": (float(self.pca_projections[idx,0]), float(self.pca_projections[idx, 1])),
                "umap_projection": (float(self.umap_projections[idx,0]), float(self.umap_projections[idx, 1]))
            }
        else:
            feature_projection = None
        
        # (4) Return ready to use feature data
        return {
            "feature_type": self.feature_type,
            "feature_vector": feature_vector,
            "named_features": named_features,
            "feature_projection": feature_projection
        }
                

@dataclass
class ImageFeatures:
    """
    Dataclass providing scheme for image features storage.
    """
    feature_names: List[str]
    raw_features: np.ndarray
    norm_features: np.ndarray
    pca_projections: Optional[np.ndarray] = None
    umap_projections: Optional[np.ndarray] = None


@dataclass
class OutlierDetectionResults:
    """
    Dataclass providing scheme for outlier detection results.
    """
    outliers: List[bool]
    scores: List[float]


@dataclass
class ReferenceData:
    """
    Dataclass providing scheme for storing extracted reference features.
    """
    inspector_id: str
    feature_type: FeatureType
    raw_features: pd.DataFrame
    norm_features: pd.DataFrame
    pca_projections: Optional[pd.DataFrame] = None
    umap_projections: Optional[pd.DataFrame] = None

    def _validate_number_of_records(self):
        """
        Checks whether all data frames contain the same
        number of examples.
        """
        lens = {}

        lens["raw_features"] = len(self.raw_features.index)
        lens["norm_features"] = len(self.norm_features.index)
    
        if self.pca_projections is not None:
            lens["pca_projections"] = len(self.pca_projections.index)
        
        if self.umap_projections is not None:
            lens["umap_projections"] = len(self.umap_projections.index)

        if len(set(lens.values())) != 1:
            raise ValueError("Incosistent number of records across dataframes.")
        else:
            return lens["raw_features"]


    def prepare_data2upload(self) -> pd.DataFrame:
        """
        The method prepares data for the upload into ObzAI Backend.
        """
        # (1) Validate reference data
        n_examples = self._validate_number_of_records()

        # (2) Create a list of records
        records = []
        for idx in range(n_examples):
            # (2.1) Extract row with normalized features and convert into a feature vector
            norm_row = self.norm_features.iloc[idx]
            feature_vector = norm_row.astype(float).to_list()

            # (2.2) If needed, provide feat_name -> feat_value mapping
            if self.feature_type == "INTERPRETABLE":
                named_features = norm_row.astype(float).to_dict()
            else:
                named_features = None

            # (2.3) If needed, provide projections
            if (self.feature_type == "PROJECTION") and self.pca_projections is not None and self.umap_projections is not None:
                pca_projection = self.pca_projections.iloc[idx].astype(float).to_dict()
                umap_projection = self.umap_projections.iloc[idx].astype(float).to_dict()
            else:
                pca_projection = umap_projection = None

            # (2.4) Synthesize data into novel records
            rec = {
                "feature_type": self.feature_type,
                "feature_vector": feature_vector,
                "named_features": named_features,
                "pca_projection": pca_projection,
                "umap_projection": umap_projection
            }
            records.append(rec)
        
        return pd.DataFrame.from_records(records)


@dataclass
class DataInspectorMeta:
    """
    Dataclass providing scheme for data inspector metadata.
    """
    local_id: str
    name: str
    feature_type: FeatureType
    feature_names: List[str]
    hyperparams: Dict[str, Any]
