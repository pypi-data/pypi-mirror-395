# Obz AI - Copyright (C) 2025 Alethia XAI Sp. z o.o.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.


from typing import Literal, Union, List, Optional, Callable
import torch.nn as nn
import numpy as np
import contextlib
import torch


from obzai.xai.tools.xai_tool import BaseXAITool
from obzai.xai.postprocessing import Regionizer


class BaseCDAM(BaseXAITool):
    """Base class for all CDAM-based XAI Tools."""
    def __init__(
        self,
        model: nn.Module,
        gradient_type: Literal["from_logits", "from_probabilities"] = "from_logits",
        activation_type: Optional[Literal["sigmoid", "softmax"]] = None,
        ommit_tokens: int = 1,
        transform_fn: Optional[Callable] = None,
        regionizer: Optional[Regionizer] = None
    ):
        super().__init__(model, transform_fn, regionizer)

        self.gradient_type = gradient_type
        self.activation_type = activation_type
        self.ommit_tokens = ommit_tokens

        if self.gradient_type not in ["from_logits", "from_probabilities"]:
            raise ValueError(
                "Expected gradient_type argument to be equal: 'from_logits' or 'from_probabilities',",
                f"but got {self.gradient_type} instead."
            )
        if self.gradient_type == "from_probabilities" and self.activation_type not in ["sigmoid", "softmax"]:
            raise ValueError(
                f"Expected activation type to be provided when gradient type was set to {self.gradient_type},"
                f"but got {self.activation_type} instead."
            )
        if self.ommit_tokens < 1:
            raise ValueError(
                "Expected ommit_tokens argument to be greater than 1,"
                f"but got {self.ommit_tokens} instead"
            )

        self.gradients = {}
        self.activations = {}
        self.created_hooks = False
        self.run_hook = False
        self.layer_name = None
        self.gradient_hook = None
        self.activation_hook = None

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

    def remove_hooks(self):
        """Remove any registered hooks."""
        if self.created_hooks:
            self.gradient_hook.remove()
            self.activation_hook.remove()
            self.created_hooks = False
        else:
            raise RuntimeWarning("No hooks to remove.")

    def _compute_cdam(self, batch: torch.Tensor, target_idxs: List[int]) -> torch.Tensor:
        """
        This method performs core CDAM operation i.e. computes a dot product between
        tokens and corresponding gradients.

        Args:
            batch: Tensor of shape (B, C, H, W). It assumes that H == W.
            target_idxs: Integer or list of integers indicating target classes.
                        List is expected to have length equal to the batch size (B).
        
        Returns:
            cdam_map: Tensor of shape (B, 1, H, W)
        """
        if not self.created_hooks:
            raise RuntimeError("Hooks must be created before computing CDAM.")

        B, C, H, W = batch.shape

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

        tokens = self.activations[self.layer_name][:, self.ommit_tokens:, :]
        grads = self.gradients[self.layer_name][:, self.ommit_tokens:, :]

        # dot-product between tokens and gradients
        scores = torch.einsum('bij,bij->bi', tokens, grads)

        side = int(np.sqrt(grads.size(1)))
        maps = scores.reshape(B, side, side)
        # clamp extremes and upscale to input resolution
        maps = torch.clamp(
            maps,
            min=torch.quantile(maps, 0.01),
            max=torch.quantile(maps, 0.99)
        )
        return torch.nn.functional.interpolate(
            maps.unsqueeze(1), scale_factor=H/side, mode="nearest"
        ).cpu()


class VanillaCDAMTool(BaseCDAM):
    """Vanilla CDAM implementation"""
    def __init__(self,
                 model: nn.Module,
                 gradient_type: Literal["from_logits", "from_probabilities"] = "from_logits",
                 activation_type: Optional[Literal["sigmoid", "softmax"]] = None,
                 ommit_tokens: int = 1,
                 transform_fn: Optional[Callable] = None,
                 regionizer: Optional[Regionizer] = None
                 ):
        super().__init__(model=model, 
                         gradient_type=gradient_type, 
                         activation_type=activation_type,
                         ommit_tokens=ommit_tokens,
                         transform_fn=transform_fn,
                         regionizer=regionizer
                         )
        self.xai_method_name = "Vanilla CDAM"

    def create_hooks(self, layer_name: str):
        """Register forward & backward hooks that capture raw activations and gradients."""
        if self.created_hooks:
            raise RuntimeError("Hooks already exist.")
        self.layer_name = layer_name
        layer = dict(self.model.named_modules())[layer_name]

        def backward_hook(module, grad_input, grad_output):
            if self.run_hook:
                self.gradients[layer_name] = grad_output[0]

        def forward_hook(module, input, output):
            if self.run_hook:
                self.activations[layer_name] = output.detach()
            return output

        self.gradient_hook = layer.register_full_backward_hook(backward_hook)
        self.activation_hook = layer.register_forward_hook(forward_hook)
        self.created_hooks = True

    def _attribute(self, batch: torch.Tensor, target_idxs: Union[int, List[int]]) -> torch.Tensor:
        """
        Method provides XAI maps to a provided batch of images.

        Args:
            batch (torch.Tensor): Input tensor of shape (B, C, H, W)
            target_idxs (List[int]): Target class indices of length B

        Returns:
            torch.Tensor: Attribution maps of shape (B, 1, H, W)
        """
        xai_maps = self._compute_cdam(batch, target_idxs)
        return xai_maps


