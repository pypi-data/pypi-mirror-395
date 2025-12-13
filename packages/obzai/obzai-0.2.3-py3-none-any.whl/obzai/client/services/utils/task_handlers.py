# Obz AI - Copyright (C) 2025 Alethia XAI Sp. z o.o.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.


from typing import List, Dict, Any, Callable, Optional
import torch

from obzai.client.services.utils.array_encoding import (encode_into_jpeg, 
                                                        encode_into_npygz)
from obzai.client.schemas.types import UploadFnProtocol


# --- Task Handlers ---
def handle_regression(prediction: torch.Tensor) -> Dict[str, List[float]]:
    """
    Transform a typical model output for the **regression task**, 
    into a desired serializable list of values.

    Args:
        prediction: a torch.Tensor of shape (K,) where K is the number of predicted variables.
    
    Returns:
        A dictionary storing list of predicted floats under the `pred_numeric` key.
        
    Raises:
        RuntimeError when assumptions about prediction argument are not met.
    """

    if not isinstance(prediction, torch.Tensor):
        raise RuntimeError("Predictions must be a torch.Tensor for the regression task.")
    
    if prediction.ndim != 1:
        raise RuntimeError(f"Regression predictions must be 1D (K,). Got {prediction.shape}")
    
    return {"pred_numeric": prediction.tolist()}


def handle_classification(prediction: torch.Tensor) -> Dict[str, List[float]]:
    """
    Transform a typical model output for the **classiification task**, 
    into a desired serializable list of values.

    Args:
        prediction: a torch.Tensor of shape (K,) where K is the number of predicted class probabilities.
    
    Returns:
        A dictionary storing list of predicted floats under the `pred_numeric` key.
        
    Raises:
        RuntimeError when assumptions about prediction argument are not met.
    """

    if not isinstance(prediction, torch.Tensor):
        raise RuntimeError("Predictions must be a torch.Tensor for the classification task.")
    
    if prediction.ndim != 1:
        raise RuntimeError(f"Classification predictions must be 1D (K,). Got {prediction.shape}")
    
    return {"pred_numeric": prediction.tolist()}


def handle_translation(
        prediction: torch.Tensor, 
        project_id: int,
        api_key: str,
        upload_fn: UploadFnProtocol
        ) -> Dict[str, Optional[str]]:
    """
    Handle a typical model output for the **translation task**.
    Translated image is serrialized and uploaded to the Object Storage.

    Args:
        prediction: a torch.Tensor of shape either (C, H, W) or (C, D, H, W).
        project_id: an integer corresponding to the project ID
        api_key: API key needed for uploading image through secured endpoint
        upload_fn: A function handling an upload.
    
    Returns:
        A dictionary key to the uploaded image under the `pred_key` key.
        
    Raises:
        RuntimeError when assumptions about prediction argument are not met.
    """

    if not isinstance(prediction, torch.Tensor):
        raise RuntimeError("Predictions must be a torch.Tensor for translation.")
    
    if prediction.ndim == 3:
        image_bytes = encode_into_jpeg(prediction.cpu().numpy())
        ext = "jpeg"
    elif prediction.ndim == 4:
        image_bytes = encode_into_npygz(prediction.cpu().numpy())
        ext = "npy.gz"
    else:
        raise RuntimeError(f"Translation predictions must be either 3D (C, H, W) or 4D (C, D, H, W). Got {prediction.shape}")
    
    pred_key = upload_fn(image_bytes, ext, project_id, api_key)
    return {"pred_key": pred_key}


def handle_segmentation(
        prediction: torch.Tensor, 
        project_id: int,
        api_key: str,
        upload_fn: UploadFnProtocol
        ) -> Dict[str, Optional[str]]:
    """
    Handle a typical model output for the **segmentation task**.
    Segmentaion mask is serrialized and uploaded to the Object Storage.

    Args:
        prediction: a torch.Tensor of shape either (1, H, W) or (1, D, H, W).
        project_id: an integer corresponding to the project ID
        api_key: API key needed for uploading image through secured endpoint
        upload_fn: A function handling an upload.
    
    Returns:
        A dictionary key to the uploaded mask under the `pred_key` key.
        
    Raises:
        RuntimeError when assumptions about prediction argument are not met.
    """
    
    if not isinstance(prediction, torch.Tensor):
        raise RuntimeError("Predictions must be a torch.Tensor for segmentation.")
    
    if prediction.ndim not in (3, 4):
        raise RuntimeError(f"Segmentation predictions must be 3D (1, H, W) or 4D (1, D, H, W). Got {prediction.shape}")
    
    image_bytes = encode_into_npygz(prediction.cpu().numpy())
    ext = "npy.gz"

    pred_key = upload_fn(image_bytes, ext, project_id, api_key)
    return {"pred_key": pred_key}