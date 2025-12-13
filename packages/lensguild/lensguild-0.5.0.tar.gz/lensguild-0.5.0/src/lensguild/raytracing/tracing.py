from typing import List
from RayTracing.ray import Ray
from RayTracing.ray_vector import RayVector
from RayTracing.matrix import TransferMatrix, RefractionMatrix
from Optics.surface import OpticalSurface

class ParaxialRayTracer:
    @staticmethod
    def trace_ray(ray: Ray, surfaces: List[OpticalSurface]) -> List[RayVector]:
        if not surfaces or len(surfaces) < 2:
            raise ValueError("At least two surfaces are required to trace a ray.")

        traced_vectors = []
        rv = RayVector.from_ray(ray, surfaces[0])
        traced_vectors.append(rv)

        for i in range(1, len(surfaces)):
            prev_surface = surfaces[i - 1]
            curr_surface = surfaces[i]

            # Transfer through medium
            transfer = TransferMatrix.from_surface(prev_surface)
            rv = transfer @ rv

            # Refraction at curved surface
            refraction = RefractionMatrix.from_surfaces(prev_surface, curr_surface)
            rv = refraction @ rv

            traced_vectors.append(rv)

        return traced_vectors
