from dataclasses import dataclass
from typing import Optional, Tuple, Union, Any
from allytools.units import Length, LengthUnit
from imagera.plotter.cmap import CMaps
from matplotlib.colors import Colormap

Number = float
Percentile = str

@dataclass(frozen=True)
class PlotParameters:
    size_in: Tuple[Length, Length] = (
        Length(4.0, LengthUnit.INCH),
        Length(4.0, LengthUnit.INCH))
    dpi: int = 150
    use_levels: bool = True
    n_levels: int = 100
    cmap: Union[str, Colormap, CMaps] = CMaps.JET
    with_colorbar: bool = False
    hide_ticks: bool = True
    interpolation: Optional[str] = None
    x_label: Optional[str] = None
    y_label: Optional[str] = None
    value_label: Optional[str] = None
    plot_label: Optional[str] = None
    v_min: Optional[Union[Number, Percentile]] = None
    v_max: Optional[Union[Number, Percentile]] = None
    extent: Optional[Tuple[Length, Length, Length, Length]] = None
    show_lattice: bool = False
    lattice_pitch: Optional[Length] = None
    lattice_color: Any = (1, 1, 1, 0.4)

    def __post_init__(self) -> None:
        for size in self.size_in:
            if size.original_unit() is not LengthUnit.INCH:
                raise ValueError(f"PlotParameters.size_in must be in INCH units, "
                    f"got {size.original_unit()!r}")
        if self.extent is not None:
            units = {v.original_unit() for v in self.extent}

            if len(units) != 1:
                raise ValueError(f"All Length elements in extent must use the same unit, got {units!r}")
            (extent_unit,) = units

