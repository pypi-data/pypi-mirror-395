# Geometric Unit conversions
# Ivan Markin 2022

from astropy import units as u, constants as const

class GU():
    def __init__(self, v):
        self.v = v*u.Msun
        self.Mass = self._to(u.g)
        self.Length = self._to(u.cm)
        self.Time = self._to(u.s)
        self.Energy = self.MLT(1, 2, -2)
        self.Luminosity = self.Energy/self.Time
        self.Density = self.MLT(1, -3, 0)
        self.Pressure = self.MLT(1, -1, -2)
        self.Frequency = self.MLT(0, 0, -1)
    def _to(self, unit):
        if unit.is_equivalent(u.Msun):
            return self.v.to(unit)
        if unit.is_equivalent(u.cm):
            return (self.v*const.G/const.c**2).to(unit)
        if unit.is_equivalent(u.s):
            return (self.v*const.G/const.c**3).to(unit)
    def MLT(self, m, l, t):
        return self.Mass**m * self.Length**l * self.Time**t
