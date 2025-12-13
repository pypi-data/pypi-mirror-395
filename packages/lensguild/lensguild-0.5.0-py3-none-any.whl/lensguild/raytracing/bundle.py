from typing import List, Iterable
from lensguild.raytracing.ray import Ray

class Bundle:
    """A simple container for a bundle of Ray objects."""

    def __init__(self, rays: Iterable[Ray] = ()):
        self._rays: List[Ray] = list(rays)

    def add(self, ray: Ray) -> None:
        """Add a single ray to the bundle."""
        self._rays.append(ray)

    def extend(self, rays: Iterable[Ray]) -> None:
        """Add multiple rays to the bundle."""
        self._rays.extend(rays)

    def __len__(self) -> int:
        return len(self._rays)

    def __getitem__(self, index: int) -> Ray:
        return self._rays[index]

    def __iter__(self):
        return iter(self._rays)

    def __repr__(self) -> str:
        return f"Bundle(N={len(self._rays)})"
