## geounit

`geounit` makes conversion of geometric units (G=c=1) easy and hassle-free. Geometric units are commonplace in numerical relativity and gravitational wave astrophysics.

At its core, `geounit` uses wonderful `astropy.units` package and operates with quantities with units.

### Installation

```python
pip install geounit
```

Currently implemented quantities:
 * Mass
 * Length
 * Time
 * Energy
 * Luminosity
 * Density
 * Pressure
 * Frequency

### Examples

For the total mass of M = 5Msun, calculate how much 12M is in ms:

```python
>>> import geounit
>>> M = 5
>>> gu = geounit.GU(M)
>>> 12 * gu.Time.to("ms")
<Quantity 0.29552946 ms>
>>> 12 * gu.Time.to("ms").value
np.float64(0.29552945685847604)
```

In units of one solar mass, there is a convinience variable:
```python
>>> from geounit import one as gu
>>> gu.Frequency.to("kHz")
<Quantity 203.02544673 kHz>
```

One can operate with fundamental mass-length-time (MLT) units:
```python
>>> import geounit
>>> energy = geounit.one.MLT(1, 2, -2) # mc**2
>>> energy.to("erg")
<Quantity 1.78709367e+54 erg>
```