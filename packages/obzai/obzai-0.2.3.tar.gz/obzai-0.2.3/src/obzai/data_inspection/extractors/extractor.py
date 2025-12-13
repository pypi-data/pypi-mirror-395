# Obz AI - Copyright (C) 2025 Alethia XAI Sp. z o.o.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

import importlib
import torchvision.transforms.v2.functional as F
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Sequence, Type
import numpy as np
import torch

# Registry for reconstructing extractors from lightweight configs.
EXTRACTOR_REGISTRY: Dict[str, Type["Extractor"]] = {}


def register_extractor(cls: Type["Extractor"]) -> Type["Extractor"]:
    """
    Registers an extractor class so it can be rebuilt from a serialized config.
    """
    EXTRACTOR_REGISTRY[cls.__name__] = cls
    return cls


class Extractor(ABC):
    def __init__(self):
        self.id: int = None
        self.name: str = None

    def _process_batch(self, 
                       batch: torch.Tensor,
                       image_size: int|Sequence[int] = 224,
                       ensure_grayscale: bool = False,
                       ensure_scale: bool=True) -> torch.Tensor:
        """
        Method accepts a torch.Tensor batch of images and processes it by resizing, optionaly grey scaling.
        Parameters:
            image: Input image as a torch.Tensor of shape (B, C, H, W) or (B, 1, H, W) if grayscale.
        """
        batch = batch.cpu()

        # Ensure proper DataType and scale:
        if ensure_scale:
            batch = F.to_dtype(batch, dtype=torch.float32, scale=True)

        # Resizing the image into a specified size
        if isinstance(image_size, int):
            image_size = [image_size, image_size]
        batch = F.resize(batch, size=image_size)
        
        # Convert RGB image to grayscale (if needed)
        if ensure_grayscale:
            F.rgb_to_grayscale(batch)
        
        return batch
    
    @abstractmethod
    def extract(self, image_batch: torch.Tensor) -> np.ndarray:
        """
        Method implements a custom loop over batch during features extraction.
        """
        pass

    @abstractmethod
    def get_config(self) -> Dict[str, Any]:
        """
        Returns a lightweight, serializable configuration for recreating the extractor.
        Heavy model weights must not be included.
        """
        raise NotImplementedError

    @classmethod
    def from_config(cls, config: Dict[str, Any], device: Optional[str] = None) -> "Extractor":
        """
        Rebuilds a registered extractor from its config.

        Args:
            config: Serialized extractor configuration.
            device: Optional device hint (used by deep extractors).
        """
        class_name = config.get("class")
        module_path = config.get("module")
        if class_name is None or module_path is None:
            raise ValueError("Extractor config must contain 'class' and 'module' keys.")

        extractor_cls = EXTRACTOR_REGISTRY.get(class_name)
        if extractor_cls is None:
            # Best effort dynamic import if not yet registered.
            importlib.import_module(module_path)
            extractor_cls = EXTRACTOR_REGISTRY.get(class_name)

        if extractor_cls is None:
            raise ValueError(f"Extractor class '{class_name}' is not registered.")

        if hasattr(extractor_cls, "_from_config"):
            return extractor_cls._from_config(config, device=device)  # type: ignore[attr-defined]

        if extractor_cls is not cls and extractor_cls.from_config is not Extractor.from_config:
            return extractor_cls.from_config(config, device=device)  # type: ignore[call-arg]

        raise ValueError(f"Extractor class '{class_name}' does not support config-based reconstruction.")
