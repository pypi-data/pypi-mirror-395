# Obz AI - Copyright (C) 2025 Alethia XAI Sp. z o.o.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

from typing import (Any, Dict, Iterable, List, Optional, Union)
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from collections.abc import Sequence
from umap import UMAP
from tqdm import tqdm
import numpy as np
import torch

from obzai.data_inspection.extractors.extractor import Extractor
from obzai.data_inspection.schemas.dataclasses import ImageFeatures
from obzai.data_inspection.schemas.exceptions import FeaturePipelineError
from obzai.data_inspection.schemas.types import TensorOrSequenceOrDict


class FeaturePipeline:
    """
    Handles image features extraction and features normalization.
    """
    def __init__(
            self, extractors: Union[Extractor, Sequence[Extractor]], project_features: bool = False) -> None:
        """
        Initialize an instance of FeaturePipeline class.

        Args:
            extractors: a single instance or sequence of extractor objects is required.
            project_features: a boolean flag controlling whether features are projected or not
        
        Raises:
            FeaturePipelineError: When provided extractors don't meet requirements.
        """
        self.project_features = project_features
        self.extractors = self._extractors_sanity_check(extractors)

        self._extractor_ids = [extrc.id for extrc in self.extractors]
        self.scalers: Dict[int, StandardScaler] = {}

        if project_features:
            self._pca_transform = PCA(n_components=2)
            self._umap_transform = UMAP(n_components=2)
        else:
            self._pca_transform, self._umap_transform = None, None

        self._feature_names: List[str] = []
        for extrc in self.extractors:
            self._feature_names.extend(extrc.feature_names)
        
        self._fitted = False

    @property
    def feature_names(self) -> List[str]:
        """
        Returns the feature names for the feature pipeline.
        """
        return self._feature_names

    def _extract_image_features(self, image_batches: Iterable[TensorOrSequenceOrDict], show_progress: bool = False) -> Dict[int, np.ndarray]:
        """
        Extracts raw image features. Input iterable is expected to yield batches containing valid tensor data.

        Args:
            image_batches: Iterable yielding TensorOrSequenceOrDict batches.
        
        Returns:
            Dict[int, np.ndarray] - Dictionary storing per-extractor image features.
        """
        # (1) Create empty dictionaries to store batched, per-extractor image features and final results.
        ## Temp storage of per-batch results
        temp_extracted_feats: Dict[int, List[np.ndarray]] = {extrc.id: [] for extrc in self.extractors}
        ## Final storage with stacked results
        extracted_feats: Dict[int, np.ndarray] = {}

        # (2) Extract image features with Extractor objects.
        iterator = tqdm(
            image_batches, 
            desc="Extracting image features ..."
            ) if show_progress else image_batches
        for image_batch in iterator:
            unwrapped_batch = self._unwrap_tensor_batch(image_batch)
            for extrc in self.extractors:
                feats = extrc.extract(unwrapped_batch)
                temp_extracted_feats[extrc.id].append(feats)
        
        # (3) Concatenate batched image features into a one array.
        for key in self._extractor_ids:
            try:
                extracted_feats[key] = np.concatenate(temp_extracted_feats[key], axis=0)
            except Exception as e:
                raise FeaturePipelineError(f"Error during concatenating batches of image features: {e}")
        
        # (4) Return dictionary containing per-extractor raw image features.
        return extracted_feats
    
    def setup(self, reference_images: Iterable[TensorOrSequenceOrDict]) -> ImageFeatures:
        """
        Setups feature pipeline by extracting reference features with features extractors passed in __init__().
        Extracted reference features are used to fit z-score normalization protocol.

        Args:
            reference_images: Iterable yielding TensorOrSequenceOrDict batches
        
        Returns:
            ref_features: An object storing both raw and normalized image features.
        """
        # (1) Sanity Check of an input
        validated_iter = self._batches_sanity_check(reference_images)

        # (2) Iterate over batches and extract raw image features
        raw_extracted_feats = self._extract_image_features(validated_iter, show_progress=True)
        
        # (3) Fit feature scalers on extracted image features
        raw_features_lst: List[np.ndarray] = []
        norm_features_lst: List[np.ndarray] = []
        for extrc_id in self._extractor_ids:
            raw_feat_array = raw_extracted_feats[extrc_id]
            scaler = StandardScaler()
            norm_feat_array = scaler.fit_transform(raw_feat_array)
            self.scalers[extrc_id] = scaler
            raw_features_lst.append(raw_feat_array)
            norm_features_lst.append(norm_feat_array)

        # (4) Concatenate horizontally image features extracted from different extractors
        raw_features_arr: np.ndarray = np.concatenate(raw_features_lst, axis=1)
        norm_features_arr: np.ndarray = np.concatenate(norm_features_lst, axis=1)

        # (5) Optionally, fit feature projectors
        if self.project_features:
            pca_ref_projections = self._pca_transform.fit_transform(norm_features_arr)
            umap_ref_projections = self._umap_transform.fit_transform(norm_features_arr)
        else:
            pca_ref_projections, umap_ref_projections = None, None

        # (6) Mark feature pipeline instance as fitted
        self._fitted = True

        # (7) Return extracted reference data representation in a standardized way
        return ImageFeatures(
            feature_names    = self._feature_names,
            raw_features     = raw_features_arr,
            norm_features    = norm_features_arr,
            pca_projections  = pca_ref_projections,
            umap_projections = umap_ref_projections
            )

    def run_pipeline(self, input_images: TensorOrSequenceOrDict) -> ImageFeatures:
        """
        Run a pipeline, extracts image features and normalize them utilizing already fitted standard scalers.
        """
        # (1) Check whether feature pipeline instance was already fitted
        if not self._fitted:
            raise FeaturePipelineError("The .setup() method must be called before the .run_pipeline() method.")

        # (2) Feature extraction is batch-oriented. Create dummy iterable yielding a one batch
        single_iter = (input_images, )

        # (3) Sanity Check of an iterable
        validated_iter = self._batches_sanity_check(single_iter)
        
        # (4) Extract raw image features from that one batch
        raw_extracted_feats = self._extract_image_features(validated_iter)

        # (5) Normalize image features
        raw_features_lst: List[np.ndarray] = []
        norm_features_lst: List[np.ndarray] = []
        for extrc_id in self._extractor_ids:
            scaler = self.scalers.get(extrc_id)
            raw_feat_array = raw_extracted_feats[extrc_id]
            norm_feat_array = scaler.transform(raw_feat_array)
            raw_features_lst.append(raw_feat_array)
            norm_features_lst.append(norm_feat_array)

        # (6) Concatenate per-extractor results
        raw_features_arr = np.concatenate(raw_features_lst, axis=1)
        norm_features_arr = np.concatenate(norm_features_lst, axis=1)

        # (7) Optionally, project image features
        if self.project_features:
            pca_projections = self._pca_transform.transform(norm_features_arr)
            umap_projections = self._umap_transform.transform(norm_features_arr)
        else:
            pca_projections, umap_projections = None, None

        # (8) Return raw and normalized image features in a standarized way
        return ImageFeatures(
            feature_names    = self._feature_names,
            raw_features     = raw_features_arr,
            norm_features    = norm_features_arr,
            pca_projections  = pca_projections,
            umap_projections = umap_projections
            )

    def serialize_state(self) -> Dict[str, Any]:
        """
        Serializes fitted feature pipeline components required for inference.
        """
        if not self._fitted:
            raise FeaturePipelineError("Feature pipeline must be fitted before serialization.")

        extractor_configs = [extrc.get_config() for extrc in self.extractors]
        return {
            "project_features": self.project_features,
            "feature_names": self._feature_names,
            "extractor_configs": extractor_configs,
            "_extractor_ids": self._extractor_ids,
            "scalers": self.scalers,
            "pca_transform": self._pca_transform,
            "umap_transform": self._umap_transform
        }

    def load_state(self, state: Dict[str, Any], device: Optional[str] = None) -> None:
        """
        Restores feature pipeline internals from a serialized state.
        """
        extractor_configs = state.get("extractor_configs")
        if extractor_configs is None:
            raise FeaturePipelineError("Serialized state missing extractor configurations.")

        self.extractors = [Extractor.from_config(cfg, device=device) for cfg in extractor_configs]
        self._extractor_ids = state.get("_extractor_ids", [extrc.id for extrc in self.extractors])
        self._feature_names = state.get("feature_names", [])
        self.project_features = bool(state.get("project_features", False))
        self.scalers = state.get("scalers", {})
        self._pca_transform = state.get("pca_transform")
        self._umap_transform = state.get("umap_transform")
        self._fitted = True

    @staticmethod
    def _unwrap_tensor_batch(batch: TensorOrSequenceOrDict) -> torch.Tensor:
        """
        Extracts Tensor data from various batch formats: Tensor, (Tensor, _), {'images': Tensor, ...}.
        """
        if isinstance(batch, torch.Tensor):
            return batch
        if isinstance(batch, dict) and 'images' in batch:
            return batch['images']
        if isinstance(batch, tuple) or isinstance(batch, list):
            return batch[0]
        raise ValueError("Batch format not supported for feature extraction.")

    @staticmethod
    def _extractors_sanity_check(extractors: Extractor | Sequence[Extractor]) -> Sequence[Extractor]:
        """
        Performs a sanity check on a provided sequence of Extractor objects or single extractor.
        In particular, each provided object must be an instance of Extractor class and has the following attributes:
            * .id -> ID of an Extractor (integer)
            * .feature_names -> Names of a features (list of names corresponding to fields in feature vectors)
        
        Args:
            extractors: A single Extractor object or sequence of Extractor objects.
        
        Raises:
            FeaturePipelineError: When provided objects don't meet requirements.
        """
        # (1) Check whether extractors is not a sequence
        if not isinstance(extractors, tuple) and not isinstance(extractors, list):
            # (1.1) Check whether is a single Extractor object, if True then wrap it into a single-element list.
            if isinstance(extractors, Extractor):
                extractors = [extractors]
            # (1.2) Not a tuple/list, nor Extractor? Raise error.
            else:
                raise FeaturePipelineError("Provided extractors is expected to be a sequence of Extractor objects or a single Extractor object")
        
        # (2) If tuple or list, iterate over object and check whether each is Extractor and has required attributes.
        for extrc in extractors:
            if not isinstance(extrc, Extractor):
                raise FeaturePipelineError("Each object in a sequence is expected to be an instance of Extractor class.")
            
            if not hasattr(extrc, "id") or not hasattr(extrc, "feature_names"):
                raise FeaturePipelineError("Each object in a sequence is expected to have .id and .feature_names attributes.")
        
        # (3) Return validated sequence of Extractors.
        return extractors

    @staticmethod
    def _batches_sanity_check(input_batches: Iterable[TensorOrSequenceOrDict]) -> Iterable[TensorOrSequenceOrDict]:
        """
        Checks whether input batches are correctly provided as an iterable returning `TensorOrSequenceOrDict` batches.

        Args:
            input_batches: An object to be checked.
        
        Raises:
            FeaturePipelineError: If provided input abtches do not meet requirements.

        Returns:
            validated_iter: A validated iterable which can be used in further processing.
        """
        def is_valid_tensor(t: Any) -> bool:
            return isinstance(t, torch.Tensor) and t.ndim in (4, 5)

        if not hasattr(input_batches, "__iter__"):
            raise FeaturePipelineError("Input batches must be an iterable.")

        iterator = iter(input_batches)
        try:
            first = next(iterator)
        except StopIteration:
            raise FeaturePipelineError("Provided iterable is empty.")
        except Exception as exc:
            raise FeaturePipelineError(f"Provided input is not a valid iterable: {exc}")

        # Validate the first element
        if isinstance(first, torch.Tensor):
            if not is_valid_tensor(first):
                raise FeaturePipelineError("A torch.Tensor was provided, but with invalid shape (expected 4 or 5 dimensions).")
        elif isinstance(first, tuple) or isinstance(first, list):
            if len(first) == 0 or not is_valid_tensor(first[0]):
                raise FeaturePipelineError("A sequence provided as batch is empty or first element not a valid torch.Tensor.")
        elif isinstance(first, dict):
            images_tensor = first.get("images", None)
            if not is_valid_tensor(images_tensor):
                raise FeaturePipelineError("Dict provided, but 'images' key does not contain a valid torch.Tensor.")
        else:
            raise FeaturePipelineError("Iterable must yield torch.Tensor, tuple, or dict with 'images' key containing a valid tensor.")

        # If validation was succesful, return unchanged iterable
        return input_batches
