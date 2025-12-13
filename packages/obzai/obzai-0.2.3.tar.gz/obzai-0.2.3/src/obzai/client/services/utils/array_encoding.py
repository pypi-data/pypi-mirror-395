# Obz AI - Copyright (C) 2025 Alethia XAI Sp. z o.o.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.


from io import BytesIO
from PIL import Image
import numpy as np
import gzip


def encode_into_npygz(arr: np.ndarray) -> bytes:
    """
    Compress and serialize a NumPy array using gzip and .npy format.

    Args:
        arr (np.ndarray): The NumPy array to serialize.

    Returns:
        bytes: Gzipped binary representation of the array.
    """
    buf = BytesIO()
    with gzip.GzipFile(fileobj=buf, mode='wb') as gz:
        np.save(gz, arr)
    buf.seek(0)

    return buf.getvalue()


def encode_into_jpeg(arr: np.ndarray, quality: int = 75) -> bytes:
    """
    Encode a 3D NumPy array (C, H, W) into a JPEG image.

    Args:
        arr (np.ndarray): Array of shape (C, H, W), values in [0, 1] or [0, 255].
        quality (int): JPEG compression quality (1–95). Default is 75.

    Returns:
        bytes: JPEG-encoded image as a byte stream.
    """
    if arr.ndim != 3:
        raise ValueError("Input array must have 3 dimensions (C, H, W)")

    if arr.shape[0] == 1:
        arr = arr.squeeze(0)
    elif arr.shape[0] == 3:
        # Move channel axis to the end
        arr = np.permute_dims(arr, axes=[1,2,0])
    else:
        raise ValueError("Input array must have 1 or 3 channels")

    # Normalize and cast
    if arr.max() <= 1.0:
        arr = arr * 255
    arr = arr.astype(np.uint8)

    # Encode to JPEG
    buf = BytesIO()
    Image.fromarray(arr).save(buf, format="JPEG", quality=quality)
    return buf.getvalue()