# Obz AI - Copyright (C) 2025 Alethia XAI Sp. z o.o.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.


from captum.attr import Saliency, NoiseTunnel
from typing import List, Optional, Callable
import torch.nn as nn
import torch


from obzai.xai.postprocessing import Regionizer
from obzai.xai.tools.xai_tool import BaseXAITool


class SmoothGradTool(BaseXAITool):
    def __init__(self, 
                 model: nn.Module,
                 abs: bool = True,
                 noising_steps: int = 10,
                 internal_batch_size: Optional[int] = None,
                 transform_fn: Optional[Callable] = None,
                 regionizer: Optional[Regionizer] = None
                 ):
        super().__init__(model, transform_fn, regionizer)

        self.xai_method_name = "Smooth Grad"

        self.noising_steps = noising_steps
        self.internal_batch_size = internal_batch_size
        self.abs = abs

        if self.abs not in [True, False]:
            raise ValueError(
                "Expected abs argument to be True or False,"
                f" but got {self.abs} instead."
                )        
        if not isinstance(self.noising_steps, int) or self.noising_steps < 1:
            raise ValueError(
                "Expected noising_steps argument to be positive integer,"
                f" but got {self.noising_steps} instead."
                )
        if self.internal_batch_size is not None and (not isinstance(self.internal_batch_size, int) or self.internal_batch_size < 1):
            raise ValueError(
                "Expected internal_batch_size argument to be positive integer,"
                f" but got {self.internal_batch_size} instead"
                )
        
        self.saliency = NoiseTunnel(Saliency(model)) 

    @property
    def requires_target(self) -> bool:
        return True
    
    def _attribute(self, batch: torch.Tensor, target_idxs: List[int]) -> torch.Tensor:
        """
        Computes SmoothGrad maps for 2D image inputs.

        Args:
            batch (torch.Tensor): Input tensor of shape (B, C, H, W)
            target_idxs (List[int]): Target class indices of length B

        Returns:
            torch.Tensor: Attribution maps of shape (B, 1, H, W)
        """ 
        if batch.dim() != 4:
            raise ValueError(f"SmoothGradTool only supports 2D inputs (B, C, H, W), but got shape {batch.shape}")

        batch.requires_grad_(True)
        attributions = self.saliency.attribute(batch,
                                               abs=self.abs,
                                               nt_samples=self.noising_steps,
                                               nt_samples_batch_size=self.internal_batch_size,
                                               target=target_idxs)
        batch.requires_grad_(False)

        attributions = torch.sum(attributions, dim=1, keepdim=True).detach().cpu()
        attributions = torch.clamp(
            attributions,
            min=torch.quantile(attributions, 0.01),
            max=torch.quantile(attributions, 0.99)
        )

        return attributions  
