from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Tuple
import numpy as np
import io
import base64

try:
    from PIL import Image
except ImportError:
    Image = None

# Optional deps – only used if available
try:
    import torch
except ImportError:
    torch = None

try:
    import tensorflow as tf
except ImportError:
    tf = None

@dataclass
class ImageBundle:
    """
    A thin adapter around a NumPy image that can produce
    multiple formats on demand (with simple caching).
    """
    # Accepts (H,W), (H,W,3) RGB, or (H,W,4) RGBA
    array: np.ndarray
    # If True, assume self.array in [0,1] float and auto-scale to uint8 for 8-bit formats
    assume_float_in_01: bool = False

    _cached_pil: Optional["Image.Image"] = field(default=None, init=False, repr=False)
    _cached_rgba8: Optional[np.ndarray] = field(default=None, init=False, repr=False)

    def __post_init__(self):
        a = self.array

        # ✅ Must be numpy
        if not isinstance(a, np.ndarray):
            raise TypeError(f"array must be a numpy.ndarray, got {type(a)}")

        # ✅ Shape checks
        if a.ndim == 2:
            # grayscale
            pass
        elif a.ndim == 3:
            if a.shape[2] not in (1, 3, 4):
                raise ValueError(
                    f"Third dimension must be 1, 3, or 4 channels, got {a.shape[2]}"
                )
        else:
            raise ValueError(
                f"array must be 2D (H,W) or 3D (H,W,C), got shape {a.shape}"
            )

        # ✅ dtype must be numeric (int or float)
        if not np.issubdtype(a.dtype, np.floating) and not np.issubdtype(a.dtype, np.integer):
            raise TypeError(
                f"Image array must have numeric dtype, got {a.dtype}"
            )

        # ✅ Optional float validation
        if np.issubdtype(a.dtype, np.floating) and self.assume_float_in_01:
            if np.nanmin(a) < 0.0 or np.nanmax(a) > 1.0:
                raise ValueError(
                    "assume_float_in_01=True but values are outside [0,1]"
                )

        # ✅ Channel=1 → treat as grayscale
        if a.ndim == 3 and a.shape[2] == 1:
            # collapse (H,W,1) → (H,W)
            self.array = a.reshape(a.shape[0], a.shape[1])


    def _to_rgba8(self) -> np.ndarray:
        """
        Returns an (H, W, 4) uint8 RGBA array.
        - Converts grayscale/RGB to RGBA.
        - Scales float arrays to uint8 if needed.
        """
        if self._cached_rgba8 is not None:
            return self._cached_rgba8

        a = self.array
        if a.ndim == 2:
            # Grayscale -> RGB
            a = np.stack([a, a, a], axis=-1)
        if a.ndim != 3 or a.shape[2] not in (3, 4):
            raise ValueError(f"Unsupported input shape: {self.array.shape}")

        # Handle dtype/scale
        if np.issubdtype(a.dtype, np.floating):
            # If values not in [0,1], try to auto-normalize per min/max
            if not self.assume_float_in_01:
                amin, amax = float(np.nanmin(a)), float(np.nanmax(a))
                if amax > amin:
                    a = (a - amin) / (amax - amin)
                else:
                    a = np.zeros_like(a)
            a = np.clip(a, 0.0, 1.0)
            a = (a * 255.0 + 0.5).astype(np.uint8)
        elif a.dtype != np.uint8:
            # Best-effort cast
            a = np.clip(a, 0, 255).astype(np.uint8)

        if a.shape[2] == 3:
            # Add opaque alpha
            alpha = np.full(a.shape[:2] + (1,), 255, dtype=np.uint8)
            a = np.concatenate([a, alpha], axis=2)

        self._cached_rgba8 = a
        return a

    def to_numpy(self, want: str = "rgba8") -> np.ndarray:
        """
        Return NumPy array in requested layout:
          - "rgb8"  -> (H,W,3) uint8
          - "rgba8" -> (H,W,4) uint8
          - "gray8" -> (H,W)   uint8 (luma from RGB)
        """
        rgba = self._to_rgba8()
        if want == "rgba8":
            return rgba
        if want == "rgb8":
            return rgba[..., :3]
        if want == "gray8":
            # simple luma approximation
            r, g, b = rgba[..., 0], rgba[..., 1], rgba[..., 2]
            y = (0.299 * r + 0.587 * g + 0.114 * b + 0.5).astype(np.uint8)
            return y
        raise ValueError(f"Unknown numpy format: {want}")

    def to_pillow(self) -> "Image.Image":
        """Return a Pillow Image (mode RGBA)."""
        if Image is None:
            raise RuntimeError("Pillow not installed.")
        if self._cached_pil is None:
            rgba = self._to_rgba8()
            self._cached_pil = Image.fromarray(rgba, mode="RGBA")
        return self._cached_pil

    def to_png_bytes(self, **pil_save_kwargs) -> bytes:
        """Return PNG bytes (lossless, supports alpha)."""
        im = self.to_pillow()
        buf = io.BytesIO()
        im.save(buf, format="PNG", **pil_save_kwargs)
        return buf.getvalue()

    def to_jpeg_bytes(self, quality: int = 90, **pil_save_kwargs) -> bytes:
        """Return JPEG bytes (lossy, no alpha)."""
        im = self.to_pillow().convert("RGB")
        buf = io.BytesIO()
        im.save(buf, format="JPEG", quality=int(quality), **pil_save_kwargs)
        return buf.getvalue()

    def to_tiff_bytes(self, **pil_save_kwargs) -> bytes:
        """Return TIFF bytes (can be lossless; good for high bit-depth)."""
        im = self.to_pillow()
        buf = io.BytesIO()
        im.save(buf, format="TIFF", **pil_save_kwargs)
        return buf.getvalue()

    def to_bmp_bytes(self, **pil_save_kwargs) -> bytes:
        """Return BMP bytes (un/low-compressed; legacy)."""
        im = self.to_pillow()
        buf = io.BytesIO()
        im.save(buf, format="BMP", **pil_save_kwargs)
        return buf.getvalue()

    def to_opencv_bgr(self) -> np.ndarray:
        """
        Return (H,W,3) uint8 in BGR order for OpenCV.
        Alpha channel (if any) is dropped.
        """
        rgb = self.to_numpy("rgb8")
        # RGB -> BGR
        return rgb[..., ::-1].copy()

    def to_torch_tensor(self, normalize_01: bool = True):
        """
        Return a torch.FloatTensor of shape (C,H,W).
        If normalize_01=True, scale to [0,1].
        """
        if torch is None:
            raise RuntimeError("PyTorch not installed.")
        rgb = self.to_numpy("rgb8").astype(np.float32)
        if normalize_01:
            rgb = rgb / 255.0
        t = torch.from_numpy(rgb)             # (H,W,C)
        return t.permute(2, 0, 1).contiguous()  # (C,H,W)

    def to_tf_tensor(self, normalize_01: bool = True):
        """
        Return a tf.float32 Tensor of shape (H,W,C).
        If normalize_01=True, scale to [0,1].
        """
        if tf is None:
            raise RuntimeError("TensorFlow not installed.")
        rgb = self.to_numpy("rgb8").astype(np.float32)
        if normalize_01:
            rgb = rgb / 255.0
        return tf.convert_to_tensor(rgb, dtype=tf.float32)

    def to_data_uri_png(self) -> str:
        """Return a data:image/png;base64,... string."""
        b = self.to_png_bytes()
        return "data:image/png;base64," + base64.b64encode(b).decode("ascii")

    def save(self, path: str, format: Optional[str] = None, **kwargs) -> None:
        """
        Save to disk using Pillow. Format inferred from extension if not given.
        """
        im = self.to_pillow()
        im.save(path, format=format, **kwargs)
