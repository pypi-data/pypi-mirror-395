# Obz AI - Copyright (C) 2025 Alethia XAI Sp. z o.o.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.


from captum.attr import Saliency
from typing import List, Optional, Callable, List
import torch.nn as nn
import torch


from obzai.xai.tools.xai_tool import BaseXAITool
from obzai.xai.postprocessing import Regionizer


class SaliencyTool(BaseXAITool):
    def __init__(self, 
                 model: nn.Module,
                 abs: bool = True,
                 transform_fn: Optional[Callable] = None,
                 regionizer: Optional[Regionizer] = None):
        super().__init__(model, transform_fn, regionizer)

        self.xai_method_name = "Saliency"
        self.abs = abs

        if self.abs not in [True, False]:
            raise ValueError(f"Expected abs argument to be True or False, but got {self.abs} instead.")

        self.saliency = Saliency(model)

    @property
    def requires_target(self) -> bool:
        return True

    def _attribute(self, batch: torch.Tensor, target_idxs: List[int]) -> torch.Tensor:
        """
        Computes saliency maps for 2D image inputs.

        Args:
            batch (torch.Tensor): Input tensor of shape (B, C, H, W)
            target_idxs (List[int]): Target class indices of length B

        Returns:
            torch.Tensor: Attribution maps of shape (B, 1, H, W)
        """
        if batch.dim() != 4:
            raise ValueError(f"SaliencyTool only supports 2D inputs (B, C, H, W), but got shape {batch.shape}")

        batch.requires_grad_(True)
        attributions = self.saliency.attribute(batch, target=target_idxs, abs=self.abs)
        batch.requires_grad_(False)

        attributions = torch.sum(attributions, dim=1, keepdim=True).detach().cpu()

        attributions = torch.clamp(
            attributions,
            min=torch.quantile(attributions, 0.01),
            max=torch.quantile(attributions, 0.99)
        )

        return attributions

    