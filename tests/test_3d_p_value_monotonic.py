from gci.model import representative_grid_size, refinement_factor, sign_calculation
from gci.model import apparent_order_function, fixed_point_iter

h1, h2, h3 = representative_grid_size(2583006, 678911, 93188, 1/3)
r21, r32 = refinement_factor(h1, h2, h3)
ep21, ep32, s = sign_calculation(1.05100, 1.03460, 0.88580)
init_value = 1


def apparent_order_wrapper(x):
    return apparent_order_function(x, r21, r32, ep21, ep32, s)


def test_fixed_point_iter():
    result, iterations = fixed_point_iter(apparent_order_wrapper, init_value=1)
    assert isinstance(result, float)
    assert isinstance(iterations, int)
    assert iterations < 100


def test_2d_p_value_monotonic_convergence():
    aparent_order, num_iterations = fixed_point_iter(apparent_order_wrapper, init_value)
    assert aparent_order == 3.102008336139048
