from gci.model import representative_grid_size, refinement_factor, epsilon_and_sign_calculation
from gci.model import apparent_order_function, fixed_point_iter

h1, h2, h3 = representative_grid_size(18000, 4500, 980, 1/2)
r21, r32 = refinement_factor(h1, h2, h3)
ep21, ep32, s = epsilon_and_sign_calculation(10.7880, 10.7250, 10.6050)
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
    assert aparent_order == 0.7519005286525121
