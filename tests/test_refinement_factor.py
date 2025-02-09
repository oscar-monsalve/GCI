from gci.model import representative_grid_size
from gci.model import refinement_factor


def test_2d_monotonic_convergence_refinement_factor():
    """Data from ASME's data https://doi.org/10.1115/1.2960953"""
    h1, h2, h3 = representative_grid_size(18000, 8000, 4500, 1/2)
    assert refinement_factor(h1, h2, h3) == (1.5, 1.3333333333333333)


def test_2d_low_p_refinement_factor():
    """Data from ASME's data https://doi.org/10.1115/1.2960953"""
    h1, h2, h3 = representative_grid_size(18000, 4500, 980, 1/2)
    assert refinement_factor(h1, h2, h3) == (2.0, 2.142857142857143)


