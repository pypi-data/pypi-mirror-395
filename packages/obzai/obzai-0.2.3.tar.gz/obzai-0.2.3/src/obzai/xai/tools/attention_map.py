# Obz AI - Copyright (C) 2025 Alethia XAI Sp. z o.o.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.


from typing import Optional, Callable
from torch import nn
import numpy as np
import torch


from obzai.xai.tools.xai_tool import BaseXAITool
from obzai.xai.postprocessing import Regionizer


class AttentionMapTool(BaseXAITool):
    """
    Prepares attention maps.
    Class expects model, which return attention weights, like transformers from huggingface package.
    So, model's forward method must handle keyword argument -> output_attention: bool
    """
    def __init__(self, 
                 model: nn.Module,
                 attention_layer_id: int = -1,
                 head: Optional[int] = None,
                 ommit_tokens: int = 1,
                 transform_fn: Optional[Callable] = None,
                 regionizer: Optional[Regionizer] = None
                 ):
        super().__init__(model, transform_fn, regionizer)

        self.xai_method_name = "Attention Map"

        self.attention_layer_id = attention_layer_id
        self.head = head
        self.ommit_tokens = ommit_tokens

        if not isinstance(self.attention_layer_id, int) or self.attention_layer_id < -1:
            raise ValueError(
                "Expected attention_layer_id to be integer: -1 or non-negative,"
                f" but got {self.attention_layer_id} instead."
                )
        if self.head is not None and (not isinstance(self.head, int) or self.head < 0):
            raise ValueError(
                "Expected head argument to be positive integer,"
                f" but got {self.head} instead."
            )
        if not isinstance(self.ommit_tokens, int) or self.ommit_tokens < 1:
            raise ValueError(
                "Expected ommit_tokens argument to be a positive integer,"
                f" but got {self.ommit_tokens} instead."
            )

    @property
    def requires_target(self) -> bool:
        return False

    def _check_if_images_are_square(self, batch: torch.Tensor):
        B, C, H, W = batch.shape
        if H != W:
            raise ValueError("Expected input images to be squares, "
                             f"but got images of height {H} and width {W}.")

    def _attribute(self, batch: torch.Tensor, target_idxs = None) -> torch.Tensor:
        """
        Method implements XAI maps preparation.

        Args:
            batch: Tensor of shape (B, C, H, W). Assumes that H==W.
            target_idx: None -> Not used by class agnostic method.
        
        Returns:
            xai_maps: Tensor of shape (B, 1, H, W)
        """
        _, _, img_H, img_W = batch.shape

        with torch.no_grad():
            preds, all_atts = self.model(batch, output_attentions=True)

        if self.attention_layer_id != -1 and self.attention_layer_id not in range(len(all_atts)):
            raise ValueError(f"There are only {len(all_atts)} layers! Please provide layer id: 0 - {len(all_atts)-1}.")

        layer_att = all_atts[self.attention_layer_id]
        B, n_heads, _, _ = layer_att.shape
        att_H = att_W = int(np.sqrt(layer_att.shape[-1] - 1)) # Attention map shape without a CLS token

        # Extracting attentions scores when CLS is used as query
        layer_att = layer_att[:, :, self.ommit_tokens-1, self.ommit_tokens:].reshape(B, n_heads, -1)

        layer_att = layer_att.reshape(B, n_heads, att_H, att_W)

        layer_att = torch.nn.functional.interpolate(
            layer_att, scale_factor=img_H//att_H, mode="nearest")
        
        if self.head:
            if self.head and self.head not in range(n_heads):
                raise ValueError(f"Provided head argument should be in range: 0-{n_heads-1}.")
            return layer_att[:, self.head, :, :].unsqueeze(dim=1).cpu()
        else:
            averaged_layer_att = torch.mean(layer_att, dim=1, keepdim=True).cpu()
            return averaged_layer_att