from typing import  Final
from isensor.sensor import Sensor, SensorModel, SensorBrand
from isensor.sensor_type import SensorType, SensorFormats
from isensor.bit_depth import BitDepth, BitDepthOptions
from isensor.pixel import Pixel
from allytools.units import Percentage, Length, LengthUnit
from allytools.db import FrozenDB

class SensorsDB(metaclass=FrozenDB):
    __slots__ = ()
    SONY_IMX547: Final[Sensor] = Sensor(sensor_model=SensorModel(SensorBrand.Sony, "IMX547"),
                                        horizontal_pixels= 2448,
                                        vertical_pixels= 2048,
                                        pixel= Pixel(Length(2.74, LengthUnit.UM),Percentage(100)),
                                        bit_depth=BitDepth(BitDepthOptions.BD_12),
                                        sensor_format=SensorFormats.S_1_2_3,
                                        sensor_type=SensorType.CMOS)
    SONY_IMX174: Final[Sensor] = Sensor(sensor_model=SensorModel(SensorBrand.Sony, "IMX174"),
                                        horizontal_pixels = 1936,
                                        vertical_pixels = 1216,
                                        pixel= Pixel(Length(5.86, LengthUnit.UM),Percentage(100)),
                                        bit_depth = BitDepth(BitDepthOptions.BD_12),
                                        sensor_format= SensorFormats.S_1_2,
                                        sensor_type = SensorType.CMOS)
    SONY_IMX900: Final[Sensor] = Sensor(sensor_model=SensorModel(SensorBrand.Sony, "IMX900"),
                                        horizontal_pixels = 2064,
                                        vertical_pixels = 1552,
                                        pixel = Pixel(Length(2.25, LengthUnit.UM),Percentage(100)),
                                        bit_depth = BitDepth(BitDepthOptions.BD_12),
                                        sensor_format = SensorFormats.S_1_3_1,
                                        sensor_type=SensorType.CMOS)

    SONY_IMX445: Final[Sensor] = Sensor(sensor_model=SensorModel(SensorBrand.Sony, "IMX445"),
                                        horizontal_pixels = 1280,
                                        vertical_pixels = 960,
                                        pixel = Pixel(Length(3.75, LengthUnit.UM),Percentage(100)),
                                        bit_depth = BitDepth(BitDepthOptions.BD_8),
                                        sensor_format = SensorFormats.S_1_3,
                                        sensor_type=SensorType.CCD)

    SONY_IMX420: Final[Sensor] = Sensor(sensor_model=SensorModel(SensorBrand.Sony, "IMX420"),
                                        horizontal_pixels = 3216,
                                        vertical_pixels = 2208,
                                        pixel = Pixel(Length(4.5, LengthUnit.UM),Percentage(100)),
                                        bit_depth = BitDepth(BitDepthOptions.BD_8),
                                        sensor_format = SensorFormats.S_1_1,
                                        sensor_type=SensorType.CMOS)