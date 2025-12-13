# Obz AI - Copyright (C) 2025 Alethia XAI Sp. z o.o.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

from typing import Union, TypedDict, Dict, Any, Literal, Protocol, Optional
from collections.abc import Sequence
from enum import Enum
import torch

# Base classes
from obzai.data_inspection.inspectors.base_data_inspector import _BaseDataInspector
from obzai.xai.tools.xai_tool import BaseXAITool

# Dataclasses
from obzai.xai.schemas.xai_results import XAIResults
from obzai.data_inspection.schemas.dataclasses import DataInspectionResults

# Typical inputs to the ObzAI Client __init__() method.
OneOrManyDataInspectors = Union[_BaseDataInspector, Sequence[_BaseDataInspector]]
OneOrManyXAITools = Union[BaseXAITool, Sequence[BaseXAITool]]

# Class specifying typing for dict returned by CacheService
class CachedResults(TypedDict, total=False):
    xai_results: list[XAIResults]
    data_inspection_results: list[DataInspectionResults]

# Inference Input
TensorOrSequenceOrDict = Union[
    torch.Tensor,
    Sequence[Union[torch.Tensor, Any]],
    Dict[str, Union[torch.Tensor, Any]]
]

# ML Tasks
class MLTask(str, Enum):
    """
    Enum type specifying available ML Tasks.
    """
    REGRESSION     = "REGRESSION"
    CLASSIFICATION = "CLASSIFICATION"
    TRANSLATION    = "TRANSLATION"
    SEGMENTATION   = "SEGMENTATION"
    

# Upload to storage fn signature
class UploadFnProtocol(Protocol):
    def __call__(self, object_bytes: bytes, ext: str, project_id: int, api_key: str) -> Optional[str]:
        ...