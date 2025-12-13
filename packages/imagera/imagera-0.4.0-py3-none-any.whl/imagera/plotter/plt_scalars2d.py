from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from imagera.plotter import PltScalar2d
from imagera.plotter.aid import size_in_inches
from matplotlib.colors import Normalize, BoundaryNorm
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from dataclasses import replace
from typing import Optional, Tuple, Iterable, Union, Any
from imagera.plotter.plot_parameters import PlotParameters
from imagera.plotter.cmap import resolve_cmap
from imagera.plotter.fit_title import fit_title


def _as_xy_tuple(cell: Any) -> Tuple[float, float]:
    """
    Accept (x,y) in various forms:
      - tuple/list of length 2
      - ndarray shape (2,)
      - ndarray shape (1,2) or (2,1)
    Return (float(x), float(y)).
    """
    a = np.asarray(cell).reshape(-1)
    if a.size != 2:
        raise ValueError(f"Grid cell does not represent (x,y): got shape {np.asarray(cell).shape}")
    return float(a[0]), float(a[1])


def _iterate_tiles(values_array: np.ndarray) -> Iterable[Tuple[int, int, np.ndarray]]:
    """
    Yield (i, j, tile) where tile is a 2D array (Ny, Nx) for each field.
    Supports:
      - new numeric format: (R, C, Ny, Nx)
      - old object grid: (R, C) dtype=object with 2D arrays per cell
    """
    if values_array.ndim == 4:
        R, C, _, _ = values_array.shape
        for i in range(R):
            for j in range(C):
                yield i, j, np.asarray(values_array[i, j], dtype=float)
    elif values_array.ndim == 2 and values_array.dtype == object:
        R, C = values_array.shape
        for i in range(R):
            for j in range(C):
                tile = values_array[i, j]
                if tile is None:
                    yield i, j, None  # allow None (will render "No PSF")
                else:
                    yield i, j, np.asarray(tile, dtype=float)
    else:
        raise ValueError(
            "values_array must be either (R,C,Ny,Nx) numeric or (R,C) object grid of 2D arrays."
        )


def _deduce_field_shape(values_array: np.ndarray) -> Tuple[int, int]:
    if values_array.ndim == 4:
        return values_array.shape[:2]
    elif values_array.ndim == 2 and values_array.dtype == object:
        return values_array.shape
    else:
        raise ValueError("values_array must be either (R,C,Ny,Nx) numeric or (R,C) object grid.")


def plt_scalars2d(
    grid: np.ndarray,
    values_array: np.ndarray,
    *,
    params: Optional[PlotParameters] = None,
    mosaic_title: Optional[str] = None,
    **param_overrides
) -> np.ndarray:
    """
    Render an R×C mosaic of PSF tiles into a single RGBA uint8 image.
    Supports both the old object-grid format and the new stacked numeric format.
    """

    # 1️⃣ Determine R, C from values
    R, C = _deduce_field_shape(values_array)

    # Basic grid sanity: expect (R,C,2) numeric or (R,C) object/tuples that can become (x,y)
    if grid.shape[:2] != (R, C):
        raise ValueError(f"grid and values_array field shapes must match; got grid {grid.shape[:2]} vs values {(R, C)}")

    # 2️⃣ Extract function-only flags, build PlotParams
    tile_titles = bool(param_overrides.pop("tile_titles", False))
    with_colorbar = bool(param_overrides.pop("with_colorbar", True))
    mosaic_title = param_overrides.pop("mosaic_title", mosaic_title)

    base = params if params is not None else PlotParameters()
    p = replace(base, **param_overrides)
    cmap, _ = resolve_cmap(p.cmap)

    # 3️⃣ Global vmin/vmax across all tiles (ignore None)
    vmins, vmaxs = [], []
    for _, _, tile in _iterate_tiles(values_array):
        if tile is None:
            continue
        if np.isfinite(tile).any():
            vmins.append(np.nanmin(tile))
            vmaxs.append(np.nanmax(tile))
    if not vmins:
        raise ValueError("No valid PSF grids to render.")
    vmin = p.v_min if getattr(p, "v_min", None) is not None else float(min(vmins))
    vmax = p.v_max if getattr(p, "v_max", None) is not None else float(max(vmaxs))

    if p.use_levels:
        n_levels = max(2, int(p.n_levels))
        levels = np.linspace(vmin, vmax, n_levels)
        ncolors = getattr(cmap, "N", 256)
        norm = BoundaryNorm(levels, ncolors=ncolors, clip=True)
    else:
        norm = Normalize(vmin=vmin, vmax=vmax)

    # 4️⃣ Figure / GridSpec layout
    tile_w_in, tile_h_in =size_in_inches(p.size_in)
    extra_w = 0.6 if with_colorbar else 0.0
    fig_w_in = C * tile_w_in + extra_w
    fig_h_in = R * tile_h_in
    fig = plt.figure(figsize=(fig_w_in, fig_h_in), dpi=p.dpi)
    if with_colorbar:
        gs = gridspec.GridSpec(R, C + 1, figure=fig, width_ratios=[1] * C + [0.05])
        last_col_index = -1
    else:
        gs = gridspec.GridSpec(R, C, figure=fig, width_ratios=[1] * C)
        last_col_index = None

    # 5️⃣  Render (bottom-left = [0,0] in logical indices)
    mappable = None
    for i in range(R):
        # Logical row i=0 is bottom, but Matplotlib row 0 is top,
        # so map logical row i to plotting row (R-1-i).
        plot_row = R - 1 - i
        for j in range(C):
            ax = fig.add_subplot(gs[plot_row, j])

            # pick the tile for logical (i,j)
            if values_array.ndim == 4:
                tile = np.asarray(values_array[i, j], dtype=float)
            else:  # old object grid
                tile = values_array[i, j]
                tile = None if tile is None else np.asarray(tile, dtype=float)

            if tile is None:
                ax.text(0.5, 0.5, "No PSF", ha="center", va="center")
                ax.set_axis_off()
                continue
            dp = PltScalar2d(tile, params=p)

            # per-tile (x,y) annotation from logical grid (i,j)
            try:
                annotate_xy = (
                    None if getattr(p, "annotate_xy", None) is not None
                    else _as_xy_tuple(grid[i, j])
                )
            except Exception:
                annotate_xy = None

            plot_label = ("\u00A0" if not tile_titles else None)

            im, _ = dp.render_into(ax, norm=norm, annotate_xy=annotate_xy, plot_label=plot_label)
            if mappable is None:
                mappable = im

    # 6️⃣  Colorbar
    if with_colorbar and (mappable is not None) and (last_col_index is not None):
        cax = fig.add_subplot(gs[:, last_col_index])
        cbar = fig.colorbar(mappable, cax=cax)
        label = getattr(p, "value_label", None)
        if not label:
            # best-effort: look for a 'value_label' on first non-None tile-like object (old pipelines)
            if hasattr(values_array, "value_label"):
                label = getattr(values_array, "value_label")
        if label:
            cbar.set_label(str(label), fontsize=12)

    ## 7️⃣ Title & rasterize to RGBA
    if mosaic_title:
        # Leave some headroom for the title band
        fit_title(fig, str(mosaic_title))
        # Reserve space for suptitle so tight_layout doesn't collide with it
        fig.tight_layout(rect=(0.0, 0.0, 1.0, 0.95))
    else:
        fig.tight_layout()

    canvas = FigureCanvas(fig)
    canvas.draw()
    rgba = np.asarray(canvas.buffer_rgba()).copy()
    plt.close(fig)
    return rgba
