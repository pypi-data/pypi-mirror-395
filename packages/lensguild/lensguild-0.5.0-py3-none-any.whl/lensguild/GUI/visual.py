from tabulate import tabulate
from RayTracing.tracing import ParaxialRayTracer
from RayTracing.ray import Ray
from RayTracing.point import Point
from RayTracing.direction import Direction
from GUI.print_layout import print_layout
from Optics.system import System


sys = System()  # ← instantiate or pass a real system
print_layout(sys)

initial_ray = Ray(point=Point(0, 1, 0), direction=Direction(paraxial_u=0.0), is_paraxial=True)

traced_rays = ParaxialRayTracer.trace_ray(initial_ray, sys.lens.surfaces)
table_rows = []
for surface, ray in zip(sys.lens.surfaces, traced_rays):
    table_rows.append([
        surface.base.name if surface.base else "—",
        surface.comment,
        f"{ray.y:.2f} mm",
        f"{ray.nu:.4f}",
        f"{surface.material.refractive_index.n:.5f}"
    ])

# --- Print table ---
headers = ["#", "plane", "Height y", "Angle un", "Ref.ind"]
print(tabulate(table_rows, headers=headers, tablefmt="grid"))
#draw_layout(sys, traced_rays)
#epp = compute_entrance_pupil_position(sys.lens.surfaces)
#print(f"\nEntrance Pupil Position: {epp}")