class SmoothCDAMTool(BaseCDAM):
    """Smooth CDAM: averages noisy passes."""
    def __init__(self,
                 model: nn.Module,
                 gradient_type: Literal["from_logits", "from_probabilities"] = "from_logits",
                 activation_type: Optional[Literal["sigmoid", "softmax"]] = None,
                 ommit_tokens: int = 1,
                 noise_level: float = 0.05, 
                 num_steps: int = 50,
                 transform_fn: Optional[Callable] = None,
                 regionizer: Optional[Regionizer] = None
                 ):
        super().__init__(model=model, 
                         gradient_type=gradient_type, 
                         activation_type=activation_type,
                         ommit_tokens=ommit_tokens,
                         transform_fn=transform_fn,
                         regionizer=regionizer)
  
        self.xai_method_name = "Smooth CDAM"

        self.noise_level = noise_level
        self.num_steps = num_steps

    def create_hooks(self, layer_name: str):
        """Register hooks, replacing forward with noise injection."""
        if self.created_hooks:
            raise RuntimeError("Hooks already exist.")
        self.layer_name = layer_name
        layer = dict(self.model.named_modules())[layer_name]

        def backward_hook(module, grad_input, grad_output):
            if self.run_hook:
                self.gradients[layer_name] = grad_output[0]

        def forward_hook(module, input, output):
            if self.run_hook:
                std = self.noise_level * (output.max() - output.min()).item()
                noise = torch.normal(0.0, std, output.shape, device=output.device)
                modified = (output + noise).requires_grad_()
                self.activations[layer_name] = modified.detach()
                return modified
            return output

        self.gradient_hook = layer.register_full_backward_hook(backward_hook)
        self.activation_hook = layer.register_forward_hook(forward_hook)
        self.created_hooks = True

    def _attribute(self, batch: torch.Tensor, target_idxs: Union[int, List[int]]) -> torch.Tensor:
        """
        Method provides XAI maps to a provided batch of images.

        Args:
            batch (torch.Tensor): Input tensor of shape (B, C, H, W)
            target_idxs (List[int]): Target class indices of length B

        Returns:
            torch.Tensor: Attribution maps of shape (B, 1, H, W)
        """
        maps = []

        for _ in range(self.num_steps):
            maps.append(self._compute_cdam(batch, target_idxs))

        xai_maps = torch.mean(torch.stack(maps), dim=0)

        return xai_maps


class IntegratedCDAMTool(BaseCDAM):
    """Integrated CDAM: interpolate baseline to real activations."""
    def __init__(self,
                 model: nn.Module,
                 gradient_type: Literal["from_logits", "from_probabilities"] = "from_logits",
                 activation_type: Optional[Literal["sigmoid", "softmax"]] = None,
                 ommit_tokens: int = 1,
                 noise_level: float = 0.05, 
                 num_steps: int = 50,
                 transform_fn: Optional[Callable] = None,
                 regionizer: Optional[Regionizer] = None
                 ):
        self.xai_method_name = "Integrated CDAM"
        
        self.noise_level = noise_level
        self.num_steps = num_steps
        super().__init__(model=model, 
                         gradient_type=gradient_type, 
                         activation_type=activation_type,
                         ommit_tokens=ommit_tokens,
                         transform_fn=transform_fn,
                         regionizer=regionizer
                         )

    def create_hooks(self, layer_name: str):
        """Register hooks, replacing forward with integration logic."""
        if self.created_hooks:
            raise RuntimeError("Hooks already exist.")
        self.layer_name = layer_name
        layer = dict(self.model.named_modules())[layer_name]

        def backward_hook(module, grad_input, grad_output):
            if self.run_hook:
                self.gradients[layer_name] = grad_output[0]

        def forward_hook(module, input, output):
            if self.run_hook:
                baseline = torch.zeros_like(output)
                std = self.noise_level * (output.max() - output.min()).item()
                noise = torch.normal(0.0, std, output.shape, device=output.device)
                alpha = self.iter_idx / self.num_steps
                modified = (baseline + alpha * (output - baseline) + noise).requires_grad_()
                self.activations[layer_name] = modified.detach()
                return modified
            return output

        self.gradient_hook = layer.register_full_backward_hook(backward_hook)
        self.activation_hook = layer.register_forward_hook(forward_hook)
        self.created_hooks = True

    def _attribute(self, batch: torch.Tensor, target_idxs: Union[int, List[int]]) -> torch.Tensor:
        """
        Method provides XAI maps to a provided batch of images.

        Args:
            batch (torch.Tensor): Input tensor of shape (B, C, H, W)
            target_idxs (List[int]): Target class indices of length B

        Returns:
            torch.Tensor: Attribution maps of shape (B, 1, H, W)
        """
        maps = []
        for i in range(self.num_steps + 1):
            self.iter_idx = i
            maps.append(self._compute_cdam(batch, target_idxs))

        xai_maps = torch.mean(torch.stack(maps), dim=0)

        return xai_maps