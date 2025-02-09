from gci.model import representative_grid_size


def test_2d_monotonic_convergence_grid_size_magnitudes():
    """Data from ASME's data https://doi.org/10.1115/1.2960953"""
    h1, h2, h3 = representative_grid_size(18000, 8000, 4500, 1/2)
    assert h1 < h2
    assert h2 < h3


def test_2d_monotonic_convergence_grid_size_h():
    """Data from ASME's data https://doi.org/10.1115/1.2960953"""
    assert representative_grid_size(18000, 8000, 4500, 1/2) == (0.007453559924999299, 0.011180339887498949, 0.014907119849998597)


def test_2d_low_p_grid_size_magnitudes():
    """Data from ASME's data https://doi.org/10.1115/1.2960953"""
    h1, h2, h3 = representative_grid_size(18000, 4500, 980, 1/2)
    assert h1 < h2
    assert h2 < h3


def test_2d_low_p_grid_size_h():
    """Data from ASME's data https://doi.org/10.1115/1.2960953"""
    assert representative_grid_size(18000, 4500, 980, 1/2) == (0.007453559924999299, 0.014907119849998597, 0.031943828249996996)


# -----------------------------------------


def test_grid_sizes_h_magnitude_3d():
    """Data from master thesis at https://repositorio.itm.edu.co/handle/20.500.12622/6477"""
    h1, h2, h3 = representative_grid_size(2583006, 678911, 93188, 1/3)
    assert h1 < h2
    assert h2 < h3


def test_grid_sizes_h_3d():
    """Data from master thesis at https://repositorio.itm.edu.co/handle/20.500.12622/6477"""
    assert representative_grid_size(2583006, 678911, 93188, 1/3) == (0.007288276857229988, 0.011377907137397423, 0.022057011502256973)
