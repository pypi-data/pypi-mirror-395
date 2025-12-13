import numpy as np
from dataclasses import dataclass
from RayTracing.ray_vector import RayVector

@dataclass
class TransferMatrix:
    t: float  # thickness in mm
    n: float  # refractive index

    def as_array(self) -> np.ndarray:
        return np.array([
            [1.0, 0.0],
            [self.t / self.n, 1.0]
        ], dtype=float)

    def __matmul__(self, ray_vector: RayVector) -> RayVector:
        if not isinstance(ray_vector, RayVector):
            raise TypeError("Expected a RayVector")
        result = self.as_array() @ ray_vector.as_array()
        return RayVector(nu=result[0, 0], y=result[1, 0])

    def __repr__(self) -> str:
        return f"TransferMatrix(t={self.t}, n={self.n})"

    @staticmethod
    def from_surface(surface) -> "TransferMatrix":
        n = surface.material.refractive_index.n
        t = surface.thickness.value_mm
        return TransferMatrix(t=t, n=n)




@dataclass
class RefractionMatrix:
    n1: float  # refractive index before the surface
    n2: float  # refractive index after the surface
    R: float   # radius of curvature of the surface (in mm)

    def as_array(self) -> np.ndarray:
        power = (self.n2 - self.n1) / self.R
        return np.array([
            [1.0, -power],
            [0.0, 1.0]
        ], dtype=float)

    def __matmul__(self, ray_vector: RayVector) -> RayVector:
        if not isinstance(ray_vector, RayVector):
            raise TypeError("Expected a RayVector")
        result = self.as_array() @ ray_vector.as_array()
        return RayVector(nu=result[0, 0], y=result[1, 0])

    def __repr__(self) -> str:
        power = (self.n2 - self.n1) / self.R
        return f"RefractionMatrix(Φ={power:.6f}, n1={self.n1}, n2={self.n2}, R={self.R})"

    @staticmethod
    def from_surfaces(surface_before, surface_after) -> "RefractionMatrix":
        n1 = surface_before.material.refractive_index.n
        n2 = surface_after.material.refractive_index.n
        R = surface_after.radius.value_mm
        return RefractionMatrix(n1=n1, n2=n2, R=R)