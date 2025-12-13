from enum import Enum
from typing import Optional
from allytools.units.length import Length, LengthUnit
from allytools.units.percentage import Percentage

class PixelUnit(Enum):
    UM = LengthUnit.UM

class Pixel:
    def __init__(self, width: Length, fill_factor: Percentage,
                 height: Optional[Length] = None):
        self._constructed_as_square = height is None

        if width.original_unit() is not LengthUnit.UM:
            raise ValueError("Length must be specified in UM (micrometres).")
        if height is not None and height.original_unit() is not LengthUnit.UM:
            raise ValueError("Length must be specified in UM (micrometres).")
        self.width = width
        self.height = height if height is not None else width
        self.fill_factor = fill_factor

    @property
    def is_square(self) -> bool:
        return self._constructed_as_square

    @property
    def length(self) -> Length:
        if self.is_square:
            return self.width
        raise ValueError("Pixel is not square; 'height' was provided explicitly.")

    def __str__(self):
        return (f"Pixel: {self.width.to(LengthUnit.UM):.2f} µm × "
                f"{self.height.to(LengthUnit.UM):.2f} µm, "
                f"Fill Factor: {self.fill_factor}, "
                f"{'Square' if self.is_square else 'Non-square'}")

