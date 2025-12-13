# Obz AI - Copyright (C) 2025 Alethia XAI Sp. z o.o.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.


from typing import Iterable, Dict, Any, List, Optional
from abc import ABC, abstractmethod
from io import BytesIO
import json
import pandas as pd
import joblib
import uuid
import os
import zipfile
from datetime import datetime, timezone

# Feature Pipeline
from obzai.data_inspection.feature_pipeline import FeaturePipeline

# OD Model base class (for typing)
from obzai.data_inspection.od_models.base_od_model import _BaseODModel
from obzai.data_inspection.od_models.base_od_model import OD_MODEL_REGISTRY

# Dataclasses, Types & Exceptions 
from obzai.data_inspection.schemas.dataclasses import (ImageFeatures, ReferenceData, 
                                                       DataInspectionResults, DataInspectorMeta)
from obzai.data_inspection.schemas.exceptions import (DataInspectorError, 
                                                      CheckpointError,
                                                      CheckpointVersionError,
                                                      CheckpointCorruptedError)
from obzai.data_inspection.schemas.types import TensorOrSequenceOrDict
from obzai.data_inspection.schemas.types import FeatureType


# To remove annoying, scikit-learn internal warnings related to deprecation.
import warnings
warnings.filterwarnings(
    "ignore",
    message=".*'force_all_finite' was renamed to 'ensure_all_finite'.*",
    category=FutureWarning,
    module="sklearn"
)


