import math
from enum import Enum
from dataclasses import dataclass, field
from allytools.units import Length, LengthUnit
from allytools.db import ModelID

from isensor.pixel import Pixel
from isensor.bit_depth import BitDepth
from isensor.sensor_type import SensorFormats, SensorType
from isensor.grid import Grid

class SensorBrand(Enum):
    Sony = "Sony"

@dataclass(frozen=True)
class SensorModel(ModelID[SensorBrand]):
    pass

@dataclass(frozen=True, kw_only=True)
class Sensor:
    sensor_model: SensorModel
    pixel: Pixel
    horizontal_pixels: int
    vertical_pixels: int
    bit_depth: BitDepth
    sensor_format: SensorFormats
    sensor_type: SensorType
    grid: Grid = field(init=False)

    def __post_init__(self):
        if not isinstance(self.pixel, Pixel):
            raise TypeError("pixel must be a Pixel instance.")
        if not isinstance(self.sensor_format, SensorFormats):
            raise TypeError("sensor_format must be a SensorFormats instance.")
        if not isinstance(self.sensor_type, SensorType):
            raise TypeError("sensor_type must be a SensorType instance.")
        if not isinstance(self.bit_depth, BitDepth):
            raise TypeError("bit_depth must be a BitDepth instance.")
        if not isinstance(self.horizontal_pixels, int) or self.horizontal_pixels <= 0:
            raise TypeError("horizontal_pixels must be a positive int.")
        if not isinstance(self.vertical_pixels, int) or self.vertical_pixels <= 0:
            raise TypeError("vertical_pixels must be a positive int.")
        object.__setattr__(self, "grid", Grid(self))

    # ---- convenient aliases (back-compat) ----
    @property
    def width_pix(self) -> int:
        return self.horizontal_pixels

    @property
    def height_pix(self) -> int:
        return self.vertical_pixels

    # ---- geometry (computed) ----
    @property
    def width(self) -> Length:
        """
        Sensor width as a Length.
        - Prefer rectangular pixels via pixel.width; else fall back to pixel.length.
        """
        if hasattr(self.pixel, "width") and isinstance(self.pixel.width, Length):
            px_w_mm = self.pixel.width.value_mm  # Length already stores mm internally
        elif hasattr(self.pixel, "length") and isinstance(self.pixel.length, Length):
            px_w_mm = self.pixel.length.value_mm
        else:
            raise AttributeError("Pixel must have a Length in .width or .length.")
        return Length(self.horizontal_pixels * px_w_mm, LengthUnit.MM)

    @property
    def height(self) -> Length:
        """
        Sensor height as a Length.
        - Prefer rectangular pixels via pixel.height; else fall back to pixel.length.
        """
        if hasattr(self.pixel, "height") and isinstance(self.pixel.height, Length):
            px_h_mm = self.pixel.height.value_mm
        elif hasattr(self.pixel, "length") and isinstance(self.pixel.length, Length):
            px_h_mm = self.pixel.length.value_mm
        else:
            raise AttributeError("Pixel must have a Length in .height or .length.")
        return Length(self.vertical_pixels * px_h_mm, LengthUnit.MM)

    @property
    def diagonal(self) -> Length:
        w_mm = self.width.value_mm
        h_mm = self.height.value_mm
        return Length(math.hypot(w_mm, h_mm), LengthUnit.MM)



    # ---- repr/str ----
    def __str__(self) -> str:
        # Include SensorModel on the first line, then core specs
        return (
            f"{self.sensor_model}: {self.horizontal_pixels}×{self.vertical_pixels} px\n"
            f"  pixel     : {self.pixel}\n"
            f"  size      : {self.width} × {self.height} (diag {self.diagonal})\n"
            f"  bit_depth : {self.bit_depth}\n"
            f"  format    : {self.sensor_format}\n"
            f"  type      : {self.sensor_type}"
        )


    def __repr__(self) -> str:
        fmt = getattr(self.sensor_format, "name", self.sensor_format)
        typ = getattr(self.sensor_type, "name", self.sensor_type)
        bd = getattr(self.bit_depth, "name", self.bit_depth)
        return (
            f"Sensor(sensor_model={self.sensor_model!r}, "
            f"horizontal_pixels={self.horizontal_pixels!r}, vertical_pixels={self.vertical_pixels!r}, "
            f"pixel={self.pixel!s}, bit_depth={bd!s}, "
            f"sensor_format={fmt!s}, sensor_type={typ!s}, "
            f"width={self.width!s}, height={self.height!s}, diagonal={self.diagonal!s})"
        )
