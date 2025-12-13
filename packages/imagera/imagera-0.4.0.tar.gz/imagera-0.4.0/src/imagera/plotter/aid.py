from typing import Tuple
from allytools.units import Length, LengthUnit


def size_in_inches(size_in: Tuple[Length, Length]) -> Tuple[float, float]:
    w_len, h_len = size_in
    w_in = w_len.to(LengthUnit.INCH)
    h_in = h_len.to(LengthUnit.INCH)
    return float(w_in), float(h_in)

def extent_numeric(extent: Tuple[Length, Length, Length, Length], unit: LengthUnit) -> Tuple[float, float, float, float]:
    xmin = extent[0].to(unit)
    xmax = extent[1].to(unit)
    ymin = extent[2].to(unit)
    ymax = extent[3].to(unit)
    return float(xmin), float(xmax), float(ymin), float(ymax)