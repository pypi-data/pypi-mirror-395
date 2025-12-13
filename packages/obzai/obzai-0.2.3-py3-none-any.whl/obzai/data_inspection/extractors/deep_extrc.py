# Obz AI - Copyright (C) 2025 Alethia XAI Sp. z o.o.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

from transformers import AutoImageProcessor, AutoModel
import numpy as np
import torch

from obzai.data_inspection.extractors.extractor import Extractor, register_extractor


class DeepExtractor(Extractor):
    """
    DeepExtractor enables using Huggingface vision models as feature extractors.
    It handle generic models which are available through HuggingFace AutoModel API.
    """
    def __init__(self, model_path: str = "openai/clip-vit-base-patch32"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.img_processor = AutoImageProcessor.from_pretrained(model_path, use_fast=True)
        model = AutoModel.from_pretrained(model_path)
        self.model_path = model_path
        # Use only the vision encoder if present
        self.model = getattr(model, "vision_model", model)
        self.model.to(self.device)
        self.model.eval()
        # Infer feature size
        hidden_size = getattr(self.model.config, "hidden_size")
        self.feature_names = [f"feat_{i}" for i in range(hidden_size)]
        self.id = 2
        self.name = self.__class__.__name__

    def extract(self, image_batch: torch.Tensor, do_rescale: bool = False) -> np.ndarray:
        """
        Extracts features during production.
        """
        image_batch = self.img_processor(images=image_batch, return_tensors="pt", do_rescale=do_rescale)
        with torch.no_grad():
            outputs = self.model(image_batch['pixel_values'].to(self.device))
        # Try to use pooler_output, fallback to last_hidden_state
        if hasattr(outputs, "pooler_output"):
            feats = outputs.pooler_output
        else:
            feats = outputs.last_hidden_state.mean(dim=1)
        return feats.detach().cpu().numpy()

    def get_config(self):
        return {
            "class": self.__class__.__name__,
            "module": self.__module__,
            "model_path": self.model_path
        }

    @classmethod
    def _from_config(cls, config, device=None):
        model_path = config.get("model_path", "openai/clip-vit-base-patch32")
        instance = cls(model_path=model_path)
        if device is not None:
            instance.device = device
            instance.model.to(device)
        return instance


# Register in the extractor registry for checkpoint reconstruction.
register_extractor(DeepExtractor)
