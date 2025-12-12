# snipbackground

A vectorized CPU implementation of the SNIP background subtraction algorithm for spectroscopy.

## Usage

```python
from snipbackground import snip_background

SNIPed, background = snip_background(repeat_energy, source_photons, m=30)

