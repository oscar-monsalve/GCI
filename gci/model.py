from logging import warning
from math import log, isinf


def physical_dimension_prompt() -> float:
    """Returns the numerical value of f (1, 1/2 or 1/3) prompting the user for the grid's dimensions."""
    while True:
        dimension = input("Type '1', '2' or '3' if your simulation is in one (1D), two (2D) or three (3D) dimensions, respectively: ")
        if dimension not in ("1", "2", "3"):
            print("Insert a valid argument for the dimensions of the problem. Enter either '1', '2' or '3'.\n")
            continue
        match dimension:
            case "1":
                return 1.0
            case "2":
                return 1.0/2
            case "3":
                return 1.0/3


def physical_dimension_no_prompt(dimension: str) -> float:
    """
    Returns the numerical value of f (1, 1/2 or 1/3) according to the manually-given grid's dimensions.

    Args:
    dimension: "2d" or "3d", according to the grid's dimensions.
    """
    if dimension not in ("1", "2", "3"):
        raise TypeError("Insert a valid argument for the dimensions of the problem. Enter either (2D, 2d), or (3D, 3d) as strings.\n")
    match dimension:
        case "1":
            return 1.0
        case "2":
            return 1.0/2
        case "3":
            return 1.0/3


def representative_grid_size(n1: int, n2: int, n3: int, f: float) -> [float, float, float]:
    """
    Returns three represetative grid sizes (h1, h2, h3), which must be h1 < h2 < h3.

    Args:
    n1, n2, n3: fine, medium and coarse grid cell counts, respectively.
    """
    h1 = (1 / n1) ** f
    h2 = (1 / n2) ** f
    h3 = (1 / n3) ** f
    return h1, h2, h3


def refinement_factor(h1: float, h2: float, h3: float) -> [float, float]:
    """
    Returns two grid refinement factors (r21, r32), which should be >1.3

    Args:
    h1, h2, h3: representative grid sizes that follow h1 < h2 < h3.
    """
    r21 = h2/h1
    r32 = h3/h2
    return r21, r32


def check_refinement_factor(r21: float, r32: float) -> None:
    if r21 <= 1.3:
        warning(f"It is recommended that the refinement factor r21={r21:.2f} is greater than 1.3.\n")
    elif r32 <= 1.3:
        warning(f"It is recommended that the refinement factor r32={r32:.2f} is greater than 1.3.\n")
    else:
        return


def sign(x: float) -> int:
    """
    Implemented manually the sign function to avoid importing numpy. Numpy was causing problems with pytest.
    """
    return (x > 0) - (x < 0)


def epsilon_and_sign_calculation(phi1: float, phi2: float, phi3: float) -> [float, float, float]:
    """
    Returns the difference of the CFD solutions between the medium-to-fine grid (ep21) and the coarse-to-medium grid
    (ep32), and the sign value "s".

    Args:
    phi1, phi2, phi3: fine, medium and coarse grid solutions, respectively.
    """
    ep21 = phi2-phi1
    ep32 = phi3-phi2
    s = 1*sign(ep32/ep21)
    return ep21, ep32, s


def check_convergence_condition(ep21: float, ep32: float) -> None:
    convergence_condition = ep21 / ep32

    # Monotonic convergence
    if convergence_condition > 0 and convergence_condition < 1:
        print("(OK) Monotonic convergence detected. The GCI results should be acceptable in terms of working intent.")
        # print("(OK) Monotonic convergence detected. The GCI procedure works best for this type of convergence condition.")
    # Oscillatory convergence
    elif convergence_condition > -1 and convergence_condition < 0:
        warning("Oscillatory convergence detected. For these cases, the GCI results might be fine, but sometimes it could increase the uncertainty of the results.")
        warning("If the GCI results are not satisfactory, it is recommended to remesh and aim for monotonic convergence.")
    # Monotonic divergence
    elif convergence_condition > 1:
        warning("Monotonic divergence detected. It is recommended to remesh and aim for a monotonic convergence solution.")
    # Oscillatory divergence
    elif convergence_condition < -1:
        warning("Oscillatory divergence detected. It is recommended to remesh and aim for a monotonic convergence solution.")


