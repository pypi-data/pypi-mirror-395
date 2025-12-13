# Obz AI - Copyright (C) 2025 Alethia XAI Sp. z o.o.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
import torch
import contextlib
import torch.nn as nn
from typing import Literal, Optional, Callable, Union, List

from obzai.xai.tools.xai_tool import BaseXAITool
from obzai.xai.postprocessing import Regionizer
from obzai.xai.schemas.xai_results import XAIResults


class GradCAMViTTool(BaseXAITool):
    """
    Grad-CAM implementation for Vision Transformers.
    """
    def __init__(
        self,
        model: nn.Module,
        gradient_type: Literal["from_logits", "from_probabilities"] = "from_logits",
        activation_type: Literal['sigmoid','softmax'] = 'softmax',
        ommit_tokens: int = 1,
        transform_fn: Optional[Callable] = None,
        regionizer: Optional[Regionizer] = None,
        apply_relu: bool = True
    ):
        super().__init__(model, transform_fn, regionizer)
        
        self.xai_method_name = "GradCAM (ViT)"

        self.gradient_type = gradient_type
        self.activation_type = activation_type
        self.ommit_tokens = ommit_tokens
        self.apply_relu = apply_relu

        if self.gradient_type not in ["from_logits", "from_probabilities"]:
            raise ValueError(
                "Expected gradient_type argument to be equal: 'from_logits' or 'from_probabilities',"
                f"but got {self.gradient_type} instead."
            ) 
        if self.gradient_type == "from_probabilities" and self.activation_type not in ["sigmoid", "softmax"]:
            raise ValueError(
                f"Expect activation type to be provided when gradient type is set to {self.gradient_type},"
                f"but got {self.activation_type} instead."
            )
        if self.ommit_tokens < 1:
            raise ValueError(
                "Expected ommit_tokens argument to be greater than 1,"
                f"but got {self.ommit_tokens} instead"
            )
    
        # placeholders for hooks
        self.feature_maps = None
        self.gradients = None
        self.hook_handles = []
        self.run_hook = False
        self.created_hooks = False
    
    @property
    def requires_target(self) -> bool:
        return True

    def _check_if_images_are_square(self, batch: torch.Tensor):
        B, C, H, W = batch.shape
        if H != W:
            raise ValueError("Expected input images to be squares, ",
                             f"but got images of height {H} and width {W}.")

    @contextlib.contextmanager
    def hook_manager(self):
        """Enable hooks for a single forward/backward pass."""
        self.run_hook = True
        try:
            yield
        finally:
            self.run_hook = False

    def create_hooks(self, layer_name: str):
        """
        Register backward and forward hooks that capture raw gradients.
        """
        if self.created_hooks:
            raise RuntimeError("Hooks already exists for GradCAMTool.")
        self.layer_name = layer_name
        layer = dict(self.model.named_modules())[layer_name]

        def forward_hook(module, inp, out):
            # capture features and reshape
            if self.run_hook:
                self.feature_maps = self._reshape_transform(out.detach())

        def backward_hook(module, grad_in, grad_out):
            # capture gradients of output
            if self.run_hook:
                self.gradients = self._reshape_transform(grad_out[0])

        # register hooks
        self.hook_handles.append(layer.register_forward_hook(forward_hook))
        self.hook_handles.append(layer.register_full_backward_hook(backward_hook))
        self.created_hooks = True

    def remove_hooks(self):
        """Remove any registered hooks."""
        for handle in self.hook_handles:
            handle.remove()
        self.hook_handles.clear()
        self.created_hooks = False

    def _reshape_transform(self, tensor: torch.Tensor) -> torch.Tensor:
        # tensor: [B, tokens, dim]
        B, N, D = tensor.size()
        # drop additional tokens
        tokens = tensor[:, self.ommit_tokens:, :]
        h = w = int(np.sqrt(tokens.size(1)))
        # reshape to [B, D, h, w]
        maps = tokens.reshape(B, h, w, D).permute(0, 3, 1, 2)
        return maps

    def _attribute(self, batch: torch.Tensor, target_idxs: List[int]) -> torch.Tensor:
        """
        Computes GradCAM maps for 2D image inputs.

        Args:
            batch (torch.Tensor): Input tensor of shape (B, C, H, W)
            target_idxs (List[int]): Target class indices of length B

        Returns:
            torch.Tensor: Attribution maps of shape (B, 1, H, W)
        """ 
        if not self.created_hooks:
            raise RuntimeError("create_hooks must be called before _prepare_xai_maps.")

        if self.transform_fn:
            batch = self.transform_fn(batch)

        B, C, H, W = batch.shape

        # Checks whether provided batch meet requirements
        self._batch_sanity_check(batch)
        self._check_if_images_are_square(batch)

        with self.hook_manager():
            outputs = self.model(batch)
            self.model.zero_grad()

            if self.gradient_type == "from_logits":
                outputs[range(B), target_idxs].sum().backward()
            else:
                if self.activation_type == "sigmoid":
                    probs = torch.sigmoid(outputs)
                else:
                    probs = torch.softmax(outputs, dim=1)
                probs[range(B), target_idxs].sum().backward()

        # compute weights: global average pooling of gradients
        grads = self.gradients  # [B, D, h, w]
        weights = torch.mean(grads.view(B, grads.size(1), -1), dim=2)  # [B, D]

        # weighted combination of feature maps
        feats = self.feature_maps  # [B, D, h, w]
        cams = (weights.unsqueeze(-1).unsqueeze(-1) * feats).sum(dim=1, keepdim=True)  # [B,1,h,w]
        if self.apply_relu:
            cams = nn.functional.relu(cams)

        # normalize and upscale
        cams = nn.functional.interpolate(cams, size=(H, W), mode='nearest')
        return cams.cpu()
