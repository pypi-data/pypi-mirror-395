# Obz AI - Copyright (C) 2025 Alethia XAI Sp. z o.o.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

from skimage.morphology import dilation, disk
from typing import Optional, Callable, Tuple
from skimage.transform import resize
from skimage import segmentation
import torch


class Regionizer:
    """
    Class is responsible for XAI map post-processing according to a procedure 
    described in XRAI - Better Attributions Through Regions (https://arxiv.org/abs/1906.02825)
    """
    def __init__(self, 
                 seg_dilation: int = 3, 
                 area_perc_th: float = 1.0, 
                 min_pixel_diff: int = 50, 
                 approximate: bool = False
                 ):
        """
        Construct a Regionizer object enabling XAI maps postprocessing
        according to XRAI method.

        Args:
            seg_dilation: (Integer) Indicates level of mask dilation. Higher values yields
                smoother regions.
            area_perc_th: (Float) The region map is computed to cover area_perc_th of
                the image. Lower values will run faster, but produce uncomputed areas 
                in the image that will be filled to satisfy completeness. Defaults to 1.0.
                Not used if apprxomiate is set to True.
            min_pixel_diff: (Integer) Do not consider masks that have difference less than
                this number compared to the current mask. Set it to 1 to remove masks that 
                completely overlap with the current mask.
            approximate: (Boolean) If set to False (default), do not consider mask overlap 
                during importance ranking, significantly speeding up the algorithm for less 
                accurate results.
        """
        self.dilation_rad = seg_dilation
        self.area_perc_th = area_perc_th
        self.min_pixel_diff = min_pixel_diff
        self.approximate = approximate

        if not isinstance(self.dilation_rad, int) or self.dilation_rad < 1:
            raise ValueError(
                "Expected dialtion_rad argument to be a positive integer,"
                f" but got {self.dilation_rad} instead."
                )        
        if not isinstance(self.area_perc_th, float) or self.area_perc_th < 0.0 or self.area_perc_th > 1.0:
            raise ValueError(
                "Expected area_perc_th argument to be float in range 0.0 - 1.0,"
                f" but got {self.area_perc_th} instead."
                )
        if not isinstance(self.min_pixel_diff, int) or self.min_pixel_diff < 1:
            raise ValueError(
                "Expected min_pixel_diff argument to be a positive integer,"
                f" but got {self.min_pixel_diff} instead."
                )
        if self.approximate not in [False, True]:
            raise ValueError(
                "Expected approximate argument to be True or False,"
                f" but got {self.approximate} instead."
            )


    def _input_sanity_check(self, raw_images: torch.Tensor, attribution_maps: torch.Tensor):
        if raw_images.dim() < 4:
            raise ValueError(
                f"Expected raw_images to be 4'th order tensor, but got tensor of shape: {raw_images.shape} instead."
            )
        if attribution_maps.dim() < 4:
            raise ValueError(
                f"Expected attribution_maps to be 4'th order tensor, but got tensor of shape: {attribution_maps.shape} instead."
            )

        i_B, i_C, i_H, i_W = raw_images.shape
        a_B, a_C, a_H, a_W = attribution_maps.shape

        if raw_images.requires_grad:
            raw_images = raw_images.detach()

        if attribution_maps.requires_grad:
            attribution_maps = attribution_maps.detach()

        if raw_images.device != "cpu" or attribution_maps.device != "cpu":
            raw_images = raw_images.cpu()
            attribution_maps = attribution_maps.cpu()

        if i_B != a_B:
            raise ValueError(
                "Expected raw_images and attributions_maps to have the same batch size,"
                f" but got raw_images of shape: {raw_images.shape} and attribution_maps: {attribution_maps.shape}."
            )
        if i_C not in [1, 3]:
            raise ValueError(
                "Expected raw_images to have 1 or 3 channels,"
                f" but got {i_C} channels instead."
            )
        if a_C != 1:
            raise ValueError(
                "Expected attribution maps to have one channel,"
                f" but got {a_C} channels instead."
            )
        
        return raw_images, attribution_maps


    def regionize(self, 
                raw_images: torch.Tensor, 
                attribution_maps: torch.Tensor,
                gain_fun: Optional[Callable] = None
                ):
        """
        Compute explainable regions given attribution maps and raw images. Explainable regions are
        a set of importance scores (identical dimensions as an input `maps` except the color channel),
        by aggregating and comparing importance scores that fall in each segment.
        Based on XRAI - Better Attributions Through Regions (https://arxiv.org/abs/1906.02825).

        Args:
            raw_images: (torch.Tensor of shape (B, C, H, W)) - Batch of raw images from which segments will be extracted.
            attribution_maps: (torch.Tensor of shape (B, 1, H, W)) - Batch of corresponding attribution maps.
            gain_fun: (Callable) - Custom callable function that computes region importances from attribution maps.
        
        Returns:
            region_maps: batch of corresponding regionized XAI maps.
        """

        raw_images, attribution_maps = self._input_sanity_check(raw_images, attribution_maps)

        results = []
        for image, attr_maps in zip(raw_images, attribution_maps):
            segs = self._get_segments_felzenszwalb(image)
            merged_map, importance = self._compute_region_importance(
                attr_maps,
                segs,
                gain_fun=gain_fun or self._gain_density,
                integer_segments=True
            )
            results.append(torch.tensor(merged_map))
        return torch.stack(results, dim=0)

    @staticmethod
    def _normalize_image(im: torch.Tensor, value_range: Tuple[int, int], resize_shape: Optional[Tuple[int, int]] = None):
        im = (im - im.min()) / (im.max() - im.min() + 1e-8)
        im = im * (value_range[1] - value_range[0]) + value_range[0]
        im_np = im.permute(1, 2, 0).cpu().numpy()  # HWC
        if resize_shape is not None:
            im_np = resize(im_np, resize_shape, order=3, mode="constant",
                           preserve_range=True, anti_aliasing=True)
        return im_np

    def _get_segments_felzenszwalb(self, image: torch.Tensor, resize_image: bool = True, scale_range: Optional[Tuple[int, int]] = None):
        FELZENSZWALB_SCALE_VALUES = [50, 100, 150, 250, 500, 1200]
        FELZENSZWALB_SIGMA_VALUES = [0.8]
        FELZENSZWALB_IM_RESIZE = (224, 224)
        FELZENSZWALB_MIN_SEGMENT_SIZE = 150
        if scale_range is None:
            scale_range = [-1.0, 1.0]

        original_shape = image.shape[1:]  # CHW
        norm_img = self._normalize_image(image, 
                                         value_range = scale_range, 
                                         resize_shape = FELZENSZWALB_IM_RESIZE if resize_image else None)

        segs = []
        for scale in FELZENSZWALB_SCALE_VALUES:
            for sigma in FELZENSZWALB_SIGMA_VALUES:
                seg = segmentation.felzenszwalb(norm_img, scale=scale, sigma=sigma,
                                                min_size=FELZENSZWALB_MIN_SEGMENT_SIZE)
                if resize_image:
                    seg = resize(seg, original_shape, order=0,
                                 preserve_range=True, mode="constant", anti_aliasing=False).astype(int)
                segs.append(seg)

        masks = self._unpack_segs_to_masks(segs)
        if self.dilation_rad:
            footprint = disk(self.dilation_rad)
            masks = [torch.from_numpy(dilation(mask, footprint=footprint)) for mask in masks]
        else:
            masks = [torch.from_numpy(mask) for mask in masks]
        return masks

    def _compute_region_importance(self, attr: torch.Tensor, segs, gain_fun, integer_segments):
        attr = attr.clone().cpu()
        output_importance = torch.full_like(attr, -float('inf'), dtype=torch.float32)
        current_mask = torch.zeros_like(attr, dtype=torch.bool)
        masks_trace = []

        if not self.approximate:
            remaining_masks = {i: mask for i, mask in enumerate(segs)}
            current_area_perc = 0.0

            while current_area_perc <= self.area_perc_th and remaining_masks:
                best_gain = -float('inf')
                best_key = None
                remove_queue = []
                for k, m in remaining_masks.items():
                    if self._get_diff_cnt(m, current_mask) < self.min_pixel_diff:
                        remove_queue.append(k)
                        continue
                    gain = gain_fun(m, attr, current_mask)
                    if gain > best_gain:
                        best_gain = gain
                        best_key = k

                for k in remove_queue:
                    del remaining_masks[k]

                if best_key is None:
                    break

                new_mask = remaining_masks.pop(best_key)
                mask_diff = self._get_diff_mask(new_mask, current_mask)
                output_importance[mask_diff] = best_gain
                masks_trace.append(mask_diff)
                current_mask = torch.logical_or(current_mask, new_mask)
                current_area_perc = current_mask.float().mean().item()
        else:
            importance_list = [(m, gain_fun(m, attr)) for m in segs]
            sorted_masks = sorted(importance_list, key=lambda x: -x[1])
            for m, g in sorted_masks:
                if self._get_diff_cnt(m, current_mask) < self.min_pixel_diff:
                    continue
                mask_diff = self._get_diff_mask(m, current_mask)
                output_importance[mask_diff] = g
                masks_trace.append(mask_diff)
                current_mask = torch.logical_or(current_mask, m)

        uncomputed = output_importance == -float('inf')
        output_importance[uncomputed] = gain_fun(uncomputed, attr)
        masks_trace.append(uncomputed)

        if integer_segments:
            ranking = torch.zeros_like(attr, dtype=torch.int)
            for i, m in enumerate(masks_trace):
                ranking[m] = i + 1
            return output_importance.numpy(), ranking.numpy()
        else:
            return output_importance.numpy(), masks_trace

    @staticmethod
    def _unpack_segs_to_masks(segs):
        masks = []
        for seg in segs:
            unique_labels = range(seg.min(), seg.max() + 1)
            for label in unique_labels:
                masks.append((seg == label))
        return masks

    @staticmethod
    def _gain_density(mask1, attr, mask2=None):
        diff_mask = mask1 if mask2 is None else Regionizer._get_diff_mask(mask1, mask2)
        return -float('inf') if not diff_mask.any() else attr[diff_mask].float().mean().item()

    @staticmethod
    def _get_diff_mask(add_mask, base_mask):
        return torch.logical_and(add_mask, ~base_mask)

    @staticmethod
    def _get_diff_cnt(add_mask, base_mask):
        return Regionizer._get_diff_mask(add_mask, base_mask).sum().item()