# Obz AI - Copyright (C) 2025 Alethia XAI Sp. z o.o.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.


from typing import List, Union, Optional, Tuple, Callable
from abc import ABC, abstractmethod
from torch import nn
import torch
import uuid


from obzai.xai.schemas.xai_results import XAIResults
from obzai.xai.postprocessing import Regionizer


class BaseXAITool(ABC):
    """
    Base class for all XAI tools. Unifies class-discriminative and class-agnostic tools.
    Handles transform, attribution, postprocessing, and result packaging.
    """
    def __init__(self,
                 model: nn.Module,
                 transform_fn: Optional[Callable] = None,
                 regionizer: Optional[Regionizer] = None
                 ):
        self.id = self._generate_unique_id()
        self.model = model.eval()
        self.transform_fn = transform_fn
        self.regionizer = regionizer
        self.xai_method_name = self.__class__.__name__

        if regionizer is not None and not isinstance(regionizer, Regionizer):
            raise ValueError(f"'regionizer' must be of type Regionizer, got {type(regionizer)}")

    def _generate_unique_id(self) -> str:
        """
        Generate a unique identifier that includes the class name and a UUID.
        Example: "VanillaCDAMTool_3fa85f64-5717-4562-b3fc-2c963f66afa6"
        """
        return f"{self.__class__.__name__}_{uuid.uuid4()}"

    def _batch_sanity_check(self, batch: torch.Tensor):
        if not isinstance(batch, torch.Tensor):
            raise ValueError(f"Expected input to be a torch.Tensor, got {type(batch)}")

        if batch.dim() not in [4, 5]:
            raise ValueError(f"Expected 4D or 5D tensor (B, C, H, W) or (B, C, D, H, W), got {batch.shape}")
    
    def _target_sanity_check(self,
                             batch: torch.Tensor,
                             target_idxs: Optional[Union[int, List[int]]]) -> Optional[List[int]]:
        
        if target_idxs is None:
            return None

        B = batch.size(0)

        if isinstance(target_idxs, int):
            return [target_idxs] * B
        elif isinstance(target_idxs, list):
            if len(target_idxs) != B:
                raise ValueError(f"Expected target_idxs of length {B}, got {len(target_idxs)}")
            return target_idxs
        else:
            raise ValueError(f"Expected int or list[int] for target_idxs, got {type(target_idxs)}")


    def _prepare_results(self,
                         xai_maps: torch.Tensor,
                         target_idxs: Optional[List[int]] = None
                         ) -> XAIResults:

        xai_maps_np = [xai_maps[i].cpu().numpy() for i in range(xai_maps.shape[0])]

        return XAIResults(
            tool_id=self.id,
            method_name=self.xai_method_name,
            target_idxs=target_idxs,
            xai_maps=xai_maps_np,
            postprocessing_method=self.regionizer.__class__.__name__ if self.regionizer else None
        )

    def explain(self,
                batch: torch.Tensor,
                target_idxs: Optional[Union[int, List[int]]] = None) -> XAIResults:
        """
        Main user-facing method for generating explanations.

        Args:
            batch (torch.Tensor): Input tensor of shape (B, C, H, W) or (B, C, D, H, W)
            target_idxs (int | list[int] | None): Optional class indices for class-discriminative tools.

        Returns:
            XAIResults: Structured explanation output.
        """
        self._batch_sanity_check(batch)
        target_idxs = self._target_sanity_check(batch, target_idxs)

        if self.requires_target and target_idxs is None:
            raise ValueError(f"{self.__class__.__name__} requires target_idxs but none were provided.")
        if not self.requires_target and target_idxs is not None:
            raise ValueError(f"{self.__class__.__name__} is class-agnostic and does not accept target_idxs.")

        if self.transform_fn:
            batch = self.transform_fn(batch)

        xai_maps = self._attribute(batch, target_idxs)

        if self.regionizer:
            xai_maps = self.regionizer.regionize(batch, xai_maps)

        return self._prepare_results(xai_maps, target_idxs)

    @property
    @abstractmethod
    def requires_target(self) -> bool:
        """        
        Indicates whether the tool requires target class indices (e.g., for classification tasks).
        Override in subclasses as needed.
        """

    @abstractmethod
    def _attribute(self,
                   batch: torch.Tensor,
                   target_idxs: Optional[List[int]]) -> torch.Tensor:
        """
        Abstract method to compute attributions.

        Args:
            batch (torch.Tensor): Input batch
            target_idxs (int | list[int] | None): Optional class indices

        Returns:
            torch.Tensor: Output attribution maps of shape (B, 1, H, W)
        """
        pass