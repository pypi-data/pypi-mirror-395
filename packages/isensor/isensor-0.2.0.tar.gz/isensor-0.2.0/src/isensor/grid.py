from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from numpy.typing import NDArray
from allytools.units import Length
from typing import Tuple, TYPE_CHECKING, Sequence
from isensor.sensor_positions import SensorPosition

if TYPE_CHECKING:
    from isensor.sensor import Sensor


def _axis_1d(
        start_end: Tuple[float, float],
    step_mm: Length,
    *,
    reverse: bool,
    shift_to_zero: bool,
) -> np.ndarray:
    if not isinstance(step_mm, Length):
        raise TypeError("step_mm must be a Length instance.")
    if step_mm.value_mm <= 0:
        raise ValueError("step_mm must be positive.")

    start, end = start_end
    vals = np.arange(start, end + 1e-9, step_mm.value_mm, dtype=np.float64)
    if reverse:
        vals = vals[::-1]
    if shift_to_zero:
        vals -= start  # 0 at quadrant origin (sensor center)
    return vals


def length_to_mm(arr:np.ndarray) -> np.ndarray:
    return np.array([x.value_mm for x in arr], dtype=float)


@dataclass(frozen=True, slots=True)
class Grid:
    _sensor: Sensor


    @staticmethod
    def _px_pitch_x(sensor) -> float:
        if hasattr(sensor.pixel, "width") and isinstance(sensor.pixel.width, Length):
            return sensor.pixel.width.value_mm
        if hasattr(sensor.pixel, "length") and isinstance(sensor.pixel.length, Length):
            return sensor.pixel.length.value_mm
        raise AttributeError("Pixel must have .width or .length as Length for X pitch.")

    @staticmethod
    def _px_pitch_y(sensor) -> float:
        if hasattr(sensor.pixel, "height") and isinstance(sensor.pixel.height, Length):
            return sensor.pixel.height.value_mm
        if hasattr(sensor.pixel, "length") and isinstance(sensor.pixel.length, Length):
            return sensor.pixel.length.value_mm
        raise AttributeError("Pixel must have .height or .length as Length for Y pitch.")

    @staticmethod
    def _quadrant_start_end(n_pix: int, pitch_mm: float) -> Tuple[float, float]:
        mid = n_pix / 2.0
        start = (mid - 0.5) * pitch_mm
        end   = (n_pix - 0.5) * pitch_mm
        return start, end

    @property
    def x_start_end(self) -> Tuple[float, float]:
        """Start and end X values of the top-right quadrant (mm)."""
        s = self._sensor
        px = self._px_pitch_x(s)
        return self._quadrant_start_end(s.width_pix, px)

    @property
    def y_start_end(self) -> Tuple[float, float]:
        """Start and end Y values of the top-right quadrant (mm)."""
        s = self._sensor
        py = self._px_pitch_y(s)
        return self._quadrant_start_end(s.height_pix, py)

    def x1d_mm(self, step_mm: Length) ->Sequence[Length]:
        """
        1D X axis (0 → +X), bottom-to-right, returns Length objects in mm.
        """
        vals = _axis_1d(self.x_start_end, step_mm, reverse=False, shift_to_zero=True)
        return [Length(v) for v in vals]

    def y1d_mm(self, step_mm: Length) -> Sequence[Length]:
        """
        1D Y axis (0 → +Y), bottom-to-top, returns Length objects in mm.
        """
        vals = _axis_1d(self.y_start_end, step_mm, reverse=False, shift_to_zero=True)
        return [Length(v) for v in vals]

    def x1d_n(self, num_samples: int) -> Sequence[Length]:
        """
        num_samples points from sensor center (0 mm) to +X edge,
        equally spaced, returned as Length objects in millimeters.
        """
        if num_samples <= 0:
            raise ValueError("num_samples must be positive")

        start, end = self.x_start_end  # mm
        span = end - start  # mm (distance center → edge)

        xs = np.linspace(0.0, span, num_samples, dtype=np.float64)
        return [Length(x) for x in xs]

    def y1d_n(self, num_samples: int) -> Sequence[Length]:
        """
        num_samples points from sensor center (0 mm) to +Y edge,
        equally spaced, returned as Length objects in millimeters.
        """
        if num_samples <= 0:
            raise ValueError("num_samples must be positive")

        start, end = self.y_start_end
        span = end - start
        ys = np.linspace(0.0, span, num_samples, dtype=np.float64)

        return [Length(y) for y in ys]

    # ---------- 2D grids on demand ----------
    def x(self, step_mm: Length) -> NDArray[np.float64]:
        xs = np.array(self.x1d_mm(step_mm), dtype=object)
        ys = np.array(self.y1d_mm(step_mm), dtype=object)

        xs_mm = np.array([x.value_mm for x in xs], dtype=np.float64)
        ys_mm = np.array([y.value_mm for y in ys], dtype=np.float64)

        return np.tile(xs_mm, (ys_mm.size, 1))

    def y(self, step_mm: Length) -> NDArray[np.float64]:
        xs = np.array(self.x1d_mm(step_mm), dtype=object)
        ys = np.array(self.y1d_mm(step_mm), dtype=object)

        xs_mm = np.array([x.value_mm for x in xs], dtype=np.float64)
        ys_mm = np.array([y.value_mm for y in ys], dtype=np.float64)

        return np.tile(ys_mm[:, None], (1, xs_mm.size))
    # ---------- radial sequence ----------
    def get_radial(self, step_mm: Length) ->Sequence[Length]:
        """
        Radial coordinates from center (0 mm) to the sensor's half-diagonal,
        with step given by step_mm. Returns Length objects (mm).
        """
        if not isinstance(step_mm, Length):
            raise TypeError("step_mm must be a Length instance.")
        if step_mm.value_mm <= 0:
            raise ValueError("step_mm must be positive.")

        r_max_mm = 0.5 * self._sensor.diagonal.value_mm

        # generate float radii in mm
        seq = np.arange(0.0, r_max_mm + 1e-9, step_mm.value_mm, dtype=np.float64)
        seq = seq[seq <= r_max_mm + 1e-9]

        # convert to Length objects
        return [Length(r) for r in seq]

    def sparse_quadrant(self, n: int) -> tuple[Sequence[Length], Sequence[Length]]:
        """
        Sparse top-right quadrant axes.

        - Only uses the top-right quadrant of the sensor (from the center outward).
        - Takes every n-th pixel center in both X and Y.
        - Returns distances from the sensor center as Length objects (in mm).
        """
        if n <= 0:
            raise ValueError("n must be positive")

        s = self._sensor

        # pixel pitches (mm)
        pitch_x = self._px_pitch_x(s)
        pitch_y = self._px_pitch_y(s)

        # number of pixels in top-right quadrant along each axis
        n_qx = s.width_pix // 2  # pixels from center to right edge
        n_qy = s.height_pix // 2  # pixels from center to top edge

        # indices within the quadrant: 0 is the pixel just next to the center,
        # 1 is the next one, and so on
        idx_x = np.arange(0, n_qx, n, dtype=int)
        idx_y = np.arange(0, n_qy, n, dtype=int)

        # distance from sensor center to each pixel center (float mm)
        x_mm = (0.5 + idx_x.astype(float)) * pitch_x
        y_mm = (0.5 + idx_y.astype(float)) * pitch_y

        # convert to Length(mm)
        x_len = [Length(v) for v in x_mm]
        y_len = [Length(v) for v in y_mm]

        return x_len, y_len

    def get_position(self, position: SensorPosition) -> tuple[Length, Length]:
        """
        Return the pixel-center coordinates for the chosen sensor position.
        Coordinates are measured from sensor center (0,0), in Length(mm).
        """

        s = self._sensor
        pitch_x = self._px_pitch_x(s)
        pitch_y = self._px_pitch_y(s)

        # Half-pixel distances
        nx = s.width_pix  // 2
        ny = s.height_pix // 2

        # Compute max pixel centers in each direction
        x_max_mm = (nx - 0.5) * pitch_x
        y_max_mm = (ny - 0.5) * pitch_y

        # CENTER
        if position is SensorPosition.CENTER:
            return Length(0.0), Length(0.0)

        # TOP RIGHT
        if position is SensorPosition.TOP_RIGHT:
            return Length(+x_max_mm), Length(+y_max_mm)

        # TOP LEFT
        if position is SensorPosition.TOP_LEFT:
            return Length(-x_max_mm), Length(+y_max_mm)

        # BOTTOM RIGHT
        if position is SensorPosition.BOTTOM_RIGHT:
            return Length(+x_max_mm), Length(-y_max_mm)

        # BOTTOM LEFT
        if position is SensorPosition.BOTTOM_LEFT:
            return Length(-x_max_mm), Length(-y_max_mm)

        raise ValueError(f"Unsupported SensorPosition: {position}")
