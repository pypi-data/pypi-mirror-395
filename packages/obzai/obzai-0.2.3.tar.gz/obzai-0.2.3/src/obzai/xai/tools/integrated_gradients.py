# Obz AI - Copyright (C) 2025 Alethia XAI Sp. z o.o.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.


from typing import List, Optional, Literal, Callable
from captum.attr import IntegratedGradients
import torch.nn as nn
import torch


from obzai.xai.postprocessing import Regionizer
from obzai.xai.tools.xai_tool import BaseXAITool


class IntegratedGradientsTool(BaseXAITool):
    def __init__(self, 
                 model: nn.Module,
                 n_steps: int = 50,
                 baseline: Optional[torch.Tensor|float] = None,
                 method: Literal["gausslegendre", "riemann_right", 
                                "riemann_left", "riemann_middle", 
                                "riemann_trapezoid"] = "gausslegendre",
                 internal_batch_size: Optional[int] = None,
                 transform_fn: Optional[Callable] = None,
                 regionizer: Optional[Regionizer] = None
                 ):
        super().__init__(model, transform_fn, regionizer)

        self.xai_method_name = "Integrated Gradients"

        self.n_steps = n_steps
        self.baseline = baseline
        self.method = method
        self.internal_batch_size = internal_batch_size

        if not isinstance(self.n_steps, int) or self.n_steps < 1:
            raise ValueError(
                "Expected n_steps argument to be positive integer,"
                f" but got {self.n_steps} instead."
                )
        if self.baseline is not None and (not torch.is_tensor(self.baseline) and not isinstance(self.baseline, float)):
            raise ValueError(
                "Expected baseline argument to be torch.Tensor or float,"
                f" but got {type(self.baseline)} instead."
                )
        if self.method not in ["gausslegendre", "riemann_right", "riemann_left", "riemann_middle", "riemann_trapezoid"]:
            raise ValueError(
                "Expected method argument to be one of: gausslegendre, riemann_right, riemann_left, riemann_middle, riemann_trapezoid"
                f", but got {self.method} instead."
                )
        if self.internal_batch_size is not None and (not isinstance(self.internal_batch_size, int) or self.internal_batch_size < 1):
            raise ValueError(
                "Expected internal_batch_size argument to be positive integer,"
                f" but got {self.internal_batch_size} instead."
                )

        self.ig = IntegratedGradients(model)   
    
    @property
    def requires_target(self) -> bool:
        return True

    def _attribute(self, batch: torch.Tensor, target_idxs: List[int]) -> torch.Tensor:
        """
        Computes Integrated Gradients maps for 2D image inputs.

        Args:
            batch (torch.Tensor): Input tensor of shape (B, C, H, W)
            target_idxs (List[int]): Target class indices of length B

        Returns:
            torch.Tensor: Attribution maps of shape (B, 1, H, W)
        """ 
        if batch.dim() != 4:
            raise ValueError(f"IntegratedGradientsTool only supports 2D inputs (B, C, H, W), but got shape {batch.shape}")

        batch.requires_grad_(True)
        attributions = self.ig.attribute(batch,
                                         baselines=self.baseline,
                                         target=target_idxs,
                                         n_steps=self.n_steps,
                                         method=self.method,
                                         internal_batch_size=self.internal_batch_size
                                         )
        batch.requires_grad_(False)

        attributions = torch.sum(attributions, dim=1, keepdim=True).detach().cpu()

        attributions = torch.clamp(
            attributions,
            min=torch.quantile(attributions, 0.01),
            max=torch.quantile(attributions, 0.99)
        )

        return attributions
    