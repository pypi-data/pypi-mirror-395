import math
import numpy as np
from bokeh.io import output_notebook
from matterwave import plotting

import fftarray as fa

output_notebook(hide_banner=True)

def fa_array_assert_all_close(space: fa.Space, a: fa.Array, b: fa.Array):
    # Since we compare a real-valued and a complex-valued array, we have to give some absolute tolerance.
    # Otherwise the imaginary values which move slightly away from zero would make the comparison fail.
    np.testing.assert_allclose(a.values(space, xp=np), b.values(space, xp=np), atol=4e-15)

def gauss_pos(x, a, sigma):
    return (a * fa.exp(-(x**2/(2.* sigma**2))))/(math.sqrt(2 * np.pi) * sigma)

def gauss_freq(f, a, sigma):
    return (a * fa.exp(-(1/2)*(2*np.pi*f)**2*sigma**2))


dim = fa.dim_from_constraints("x",
        pos_middle=1.,
        pos_extent = 10.,
        freq_middle = 2.5/(2*np.pi),
        freq_extent = 20./(2*np.pi),
        loose_params=["pos_extent", "freq_extent"]
    )


x = fa.coords_from_dim(dim, "pos")
f = fa.coords_from_dim(dim, "freq")

plotting.plot_array(x)
plotting.plot_array(f)