def fixed_point_iter(apparent_order_function, init_value: int, tol=1e-6, max_iter=100) -> [float, int]:
    """
    Performs a fixed-point iteration and returns its result and the iteration step if within specified tolerance and number of iterations.

    Args:
    aparent_order: function of interest to iterate over it. In this case is the aparent order function.
    init_value: starting point of the iteration process. For the aparent order function, "init_value" could be 1.
    tol, max_iter: stop criteria of the iteration process.
    """
    x = init_value
    for i in range(max_iter):
        x_next = apparent_order_function(x)
        if abs(x_next-x) < tol:
            return x_next, i
        x = x_next
    raise ValueError(f"Failed to converge after {max_iter} iterations")


def apparent_order_function(init_value: int, r21: float, r32: float, ep21: float, ep32: float, s: int) -> float:
    """
    Returns the aparent order p.

    Args:
    init_value: iteration variable obtained from the fixed-point iteration.
    r21, r32: grid refinement factors.
    ep21, ep32: medium-to-fine and coarse-to-medium grid solution differences, respectively.
    s: obtained from the sign function.
    """
    return (1/(log(r21))) * abs(log(abs(ep32/ep21)) + log(((r21**init_value)-s)/((r32**init_value)-s)))


def extrapolated_values(phi1: float, phi2: float, phi3: float, r21: float, r32: float, aparent_order: float) -> [float, float]:
    """
    Returns two extrapolated values (phi21_ext, phi32_ext) of the solutions.

    Args:
    phi1, phi2, phi3: fine, medium and coarse grid solutions, respectively.
    r21, r32: grid refinement factors.
    aparent_order: the aparent order of the grid solutions.
    """
    phi21_ext = (((r21**aparent_order)*phi1)-phi2)/((r21**aparent_order)-1)
    phi32_ext = (((r32**aparent_order)*phi2)-phi3)/((r32**aparent_order)-1)
    return phi21_ext, phi32_ext


def approximate_relative_errors(phi1: float, phi2: float, phi3: float) -> [float, float]:
    """
    Returns the approximate relative errors between the grid solutions given by the user.

    Args:
    phi1, phi2, phi3: fine, medium and coarse grid solutions, respectively.
    """
    e21_a = (abs((phi1-phi2)/phi1))*100
    e32_a = (abs((phi2-phi3)/phi2))*100
    return e21_a, e32_a


def extrapolated_relative_errors(phi1: float, phi2: float, phi21_ext: float, phi32_ext: float) -> [float, float]:
    """
    Returns two extrapolated relative errors between the computed extrapolated solutions.

    Args:
    phi1, phi2, phi3: fine, medium and coarse grid solutions, respectively.
    phi21_ext, phi32_ext: medium-to-fine, and coarse-to-medium extrapolated values of the solutions.
    """
    e21_ext = (((phi21_ext-phi1)/phi21_ext)) * 100
    e32_ext = (((phi32_ext-phi2)/phi32_ext)) * 100
    return e21_ext, e32_ext


def gci(r21: float, r32: float, e21_a: float, e32_a: float, aparent_order: float) -> [float, float]:
    """
    Returns the two GCI results for the fine (GCI21_fine) and medium (GCI32_medium) grids.

    Args:
    r21, r32: grid refinement factors.
    e21_a, e32_a: approximate relative errors.
    aparent_order: the aparent order of the grid solutions.
    """
    gci21_fine = ((1.25*e21_a)/((r21**aparent_order)-1))
    gci32_medium = ((1.25*e32_a)/((r32**aparent_order)-1))
    return gci21_fine, gci32_medium


def asymptotic_range(gci21_fine: float, gci32_medium: float, r21: float, aparent_order: float) -> float:
    return (r21 ** aparent_order) * (gci21_fine / gci32_medium)


def is_close(n1: float, n2: float, rel_tol=1e-10, abs_tol=0.0) -> bool:
    # check on the input tolerances
    if rel_tol < 0 or abs_tol < 0:
        raise ValueError("tolerances must be non-negative")
    # check for infinities
    if isinf(n1) or isinf(n2):
        return False
    # check for equality
    if n1 == n2:
        return True
    return abs(n1 - n2) <= max(rel_tol * max(abs(n1), abs(n2)), abs_tol)
