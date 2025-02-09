from gci.model import representative_grid_size
from gci.model import sign_calculation
from gci.model import refinement_factor
from gci.gci_no_prompt import fixed_point_iter, apparent_order_function


def test_2d_p_value_monotonic_convergence():
    h1, h2, h3 = representative_grid_size(18000, 8000, 4500, 1/2)
    ep21, ep32, s = sign_calculation(6.0630, 5.9720, 5.8630)
    r21, r32 = refinement_factor(h1, h2, h3)
    init_value = 1
    aparent_order, num_iterations = fixed_point_iter(apparent_order_function, init_value)
    assert aparent_order == 1.5339689568101367
