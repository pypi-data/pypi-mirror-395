from tabulate import tabulate
from Optics.system import System
from aidkit.units.length_unit import LengthUnit

def print_layout(sys:System):
    headers = ["#", "Basic", "Type", "Radius (mm)", "Thickness (mm)", "Material", "Comment"]
    rows = []

    for surface in sys.lens.surfaces:
        rows.append([
            surface.base.name if surface.base else "—",
            surface.type.name,
            str(surface.radius),
            f"{surface.thickness.to(LengthUnit.MM):.2f}",
            surface.material.name if surface.material else "—",
            surface.comment
        ])

    print(tabulate(rows, headers=headers, tablefmt="grid"))