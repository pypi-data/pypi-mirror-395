# Obz AI - Copyright (C) 2025 Alethia XAI Sp. z o.o.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

from typing import List, Optional, Dict, Literal, Tuple, Any, cast
from io import BytesIO
import pandas as pd
import numpy as np
import httpx
import torch
import uuid

# API Configs
from obzai.client.configs.api_config import APIConfig

# Types & Dataclasses
from obzai.data_inspection.schemas.dataclasses import DataInspectionResults, ReferenceData
from obzai.client.schemas.types import TensorOrSequenceOrDict
from obzai.client.schemas.dataclasses import ProjectMeta
from obzai.xai.tools.xai_tool import XAIResults
from obzai.client.schemas.types import MLTask

# Custom exceptions
from obzai.client.schemas.exceptions import UploadServiceError

# ML Task Handlers
from obzai.client.services.utils.task_handlers import (handle_regression, 
                                                       handle_classification,
                                                       handle_translation,
                                                       handle_segmentation)
# Array encoding helpers
from obzai.client.services.utils.array_encoding import (encode_into_npygz,
                                                        encode_into_jpeg)


class _UploadService:
    """
    Service responsible for uploading both reference
    and inference data to the ObzAI Backend.
    """
    def __init__(
        self,
        client: httpx.Client
        ) -> None:
        """
        Constructs an instance of the UploadService class.
        """
        self.client = client


    def _serialize_array(
            self, arr: np.ndarray, trg_type: Literal["jpeg", "npy.gz"]
            ) -> bytes:
        """
        The private method serializes a provided array into a byte stream.

        Args:
            arr: A numpy.ndarray to serialize.
            trg_type: One from: "jpeg", "npy.gz"
        
        Returns:
            byte stream with the encoded array in proper format.
        
        Raises:
            ValueError when provided target type is wrong.
        """
        if trg_type == "jpeg":
            arr_bytes = encode_into_jpeg(arr)
        elif trg_type == "npy.gz":
            arr_bytes = encode_into_npygz(arr)
        else:
            raise ValueError(f"Provided target type: {trg_type} is wrong!")

        return arr_bytes
    

    def _upload_to_storage(
            self, 
            object_bytes: bytes, 
            ext: str,
            project_id: int,
            api_key: str
            ) -> Optional[str]:
        """
        The private method uploads a provided object into
        the ObzAI Object Storage.

        Args:
            object_bytes: bytes - A stream bytes of an object.
            ext: str - Desired extension of a file.
            project_id: int - ID of a project.
            api_key: str - API Key to get through a secured endpoint.
        
        Returns:
            A string containing key to the uploaded object.
        
        Raises:
            KeyError if response doesn't contain required key.
            NOTE! If upload fails, code skip that example.
        """
        files = {'file': (f"uploaded_file.{ext}", object_bytes)}
        payload = {'project_id': project_id}
        headers = {
            "Authorization": f"Bearer {api_key}"
            }
        
        try:
            response = self.client.post(
                APIConfig.get_url("upload_file"),
                files=files,
                data=payload,
                headers=headers,
                timeout=500
                )
            response.raise_for_status()
        except Exception:
            # TODO: Is there better solution to handle failed upload?
            return None
        
        data = response.json()
        if "key" in data:
            return data.get("key")
        else:
            raise KeyError("Response body should contain a key to the uploaded object!")


    def _process_prediction(
            self, 
            prediction: torch.Tensor,
            ml_task: MLTask,
            project_id: int,
            api_key: str
            ) -> Dict[str, Any]:
        """
        The private method processes various types of predictions.

        Args:
            prediction (torch.Tensor): Model output.
                Expected shape depends on the task:
                    - For regression: 1D tensor (K,), where K is the number of predicted variables.
                    - For classification: 1D tensor (K,), where K is the number of classes.
                    - For translation: 3D tensor (C, H, W) or 4D tensor (C, D, H, W).
                    - For segmentation: 3D tensor (C, H, W).
            ml_task: Enum type containing ML Task name.
            project_id: An integer corresponding to project's ID
            api_key: An API key needed to upload data through secured endpoint
        
        Returns:
            processed_pred - a dictionary containing either `pred_numeric` or `pred_key` values, 
                            depending on a ML Task.
        Raises:
            A ValueError when provided `ml_task_name` is not valid.
        """
        if ml_task == "REGRESSION":
            processed_pred = handle_regression(prediction=prediction)

        elif ml_task == "CLASSIFICATION":
            processed_pred = handle_classification(prediction=prediction)

        elif ml_task == "TRANSLATION":
            processed_pred = handle_translation(
                prediction=prediction, 
                project_id=project_id, 
                api_key=api_key,
                upload_fn=self._upload_to_storage
            ) 
        elif ml_task == "SEGMENTATION":
            processed_pred = handle_segmentation(
                prediction=prediction, 
                project_id=project_id, 
                api_key=api_key,
                upload_fn=self._upload_to_storage
            )
        else:
            raise ValueError("Provided ml_task is not valid.")
        
        return processed_pred


    def _handle_inputs(
            self,
            input_images: torch.Tensor,
            project_id: int,
            api_key: str
            ) -> List[Dict[str, Any]]:
        """
        Helper method parses input images, uploads the to the Object Storage
        and return JSON items.

        Args:
            input_images: A torch.Tensor of shape (B, C, H, W) or (B, C, D, H, W).
            project_id: The ID of target project.
            api_key: The valid API key required upload data through secured an secured endpoint.
        
        Returns:
            list of JSON items
        """
        input_items: List[Dict[str, Any]] = []

        for i, img in enumerate(input_images):
            input_id = f"{uuid.uuid4()}"
            img_bytes = self._serialize_array(img.cpu().numpy(), trg_type="jpeg")
            img_key = self._upload_to_storage(
                object_bytes=img_bytes,
                ext="jpeg",
                project_id=project_id,
                api_key=api_key
            )
            input_items.append({
                "input_id": input_id,
                "artifact": {
                    "art_type": "image", 
                    "key": img_key
                    } if img_key is not None else None
            })
        return input_items


    def _handle_predictions(
            self,
            predictions: torch.Tensor,
            input_items: List[Dict[str, Any]],
            project_meta: ProjectMeta,
            api_key: str
            ) -> List[Dict[str, Any]]:
        """
        Helper method parses predictions, if needed uploads data to the Object Storage
        and return appropriate JSON items.

        Args:
            predictions: A torch.Tensor of shape (B, C, H, W) or (B, C, D, H, W).
            input_items: A list of inserted input items.
            project_meta: The project metadata.
            api_key: A valid API key needed to upload data through secured endpoint.
            
        Returns:
            list of JSON items
        """
        prediction_items: List[Dict[str, Any]] = []

        B = len(input_items)
        for i in range(B):
            pred = predictions[i]
            processed_pred = self._process_prediction(
                prediction=pred,
                ml_task=project_meta.ml_task,
                project_id=project_meta.project_id,
                api_key=api_key
            )
            prediction_items.append({
                "input_id": input_items[i]["input_id"],
                "ml_task": project_meta.ml_task,
                "pred_numeric": processed_pred.get("pred_numeric", None),
                "pred_artifact": {
                    "art_type": "image", 
                    "key": processed_pred.get("pred_key")
                    } if "pred_key" in processed_pred else None
            })
        return prediction_items


    def _handle_xai_results(
            self,
            xai_results: List[XAIResults],
            input_items: List[Dict[str, Any]],
            project_id: int,
            api_key: str
            ) -> List[Dict[str, Any]]:
        """
        Helper method parses XAIResults, upload XAI maps to the 
        Object Storage and return appropriate JSON items.

        Args:
            xai_results: An optional list of XAIResults objects.      
            input_items: A list of inserted input items.
            project_id: An integer corresponding to the project ID.
            api_key: A valid API key needed to upload data through secured endpoint.
            
        Returns:
            list of JSON items
        """
        xai_items: List[Dict[str, Any]] = []
        
        B = len(input_items)
        for res in xai_results:
            for i in range(B):
                xai_map = res.xai_maps[i]
                xai_bytes = self._serialize_array(xai_map, trg_type="npy.gz")
                xai_key = self._upload_to_storage(
                    object_bytes=xai_bytes,
                    ext="npy.gz",
                    project_id=project_id,
                    api_key=api_key
                )
                xai_items.append({
                    "input_id": input_items[i]["input_id"],
                    "tool_id": res.tool_id,
                    "method_name": res.method_name,
                    "target_idx": res.target_idxs[i] if res.target_idxs is not None else None,
                    "postprocessing": res.postprocessing_method,
                    "artifact": {
                        "art_type": "heatmap", 
                        "key": xai_key
                        } if xai_key is not None else None
                })
        return xai_items


    def _handle_data_inspection_results(
            self,
            data_inspection_results: List[DataInspectionResults],
            input_items: List[Dict[str, Any]],
            data_inspector_local2remote_id: Dict[str, int]
            ) -> List[Dict[str, Any]]:
        """
        Helper method parses DataInspectionResults and return appropriate JSON items.

        Args:
            data_inspection_results: An optional list of DataInspectionResults objects.      
            input_items: A list of inserted input items.
            
        Returns:
            list of JSON items
        """
        data_inspection_items: List[Dict[str, Any]] = []
        
        B = len(input_items)
        for res in data_inspection_results:
            for i in range(B):
                features_data = res.extract_features_data_for_example(idx=i)
                data_inspection_items.append(
                    {
                        "input_id": input_items[i]["input_id"],
                        "data_inspector_id": data_inspector_local2remote_id[res.inspector_id],
                        "outlier_prediction": res.outliers[i],
                        "outlier_score": res.scores[i],
                        "features_data": features_data
                    }
                )
        return data_inspection_items


    def _aggregate_outlier_statuses(
            self,
            data_inspection_results: List[DataInspectionResults],
            batch_size: int,
            rule: Literal["AND", "OR"]
            ) -> List[Optional[bool]]:
        """
        Aggregates per-example outlier predictions coming from data inspectors.

        Args:
            data_inspection_results: Collection of inspector results for the batch.
            batch_size: Number of inputs in the batch.
            rule: Aggregation strategy; "AND" requires unanimity, "OR" requires any positive vote.

        Returns:
            List where each element corresponds to the final outlier status for a single input.
        """
        # (1) Validate Input
        try:
            normalized_rule = rule.upper()
        except AttributeError:
            raise UploadServiceError("Provided outlier aggregation rule has invalid type.")

        if normalized_rule not in ("AND", "OR"):
            raise UploadServiceError(f"Unsupported outlier aggregation rule: {rule}")

        # (2) Aggregate Outlier Statuses
        aggregated: List[Optional[bool]] = [None] * batch_size

        # (3) Validate Input
        for res in data_inspection_results:
            if len(res.outliers) != batch_size:
                raise ValueError("Data inspector results do not match batch size for outlier aggregation.")

        predictions_per_input: List[List[bool]] = [[] for _ in range(batch_size)]
        for res in data_inspection_results:
            for idx in range(batch_size):
                predictions_per_input[idx].append(bool(res.outliers[idx]))

        for idx, predictions in enumerate(predictions_per_input):
            if not predictions:
                continue
            if rule == "AND":
                aggregated[idx] = all(predictions)
            elif rule == "OR":
                aggregated[idx] = any(predictions)
            else:
                raise ValueError(f"Unsupported outlier aggregation rule: {rule}")

        return aggregated


    def _log_inference(
            self, payload: Dict[str, Any], api_key: str
            ) -> None:
        """
        The private method send inference-log request to the ObzAI Backend.

        Args:
            payload: (dict) A dictionary containing payload to sent.
            api_key: (str) An API key needed for authentication.
        
        Raises:
            In case of any error, re-raises it.
        """ 
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        url = APIConfig.get_url("log_inference")
        try:
            resp = self.client.post(
                url, json=payload, headers=headers, timeout=200
            )
            resp.raise_for_status()
        except Exception:
            raise 


    def upload_inference_log(
        self,
        api_key: str,
        project_meta: ProjectMeta,
        input_images: TensorOrSequenceOrDict,
        predictions: torch.Tensor,
        xai_results: Optional[List[XAIResults]] = None,
        data_inspection_results: Optional[List[DataInspectionResults]] = None,
        outlier_aggregation_rule: Literal["AND", "OR"] = "OR"
        ) -> None:
        """
        Uploads data to the ObzAI Backend.

        Args:
            api_key: A string containing API Key to send data through a secured endpoint.
            project_meta: An object containing project-related metadata, e.g. ID and ML Task ID.
            input_images: Batch of input images provided in the following forms:
                (i) a simple torch.Tensor of shape (B, C, H, W) or (B, C, D, H, W);
                (ii) a tuple[torch.Tensor, ...] or a list[torch.Tensor, ...] containing images at the first position;
                (iii) a dict[str, torch.Tensor | Any] containing images under key `images`.
            predictions (torch.Tensor): Model output predictions.
                Expected shape depends on the task:
                    - For regression: 2D tensor (B, K), where K is the number of predicted variables.
                    - For classification: 2D tensor (B, K), where K is the number of classes.
                    - For translation: 4D tensor (B, C, H, W) or 5D tensor (B, C, D, H, W).
                    - For segmentation: 4D tensor (B, 1, H, W) or 5D tensor (B, 1, D, H, W).
            xai_results (Optional[List[XAIResults]]): Optional list of XAIResults objects.
            data_inspection_results (Optional[List[DataInspectionResults]]): Optional list DataInspectionResults objects.
            outlier_aggregation_rule (Literal["AND", "OR"]): Strategy used to derive final outlier status per log item.
        
        Raises:
            UploadServiceError when uploading data fails for some reason.
        """
        # (1) Unwrap & Validate Input Batch
        try:
            input_images = self._unwrap_tensor_batch(input_images)
        except Exception as e:
            raise UploadServiceError("Provided batch of images has wrong format.") from e

        # (2) Handle Input Images
        try:
            log_items = self._handle_inputs(
                input_images=input_images,
                project_id=project_meta.project_id,
                api_key=api_key
            )
        except Exception as e:
            raise UploadServiceError("An error occured during input images processing.") from e

        # (3) Handle Predictions
        try:
            prediction_items = self._handle_predictions(
                predictions=predictions,
                input_items=log_items,
                project_meta=project_meta,
                api_key=api_key
            )
        except Exception as e:
            raise UploadServiceError("An error occured during predictions processing.") from e

        # (4) Handle XAI Results
        if xai_results is not None:
            try:
                xai_items = self._handle_xai_results(
                    xai_results=xai_results,
                    input_items=log_items,
                    project_id=project_meta.project_id,
                    api_key=api_key
                )
            except Exception as e:
                raise UploadServiceError("An error occured during processing XAI Results.") from e
        else:
            xai_items = []

        # (5) Handle Data Inspection Results and Outlier Statuses
        if data_inspection_results is not None and project_meta.data_inspector_local2remote_id is not None:
            try:
                data_inspection_items = self._handle_data_inspection_results(
                    data_inspection_results=data_inspection_results,
                    input_items=log_items,
                    data_inspector_local2remote_id=project_meta.data_inspector_local2remote_id
                )
            except Exception as e:
                raise UploadServiceError("An error occured during processing Data Inspection Results.") from e
        
            try:
                aggregated_outlier_statuses = self._aggregate_outlier_statuses(
                    data_inspection_results=data_inspection_results,
                    batch_size=len(log_items),
                    rule=outlier_aggregation_rule
                )
                for idx, outlier_status in enumerate(aggregated_outlier_statuses):
                    log_items[idx]["outlier_status"] = outlier_status
            except Exception as e:
                raise UploadServiceError("An error occured during processing Outlier Statuses.") from e
        else:
            data_inspection_items = []
            aggregated_outlier_statuses = []

        # (6) Build payload
        payload = {
            "project_id": project_meta.project_id,
            "log_items": log_items,
            "pred_items": prediction_items,
            "xai_items": xai_items,
            "data_inspection_items": data_inspection_items,
        }

        # 7) Send payload
        try:
            self._log_inference(payload, api_key=api_key)
        except Exception as e:
            raise UploadServiceError("An error occured during uploading inference log.") from e


    def _compress_dataframe(self, df: pd.DataFrame) -> bytes:
        """
        The private method converts a provided DataFrame into .csv file
        and compresses it into bytes stream.
  
        Args: 
            df (pandas DataFrame) - Dataframe to compress
        
        Returns:
            gzipped_csv: (bytes) - Compressed file with image features.
        """
        buf = BytesIO()
        df.to_parquet(path=buf, compression='gzip', index=False)
        compressed_df = buf.getvalue()
        return compressed_df


    def _log_reference(
            self, payload: Dict[str, Any], file: Dict[str, Tuple[str, bytes, str]], api_key: str
            ) -> None:
        """
        The private method send reference-log request to the ObzAI Backend.
    
        Args:
            payload: (dict) A dictionary containing payload to send.
            file: (dict) A dict containing file and it's meta.
            api_key: (str) An API key needed for authentication.
        
        Raises:
            In case of any error, re-raises it.
        """ 
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        url = APIConfig.get_url("log_reference")
        try:
            resp = self.client.post(
                url, headers=headers, data=payload, files=file, timeout=500
            )
            resp.raise_for_status()
        except Exception:
            raise 


    def upload_reference_log(
            self,
            api_key: str,
            reference_data: List[ReferenceData],
            data_inspector_local2remote_id: Dict[str, int]
            ) -> None:
        """
        Uploads reference data from Data Inspector into ObzAI platform.
        It retrieve reference  data from Data Inspectors and send it
        to the ObzAI Backend.

        Args:
            api_key: (string) A string with API key needed for authentication.
            reference_data: (List[ReferenceData]) A list of `ReferenceData` objects.
        
        Raises:
            UploadServiceError when uploading data fails for some reason.
        """

        # (1) Loop over ReferenceData objects
        for ref_data in reference_data:
            
            # (1.2) Retrieve data in a handy format
            try:
                df2upload = ref_data.prepare_data2upload()
            except Exception as e:
                raise UploadServiceError("An error occured during reference data preparation.") from e

            # (1.3) Convert dataframe into a parquet file and compress it
            gzipped_data = self._compress_dataframe(df2upload)
            file = {
                "reference_data": ("reference_data.parquet.gz", gzipped_data, "application/gzip")
            }
            # (1.4) Create a payload with data_inspector_id
            payload = {
                "data_inspector_id": data_inspector_local2remote_id[ref_data.inspector_id]
            }

            # (1.5) Upload data
            try:
                self._log_reference(
                    payload=payload, file=file, api_key=api_key
                )
            except Exception as e:
                raise UploadServiceError("An error occured during uploading reference data.") from e
        

    @staticmethod
    def _unwrap_tensor_batch(batch: TensorOrSequenceOrDict) -> torch.Tensor:
        """
        Extracts Tensor data from various batch formats: 
        Tensor, (Tensor, ...), {'images': Tensor, ...}.
        """
        if isinstance(batch, torch.Tensor):
            return batch
        if isinstance(batch, dict) and 'images' in batch:
            return batch['images']
        if isinstance(batch, tuple) or isinstance(batch, list):
            return batch[0]
        raise ValueError("Batch format not supported.")