class _BaseDataInspector(ABC):
    """
    Base class implementing key methods of Data Inspector. 
    It provides robust skeleton for all inheriting variants of Data Inspectors.
    """
    _CHECKPOINT_VERSION = "1.0"
    def __init__(
        self,
        feature_pipeline: FeaturePipeline,
        od_model: _BaseODModel
        ) -> None:
        """
        Initialize an instance of Data Inspector.
        In particular generate instance-specific ID of Data Inspector
        and ensure that .obz directory is created at current working directory.
        
        Args:
            feature_pipeline: Instance of a feature pipeline
            od_model: Instance of an outlier detection model
        """
        # Feature Pipeline & Outlier Detection model
        self.feature_pipeline = feature_pipeline
        self.od_model = od_model
        
        # Helper attributes
        self._id = self._generate_unique_id()
        self._is_fitted = False

        # Setup Obz Directory
        self._setup_obz_directory()
    
    @property
    @abstractmethod
    def name(self) -> str:
        """
        Name of a Data Inspector.
        """
        ...

    @property
    @abstractmethod
    def logged_feature_type(self) -> FeatureType:
        """
        Type of logged feature type.
        """
        ...

    @property
    @abstractmethod
    def feature_names(self) -> Optional[List[str]]:
        """
        Returns the feature names for the feature pipeline.
        """
        ...

    @property
    @abstractmethod
    def hyperparams(self) -> Dict[str, Any]:
        """
        Hyperparameters of Data Inspector.
        """
        ...

    @property
    def id(self) -> str:
        """
        Returns the unique identifier for this inspector instance.
        """
        return self._id
    
    @property
    def metadata(self) -> DataInspectorMeta:
        """
        Returns metadata of that specific Data Inspector Instance.
        """
        return DataInspectorMeta(
            local_id=self._id,
            name=self.name,
            feature_type=self.logged_feature_type,
            feature_names=self.feature_names,
            hyperparams=self.hyperparams
        )

    def _generate_unique_id(self) -> str:
        """
        Generate a unique identifier that includes the class name and a UUID.
        """
        return f"{uuid.uuid4()}"

    def _setup_obz_directory(self) -> None:
        """
        Creates a directory containing Data Inspector related data.
        """
        self._root_dir = os.path.join(os.getcwd(), ".obz", self._id)
        os.makedirs(self._root_dir, exist_ok=True)

    def _save_reference_features(self, reference_features: ImageFeatures) -> None:
        """
        Saves reference features in the .obz directory located at current working directory.

        Args:
            reference_features: A dataclass containing raw, normalize and optionally projected image features.
        """
        # (1) Ensure that reference dir is located under .obz dir
        save_path = os.path.join(self._root_dir, "reference")
        os.makedirs(save_path, exist_ok=True)
        
        # (2) Save raw and normalized features
        raw_features_df = pd.DataFrame(reference_features.raw_features, columns=reference_features.feature_names)
        norm_features_df = pd.DataFrame(reference_features.norm_features, columns=reference_features.feature_names)

        raw_features_df.to_parquet(os.path.join(save_path, "ref_raw.parquet"), index=False)
        norm_features_df.to_parquet(os.path.join(save_path, "ref_norm.parquet"), index=False)

        # (3) Save 2D projections if available
        if reference_features.pca_projections is not None and reference_features.umap_projections is not None:
            pca_projections_df = pd.DataFrame(reference_features.pca_projections, columns=["x_coor", "y_coor"])
            umap_projections_df = pd.DataFrame(reference_features.umap_projections, columns=["x_coor", "y_coor"])

            pca_projections_df.to_parquet(os.path.join(save_path, "ref_pca_proj.parquet"), index=False)
            umap_projections_df.to_parquet(os.path.join(save_path, "ref_umap_proj.parquet"), index=False)

    def load_reference_data(self) -> ReferenceData:
        """
        Loads reference data stored under `reference` directory in .obz dir.

        Returns:
            ref_data: Objects containing loaded image features and if available correspoding 2D projections
        """
        # (1) Checks whether Data Inspector instance was already fitted. If not, reference data cannot be loaded.
        if not self._is_fitted:
            raise DataInspectorError("Inspector should be first fitted on reference data.")
        
        # (2) Path to directory storing reference features
        storage_path = os.path.join(self._root_dir, "reference")

        # (3) Try to load raw and normalized reference features
        try:
            raw_features = pd.read_parquet(os.path.join(storage_path, "ref_raw.parquet"))
            norm_features = pd.read_parquet(os.path.join(storage_path, "ref_norm.parquet"))
        except FileNotFoundError as e:
            raise DataInspectorError(f"Reference data not found: {e}")

        # (4) Try to load 2D projections of features if available
        try:
            pca_projections = pd.read_parquet(os.path.join(storage_path, "ref_pca_proj.parquet"))
            umap_projections = pd.read_parquet(os.path.join(storage_path, "ref_umap_proj.parquet"))
        except FileNotFoundError:
            pca_projections, umap_projections = None, None

        # (5) Return reference data (both features and projections) in a standardized way
        return ReferenceData(
            inspector_id     = self._id,
            feature_type     = self.logged_feature_type,
            raw_features     = raw_features,
            norm_features    = norm_features,
            pca_projections  = pca_projections,
            umap_projections = umap_projections
            )

    def fit(self, reference_images: Iterable[TensorOrSequenceOrDict]) -> None:
        """
        Extracts image features and fit outlier detection model.
        Saves extracted features in current working directory in the .obz/<Data Inspector ID> directory.

        Args:
            reference_images: Reference images might be provided as an Iterable returning:
                (i) a simple torch.Tensor of shape (B, C, H, W) or (B, C, D, H, W);
                (ii) a tuple[torch.Tensor, ...] or a list[torch.Tensor, ...] containing images at the first position;
                (iii) a dict[str, torch.Tensor | Any] containing images under key `images`.
        """
        # (1) Setup a feature pipeline
        ref_features = self.feature_pipeline.setup(reference_images)
        
        # (2) Save extracted reference features
        self._save_reference_features(ref_features)

        # (3) Fit OD model on normalized reference features
        self.od_model.fit(ref_features.norm_features)
        self._is_fitted = True

    def inspect(self, input_images: TensorOrSequenceOrDict) -> DataInspectionResults:
        """
        Extracts image features from a batch of input images and performs outlier detection.

        Args:
            input_images: Batch of input images provided in the following forms:
                (i) a simple torch.Tensor of shape (B, C, H, W) or (B, C, D, H, W);
                (ii) a tuple[torch.Tensor, ...] or a list[torch.Tensor, ...] containing images at the first position;
                (iii) a dict[str, torch.Tensor | Any] containing images under key `images`.

        Raises:
            DataInspectorError - Raises an error when any error occurs.
        
        Returns:
            DataInspectionResults - Object containing results of Data Inspections and extracted on the fly image features.
        """
        # (1) Checks whether Data Inspector instance was already fitted.
        if not self._is_fitted:
            raise DataInspectorError("Inspector should be first fitted on reference data.")
        
        # (2) Extracts image features
        try:
            image_features = self.feature_pipeline.run_pipeline(input_images)
        except Exception as e:
            raise DataInspectorError("Features extraction failed!") from e
        
        # (3) Performs outlier detection.
        try:
            outlier_detection_results = self.od_model.predict(image_features.norm_features)
        except Exception as e:
            raise DataInspectorError("Fitting an OD model failed!") from e  

        return DataInspectionResults(
            inspector_id     = self._id,
            outliers         = outlier_detection_results.outliers,
            scores           = outlier_detection_results.scores,
            feature_type     = self.logged_feature_type,
            feature_names    = image_features.feature_names,
            raw_features     = image_features.raw_features,
            norm_features    = image_features.norm_features,
            pca_projections  = image_features.pca_projections,
            umap_projections = image_features.umap_projections
            )

    def save_checkpoint(self, path: Optional[str] = None) -> str:
        """
        Saves fitted feature pipeline and OD model so they can be restored without re-fitting.

        Args:
            path: Optional path to store checkpoint archive. If not provided, defaults to
                  <cwd>/.obz/<inspector_id>/checkpoint.obz. If provided without .obz
                  suffix, the suffix is appended automatically.
        
        Returns:
            The path to the checkpoint archive.
        """
        if not self._is_fitted:
            raise DataInspectorError("Inspector must be fitted before saving a checkpoint.")

        checkpoint_path = path or os.path.join(self._root_dir, "checkpoint.obz")
        if not checkpoint_path.endswith(".obz"):
            checkpoint_path = f"{checkpoint_path}.obz"
        checkpoint_dir = os.path.dirname(checkpoint_path)
        if checkpoint_dir:
            os.makedirs(checkpoint_dir, exist_ok=True)

        # Serialize components
        pipeline_state = self.feature_pipeline.serialize_state()
        od_model_state = self.od_model.state_dict()

        manifest = {
            "checkpoint_version": self._CHECKPOINT_VERSION,
            "created_at": datetime.now(timezone.utc).isoformat() + "Z",
            "inspector": {
                "id": self._id,
                "class": self.__class__.__name__,
                "module": self.__class__.__module__,
                "name": self.name,
                "feature_type": self.logged_feature_type.value,
                "hyperparams": self.hyperparams
            }
        }

        # Write archive
        with zipfile.ZipFile(checkpoint_path, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("manifest.json", json.dumps(manifest, indent=2))

            pipeline_buf = BytesIO()
            joblib.dump(pipeline_state, pipeline_buf)
            pipeline_buf.seek(0)
            zf.writestr("pipeline.pkl", pipeline_buf.read())

            od_buf = BytesIO()
            joblib.dump(od_model_state, od_buf)
            od_buf.seek(0)
            zf.writestr("od_model.pkl", od_buf.read())

        return checkpoint_path

    @classmethod
    def load_checkpoint(cls, path: str, *, device: Optional[str] = None) -> "_BaseDataInspector":
        """
        Restores a fitted inspector from a checkpoint archive.

        Args:
            path: Path to checkpoint archive (.obz zip).
            device: Optional device hint forwarded to extractors (e.g., DeepExtractor).
        """
        if not os.path.exists(path):
            raise CheckpointCorruptedError("Checkpoint file does not exist.")

        try:
            with zipfile.ZipFile(path, mode="r") as zf:
                required = {"manifest.json", "pipeline.pkl", "od_model.pkl"}
                if not required.issubset(set(zf.namelist())):
                    raise CheckpointCorruptedError("Checkpoint archive is missing required files.")

                manifest = json.loads(zf.read("manifest.json"))
                pipeline_state = joblib.load(BytesIO(zf.read("pipeline.pkl")))
                od_model_state = joblib.load(BytesIO(zf.read("od_model.pkl")))
        except CheckpointCorruptedError:
            raise
        except Exception as exc:
            raise CheckpointCorruptedError("Failed to load checkpoint archive.") from exc

        inspector_meta = manifest.get("inspector", {})
        saved_cp_version = manifest.get("checkpoint_version")
        if saved_cp_version != cls._CHECKPOINT_VERSION:
            raise CheckpointVersionError(
                f"Incompatible checkpoint version: found {saved_cp_version}, expected {cls._CHECKPOINT_VERSION}."
            )
        saved_class = inspector_meta.get("class")
        if saved_class != cls.__name__:
            raise CheckpointError(f"Checkpoint was created by {saved_class}, cannot load into {cls.__name__}.")

        # Rebuild feature pipeline
        pipeline = FeaturePipeline.__new__(FeaturePipeline)
        pipeline.load_state(pipeline_state, device=device)

        # Rebuild OD model
        od_class_name = od_model_state.get("class")
        od_cls = OD_MODEL_REGISTRY.get(od_class_name)
        if od_cls is None:
            raise CheckpointCorruptedError(f"OD model class '{od_class_name}' not registered.")
        init_params = od_model_state.get("init_params", {})
        od_model = od_cls(**init_params)
        od_model.load_state_dict(od_model_state)

        # Instantiate inspector without running __init__
        instance = cls.__new__(cls)
        instance.feature_pipeline = pipeline
        instance.od_model = od_model
        instance._id = inspector_meta.get("id")
        if instance._id is None:
            raise CheckpointError("Checkpoint is missing inspector id.")

        instance._is_fitted = True
        instance._name = inspector_meta.get("name", cls.__name__)
        feature_type = inspector_meta.get("feature_type")
        if feature_type is None:
            raise CheckpointCorruptedError("Checkpoint is missing feature type.")
        instance._logged_feature_type = FeatureType(feature_type)
        instance._hyperparams = inspector_meta.get("hyperparams", {})

        # Recreate working directory for any downstream persistence.
        instance._setup_obz_directory()
        return instance
