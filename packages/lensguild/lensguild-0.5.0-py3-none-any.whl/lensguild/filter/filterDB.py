from lensguild.filter import OpticalFilter
from lensguild.wavelength import Wavelength
from allytools.units.length import Length, LengthUnit

class CoatingDB:
    MgF2 = OpticalFilter(
        name="MgF₂ AR Coating",
        min_wavelength=Wavelength(Length(420, LengthUnit.NM)),
        max_wavelength=Wavelength(Length(700, LengthUnit.NM)),
        reflectance_curve=((Wavelength(Length(420, LengthUnit.NM)), 0.02),)
    )

    BBAR = OpticalFilter(
        name="BBAR Coating",
        min_wavelength=Wavelength(Length(420, LengthUnit.NM)),
        max_wavelength=Wavelength(Length(700, LengthUnit.NM)),
        reflectance_curve=((Wavelength(Length(420, LengthUnit.NM)), 0.0025),)
    )
    ALL = {
        "MgF2": MgF2,
        "BBAR": BBAR,
    }

    @staticmethod
    def get(name: str) -> Optional[OpticalFilter]:
        key = name.strip()
        # accept a couple of common variants
        aliases = {
            "MGF2": "MgF2",
            "MGF₂": "MgF2",
            "BBAR": "BBAR",
        }
        key_norm = aliases.get(key.upper(), key)
        return FilterDB.ALL.get(key_norm)