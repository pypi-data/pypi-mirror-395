from dataclasses import dataclass, field
from typing import Tuple
from math import isfinite
from lensguild.optics import  Wavelength, WavelengthUnit

@dataclass(frozen=True)
class OpticalFilter:
    name: str
    min_wavelength: Wavelength
    max_wavelength: Wavelength
    reflectance_curve: Tuple[Tuple[Wavelength, float], ...] = field(default_factory=tuple)

    def __str__(self):
        return self.name

    def __post_init__(self):
        # Basic validations
        if not (self.min_wavelength < self.max_wavelength):
            raise ValueError("min_wavelength must be < max_wavelength")

        if not self.reflectance_curve:
            raise ValueError("reflectance_curve must contain at least one (wavelength, R) point")

        # Ensure curve is sorted and inside the range, and values are sane
        points = list(self.reflectance_curve)
        # sort by wavelength (in mm under the hood)
        points.sort(key=lambda p: p[0].length)
        object.__setattr__(self, "reflectance_curve", tuple(points))

        if points[0][0] < self.min_wavelength or points[-1][0] > self.max_wavelength:
            raise ValueError("reflectance_curve points must lie within [min_wavelength, max_wavelength]")

        for wl, R in points:
            if not (0.0 <= R <= 1.0) or not isfinite(R):
                raise ValueError(f"Reflectance must be finite in [0,1]; got {R} at {wl}")

    def reflection_at(self, wavelength: Wavelength, *, clamp: bool = False) -> float:
        """
        Linear interpolation of reflectance at 'wavelength'.
        If clamp=False, raises ValueError when outside the [min, max] range.
        If clamp=True, returns reflectance at nearest boundary point.
        """
        pts = self.reflectance_curve

        # Range handling
        if wavelength < self.min_wavelength:
            if not clamp:
                raise ValueError(
                    f"{wavelength} is below the supported range [{self.min_wavelength}, {self.max_wavelength}]")
            return pts[0][1]
        if wavelength > self.max_wavelength:
            if not clamp:
                raise ValueError(
                    f"{wavelength} is above the supported range [{self.min_wavelength}, {self.max_wavelength}]")
            return pts[-1][1]

        # Exact match?
        for wl, R in pts:
            if wl == wavelength:
                return R

        # Find neighbors for interpolation (linear)
        # Since pts is sorted, scan once (list is typically small)
        prev_wl, prev_R = pts[0]
        for i in range(1, len(pts)):
            wl, R = pts[i]
            if wavelength < wl:
                # interpolate between prev_wl..wl
                x0 = prev_wl.to(WavelengthUnit.NM)
                x1 = wl.to(WavelengthUnit.NM)
                x = wavelength.to(WavelengthUnit.NM)
                # linear interpolation
                t = (x - x0) / (x1 - x0)
                return prev_R + t * (R - prev_R)
            prev_wl, prev_R = wl, R

        # If we land here, wavelength is at/after last point (shouldn’t happen due to earlier range check)
        return pts[-1][1]