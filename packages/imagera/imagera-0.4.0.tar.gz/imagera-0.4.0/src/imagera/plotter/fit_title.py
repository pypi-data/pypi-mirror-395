from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def fit_title(fig, text: str, *,
                  max_width_frac: float = 0.98,
                  max_height_frac: float = 0.08,
                  min_fontsize: int = 6,
                  max_fontsize: int = 24,
                  y_top: float = 0.995):
    """
    Create a suptitle that auto-shrinks to fit figure width/height and avoids clipping.
    Returns the Text instance (or None).
    """
    if not text:
        return None

    # Ensure we have a canvas/renderer
    canvas = FigureCanvas(fig)

    # Start large and shrink to fit
    t = fig.suptitle(text, y=y_top, fontsize=max_fontsize)
    canvas.draw()
    renderer = canvas.get_renderer()

    fig_w_px, fig_h_px = fig.get_size_inches() * fig.dpi
    fs = max_fontsize
    bb = t.get_window_extent(renderer=renderer)

    # shrink if too wide or too tall a band
    while fs > min_fontsize and (
        bb.width > max_width_frac * fig_w_px or
        bb.height > max_height_frac * fig_h_px
    ):
        fs -= 1
        t.set_fontsize(fs)
        canvas.draw()
        bb = t.get_window_extent(renderer=renderer)

    # If top is beyond the canvas, move it down a bit
    if bb.y1 > fig_h_px:
        overshoot = bb.y1 - fig_h_px
        new_y = 1.0 - (overshoot + 2.0) / fig_h_px  # 2 px padding
        # keep within a sensible band
        t.set_y(max(0.94, min(y_top, new_y)))
        canvas.draw()

    return t
